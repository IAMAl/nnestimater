# Sequential Store
import numpy


def statics_store_cycles_sequential(config_hard, number_of_stores):
    execution_clock_frequency                   = int(config_hard['exexcution_clock_frequency'])
    store_clock_frequency                       = int(config_hard['store_clock_frequency'])
    store_path_length                           = int(config_hard['store_path_length'])
    store_over_heads                            = int(config_hard['store_over_heads'])
    store_burst_length                          = int(config_hard['store_burst_length'])

    total_store_sequential_cycles       = float(store_over_heads) * numpy.ceil(float(number_of_stores)/float(store_burst_length)) + numpy.ceil(float(execution_clock_frequency) / float(store_clock_frequency)) * number_of_stores

    return total_store_sequential_cycles
