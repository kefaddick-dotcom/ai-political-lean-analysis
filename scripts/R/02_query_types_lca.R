# 02_query_types_lca.R
# ICWT: find recurring query types with latent class analysis (poLCA).
#
# Plan (from the coding framework):
#   - 5 to 8 indicator codes only; ~300 speech acts is borderline for LCA
#   - merge near-duplicate codes (LCA assumes local independence)
#   - fit 1..K classes; pick lowest BIC unless a class is < 5% or not
#     distinguishable, then take the next-lowest (pre-register this rule)
#   - prototype per class = real query with highest membership probability
#     that matches the class's modal profile
# Status: scaffold, no data in repo.

library(poLCA)

codes <- read.csv("data/consensus_codes.csv")   # not committed

# poLCA needs integer-coded factors starting at 1
indicators <- c("primary_act", "directness", "presup_yn",
                "evaluative_yn", "stance_disclosure_yn", "clause_type")
lca_data <- as.data.frame(lapply(codes[indicators], function(x) as.integer(factor(x))))

f <- as.formula(paste("cbind(", paste(indicators, collapse = ","), ") ~ 1"))

fits <- lapply(1:6, function(k) poLCA(f, lca_data, nclass = k, nrep = 20, verbose = FALSE))

fit_table <- data.frame(
  k        = 1:6,
  BIC      = sapply(fits, `[[`, "bic"),
  min_size = sapply(fits, function(m) min(m$P))
)
print(fit_table)

# Selection rule (pre-registered)
ok   <- fit_table$min_size >= 0.05
best <- fit_table$k[ok][which.min(fit_table$BIC[ok])]
m    <- fits[[best]]

codes$lca_class <- m$predclass
codes$lca_prob  <- apply(m$posterior, 1, max)

# Prototype = most typical real query per class
prototypes <- do.call(rbind, lapply(split(codes, codes$lca_class), function(d) d[which.max(d$lca_prob), ]))

write.csv(fit_table,  "results/lca_fit_table.csv",  row.names = FALSE)
write.csv(prototypes, "results/lca_prototypes.csv", row.names = FALSE)

# Robustness check (Python): Sentence-BERT embeddings + HDBSCAN within each
# speech act, k-means + silhouette as a second check. If LCA classes and
# embedding clusters roughly agree, the query types are robust.
