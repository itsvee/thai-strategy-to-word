"""Validate interview completeness, not the truth or quality of answers."""
import argparse
import json
from pathlib import Path

FIELDS = (
    'company', 'business', 'customers', 'user_role', 'strategy_scope',
    'audience', 'decision', 'problem', 'desired_outcome', 'horizon',
    'constraints', 'tradeoffs', 'non_goals',
)
STATUSES = {'verified', 'user_reported', 'hypothesis', 'proposed', 'unknown'}
UNKNOWN = {'', 'unknown', 'tbd', 'todo', 'n/a', 'ไม่ทราบ', 'ยังไม่ทราบ', 'ไม่รู้', 'ยังไม่รู้', '-', '?'}


def meaningful(value):
    return isinstance(value, str) and value.strip().casefold() not in UNKNOWN


def revision(value):
    return type(value) is int and value > 0


def evaluate(state):
    if not isinstance(state, dict):
        raise ValueError('State must be a JSON object.')
    current = state.get('brief_revision')
    confirmed = state.get('confirmed_revision')
    if not revision(current):
        raise ValueError('brief_revision must be a positive integer.')
    if confirmed is not None and not revision(confirmed):
        raise ValueError('confirmed_revision must be null or a positive integer.')
    if confirmed is not None and confirmed > current:
        raise ValueError('confirmed_revision cannot exceed brief_revision.')
    brief = state.get('brief')
    if not isinstance(brief, dict):
        raise ValueError('brief must be an object.')
    for key in ('evidence', 'gaps', 'contradictions'):
        if not isinstance(state.get(key), list):
            raise ValueError(f'{key} must be a list.')
    blockers = []
    for key in FIELDS:
        if not meaningful(brief.get(key)):
            blockers.append({'field': key, 'reason': 'Missing substantive brief answer.'})
    observed = False
    for index, item in enumerate(state['evidence']):
        if not isinstance(item, dict) or item.get('status') not in STATUSES:
            raise ValueError(f'evidence[{index}] must have a valid status.')
        if not meaningful(item.get('claim')):
            blockers.append({'field': f'evidence[{index}]', 'reason': 'Evidence claim is missing.'})
        if item['status'] in {'verified', 'user_reported'}:
            if meaningful(item.get('claim')) and meaningful(item.get('source')):
                observed = True
            else:
                blockers.append({'field': f'evidence[{index}]', 'reason': 'Observed evidence needs a claim and source.'})
    if not observed:
        blockers.append({'field': 'evidence', 'reason': 'At least one sourced observation or specific user report is required.'})
    for index, gap in enumerate(state['gaps']):
        if not isinstance(gap, dict) or not meaningful(gap.get('field')):
            raise ValueError(f'gaps[{index}] must identify a field.')
        treatment = gap.get('treatment')
        if treatment not in {'block', 'collection_plan'}:
            raise ValueError(f'gaps[{index}] has an invalid treatment.')
        if treatment == 'block':
            blockers.append({'field': gap['field'], 'reason': 'Unresolved blocking gap.'})
        elif not all(meaningful(gap.get(key)) for key in ('owner', 'method', 'deadline')) or gap.get('accepted') is not True:
            blockers.append({'field': gap['field'], 'reason': 'Collection plan needs owner, method, deadline and explicit acceptance.'})
    if state['contradictions']:
        blockers.append({'field': 'contradictions', 'reason': 'Resolve material contradictions before drafting.'})
    status = 'needs_interview' if blockers else ('ready_for_analysis' if confirmed == current else 'ready_for_confirmation')
    return {'ok': True, 'status': status, 'brief_revision': current,
            'blockers': blockers, 'semantic_review_required': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('state', type=Path)
    args = parser.parse_args()
    try:
        result = evaluate(json.loads(args.state.read_text(encoding='utf-8')))
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({'ok': False, 'error': str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'ready_for_analysis' else 2


if __name__ == '__main__':
    raise SystemExit(main())
