# FEZ documentation

FEZ is a C++ continuous Galerkin finite-element code for single- and two-phase flow and fluid–structure interaction, built on [deal.II](https://www.dealii.org/). This guide describes the official [arthurbawin/fez](https://github.com/arthurbawin/fez) repository at commit [`c6c4dd08b4ab3376062f031d577406a30a6e06bf`](https://github.com/arthurbawin/fez/tree/c6c4dd08b4ab3376062f031d577406a30a6e06bf), confirmed as the head of `master` on 16 November 2026.

## FEZ and its solvers

- [Overview and software organization](overview.md)
- [Solver selection and physical scope](solvers.md)
- [Incompressible single-phase flow](incompressible-flow.md)
- [Incompressible flow with boundary multipliers](incompressible-flow-lambda.md)
- [Incompressible two-phase flow](two-phase-flow.md)
- [Two-phase flow on a moving mesh](two-phase-flow-ale.md)
- [Compressible flow](compressible-flow.md)
- [Fluid–structure interaction: fsi](fsi.md)
- [Monolithic fluid–structure interaction](monolithic-fsi.md)
- [Elastic mesh models](elasticity.md)
- [Heat equation](heat.md)

## Common methods and reference

- [Material properties and applicability](physical-properties.md)
- [Spatial discretization and stabilization](spatial-discretization.md)
- [Time integration](time-integration.md)
- [Linear and nonlinear solution](algebraic-solvers.md)
- [Meshes and adaptation](mesh-adaptation.md)
- [Boundary conditions, initial fields and sources](boundary-conditions.md)
- [Output, restart and diagnostics](outputs.md)
- [Parameter index](parameter-index.md)
- [Verified limitations and open scientific questions](limitations.md)

## Scope and evidence

Each model page separates governing residuals, assumptions, discretization and effective parameter use. Method pages own shared parameter definitions. The index links to those definitions without repeating defaults. Source links are pinned to the documented commit, rather than to a moving branch.

This edition is a source-audited reference. It includes declaration tables and identified compatibility restrictions; it does not claim numerical validation of every parameter combination. The parameter inventory explicitly identifies delegated function data that still need a separate exhaustive reference. Installation, case creation, launching calculations and worked examples are reserved for a later stage.

The historical atlas and earlier reference snapshots remain unchanged outside `docs/`. They are separate historical material and are not evidence for the current master guide. The [documentation maintenance note](documentation-maintenance.md) records coverage and a proposed local-preview organization; no hosting or publication is configured by this guide.
