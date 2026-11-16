# Incompressible single-phase flow

`incompressible_ns` instantiates `NSSolver<dim>` on a fixed mesh. Its unknowns are velocity \(\mathbf u\) and pressure \(p\). The formulation uses the kinematic viscosity of fluid 0, and its momentum residual is divided by density. Consequently its pressure variable has the role of kinematic pressure, unlike the force-unit pressure in CHNS.

## Equations and assumptions

With constant kinematic viscosity \(\nu\), the unstabilized volume problem is

$$
\partial_t\mathbf u+(\mathbf u\cdot\nabla)\mathbf u
+\nabla p-\nu\Delta\mathbf u+\mathbf s_u=0,
\qquad \nabla\cdot\mathbf u=s_p.
$$

Here `Source terms / fluid` supplies the velocity and pressure source components. The zero-source model is incompressible Newtonian flow. The volume assembler does not insert `Physical properties / body force` in this formulation; an acceleration source must follow the residual sign convention above. Fluid density and dynamic viscosity are globally declared but do not replace `kinematic viscosity` in this volume model.

## Discretization and boundaries

The constructor builds continuous `FE_Q` or `FE_SimplexP` velocity and pressure fields. The default degrees are 2 and 1. Equal-order settings being accepted by the parser does not establish stability of an unstabilized mixed formulation. See [spatial discretization](spatial-discretization.md), [time integration](time-integration.md) and [algebraic solvers](algebraic-solvers.md).

`setup_assemblers()` selects the Laplacian viscous form, with optional SUPG/PSPG terms through `Stabilization / enable supg`. Strong velocity data, no-slip and pressure constraints are handled by the common Navier–Stokes constraint machinery; open and weak pressure conditions add boundary terms. [Boundary conditions](boundary-conditions.md) documents the declaration vocabulary and pressure-gauge incompatibilities. `weak_no_slip` requires the [multiplier formulation](incompressible-flow-lambda.md).

## Model parameters

The [fluid property declarations](physical-properties.md) define `Physical properties / Fluid 0 / kinematic viscosity`. Only that viscosity is consumed by the NS volume diffusion term. `FiniteElements / Velocity degree` and `Pressure degree`, plus quadrature and mapping choices, are detailed with [spatial methods](spatial-discretization.md). Shared Newton, linear-solve, time, mesh and output controls retain their own pages.


## Implementation references

All references target the [documented revision](index.md).

- [src/incompressible_ns_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/incompressible_ns_solver.cpp)
- [src/assembly/incompressible_ns_assemblers.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/assembly/incompressible_ns_assemblers.cpp)
- [src/navier_stokes_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/navier_stokes_solver.cpp)
- [src/scratch_data.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/scratch_data.cpp)
