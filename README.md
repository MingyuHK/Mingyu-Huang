# Distributed differentially private energy management of virtual power plants
*This work propose a distributed differentially private energy management scheme of virtual power plants, leveraging distributed optimization framework and differential privacy. There are three different folders that represent different optimization schemes with the same data.*

Codes for "Distributed differentially private energy management of virtual power plants"
 *(https://doi.org/10.1016/j.epsr.2024.110687)*

Authors: Mingyu Huang, Xueyuan Cui, Yi Wang

## Requirements

python version: 3.8.10

The must-have packages can be installed by running
```
pip install requirements.txt
```
## Experiments
### Data
*Data storage*

All the data for experiments are saved in ```../data```. 

### Reproduction

To reproduce the experiments in the paper, please refer to the detailed ```README.md``` in the following folders.

#### Centralized optimization
Results serve as the benchmark for VPP's decision-making.

#### Distributed optimization
Results show the concergence for the distributed scheme.

#### Distributed differentially private optimization
Results show the impact of the added noise in dual variable.
