# 01_study1_descriptives.R
# ICWT Study 1, RQ1.1: how often each speech act appears, and how acts follow each other.
#
# Input: final consensus codes, one row per speech act
#   (columns: speech_act_id, participant, turn_position, primary_act, ...)
# Status: scaffold. Runs on any data with those columns; no participant data in this repo.

library(dplyr)
library(tidyr)

codes <- read.csv("data/consensus_codes.csv")   # not committed (see data/README.md)

# 1. Speech act frequencies with cluster-bootstrap 95% CIs ------------------
# Turns from the same person aren't independent, so resample PARTICIPANTS, not turns.
cluster_boot_props <- function(df, var = "primary_act", B = 2000, seed = 1) {
  set.seed(seed)
  ids <- unique(df$participant)
  levels_ <- sort(unique(df[[var]]))
  boot <- replicate(B, {
    s <- sample(ids, length(ids), replace = TRUE)
    d <- bind_rows(lapply(s, function(i) df[df$participant == i, ]))
    prop.table(table(factor(d[[var]], levels = levels_)))
  })
  data.frame(
    level    = levels_,
    prop     = as.numeric(prop.table(table(factor(df[[var]], levels = levels_)))),
    ci_low   = apply(boot, 1, quantile, 0.025),
    ci_high  = apply(boot, 1, quantile, 0.975)
  )
}

freqs <- cluster_boot_props(codes)
write.csv(freqs, "results/s1_speech_act_freqs.csv", row.names = FALSE)

# 2. Transition matrix: act at turn t -> act at turn t+1 ---------------------
transitions <- codes %>%
  group_by(participant) %>%
  arrange(turn_position, .by_group = TRUE) %>%
  mutate(next_act = lead(primary_act)) %>%
  filter(!is.na(next_act)) %>%
  count(primary_act, next_act) %>%
  group_by(primary_act) %>%
  mutate(prop = n / sum(n)) %>%
  select(-n) %>%
  pivot_wider(names_from = next_act, values_from = prop, values_fill = 0)

write.csv(transitions, "results/s1_transition_matrix.csv", row.names = FALSE)

# 3. Inferential version (TODO once data are in) -----------------------------
# Multinomial mixed model: speech_act ~ turn_position + (1 | participant)
# lme4 can't fit multinomial models, so use brms:
# library(brms)
# m <- brm(primary_act ~ turn_position + (1 | participant),
#          family = categorical(), data = codes)
