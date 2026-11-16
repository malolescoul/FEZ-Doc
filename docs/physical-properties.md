# Material properties and model applicability

`Physical properties` declares fluid and pseudosolid data centrally. Reading a property is separate from using it in a volume or boundary model.

| Property family | Confirmed consumer |
|---|---|
| Fluid 0 kinematic viscosity | Incompressible NS and its multiplier/ALE fluid formulations |
| Fluid 0 and 1 density and kinematic viscosity | CHNS density and dynamic-viscosity interpolation |
| Fluid 0 dynamic viscosity, conductivity, heat capacity and reference state | Compressible flow |
| Body-force acceleration | CHNS and compressible volume residuals; not the fixed-mesh NS volume residual |
| Pseudosolid Lamé functions and constitutive selection | Elastic mesh assemblers |

When `dynamic viscosity` is negative, `Fluid::read_parameters()` replaces it with `density * kinematic viscosity`. A nonnegative value overrides that fallback in the general fluid data, but CHNS independently recomputes its endpoint viscosities from density and kinematic viscosity.

The parser also computes a gas constant and checks `abs(density * temperature reference) > 1e-14` and a positive resulting gas constant when reading each active fluid. These checks occur even when an incompressible solver does not need that gas constant. `number of fluids` is limited by `max_fluids`, and pseudosolids by `max_pseudosolids`; these are storage limits, not support for arbitrary multiphase physics. `max_fluids` is 2 and `max_pseudosolids` is 1 in `parameters.h`.

Pseudosolid `ogden beta` must have magnitude greater than `1e-14` when read, even if another constitutive model is selected. Parsed Lamé functions are declared inside `lame lambda` and `lame mu`. The complete inherited parsed-function vocabulary is discussed under [function data](boundary-conditions.md#function-data).

The tables below give declaration defaults rather than recommended material data. In their paths `i` is a zero-based material index, and `dim` is 2 or 3. Unrestricted double patterns do not enforce positive viscosity, conductivity or heat capacity.


## Implementation references

All references target the [documented revision](index.md).

- [src/parameters.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp)
- [include/parameters.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/parameters.h)
- [src/scratch_data.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/scratch_data.cpp)
- [include/scratch_data.h](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/include/scratch_data.h)


## Parameter declaration reference

The following tables are transcribed from FEZ-owned declarations at the documented revision. `Patterns::Double()` accepts a real number; `Double(a, b)` adds bounds. `Integer` behaves similarly. `Selection` lists exact spellings; `Bool` accepts `true` or `false`. C++ expressions are retained when a pattern depends on program constants. A source description states declaration intent; applicability is qualified in the model and method text above. Empty defaults are written as `(empty)`.

### Physical properties

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-192"></a>`body force` | `0, 0 (2D); 0, 0, 0 (3D)` | `Patterns::List(Patterns::Double(), dim, dim, ",")` | Body force vector (e.g., gravity acceleration) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1111). |
| <a id="parameter-193"></a>`number of fluids` | `1` | `Patterns::Integer()` | Number of fluids [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1091). |
| <a id="parameter-194"></a>`number of pseudosolids` | `0` | `Patterns::Integer()` | Number of pseudosolids (linear elastic analogy for mesh movement) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1101). |

### Physical properties / Fluid i

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-195"></a>`density` | `1` | `Patterns::Double(0.)` | Fluid density for incompressible solvers and reference density for compressible solvers [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L960). |
| <a id="parameter-196"></a>`dynamic viscosity` | `-1` | `Patterns::Double()` | Fluid dynamic viscosity. If set to a negative value (default), it is computed automatically as density * kinematic viscosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L969). |
| <a id="parameter-197"></a>`heat capacity at constant pressure` | `1` | `Patterns::Double()` | Fluid heat capacity at constant pressure [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L979). |
| <a id="parameter-198"></a>`kinematic viscosity` | `1` | `Patterns::Double()` | Fluid kinematic viscosity [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L965). |
| <a id="parameter-199"></a>`pressure reference` | `1` | `Patterns::Double(0.)` | Fluid pressure reference [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L983). |
| <a id="parameter-200"></a>`temperature reference` | `1` | `Patterns::Double(0.)` | Fluid temperature reference [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L987). |
| <a id="parameter-201"></a>`thermal conductivity` | `1` | `Patterns::Double()` | Fluid thermal conductivity [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L975). |

### Physical properties / Pseudosolid i

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-202"></a>`constitutive model` | `linear elasticity` | `Patterns::Selection( "linear elasticity\|neo hookean\|ogden")` | Constitutive model for the pseudosolid [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1033). |
| <a id="parameter-203"></a>`ogden beta` | `1.` | `Patterns::Double()` | Volumetric exponent for the Ogden constitutive model [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1044). |
