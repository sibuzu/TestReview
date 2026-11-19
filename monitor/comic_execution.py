"""Explicit user scope controls also apply to ready or already attached drafts."""
import json
import hashlib
import re
from pathlib import Path


def _local_file(root, relative, directory):
    path = Path(relative)
    target = (root/path).resolve()
    if path.is_absolute() or not target.is_relative_to((root/directory).resolve()) or not target.is_file():
        raise ValueError('新來源授權檔案缺漏或越出指定目錄。')
    return target


def authorized_new_source(root, qid):
    """A frozen, acquired new source never grants permission to resume old work."""
    pointer = root/'monitor/new-source-authorization.json'
    if not pointer.exists():
        return False
    try:
        config = json.loads(pointer.read_text())
        if config.get('state') != 'active':
            return False
        scope_path = _local_file(root, config['scopePath'], 'docs/imports')
        if hashlib.sha256(scope_path.read_bytes()).hexdigest() != config['scopeSHA256']:
            raise ValueError('新來源凍結白名單雜湊不符。')
        scope = json.loads(scope_path.read_text())
        ids = scope['newQuestionIds']
        if not ids or len(ids) != len(set(ids)) or any(not re.fullmatch(r'q-[0-9]+', q) for q in ids):
            raise ValueError('新來源題號白名單無效。')
        baseline = scope['baselineQuestionIds']
        highest = max(int(q[2:]) for q in baseline)
        if (scope.get('kind') != 'explicit_new_source' or scope.get('authorizedBy') != 'user_add'
                or scope.get('sourceId') != config.get('sourceId') or scope.get('url') != config.get('url')
                or not re.fullmatch(r'src-more-[0-9]{3}', scope['sourceId'])
                or not re.fullmatch(r'https://chatgpt.com/share/[0-9a-f-]{36}', scope['url'])
                or scope['sourceId'] in scope['baselineSourceIds']
                or any(int(q[2:]) <= highest for q in ids)
                or scope.get('originalsVisualChecked') is not True
                or scope.get('crossSourceDuplicatesChecked') is not True):
            raise ValueError('新來源未完成原卷核對、查重或包含舊題號。')
        old_plan = root/'docs/comics/biology-rework-20261112/plan.json'
        if old_plan.exists():
            old_ids = {q for e in json.loads(old_plan.read_text()).get('entries', [])
                       for q in e.get('originalQuestionIds', [e['id']])}
            if old_ids.intersection(ids):
                raise ValueError('新來源授權不得包含舊重製題。')
        if qid not in ids:
            return False
        progress_path = _local_file(root, config['progressPath'], 'docs/imports')
        progress = json.loads(progress_path.read_text())
        completed = progress.get('completedQuestionIds', [])
        awaiting = progress.get('awaitingConfirmationQuestionIds', [])
        if (progress.get('state') != 'active' or progress.get('sourceId') != scope['sourceId']
                or not set(completed) <= set(ids) or len(completed) != len(set(completed))
                or not set(awaiting) <= set(ids) or len(awaiting) != len(set(awaiting))
                or set(completed).intersection(awaiting)
                or qid in completed or qid in awaiting or len(completed)+len(awaiting) == len(ids)):
            raise ValueError('新來源本題已完成或授權已停止。')
        acquisition_directory = ('docs/acquisition' if str(scope['acquisitionPath']).startswith('docs/acquisition/')
                                 else str(scope_path.parent.relative_to(root)))
        acquisition_path = _local_file(root, scope['acquisitionPath'], acquisition_directory)
        if hashlib.sha256(acquisition_path.read_bytes()).hexdigest() != scope['acquisitionSHA256']:
            raise ValueError('新來源原卷取得紀錄雜湊不符。')
        acquisition = json.loads(acquisition_path.read_text())
        images = acquisition['downloadedImages']
        if (acquisition.get('state') != 'acquired' or acquisition.get('sourceId') != scope['sourceId']
                or acquisition.get('url') != scope['url'] or not images
                or len(images) != acquisition['imagesExpected']):
            raise ValueError('新來源原卷尚未全部取得。')
        paths = [i['path'] for i in images]
        if len(paths) != len(set(paths)):
            raise ValueError('新來源原卷清單重複。')
        for image in images:
            path = _local_file(root, image['path'], 'docs/source-pages')
            if (image.get('decoded') is not True or image.get('archiveSizeMatched') is not True
                    or min(image.get('width', 0), image.get('height', 0)) <= 0
                    or path.stat().st_size != image['bytes']
                    or hashlib.sha256(path.read_bytes()).hexdigest() != image['sha256']):
                raise ValueError('新來源原圖缺漏或大小、雜湊、解碼驗證不符。')
        return True
    except (KeyError, TypeError, OSError, json.JSONDecodeError) as error:
        raise ValueError('新來源授權證據不完整；維持停止。') from error


def authorized_question_update(root, qid):
    """A user update unlocks only its existing questions, without resuming a queue."""
    pointer = root/'monitor/question-update-authorization.json'
    if not pointer.exists():
        return False
    try:
        config = json.loads(pointer.read_text())
        if config.get('state') != 'active':
            return False
        scope_path = _local_file(root, config['scopePath'], 'docs/imports')
        if hashlib.sha256(scope_path.read_bytes()).hexdigest() != config['scopeSHA256']:
            raise ValueError('題目更新白名單雜湊不符。')
        scope = json.loads(scope_path.read_text())
        ids = scope['questionIds']
        if (not 1 <= len(ids) <= 2 or len(ids) != len(set(ids))
                or any(not re.fullmatch(r'q-[0-9]+', q) for q in ids)
                or scope.get('kind') != 'explicit_question_update'
                or scope.get('authorizedBy') not in ('user_update', 'monitor_confirmation')
                or scope.get('sourceId') != config.get('sourceId')
                or scope.get('url') != config.get('url')
                or not re.fullmatch(r'https://chatgpt.com/share/[0-9a-f-]{36}', scope['url'])
                or scope.get('originalsVisualChecked') is not True
                or scope.get('existingQuestionIdentityChecked') is not True
                or scope.get('noNewQuestions') is not True):
            raise ValueError('題目更新僅限已核對的至多兩題，不得恢復舊佇列。')
        if qid not in ids:
            return False
        baseline = scope['baselineQuestions']
        questions = json.loads((root/'site/dist/data.json').read_text())['questions']
        existing = {q['id']: q for parent in questions for q in (parent.get('groupQuestions') or [parent])}
        if (set(baseline) != set(ids) or any(q not in existing for q in ids)
                or any(baseline[q] != {k: existing[q][k] for k in ('id', 'sourceId', 'date')}
                       or baseline[q]['sourceId'] != scope['sourceId'] for q in ids)):
            raise ValueError('題目更新不得新增題號或改變既有來源、日期。')
        if scope['authorizedBy'] == 'monitor_confirmation':
            evidence = scope['confirmationEvidence']
            resolved = json.loads((root/'monitor/confirmations.json').read_text()).get('resolved', [])
            if len(evidence) != len(ids) or {e['questionId'] for e in evidence} != set(ids):
                raise ValueError('監看確認更新須逐題具備原確認紀錄。')
            for item in evidence:
                record = next((r for r in resolved if r['id'] == item['requestId']), None)
                if (not record or record.get('state') != 'resolved'
                        or (record.get('questionId') or record['id']) != item['questionId']
                        or hashlib.sha256(json.dumps(record, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
                        != item['snapshotSHA256']):
                    raise ValueError('監看確認紀錄缺漏或已變更，維持停止。')
        progress = json.loads(_local_file(root, config['progressPath'], str(scope_path.parent.relative_to(root))).read_text())
        completed = progress['completedQuestionIds']
        if (progress.get('state') != 'active' or progress.get('sourceId') != scope['sourceId']
                or len(completed) != len(set(completed)) or not set(completed) <= set(ids)
                or qid in completed or len(completed) == len(ids)):
            raise ValueError('題目更新本題已完成或授權已停止。')
        acquisition_path = _local_file(root, scope['acquisitionPath'], str(scope_path.parent.relative_to(root)))
        if hashlib.sha256(acquisition_path.read_bytes()).hexdigest() != scope['acquisitionSHA256']:
            raise ValueError('題目更新原卷紀錄雜湊不符。')
        acquisition = json.loads(acquisition_path.read_text())
        images = acquisition['downloadedImages']
        if (acquisition.get('state') != 'acquired' or acquisition.get('sourceId') != scope['sourceId']
                or acquisition.get('url') != scope['url'] or not images
                or len(images) != acquisition['imagesExpected']
                or len(images) != scope['expectedOriginalImages']
                or len({i['path'] for i in images}) != len(images)):
            raise ValueError('題目更新原卷尚未完整取得。')
        for image in images:
            path = _local_file(root, image['path'], 'docs/source-pages')
            if (image.get('decoded') is not True or image.get('archiveSizeMatched') is not True
                    or min(image.get('width', 0), image.get('height', 0)) <= 0
                    or path.stat().st_size != image['bytes']
                    or hashlib.sha256(path.read_bytes()).hexdigest() != image['sha256']):
                raise ValueError('題目更新原圖缺漏或驗證不符。')
        return True
    except (KeyError, TypeError, OSError, json.JSONDecodeError) as error:
        raise ValueError('題目更新授權證據不完整；維持停止。') from error


def assert_limited_biology_allowed(root, control, qid):
    """The frozen batch, rather than a general biology flag, grants permission."""
    relative = Path(control.get('limitedBatch', ''))
    path = (root/relative).resolve()
    if (relative.is_absolute() or not path.is_relative_to((root/'docs/comics').resolve())
            or not path.is_file()):
        raise ValueError('生物限量批次白名單缺漏；不得繼續領題或整合。')
    batch = json.loads(path.read_text())
    ids = batch.get('questionIds', [])
    active = control.get('activeOriginalQuestionIds', [])
    completed = batch.get('completedQuestionIds', [])
    if (batch.get('limit') != 10 or len(ids) != 10 or len(set(ids)) != 10
            or set(active) != set(ids) or len(active) != 10
            or len(completed) != len(set(completed)) or not set(completed) <= set(ids)):
        raise ValueError('生物限量批次白名單不一致；只授權凍結的10題。')
    if (batch.get('state') != 'active' or control.get('biologyQualityUpgrade') != 'active'
            or len(completed) >= batch['limit']
            or control.get('remainingActiveOriginalQuestions', 10) <= 0):
        raise ValueError('生物限量批次已停止；不得續作第11題或重新整合。')
    if qid not in ids or qid in completed:
        raise ValueError(f'{qid}: 不在本批尚未完成的10題白名單；其他重製維持暫停。')


def assert_work_allowed(root, qid):
    if authorized_question_update(root, qid):
        return
    if authorized_new_source(root, qid):
        return
    path = root/'docs/comics/biology-rework-20261112/plan.json'
    if not path.exists():
        return
    plan = json.loads(path.read_text())
    control = plan.get('executionControl', {})
    if control.get('mode') == 'biology_limited':
        assert_limited_biology_allowed(root, control, qid)
        return
    if control.get('mode') != 'missing_only':
        return
    for entry in plan.get('entries', []):
        if qid in entry.get('originalQuestionIds', [entry['id']]):
            if 'missing_illustration' not in entry.get('reasons', []):
                raise ValueError(f'{qid}: 使用者已暫停重製；保留草稿，不續製作、驗收或整合。')
            return
