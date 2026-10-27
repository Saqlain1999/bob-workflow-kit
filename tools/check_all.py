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
    tests = [sys.executable, '-B', '-W', 'error::ResourceWarning',
             str(root / 'tools/run_component_tests.py')]
    provenance = [sys.executable, '-B', str(root / 'tools/verify_consolidation.py')]
    if require_history:
        provenance.append('--require-history')
    return [
        {'name': 'installer', 'cwd': root, 'command': tests + ['installer']},
        {'name': 'evaluator', 'cwd': root / 'evals', 'command': tests + ['evaluator']},
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
        command = list(check['command'])
        evidence_path = None
        if check['name'] in ('installer', 'evaluator'):
            evidence_path = log_dir / (check['name'] + '-tests.json')
            command.extend(['--report', str(evidence_path)])
        with (log_dir / (check['name'] + '.log')).open('w', encoding='utf-8') as log:
            try:
                result = subprocess.run(command, cwd=check['cwd'],
                                        env=test_environment(os.environ), stdout=log,
                                        stderr=subprocess.STDOUT, timeout=180)
                code = result.returncode
            except (OSError, subprocess.TimeoutExpired) as exc:
                log.write(str(exc) + '\n')
                code = 1
        row = {'name': check['name'], 'exit_code': code}
        if evidence_path is not None:
            try:
                evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
                if not isinstance(evidence, dict):
                    raise ValueError('test evidence must be an object')
                row['tests'] = evidence
                if not evidence.get('all_successful') and code == 0:
                    code = 1
            except (OSError, ValueError) as exc:
                row['evidence_error'] = str(exc)
                if code == 0:
                    code = 1
            row['exit_code'] = code
        results.append(row)
        print(check['name'] + ': ' + ('PASS' if code == 0 else 'FAIL'), flush=True)
    report = {'checks': results, 'log_dir': str(log_dir),
              'all_successful': all(row['exit_code'] == 0 for row in results)}
    (log_dir / 'summary.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0 if report['all_successful'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
