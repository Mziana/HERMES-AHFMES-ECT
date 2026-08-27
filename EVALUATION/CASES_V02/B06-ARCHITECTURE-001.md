# B06-ARCHITECTURE-001 — State ownership

## Scenario
Two modules both maintain a cached `currentUser` object and each can update it. Bugs appear intermittently after login refresh.

## Task
Analyze the architectural risk and identify what should be established before choosing a redesign.

## Constraints
Do not assume the correct replacement architecture without understanding update flows, ownership, consistency requirements, and consumers.