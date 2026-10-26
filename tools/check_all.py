#!/usr/bin/env python3
"""Run the offline component suites, without Bob, provider keys or network calls."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def test_environment(source):
    allowed = {'PATH', 'HOME', 'USERPROFILE', 'SYSTEMROOT', 'SystemRoot', 'WINDIR',
               'COMSPEC', 'PATHEXT', 'TMP', 'TEMP', 'TMPDIR', 'LANG', 'LC_ALL',
               'LOCALAPPDATA', 'APPDATA'}
    env = {key: value for key, value in source.items() if key in allowed}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONUTF8'] = '1'
    return env


def checks(root, require_history=False):
    tests = [sys.executable, '-B', '-W', 'error::ResourceWarning', '-m', 'unittest',
             'discover', '-s', 'tests', '-v']
    provenance = [sys.executable, '-B', str(root / 'tools/verify_consolidation.py')]
    if require_history:
        provenance.append('--require-history')
    return [
        {'name': 'installer', 'cwd': root, 'command': tests},
        {'name': 'evaluator', 'cwd': root / 'evals', 'command': tests},
        {'name': 'catalogue', 'cwd': root / 'docs/resources/catalogue',
         'command': [sys.executable, '-B', 'tools/validate_catalog.py']},
        {'name': 'provenance', 'cwd': root, 'command': provenance},
        {'name': 'links', 'cwd': root,
         'command': [sys.executable, '-B', str(root / 'tools/verify_consolidation.py'), '--links']},
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='show commands without running them')
    parser.add_argument('--require-history', action='store_true', help='also require original Git ancestry')
    parser.add_argument('--log-dir', type=Path, help='new directory for logs; never overwrite an existing directory')
    args = parser.parse_args()
    suite = checks(ROOT, args.require_history)
    if args.list:
        print(json.dumps(suite, indent=2, default=str))
        return 0
    if args.log_dir:
        log_dir = args.log_dir.resolve()
        log_dir.mkdir(parents=True, exist_ok=False)
    else:
        log_dir = Path(tempfile.mkdtemp(prefix='bob-kit-checks-'))
    results = []
    for check in suite:
        with (log_dir / (check['name'] + '.log')).open('w', encoding='utf-8') as log:
            try:
                result = subprocess.run(check['command'], cwd=check['cwd'],
                                        env=test_environment(os.environ), stdout=log,
                                        stderr=subprocess.STDOUT, timeout=180)
                code = result.returncode
            except (OSError, subprocess.TimeoutExpired) as exc:
                log.write(str(exc) + '\n')
                code = 1
        results.append({'name': check['name'], 'exit_code': code})
        print(check['name'] + ': ' + ('PASS' if code == 0 else 'FAIL'), flush=True)
    report = {'checks': results, 'log_dir': str(log_dir),
              'all_successful': all(row['exit_code'] == 0 for row in results)}
    (log_dir / 'summary.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0 if report['all_successful'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
