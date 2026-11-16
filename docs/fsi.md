# Fluid–structure interaction: `fsi`

`fsi` instantiates `FSISolverLessLambda<dim>`. The constructor builds fluid velocity, pressure, mesh position and boundary multiplier fields. The class name does not mean that all multipliers are absent: its implementation also introduces force accumulators and position constraints.

## Physical scope and coupling

The fluid uses an incompressible Newtonian ALE formulation, with convective velocity \(\mathbf u-\partial_t\mathbf x\), divergence-form viscous stress and boundary multiplier coupling. Elastic pseudosolid equations govern the computational mesh. The obstacle's rigid translation is tied to the integrated boundary multiplier and a spring stiffness. This is not a general continuum solid deformation model.

The position-constraint construction uses the reciprocal `FSI / spring constant`. A zero spring stiffness is accepted by the generic double parser but is not a usable value for this construction. The force/displacement convention is checked in the code against a negative spring stiffness ratio.

## Parameters and compatibility

`FSI / enable coupling` must agree with a pseudosolid boundary of type `coupled_to_fluid`. The common parameter reader rejects an enabled coupling without such a boundary and rejects that boundary type when coupling is disabled. Weak no-slip fluid data supply the multiplier coupling.

The full FSI declaration table is owned by the [monolithic FSI page](monolithic-fsi.md). In particular, `mass`, `damping`, `use zero mass model` and `Rigid body rotation` being declared by `ParameterReader` does not imply that this older class uses them: its force-position construction is spring-based. Finite-mass and rotation equations must be associated with the explicit implementation in `FSISolver`, not transferred to this class by name.

The solver uses hp spaces with inactive multiplier components away from relevant boundaries. See [spatial methods](spatial-discretization.md), [elastic mesh models](elasticity.md), [boundaries](boundary-conditions.md), [time integration](time-integration.md) and [algebraic methods](algebraic-solvers.md). Mesh adaptation compatibility for every FSI configuration has not been established by a runtime test in this documentation audit.


## Implementation references

All references target the [documented revision](index.md).

- [src/fsi_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/fsi_solver.cpp)
- [solvers/fsi.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/fsi.cpp)
- [src/assembly/lagrange_multiplier_assemblers.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/assembly/lagrange_multiplier_assemblers.cpp)
- [src/parameter_reader.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameter_reader.cpp)
