#!/usr/bin/env python3
"""Verify preserved source bytes/history or local Markdown links; no network."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import TypeGuard

ROOT = Path(__file__).resolve().parents[1]

# Reviewed import identities are code-level trust anchors, not manifest claims.
# Updating an origin is an explicit reviewed source change, never a map refresh.
KIT_BASE_ANCHOR = 'c09f0c9b22521d3b48db1a645ba54d93484be77f'
REVIEWED_FORK_DIGEST = '1a7355aa8ca937f9cf488cd3869512db75c0d1de1cdd35cd1784e7e5018aadb6'
SOURCE_ANCHORS = {
    'Saqlain1999/bob-workflow-evals':
        ('5e2075ab510d947675c3e2e824ff384de899dc1a', 'evals'),
    'Saqlain1999/awesome-bob-workflows':
        ('e64911f216f700106dae66f4193ec2f400d7e2bd', 'docs/resources/catalogue'),
    'Saqlain1999/bob-workflow-runner':
        ('e03c17c436c8891415c533fad3b132f08c783184', 'docs/design/runner'),
}


def safe_path(name) -> TypeGuard[str]:
    """Require a canonical relative POSIX path, not a normalized unsafe alias."""
    return (isinstance(name, str) and bool(name) and '\\' not in name
            and ':' not in name and not any(ord(char) < 32 for char in name)
            and not PurePosixPath(name).is_absolute()
            and all(part not in ('', '.', '..') and part.casefold() != '.git'
                    for part in name.split('/')))


def verify_files(root, manifest):
    """Small byte-check helper; full provenance validation is verify_history's job."""
    errors = []
    root = root.resolve()
    for source in manifest['sources']:
        for entry in source['files']:
            name = entry['destination']
            if not safe_path(name):
                errors.append('Unsafe destination: ' + str(name))
                continue
            try:
                path = root.joinpath(*PurePosixPath(name).parts).resolve()
                if root not in path.parents:
                    errors.append('Destination escapes checkout: ' + name)
                elif not path.is_file():
                    errors.append('Missing imported file: ' + name)
                elif hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
                    errors.append('Imported file changed: ' + name)
            except (OSError, RuntimeError) as exc:
                errors.append('Cannot read imported file ' + name + ': ' + str(exc))
    return errors


def identifier(value, length):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{' + str(length) + '}', value) is not None


def validate_manifest(manifest):
    """Validate shape and mapping before any Git or destination-file operations."""
    if not isinstance(manifest, dict):
        return ['Manifest must be an object']
    errors = []
    if type(manifest.get('schema_version')) is not int or manifest['schema_version'] != 1:
        errors.append('Unsupported manifest schema_version')
    if not identifier(manifest.get('kit_base'), 40):
        errors.append('Invalid kit base commit identifier')
    sources = manifest.get('sources')
    if not isinstance(sources, list) or not sources:
        return errors + ['Manifest sources must be a nonempty list']
    destinations = set()
    prefixes = set()
    for index, source in enumerate(sources):
        label = 'Source ' + str(index)
        if not isinstance(source, dict):
            errors.append(label + ' must be an object')
            continue
        if not isinstance(source.get('repository'), str) or not source['repository'].strip():
            errors.append(label + ' repository must be a nonempty string')
        if not identifier(source.get('source_commit'), 40):
            errors.append(label + ' has invalid source commit identifier')
        prefix = source.get('prefix')
        if not safe_path(prefix):
            errors.append(label + ' has unsafe prefix')
        elif prefix in prefixes:
            errors.append('Duplicate source prefix: ' + prefix)
        else:
            prefixes.add(prefix)
        files = source.get('files')
        if not isinstance(files, list) or not files:
            errors.append(label + ' files must be a nonempty list')
            continue
        source_paths = set()
        for entry in files:
            if not isinstance(entry, dict):
                errors.append(label + ' file entry must be an object')
                continue
            source_path = entry.get('source_path')
            destination = entry.get('destination')
            if not safe_path(source_path):
                errors.append(label + ' has unsafe source path')
            elif source_path in source_paths:
                errors.append(label + ' duplicate source path: ' + source_path)
            else:
                source_paths.add(source_path)
            if not safe_path(destination):
                errors.append(label + ' has unsafe destination')
            elif destination in destinations:
                errors.append('Duplicate destination: ' + destination)
            else:
                destinations.add(destination)
            if (safe_path(prefix) and safe_path(source_path)
                    and destination != prefix + '/' + source_path):
                errors.append(label + ' destination does not match prefix/source_path')
            if not identifier(entry.get('sha256'), 64):
                errors.append(label + ' has invalid SHA256')
            if not identifier(entry.get('git_blob'), 40):
                errors.append(label + ' has invalid Git blob identifier')
            # This import format preserves regular files, not symlinks or submodules.
            if entry.get('source_mode') not in ('100644', '100755'):
                errors.append(label + ' has unsupported source mode')
    return errors


def git(root, *args):
    # Replacement refs must not redefine the original commit/blob contents.
    return subprocess.run(['git', '--no-replace-objects', *args], cwd=root,
                          capture_output=True, check=True).stdout


def verify_history(root, manifest, required):
    """Bind the complete manifest to original Git trees/blobs, then check ancestry."""
    errors = validate_manifest(manifest)
    if errors:
        return errors, 'failed: invalid manifest'
    declared = {source['repository']: (source['source_commit'], source['prefix'])
                for source in manifest['sources']}
    if (manifest['kit_base'] != KIT_BASE_ANCHOR
            or len(declared) != len(manifest['sources'])
            or declared != SOURCE_ANCHORS):
        return ['Manifest source roster/identities differ from reviewed import anchors'], 'failed: import identity mismatch'
    try:
        top = git(root, 'rev-parse', '--show-toplevel').decode().strip()
        available = Path(top).resolve() == root.resolve()
    except (OSError, subprocess.CalledProcessError, UnicodeError):
        available = False
    if not available:
        return (['Original Git history required but unavailable'] if required else [],
                'not checked: bundled manifest only; original Git inventories and blobs unverified')
    commits = [manifest['kit_base']] + [source['source_commit'] for source in manifest['sources']]
    for commit in commits:
        try:
            git(root, 'merge-base', '--is-ancestor', commit, 'HEAD')
        except (OSError, subprocess.CalledProcessError) as exc:
            errors.append('Missing original source ancestry: ' + commit + ' (' + str(exc) + ')')
    for source in manifest['sources']:
        label = source['repository']
        try:
            records = git(root, 'ls-tree', '-r', '-z', '--full-tree', source['source_commit'])
            inventory = {}
            for record in records.split(b'\0'):
                if not record:
                    continue
                metadata, name = record.split(b'\t', 1)
                mode, kind, blob = metadata.decode('ascii').split()
                name = name.decode('utf-8')
                if kind != 'blob' or mode not in ('100644', '100755'):
                    raise ValueError('unsupported Git tree entry: ' + name)
                if name in inventory:
                    raise ValueError('duplicate Git tree entry: ' + name)
                inventory[name] = (mode, blob)
            expected = {entry['source_path']: (entry['source_mode'], entry['git_blob'])
                        for entry in source['files']}
            if inventory != expected:
                errors.append('Original Git inventory mismatch: ' + label)
                continue
            for entry in source['files']:
                data = git(root, 'cat-file', 'blob', entry['git_blob'])
                if hashlib.sha256(data).hexdigest() != entry['sha256']:
                    errors.append('SHA256 does not match original Git blob: '
                                  + label + ':' + entry['source_path'])
        except (OSError, subprocess.CalledProcessError, ValueError, UnicodeError) as exc:
            errors.append('Cannot verify original Git inventory/blobs: ' + label + ' (' + str(exc) + ')')
    return errors, ('failed' if errors else
                    'all original source heads are ancestors; complete inventories and blob SHA256s verified')


def verify_reviewed_fork(root):
    """Verify an explicit active-code fork without rewriting original provenance."""
    report = {}
    try:
        raw = (root / 'docs/consolidation/reviewed-evals-fork.json').read_bytes()
        if hashlib.sha256(raw).hexdigest() != REVIEWED_FORK_DIGEST:
            return ['Reviewed fork map differs from its trusted code-level digest'], report
        fork = json.loads(raw)
        prefix = fork['prefix']
        if prefix != 'evals' or not identifier(fork['reviewed_commit'], 40) or not fork['files']:
            return ['Invalid reviewed fork identity/inventory'], report
        report.update(prefix=prefix, reviewed_commit=fork['reviewed_commit'],
                      reviewed_files=len(fork['files']))
        try:
            available = Path(git(root, 'rev-parse', '--show-toplevel').decode().strip()).resolve() == root.resolve()
        except (OSError, subprocess.CalledProcessError, UnicodeError):
            available = False
        errors = []
        if available:
            git(root, 'merge-base', '--is-ancestor', fork['reviewed_commit'], 'HEAD')
            expected = {entry['destination']: (entry['mode'], entry['git_blob'])
                        for entry in fork['files']}
            for revision in (fork['reviewed_commit'], 'HEAD'):
                inventory = {}
                for record in git(root, 'ls-tree', '-r', '-z', revision, '--', prefix).split(b'\0'):
                    if not record:
                        continue
                    metadata, name = record.split(b'\t', 1)
                    mode, kind, blob = metadata.decode().split()
                    if kind != 'blob':
                        raise ValueError('unsupported reviewed fork entry')
                    inventory[name.decode()] = (mode, blob)
                if inventory != expected:
                    errors.append('Reviewed fork complete Git inventory mismatch: ' + revision)
            report['history'] = 'recorded fork ancestry and complete active Git tree checked'
        else:
            report['history'] = 'unverified: bundled fork map consistency only, no Git history proof'
        errors.extend(verify_files(root, {'sources': [{'files': fork['files']}]}))
        return errors, report
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        return ['Cannot verify reviewed fork: ' + type(exc).__name__], report


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
        try:
            manifest = json.loads((ROOT / 'docs/consolidation/source-map.json').read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            print(json.dumps({'history': 'failed', 'errors': ['Cannot read manifest: ' + str(exc)]}, indent=2))
            return 1
        errors, history = verify_history(ROOT, manifest, args.require_history)
        # Never trust destination hashes until the full manifest/history gate passes.
        fork_report = {}
        if not errors:
            fork_errors, fork_report = verify_reviewed_fork(ROOT)
            errors.extend(fork_errors)
            # Original evals blobs stay bound to their source above; active evals
            # bytes are now checked against an explicit recorded fork, not relabelled.
            originals = {'sources': [source for source in manifest['sources']
                                     if source['prefix'] != 'evals']}
            errors.extend(verify_files(ROOT, originals))
        report = {'history': history, 'errors': errors}
        if fork_report:
            report['reviewed_fork'] = fork_report
        if not validate_manifest(manifest):
            report.update(source_repositories=len(manifest['sources']) + 1,
                          imported_files=sum(len(source['files']) for source in manifest['sources']))
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
