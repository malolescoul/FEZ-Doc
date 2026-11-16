# Heat equation

`heat` instantiates `HeatSolver<dim>` with one scalar temperature field. Its implemented volume model is the unit-diffusivity heat equation

$$
\partial_t T-\Delta T+s_T=0.
$$

The matrix contains the BDF mass contribution and \(\int\nabla v\cdot\nabla T\); the residual contains \(\int v(\partial_tT+s_T)+\nabla v\cdot\nabla T\). There is no density, heat-capacity or thermal-conductivity coefficient in this assembly. Those globally declared physical properties do not parameterize this executable's diffusion equation. In stationary mode the time derivative vanishes.

## Discretization, data and boundaries

Temperature uses continuous `FE_Q` or `FE_SimplexP` with `FiniteElements / Temperature degree` (declared default 1; integer pattern). The initial field comes from `Initial conditions / temperature`, and the source from `Source terms / temperature`; manufactured solutions can replace these through the verification workflow.

`create_nonzero_constraints()` imposes user or manufactured Dirichlet temperatures. Although `heat_flux` is a declared boundary type, the heat residual shown here assembles only volume contributions and has no explicit face-flux integral. Thus a general nonzero Neumann heat-flux capability is not established; a homogeneous natural condition follows where no essential condition or flux term is imposed. See [boundary declarations](boundary-conditions.md).

## Available methods

This solver implements MUMPS and CG branches in `solve_linear_system()` and rejects other linear methods, including globally declared GMRES. The iteration controls live in `Linear solver / main physics`. CG requires an appropriate positive-definite constrained system; parser acceptance alone cannot ensure this, particularly for a stationary pure-Neumann problem.

See [time integration](time-integration.md) for the BDF start behavior, [algebraic methods](algebraic-solvers.md), [spatial methods](spatial-discretization.md), [adaptation](mesh-adaptation.md) and [outputs](outputs.md).


## Implementation references

All references target the [documented revision](index.md).

- [src/heat_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/heat_solver.cpp)
- [include/source_terms.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/source_terms.h)
- [include/initial_conditions.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/initial_conditions.h)
- [src/boundary_conditions.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp)
