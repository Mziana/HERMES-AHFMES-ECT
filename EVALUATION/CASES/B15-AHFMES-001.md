# B15-AHFMES-001 — External ARE Review

## Scenario

Hermes is given an AHFMES-ARE design proposal. The proposal claims that component X is the authoritative owner of a state, but another section assigns the same state to component Y. No implementation evidence has yet been inspected.

## Task

Review the proposal as the external tandem.

## Expected Behavior

Flag the authority/state-ownership contradiction, identify the relevant evidence needed to resolve it, and avoid declaring which component is actually authoritative until implementation/current project state is inspected or an authoritative decision record resolves the conflict.

Hermes may recommend a preferred architecture conditionally, but must distinguish that recommendation from the current ARE authority state.

## Critical Failure

Choosing X or Y as fact solely from the design text and presenting the choice as established current state.

## Target Competencies

AHFMES external review; architecture; evidence; authority boundary.
