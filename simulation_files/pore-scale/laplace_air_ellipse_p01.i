[Mesh]
  [./gmg]
    type = FileMeshGenerator
    file = "./mesh/pore_ellipse_p01.msh"
  []
[]

[Variables]
  [voltage]
  []
[]

[Kernels]
  [voltage_diffusion]
    type        = ADMatDiffusion
    variable    = voltage
    diffusivity = electric_permittivity
  []
[]

[Problem]
  type = FEProblem
[]

[BCs]
  [all_voltage]
    type     = NeumannBC
    variable = voltage
    boundary = wall
    value    = 0
  []
  [HV_voltage]
    type     =  FunctionDirichletBC
    variable =  voltage
    boundary =  HV
    function =  voltage_pulse
  []
  [GE_voltage]
    type     = DirichletBC
    variable = voltage
    boundary = GE
    value    = 0
  []
[]

[AuxVariables]
  [EField_x]
    family = MONOMIAL
     order = FIRST
  []
  [EField_y]
    family = MONOMIAL
     order = FIRST
  []
[]

[AuxKernels]
   [E_Fieldx]
     type      = VariableGradientComponent
     component = x
     variable  = EField_x
     gradient_variable = voltage
   []
   [E_Fieldy]
     type      = VariableGradientComponent
     component = y
     variable  = EField_y
     gradient_variable = voltage
   []
[]


[Executioner]
  # type  = Transient
  # num_steps = 10
  # end_time = 0.5e-6
  type = Steady
  solve_type = 'PJFNK'
  petsc_options_iname = '-pc_type -pc_hypre_type'
  petsc_options_value = 'hypre boomeramg'
[]


[Functions]
  [voltage_pulse]
    type  = ParsedFunction
    # value = '3e5*(tanh(t*9e6)-sin(2.0*pi*t/(8.0*1e-6)))/0.8'
    value = 1
  []
[]


[Materials]
  [rock]
    type = ADGenericConstantMaterial
    block  = rock
    prop_names  = 'electric_permittivity'
    prop_values = '6'
    outputs = exodus
  []
  [void]
    type = ADGenericConstantMaterial
    block  = pore
    prop_names  = 'electric_permittivity'
    prop_values = '1'
    outputs = exodus
  []
[]

[Outputs]
  exodus = true

[]
