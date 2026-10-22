#!/usr/bin/env python3
"""Offline strict scoring for the released JSON annotations; no API calls."""
import argparse
import json
import re
from pathlib import Path

SUBSETS = ('en_emoji', 'en_image', 'zh_emoji', 'zh_image')


def normalize(value):
    value = str(value or '').lower().strip().replace('’', "'").replace('“', '"').replace('”', '"')
    value = re.sub(r'[-_·・]+', ' ', value)
    return re.sub(r'\s+', ' ', re.sub(r'[^一-鿿a-z0-9 ]', '', value)).strip()


def score_records(references, predictions):
    by_id = {r['uid']: r for r in references}
    if len(by_id) != len(references):
        raise ValueError('Duplicate reference UID')
    parsed = {}
    for row in predictions:
        uid = row['uid']
        if uid not in by_id:
            raise ValueError(f'Unknown prediction UID: {uid}')
        if uid in parsed:
            raise ValueError(f'Duplicate prediction UID: {uid}')
        if not isinstance(row.get('prediction', ''), str):
            raise ValueError(f'Prediction must be text: {uid}')
        parsed[uid] = row
    result = {}
    for subset in (*SUBSETS, 'overall'):
        group = [r for r in references if subset == 'overall' or r['subset'] == subset]
        n = len(group)
        valid = correct = recorded = 0
        for ref in group:
            row = parsed.get(ref['uid'])
            if row is None:
                continue
            recorded += 1
            text = row.get('prediction', '').strip()
            if row.get('status', 'ok') == 'ok' and text:
                valid += 1
                correct += bool(normalize(ref['answer'])) and normalize(text) == normalize(ref['answer'])
        result[subset] = {
            'expected': n, 'recorded': recorded, 'missing': n - recorded,
            'valid_nonempty': valid, 'failed_or_empty': recorded - valid, 'correct': correct,
            'strict_all_pct': 100 * correct / n if n else None,
            'strict_valid_pct': 100 * correct / valid if valid else None,
        }
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'data')
    ap.add_argument('--predictions', type=Path, required=True)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    references = []
    for subset in SUBSETS:
        references.extend(json.loads((args.data_dir / f'{subset}.json').read_text(encoding='utf-8')))
    predictions = [json.loads(line) for line in args.predictions.read_text(encoding='utf-8').splitlines() if line.strip()]
    result = {'metric': 'historical_normalized_exact_match', 'answer_extraction': 'supply the final prediction only; no substring credit',
              'scores': score_records(references, predictions)}
    output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        if args.output.exists():
            ap.error('Output exists; choose a new path to preserve prior scores.')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
