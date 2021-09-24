# Pore Characteristics Impact on PPGD
This electrostatic model calculates the electric field distribution across the granite pores, thereby investigating the impact of the pore characteristics on the localized electric breakdown, which is responsible for the rock damage in the Plasma Pulse Geo Drilling process.

#### Studied parameters:
1. Pore fluids: Air and water.
2. Pore shapes: ellipse, circle, and square.
3. Pore sizes: 10 to 150 micrometer.
4. Pore pressures: 0.1 to 2.5 MPa.

#### How to run the simulations:
1. Install [MOOSE Framework](https://mooseframework.inl.gov/getting_started/installation/index.html) as explained here.
2. Clone the repository in the `~/projects` directory, which is defined in [MOOSE installation](https://mooseframework.inl.gov/getting_started/installation/index.html)):
   * `git clone https://github.com/mezzatf/pore_impact_on_ppgd.git`
3. For the sample-scale simulations:
   * `cd ~/projects/pore_impact_on_ppgd/simulation_files/sample-scale/`
   * `../../moose/test/moose_test-opt -i simulation_file_name.i`
   * example: `../../moose/test/moose_test-opt -i laplace_rock_top.i`
4. For the pore-scale simulations:
   * `cd ~/projects/pore_impact_on_ppgd/simulation_files/pore-scale/`
   * `../../moose/test/moose_test-opt -i simulation_file_name.i`
   * example: `../../moose/test/moose_test-opt -i laplace_water_ellipse_x_p01.i`
5. To plot all figures, please consult the data_processing directory
   * `cd ~/projects/pore_impact_on_ppgd/data_processing`

#### Project:
This work comes is a part of the [Plasma Pulse Geo Drilling](https://geg.ethz.ch/project-plasma_drilling/) project, Geothermal Energy and Geofluids ([GEG.ethz.ch](https://geg.ethz.ch/)) group at ETH Zurich (ETHZ), Switzerland.

#### Publications:
- Ezzat, M., Vogler, D., Saar, M. O. & Adams, B. M. Numerical Modelling of Pore Characteristics in Plasma Pulse Geo Drilling (PPGD). (In prep. 2021).

#### Funding:
- This research was funded by Innosuisse - Swiss Innovation Agency - under grant number 28305.1 PFIW-IW.
- M. O. Saar further thanks the [Werner Siemens Foundation](http://www.wernersiemens-stiftung.ch/home/) (Werner Siemens-Stiftung, WSS) for their support of the Geothermal Energy and Geofluids ([GEG.ethz.ch](https://geg.ethz.ch/)) group at ETH Zurich (ETHZ), Switzerland.
