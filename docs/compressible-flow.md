# Compressible flow

`compressible_ns` solves for velocity \(\mathbf u\), pressure variable \(p\), and temperature variable \(T\) using `CompressibleNSSolver<dim>`. The density is evaluated algebraically from these unknowns; it is not a separate conserved finite-element field.

## Thermodynamic convention and equations

The implemented density law is

$$
\rho=\rho_r\frac{1+p/p_r}{1+T/T_r},
\qquad a_p=\frac{1/p_r}{1+p/p_r},
\qquad b_T=\frac{1/T_r}{1+T/T_r}.
$$

The offsets are essential: interpreting the finite-element variables directly as absolute pressure and temperature would change the law. The code also computes \(R=p_r/(\rho_rT_r)\) when reading fluid data. `parameters.h` explicitly identifies the solved variables as perturbations: absolute pressure is `pressure reference + p` and absolute temperature is `temperature reference + T`. The remaining unit and force-presentation questions are grouped in [open questions](limitations.md).

Writing \(D_t=\partial_t+\mathbf u\cdot\nabla\), the zero-source volume residual is

$$
\nabla\cdot\mathbf u+a_pD_tp-b_TD_tT=0,
\qquad
\rho D_t\mathbf u+\nabla p-\nabla\cdot\boldsymbol\tau-\rho\mathbf g=0,
$$

$$
\rho c_pD_tT-D_tp-k\Delta T-\boldsymbol\tau:\nabla\mathbf u=0,
\qquad
\boldsymbol\tau=2\eta D(\mathbf u)
-\tfrac23\eta(\nabla\cdot\mathbf u)\mathbf I.
$$

The factor \(2/3\) is used in the implementation, including its 2D instantiation. Velocity, pressure and temperature sources appear additively in these residuals. This is a primitive-variable formulation with viscous work and pressure work in the temperature equation; no shock-capturing capability is inferred from the executable name.

## Parameters and discretization

The model consumes fluid 0's `density`, `dynamic viscosity`, `thermal conductivity`, `heat capacity at constant pressure`, `pressure reference` and `temperature reference`, plus `Physical properties / body force`. [Physical properties](physical-properties.md) gives exact defaults, parser patterns and the negative-dynamic-viscosity fallback. The global `kinematic viscosity` affects this model through that fallback.

The constructor creates continuous velocity, pressure and temperature fields. Their degrees, geometry and quadrature are documented under [spatial discretization](spatial-discretization.md); temporal derivatives use the common [time handler](time-integration.md). Its source setup and boundary assembly are separate from incompressible NS. Temperature constraints use the heat boundary data, while the explicit temperature Neumann/flux treatment and pressure-boundary Jacobian consistency require the qualifications in [limitations](limitations.md).


## Implementation references

All references target the [documented revision](index.md).

- [src/compressible_ns_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/compressible_ns_solver.cpp)
- [src/scratch_data.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/scratch_data.cpp)
- [src/parameters.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp)
- [src/navier_stokes_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/navier_stokes_solver.cpp)
