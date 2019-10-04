# nnestimator
Neural Network Workload Estimater

This open source software estimates workload neural netork models;
- How many parameters are in every layer,
- How many operations are taken in every layer,
- How many execution cycles are involved in every layer,
- How mutch energy is consumed in every layer, and 
- How many total executiona cycles and latency is necessary for target hardware configuration

TOPS value and Wattage can be estimated. In addition, it also shows breakdown of operation type, execution type, and energy consumption.

## Exexcution

The nnestimator feeds hardware configuration file and network configuration file to estimate. You can edit both files as you like.
The script can run with following command:
>python3 nnestimator.py

Default file name of the hardware configuation file and the netowrk configuration file, are "hard_config.txt" and "nn_config.txt", repectively. Default output file name is "nn_estimated.txt". There is option to estimate with sparseness, compression and zero-skipping (see source code of nnestimator.py).