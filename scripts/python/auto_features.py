"""
auto_features.py
ICWT Study 1: automatic linguistic features for participant queries.

Covers the features marked "auto" in the coding framework:
length, wh-word, modals, negation, person, hedges/epistemic markers,
orthography, plus the participant / chat / turn position parsed from the
Query ID. Clause type is auto-suggested here and checked by a human coder.

Usage:
    python auto_features.py ../../data/example/example_queries.csv out.csv

Input CSV needs at least: query_id, query_text
Query IDs look like P900_C1_Q03 (participant_chat_turn).
"""

import csv
import re
import sys

WH_WORDS = {"what", "why", "how", "who", "whom", "whose", "which", "when", "where"}
MODALS = {"can", "could", "may", "might", "must", "shall", "should", "will",
          "would", "ought", "cant", "couldnt", "wont", "wouldnt", "shouldnt"}
NEGATION = {"not", "no", "never", "nothing", "nobody", "none", "nor", "neither",
            "isnt", "arent", "wasnt", "werent", "dont", "doesnt", "didnt", "cant",
            "couldnt", "wont", "wouldnt", "shouldnt", "hasnt", "havent", "hadnt", "aint"}
FIRST = {"i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "im", "ive", "id"}
SECOND = {"you", "your", "yours", "yourself", "u", "ur", "youre"}
THIRD = {"he", "she", "they", "him", "her", "them", "his", "their", "theirs", "it", "its"}
AUX_START = {"is", "are", "was", "were", "do", "does", "did", "can", "could", "will",
             "would", "should", "has", "have", "had", "isnt", "arent", "dont", "doesnt"}

# Placeholder hedge list. Swap for a published hedge lexicon before real coding
# (framework note: "use a published hedge lexicon").
HEDGES = {"maybe", "perhaps", "probably", "possibly", "kinda", "sorta", "like",
          "apparently", "seems", "seem", "guess", "think", "suppose", "somewhat",
          "basically", "actually", "really", "honestly"}


def tokens(text):
    """Lowercase word tokens with apostrophes dropped (isn't -> isnt)."""
    return re.findall(r"[a-z0-9#]+", text.lower().replace("'", "").replace("’", ""))


def parse_id(qid):
    m = re.match(r"^(?P<p>[^_]+)_(?P<c>C\d+)_Q(?P<t>\d+)", qid or "")
    if not m:
        return "", "", ""
    return m["p"], m["c"], int(m["t"])


def clause_type_guess(text, toks):
    """Rough first pass. A coder confirms or overrides this."""
    if not toks:
        return "Fragment"
    first = toks[0]
    # skip discourse openers like "ok but", "so"
    for t in toks:
        if t not in {"ok", "okay", "so", "but", "and", "um", "well", "hey"}:
            first = t
            break
    if first in WH_WORDS:
        return "Interrogative (wh)"
    if first in AUX_START or text.strip().endswith("?"):
        return "Interrogative (polar)"
    if first in {"tell", "explain", "give", "list", "summarize", "describe", "show"}:
        return "Imperative"
    if len(toks) < 3:
        return "Fragment"
    return "Declarative"


def features(qid, text):
    toks = tokens(text)
    p, c, t = parse_id(qid)
    clauses = max(1, len(re.findall(r"[.?!;]+|\b(?:but|because|and|so|if)\b", text.lower())))
    return {
        "query_id": qid,
        "participant": p,
        "chat": c,
        "turn_position": t,
        "n_words": len(toks),
        "n_clauses_est": clauses,
        "clause_type_auto": clause_type_guess(text, toks),
        "wh_word": next((w for w in toks if w in WH_WORDS), ""),
        "n_modals": sum(w in MODALS for w in toks),
        "negation": int(any(w in NEGATION for w in toks)),
        "person_1": int(any(w in FIRST for w in toks)),
        "person_2": int(any(w in SECOND for w in toks)),
        "person_3": int(any(w in THIRD for w in toks)),
        "n_hedges": sum(w in HEDGES for w in toks),
        "has_question_mark": int("?" in text),
        "all_lowercase": int(text == text.lower()),
        "has_caps_word": int(bool(re.search(r"\b[A-Z]{2,}\b", text))),
        "textspeak": int(any(w in {"u", "ur", "tho", "rn", "idk", "lol", "pls"} for w in toks)),
    }


def main(inp, out):
    with open(inp, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    feats = [features(r["query_id"], r["query_text"]) for r in rows]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(feats[0].keys()))
        w.writeheader()
        w.writerows(feats)
    print(f"Wrote {len(feats)} rows to {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python auto_features.py input.csv output.csv")
    main(sys.argv[1], sys.argv[2])
