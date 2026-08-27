# Preliminary Training Gap — Blind v0.2

This is a qualitative analysis of the first five inspected responses from the 2026-08-27 blind run. It is not an official aggregate score.

## Strengths observed

- consistently separates evidence, inference, assumptions, and unknowns;
- usually proposes concrete inspection or verification steps;
- understands recommendation versus authority boundaries;
- recognizes that implementation is not verified merely because it is plausible;
- uses appropriate architecture vocabulary around ownership, consistency, coupling, and trade-offs.

## Gaps observed

### 1. Unsupported assumptions
B05 explicitly introduced assumptions such as the implementation being correct and the null being a valid input, despite no evidence supporting those assumptions. This is contrary to the evidence-discipline objective.

### 2. Premature causal confidence
B06 called the duplicated `currentUser` state "likely the root cause" when the scenario only established a correlation and listed missing architectural evidence. The model should distinguish a plausible hypothesis from a likely root cause more carefully.

### 3. Generic boilerplate
Several responses reproduce a long template of observations/inferences/assumptions/unknowns even when a shorter answer would be more useful. Training should reward decision-relevant structure rather than fixed headings.

### 4. Restatement over resolution
Some responses spend substantial space restating the scenario instead of converting the evidence into a prioritized engineering action. Training should emphasize concise synthesis and prioritization.

### 5. Trade-off precision
B13 correctly identified missing requirements but used generic pros/cons. Future examples should force explicit decision criteria, failure-mode analysis, and conditions under which each architecture wins.

### 6. Authority overreach risk
B15 proposed explicit authorization and review steps appropriately, but training should distinguish when authorization is actually required from when Hermes is merely providing analysis.

## Training implication
Do not simply add more examples of the current template. Build contrastive examples where:

- a plausible assumption is explicitly rejected;
- a hypothesis is downgraded when evidence is weak;
- a concise answer beats a verbose checklist;
- two valid architectures are compared using measurable constraints;
- authority is invoked only when an action crosses an actual authority boundary;
- the model must revise an answer after new evidence.

## Gate
This report does not authorize full training. Corrected V0.2 execution and independent semantic scoring remain required before selecting the final training corpus.
