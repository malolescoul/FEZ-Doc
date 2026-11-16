# Parameter index

Entries are grouped by exact subsection path. Each link opens the owning model or method table, which records its declaration contract and source. This index deliberately does not repeat defaults. `i` is a zero-based repeated-section index.

This inventory covers explicit FEZ-owned declarations in `parameters.cpp`, `metric_field_parameters.cpp`, boundary records and initial-condition switches, plus verbosity macros and quadrature helpers. Parsed-function and manufactured-field entries inherited or delegated to library objects are described under [function data](boundary-conditions.md#function-data); this is not yet an exhaustive inventory of that delegated vocabulary.

### Cahn Hilliard

- [`alpha`](two-phase-flow.md#parameter-1)
- [`beta`](two-phase-flow.md#parameter-2)
- [`enable tracer limiter`](two-phase-flow.md#parameter-3)
- [`interface thickness`](two-phase-flow.md#parameter-4)
- [`mobility`](two-phase-flow.md#parameter-5)
- [`mobility model`](two-phase-flow.md#parameter-6)
- [`surface tension`](two-phase-flow.md#parameter-7)

### CahnHilliard boundary conditions

- [`number`](boundary-conditions.md#parameter-8)

### CahnHilliard boundary conditions / boundary i

- [`id`](boundary-conditions.md#parameter-9)
- [`name`](boundary-conditions.md#parameter-10)
- [`type`](boundary-conditions.md#parameter-11)

### Checkpoint Restart

- [`checkpoint file`](outputs.md#parameter-12)
- [`checkpoint frequency`](outputs.md#parameter-13)
- [`enable checkpoint`](outputs.md#parameter-14)
- [`restart`](outputs.md#parameter-15)

### Debug

- [`apply exact solution`](outputs.md#parameter-16)
- [`fsi_apply_erroneous_coupling`](outputs.md#parameter-17)
- [`fsi_check_mms_on_boundary`](outputs.md#parameter-18)
- [`fsi_coupling_option`](outputs.md#parameter-19)
- [`verbosity`](outputs.md#parameter-20)
- [`write dealii mesh as msh`](outputs.md#parameter-21)
- [`write partition gmsh`](outputs.md#parameter-22)

### Dimension

- [`dimension`](overview.md#parameter-23)

### FSI

- [`compute error on forces`](monolithic-fsi.md#parameter-49)
- [`cylinder center`](monolithic-fsi.md#parameter-50)
- [`cylinder length`](monolithic-fsi.md#parameter-51)
- [`cylinder radius`](monolithic-fsi.md#parameter-52)
- [`damping`](monolithic-fsi.md#parameter-53)
- [`enable coupling`](monolithic-fsi.md#parameter-54)
- [`fix z component`](monolithic-fsi.md#parameter-55)
- [`force-position coupling`](monolithic-fsi.md#parameter-56)
- [`initial velocity`](monolithic-fsi.md#parameter-57)
- [`mass`](monolithic-fsi.md#parameter-58)
- [`spring constant`](monolithic-fsi.md#parameter-59)
- [`use zero mass model`](monolithic-fsi.md#parameter-60)
- [`verbosity`](monolithic-fsi.md#parameter-61)

### FSI / Rigid body rotation

- [`center of rotation`](monolithic-fsi.md#parameter-62)
- [`enable`](monolithic-fsi.md#parameter-63)

### FiniteElements

- [`Lagrange multiplier degree`](spatial-discretization.md#parameter-24)
- [`mapping degree`](spatial-discretization.md#parameter-25)
- [`Mesh position degree`](spatial-discretization.md#parameter-26)
- [`Potential degree`](spatial-discretization.md#parameter-27)
- [`Pressure degree`](spatial-discretization.md#parameter-28)
- [`Temperature degree`](spatial-discretization.md#parameter-29)
- [`Tracer degree`](spatial-discretization.md#parameter-30)
- [`use quads`](spatial-discretization.md#parameter-31)
- [`Velocity degree`](spatial-discretization.md#parameter-32)

### FiniteElements / Quadrature rule

- [`number of 1d nodes for cell quadrature`](spatial-discretization.md#parameter-33)
- [`number of 1d nodes for face quadrature`](spatial-discretization.md#parameter-34)
- [`rule for simplices`](spatial-discretization.md#parameter-35)

### FiniteElements / Quadrature rule for error

- [`number of 1d nodes for cell quadrature`](spatial-discretization.md#parameter-36)
- [`number of 1d nodes for face quadrature`](spatial-discretization.md#parameter-37)
- [`rule for simplices`](spatial-discretization.md#parameter-38)

### Fluid boundary conditions

- [`enforce zero mean pressure`](boundary-conditions.md#parameter-39)
- [`fix pressure constant`](boundary-conditions.md#parameter-40)
- [`number`](boundary-conditions.md#parameter-41)
- [`verbosity`](boundary-conditions.md#parameter-42)

### Fluid boundary conditions / boundary i

- [`id`](boundary-conditions.md#parameter-43)
- [`name`](boundary-conditions.md#parameter-44)
- [`type`](boundary-conditions.md#parameter-45)
- [`weak no slip tolerance`](boundary-conditions.md#parameter-46)

### Fluid boundary conditions / boundary i / rigid body rotation

- [`center of rotation`](boundary-conditions.md#parameter-47)
- [`enable`](boundary-conditions.md#parameter-48)

### Heat boundary conditions

- [`number`](boundary-conditions.md#parameter-64)

### Heat boundary conditions / boundary i

- [`id`](boundary-conditions.md#parameter-65)
- [`name`](boundary-conditions.md#parameter-66)
- [`type`](boundary-conditions.md#parameter-67)

### Initial conditions

- [`to mms`](boundary-conditions.md#parameter-68)

### Linear elasticity / current mesh source term

- [`continuation steps`](elasticity.md#parameter-69)
- [`enable`](elasticity.md#parameter-70)
- [`max multiplier`](elasticity.md#parameter-71)
- [`min multiplier`](elasticity.md#parameter-72)

### Linear solver / linear elasticity

- [`absolute tolerance`](algebraic-solvers.md#parameter-73)
- [`ilu fill level`](algebraic-solvers.md#parameter-74)
- [`max iterations`](algebraic-solvers.md#parameter-75)
- [`max krylov vectors`](algebraic-solvers.md#parameter-76)
- [`method`](algebraic-solvers.md#parameter-77)
- [`preconditioner`](algebraic-solvers.md#parameter-78)
- [`relative tolerance`](algebraic-solvers.md#parameter-79)
- [`reuse`](algebraic-solvers.md#parameter-80)
- [`right preconditioning`](algebraic-solvers.md#parameter-81)
- [`verbosity`](algebraic-solvers.md#parameter-82)

### Linear solver / main physics

- [`absolute tolerance`](algebraic-solvers.md#parameter-83)
- [`ilu fill level`](algebraic-solvers.md#parameter-84)
- [`max iterations`](algebraic-solvers.md#parameter-85)
- [`max krylov vectors`](algebraic-solvers.md#parameter-86)
- [`method`](algebraic-solvers.md#parameter-87)
- [`preconditioner`](algebraic-solvers.md#parameter-88)
- [`relative tolerance`](algebraic-solvers.md#parameter-89)
- [`reuse`](algebraic-solvers.md#parameter-90)
- [`right preconditioning`](algebraic-solvers.md#parameter-91)
- [`verbosity`](algebraic-solvers.md#parameter-92)

### Manufactured solution

- [`compute rates only at end`](outputs.md#parameter-93)
- [`convergence file prefix`](outputs.md#parameter-94)
- [`convergence steps`](outputs.md#parameter-95)
- [`enable`](outputs.md#parameter-96)
- [`error at timesteps file prefix`](outputs.md#parameter-97)
- [`force source term`](outputs.md#parameter-98)
- [`print error at timesteps in console`](outputs.md#parameter-99)
- [`print error at timesteps to file`](outputs.md#parameter-100)
- [`run only step`](outputs.md#parameter-101)
- [`subtract mean pressure`](outputs.md#parameter-102)
- [`type`](outputs.md#parameter-103)
- [`write convergence table to file`](outputs.md#parameter-104)

### Manufactured solution / Space convergence

- [`first mesh`](outputs.md#parameter-105)
- [`initial target number of vertices`](outputs.md#parameter-106)
- [`mesh prefix`](outputs.md#parameter-107)
- [`norms to compute`](outputs.md#parameter-108)
- [`target vertices multiplier between steps`](outputs.md#parameter-109)
- [`time intervals multiplier between steps`](outputs.md#parameter-110)
- [`use dealii cube mesh`](outputs.md#parameter-111)
- [`use dealii holed plate mesh`](outputs.md#parameter-112)

### Manufactured solution / Time convergence

- [`norm`](outputs.md#parameter-113)
- [`spatial mesh index`](outputs.md#parameter-114)
- [`time step reduction`](outputs.md#parameter-115)
- [`use spatial mesh`](outputs.md#parameter-116)

### Mesh

- [`dealii mesh parameters`](mesh-adaptation.md#parameter-117)
- [`dealii preset mesh`](mesh-adaptation.md#parameter-118)
- [`mesh file`](mesh-adaptation.md#parameter-119)
- [`refinement level`](mesh-adaptation.md#parameter-120)
- [`use dealii cube mesh`](mesh-adaptation.md#parameter-121)
- [`verbosity`](mesh-adaptation.md#parameter-122)

### Mesh / Adaptation

- [`adaptation directory`](mesh-adaptation.md#parameter-123)
- [`adapted meshes extension`](mesh-adaptation.md#parameter-124)
- [`enable`](mesh-adaptation.md#parameter-125)
- [`strategy`](mesh-adaptation.md#parameter-126)
- [`verbosity`](mesh-adaptation.md#parameter-127)

### Mesh / Adaptation / Local refinement

- [`adapt frequency`](mesh-adaptation.md#parameter-128)
- [`fraction to coarsen`](mesh-adaptation.md#parameter-129)
- [`fraction to refine`](mesh-adaptation.md#parameter-130)
- [`max grid level`](mesh-adaptation.md#parameter-131)
- [`max number of cells`](mesh-adaptation.md#parameter-132)
- [`min grid level`](mesh-adaptation.md#parameter-133)
- [`number of prerefinement steps`](mesh-adaptation.md#parameter-134)
- [`number of steady adaptation steps`](mesh-adaptation.md#parameter-135)
- [`refinement strategy`](mesh-adaptation.md#parameter-136)
- [`variables for adaptation`](mesh-adaptation.md#parameter-137)

### Mesh / Adaptation / Metric

- [`mmg verbosity level`](mesh-adaptation.md#parameter-138)
- [`n fixed point`](mesh-adaptation.md#parameter-139)
- [`n time intervals`](mesh-adaptation.md#parameter-140)
- [`transfer solution`](mesh-adaptation.md#parameter-141)

### Mesh / Adaptation / Metric / Fixed point updates

- [`verbosity`](mesh-adaptation.md#parameter-142)

### Mesh / Adaptation / Metric / Fixed point updates / CHNS interface thickness

- [`constant name`](mesh-adaptation.md#parameter-143)
- [`enable`](mesh-adaptation.md#parameter-144)
- [`factor`](mesh-adaptation.md#parameter-145)
- [`update frequency`](mesh-adaptation.md#parameter-146)

### Metric fields

- [`always compute`](mesh-adaptation.md#parameter-147)
- [`metric for adaptation`](mesh-adaptation.md#parameter-148)
- [`number`](mesh-adaptation.md#parameter-149)

### Metric fields / Metric field i

- [`component`](mesh-adaptation.md#parameter-150)
- [`max mesh size`](mesh-adaptation.md#parameter-151)
- [`min mesh size`](mesh-adaptation.md#parameter-152)
- [`type`](mesh-adaptation.md#parameter-153)
- [`variable`](mesh-adaptation.md#parameter-154)
- [`verbosity`](mesh-adaptation.md#parameter-155)

### Metric fields / Metric field i / Analytical metric

- [`enable`](mesh-adaptation.md#parameter-156)

### Metric fields / Metric field i / Gradation

- [`deterministic`](mesh-adaptation.md#parameter-157)
- [`enable`](mesh-adaptation.md#parameter-158)
- [`gradation`](mesh-adaptation.md#parameter-159)
- [`max iteration`](mesh-adaptation.md#parameter-160)
- [`spanning space`](mesh-adaptation.md#parameter-161)
- [`tolerance`](mesh-adaptation.md#parameter-162)
- [`verbosity`](mesh-adaptation.md#parameter-163)

### Metric fields / Metric field i / Intersection

- [`intersect with`](mesh-adaptation.md#parameter-164)
- [`verbosity`](mesh-adaptation.md#parameter-165)

### Metric fields / Metric field i / Multiscale optimal metric for interpolation error

- [`n target vertices`](mesh-adaptation.md#parameter-166)
- [`target norm`](mesh-adaptation.md#parameter-167)
- [`use analytical derivatives`](mesh-adaptation.md#parameter-168)

### Nonlinear solver

- [`analytic_jacobian`](algebraic-solvers.md#parameter-169)
- [`analytical_jacobian_absolute_tolerance`](algebraic-solvers.md#parameter-170)
- [`analytical_jacobian_relative_tolerance`](algebraic-solvers.md#parameter-171)
- [`compare jacobian matrix with finite differences`](algebraic-solvers.md#parameter-172)
- [`divergence_tolerance`](algebraic-solvers.md#parameter-173)
- [`enable_line_search`](algebraic-solvers.md#parameter-174)
- [`max_iterations`](algebraic-solvers.md#parameter-175)
- [`tolerance`](algebraic-solvers.md#parameter-176)
- [`verbosity`](algebraic-solvers.md#parameter-177)
- [`write problematic elements`](algebraic-solvers.md#parameter-178)

### Nonlinear solver / reassembly heuristic

- [`decrease tolerance`](algebraic-solvers.md#parameter-179)

### Output

- [`number of subdivisions`](outputs.md#parameter-180)
- [`number of vtu groups`](outputs.md#parameter-181)
- [`output directory`](outputs.md#parameter-182)
- [`output prefix`](outputs.md#parameter-183)
- [`vtu output frequency`](outputs.md#parameter-184)
- [`write vtu results`](outputs.md#parameter-185)

### Output / fixed point method

- [`show solution transfer`](outputs.md#parameter-186)
- [`single pvd file`](outputs.md#parameter-187)

### Output / skin

- [`boundary id`](outputs.md#parameter-188)
- [`output frequency`](outputs.md#parameter-189)
- [`output prefix`](outputs.md#parameter-190)
- [`write vtu results`](outputs.md#parameter-191)

### Physical properties

- [`body force`](physical-properties.md#parameter-192)
- [`number of fluids`](physical-properties.md#parameter-193)
- [`number of pseudosolids`](physical-properties.md#parameter-194)

### Physical properties / Fluid i

- [`density`](physical-properties.md#parameter-195)
- [`dynamic viscosity`](physical-properties.md#parameter-196)
- [`heat capacity at constant pressure`](physical-properties.md#parameter-197)
- [`kinematic viscosity`](physical-properties.md#parameter-198)
- [`pressure reference`](physical-properties.md#parameter-199)
- [`temperature reference`](physical-properties.md#parameter-200)
- [`thermal conductivity`](physical-properties.md#parameter-201)

### Physical properties / Pseudosolid i

- [`constitutive model`](physical-properties.md#parameter-202)
- [`ogden beta`](physical-properties.md#parameter-203)

### Postprocessing / chns phase average velocity

- [`enable`](outputs.md#parameter-204)
- [`output frequency`](outputs.md#parameter-205)
- [`output prefix`](outputs.md#parameter-206)
- [`precision`](outputs.md#parameter-207)
- [`verbosity`](outputs.md#parameter-208)
- [`write results`](outputs.md#parameter-209)

### Postprocessing / chns phase center of mass

- [`enable`](outputs.md#parameter-210)
- [`output frequency`](outputs.md#parameter-211)
- [`output prefix`](outputs.md#parameter-212)
- [`precision`](outputs.md#parameter-213)
- [`verbosity`](outputs.md#parameter-214)
- [`write results`](outputs.md#parameter-215)

### Postprocessing / chns phase volume

- [`enable`](outputs.md#parameter-216)
- [`output frequency`](outputs.md#parameter-217)
- [`output prefix`](outputs.md#parameter-218)
- [`precision`](outputs.md#parameter-219)
- [`verbosity`](outputs.md#parameter-220)
- [`write results`](outputs.md#parameter-221)

### Postprocessing / field integral

- [`enable`](outputs.md#parameter-222)
- [`output frequency`](outputs.md#parameter-223)
- [`output prefix`](outputs.md#parameter-224)
- [`precision`](outputs.md#parameter-225)
- [`variables`](outputs.md#parameter-226)
- [`verbosity`](outputs.md#parameter-227)
- [`write results`](outputs.md#parameter-228)

### Postprocessing / forces computation

- [`boundary ids`](outputs.md#parameter-229)
- [`computation method`](outputs.md#parameter-230)
- [`enable`](outputs.md#parameter-231)
- [`output frequency`](outputs.md#parameter-232)
- [`output prefix`](outputs.md#parameter-233)
- [`precision`](outputs.md#parameter-234)
- [`verbosity`](outputs.md#parameter-235)
- [`write results`](outputs.md#parameter-236)

### Postprocessing / mesh velocity

- [`computation method`](outputs.md#parameter-237)
- [`degree`](outputs.md#parameter-238)
- [`enable`](outputs.md#parameter-239)
- [`output frequency`](outputs.md#parameter-240)
- [`verbosity`](outputs.md#parameter-241)

### Postprocessing / q_criterion

- [`computation method`](outputs.md#parameter-242)
- [`degree`](outputs.md#parameter-243)
- [`enable`](outputs.md#parameter-244)
- [`output frequency`](outputs.md#parameter-245)
- [`verbosity`](outputs.md#parameter-246)

### Postprocessing / slicing

- [`along which axis`](outputs.md#parameter-247)
- [`boundary ids`](outputs.md#parameter-248)
- [`compute forces`](outputs.md#parameter-249)
- [`enable`](outputs.md#parameter-250)
- [`number of slices`](outputs.md#parameter-251)
- [`output frequency`](outputs.md#parameter-252)
- [`output prefix`](outputs.md#parameter-253)
- [`precision`](outputs.md#parameter-254)
- [`verbosity`](outputs.md#parameter-255)
- [`write results`](outputs.md#parameter-256)

### Postprocessing / structure position

- [`boundary ids`](outputs.md#parameter-257)
- [`enable`](outputs.md#parameter-258)
- [`output frequency`](outputs.md#parameter-259)
- [`output prefix`](outputs.md#parameter-260)
- [`precision`](outputs.md#parameter-261)
- [`verbosity`](outputs.md#parameter-262)
- [`write results`](outputs.md#parameter-263)

### Postprocessing / vorticity

- [`computation method`](outputs.md#parameter-264)
- [`degree`](outputs.md#parameter-265)
- [`enable`](outputs.md#parameter-266)
- [`output frequency`](outputs.md#parameter-267)
- [`verbosity`](outputs.md#parameter-268)

### Pseudosolid boundary conditions

- [`number`](boundary-conditions.md#parameter-269)

### Pseudosolid boundary conditions / boundary i

- [`id`](boundary-conditions.md#parameter-270)
- [`name`](boundary-conditions.md#parameter-271)
- [`type`](boundary-conditions.md#parameter-272)

### Stabilization

- [`enable supg`](spatial-discretization.md#parameter-273)
- [`enable tracer supg`](spatial-discretization.md#parameter-274)

### Time integration

- [`bdf start method`](time-integration.md#parameter-275)
- [`bdf start step ratio`](time-integration.md#parameter-276)
- [`dt`](time-integration.md#parameter-277)
- [`scheme`](time-integration.md#parameter-278)
- [`t_end`](time-integration.md#parameter-279)
- [`t_initial`](time-integration.md#parameter-280)
- [`verbosity`](time-integration.md#parameter-281)

### Time integration / Adaptation

- [`adaptation strategy`](time-integration.md#parameter-282)
- [`cfl ratio to reject`](time-integration.md#parameter-283)
- [`compute error on estimator`](time-integration.md#parameter-284)
- [`enable`](time-integration.md#parameter-285)
- [`error ratio to reject`](time-integration.md#parameter-286)
- [`max timestep`](time-integration.md#parameter-287)
- [`max timestep increase`](time-integration.md#parameter-288)
- [`max timestep reduction`](time-integration.md#parameter-289)
- [`min timestep`](time-integration.md#parameter-290)
- [`reject timestep with large cfl`](time-integration.md#parameter-291)
- [`reject timestep with large error`](time-integration.md#parameter-292)
- [`required times`](time-integration.md#parameter-293)
- [`target cfl number`](time-integration.md#parameter-294)
- [`target error on lagrange_mult`](time-integration.md#parameter-295)
- [`target error on mesh_position`](time-integration.md#parameter-296)
- [`target error on phase_potential`](time-integration.md#parameter-297)
- [`target error on phase_tracer`](time-integration.md#parameter-298)
- [`target error on pressure`](time-integration.md#parameter-299)
- [`target error on temperature`](time-integration.md#parameter-300)
- [`target error on velocity`](time-integration.md#parameter-301)
- [`verbosity`](time-integration.md#parameter-302)

### Timer

- [`enable timer`](outputs.md#parameter-303)

