# Monolithic fluid–structure interaction

`monolithic_fsi` instantiates `FSISolver<dim>`. It assembles incompressible ALE fluid equations, elastic mesh equations, boundary multiplier equations and rigid-obstacle coupling in one nonlinear system.

## Unknowns and obstacle dynamics

The field unknowns are velocity, pressure, mesh position and boundary multipliers. Additional otherwise unused algebraic degrees of freedom are repurposed for the obstacle velocity when finite mass is enabled, and for a rotation angle when the rotation model is enabled. This implementation detail matters when interpreting component lists: the rigid-body variables are not independent continuum fields.

The translational model includes spring, damping and, when enabled, inertial terms. In schematic physical notation these contributions have the form \(m\ddot{\mathbf d}+c\dot{\mathbf d}+k\mathbf d\), coupled to the integrated fluid boundary multiplier. The code fixes the force sign through its multiplier residual. The zero-mass option removes the corresponding inertial model. Rotation is a constrained rigid-body motion about a specified center, with torque coupling and a rod length inferred from the initial body center; it is not a general three-dimensional free rigid-body solver.

## Enforced restrictions

The constructor rejects more than one `weak_no_slip` fluid boundary and rejects `enforce zero mean pressure` on the moving mesh. Rigid-body rotation requires `force-position coupling = all_position_to_all_lambda`; the default coupling strategy is therefore not compatible with rotation enabled. The finite-mass sparsity construction requires `local_position_master_to_lambda_accumulators` or `global_position_master_to_global_accumulator`. These choices differ from the all-to-all requirement for rotation, so combined finite-mass and rotation support must not be inferred. The listed selection values are a declaration vocabulary, not a matrix of independently validated combinations.

The pseudosolid boundary must use `coupled_to_fluid` consistently with `enable coupling`. `fix z component` constrains the corresponding translational component where applicable. Parameters controlling an idealized cylinder describe the obstacle and its force normalization; they do not themselves generate a matching mesh.

Shared methods: [elastic mesh models](elasticity.md), [physical properties](physical-properties.md), [boundary conditions](boundary-conditions.md), [spatial discretization](spatial-discretization.md), [time integration](time-integration.md), [algebraic methods](algebraic-solvers.md).

## FSI parameter declarations

These entries belong to `FSI`. Their effective use must be checked against the two distinct FSI classes. The table below reports parser constraints; it does not guarantee physically sensible positive mass, stiffness, damping or geometric dimensions.


## Implementation references

All references target the [documented revision](index.md).

- [src/monolithic_fsi_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/monolithic_fsi_solver.cpp)
- [solvers/monolithic_fsi.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers/monolithic_fsi.cpp)
- [src/fsi_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/fsi_solver.cpp)
- [src/parameters.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp)


## Parameter declaration reference

The following tables are transcribed from FEZ-owned declarations at the documented revision. `Patterns::Double()` accepts a real number; `Double(a, b)` adds bounds. `Integer` behaves similarly. `Selection` lists exact spellings; `Bool` accepts `true` or `false`. C++ expressions are retained when a pattern depends on program constants. A source description states declaration intent; applicability is qualified in the model and method text above. Empty defaults are written as `(empty)`.

### FSI

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-49"></a>`compute error on forces` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1955). |
| <a id="parameter-50"></a>`cylinder center` | `0, 0 (2D); 0, 0, 0 (3D)` | `Patterns::List(Patterns::Double(), dim, dim, ",")` | Center of the cylinder [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1946). |
| <a id="parameter-51"></a>`cylinder length` | `1` | `Patterns::Double()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1945). |
| <a id="parameter-52"></a>`cylinder radius` | `1` | `Patterns::Double()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1944). |
| <a id="parameter-53"></a>`damping` | `1` | `Patterns::Double()` | Damping coefficient of the studied system [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1936). |
| <a id="parameter-54"></a>`enable coupling` | `false` | `Patterns::Bool()` | Enable coupling between fluid and solid obstacle [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1923). |
| <a id="parameter-55"></a>`fix z component` | `true` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1954). |
| <a id="parameter-56"></a>`force-position coupling` | `local_position_master_to_all_lambda` | `Patterns::Selection( "all_position_to_all_lambda\|local_position_master_to_all_lambda\|" "global_position_master_to_all_lambda\|local_position_master_to_" "lambda_accumulators\|global_position_master_to_global_accumulator")` | Coupling strategy between force (Lagrange multiplier) and position dofs [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1959). |
| <a id="parameter-57"></a>`initial velocity` | `0, 0 (2D); 0, 0, 0 (3D)` | `Patterns::List(Patterns::Double(), dim, dim, ",")` | Center of the cylinder [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1950). |
| <a id="parameter-58"></a>`mass` | `1` | `Patterns::Double()` | Mass of the studied system [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1940). |
| <a id="parameter-59"></a>`spring constant` | `1` | `Patterns::Double()` | Spring stiffness constant attached to solid object [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1932). |
| <a id="parameter-60"></a>`use zero mass model` | `true` | `Patterns::Bool()` | Use evolution equation for the solid obstacle assuming zero mass [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1927). |
| <a id="parameter-61"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1922). |

### FSI / Rigid body rotation

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-62"></a>`center of rotation` | `0, 0 (2D); 0, 0, 0 (3D)` | `Patterns::List(Patterns::Double(), dim, dim, ",")` | Fixed center of rotation [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1976). |
| <a id="parameter-63"></a>`enable` | `false` | `Patterns::Bool()` | Enable rigid-body rotation around center of rotation [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1971). |
