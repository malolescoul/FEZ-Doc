# Time integration

FEZ's `TimeHandler` implements a stationary option and backward differentiation formulas of order one and two (BDF1 and BDF2). This page describes the common time-handling implementation at the [documented revision](index.md); individual solver entry points and workflows determine how it is used.

## Discrete time derivative

For an unknown `y`, BDF1 approximates the derivative at time level `n` by

```math
\frac{dy}{dt}(t_n) \approx \frac{y^n-y^{n-1}}{\Delta t_n}.
```

With `h = Δt_n` and `k = Δt_{n-1}`, the variable-step BDF2 coefficients implemented by `TimeHandler` are

```math
\frac{dy}{dt}(t_n) \approx
\left(\frac1h+\frac1{h+k}\right)y^n
-\left(\frac1h+\frac1k\right)y^{n-1}
+\frac{h}{k(h+k)}y^{n-2}.
```

For equal consecutive time steps, these reduce to `(3yⁿ − 4yⁿ⁻¹ + yⁿ⁻²)/(2Δt)`. The stationary option sets the time-derivative coefficient to zero.

## Parameters

The entries below belong to `subsection Time integration`. Defaults are the values declared by FEZ, not recommended settings for a particular problem.

| Entry | Default | Values / effect |
|---|---|---|
| `scheme` | `stationary` | `stationary`, `BDF1`, or `BDF2`. |
| `dt` | `1` | Initial time-step size. |
| `t_initial` | `1` | Initial simulation time. |
| `t_end` | `1` | Final simulation time. |
| `bdf start method` | `initial condition` | `initial condition` or `BDF1`; used to provide starting data for higher-order BDF schemes. |
| `bdf start step ratio` | `0.1` | For BDF2 with BDF1 start, the initial step is `dt` multiplied by this ratio. Its declared pattern is non-negative. |

The parameter reader checks `dt <= t_end`. When constant time stepping is used, `TimeHandler` also checks that the length of each time subinterval is an integer multiple of the initial time step, within its numerical tolerance. These implementation checks do not replace a physically meaningful choice of times and step size.

The starting strategy has consequences beyond selecting an order: individual solvers handle the `initial condition` starting step in their time loop. For example, the heat solver repeats its initial condition, or uses an exact solution in its applicable verification modes. Consult the relevant solver's implementation before assuming the same behaviour in every workflow.

## Adaptive stepping

Under `Time integration / Adaptation`, `enable` defaults to `false`. The declared `adaptation strategy` values are `bdf truncation error` (default) and `cfl`. A CFL-based strategy requires a velocity variable: `TimeHandler::validate_parameters` rejects its use with a solver that does not provide one. Error and CFL targets, time-step bounds, and optional rejection controls are declared in the same subsection. Their detailed behaviour and solver applicability require separate documentation.

## Source references

- [Parameter declarations and parsing](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp)
- [TimeHandler implementation](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/time_handler.cpp)
- [Heat solver time loop](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/heat_solver.cpp)
