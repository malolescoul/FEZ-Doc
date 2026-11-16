# Verified limitations and open scientific questions

This documentation is based on source inspection at `c6c4dd08b4ab3376062f031d577406a30a6e06bf`, not a numerical validation campaign. The following distinctions are part of the model reference.

## Implementation facts

- CHNS declares only constant mobility. Its reader compares the selected name against `linear`, inconsistent with the declaration, while its assembler directly uses the scalar mobility. No adaptive, degenerate or tensor mobility is established.
- CHNS computes endpoint dynamic viscosity as density times kinematic viscosity, independently of the general dynamic-viscosity override. The limiter clips the tracer for material evaluation, while its material derivative helper remains the linear endpoint derivative.
- The standalone heat equation has unit diffusivity and no explicit Neumann face-flux residual. Globally declared fluid conductivity and `heat_flux` do not establish those capabilities.
- The NS multiplier assembler selection does not enable SUPG. Global stabilization flags do not prove that every solver consumes them.
- Linear methods are solver-specific: heat rejects GMRES and the classic NS iterative path requires GMRES. Generic ILU is serial and generic AMG requires a dedicated setup.
- Tree refinement requires quads/hexes and a single time subinterval. ALE CHNS does not select the same entry-point metric loop as fixed-mesh CHNS.
- Monolithic FSI rejects more than one weak no-slip boundary and moving-mesh zero-mean pressure. Rotation requires the all-position-to-all-multiplier coupling; finite-mass choices have additional coupling-specific checks.
- Defaults admit incomplete cases: one Newton iteration, one globally active fluid and stationary time integration do not describe a validated nonlinear two-phase transient configuration.

## Questions grouped for scientific review

1. **Thermodynamics and units.** Confirm the intended dimensional/reference-state convention for compressible pressure and temperature offsets, and the preferred presentation of incompressible versus CHNS pressure and force units.
2. **Phase-field nonlinear consistency.** Confirm the intended treatment of material derivatives when the property-evaluation limiter is active, and the intended resolution of the mobility-name mismatch. The implementation facts above are retained until clarified.
3. **Mesh constitutive conventions.** Establish the precise energy normalization intended for the implemented Ogden pseudosolid and any recommended parameter ranges. Only verified stress expressions are currently reproduced.
4. **FSI force and geometry conventions.** Establish a single documented multiplier-to-force sign and dimensional normalization across both FSI classes, including cylinder length and rotation assumptions; confirm which coupling strategies are intended as supported user options rather than experimental alternatives.
5. **Boundary and workflow validation.** Verify nonzero heat-flux treatment, the FIXME on compressible pressure-boundary Jacobian consistency, and the intended support matrix for ALE/FSI with remeshing and restart. Source declarations alone cannot resolve these as tested capabilities.

These questions do not prevent reference documentation of the implemented residuals and parser contracts. Installation, case creation, execution and worked examples remain a subsequent documentation stage.


## Implementation references

All references target the [documented revision](index.md).

- [src/parameters.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp)
- [include/cahn_hilliard.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/cahn_hilliard.h)
- [include/scratch_data.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/scratch_data.h)
- [src/heat_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/heat_solver.cpp)
- [src/compressible_ns_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/compressible_ns_solver.cpp)
- [src/monolithic_fsi_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/monolithic_fsi_solver.cpp)
- [src/fsi_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/fsi_solver.cpp)
- [src/parameter_reader.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameter_reader.cpp)
