#!/usr/bin/env python3
"""Verify the local GitHub/HF pair without fetching data or calling model APIs."""
import argparse
import hashlib
import io
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    import pyarrow.parquet as pq
    import yaml
    from PIL import Image
    from datasets import Features, Image as ImageFeature

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--github-dir', type=Path, required=True)
    ap.add_argument('--hf-dir', type=Path, required=True)
    args = ap.parse_args()
    gh, hf = args.github_dir.resolve(), args.hf_dir.resolve()
    release = json.loads((gh / 'data/release.json').read_text(encoding='utf-8'))
    require(release == json.loads((hf / 'release.json').read_text(encoding='utf-8')), 'Release manifests differ')
    image_manifest = json.loads((hf / 'image_manifest.json').read_text(encoding='utf-8'))
    require(image_manifest == json.loads((gh / 'data/image_manifest.json').read_text(encoding='utf-8')), 'Image manifests differ')
    mapping = {(r['uid'], r['slot']): r for r in image_manifest}
    card = (hf / 'README.md').read_text(encoding='utf-8')
    require(card.startswith('---\n'), 'HF YAML must start at the beginning')
    config = yaml.safe_load(card.split('---', 2)[1])
    configs = {r['config_name']: r for r in config['configs']}
    require(set(configs) == {'en_emoji', 'en_image', 'zh_emoji', 'zh_image'}, 'Wrong config names')
    all_ids, image_total, row_total, checks = set(), 0, 0, []
    for subset in release['subsets']:
        name = subset['name']
        public_rows = json.loads((gh / 'data' / f'{name}.json').read_text(encoding='utf-8'))
        file = hf / subset['parquet']
        require(file.is_relative_to(hf), 'Unsafe Parquet path')
        require(digest(file.read_bytes()) == subset['parquet_sha256'], 'Parquet checksum mismatch')
        matches = []
        for entry in configs[name]['data_files']:
            require(entry['split'] == 'test', 'Unexpected split')
            matches.extend(hf.glob(entry['path']))
        require(matches == [file], f'Config mismatch: {name}')
        table = pq.read_table(file)
        features = Features.from_arrow_schema(table.schema)
        for key in ('image_1', 'image_2'):
            require(isinstance(features[key], ImageFeature), f'{key} must have Image metadata')
        hf_rows = table.to_pylist()
        require(len(public_rows) == len(hf_rows) == subset['rows'], 'Row count mismatch')
        subset_images = 0
        expected_images = 2 if name == 'en_image' else 1 if name == 'zh_image' else 0
        for row, hf_row in zip(public_rows, hf_rows):
            uid = row['uid']
            require(uid not in all_ids and uid == name + '_' + row['source_id'], 'Duplicate/invalid UID')
            all_ids.add(uid)
            require(bool(row['answer'].strip()), 'Empty reference')
            for key, value in row.items():
                if key not in ('image_1', 'image_2'):
                    require(value == hf_row[key], f'Annotation mismatch: {uid}/{key}')
            require(row['reference_review'] == 'inherited_unverified', 'Unjustified annotation verification')
            count = 0
            for slot in (1, 2):
                key = f'image_{slot}'
                if row[key] is None:
                    require(hf_row[key] is None and not row[key + '_sha256'], 'Null image mismatch')
                    continue
                count += 1
                payload = hf_row[key]
                require(payload and payload['bytes'], 'Image must embed bytes')
                require(Path(payload['path']).name == payload['path'], 'Image path is not portable')
                require(digest(payload['bytes']) == row[key + '_sha256'], 'Image checksum mismatch')
                preview = (gh / row[key]).resolve()
                require(preview.is_relative_to(gh), 'Unsafe preview path')
                with Image.open(preview) as image:
                    require(max(image.size) <= 960, 'Preview too large')
                    image.verify()
                meta = mapping[uid, slot]
                require(meta['released_png_sha256'] == row[key + '_sha256'], 'Image provenance mismatch')
                with Image.open(io.BytesIO(payload['bytes'])) as image:
                    require(image.format == 'PNG', 'Full image must be PNG')
                    require(list(image.size) == meta['released_dimensions'], 'Dimension mismatch')
                    require(not image.getexif() and not image.info, 'Image metadata not stripped')
                    image.load()
            require(count == expected_images, f'Wrong ordered image count: {uid}')
            subset_images += count
        require(subset_images == subset['images'], 'Subset image count mismatch')
        row_total += len(hf_rows)
        image_total += subset_images
        checks.append({'subset': name, 'rows': len(hf_rows), 'decoded_images': subset_images, 'hf_image_features': True})
    require(row_total == release['total_rows'] and image_total == release['total_images'], 'Total mismatch')
    require(len(mapping) == image_total, 'Unreferenced image manifest rows')
    actual_previews = {p.relative_to(gh).as_posix() for p in (gh / 'assets/previews').glob('*') if p.is_file()}
    require(actual_previews == {r['preview'] for r in image_manifest}, 'Orphan/missing previews')
    banned = {'k', '.env', 'users.json', 'answers.json', 'answers.csv', 'modellist'}
    for root in (gh, hf):
        for file in root.rglob('*'):
            if file.is_file():
                require(file.name not in banned and file.suffix != '.log', 'Private artifact in release')
                require(file.stat().st_size < 100 * 1024 ** 2 or file.suffix == '.parquet', 'Oversized ordinary Git asset')
    report = {'technical_validation': 'passed', 'rows': row_total, 'images': image_total, 'subsets': checks,
              'not_certified': ['license/redistribution rights', 'human reference validation', 'paper split identity', 'remote Dataset Viewer build']}
    target = gh / 'release_validation.json'
    target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
