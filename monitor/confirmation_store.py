"""Serialize confirmation updates from the monitor and curation scripts."""
from contextlib import contextmanager
import fcntl
import json
import os
import tempfile


@contextmanager
def edit_confirmations(root):
    path = root/'monitor/confirmations.json'
    lock = root/'.cache/monitor-confirmations.lock'
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        records = json.loads(path.read_text(encoding='utf-8'))
        yield records
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                             prefix='.confirmations-', delete=False) as output:
                temporary = output.name
                json.dump(records, output, ensure_ascii=False, indent=2)
                output.write('\n')
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, path)
        finally:
            if temporary and os.path.exists(temporary):
                os.unlink(temporary)
