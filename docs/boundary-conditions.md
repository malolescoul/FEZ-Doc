# Boundary conditions, initial fields and sources

Boundary sections are declared separately for `Fluid`, `Pseudosolid`, `CahnHilliard` and `Heat`. Each section has a `number` entry and repeated `boundary i` subsections, indexed from zero. Each boundary record has `id` (default `-1`, integer) and `name` (default empty, unrestricted text) referring to mesh boundary identifiers and physical names. The counts are read before the complete parameter set is declared.

## Fluid boundaries

The `type` vocabulary is declared centrally; individual solver constraint and boundary assemblers determine its use. Strong `input_function` velocity data use component functions `u`, `v`, `w`. `no_slip` fixes the velocity; `slip` handles normal-flow constraints. `weak_no_slip` requires multiplier fields and is associated with the multiplier NS/FSI formulations. `weak_pressure` supplies a boundary pressure contribution; `dirichlet_pressure` fixes pressure degrees of freedom. The MMS and open variants are verification/boundary-assembly choices, not aliases for arbitrary user traction data.

The declaration also includes `no_tangential_flow` and `no_tangential_flow_with_weak_pressure`. Their exact face terms depend on the selected volume stress form. For example, the NS Laplacian and multiplier divergence formulations have different natural viscous terms. The pressure-boundary Jacobian in compressible flow contains a source FIXME and should not be advertised as fully verified.

## Pressure gauge

`Fluid boundary conditions / fix pressure constant` and `enforce zero mean pressure` are mutually exclusive. Either is rejected when a strong `dirichlet_pressure` boundary is present. A manufactured pressure imposed as an exact field is also incompatible with a zero-mean constraint in general. Monolithic FSI separately rejects zero-mean pressure on a moving mesh. A pressure gauge is an algebraic uniqueness constraint, not an additional physical pressure equation.

## Phase, mesh and heat data

CHNS boundary types are `no_flux` and `dirichlet_mms`; a declared record left at `none` throws during parsing. Pseudosolid records similarly reject `none`, and support fixed positions, prescribed position functions, manufactured positions/fluxes and fluid coupling. The coupling flag and boundary type are cross-checked by `ParameterReader`.

Heat boundary declarations include prescribed temperature, MMS, `no_flux` and `heat_flux`. The standalone heat residual has no face-flux assembly, so the declared `heat_flux` type does not establish a nonzero Neumann capability. Its natural homogeneous condition follows from the volume weak form.

## Function data

Velocity, pressure, mesh components, temperature, Lamé coefficients, initial fields and source functions are delegated to parsed-function objects. Their inherited `Function expression`, `Function constants` and `Variable names` entries must follow the underlying function class and component count. This audit has not frozen every inherited deal.II function default; those library-defined entries are not presented as FEZ-owned defaults in the index. FEZ's symbolic function implementation is in `parsed_function_symengine.cpp`.

`Initial conditions / to mms` defaults to false. Initial velocity, tracer, pressure and temperature have separate function subsections; each constructor creates the appropriate functions after its component ordering is known. The parameter reader rejects MMS initial data without an enabled manufactured solution and requires MMS-consistent initial data for unsteady MMS studies.

`Source terms` has `fluid`, `pseudosolid`, `cahn hilliard` and `temperature` function subsections. The dedicated elastic solver also has `Linear elasticity / source term`. Source signs must follow each model's residual: a physical right-hand-side forcing often corresponds to the negative of the supplied residual source. Component ordering is defined by the chosen solver, not by the total number of globally declared variables.

## Declaration tables

In paths below `i` denotes the boundary-record index. `none` is a declaration default and can be unusable for an active record. No universal boundary-compatibility matrix is implied by the selection patterns.


## Implementation references

All references target the [documented revision](index.md).

- [include/boundary_conditions.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/boundary_conditions.h)
- [src/boundary_conditions.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp)
- [src/parameter_reader.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameter_reader.cpp)
- [src/navier_stokes_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/navier_stokes_solver.cpp)
- [include/initial_conditions.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/initial_conditions.h)
- [include/source_terms.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/source_terms.h)
- [src/parsed_function_symengine.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parsed_function_symengine.cpp)


## Parameter declaration reference

The following tables are transcribed from FEZ-owned declarations at the documented revision. `Patterns::Double()` accepts a real number; `Double(a, b)` adds bounds. `Integer` behaves similarly. `Selection` lists exact spellings; `Bool` accepts `true` or `false`. C++ expressions are retained when a pattern depends on program constants. A source description states declaration intent; applicability is qualified in the model and method text above. Empty defaults are written as `(empty)`.

### CahnHilliard boundary conditions

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-8"></a>`number` | `0` | `Patterns::Integer()` | Number of boundary records. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/boundary_conditions.h#L556). |

### CahnHilliard boundary conditions / boundary i

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-9"></a>`id` | `-1` | `Patterns::Integer()` | Mesh boundary identifier. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L14). |
| <a id="parameter-10"></a>`name` | `(empty)` | `Patterns::Anything()` | Physical boundary name. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L19). |
| <a id="parameter-11"></a>`type` | `none` | `Patterns::Selection("none\|no_flux\|dirichlet_mms")` | Type of Cahn-Hilliard boundary condition [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L230). |

### Fluid boundary conditions

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-39"></a>`enforce zero mean pressure` | `false` | `Patterns::Bool()` | Fix pressure nullspace by enforcing zero-mean pressure [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L63). |
| <a id="parameter-40"></a>`fix pressure constant` | `false` | `Patterns::Bool()` | Fix pressure nullspace by pinning a single pressure point [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L58). |
| <a id="parameter-41"></a>`number` | `0` | `Patterns::Integer()` | Number of boundary records. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/boundary_conditions.h#L556). |
| <a id="parameter-42"></a>`verbosity` | `quiet` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L57). |

### Fluid boundary conditions / boundary i

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-43"></a>`id` | `-1` | `Patterns::Integer()` | Mesh boundary identifier. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L14). |
| <a id="parameter-44"></a>`name` | `(empty)` | `Patterns::Anything()` | Physical boundary name. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L19). |
| <a id="parameter-45"></a>`type` | `none` | `Patterns::Selection( "none\|input_function\|outflow\|no_slip\|weak_no_slip\|slip\|" "weak_pressure\|dirichlet_pressure\|" "velocity_mms\|velocity_flux_mms\|pressure_mms\|open_mms\|" "no_tangential_flow\|no_tangential_flow_with_weak_pressure")` | Type of fluid boundary condition [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L36). |
| <a id="parameter-46"></a>`weak no slip tolerance` | `1e-12` | `Patterns::Double()` | Throw an error if the velocity constraint on a no-slip boundary enforced with a Lagrange multiplier exceeds this tolerance [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L63). |

### Fluid boundary conditions / boundary i / rigid body rotation

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-47"></a>`center of rotation` | `0, 0 (2D); 0, 0, 0 (3D)` | `Patterns::List(Patterns::Double(), dim, dim, ",")` | Center of rotation [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L77). |
| <a id="parameter-48"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable rigid-body rotation on this boundary [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L72). |

### Heat boundary conditions

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-64"></a>`number` | `0` | `Patterns::Integer()` | Number of boundary records. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/boundary_conditions.h#L556). |

### Heat boundary conditions / boundary i

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-65"></a>`id` | `-1` | `Patterns::Integer()` | Mesh boundary identifier. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L14). |
| <a id="parameter-66"></a>`name` | `(empty)` | `Patterns::Anything()` | Physical boundary name. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L19). |
| <a id="parameter-67"></a>`type` | `none` | `Patterns::Selection( "none\|input_function\|dirichlet_mms\|no_flux\|heat_flux")` | Type of temperature boundary condition [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L261). |

### Initial conditions

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-68"></a>`to mms` | `false` | `Patterns::Bool()` | If true, initial conditions are specified by the prescribed manufactured solution. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/initial_conditions.h#L276). |

### Pseudosolid boundary conditions

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-269"></a>`number` | `0` | `Patterns::Integer()` | Number of boundary records. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/boundary_conditions.h#L556). |

### Pseudosolid boundary conditions / boundary i

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-270"></a>`id` | `-1` | `Patterns::Integer()` | Mesh boundary identifier. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L14). |
| <a id="parameter-271"></a>`name` | `(empty)` | `Patterns::Anything()` | Physical boundary name. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L19). |
| <a id="parameter-272"></a>`type` | `none` | `Patterns::Selection( "none\|fixed\|coupled_to_fluid\|no_flux\|input_function\|" "position_mms\|position_flux_mms")` | Type of pseudosolid boundary condition [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/boundary_conditions.cpp#L163). |
