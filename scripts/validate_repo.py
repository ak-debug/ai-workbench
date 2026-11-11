"""Validate local catalog, skill structure and selected publication-risk patterns.

No network calls. This is not a complete secret scan or confidentiality audit.
Finding messages identify a file and category, never echo a matched secret.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '.DS_Store', '__pycache__', '.venv', 'venv', 'node_modules', '.pytest_cache'}
PATTERNS = {
    'personal absolute path': r'/(?:Users|home)/[A-Za-z0-9_.-]+/',
    'private key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'credential-like token': r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{32,}|AKIA[A-Z0-9]{16})\b',
    'non-public example domain': r'\b[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*\.(?:internal|corp|local)\b',
}
GENERATED = {'.pptx', '.pdf', '.zip', '.log', '.pem', '.key'}


def scan_text(text, deny_text=()):
    findings = [name for name, pattern in PATTERNS.items() if re.search(pattern, text)]
    if any(term and term.casefold() in text.casefold() for term in deny_text):
        findings.append('explicitly disallowed text')
    return findings


def local_path(root, value):
    if not isinstance(value, str) or not value.startswith('./') or '..' in Path(value).parts:
        raise ValueError('Catalog paths must start with ./ and stay inside the repository.')
    candidate = root / value
    if candidate.is_symlink() or not candidate.resolve().is_relative_to(root.resolve()):
        raise ValueError('Catalog path escapes the repository or uses a symlink.')
    if not candidate.is_dir():
        raise ValueError('Catalog path does not name an existing directory.')
    return candidate


def png_chunks(data):
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('Invalid PNG signature.')
    chunks, offset = [], 8
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError('Truncated PNG chunk.')
        size = int.from_bytes(data[offset:offset + 4], 'big')
        end = offset + size + 12
        if end > len(data):
            raise ValueError('Truncated PNG payload.')
        chunks.append(data[offset + 4:offset + 8])
        offset = end
    return chunks


def validate(root=ROOT, deny_text=()):
    root = Path(root)
    errors = []
    manifest_path = root / '.claude-plugin/marketplace.json'
    try:
        catalog = json.loads(manifest_path.read_text())
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', catalog.get('name', '')):
            errors.append('Marketplace needs a lowercase kebab-case name.')
        if not catalog.get('owner', {}).get('name'):
            errors.append('Marketplace owner name is missing.')
        entries = catalog.get('plugins', [])
        if not entries:
            errors.append('Marketplace has no packages.')
        seen = set()
        for entry in entries:
            name = entry.get('name', '')
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or name in seen:
                errors.append('Invalid or duplicate package name.')
            seen.add(name)
            plugin_root = local_path(root, entry.get('source'))
            for value in entry.get('skills', []):
                skill = local_path(plugin_root, value)
                if not (skill / 'SKILL.md').is_file():
                    errors.append('Catalog skill has no SKILL.md.')
            if entry.get('strict') is False and entry.get('skills') and (plugin_root / '.claude-plugin/plugin.json').exists():
                errors.append('Root skill package conflicts with a plugin manifest.')
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        errors.append(f'Catalog could not be validated ({type(exc).__name__}).')

    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if any(part in SKIP for part in rel.parts):
            continue
        if path.is_symlink():
            errors.append(f'{rel}: unexpected symlink; inspect before publishing.')
            continue
        if not path.is_file():
            continue
        if path.name.startswith('.env') or path.suffix in GENERATED:
            errors.append(f'{rel}: generated output or sensitive configuration is not allowed.')
        data = path.read_bytes()
        if path.suffix == '.png':
            try:
                chunks = png_chunks(data)
                if not set(chunks) <= {b'IHDR', b'IDAT', b'IEND'}:
                    errors.append(f'{rel}: unexpected PNG metadata; inspect before publishing.')
            except ValueError:
                errors.append(f'{rel}: malformed PNG.')
            continue
        try:
            content = data.decode('utf-8')
        except UnicodeDecodeError:
            errors.append(f'{rel}: unreviewed binary type.')
            continue
        for finding in scan_text(content, deny_text):
            errors.append(f'{rel}: {finding}.')
        if path.name == 'SKILL.md':
            match = re.match(r'\A---\n(.*?)\n---\n', content, re.S)
            if not match:
                errors.append(f'{rel}: missing frontmatter.')
            else:
                fields = dict(re.findall(r'^(name|description):\s*(.+)$', match[1], re.M))
                if fields.get('name') != path.parent.name or not fields.get('description'):
                    errors.append(f'{rel}: name or description is missing or mismatched.')
        if path.suffix == '.md':
            for target in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', content):
                if '://' in target or target.startswith(('#', 'mailto:')):
                    continue
                if not (path.parent / target.split('#')[0]).exists():
                    errors.append(f'{rel}: broken local documentation link.')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--deny-text', action='append', default=[], help='Additional private identifier to reject; never printed')
    args = parser.parse_args()
    problems = validate(args.root, args.deny_text)
    for problem in problems:
        print(problem)
    if problems:
        raise SystemExit(1)
    print('Catalog, skills, links and selected publication guardrails passed.')
    print('Human review of content, image pixels, rights and Git history is still required.')
