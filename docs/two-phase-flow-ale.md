# Two-phase flow on a moving mesh

`incompressible_chns_ale` instantiates `CHNSSolver<dim, true>`. It extends the [CHNS model](two-phase-flow.md) with a mesh-position field \(\mathbf x(\mathbf X,t)\), expressed relative to reference coordinates \(\mathbf X\). Its mesh velocity is obtained from the time derivative of that field.

## ALE equations and mesh model

In the fluid and phase residuals the convective velocity becomes \(\mathbf u-\mathbf w\), with \(\mathbf w=\partial_t\mathbf x\). Time derivatives are evaluated at fixed reference coordinates. Volume integrals use the moving mapping and current geometric weights. The mesh position is solved through the [elastic pseudosolid model](elasticity.md), with constitutive parameters in `Physical properties / Pseudosolid 0`.

`Cahn Hilliard / alpha` and `beta` are declared with descriptions of mesh-source contributions proportional to \(\alpha\phi\nabla\phi\) and \(\beta[(\mathbf u-\mathbf w)\cdot\nabla\phi]\nabla\phi\). Their defaults are zero and their patterns accept unrestricted doubles. The inspected source and assemblers do not establish a consumer of these two values. They are therefore documented as declared intent, not as effective ALE mesh forcing in this revision.

## Compatibility

Mesh motion needs pseudosolid data and boundary constraints that determine the mapping. A mesh position field is not evidence that fluid–rigid-body dynamics are enabled. That coupling belongs to the [FSI solvers](fsi.md). `Mesh position degree` controls the position approximation independently of the fluid fields.

The ALE entry point calls the regular `run()` outside manufactured-solution studies. The fixed-mesh CHNS entry point explicitly selects a metric fixed-point loop when metric adaptation is requested. These workflows must not be described as interchangeable. See [mesh and adaptation](mesh-adaptation.md), [time integration](time-integration.md), [spatial discretization](spatial-discretization.md) and [boundaries](boundary-conditions.md).


## Implementation references

All references target the [documented revision](index.md).

- [solvers/incompressible_chns_ale.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/incompressible_chns_ale.cpp)
- [solvers/incompressible_chns.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/incompressible_chns.cpp)
- [src/incompressible_chns_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/incompressible_chns_solver.cpp)
- [src/assembly/incompressible_chns_assemblers.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/assembly/incompressible_chns_assemblers.cpp)
- [src/assembly/elasticity_assemblers.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/assembly/elasticity_assemblers.cpp)
