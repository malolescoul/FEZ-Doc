# Linear and nonlinear solution

The common nonlinear interface solves an assembled residual by Newton updates, with an analytical or finite-difference Jacobian and optional line search. `newton_solver.h` controls the nonlinear loop; each physical solver provides residual, Jacobian, constraints and a linear-solve implementation. Nonlinear stopping tolerances and linear residual tolerances are different controls.

## Newton iteration

`Nonlinear solver / max_iterations` defaults to **1**. This is a declared default, not a recommendation for convergence of a nonlinear fluid or finite-deformation problem. `tolerance` applies to the nonlinear residual; `divergence_tolerance` is a separate upper threshold. The reassembly heuristic compares successive residual norms to determine whether an existing matrix can be reused. Its zero default leads to frequent reassembly for nonzero residuals.

`analytic_jacobian` selects the analytic assembly branch where the solver implements it. The comparison flags and absolute/relative tolerances are diagnostic controls for checking that matrix against finite differences. They do not alter the governing equations. The line-search acceptance logic is defined in `NewtonSolver`, not by an additional relaxation parameter guessed from the name.

## Linear methods and actual availability

Two declaration blocks exist: `Linear solver / main physics` and `Linear solver / linear elasticity`. They have the same entry vocabulary, but apply to different solver identifiers.

| Consumer | Confirmed methods |
|---|---|
| `NSSolver` | MUMPS; otherwise explicitly requires GMRES |
| `HeatSolver` | MUMPS, CG; GMRES rejected |
| `LinearElasticitySolver` | MUMPS, CG |
| Other flow solvers | Dedicated implementations must be checked; the common enum alone is not a compatibility guarantee |

MUMPS is a direct sparse solve through PETSc. Iterative tolerances do not control a MUMPS factorization. The shared CG implementation uses a zero initial guess and `ReductionControl`, stopping at either the absolute target or the relative target times the initial residual. CG requires suitable symmetry and definiteness; a Navier–Stokes saddle-point system is not made suitable by selecting `cg` in a parameter file.

`NSSolver` has a dedicated GMRES and AMG setup, including a block preconditioner. The generic preconditioner factory supports `none`, serial `ilu`, and `block_jacobi`; it rejects `amg` unless a dedicated solver initializes it. ILU explicitly requires one MPI process. GMRES restart length and right/left preconditioning are irrelevant to CG. Matrix/preconditioner reuse remains tied to each solver's lifecycle.

## Parameter declarations

The patterns and defaults below describe parsing. Mathematical prerequisites and consumer restrictions above remain applicable.


## Implementation references

All references target the [documented revision](index.md).

- [include/newton_solver.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/newton_solver.h)
- [src/generic_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/generic_solver.cpp)
- [src/linear_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/linear_solver.cpp)
- [include/linear_solver.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/linear_solver.h)
- [src/incompressible_ns_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/incompressible_ns_solver.cpp)
- [src/heat_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/heat_solver.cpp)
- [src/linear_elasticity_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/linear_elasticity_solver.cpp)
- [src/parameters.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp)


## Parameter declaration reference

The following tables are transcribed from FEZ-owned declarations at the documented revision. `Patterns::Double()` accepts a real number; `Double(a, b)` adds bounds. `Integer` behaves similarly. `Selection` lists exact spellings; `Bool` accepts `true` or `false`. C++ expressions are retained when a pattern depends on program constants. A source description states declaration intent; applicability is qualified in the model and method text above. Empty defaults are written as `(empty)`.

### Linear solver / linear elasticity

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-73"></a>`absolute tolerance` | `1e-12` | `Patterns::Double(0.)` | Absolute tolerance for iterative solver. The solver stops when the residual norm is below this value, or below the relative tolerance times the initial residual norm. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1249). |
| <a id="parameter-74"></a>`ilu fill level` | `0` | `Patterns::Integer()` | Max level of fill-in for ILU preconditioner [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1280). |
| <a id="parameter-75"></a>`max iterations` | `100` | `Patterns::Integer()` | Max number of outer iterations for iterative solver [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1263). |
| <a id="parameter-76"></a>`max krylov vectors` | `100` | `Patterns::Integer(1)` | Number of Krylov vectors stored before restarting GMRES (restart length). Unused by CG. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1267). |
| <a id="parameter-77"></a>`method` | `direct_mumps` | `Patterns::Selection("direct_mumps\|cg\|gmres")` | Method [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1241). |
| <a id="parameter-78"></a>`preconditioner` | `none` | `Patterns::Selection("none\|ilu\|block_jacobi\|amg")` | Method [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1245). |
| <a id="parameter-79"></a>`relative tolerance` | `1e-6` | `Patterns::Double(0.)` | Relative tolerance for iterative solver, with respect to the initial residual norm (the norm of the right-hand side, since the initial guess is zero). Set to 0 to use only the absolute tolerance. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1256). |
| <a id="parameter-80"></a>`reuse` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1284). |
| <a id="parameter-81"></a>`right preconditioning` | `true` | `Patterns::Bool()` | Use right preconditioning for GMRES, so that the tolerances apply to the true (unpreconditioned) residual. If false, left preconditioning is used and the tolerances apply to the preconditioned residual. Unused by CG. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1272). |
| <a id="parameter-82"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1285). |

### Linear solver / main physics

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-83"></a>`absolute tolerance` | `1e-12` | `Patterns::Double(0.)` | Absolute tolerance for iterative solver. The solver stops when the residual norm is below this value, or below the relative tolerance times the initial residual norm. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1249). |
| <a id="parameter-84"></a>`ilu fill level` | `0` | `Patterns::Integer()` | Max level of fill-in for ILU preconditioner [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1280). |
| <a id="parameter-85"></a>`max iterations` | `100` | `Patterns::Integer()` | Max number of outer iterations for iterative solver [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1263). |
| <a id="parameter-86"></a>`max krylov vectors` | `100` | `Patterns::Integer(1)` | Number of Krylov vectors stored before restarting GMRES (restart length). Unused by CG. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1267). |
| <a id="parameter-87"></a>`method` | `direct_mumps` | `Patterns::Selection("direct_mumps\|cg\|gmres")` | Method [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1241). |
| <a id="parameter-88"></a>`preconditioner` | `none` | `Patterns::Selection("none\|ilu\|block_jacobi\|amg")` | Method [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1245). |
| <a id="parameter-89"></a>`relative tolerance` | `1e-6` | `Patterns::Double(0.)` | Relative tolerance for iterative solver, with respect to the initial residual norm (the norm of the right-hand side, since the initial guess is zero). Set to 0 to use only the absolute tolerance. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1256). |
| <a id="parameter-90"></a>`reuse` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1284). |
| <a id="parameter-91"></a>`right preconditioning` | `true` | `Patterns::Bool()` | Use right preconditioning for GMRES, so that the tolerances apply to the true (unpreconditioned) residual. If false, left preconditioning is used and the tolerances apply to the preconditioned residual. Unused by CG. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1272). |
| <a id="parameter-92"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1285). |

### Nonlinear solver

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-169"></a>`analytic_jacobian` | `true` | `Patterns::Bool()` | Compute exact Jacobian matrix. If false, use finite differences. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1169). |
| <a id="parameter-170"></a>`analytical_jacobian_absolute_tolerance` | `1e-3` | `Patterns::Double()` | If maximum absolute error exceeds this value, print matrices to console [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1190). |
| <a id="parameter-171"></a>`analytical_jacobian_relative_tolerance` | `1e-3` | `Patterns::Double()` | If maximum relative error exceeds this value, print matrices to console [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1195). |
| <a id="parameter-172"></a>`compare jacobian matrix with finite differences` | `false` | `Patterns::Bool()` | Compare the analytic jacobian with its finite difference approximation on all cells [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1185). |
| <a id="parameter-173"></a>`divergence_tolerance` | `1e4` | `Patterns::Double()` | Stop nonlinear solver if residual exceeds this value [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1157). |
| <a id="parameter-174"></a>`enable_line_search` | `true` | `Patterns::Bool()` | Enable line search [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1165). |
| <a id="parameter-175"></a>`max_iterations` | `1` | `Patterns::Integer()` | Maximum number of Newton iterations [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1161). |
| <a id="parameter-176"></a>`tolerance` | `1e-10` | `Patterns::Double()` | Stopping tolerance for the Newton solver [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1153). |
| <a id="parameter-177"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1184). |
| <a id="parameter-178"></a>`write problematic elements` | `false` | `Patterns::Bool()` | Write mesh elements for which the analytic jacobian differs from its approximation to a Gmsh's .pos file [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1200). |

### Nonlinear solver / reassembly heuristic

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-179"></a>`decrease tolerance` | `0.` | `Patterns::Double()` | If the norm of the current residual is higher than this value times the previous residual norm, reassemble the matrix. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1176). |
