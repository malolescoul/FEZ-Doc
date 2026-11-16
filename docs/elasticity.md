# Elastic mesh models

`linear_elasticity` instantiates `LinearElasticitySolver<dim>`. It solves for the current mesh-position field \(\mathbf x(\mathbf X)\), not directly for displacement. The displacement is \(\mathbf d=\mathbf x-\mathbf X\). The same elasticity assemblers provide mesh regularization in ALE and FSI formulations.

## Constitutive equations

The linear elastic residual uses

$$
\boldsymbol\varepsilon=\operatorname{sym}(\nabla_X\mathbf x)-\mathbf I,
\qquad
\boldsymbol\sigma=\lambda\operatorname{tr}(\boldsymbol\varepsilon)\mathbf I
+2\mu_s\boldsymbol\varepsilon,
\qquad
-\nabla_X\cdot\boldsymbol\sigma+\mathbf s_x=0.
$$

The source is additive in the weak residual. Lamé coefficients can be space- and time-dependent parsed functions. The selectable neo-Hookean assembler instead uses \(\mathbf F=\nabla_X\mathbf x\), \(J=\det\mathbf F\), and first Piola stress

$$
\mathbf P=\mu_s(\mathbf F-\mathbf F^{-T})+\lambda\log(J)\mathbf F^{-T}.
$$

The `ogden` branch uses the first Piola stress below, where `ogden beta` supplies \(\beta_o\):

$$
\mathbf P=\mu_s(\mathbf F-\mathbf F^{-T})
+\lambda\frac{1-J^{-\beta_o}}{\beta_o}\mathbf F^{-T}.
$$

This expression specifies the implemented mesh model; a constitutive name alone would not define its normalization. Finite-deformation branches require meaningful invertible mappings (the neo-Hookean logarithm requires \(J>0\)); the parameter parser does not guarantee this.

## Parameters and methods

`Physical properties / Pseudosolid 0 / constitutive model` selects among the implemented branches; see [physical properties](physical-properties.md) for its declaration and Lamé functions. `FiniteElements / Mesh position degree` sets the continuous position-space degree. Pseudosolid boundary types supply fixed reference positions, input position functions, manufactured data or coupled boundary positions. See [boundaries](boundary-conditions.md).

`Linear elasticity / current mesh source term` controls evaluation of the source on current rather than reference coordinates and a continuation multiplier. This option is rejected together with manufactured-solution studies. The dedicated solver has MUMPS and CG branches; its linear controls are under `Linear solver / linear elasticity`. Nonlinear constitutive models still need nonlinear iterations despite the executable name. See [algebraic methods](algebraic-solvers.md).


## Implementation references

All references target the [documented revision](index.md).

- [src/linear_elasticity_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/linear_elasticity_solver.cpp)
- [src/assembly/elasticity_assemblers.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/assembly/elasticity_assemblers.cpp)
- [include/assembly/elasticity_assemblers.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/assembly/elasticity_assemblers.h)
- [src/parameter_reader.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameter_reader.cpp)


## Parameter declaration reference

The following tables are transcribed from FEZ-owned declarations at the documented revision. `Patterns::Double()` accepts a real number; `Double(a, b)` adds bounds. `Integer` behaves similarly. `Selection` lists exact spellings; `Bool` accepts `true` or `false`. C++ expressions are retained when a pattern depends on program constants. A source description states declaration intent; applicability is qualified in the model and method text above. Empty defaults are written as `(empty)`.

### Linear elasticity / current mesh source term

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-69"></a>`continuation steps` | `1` | `Patterns::Integer(1)` | Number of steps to use in the continuation method [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1649). |
| <a id="parameter-70"></a>`enable` | `false` | `Patterns::Bool()` | Enable the evaluation of the given position source term on the current mesh (and not on the reference mesh as usual) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1633). |
| <a id="parameter-71"></a>`max multiplier` | `1.` | `Patterns::Double(1.)` | Maximum coefficient multiplying the source term evaluated on the current mesh [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1644). |
| <a id="parameter-72"></a>`min multiplier` | `1.` | `Patterns::Double(1.)` | Minimum coefficient multiplying the source term evaluated on the current mesh [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1639). |
