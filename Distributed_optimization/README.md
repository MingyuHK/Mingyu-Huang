# Distributed optimization
*VPP's day-ahead decision-making through distributed coordination conducted by VPP and prosumers. Primal and dual variables are exchanged between VPP and prosumers in the iteration process. Results show the convergence of the distributed framework.*

## Requirements
*configurations on environments*

python version: 3.8.10

The must-have packages can be installed by running
```
pip install requirements.txt
```

## Experiments
### Data
*Data storage*

All the data for experiments are saved in ```data/```. 

### Reproduction

To reproduce the experiments in the paper, please run
```
distributed_test.py
```
Results are saved in ```result/``` folder

To get the figure, please run
```
show_result.py
```



