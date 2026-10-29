"""Collect the user's ten-image timing sample after actual visual completion."""
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

def record(qid):
    batch_path = ROOT/'docs/comics/speed-comparison.json'
    batch = json.loads(batch_path.read_text())
    timing_path = ROOT/'docs/comics/generation-times'/f'{qid}.json'
    if not timing_path.exists():
        return  # SVGs and reused art do not count as a generated illustration.
    progress = json.loads((ROOT/'docs/comics/progress.json').read_text())
    entry = next(e for e in progress['entries'] if e['id'] == qid)
    if entry['state'] != 'complete' or not entry.get('visualChecked'):
        raise ValueError('Only visually completed illustrations enter the sample.')
    timing = json.loads(timing_path.read_text())
    assert timing['attempts'] and all(a['seconds'] >= 0 for a in timing['attempts'])
    sample = dict(timing, completedAt=entry['completedAt'],
                  totalGenerationSeconds=sum(a['seconds'] for a in timing['attempts']))
    sample['workSeconds'] = (datetime.fromisoformat(entry['completedAt']) -
                             datetime.fromisoformat(timing['workStartedAt'])).total_seconds()
    index = next((i for i,s in enumerate(batch['samples']) if s['id']==qid), None)
    if index is None:
        if len(batch['samples']) >= batch['target']:
            return
        batch['samples'].append(sample)
    else:
        batch['samples'][index] = sample
    batch['updatedAt'] = datetime.now(timezone.utc).isoformat()
    if len(batch['samples']) == batch['target']:
        n = batch['target']
        generation = sum(s['totalGenerationSeconds'] for s in batch['samples'])/n
        work = sum(s['workSeconds'] for s in batch['samples'])/n
        first = min(datetime.fromisoformat(s['workStartedAt']) for s in batch['samples'])
        last = max(datetime.fromisoformat(s['completedAt']) for s in batch['samples'])
        cycle = (last-first).total_seconds()/n
        baseline = batch['baseline']['averageSecondsPerWork']
        change = 100*(cycle/baseline-1)
        batch.update(state='complete', completedAt=batch['updatedAt'],
                     averageGenerationSeconds=generation, averageWorkSeconds=work,
                     averageCompletionCycleSeconds=cycle,
                     elapsedWindowSeconds=(last-first).total_seconds(),
                     workChangePercent=change,
                     summary=f'速度比較：10張平均產圖{generation:.1f}秒；整段完成週期平均{cycle/60:.2f}分鐘（含核對排版及穿插處理其他題）。前50份平均{baseline/60:.2f}分鐘，差異{change:+.1f}%。前批未記純產圖秒數且圖文種類不同，不能據此斷言模式的純產圖速度差。')
    batch_path.write_text(json.dumps(batch, ensure_ascii=False, indent=2)+'\n')
    print(f'Timing sample: {len(batch["samples"])}/{batch["target"]}')

if __name__ == '__main__':
    record(sys.argv[1])
