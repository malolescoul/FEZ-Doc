# FEZ documentation

FEZ is a C++ finite element code for fluid mechanics and fluid–structure interaction, built on [deal.II](https://www.dealii.org/). This documentation describes the official FEZ repository at commit [`c6c4dd08b4ab3376062f031d577406a30a6e06bf`](https://github.com/arthurbawin/fez/tree/c6c4dd08b4ab3376062f031d577406a30a6e06bf).

## Contents

- [FEZ overview](overview.md): scope, executable entry points and the parameter system.

The documentation is being developed. Solver-specific models and parameters, common numerical methods, and a parameter index will be added as they are checked against the source. Installation, execution and example workflows will be documented separately.

## Documentation scope

A solver page describes its physical model, assumptions, unknowns, discretization, boundary conditions and relevant parameters. Shared numerical methods are documented independently and linked from the solver pages. Parameter names, accepted values and defaults are taken from the implementation; the existence of a declared option alone does not imply support by every solver.

The previous atlas and reference material remain in the repository outside this directory. They describe earlier snapshots and are not the reference for this documentation.
