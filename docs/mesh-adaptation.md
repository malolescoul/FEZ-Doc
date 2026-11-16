# Meshes and adaptation

FEZ reads Gmsh meshes or requests a supported deal.II preset geometry. `mesh file`, legacy `use dealii cube mesh`, `dealii preset mesh`, and the preset-specific argument string are distinct inputs. The geometry selection and file parsing are implemented in `create_mesh` and `mesh.cpp`; a preset name does not describe arbitrary external mesh support.

## Tree-based refinement

`Mesh / Adaptation / strategy = local refinement` uses deal.II/p4est refinement and coarsening. The parameter reader requires quadrilateral/hexahedral elements (`FiniteElements / use quads = true`) and a single time subinterval. Local refinement of simplices is rejected by this path. Marking may use a fixed number or a fixed fraction, with selected solution variables, grid-level bounds, cell-count bound and a time-step frequency. Steady adaptation and initial prerefinement have their own counts.

## Metric-based remeshing

`strategy = riemannian metric` describes metric-driven remeshing. `Metric fields` provides one or more fields and selects the field used for adaptation. A metric describes directional target mesh sizes; it is not a scalar cell-refinement fraction. Its construction may use interpolation-error or graph formulations, analytical data, size bounds and metric processing controls. MMG support is optional at build time; declaring MMG parameters does not establish that a binary was built with it.

`Mesh / Adaptation / Metric` configures mesh–solution fixed-point iterations and time subintervals. For unsteady problems, the transient fixed-point implementation converges solution–mesh pairs across subintervals. `transfer solution` is described as a steady-state option; transient transfer is performed regardless of that toggle. In steady state a single time subinterval is required. Metric computation requires at least one metric field when adaptation is enabled or `always compute` is true.

The optional fixed-point CHNS interface-thickness update also requires its named constant in the tracer initial-condition function. The parameter reader checks this before computation. It is a change of model resolution across mesh iterations, not a general time-dependent material law.

## Workflow applicability

Heat, NS and fixed-mesh CHNS entry points explicitly distinguish regular runs from metric fixed-point adaptation. The CHNS ALE entry point does not make the same selection. Full runtime compatibility of remeshing, ALE and FSI combinations remains unverified here; see [limitations](limitations.md). Source transfer and adaptation frequency must be read in the relevant time loop rather than assumed from the declaration vocabulary.

## Parameter declarations

Metric indices are zero-based. Dynamic names such as `Metric field i` are templates for repeated subsections. The tables retain C++ expressions where a default or pattern depends on dimension or other code constants.


## Implementation references

All references target the [documented revision](index.md).

- [src/mesh.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/mesh.cpp)
- [src/navier_stokes_solver.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/navier_stokes_solver.cpp)
- [src/mesh_adaptation_tools.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/mesh_adaptation_tools.cpp)
- [src/mesh_adaptation/transient_fixed_point.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/mesh_adaptation/transient_fixed_point.cpp)
- [src/metric_field_parameters.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp)
- [src/parameter_reader.cpp](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameter_reader.cpp)
- [CMakeLists.txt](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/CMakeLists.txt)


## Parameter declaration reference

The following tables are transcribed from FEZ-owned declarations at the documented revision. `Patterns::Double()` accepts a real number; `Double(a, b)` adds bounds. `Integer` behaves similarly. `Selection` lists exact spellings; `Bool` accepts `true` or `false`. C++ expressions are retained when a pattern depends on program constants. A source description states declaration intent; applicability is qualified in the model and method text above. Empty defaults are written as `(empty)`.

### Mesh

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-117"></a>`dealii mesh parameters` | `2, 2 : 0., 0. : 1., 1. : false` | `Patterns::Anything()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L138). |
| <a id="parameter-118"></a>`dealii preset mesh` | `none` | `Patterns::Selection( "none\|cube\|rectangle\|holed plate\|uniform channel " "with cylinder\|backward facing step\|lgpi")` | Use dealii meshing routines for specified geometry [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L132). |
| <a id="parameter-119"></a>`mesh file` | `(empty)` | `Patterns::FileName()` | Mesh file in .msh format (Gmsh msh4) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L124). |
| <a id="parameter-120"></a>`refinement level` | `1` | `Patterns::Integer()` | Level of uniform refinement if using deal.II's meshing routines [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L140). |
| <a id="parameter-121"></a>`use dealii cube mesh` | `false` | `Patterns::Bool()` | Use cube mesh from deal.II's routines [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L128). |
| <a id="parameter-122"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L123). |

### Mesh / Adaptation

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-123"></a>`adaptation directory` | `adaptation` | `Patterns::Anything()` | Directory into which mesh adaptation-related files are written [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L152). |
| <a id="parameter-124"></a>`adapted meshes extension` | `adapted` | `Patterns::Anything()` | Root extension for the adapted meshes [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L157). |
| <a id="parameter-125"></a>`enable` | `false` | `Patterns::Bool()` | Enable mesh adaptation [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L148). |
| <a id="parameter-126"></a>`strategy` | `riemannian metric` | `Patterns::Selection( "riemannian metric\|local refinement")` | Mesh adaptation strategy [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L161). |
| <a id="parameter-127"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L147). |

### Mesh / Adaptation / Local refinement

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-128"></a>`adapt frequency` | `1` | `Patterns::Integer(1)` | Adapt the mesh every n time steps [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L247). |
| <a id="parameter-129"></a>`fraction to coarsen` | `0.` | `Patterns::Double(0., 1.)` | Fraction of cells or errors to mark for coarsening [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L220). |
| <a id="parameter-130"></a>`fraction to refine` | `0.3333333333 (2D); 0.142857143 (3D)` | `Patterns::Double(0., 1.)` | Fraction of cells or errors to mark for refinement [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L211). |
| <a id="parameter-131"></a>`max grid level` | `8` | `Patterns::Integer(0)` | Maximum level of grid refinement allowed [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L229). |
| <a id="parameter-132"></a>`max number of cells` | `1000000` | `Patterns::Integer(0)` | Maximum number of mesh cells allowed [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L233). |
| <a id="parameter-133"></a>`min grid level` | `0` | `Patterns::Integer(0)` | Minimum level of grid refinement allowed [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L225). |
| <a id="parameter-134"></a>`number of prerefinement steps` | `0` | `Patterns::Integer(0)` | Number of refinement steps to obtain the initial mesh [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L242). |
| <a id="parameter-135"></a>`number of steady adaptation steps` | `0` | `Patterns::Integer(0)` | Number of adaptation steps for steady-state computations [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L237). |
| <a id="parameter-136"></a>`refinement strategy` | `fixed number` | `Patterns::Selection("fixed number\|fixed fraction")` | Refinement strategy used by deal.II's refine_and_coarsen routines [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L200). |
| <a id="parameter-137"></a>`variables for adaptation` | `velocity` | `Patterns::List(Patterns::Selection( "none\|velocity\|pressure\|mesh_position\|temperature\|phase_tracer\|phase_potential\|lagrange_mult"))` | Comma-separated list of variables used for mesh adaptation [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L205). |

### Mesh / Adaptation / Metric

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-138"></a>`mmg verbosity level` | `1` | `Patterns::Integer(-1, 10)` | Verbosity level of the MMG library [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L179). |
| <a id="parameter-139"></a>`n fixed point` | `1` | `Patterns::Integer(1)` | Number of fixed point iterations to converge the mesh-solution pair [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L168). |
| <a id="parameter-140"></a>`n time intervals` | `1` | `Patterns::Integer(1)` | Number of time sub-intervals for the transient fixed point method [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L183). |
| <a id="parameter-141"></a>`transfer solution` | `true` | `Patterns::Bool()` | Enable solution transfer to the adapted mesh (steady-state only, always done for unsteady simulations) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L173). |

### Mesh / Adaptation / Metric / Fixed point updates

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-142"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L190). |

### Mesh / Adaptation / Metric / Fixed point updates / CHNS interface thickness

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-143"></a>`constant name` | `must_provide_constant_name` | `Patterns::Anything()` | Name of this constant in the function handles [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L97). |
| <a id="parameter-144"></a>`enable` | `false` | `Patterns::Bool()` | Enable/disable the update of this quantity [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L85). |
| <a id="parameter-145"></a>`factor` | `1.` | `Patterns::Double(0)` | When updated, multiply this quantity by this value [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L93). |
| <a id="parameter-146"></a>`update frequency` | `1` | `Patterns::Integer(1)` | Update this quantity every n fixed-point iterations [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/parameters.cpp#L89). |

### Metric fields

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-147"></a>`always compute` | `false` | `Patterns::Bool()` | Specifies whether the metrics should be computed even when mesh adaptation is disabled [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L21). |
| <a id="parameter-148"></a>`metric for adaptation` | `0` | `Patterns::Integer()` | Index of the metric field that will be used to adapt the mesh(es) [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L16). |
| <a id="parameter-149"></a>`number` | `0` | `Patterns::Integer()` | Number of metric tensor fields [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L12). |

### Metric fields / Metric field i

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-150"></a>`component` | `0` | `Patterns::Integer(0, dim - 1)` | If variable is vector-valued, the component of the variable used to compute the metric [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L69). |
| <a id="parameter-151"></a>`max mesh size` | `1e+6` | `Patterns::Double(1e-15)` | Maximum allowed mesh size along a principal direction [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L80). |
| <a id="parameter-152"></a>`min mesh size` | `1e-8` | `Patterns::Double(1e-15)` | Minimum allowed mesh size along a principal direction [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L75). |
| <a id="parameter-153"></a>`type` | `interpolation error` | `Patterns::Selection("interpolation error\|graph")` | Type of the underlying metric field [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L60). |
| <a id="parameter-154"></a>`variable` | `none` | `Patterns::Selection( "none\|velocity\|pressure\|mesh_position\|temperature\|phase_tracer\|phase_potential\|lagrange_mult")` | Variable used to compute the underlying metric field [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L64). |
| <a id="parameter-155"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L59). |

### Metric fields / Metric field i / Analytical metric

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-156"></a>`enable` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L87). |

### Metric fields / Metric field i / Gradation

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-157"></a>`deterministic` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L125). |
| <a id="parameter-158"></a>`enable` | `false` | `Patterns::Bool()` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L124). |
| <a id="parameter-159"></a>`gradation` | `1.5` | `Patterns::Double(1.01)` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L126). |
| <a id="parameter-160"></a>`max iteration` | `100` | `Patterns::Integer(1)` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L127). |
| <a id="parameter-161"></a>`spanning space` | `metric` | `Patterns::Selection("euclidean\|metric\|exp_metric")` | Space in which a single metric spans a full metric field [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L129). |
| <a id="parameter-162"></a>`tolerance` | `1e-2` | `Patterns::Double(0)` | No description supplied by this declaration; effective meaning requires the consumer. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L128). |
| <a id="parameter-163"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L123). |

### Metric fields / Metric field i / Intersection

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-164"></a>`intersect with` | `(empty)` | `Patterns::List(Patterns::Integer(0))` | List of metric fields with which this field will be intersected [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L139). |
| <a id="parameter-165"></a>`verbosity` | `verbose` | `quiet\|verbose` | Console verbosity. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L138). |

### Metric fields / Metric field i / Multiscale optimal metric for interpolation error

| Entry | Declared default | Parser pattern | Declaration purpose and source |
|---|---|---|---|
| <a id="parameter-166"></a>`n target vertices` | `1000` | `Patterns::Integer(0)` | Target number of vertices after adaptation, assuming no gradation [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L105). |
| <a id="parameter-167"></a>`target norm` | `L2_norm` | `Patterns::Selection( "L1_norm\|L2_norm\|L4_norm\|Linfty_norm\|H1_seminorm")` | Target norm for interpolation error minimization [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L100). |
| <a id="parameter-168"></a>`use analytical derivatives` | `false` | `Patterns::Bool()` | Enable/disable the use of the symbolic derivatives of the provided analytical field to evaluate the metric field. If not, reconstructed derivatives from the solution are used. Leaving this to false is the intended way to compute a metric field for an arbitrary numerical solution. [Source](https://github.com/arthurbawin/fez/blob/c6c4dd08b4ab3376062f031d577406a30a6e06bf/src/metric_field_parameters.cpp#L110). |
