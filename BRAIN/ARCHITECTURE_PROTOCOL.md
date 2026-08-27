# Hermes Architecture Protocol v0.1

## Objective

Enable Hermes to reason about software systems as structures rather than isolated files.

## Analysis Layers

```text
SYSTEM
 ↓
SUBSYSTEM
 ↓
COMPONENT
 ↓
INTERFACE
 ↓
IMPLEMENTATION
```

## Architecture Questions

For a significant system, identify:

1. What is the system boundary?
2. What are the major responsibilities?
3. Which component owns each state/data structure?
4. How do components communicate?
5. Which dependency directions exist?
6. Where is coupling concentrated?
7. Where are failure domains?
8. What contracts must remain stable?
9. What is observable?
10. What happens when dependencies fail?
11. How can the design evolve?

## Change Assessment

Every proposed architectural change should be classified as approximately:

```text
LOCAL IMPLEMENTATION CHANGE
INTERFACE CHANGE
COMPONENT CHANGE
SUBSYSTEM CHANGE
SYSTEM ARCHITECTURE CHANGE
```

The larger the boundary affected, the stronger the need for explicit analysis and verification.

## Architecture Tradeoffs

Do not optimize for a single quality attribute. Consider, as relevant:

- correctness;
- reliability;
- simplicity;
- performance;
- resource usage;
- maintainability;
- testability;
- extensibility;
- observability;
- security;
- migration cost.

## Documentation vs Reality

Hermes should compare architectural documentation against implementation when possible. A document is not proof that the implementation conforms to it.

## Architectural Smells

Look for:

- circular dependencies;
- hidden state ownership;
- duplicated authority;
- leaky boundaries;
- excessive coupling;
- undocumented side effects;
- interface drift;
- configuration ambiguity;
- broad components with mixed responsibilities;
- architectural changes disguised as local fixes.

## Recommendation Format

For substantial architecture decisions:

```text
CURRENT STATE
PROBLEM
CONSTRAINTS
OPTIONS
TRADEOFFS
RECOMMENDATION
RISKS
MIGRATION
VERIFICATION
```
