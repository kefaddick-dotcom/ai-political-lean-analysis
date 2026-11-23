# Scripts

| Script | Language | Status | What it does |
|---|---|---|---|
| `python/auto_features.py` | Python (stdlib only) | Working | Auto-codes length, clause type (suggested), wh-word, modals, negation, person, hedges, orthography; parses participant/chat/turn from Query IDs |
| `python/reliability.py` | Python (stdlib only) | Working | Krippendorff's alpha (nominal) per code for two coders, checked against the pre-set thresholds |
| `R/01_study1_descriptives.R` | R | Scaffold | Speech act frequencies with cluster-bootstrap CIs, transition matrix, multinomial mixed model |
| `R/02_query_types_lca.R` | R | Scaffold | Latent class analysis with the pre-registered class selection rule; picks prototype queries |
| `R/03_study2_models.R` | R | Scaffold | Study 2 ordinal mixed models (direction, register, features) and stability metrics |

Try it:

```bash
cd scripts/python
python auto_features.py ../../data/example/example_queries.csv ../../results/example_auto_features.csv
```

Example output is in [`results/example_auto_features.csv`](../results/example_auto_features.csv).
