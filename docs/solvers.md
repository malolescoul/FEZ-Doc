# Solvers and model selection

FEZ selects the physical problem through its executable, rather than through a single global model parameter. The entry points instantiate the following classes in two or three spatial dimensions.

| Executable | Class | Primary unknowns | Reference |
|---|---|---|---|
| `incompressible_ns` | `NSSolver<dim>` | Velocity, pressure | [Single-phase flow](incompressible-flow.md) |
| `incompressible_ns_lambda` | `NSSolverLambda<dim>` | Velocity, pressure, boundary multiplier | [Weak no-slip formulation](incompressible-flow-lambda.md) |
| `incompressible_chns` | `CHNSSolver<dim, false>` | Velocity, pressure, phase tracer, chemical potential | [Two-phase flow](two-phase-flow.md) |
| `incompressible_chns_ale` | `CHNSSolver<dim, true>` | CHNS fields and mesh position | [Moving-mesh two-phase flow](two-phase-flow-ale.md) |
| `compressible_ns` | `CompressibleNSSolver<dim>` | Velocity, pressure, temperature | [Compressible flow](compressible-flow.md) |
| `fsi` | `FSISolverLessLambda<dim>` | Fluid fields, mesh position, boundary multipliers and accumulators | [FSI formulation](fsi.md) |
| `monolithic_fsi` | `FSISolver<dim>` | Fluid fields, mesh position, multipliers; additional rigid-body variables when enabled | [Monolithic FSI](monolithic-fsi.md) |
| `linear_elasticity` | `LinearElasticitySolver<dim>` | Mesh position | [Elastic mesh model](elasticity.md) |
| `heat` | `HeatSolver<dim>` | Temperature | [Heat equation](heat.md) |

The ALE and FSI formulations distinguish physical fluid motion from the artificial elastic deformation used to move the computational mesh. A pseudosolid constitutive model describes that mesh analogy; it does not establish a general deformable-solid FSI capability.

## Reading equations and parameter tables

Equations below reproduce the assembled volume residuals. Boundary terms and algebraic constraints complete the discrete problem. Unless specified otherwise, equations are shown without user source terms; source signs are stated separately. A declared parser pattern is an input constraint, not a proof of physical admissibility, stability or solver compatibility.

The [parameter index](parameter-index.md) leads to the page owning each documented declaration. [Verified limitations](limitations.md) distinguish implementation restrictions from questions that need further scientific clarification. Practical installation and case-building guides are reserved for a later documentation stage.


## Implementation references

All references target the [documented revision](index.md).

- [CMakeLists.txt](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/CMakeLists.txt)
- [solvers/incompressible_ns.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/incompressible_ns.cpp)
- [solvers/incompressible_ns_lambda.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/incompressible_ns_lambda.cpp)
- [solvers/incompressible_chns.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/incompressible_chns.cpp)
- [solvers/incompressible_chns_ale.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/incompressible_chns_ale.cpp)
- [solvers/compressible_ns.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/compressible_ns.cpp)
- [solvers/fsi.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/fsi.cpp)
- [solvers/monolithic_fsi.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/monolithic_fsi.cpp)
- [solvers/linear_elasticity.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/linear_elasticity.cpp)
- [solvers/heat.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/heat.cpp)
