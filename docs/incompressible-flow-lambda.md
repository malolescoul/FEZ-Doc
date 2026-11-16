# Incompressible flow with boundary multipliers

`incompressible_ns_lambda` instantiates `NSSolverLambda<dim>`. It adds a vector Lagrange multiplier to velocity and pressure to impose a weak no-slip boundary constraint. This is a distinct executable; enabling a boundary parameter does not add multiplier unknowns to `NSSolver`.

## Model and discrete formulation

The fluid volume model is incompressible Newtonian flow with the kinematic viscosity of fluid 0. This solver selects the divergence form of the viscous stress, giving \(-\nabla\cdot(2\nu D(\mathbf u))\), where \(D(\mathbf u)=(\nabla\mathbf u+\nabla\mathbf u^T)/2\). The multiplier assembler adds boundary velocity–multiplier coupling to impose the prescribed no-slip relation. The precise multiplier sign and force conversion must be taken from the coupled boundary residual, rather than inferred from a generic traction convention.

The implementation uses an `hp::FECollection`: velocity and pressure exist throughout the fluid domain; the additional multiplier field is represented through spaces with and without multiplier components, including `FE_Nothing`. This use of hp machinery localizes fields and should not be interpreted as an automatic polynomial adaptation algorithm. The 3D simplex implementation includes custom DoF-identity handling.

## Parameters and boundaries

`Fluid boundary conditions / boundary i / type = weak_no_slip` activates the relevant boundary treatment. `FiniteElements / Lagrange multiplier degree` controls the boundary multiplier approximation (declared default 2; integer pattern). The common boundary page gives `weak no slip tolerance` and the available data functions. Fluid properties follow the [single-phase model](incompressible-flow.md); the additional CHNS and compressible-property declarations do not change this model.

The assembler selection in this class passes `divergence_form` without a stabilization flag. A globally declared `Stabilization / enable supg` must therefore not be advertised as effective in this executable. See [limitations](limitations.md), [spatial methods](spatial-discretization.md), [time integration](time-integration.md) and [algebraic methods](algebraic-solvers.md).


## Implementation references

All references target the [documented revision](index.md).

- [src/incompressible_ns_solver_lambda.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/incompressible_ns_solver_lambda.cpp)
- [src/assembly/lagrange_multiplier_assemblers.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/assembly/lagrange_multiplier_assemblers.cpp)
- [src/assembly/incompressible_ns_assemblers.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/assembly/incompressible_ns_assemblers.cpp)
