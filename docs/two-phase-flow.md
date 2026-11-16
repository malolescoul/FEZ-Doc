# Incompressible two-phase flow

`incompressible_chns` solves a coupled Cahn–Hilliard–Navier–Stokes (CHNS) problem on a fixed mesh. The primary unknowns are velocity \(\mathbf u\), pressure \(p\), phase tracer \(\phi\) and chemical potential \(\mu\). This is a diffuse-interface model with two fluid-property endpoints, not a sharp-interface tracking method.

## Phase convention and material interpolation

Fluid 0 corresponds to \(\phi=+1\), fluid 1 to \(\phi=-1\). For either density or dynamic viscosity,

$$
a(\phi)=\tfrac12[(a_0-a_1)\widehat\phi+(a_0+a_1)],
\qquad \eta_i=\rho_i\nu_i.
$$

The optional material-evaluation limiter sets \(\widehat\phi=\max(-1,\min(1,\phi))\); otherwise \(\widehat\phi=\phi\). It is used when evaluating mixed properties. It does not establish that the solved tracer is globally bounded or that the nonlinear update is clipped. The helper used for material derivatives returns half the endpoint difference even outside the clipping interval; it does not differentiate the clipping map.

Both endpoint properties must be specified consistently with the intended model. `number of fluids` defaults to 1 globally, whereas CHNS scratch data reads fluid entries 0 and 1. The presence of a second declared subsection does not make the single-fluid default a validated two-phase configuration. CHNS derives endpoint dynamic viscosities from density and kinematic viscosity; explicitly setting the general `dynamic viscosity` entry does not override them.

## Assembled equations

For zero sources on a fixed mesh, let \(\widetilde\sigma=3\sigma/(2\sqrt2)\), \(M\) be the constant mobility and \(\epsilon\) the interface thickness. The volume residual corresponds to

$$
\rho(\phi)[\partial_t\mathbf u+(\mathbf u\cdot\nabla)\mathbf u-\mathbf g]
+(\nabla\mathbf u)\mathbf J+\nabla p
-\nabla\cdot(2\eta(\phi)D(\mathbf u))+\phi\nabla\mu=0,
\qquad \nabla\cdot\mathbf u=0,
$$

$$
\partial_t\phi+\mathbf u\cdot\nabla\phi-M\Delta\mu=0,
\qquad
\mu-\frac{\widetilde\sigma}{\epsilon}\phi(\phi^2-1)
+\widetilde\sigma\epsilon\Delta\phi=0,
\qquad
\mathbf J=\tfrac12M(\rho_1-\rho_0)\nabla\mu.
$$

The code variable `diffusive_flux` is already the vector \((\nabla\mathbf u)\mathbf J\), rather than \(\mathbf J\) alone. `body force` supplies \(\mathbf g\) in acceleration units and appears multiplied by density. Velocity, tracer and potential sources enter additively in their residuals; the pressure source uses \(\nabla\cdot\mathbf u=s_p\).

## Discretization and boundaries

All four fields use continuous Galerkin spaces, with independent polynomial degrees. The chemical-potential split avoids a fourth-order primal phase-field discretization. Momentum SUPG/PSPG and tracer SUPG are separately selectable in the CHNS assembler. They are residual-based additions, not replacements for the phase diffusion terms. See [spatial methods](spatial-discretization.md) and [time integration](time-integration.md).

`CahnHilliard boundary conditions` declares `no_flux` and `dirichlet_mms`; the latter uses manufactured fields rather than a general user-supplied phase boundary function. With no explicit phase boundary flux contributions, the weak form supplies homogeneous natural flux conditions. Fluid boundary conditions use the common flow machinery; this executable has no boundary multiplier field. See [boundary conditions](boundary-conditions.md).

## Model parameters

The following table is the declaration contract for `Cahn Hilliard`. `mobility model` admits only `constant`; its parser contains an inconsistent comparison against `linear`, while the assembler directly uses the scalar `mobility`. No additional mobility law is established by this revision. `alpha` and `beta` are declared as mesh-forcing coefficients, but their use in the inspected assemblers has not been established; see [ALE compatibility](two-phase-flow-ale.md).


## Implementation references

All references target the [documented revision](index.md).

- [src/incompressible_chns_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/incompressible_chns_solver.cpp)
- [src/assembly/incompressible_chns_assemblers.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/assembly/incompressible_chns_assemblers.cpp)
- [include/scratch_data.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/scratch_data.h)
- [src/scratch_data.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/scratch_data.cpp)
- [include/cahn_hilliard.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/cahn_hilliard.h)
- [src/parameters.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp)


## Parameter declaration reference

The following tables are transcribed from FEZ-owned declarations at the documented revision. `Patterns::Double()` accepts a real number; `Double(a, b)` adds bounds. `Integer` behaves similarly. `Selection` lists exact spellings; `Bool` accepts `true` or `false`. C++ expressions are retained when a pattern depends on program constants. A source description states declaration intent; applicability is qualified in the model and method text above. Empty defaults are written as `(empty)`.

### Cahn Hilliard

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-1"></a>`alpha` | `0.0` | `Patterns::Double()` | Coefficient of pseudosolid source term alpha * phi * grad(phi). [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1591). |
| <a id="parameter-2"></a>`beta` | `0.0` | `Patterns::Double()` | Coefficient of pseudosolid source term beta * (u_ALE * grad(phi)) * grad(phi). [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1596). |
| <a id="parameter-3"></a>`enable tracer limiter` | `false` | `Patterns::Bool()` | Enable limiter for the tracer (phase field marker) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1586). |
| <a id="parameter-4"></a>`interface thickness` | `1e-2` | `Patterns::Double()` | Interface thickness (epsilon) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1582). |
| <a id="parameter-5"></a>`mobility` | `1.` | `Patterns::Double()` | Mobility value if constant [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1574). |
| <a id="parameter-6"></a>`mobility model` | `constant` | `Patterns::Selection("constant")` | Model for the mobility tensor [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1570). |
| <a id="parameter-7"></a>`surface tension` | `1.` | `Patterns::Double()` | Fluid-fluid surface tension [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1578). |
