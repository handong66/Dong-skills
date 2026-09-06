#!/usr/bin/env python3
"""Compare skill trees without modifying either side or following symlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


def safe_root(value):
    path = Path(os.path.abspath(value))
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f'symlink in root path: {part}')
    return path


def inventory(root):
    if root.is_symlink():
        return {'.': {'kind': 'unsupported'}}
    if not root.exists():
        return {}
    if not root.is_dir():
        return {'.': {'kind': 'unsupported'}}
    result = {'.': {'kind': 'directory'}}

    def walk(directory):
        with os.scandir(directory) as entries:
            for entry in sorted(entries, key=lambda item: item.name):
                key = str(Path(entry.path).relative_to(root))
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    result[key] = {'kind': 'directory'}
                    walk(entry.path)
                elif stat.S_ISREG(mode):
                    fd = os.open(entry.path, os.O_RDONLY | os.O_NOFOLLOW)
                    with os.fdopen(fd, 'rb') as stream:
                        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                    result[key] = {'kind': 'file', 'sha256': digest}
                else:
                    result[key] = {'kind': 'unsupported'}
    walk(root)
    return result


def compare(source, installed):
    left, right = inventory(source), inventory(installed)
    rows = []
    for key in sorted(left.keys() | right.keys()):
        a, b = left.get(key), right.get(key)
        if any(item and item['kind'] == 'unsupported' for item in (a, b)):
            status = 'unsupported'
        elif a is None:
            status = 'extra'
        elif b is None:
            status = 'missing'
        else:
            status = 'matching' if a == b else 'stale'
        rows.append({'path': key, 'status': status, 'source': a, 'installed': b})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, help='source skills root')
    parser.add_argument('--installed', required=True, help='installed skills root')
    parser.add_argument('--skill', action='append', help='select a skill; repeatable')
    args = parser.parse_args()
    try:
        source, installed = safe_root(args.source), safe_root(args.installed)
        if not source.is_dir():
            raise ValueError('source must be an existing directory')
        if installed.exists() and not installed.is_dir():
            raise ValueError('installed root must be a directory or absent')
        names = args.skill or sorted(p.name for p in source.iterdir() if p.is_dir() and not p.is_symlink())
        if not names:
            raise ValueError('no source skills selected')
        report = []
        for name in names:
            if name in ('.', '..') or Path(name).name != name or '/' in name or '\\' in name:
                raise ValueError(f'invalid skill name: {name}')
            origin = source / name
            if origin.is_symlink() or not origin.is_dir() or not (origin / 'SKILL.md').is_file() or (origin / 'SKILL.md').is_symlink():
                raise ValueError(f'source skill requires a regular SKILL.md: {name}')
            rows = compare(origin, installed / name)
            report.append({'skill': name, 'matching': all(r['status'] == 'matching' for r in rows), 'entries': rows})
        print(json.dumps({'readOnly': True, 'skills': report}, indent=2))
        return 0 if all(item['matching'] for item in report) else 1
    except (OSError, ValueError) as error:
        print(json.dumps({'readOnly': True, 'error': str(error)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
