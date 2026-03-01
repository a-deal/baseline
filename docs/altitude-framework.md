# Altitude Framework

## The Model

Health data complexity operates at different altitudes. Each altitude has a different audience size, different trade-offs, and different product implications. The altitude you're building at determines what scales and what doesn't.

---

## The Altitudes

### 10,000 ft — Signal Detection
**What**: Do you have labs? Exercise? Sleep tracked? Yes/no.
**Product**: Landing page calculator, rough coverage estimate.
**Audience**: Everyone. Zero barrier.
**Scales**: Infinitely. Same 8 questions for everyone.
**Trade-off**: Low resolution. Can't differentiate someone healthy from someone at risk.
**What you learn**: Whether someone is paying attention at all.

### 5,000 ft — Measurement & Benchmarking
**What**: Actual values, NHANES percentile ranking, tier-weighted scoring, gap analysis, "next 3 moves."
**Product**: The Baseline app. Voice intake → coverage score → actionable gaps.
**Audience**: Anyone willing to look at their numbers. Still scalable.
**Scales**: Yes — the tiered metrics (T1/T2) are the same for everyone. ApoB is ApoB whether you're 25 or 55. The *percentile comparison* is age/sex-adjusted, but the framework is universal.
**Trade-off**: Tells you *where you stand*, not *what to do about it* in your specific context. "Your LDL is 75th percentile" is useful. "Here's how to lower it given your genetics, medications, and goals" is a different altitude.
**What you learn**: What to measure next, how you compare, where the gaps are.

**This is where Baseline lives as a product.**

### 1,000 ft — Protocol & Intervention
**What**: Specific actions based on your data. Cut protocols, peptide stacks, sleep optimization, cardiac risk mitigation, supplementation.
**Product**: Doesn't exist yet as a product. This is what Andrew does as a guinea pig — tracking a cut with tirzepatide, managing HRV during caloric deficit, designing refeed timing around Garmin recovery data.
**Audience**: Shrinks fast. People who know their numbers AND want to act on them.
**Scales**: Partially. Some protocols are reusable patterns ("if ApoB > 90 and no statin, here's the decision tree"). But the *application* is individual.
**Trade-off**: Requires context the product doesn't have — goals, preferences, risk tolerance, medical history beyond what we score. A coverage score can tell you your HbA1c is high. It can't tell you whether to try metformin, berberine, or dietary intervention first. That depends on your doctor, your worldview, your body.
**What you learn**: What works *for you*. N=1 experimentation.

### 500 ft — Personalized Intelligence
**What**: Longitudinal pattern recognition. "Your HRV drops 15% every time you travel." "Your fasting glucose trends up in months you sleep < 6.5 hours." "Your LDL responds to dietary saturated fat more than most people."
**Product**: Future. Requires time-series data, enough observations to detect patterns, and a model that can distinguish signal from noise.
**Audience**: Small. People with 6+ months of data across multiple domains.
**Scales**: The *engine* scales (pattern detection is algorithmic). The *insights* don't — they're unique to each person.
**Trade-off**: Requires sustained data collection. Most people won't stick around long enough to generate meaningful longitudinal data. The product must create enough value at 5,000 ft to retain people until 500 ft insights emerge.

### Ground Level — Clinical / Genomic
**What**: Genetic risk scores, pharmacogenomics (how you metabolize drugs), epigenetic clocks, continuous glucose monitoring correlation, microbiome analysis.
**Product**: InsideTracker, Function Health, clinical concierge medicine.
**Audience**: Tiny. Expensive. Often requires clinical interpretation.
**Scales**: No. Each result requires individual interpretation. This is the domain of doctors, genetic counselors, and personalized medicine.
**Trade-off**: Maximum insight, minimum scale. Also highest cost and regulatory complexity.

---

## Where Does Personalization Take Off?

The boundary is between **5,000 ft** and **1,000 ft**.

At 5,000 ft, the metrics are universal. Everyone benefits from knowing their ApoB, blood pressure, and HbA1c. The scoring framework (tiers, weights, percentiles) is the same for a 25-year-old woman and a 55-year-old man — the *benchmarks* are adjusted, but the *system* is identical. This is the scalable backbone.

At 1,000 ft, it becomes about *what you do with the data*, and that's where individual context dominates:

- **Goals matter**: Are you optimizing for longevity, athletic performance, body composition, disease prevention, or cognitive function? The same biomarker profile leads to different actions depending on the goal.
- **Worldview matters**: Do you trust conventional medicine? Are you open to off-label interventions? Do you want the aggressive optimization path or the conservative one?
- **Biology matters**: Some people are hyper-responders to dietary cholesterol. Some people metabolize caffeine slowly. Some people's HRV is naturally low. The standard percentile becomes less useful when you know your individual baseline.

**The product question**: Can Baseline create enough value at 5,000 ft (scalable) to retain users until 1,000 ft (personalized) and eventually 500 ft (intelligent) insights become possible?

The answer is probably yes — *if the 5,000 ft experience is good enough*. The coverage score, gap analysis, and "next 3 moves" create immediate value. The insight carousel plants seeds ("did you know Lp(a) only needs to be tested once?"). The tracking CTA captures intent. Each altitude funds the next.

---

## Phase Implications

| Phase | Altitude | What We Build | Risk Check |
|-------|----------|---------------|------------|
| Now (v1) | 5,000 ft | Voice intake → score → gaps → next moves | Are we adding complexity that belongs at 1,000 ft? |
| Next (v2) | 5,000 ft + 1,000 ft bridge | Longitudinal tracking, trend detection, freshness decay | Are we building tracking before the score is sticky? |
| Later | 1,000 ft | Protocol templates, intervention tracking, N=1 experiments | Are we trying to scale what's inherently personal? |
| Eventually | 500 ft | Pattern recognition across time-series, personalized alerts | Do we have enough data to be useful here? |

**The altitude check**: Before building a feature, ask "what altitude is this?" If the answer is lower than where we are, it's scope creep. If it's the right altitude but wrong phase, it's premature. The altitude framework makes this explicit.

---

## The Andrew Layer

Andrew's personal use (cut tracking, peptide protocols, sleep optimization, Garmin deep dives) lives at 1,000 ft and below. This is:
- **Content source**: The experience generates authentic insights for posts and threads
- **Product R&D**: Guinea-pigging features before they're productized
- **Not the product itself**: This level of engagement doesn't scale, and shouldn't try to

The trick is knowing which 1,000 ft insights are *generalizable* ("refeed days during a cut restore strength if the issue is caloric, not sleep debt") and which are *personal* ("Andrew's HRV drops below 50 when he sleeps < 6 hours and is in a deficit"). The generalizable ones become content. The personal ones stay in the dashboard.
