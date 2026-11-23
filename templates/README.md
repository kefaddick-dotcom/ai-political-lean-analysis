# Coding workflow templates

Excel workbooks I built for the Study 1 RA team. All rows shown are invented training examples; no participant data.

| File | What it does |
|---|---|
| `ICWT_S1_Transcript_TEMPLATE.xlsx` | One file per session. Header metadata (IDs only, no demographics), then one row per turn with turn-type dropdowns, conditional formatting, and Turn ID validation that flags missing or misplaced IDs. |
| `ICWT_S1_Coding_Sheet_TEMPLATE.xlsx` | One row per speech act. Dropdown-controlled codes, formula-filled participant/chat/turn fields parsed from the Query ID, and a decision log for rules set in consensus meetings. |
| `ICWT_Consensus_TEMPLATE.xlsx` | Paste two coders' sheets in; it matches speech acts, flags segmentation mismatches, counts conflicts per row, auto-fills agreed codes, and summarizes segmentation agreement and agreement by code. |

Flow: **transcribe** → **segment + code** (two coders, blind) → **consensus meeting** → **reliability** (`scripts/python/reliability.py`).
