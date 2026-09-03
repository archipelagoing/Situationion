"""Build lexically and structurally matched situation triples for v4.

Run from the repository root:
    python structural_controls.py

The script writes candidate triples, a balanced accepted set, matching diagnostics,
and a small manual-review sample. It deliberately performs no model inference.
"""

from __future__ import annotations

import argparse
import csv
import random
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DIAGNOSTICS_DIR = ROOT / "results" / "matching_diagnostics"

NAMES = (
    ("Ava", "she", "her"),
    ("Ben", "he", "him"),
    ("Clara", "she", "her"),
    ("Diego", "he", "him"),
    ("Elena", "she", "her"),
    ("Farid", "he", "him"),
    ("Grace", "she", "her"),
    ("Hugo", "he", "him"),
    ("Inez", "she", "her"),
    ("Jonah", "he", "him"),
    ("Keira", "she", "her"),
    ("Liam", "he", "him"),
    ("Maya", "she", "her"),
    ("Noah", "he", "him"),
    ("Priya", "she", "her"),
    ("Owen", "he", "him"),
    ("Rosa", "she", "her"),
    ("Theo", "he", "him"),
    ("Uma", "she", "her"),
    ("Victor", "he", "him"),
)

OBJECTS = ("key", "map", "torch", "package", "note")
REPAIR_OBJECTS = ("bike", "radio", "lamp", "gate", "engine")
EVENT_OBJECTS = ("glass", "vase", "box", "plate", "lantern")
TEMPORAL_EVENTS = ("the alarm rang", "the bell rang", "the lights failed")

WORD_RE = re.compile(r"[a-z]+")


@dataclass(frozen=True)
class Triple:
    identifier: str
    template_id: str
    manipulation: str
    split: str
    template_split: str
    entity_split: str
    agent: str
    recipient: str
    event: str
    changed_field: str
    base: str
    paraphrase: str
    counterfactual: str


def tokens(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def jaccard(left: Iterable[object], right: Iterable[object]) -> float:
    left_set, right_set = set(left), set(right)
    return len(left_set & right_set) / len(left_set | right_set)


def multiset_f1(left: list[str], right: list[str]) -> float:
    overlap = sum((Counter(left) & Counter(right)).values())
    return 2 * overlap / (len(left) + len(right))


def normalized_edit_similarity(left: list[str], right: list[str]) -> float:
    """Token-level Levenshtein similarity; 1 means identical token sequences."""
    previous = list(range(len(right) + 1))
    for i, left_token in enumerate(left, start=1):
        current = [i]
        for j, right_token in enumerate(right, start=1):
            current.append(min(
                current[-1] + 1,
                previous[j] + 1,
                previous[j - 1] + (left_token != right_token),
            ))
        previous = current
    return 1 - previous[-1] / max(len(left), len(right), 1)


def bigrams(items: list[str]) -> list[tuple[str, str]]:
    return list(zip(items, items[1:]))


def structural_tokens(text: str, triple: Triple) -> list[str]:
    """Map lexical choices to coarse categories before comparing word order."""
    replacements = {
        triple.agent.lower(): "PERSON",
        triple.recipient.lower(): "PERSON",
        "he": "PRONOUN",
        "him": "PRONOUN",
        "she": "PRONOUN",
        "her": "PRONOUN",
        "because": "CONNECTIVE",
        "since": "CONNECTIVE",
        "when": "CONNECTIVE",
        "after": "TEMPORAL",
        "before": "TEMPORAL",
    }
    return [replacements.get(token, token) for token in tokens(text)]


def pair_metrics(base: str, comparison: str, triple: Triple) -> dict[str, float]:
    base_tokens, comparison_tokens = tokens(base), tokens(comparison)
    base_structure = structural_tokens(base, triple)
    comparison_structure = structural_tokens(comparison, triple)
    return {
        "unigram_jaccard": jaccard(base_tokens, comparison_tokens),
        "unigram_multiset_f1": multiset_f1(base_tokens, comparison_tokens),
        "bigram_jaccard": jaccard(bigrams(base_tokens), bigrams(comparison_tokens)),
        "edit_similarity": normalized_edit_similarity(base_tokens, comparison_tokens),
        "structural_edit_similarity": normalized_edit_similarity(base_structure, comparison_structure),
        "token_count": float(len(comparison_tokens)),
        "length_difference": float(abs(len(base_tokens) - len(comparison_tokens))),
    }


def build_triple(
    manipulation: str,
    style: int,
    index: int,
    agent: tuple[str, str, str],
    recipient: tuple[str, str, str],
    entity_split: str,
) -> Triple:
    agent_name, agent_subject, agent_object = agent
    recipient_name, recipient_subject, recipient_object = recipient
    template_split = "test" if style == 2 else "dev"
    split = "test_both" if template_split == entity_split == "test" else (
        "test_template" if template_split == "test" else (
            "test_entity" if entity_split == "test" else "dev"
        )
    )
    template_id = f"{manipulation}_style_{style}"
    identifier = f"{template_id}_{index:03d}"

    if manipulation == "agent_recipient":
        object_name = OBJECTS[index % len(OBJECTS)]
        connective = ("because", "since", "when")[style]
        base = f"{agent_name} gave {recipient_name} the {object_name} {connective} {recipient_subject} was locked out."
        paraphrase = f"{connective.capitalize()} {recipient_name} was locked out, {agent_name} gave {recipient_object} the {object_name}."
        counterfactual = f"{connective.capitalize()} {agent_name} was locked out, {recipient_name} gave {agent_object} the {object_name}."
        event, changed_field = "give", "agent_recipient"
    elif manipulation == "cause":
        connective = ("because", "since", "when")[style]
        base = f"{agent_name} called {recipient_name} {connective} {recipient_subject} was worried."
        paraphrase = f"{connective.capitalize()} {recipient_name} was worried, {agent_name} called {recipient_object}."
        counterfactual = f"{connective.capitalize()} {agent_name} was worried, {agent_subject} called {recipient_name}."
        event, changed_field = "call", "cause_participant"
    elif manipulation == "temporal":
        object_name = "the spill"
        temporal_event = TEMPORAL_EVENTS[style]
        base = f"{agent_name} cleaned {object_name} after {temporal_event}."
        paraphrase = f"Once {temporal_event}, {agent_name} cleaned {object_name}."
        counterfactual = f"Before {temporal_event}, {agent_name} cleaned {object_name}."
        event, changed_field = "clean", "temporal_relation"
    elif manipulation == "polarity":
        object_name = REPAIR_OBJECTS[(index + style) % len(REPAIR_OBJECTS)]
        base = f"{agent_name} did repair the {object_name} because it was broken."
        paraphrase = f"Since the {object_name} was broken, {agent_name} did mend it."
        counterfactual = f"Because the {object_name} was broken, {agent_name} did not fix it."
        event, changed_field = "repair", "polarity"
    elif manipulation == "event_state":
        object_name = EVENT_OBJECTS[(index + style) % len(EVENT_OBJECTS)]
        base = f"{agent_name} carried the {object_name} because it was fragile."
        paraphrase = f"Because the {object_name} was fragile, {agent_name} transported it."
        counterfactual = f"Because the {object_name} was fragile, {agent_name} dropped it."
        event, changed_field = "carry", "event"
    else:
        raise ValueError(f"Unsupported manipulation: {manipulation}")

    return Triple(
        identifier=identifier,
        template_id=template_id,
        manipulation=manipulation,
        split=split,
        template_split=template_split,
        entity_split=entity_split,
        agent=agent_name,
        recipient=recipient_name,
        event=event,
        changed_field=changed_field,
        base=base,
        paraphrase=paraphrase,
        counterfactual=counterfactual,
    )


def generate_candidates() -> list[Triple]:
    manipulations = ("agent_recipient", "cause", "temporal", "polarity", "event_state")
    candidates = []
    for manipulation in manipulations:
        for style in range(3):
            for entity_split, entity_pool, offset in (
                ("dev", NAMES[:14], 0),
                ("test", NAMES[14:], 14),
            ):
                for local_index, agent in enumerate(entity_pool):
                    recipient = entity_pool[(local_index + 5) % len(entity_pool)]
                    candidates.append(build_triple(
                        manipulation,
                        style,
                        offset + local_index,
                        agent,
                        recipient,
                        entity_split,
                    ))
    return candidates


def add_diagnostics(triple: Triple) -> dict[str, object]:
    row = asdict(triple)
    paraphrase_metrics = pair_metrics(triple.base, triple.paraphrase, triple)
    counterfactual_metrics = pair_metrics(triple.base, triple.counterfactual, triple)
    for metric, value in paraphrase_metrics.items():
        row[f"base_paraphrase_{metric}"] = value
    for metric, value in counterfactual_metrics.items():
        row[f"base_counterfactual_{metric}"] = value
    controlled_metrics = (
        "unigram_jaccard",
        "unigram_multiset_f1",
        "bigram_jaccard",
        "edit_similarity",
        "structural_edit_similarity",
        "length_difference",
    )
    for metric in controlled_metrics:
        row[f"absolute_{metric}_gap"] = abs(paraphrase_metrics[metric] - counterfactual_metrics[metric])
    row["match_score"] = sum(row[f"absolute_{metric}_gap"] for metric in controlled_metrics)
    return row


def is_matched(row: dict[str, object]) -> bool:
    return (
        row["absolute_unigram_jaccard_gap"] <= 0.10
        and row["absolute_unigram_multiset_f1_gap"] <= 0.10
        and row["absolute_bigram_jaccard_gap"] <= 0.10
        and row["absolute_edit_similarity_gap"] <= 0.10
        and row["absolute_structural_edit_similarity_gap"] <= 0.05
        and row["absolute_length_difference_gap"] <= 1.0
    )


def balanced_selection(rows: list[dict[str, object]], target_size: int, seed: int) -> list[dict[str, object]]:
    by_manipulation: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        if is_matched(row):
            by_manipulation[str(row["manipulation"])].append(row)

    families = sorted(by_manipulation)
    if not families:
        raise RuntimeError("No candidates passed the matching thresholds.")
    if target_size < len(families):
        raise ValueError("target_size must include at least one triple per manipulation.")

    base_count, remainder = divmod(target_size, len(families))
    selected = []
    rng = random.Random(seed)
    for family_index, family in enumerate(families):
        family_rows = by_manipulation[family]
        rng.shuffle(family_rows)
        family_rows.sort(key=lambda row: float(row["match_score"]))
        required = base_count + (family_index < remainder)
        if len(family_rows) < required:
            raise RuntimeError(f"Only {len(family_rows)} matched {family} triples; need {required}.")
        selected.extend(family_rows[:required])
    return sorted(selected, key=lambda row: str(row["identifier"]))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    metric_names = [
        "absolute_unigram_jaccard_gap",
        "absolute_unigram_multiset_f1_gap",
        "absolute_bigram_jaccard_gap",
        "absolute_edit_similarity_gap",
        "absolute_structural_edit_similarity_gap",
        "absolute_length_difference_gap",
        "match_score",
    ]
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["manipulation"])].append(row)
    summary = []
    for manipulation, group in sorted(grouped.items()):
        summary.append({
            "manipulation": manipulation,
            "n": len(group),
            **{metric: sum(float(row[metric]) for row in group) / len(group) for metric in metric_names},
        })
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-size", type=int, default=300, help="Balanced accepted dataset size (default: 300).")
    parser.add_argument("--seed", type=int, default=7, help="Seed for balanced candidate selection.")
    args = parser.parse_args()

    candidate_rows = [add_diagnostics(triple) for triple in generate_candidates()]
    accepted_rows = balanced_selection(candidate_rows, args.target_size, args.seed)

    write_csv(DATA_DIR / "candidate_triples.csv", candidate_rows)
    write_csv(DATA_DIR / "matched_triples.csv", accepted_rows)
    write_csv(DIAGNOSTICS_DIR / "matching_summary.csv", summary_rows(accepted_rows))

    review_rng = random.Random(args.seed)
    review_rows = accepted_rows.copy()
    review_rng.shuffle(review_rows)
    write_csv(DIAGNOSTICS_DIR / "manual_review_sample.csv", review_rows[: min(25, len(review_rows))])

    print(f"Wrote {len(candidate_rows)} candidates and {len(accepted_rows)} matched triples.")
    print(f"Accepted triples: {DATA_DIR / 'matched_triples.csv'}")
    print(f"Matching diagnostics: {DIAGNOSTICS_DIR}")


if __name__ == "__main__":
    main()
