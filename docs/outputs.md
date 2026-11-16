# Output, restart and diagnostics

The common output controls determine whether volume VTU data are written, their directory and prefix, output frequency and grouping. Moving-mesh and fixed-point workflows carry additional file-prefix/time-subinterval metadata. Surface output has its own enable flag, boundary identifier, prefix and frequency; enabling it does not select a physical boundary condition.

## Postprocessing

`Postprocessing` groups force computations, field integrals, structure position, slicing, phase volume, phase center of mass, phase-average velocity, vorticity, Q criterion and mesh velocity. These observables require the relevant fields in the selected solver. A declared CHNS phase observable does not add a phase field to a single-phase run.

The parameter reader restricts slicing to 3D, and force computation must be enabled when forces on slices are requested. Force definitions and signs depend on the solver stress and multiplier convention; the method selection is therefore part of the observable specification. Pressure normalization differs between incompressible NS and CHNS and must be accounted for when interpreting force units.

## Checkpoint and restart

`Checkpoint Restart` declares checkpoint writing, restart selection, prefix and frequency. Serialization and restoration are implemented in the common Navier–Stokes workflow and its solver data. These declarations must not be read as a promise that arbitrary changes of model, mesh, dimension or MPI layout are restart-compatible. Runtime restart coverage across all executable variants has not been established by this source audit.

## Verification and debug controls

Manufactured solutions replace or supply exact fields and source terms for verification studies. They are not physical boundary models for an arbitrary case. Space and time convergence settings control meshes, time-step reductions, norms and convergence tables. `Debug` contains diagnostic or deliberately altered coupling choices; it is not a menu of supported production models. `Timer` enables performance timing.

The tables below report declaration contracts. Empty source descriptions are explicitly marked; a scientific meaning is not invented for an undocumented switch.


## Implementation references

All references target the [documented revision](index.md).

- [src/post_processing_handler.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/post_processing_handler.cpp)
- [src/post_processing_tools.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/post_processing_tools.cpp)
- [src/parameters.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp)
- [src/navier_stokes_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/navier_stokes_solver.cpp)
- [src/parameter_reader.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameter_reader.cpp)


## Parameter declaration reference

The following tables are transcribed from FEZ-owned declarations at the documented revision. `Patterns::Double()` accepts a real number; `Double(a, b)` adds bounds. `Integer` behaves similarly. `Selection` lists exact spellings; `Bool` accepts `true` or `false`. C++ expressions are retained when a pattern depends on program constants. A source description states declaration intent; applicability is qualified in the model and method text above. Empty defaults are written as `(empty)`.

### Checkpoint Restart

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-12"></a>`checkpoint file` | `checkpoint` | `Patterns::Anything()` | Name of the file to write to and read from the checkpoint [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1693). |
| <a id="parameter-13"></a>`checkpoint frequency` | `10` | `Patterns::Integer()` | Write a checkpoint every N time steps [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1698). |
| <a id="parameter-14"></a>`enable checkpoint` | `false` | `Patterns::Bool()` | Save data periodically to allow restart? [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1685). |
| <a id="parameter-15"></a>`restart` | `false` | `Patterns::Bool()` | Restart simulation from given checkpoint file? [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1689). |

### Debug

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-16"></a>`apply exact solution` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L2066). |
| <a id="parameter-17"></a>`fsi_apply_erroneous_coupling` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L2067). |
| <a id="parameter-18"></a>`fsi_check_mms_on_boundary` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L2071). |
| <a id="parameter-19"></a>`fsi_coupling_option` | `1` | `Patterns::Integer()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L2075). |
| <a id="parameter-20"></a>`verbosity` | `quiet` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L2056). |
| <a id="parameter-21"></a>`write dealii mesh as msh` | `false` | `Patterns::Bool()` | If using deal.II meshing routines, write the mesh as a .msh file [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L2057). |
| <a id="parameter-22"></a>`write partition gmsh` | `false` | `Patterns::Bool()` | Write the mesh partitions as a Gmsh .pos file. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L2062). |

### Manufactured solution

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-93"></a>`compute rates only at end` | `true` | `Patterns::Bool()` | If disabled, compute and write convergence rates at each convergence step. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1762). |
| <a id="parameter-94"></a>`convergence file prefix` | `convergence_rates` | `Patterns::Anything()` | Prefix for the convergence file. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1758). |
| <a id="parameter-95"></a>`convergence steps` | `1` | `Patterns::Integer()` | Number of steps in the convergence study [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1745). |
| <a id="parameter-96"></a>`enable` | `false` | `Patterns::Bool()` | Enable convergence study for the prescribed manufactured solution. This overrides the given mesh filename. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1722). |
| <a id="parameter-97"></a>`error at timesteps file prefix` | `unsteady_errors` | `Patterns::Anything()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1775). |
| <a id="parameter-98"></a>`force source term` | `false` | `Patterns::Bool()` | Use the provided source term instead of the one computed with symbolic differentiation [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1740). |
| <a id="parameter-99"></a>`print error at timesteps in console` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1767). |
| <a id="parameter-100"></a>`print error at timesteps to file` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1771). |
| <a id="parameter-101"></a>`run only step` | `-1` | `Patterns::Integer()` | If specified, run only this convergence step (in [0, n_steps]) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1749). |
| <a id="parameter-102"></a>`subtract mean pressure` | `false` | `Patterns::Bool()` | Subtract mean pressure for L2 error computation. If disabled and if the pressure solution is not zero-mean, an error is thrown to avoid returning erroneous convergence rates. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1732). |
| <a id="parameter-103"></a>`type` | `space` | `Patterns::Selection("space\|time\|spacetime")` | Choose between space and/or time convergence study. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1728). |
| <a id="parameter-104"></a>`write convergence table to file` | `false` | `Patterns::Bool()` | Write the convergence table to a file. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1754). |

### Manufactured solution / Space convergence

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-105"></a>`first mesh` | `0` | `Patterns::Integer()` | Index of the first mesh, which will be (mesh prefix)_(first mesh).msh [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1794). |
| <a id="parameter-106"></a>`initial target number of vertices` | `1000` | `Patterns::Integer()` | For a convergence study with metric-based anisotropic mesh adaptation enabled, the initial target number of vertices in the adapted mesh. This value is then doubled at each convergence step. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1805). |
| <a id="parameter-107"></a>`mesh prefix` | `(empty)` | `Patterns::Anything()` | Prefix (including full path) for the meshes to use for the spatial convergence study [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1789). |
| <a id="parameter-108"></a>`norms to compute` | `L2_norm` | `Patterns::List( *Patterns::Tools::Convert<VectorTools::NormType>::to_pattern())` | A comma-separated list of norms (e.g., L2_norm, H1_norm) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1799). |
| <a id="parameter-109"></a>`target vertices multiplier between steps` | `2` | `Patterns::Integer(1)` | Between two convergence steps, the target number of mesh vertices is multiplied by this value. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1812). |
| <a id="parameter-110"></a>`time intervals multiplier between steps` | `2` | `Patterns::Integer(1)` | Between two convergence steps, the number of time intervals is multiplied by this value. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1817). |
| <a id="parameter-111"></a>`use dealii cube mesh` | `false` | `Patterns::Bool()` | Use cube mesh from deal.II's routines [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1781). |
| <a id="parameter-112"></a>`use dealii holed plate mesh` | `false` | `Patterns::Bool()` | Use plate with hole mesh from deal.II's routines [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1785). |

### Manufactured solution / Time convergence

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-113"></a>`norm` | `L1` | `Patterns::Selection("L1\|L2\|Linfty")` | Lp norm to use for the temporal error. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1826). |
| <a id="parameter-114"></a>`spatial mesh index` | `0` | `Patterns::Integer()` | If use spatial mesh is true, set the index (refinement level) of the used mesh. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1837). |
| <a id="parameter-115"></a>`time step reduction` | `0.5` | `Patterns::Double()` | Reduction factor between two time steps in a time convergence study. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1842). |
| <a id="parameter-116"></a>`use spatial mesh` | `false` | `Patterns::Bool()` | If true, use the mesh provided for the spatial convergence study. If false, use the provided mesh in the Mesh subsection. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L1830). |

### Output

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-180"></a>`number of subdivisions` | `2` | `Patterns::Integer(0)` | Number of subdivisions used to build visualization patches. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L389). |
| <a id="parameter-181"></a>`number of vtu groups` | `1` | `Patterns::Integer(0)` | Number of groups of VTU files when writing in parallel (0 means one per MPI process). [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L384). |
| <a id="parameter-182"></a>`output directory` | `./` | `Patterns::FileName()` | Output directory. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L371). |
| <a id="parameter-183"></a>`output prefix` | `solution` | `Patterns::FileName()` | Prefix for the output files. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L375). |
| <a id="parameter-184"></a>`vtu output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the standard vtu export. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L379). |
| <a id="parameter-185"></a>`write vtu results` | `false` | `Patterns::Bool()` | Enable/disable vtu output writing. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L367). |

### Output / fixed point method

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-186"></a>`show solution transfer` | `false` | `Patterns::Bool()` | Show the solution transfer between subinterval meshes. This duplicates the timesteps at the junction of subintervals. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L402). |
| <a id="parameter-187"></a>`single pvd file` | `true` | `Patterns::Bool()` | Generate a single pvd file when using a fixed-point mesh adaptation method. If false, one pvd file per fixed-point iteration is generated instead. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L396). |

### Output / skin

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-188"></a>`boundary id` | `0` | `Patterns::Integer(0)` | Boundary id used to define the skin. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L417). |
| <a id="parameter-189"></a>`output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the exportation of skin-related files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L425). |
| <a id="parameter-190"></a>`output prefix` | `skin` | `Patterns::FileName()` | Prefix for the output files on the skin [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L421). |
| <a id="parameter-191"></a>`write vtu results` | `false` | `Patterns::Bool()` | Enable extraction of vtu files on prescribed boundary. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L412). |

### Postprocessing / chns phase average velocity

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-204"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable this postprocessing [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L468). |
| <a id="parameter-205"></a>`output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the exportation of postprocessing files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L472). |
| <a id="parameter-206"></a>`output prefix` | `postprocessed_data` | `Patterns::FileName()` | Prefix for the postprocessing output files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L486). |
| <a id="parameter-207"></a>`precision` | `6` | `Patterns::Integer(1)` | Number of significant digits to print [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L490). |
| <a id="parameter-208"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L467). |
| <a id="parameter-209"></a>`write results` | `true` | `Patterns::Bool()` | Write result of this postprocessing to file [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L482). |

### Postprocessing / chns phase center of mass

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-210"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable this postprocessing [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L468). |
| <a id="parameter-211"></a>`output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the exportation of postprocessing files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L472). |
| <a id="parameter-212"></a>`output prefix` | `postprocessed_data` | `Patterns::FileName()` | Prefix for the postprocessing output files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L486). |
| <a id="parameter-213"></a>`precision` | `6` | `Patterns::Integer(1)` | Number of significant digits to print [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L490). |
| <a id="parameter-214"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L467). |
| <a id="parameter-215"></a>`write results` | `true` | `Patterns::Bool()` | Write result of this postprocessing to file [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L482). |

### Postprocessing / chns phase volume

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-216"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable this postprocessing [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L468). |
| <a id="parameter-217"></a>`output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the exportation of postprocessing files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L472). |
| <a id="parameter-218"></a>`output prefix` | `postprocessed_data` | `Patterns::FileName()` | Prefix for the postprocessing output files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L486). |
| <a id="parameter-219"></a>`precision` | `6` | `Patterns::Integer(1)` | Number of significant digits to print [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L490). |
| <a id="parameter-220"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L467). |
| <a id="parameter-221"></a>`write results` | `true` | `Patterns::Bool()` | Write result of this postprocessing to file [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L482). |

### Postprocessing / field integral

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-222"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable this postprocessing [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L468). |
| <a id="parameter-223"></a>`output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the exportation of postprocessing files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L472). |
| <a id="parameter-224"></a>`output prefix` | `postprocessed_data` | `Patterns::FileName()` | Prefix for the postprocessing output files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L486). |
| <a id="parameter-225"></a>`precision` | `6` | `Patterns::Integer(1)` | Number of significant digits to print [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L490). |
| <a id="parameter-226"></a>`variables` | `(empty)` | `Patterns::List(Patterns::Selection( "none\|velocity\|pressure\|mesh_position\|temperature\|phase_tracer\|phase_potential\|lagrange_mult"))` | Comma-separated list of finite element variables to integrate over the domain. Each variable is written to <output prefix>_<variable>.txt [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L538). |
| <a id="parameter-227"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L467). |
| <a id="parameter-228"></a>`write results` | `true` | `Patterns::Bool()` | Write result of this postprocessing to file [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L482). |

### Postprocessing / forces computation

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-229"></a>`boundary ids` | `(empty)` | `Patterns::List(Patterns::Integer(0))` | Comma-separated boundary ids on which this postprocessing is applied [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L499). |
| <a id="parameter-230"></a>`computation method` | `stress vector` | `Patterns::Selection( "stress vector\|lagrange multiplier")` | Method used to evaluate the hydrodynamic forces [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L528). |
| <a id="parameter-231"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable this postprocessing [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L468). |
| <a id="parameter-232"></a>`output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the exportation of postprocessing files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L472). |
| <a id="parameter-233"></a>`output prefix` | `postprocessed_data` | `Patterns::FileName()` | Prefix for the postprocessing output files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L486). |
| <a id="parameter-234"></a>`precision` | `6` | `Patterns::Integer(1)` | Number of significant digits to print [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L490). |
| <a id="parameter-235"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L467). |
| <a id="parameter-236"></a>`write results` | `true` | `Patterns::Bool()` | Write result of this postprocessing to file [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L482). |

### Postprocessing / mesh velocity

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-237"></a>`computation method` | `discontinuous` | `Patterns::Selection( "discontinuous\|l2 projection\|weighted average")` | Computation method [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L509). |
| <a id="parameter-238"></a>`degree` | `1` | `Patterns::Integer(0)` | Degree of the finite element representation of the postprocessed field [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L514). |
| <a id="parameter-239"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable this postprocessing [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L468). |
| <a id="parameter-240"></a>`output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the exportation of postprocessing files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L472). |
| <a id="parameter-241"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L467). |

### Postprocessing / q_criterion

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-242"></a>`computation method` | `discontinuous` | `Patterns::Selection( "discontinuous\|l2 projection\|weighted average")` | Computation method [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L509). |
| <a id="parameter-243"></a>`degree` | `1` | `Patterns::Integer(0)` | Degree of the finite element representation of the postprocessed field [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L514). |
| <a id="parameter-244"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable this postprocessing [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L468). |
| <a id="parameter-245"></a>`output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the exportation of postprocessing files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L472). |
| <a id="parameter-246"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L467). |

### Postprocessing / slicing

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-247"></a>`along which axis` | `z` | `Patterns::Selection("x\|y\|z")` | Axis along which the slices are defined [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L556). |
| <a id="parameter-248"></a>`boundary ids` | `(empty)` | `Patterns::List(Patterns::Integer(0))` | Comma-separated boundary ids on which this postprocessing is applied [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L499). |
| <a id="parameter-249"></a>`compute forces` | `false` | `Patterns::Bool()` | Compute and write the hydrodynamic forces on each slice [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L564). |
| <a id="parameter-250"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable this postprocessing [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L468). |
| <a id="parameter-251"></a>`number of slices` | `1` | `Patterns::Integer(1)` | Number of slices along the chosen direction [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L560). |
| <a id="parameter-252"></a>`output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the exportation of postprocessing files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L472). |
| <a id="parameter-253"></a>`output prefix` | `postprocessed_data` | `Patterns::FileName()` | Prefix for the postprocessing output files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L486). |
| <a id="parameter-254"></a>`precision` | `6` | `Patterns::Integer(1)` | Number of significant digits to print [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L490). |
| <a id="parameter-255"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L467). |
| <a id="parameter-256"></a>`write results` | `true` | `Patterns::Bool()` | Write result of this postprocessing to file [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L482). |

### Postprocessing / structure position

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-257"></a>`boundary ids` | `(empty)` | `Patterns::List(Patterns::Integer(0))` | Comma-separated boundary ids on which this postprocessing is applied [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L499). |
| <a id="parameter-258"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable this postprocessing [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L468). |
| <a id="parameter-259"></a>`output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the exportation of postprocessing files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L472). |
| <a id="parameter-260"></a>`output prefix` | `postprocessed_data` | `Patterns::FileName()` | Prefix for the postprocessing output files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L486). |
| <a id="parameter-261"></a>`precision` | `6` | `Patterns::Integer(1)` | Number of significant digits to print [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L490). |
| <a id="parameter-262"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L467). |
| <a id="parameter-263"></a>`write results` | `true` | `Patterns::Bool()` | Write result of this postprocessing to file [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L482). |

### Postprocessing / vorticity

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-264"></a>`computation method` | `discontinuous` | `Patterns::Selection( "discontinuous\|l2 projection\|weighted average")` | Computation method [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L509). |
| <a id="parameter-265"></a>`degree` | `1` | `Patterns::Integer(0)` | Degree of the finite element representation of the postprocessed field [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L514). |
| <a id="parameter-266"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable this postprocessing [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L468). |
| <a id="parameter-267"></a>`output frequency` | `1` | `Patterns::Integer(1)` | Frequency (in time steps) for the exportation of postprocessing files [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L472). |
| <a id="parameter-268"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L467). |

### Timer

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-303"></a>`enable timer` | `false` | `Patterns::Bool()` | Enable summary of elapsed time in solver components [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L36). |
