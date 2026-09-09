import re
from collections import Counter

# ============================================================
# PART 2: LIGHTWEIGHT HEURISTIC "SLOP DETECTOR"
# Transparent, rule-based (no black-box model needed) — good for
# a live demo where you explain exactly WHY something got flagged.
# ============================================================

# Common "slop" markers seen in generic AI/copy-paste social captions.
# Extend this list freely as you collect more real examples.
GENERIC_PHRASES = [
    "in today's fast-paced world",
    "dive into",
    "unlock the secrets",
    "game changer",
    "let's dive in",
    "in this day and age",
    "elevate your",
    "unleash your",
    "at the end of the day",
    "it goes without saying",
    "in conclusion",
    "level up your",
    "take it to the next level",
    "the world of",
    "when it comes to",
    "in the realm of",
    "journey of",
    "embark on",
]

def generic_phrase_score(text):
    text_lower = text.lower()
    hits = sum(1 for phrase in GENERIC_PHRASES if phrase in text_lower)
    return hits

def repetition_score(text):
    """High repetition of the same words = lower lexical diversity = more 'slop-like'."""
    words = re.findall(r"\b\w+\b", text.lower())
    if len(words) < 3:
        return 0.0
    counts = Counter(words)
    most_common_count = counts.most_common(1)[0][1]
    return most_common_count / len(words)

def emoji_density(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001FAFF"
        "\U00002700-\U000027BF"
        "\U0001F600-\U0001F64F"
        "]+", flags=re.UNICODE
    )
    emojis = emoji_pattern.findall(text)
    total_emoji_chars = sum(len(e) for e in emojis)
    return total_emoji_chars / max(len(text), 1)

def slop_score(text):
    """
    Combines three transparent signals into one score in [0, 1].
    Higher = more likely to be 'slop' (generic/copy-paste-sounding).
    Weights are simple and explainable — good for a live demo,
    not meant to be a state-of-the-art detector.
    """
    gp = generic_phrase_score(text)
    gp_norm = min(gp / 3, 1.0)          # cap contribution at 3+ generic phrases
    rep = repetition_score(text)
    emoji = emoji_density(text)
    emoji_norm = min(emoji * 5, 1.0)    # heavy emoji use nudges toward "slop"

    score = 0.5 * gp_norm + 0.3 * rep + 0.2 * emoji_norm
    return round(score, 3)

def classify(text, threshold=0.35):
    score = slop_score(text)
    label = "SLOP" if score >= threshold else "NOVEL"
    return label, score


if __name__ == "__main__":
    # Placeholder examples — REPLACE these with your own 10-20
    # real collected Instagram/LinkedIn captions before your demo.
    examples = [
        "In today's fast-paced world, it's important to dive into new opportunities and unlock the secrets to success! #motivation #hustle",
        "my dog fell asleep in the laundry basket again and I'm never doing laundry again honestly worth it",
        "Excited to embark on this incredible journey! Let's dive in and elevate your career to the next level. #grateful #blessed",
        "just spent 3 hours trying to fix a bug that was one missing comma. i want to lie down forever",
    ]

    for ex in examples:
        label, score = classify(ex)
        print(f"[{label}] (score={score})  {ex[:70]}...")
