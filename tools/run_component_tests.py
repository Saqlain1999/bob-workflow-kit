#!/usr/bin/env python3
"""Run unittest discovery, requiring nonempty mandatory component modules."""
import argparse
import json
from pathlib import Path
import sys
import unittest

REQUIRED_MODULES = {
    'installer': ('test_installer', 'test_consolidation'),
    'evaluator': ('test_evaluate', 'test_parcel_resume'),
}


def cases(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from cases(item)
        else:
            yield item


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('component', choices=REQUIRED_MODULES)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    required = dict.fromkeys(REQUIRED_MODULES[args.component], 0)
    report = {'required_modules': required, 'tests_discovered': 0, 'tests_run': 0,
              'all_successful': False}
    try:
        # Match `python -m unittest`: component-local imports start at its cwd.
        sys.path.insert(0, str(Path.cwd()))
        loader = unittest.TestLoader()
        suite = loader.discover('tests')
        for test in cases(suite):
            report['tests_discovered'] += 1
            module = type(test).__module__
            if module in required:
                required[module] += 1
        missing = [name for name, count in required.items() if count == 0]
        if missing:
            report['discovery_error'] = 'Missing or empty required suites: ' + ', '.join(missing)
        elif loader.errors:
            report['discovery_error'] = '\n'.join(loader.errors)
        else:
            result = unittest.TextTestRunner(verbosity=2).run(suite)
            report.update(tests_run=result.testsRun, failures=len(result.failures),
                          errors=len(result.errors), skipped=len(result.skipped),
                          all_successful=result.wasSuccessful() and result.testsRun > 0)
    except Exception as exc:
        report['discovery_error'] = str(exc)
    print(json.dumps(report, indent=2), flush=True)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return 0 if report['all_successful'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
