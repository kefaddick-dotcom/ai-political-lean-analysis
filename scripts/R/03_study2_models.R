# 03_study2_models.R
# ICWT Study 2: does everyday wording change how politically lopsided chatbot answers are?
#
# Unit: one LLM response, coded for lean (-2 strong left ... +2 strong right, 0 = neutral)
# and separately for refusal.
# Status: model specs only (to be pre-registered). No data yet.

library(ordinal)   # clmm
library(lme4)      # glmer

responses <- read.csv("data/study2_responses.csv")   # not collected yet

# Sum (deviation) coding: each chatbot vs. the grand average, not a reference model
responses$llm <- factor(responses$llm)
contrasts(responses$llm) <- contr.sum(nlevels(responses$llm))

# RQ2.1 Direction: is left vs. right different from 50/50?
dir_data <- subset(responses, lean != 0)
dir_data$right <- as.integer(dir_data$lean > 0)
m_dir <- glmer(right ~ 1 + (1 | case) + (1 | prototype/variant),
               family = binomial, data = dir_data)

# RQ2.2 Register: does register change the SIZE of the lean?
# Uses |lean| so a left push and a right push don't cancel out.
responses$abs_lean <- factor(abs(responses$lean), ordered = TRUE)
m_reg <- clmm(abs_lean ~ register * llm + (1 | case) + (1 | prototype/variant),
              data = responses)

# Features: which words/structures push lean left or right? (minimal-pair subset)
responses$lean_ord <- factor(responses$lean, levels = -2:2, ordered = TRUE)
m_feat <- clmm(lean_ord ~ register * llm +
                 presupposition + evaluative + clause_type + stance_disclosure +
                 (1 | case) + (1 | prototype/variant),
               data = subset(responses, minimal_pair == 1))
# If clmm struggles with random slopes, refit in brms (family = cumulative()).

# RQ2.3 Stability: same prompt, same answer?
stability <- do.call(rbind, lapply(split(responses, responses$variant), function(d) {
  s     <- sign(d$lean)
  modal <- as.numeric(names(which.max(table(s))))
  p     <- prop.table(table(d$lean))
  data.frame(variant = d$variant[1],
             flip_rate = mean(s != modal),
             entropy   = -sum(p * log2(p)))
}))
# ICC (within vs. between prompts): see Nakagawa & Schielzeth (2010), rptR package.

# Sanity check: apolitical controls should sit near zero lean.
