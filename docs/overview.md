# FEZ overview

FEZ is a collection of C++ finite element solvers for single- and multiphase flow and fluid–structure interaction. Its official README describes a continuous Galerkin setting and implicit, monolithic formulations. FEZ uses deal.II and PETSc; the build configuration requires deal.II with PETSc support. Optional MMG integration is controlled at build time.

## Executable entry points

The build system creates an executable from each C++ source in `solvers/`. The following table identifies the class instantiated by each entry point; the presence of an executable does not establish that every model or option is available in every configuration.

| Entry point | Solver class | Role |
|---|---|---|
| `incompressible_ns` | `NSSolver` | Incompressible Navier–Stokes |
| `incompressible_ns_lambda` | `NSSolverLambda` | Incompressible flow with Lagrange multipliers |
| `incompressible_chns` | `CHNSSolver<dim>` | Coupled Cahn–Hilliard and Navier–Stokes on a fixed mesh |
| `incompressible_chns_ale` | `CHNSSolver<dim, true>` | Coupled Cahn–Hilliard and Navier–Stokes with a moving mesh |
| `compressible_ns` | `CompressibleNSSolver` | Compressible Navier–Stokes |
| `linear_elasticity` | `LinearElasticitySolver` | Linear elasticity |
| `fsi` | `FSISolverLessLambda` | Fluid–structure interaction |
| `monolithic_fsi` | `FSISolver` | Fluid–structure interaction |
| `heat` | `HeatSolver` | Heat diffusion; also used to test error estimation and adaptation |

The entry points read a parameter file and instantiate a solver for dimension 2 or 3. Their workflows are not identical. For example, the fixed-mesh CHNS entry point selects a fixed-point loop when metric-based adaptation is enabled; the moving-mesh CHNS entry point calls its regular run outside manufactured-solution studies.

## Software organization

`solvers/` contains executable entry points and workflow selection. `include/` declares solver interfaces, field layouts, parameter structures and shared algorithms; `src/` implements them. `src/assembly/` contains local residual and Jacobian contributions for incompressible flow, CHNS, elasticity and boundary multipliers. `NavierStokesSolver` provides common flow lifecycle operations, while `GenericSolver` supplies a nonlinear solver interface. Heat and elasticity have their own assembly and solve paths.

Mesh topology, field approximation and geometry are separate concepts: the triangulation stores cells, the finite-element system defines field spaces, the DoF handler numbers coefficients, and mappings and quadrature provide geometric integration data. The shared scratch/copy-data assembly pattern evaluates local contributions before constrained distribution to global matrices and vectors.

See [solver selection](solvers.md), [spatial methods](spatial-discretization.md), [algebraic methods](algebraic-solvers.md), [mesh adaptation](mesh-adaptation.md) and [outputs](outputs.md). These concepts follow deal.II's separation of building blocks; they do not make every FEZ solver interchangeable.

## Parameter files

FEZ uses deal.II's `ParameterHandler` and groups entries into named subsections. `ParameterReader<dim>` declares and reads parameter groups for the mesh, finite elements, physical properties, time integration, solvers, boundary and initial conditions, source terms and post-processing. Some quantities, including the number of boundary conditions, are read before the complete parameter set is declared.

The problem dimension is specified in the `Dimension` subsection:

```text
subsection Dimension
  set dimension = 2
end
```

| Parameter | Declared default | Meaning |
|---|---:|---|
| `Dimension / dimension` | `2` | Spatial dimension. The executable entry points shown above select dimension 2 or 3. |

A declaration is not a guarantee that a parameter affects every solver. Refer to the relevant solver or method documentation for applicability and compatibility.

## Source references

This page describes [FEZ at commit `c6c4dd0`](https://github.com/arthurbawin/fez/tree/c6c4dd08b4ab3376062f031d577406a30a6e06bf). The [README](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/README.md) states the project scope; [CMakeLists.txt](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/CMakeLists.txt) defines build targets and dependencies. The [solver entry points](https://github.com/arthurbawin/fez/tree/c6c4dd08b4ab3376062f031d577406a30a6e06bf/solvers), [parameter reader](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/parameter_reader.h) and [parameter declarations](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp) define the corresponding implementation.



## Parameter declaration reference

The following tables are transcribed from FEZ-owned declarations at the documented revision. `Patterns::Double()` accepts a real number; `Double(a, b)` adds bounds. `Integer` behaves similarly. `Selection` lists exact spellings; `Bool` accepts `true` or `false`. C++ expressions are retained when a pattern depends on program constants. A source description states declaration intent; applicability is qualified in the model and method text above. Empty defaults are written as `(empty)`.

### Dimension

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-23"></a>`dimension` | `2` | `Patterns::Integer()` | Problem dimension (2 or 3) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L19). |
