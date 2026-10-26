#!/usr/bin/env python3
"""Verify preserved source bytes/history or local Markdown links; no network."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def verify_files(root, manifest):
    errors = []
    root = root.resolve()
    for source in manifest['sources']:
        for entry in source['files']:
            name = entry['destination']
            relative = PurePosixPath(name)
            if relative.is_absolute() or '..' in relative.parts or '\\' in name:
                errors.append('Unsafe destination: ' + name)
                continue
            path = root.joinpath(*relative.parts).resolve()
            if root not in path.parents:
                errors.append('Destination escapes checkout: ' + name)
            elif not path.is_file():
                errors.append('Missing imported file: ' + name)
            elif hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
                errors.append('Imported file changed: ' + name)
    return errors


def verify_history(root, manifest, required):
    try:
        top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root,
                             capture_output=True, text=True, check=True).stdout.strip()
        if Path(top).resolve() != root.resolve():
            raise ValueError('checkout is not a Git root')
    except (OSError, subprocess.CalledProcessError, ValueError):
        return (['Original Git history required but unavailable'] if required else [],
                'not checked: no Git checkout (content verification only)')
    commits = [manifest['kit_base']] + [source['source_commit'] for source in manifest['sources']]
    errors = []
    for commit in commits:
        if not re.fullmatch('[0-9a-f]{40}', commit):
            errors.append('Invalid source commit identifier')
            continue
        result = subprocess.run(['git', 'merge-base', '--is-ancestor', commit, 'HEAD'],
                                cwd=root, capture_output=True)
        if result.returncode:
            errors.append('Missing original source ancestry: ' + commit)
    return errors, 'failed' if errors else 'all original source heads are ancestors'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--links', action='store_true')
    parser.add_argument('--require-history', action='store_true')
    args = parser.parse_args()
    if args.links:
        path = ROOT / 'docs/resources/catalogue/tools/validate_catalog.py'
        spec = importlib.util.spec_from_file_location('catalogue_validator', path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        errors, files, links = module.validate_markdown(ROOT)
        report = {'markdown_files': files, 'local_links': links, 'errors': errors}
    else:
        manifest = json.loads((ROOT / 'docs/consolidation/source-map.json').read_text(encoding='utf-8'))
        errors = verify_files(ROOT, manifest)
        history_errors, history = verify_history(ROOT, manifest, args.require_history)
        errors.extend(history_errors)
        report = {'source_repositories': len(manifest['sources']) + 1,
                  'imported_files': sum(len(source['files']) for source in manifest['sources']),
                  'history': history, 'errors': errors}
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
