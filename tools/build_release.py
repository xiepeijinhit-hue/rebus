#!/usr/bin/env python3
"""Package a sanitized BiRebus snapshot. Offline only; source files are never changed."""
import argparse
import hashlib
import io
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SUBSETS = {
    'en_emoji': ('en', 'emoji', 0),
    'en_image': ('en', 'pictorial', 2),
    'zh_emoji': ('zh', 'emoji_idiom', 0),
    'zh_image': ('zh', 'pictorial', 1),
}
MODELS = ['gpt-6-astra', 'gemini-3.8-flash', 'gpt-5.6-sol', 'deepseek-v4-flash-vision-official']
STRATEGIES = {'direct': 'raw', 'vg': 'raw_vg', 'vgpi': 'raw_vgpi', 'oracle': 'raw_oracle'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def normalize(value):
    value = str(value or '').lower().strip().replace('’', "'").replace('“', '"').replace('”', '"')
    value = re.sub(r'[-_·・]+', ' ', value)
    return re.sub(r'\s+', ' ', re.sub(r'[^一-鿿a-z0-9 ]', '', value)).strip()


def load_results(path):
    if not path.is_file():
        return {}, 0
    rows = {}
    duplicates = 0
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        key = str(row['id'])
        duplicates += key in rows
        rows[key] = row
    return rows, duplicates


def valid(row):
    return row.get('status') == 'ok' and bool(str(row.get('prediction') or '').strip())


def score(row, answer):
    return valid(row) and bool(normalize(answer)) and normalize(row['prediction']) == normalize(answer)


def audit_results(source, pools):
    cells, pairs, provenance = [], [], []
    for subset, pool in pools.items():
        refs = {str(r['id']): r['answer'] for r in pool}
        cache = {}
        for strategy, folder in STRATEGIES.items():
            for model in MODELS:
                path = source / 'eval_results' / folder / f'{subset}__{model}.jsonl'
                all_rows, duplicates = load_results(path)
                rows = {k: r for k, r in all_rows.items() if k in refs}
                cache[strategy, model] = rows
                if path.exists():
                    provenance.append({'file': path.relative_to(source).as_posix(), 'sha256': sha(path.read_bytes())})
                usable = {k: r for k, r in rows.items() if valid(r)}
                correct = sum(score(r, refs[k]) for k, r in usable.items())
                cells.append({
                    'subset': subset, 'strategy': strategy, 'model_label': model,
                    'expected': len(refs), 'recorded': len(rows), 'missing': len(refs) - len(rows),
                    'valid_nonempty': len(usable), 'correct': correct,
                    'empty': sum(r.get('status') == 'ok' and not valid(r) or 'empty' in str(r.get('status')) for r in rows.values()),
                    'statuses': dict(Counter(str(r.get('status', 'unknown')) for r in rows.values())),
                    'duplicates_in_source': duplicates,
                    'strict_all_pct': round(correct / len(refs) * 100, 4) if rows else None,
                    'strict_valid_pct': round(correct / len(usable) * 100, 4) if usable else None,
                    'note': 'Historical snapshot, not a controlled rerun; missing/failed count as zero only in strict_all_pct.',
                })
        for model in MODELS:
            a, b = cache['direct', model], cache['vgpi', model]
            ids = sorted(k for k in refs if k in a and k in b and valid(a[k]) and valid(b[k]))
            ca = sum(score(a[k], refs[k]) for k in ids)
            cb = sum(score(b[k], refs[k]) for k in ids)
            pairs.append({
                'subset': subset, 'model_label': model, 'common_valid': len(ids),
                'direct_correct': ca, 'vgpi_correct': cb,
                'direct_pct': round(ca / len(ids) * 100, 4) if ids else None,
                'vgpi_pct': round(cb / len(ids) * 100, 4) if ids else None,
                'delta_pp': round((cb - ca) / len(ids) * 100, 4) if ids else None,
                'wrong_to_right': sum(not score(a[k], refs[k]) and score(b[k], refs[k]) for k in ids),
                'right_to_wrong': sum(score(a[k], refs[k]) and not score(b[k], refs[k]) for k in ids),
                'common_ids': ids,
            })
    return {'schema_version': '1.0', 'cells': cells, 'paired_direct_vgpi': pairs, 'source_hashes': provenance,
            'interpretation': 'Paired rows use the same successful IDs but still have selection/configuration confounding. No human-level claim is verified.'}


def main():
    from PIL import Image, ImageOps
    from datasets import Dataset, Features, Image as ImageFeature, Value

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-root', type=Path, required=True)
    ap.add_argument('--github-dir', type=Path, required=True)
    ap.add_argument('--hf-dir', type=Path, required=True)
    args = ap.parse_args()
    source, gh, hf = [p.resolve() for p in (args.source_root, args.github_dir, args.hf_dir)]
    if len({source, gh, hf}) != 3:
        ap.error('Source and output roots must be distinct.')
    if hf == source / 'benchmark_100' or gh == source / 'benchmark_100':
        ap.error('Never use the source benchmark directory as output.')
    gh.mkdir(parents=True, exist_ok=True)
    hf.mkdir(parents=True, exist_ok=True)
    if (gh / 'data/release.json').exists() or (hf / 'release.json').exists():
        ap.error('Release already exists. Use fresh output directories to preserve the snapshot.')
    pools = {}
    for subset, (_, _, expected_images) in SUBSETS.items():
        rows = json.loads((source / 'benchmark_100' / f'{subset}.json').read_text(encoding='utf-8'))
        if not isinstance(rows, list) or not rows:
            raise ValueError(f'Empty or invalid subset: {subset}')
        if len({str(r['id']) for r in rows}) != len(rows):
            raise ValueError(f'Duplicate ID in {subset}')
        for row in rows:
            if not str(row['answer']).strip() or len(row['images']) != expected_images:
                raise ValueError(f'Invalid answer/image count: {subset}/{row["id"]}')
            for name in row['images']:
                if Path(name).name != name:
                    raise ValueError('Unsafe source image name')
                image_path = source / 'benchmark_100/images' / name
                with Image.open(image_path) as image:
                    image.verify()
        pools[subset] = rows

    fields = ['uid', 'source_id', 'subset', 'language', 'task', 'prompt', 'emoji', 'hint', 'answer',
              'image_1_sha256', 'image_2_sha256', 'selection_status', 'reference_review']
    features = Features({**{k: Value('string') for k in fields},
                         'image_1': ImageFeature(), 'image_2': ImageFeature()})
    release = {'schema_version': '1.0', 'name': 'BiRebus local diagnostic snapshot',
               'created_at': datetime.now(timezone.utc).isoformat(), 'split': 'test',
               'status': 'local_prepublication_snapshot', 'license_status': 'unverified',
               'paper_alignment': 'Paper describes a reviewed split; independent verification of that exact split is unavailable.',
               'subsets': [], 'excluded': ['credentials', 'user answers', 'annotator identities', 'internal API configuration', 'raw model traces']}
    previews, mapping = [], []
    for subset, rows in pools.items():
        language, task, expected_images = SUBSETS[subset]
        public_rows, hf_rows = [], []
        for row in rows:
            sid = str(row['id'])
            if not re.fullmatch(r'[A-Za-z0-9_-]+', sid):
                raise ValueError('Unsafe sample ID')
            uid = f'{subset}_{sid}'
            prediction = str(row.get('source_model_prediction') or '').strip()
            selection = ('empty_response' if not prediction else
                         'nonempty_correct' if row.get('source_model_correct') else 'nonempty_incorrect')
            hint = str(row.get('input', '')).strip() if subset == 'en_image' else ''
            emoji = str(row.get('input', '')) if expected_images == 0 else ''
            prompt = (f'Image 1 is {hint}. What expression does image 2 represent?' if hint else
                      'What expression does image 2 represent?') if subset == 'en_image' else (
                      '这张图表示什么词语？' if subset == 'zh_image' else
                      '这些符号表示什么成语？' if subset == 'zh_emoji' else 'What expression do these symbols represent?')
            item = {'uid': uid, 'source_id': sid, 'subset': subset, 'language': language, 'task': task,
                    'prompt': prompt, 'emoji': emoji, 'hint': hint, 'answer': str(row['answer']),
                    'image_1': None, 'image_2': None, 'image_1_sha256': '', 'image_2_sha256': '',
                    'selection_status': selection, 'reference_review': 'inherited_unverified'}
            hf_item = dict(item)
            for i, filename in enumerate(row['images'], 1):
                raw = (source / 'benchmark_100/images' / filename).read_bytes()
                with Image.open(io.BytesIO(raw)) as im:
                    image = ImageOps.exif_transpose(im).convert('RGBA' if 'A' in im.getbands() else 'RGB')
                    clean = Image.frombytes(image.mode, image.size, image.tobytes())
                png = io.BytesIO()
                clean.save(png, format='PNG', optimize=True)
                image_bytes = png.getvalue()
                digest = sha(image_bytes)
                name = f'{uid}_{i}'
                thumb = clean.copy()
                thumb.thumbnail((960, 960), Image.Resampling.LANCZOS)
                preview_path = gh / 'assets/previews' / f'{name}.webp'
                preview_path.parent.mkdir(parents=True, exist_ok=True)
                thumb.save(preview_path, format='WEBP', quality=88, method=6)
                item[f'image_{i}'] = preview_path.relative_to(gh).as_posix()
                item[f'image_{i}_sha256'] = digest
                hf_item[f'image_{i}'] = {'bytes': image_bytes, 'path': f'{name}.png'}
                hf_item[f'image_{i}_sha256'] = digest
                mapping.append({'uid': uid, 'slot': i, 'source_file': f'benchmark_100/images/{filename}',
                                'source_sha256': sha(raw), 'released_png_sha256': digest,
                                'released_dimensions': list(clean.size), 'preview': item[f'image_{i}']})
            public_rows.append(item)
            hf_rows.append(hf_item)
        write_json(gh / 'data' / f'{subset}.json', public_rows)
        previews.extend(public_rows)
        target = hf / 'data' / subset / 'test-00000-of-00001.parquet'
        target.parent.mkdir(parents=True, exist_ok=True)
        Dataset.from_list(hf_rows, features=features).to_parquet(str(target), batch_size=10)
        release['subsets'].append({'name': subset, 'language': language, 'task': task, 'rows': len(rows),
                                   'images': len(rows) * expected_images,
                                   'source': f'benchmark_100/{subset}.json',
                                   'source_sha256': sha((source / 'benchmark_100' / f'{subset}.json').read_bytes()),
                                   'selection_status_counts': dict(Counter(r['selection_status'] for r in public_rows)),
                                   'parquet': target.relative_to(hf).as_posix(), 'parquet_sha256': sha(target.read_bytes())})
    release['total_rows'] = len(previews)
    release['total_images'] = len(mapping)
    write_json(gh / 'data/release.json', release)
    write_json(hf / 'release.json', release)
    write_json(gh / 'data/image_manifest.json', mapping)
    write_json(hf / 'image_manifest.json', mapping)
    write_json(gh / 'results/local_audit.json', audit_results(source, pools))
    print(json.dumps({'rows': len(previews), 'images': len(mapping), 'subsets': list(pools)}, indent=2))


if __name__ == '__main__':
    main()
