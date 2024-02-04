# nnestimator
Neural Network Workload Estimator

This open source software estimates workload neural network models;
- How many parameters are in every layer,
- How many operations are taken in every layer,
- How many execution cycles are involved in every layer,
- How much energy is consumed in every layer, and 
- How many total execution cycles and latency are necessary for target hardware configuration

TOPS value and Wattage can be estimated. In addition, it also shows breakdown of operation type, execution type, and energy consumption.

## License
GPL v3, See LICENSE file

## Execution

The nnestimator feeds hardware configuration file and network configuration file to estimate. You can edit both files as you like.
The script can run with following command:
>python3 nnestimator.py

Default file name of the hardware configuration file and the network configuration file, are "hard_config.txt" and "nn_config.txt", repectively. Default output file name is "nn_estimated.txt". There is option to estimate with sparseness, compression and zero-skipping (see source code of nnestimator.py).