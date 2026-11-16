# Time integration

FEZ's `TimeHandler` implements a stationary option and backward differentiation formulas of order one and two (BDF1 and BDF2). This page describes the common time-handling implementation at the [documented revision](index.md); individual solver entry points and workflows determine how it is used.

## Discrete time derivative

For an unknown `y`, BDF1 approximates the derivative at time level `n` by

$$
\frac{dy}{dt}(t_n) \approx \frac{y^n-y^{n-1}}{\Delta t_n}.
$$

With `h = Δt_n` and `k = Δt_{n-1}`, the variable-step BDF2 coefficients implemented by `TimeHandler` are

$$
\frac{dy}{dt}(t_n) \approx
\left(\frac1h+\frac1{h+k}\right)y^n
-\left(\frac1h+\frac1k\right)y^{n-1}
+\frac{h}{k(h+k)}y^{n-2}.
$$

For equal consecutive time steps, these reduce to `(3yⁿ − 4yⁿ⁻¹ + yⁿ⁻²)/(2Δt)`. The stationary option sets the time-derivative coefficient to zero.

## Parameters

The entries below belong to `subsection Time integration`. Defaults are the values declared by FEZ, not recommended settings for a particular problem.

The full declaration tables below provide the exact defaults and parser constraints.

The parameter reader checks `dt <= t_end`. When constant time stepping is used, `TimeHandler` also checks that the length of each time subinterval is an integer multiple of the initial time step, within its numerical tolerance. These implementation checks do not replace a physically meaningful choice of times and step size.

The starting strategy has consequences beyond selecting an order: individual solvers handle the `initial condition` starting step in their time loop. For example, the heat solver repeats its initial condition, or uses an exact solution in its applicable verification modes. Consult the relevant solver's implementation before assuming the same behaviour in every workflow.

## Adaptive stepping

Under `Time integration / Adaptation`, `enable` defaults to `false`. The declared `adaptation strategy` values are `bdf truncation error` (default) and `cfl`. A CFL-based strategy requires a velocity variable: `TimeHandler::validate_parameters` rejects its use with a solver that does not provide one. Error and CFL targets, time-step bounds, and optional rejection controls are declared in the same subsection. The BDF estimator uses divided differences from additional solution history and tracks the maximum coefficient error per active variable. Time-step bounds, growth/reduction factors and required output times constrain the proposed step. Rejection can be triggered by nonlinear failure, excessive estimated error or excessive CFL; the time handler rolls back the step and aborts after more than five consecutive rejections. This estimates temporal error in the represented fields, not a bound on total spatial and temporal error. See `src/timestep_adaptation.cpp` and `TimeHandler::is_timestep_accepted` for the estimator and rejection paths.

## Source references

- [Parameter declarations and parsing](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp)
- [TimeHandler implementation](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/time_handler.cpp)
- [Heat solver time loop](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/heat_solver.cpp)



## Parameter declaration reference

The following tables are transcribed from FEZ-owned declarations at the documented revision. `Patterns::Double()` accepts a real number; `Double(a, b)` adds bounds. `Integer` behaves similarly. `Selection` lists exact spellings; `Bool` accepts `true` or `false`. C++ expressions are retained when a pattern depends on program constants. A source description states declaration intent; applicability is qualified in the model and method text above. Empty defaults are written as `(empty)`.

### Time integration

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-275"></a>`bdf start method` | `initial condition` | `Patterns::Selection("initial condition\|BDF1")` | Starting method for BDF schemes of order > 1. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1351). |
| <a id="parameter-276"></a>`bdf start step ratio` | `0.1` | `Patterns::Double(0.)` | If using BDF1 as starting method for the BDF2, the first step is set to this vlue times the initial time step [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1355). |
| <a id="parameter-277"></a>`dt` | `1` | `Patterns::Double()` | Time step [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1338). |
| <a id="parameter-278"></a>`scheme` | `stationary` | `Patterns::Selection("stationary\|BDF1\|BDF2")` | Time stepping scheme (default is stationary) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1347). |
| <a id="parameter-279"></a>`t_end` | `1` | `Patterns::Double()` | End of the simulation time interval [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1343). |
| <a id="parameter-280"></a>`t_initial` | `1` | `Patterns::Double()` | Beginning of the simulation time interval [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1339). |
| <a id="parameter-281"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1361). |

### Time integration / Adaptation

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-282"></a>`adaptation strategy` | `bdf truncation error` | `Patterns::Selection("bdf truncation error\|cfl")` | Strategy used to drive timestep adaptation [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1371). |
| <a id="parameter-283"></a>`cfl ratio to reject` | `2.` | `Patterns::Double(1.)` | Time step is rejected if its CFL number exceeds this value times the target CFL [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1436). |
| <a id="parameter-284"></a>`compute error on estimator` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1423). |
| <a id="parameter-285"></a>`enable` | `false` | `Patterns::Bool()` | Enable adaptive time stepping [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1367). |
| <a id="parameter-286"></a>`error ratio to reject` | `2.` | `Patterns::Double(1.)` | Time step is rejected if its error estimate exceeds this value times the target error [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1418). |
| <a id="parameter-287"></a>`max timestep` | `100.` | `Patterns::Double()` | Maximum time step allowed [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1376). |
| <a id="parameter-288"></a>`max timestep increase` | `10.` | `Patterns::Double()` | Maximum ratio allowed between increasing time steps [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1385). |
| <a id="parameter-289"></a>`max timestep reduction` | `1e-1` | `Patterns::Double()` | Minimum ratio allowed between decreasing time steps [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1390). |
| <a id="parameter-290"></a>`min timestep` | `1e-6` | `Patterns::Double()` | Minimum time step allowed [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1381). |
| <a id="parameter-291"></a>`reject timestep with large cfl` | `false` | `Patterns::Bool()` | Reject time steps with CFL number larger than target times given factor [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1431). |
| <a id="parameter-292"></a>`reject timestep with large error` | `false` | `Patterns::Bool()` | Reject time steps with error estimate larger than target times given factor [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1409). |
| <a id="parameter-293"></a>`required times` | `(empty)` | `Patterns::List(Patterns::Double())` | Times that the time integrator must hit exactly [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1395). |
| <a id="parameter-294"></a>`target cfl number` | `1.` | `Patterns::Double()` | Target CFL number for timestep adaptation [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1427). |
| <a id="parameter-295"></a>`target error on lagrange_mult` | `1.` | `Patterns::Double()` | Target temporal coefficient-error tolerance for this variable. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1402). |
| <a id="parameter-296"></a>`target error on mesh_position` | `1.` | `Patterns::Double()` | Target temporal coefficient-error tolerance for this variable. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1402). |
| <a id="parameter-297"></a>`target error on phase_potential` | `1.` | `Patterns::Double()` | Target temporal coefficient-error tolerance for this variable. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1402). |
| <a id="parameter-298"></a>`target error on phase_tracer` | `1.` | `Patterns::Double()` | Target temporal coefficient-error tolerance for this variable. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1402). |
| <a id="parameter-299"></a>`target error on pressure` | `1.` | `Patterns::Double()` | Target temporal coefficient-error tolerance for this variable. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1402). |
| <a id="parameter-300"></a>`target error on temperature` | `1.` | `Patterns::Double()` | Target temporal coefficient-error tolerance for this variable. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1402). |
| <a id="parameter-301"></a>`target error on velocity` | `1.` | `Patterns::Double()` | Target temporal coefficient-error tolerance for this variable. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1402). |
| <a id="parameter-302"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1366). |
