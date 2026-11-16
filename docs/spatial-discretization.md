# Spatial discretization and stabilization

FEZ constructs continuous Galerkin finite-element spaces with deal.II. `FiniteElements / use quads = false` selects simplex elements (`FE_SimplexP`); `true` selects tensor-product elements (`FE_Q`). Only fields present in the selected solver are instantiated. Changing `Temperature degree` in a model without temperature does not add a heat equation.

## Geometry and integration

The fixed mapping has a separately selected degree. Moving-mesh solvers use the position field to describe the current configuration, so position degree and fixed reference-mapping degree have different roles. Quadrature has separate subsections for assembly and error evaluation. The accepted simplex rule names and node counts are declaration controls; actual quadrature construction is in `FiniteElements::create_quadrature_rule` and the generic geometry setup. A degree combination accepted as integers is not automatically a stable mixed finite-element pair.

Multiplier solvers use spaces with and without multiplier components in an hp collection to activate degrees of freedom near selected boundaries. This does not imply a general adaptive choice of polynomial degree. Hanging-node and essential constraints are built before constrained local contributions are distributed into the global matrix and residual.

## Stabilization

`Stabilization / enable supg` declares momentum SUPG/PSPG and `enable tracer supg` declares phase-tracer SUPG. Both default to false. SUPG tests the strong residual along the convective direction; PSPG adds a pressure-gradient test of the momentum residual. CHNS treats its momentum residual in force units and uses a pressure test scaled by inverse density. The strong viscous residual includes viscosity-gradient terms in CHNS.

The flags are effective in `NSSolver` and the CHNS assembler setup. `NSSolverLambda` selects divergence form without a stabilization flag; its shared parameter declarations must not be treated as confirmation that it uses SUPG. The FSI setup likewise needs its explicit assembly flags inspected. No SUPG capability is inferred for the heat or compressible assemblers from the global declarations.

`stabilization_tools.h` defines the characteristic-time formulas and geometric estimates. Their presence is not a universal stability guarantee. Temporal contributions use the leading BDF coefficient; ALE uses relative convective velocity. See [time integration](time-integration.md).

## Parameter declarations

`Patterns::Integer()` and `Patterns::Double()` below mean parser acceptance without the positive lower bound that might be needed by the algorithm. `Quadrature rule for error` repeats the same entry names with a potentially different default node count; its helper has an `error` argument, retained explicitly below.


## Implementation references

All references target the [documented revision](index.md).

- [src/parameters.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp)
- [src/navier_stokes_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/navier_stokes_solver.cpp)
- [src/incompressible_ns_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/incompressible_ns_solver.cpp)
- [src/incompressible_ns_solver_lambda.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/incompressible_ns_solver_lambda.cpp)
- [include/assembly/incompressible_chns_assemblers.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/assembly/incompressible_chns_assemblers.h)
- [include/stabilization_tools.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/stabilization_tools.h)


## Parameter declaration reference

The following tables are transcribed from FEZ-owned declarations at the documented revision. `Patterns::Double()` accepts a real number; `Double(a, b)` adds bounds. `Integer` behaves similarly. `Selection` lists exact spellings; `Bool` accepts `true` or `false`. C++ expressions are retained when a pattern depends on program constants. A source description states declaration intent; applicability is qualified in the model and method text above. Empty defaults are written as `(empty)`.

### FiniteElements

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-24"></a>`Lagrange multiplier degree` | `2` | `Patterns::Integer()` | Polynomial degree of the no-slip Lagrange multiplier interpolant [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L813). |
| <a id="parameter-25"></a>`mapping degree` | `1` | `Patterns::Selection("isoparametric velocity\|1\|2\|3\|4\|5")` | Degree of the reference-to-physical mapping, or degree of the velocity approximation if set to isoparametric [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L832). |
| <a id="parameter-26"></a>`Mesh position degree` | `1` | `Patterns::Integer()` | Polynomial degree of the mesh position interpolant [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L809). |
| <a id="parameter-27"></a>`Potential degree` | `1` | `Patterns::Integer()` | Polynomial degree of the CHNS chemical potential interpolant [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L822). |
| <a id="parameter-28"></a>`Pressure degree` | `1` | `Patterns::Integer()` | Polynomial degree of the pressure interpolant [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L805). |
| <a id="parameter-29"></a>`Temperature degree` | `1` | `Patterns::Integer()` | Polynomial degree of the temperature interpolant [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L827). |
| <a id="parameter-30"></a>`Tracer degree` | `1` | `Patterns::Integer()` | Polynomial degree of the CHNS tracer interpolant [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L818). |
| <a id="parameter-31"></a>`use quads` | `false` | `Patterns::Bool()` | If true, use quads/hexes instead of simplices [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L797). |
| <a id="parameter-32"></a>`Velocity degree` | `2` | `Patterns::Integer()` | Polynomial degree of the velocity interpolant [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L801). |

### FiniteElements / Quadrature rule

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-33"></a>`number of 1d nodes for cell quadrature` | `4` | `Patterns::Integer()` | Number of nodes in the base 1d quadrature. Will integrate a polynomial of degree 2n-1. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L780). |
| <a id="parameter-34"></a>`number of 1d nodes for face quadrature` | `4` | `Patterns::Integer()` | Number of nodes in the base 1d quadrature. Will integrate a polynomial of degree 2n-1. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L785). |
| <a id="parameter-35"></a>`rule for simplices` | `gauss` | `Patterns::Selection("gauss\|witherden_vincent")` | Gauss or Witherden-Vincent (odd order) rule. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L776). |

### FiniteElements / Quadrature rule for error

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-36"></a>`number of 1d nodes for cell quadrature` | `6 (2D), 5 (3D)` | `Patterns::Integer()` | Number of nodes in the base 1d quadrature. Will integrate a polynomial of degree 2n-1. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L780). |
| <a id="parameter-37"></a>`number of 1d nodes for face quadrature` | `6 (2D), 5 (3D)` | `Patterns::Integer()` | Number of nodes in the base 1d quadrature. Will integrate a polynomial of degree 2n-1. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L785). |
| <a id="parameter-38"></a>`rule for simplices` | `witherden_vincent` | `Patterns::Selection("gauss\|witherden_vincent")` | Gauss or Witherden-Vincent (odd order) rule. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L776). |

### Stabilization

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-273"></a>`enable supg` | `false` | `Patterns::Bool()` | Enable SUPG/PSPG stabilization for the incompressible Navier-Stokes equations. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1540). |
| <a id="parameter-274"></a>`enable tracer supg` | `false` | `Patterns::Bool()` | Enable SUPG stabilization for the tracer equation in the Cahn-Hilliard Navier-Stokes equations. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1545). |
