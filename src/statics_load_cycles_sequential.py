# Sequential Load
import numpy


def statics_load_cycles_sequential(config_hard, number_of_loads):
    execution_clock_frequency                   = int(config_hard['exexcution_clock_frequency'])
    load_clock_frequency                        = int(config_hard['load_clock_frequency'])
    load_path_length                            = int(config_hard['load_path_length'])
    load_over_heads                             = int(config_hard['load_over_heads'])
    load_burst_length                           = int(config_hard['load_burst_length'])

    total_load_filter_sequential_cycles     = float(load_over_heads + load_path_length) * numpy.ceil(float(number_of_loads)/float(load_burst_length)) + numpy.ceil(float(execution_clock_frequency) / float(load_clock_frequency)) * float(number_of_loads)

    return total_load_filter_sequential_cycles
