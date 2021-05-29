#Statistics
import numpy
import statics_load_cycles_sequential       as statics_ld_cycles
import statics_store_cycles_sequential      as statics_st_cycles
import statics_activation_cycles_sequential as statics_act_cycles


def statistics(\
    process, \
    pipeline, \
    config_layers, \
    config_hard, \
    f_out, \
    record_layer_type, \
    active_func_type, \
    statics_total_number_of_loads_data, \
    statics_total_number_of_loads_param, \
    statics_total_number_of_stores_data, \
    statics_total_number_of_inputs, \
    statics_total_number_of_params, \
    statics_total_number_of_outputs, \
    statics_total_number_of_multiplies, \
    statics_total_number_of_additions, \
    statics_total_number_of_divisions, \
    statics_total_number_of_activations\
    ):

    #Counters
    number_of_layers                    = len(config_layers)

    #Operation Calculations
    total_number_of_data_loads          = 0
    total_number_of_param_loads         = 0
    total_number_of_data_stores         = 0

    total_number_of_multiplies          = 0
    total_number_of_additions           = 0
    total_number_of_divisions           = 0
    total_number_of_activations         = 0

    #Cycle Calculations
    total_load_data_cycles              = 0
    total_load_param_cycles             = 0
    total_store_data_cycles             = 0

    total_multiplication_cycles         = 0
    total_addition_cycles               = 0
    total_division_cycles               = 0
    total_activation_cycles             = 0

    total_number_of_arith_op_per_cycle  = 0.0

    #Total Cycles
    total_cycles                        = 0

    #Total Energy
    total_energy                        = 0.0

    #Cost for Multiplication
    number_of_cycles_for_multiplication = int(config_hard['number_of_cycles_for_multiplication'])
    dwidth_for_multiplication           = int(config_hard['dwidth_for_multiplication'])

    #Cost for Addition
    number_of_cycles_for_addition       = int(config_hard['number_of_cycles_for_addition'])
    dwidth_for_addition                 = int(config_hard['dwidth_for_addition'])

    #Cost for Division
    number_of_cycles_for_division       = int(config_hard['number_of_cycles_for_division'])
    dwidth_for_division                 = int(config_hard['dwidth_for_division'])

    #Data Width on Memory Interface
    load_dtype                          = int(config_hard['load_dtype'])
    store_dtype                         = int(config_hard['load_dtype'])

    #Cost for Activation
    number_of_cycles_for_activation     = ''

    #Semiconductor Process
    semi_process                        = float(config_hard['semi_process'])

    if process == 0:
        process                         = float(config_hard['semi_process'])

    #Scale Factor
    scale_factor                        = float(process) / float(semi_process)

    #Energy Consumption on Components
    energy_multiplier                   = float(config_hard['energy_multiplier'])   * scale_factor * scale_factor   / 1000000000000.0
    energy_adder                        = float(config_hard['energy_adder'])        * scale_factor                  / 1000000000000.0
    energy_divider                      = float(config_hard['energy_divider'])      * scale_factor * scale_factor   / 1000000000000.0
    energy_activation                   = float(config_hard['energy_activation'])   * scale_factor                  / 1000000000000.0
    energy_reg_read                     = float(config_hard['energy_reg_read'])     * scale_factor                  / 1000000000000.0
    energy_reg_write                    = float(config_hard['energy_reg_write'])    * scale_factor                  / 1000000000000.0
    energy_sram_static                  = float(config_hard['energy_reg_write'])    * scale_factor * scale_factor   / 1000000000000.0
    energy_sram_read                    = float(config_hard['energy_sram_read'])    * scale_factor                  / 1000000000000.0
    energy_sram_write                   = float(config_hard['energy_sram_write'])   * scale_factor                  / 1000000000000.0
    energy_dram_read                    = float(config_hard['energy_dram_read'])    / 1000000000000.0
    energy_dram_write                   = float(config_hard['energy_dram_write'])   / 1000000000000.0

    #On-Chip Clock Frequency
    execution_clock_frequency           = float(config_hard['exexcution_clock_frequency'])

    #External Memory Load Parameters
    load_clock_frequency                = int(config_hard['load_clock_frequency'])
    load_dwidth                         = int(config_hard['load_dtype'])
    number_of_parallel_loads            = int(config_hard['number_of_parallel_loads'])

    #External Memory Store Parameters
    store_clock_frequency               = int(config_hard['store_clock_frequency'])
    store_dwidth                        = int(config_hard['store_dtype'])
    number_of_parallel_stores           = int(config_hard['number_of_parallel_stores'])

    #Recording
    total_load_data_energy              = numpy.zeros(number_of_layers + 1)
    total_load_param_energy             = numpy.zeros(number_of_layers + 1)
    total_store_data_energy             = numpy.zeros(number_of_layers + 1)
    total_multiplication_energy         = numpy.zeros(number_of_layers + 1)
    total_addition_energy               = numpy.zeros(number_of_layers + 1)
    total_division_energy               = numpy.zeros(number_of_layers + 1)
    total_activation_energy             = numpy.zeros(number_of_layers + 1)
    total_layer_energy                  = numpy.zeros(number_of_layers + 1)

    total_exec_load_data_cycles         = numpy.zeros(number_of_layers + 1)
    total_exec_load_param_cycles        = numpy.zeros(number_of_layers + 1)
    total_exec_store_data_cycles        = numpy.zeros(number_of_layers + 1)
    total_exec_multiplication_cycles    = numpy.zeros(number_of_layers + 1)
    total_exec_addition_cycles          = numpy.zeros(number_of_layers + 1)
    total_exec_division_cycles          = numpy.zeros(number_of_layers + 1)
    total_exec_activation_cycles        = numpy.zeros(number_of_layers + 1)
    total_exec_cycles                   = numpy.zeros(number_of_layers + 1)

    #
    active_func_type_                   = active_func_type.copy()
    #active_func_type.pop()
    #active_func_type.reverse()

    record_layer_type_                  = record_layer_type.copy()
    record_layer_type.reverse()
    record_layer_type.pop()

    f_out.writelines("\n\n\n2.Statistics for Layers\n")

    for layer_id in range(number_of_layers):

        if layer_id > 0 :
            config_prev_layer                   = config_layers[layer_id - 1]
            number_of_parallel_in               = int(config_prev_layer['number_of_parallel_kernels'])
            config_pres_layer                   = config_layers[layer_id]
            number_of_parallel_out              = int(config_pres_layer['number_of_parallel_kernels'])

            #Number of Operations
            number_of_data_loads                = statics_total_number_of_loads_data[layer_id] * (dwidth_for_multiplication / load_dtype)
            total_number_of_data_loads          += number_of_data_loads

            number_of_param_loads               = statics_total_number_of_loads_param[layer_id] * (dwidth_for_multiplication / load_dtype)
            total_number_of_param_loads         += number_of_param_loads

            number_of_data_stores               = statics_total_number_of_stores_data[layer_id] * (dwidth_for_multiplication / store_dtype)
            total_number_of_data_stores         += number_of_data_stores

            number_of_multiplies                = statics_total_number_of_multiplies[layer_id]
            total_number_of_multiplies          += number_of_multiplies

            number_of_additions                 = statics_total_number_of_additions[layer_id]
            total_number_of_additions           += number_of_additions

            number_of_divisions                 = statics_total_number_of_divisions[layer_id]
            total_number_of_divisions           += number_of_divisions

            number_of_activations               = statics_total_number_of_activations[layer_id]
            total_number_of_activations         += number_of_activations


            total_layer_load_data_cycles        = statics_ld_cycles.statics_load_cycles_sequential(config_hard, number_of_data_loads)
            total_load_data_cycles              += total_layer_load_data_cycles

            total_layer_load_param_cycles       = statics_ld_cycles.statics_load_cycles_sequential(config_hard, number_of_param_loads)
            total_load_param_cycles             += total_layer_load_param_cycles

            total_layer_load_cycles             = total_layer_load_data_cycles + total_layer_load_param_cycles

            total_layer_store_data_cycles       = statics_st_cycles.statics_store_cycles_sequential(config_hard, number_of_data_stores)
            total_store_data_cycles             += total_layer_store_data_cycles

            total_multiplication_sequential_cycles  = number_of_multiplies * number_of_cycles_for_multiplication
            total_multiplication_cycles             += total_multiplication_sequential_cycles

            total_addition_sequential_cycles        = number_of_additions * number_of_cycles_for_addition
            total_addition_cycles                   += total_addition_sequential_cycles

            total_division_sequential_cycles        = number_of_divisions * number_of_cycles_for_division
            total_division_cycles                   += total_division_sequential_cycles

            number_of_cycles_for_activation = statics_act_cycles.statics_activation_cycles_sequential(active_func_type[layer_id], config_hard)
            total_activation_sequential_cycles      = number_of_activations * number_of_cycles_for_activation
            total_activation_cycles                 += total_activation_sequential_cycles

            if pipeline == 'off':
                total_layer_compute_cycles          = total_multiplication_sequential_cycles + total_addition_sequential_cycles + total_division_sequential_cycles + total_activation_sequential_cycles
            elif (number_of_cycles_for_multiplication > number_of_cycles_for_addition):
                total_layer_compute_cycles          = total_multiplication_sequential_cycles + total_division_sequential_cycles + total_activation_sequential_cycles + 1
            elif (number_of_cycles_for_multiplication <= number_of_cycles_for_addition):
                total_layer_compute_cycles          = total_addition_sequential_cycles + total_division_sequential_cycles + total_activation_sequential_cycles + 1

            total_layer_cycles                  = total_layer_load_data_cycles + total_layer_load_param_cycles + total_layer_store_data_cycles + total_layer_compute_cycles
            total_cycles                        += total_layer_cycles

            total_arithmetics   = int(number_of_multiplies + number_of_additions + number_of_divisions + number_of_activations)
            total_mem_accesses  = int(number_of_data_loads + number_of_param_loads + number_of_data_stores)

            number_of_mlt_op_per_cycle    = number_of_multiplies    / total_layer_cycles
            number_of_add_op_per_cycle    = number_of_additions     / total_layer_cycles
            number_of_div_op_per_cycle    = number_of_divisions     / total_layer_cycles
            number_of_act_op_per_cycle    = number_of_activations   / total_layer_cycles

            number_of_arith_op_per_cycle  = number_of_mlt_op_per_cycle + number_of_add_op_per_cycle + number_of_div_op_per_cycle + number_of_act_op_per_cycle

            total_number_of_arith_op_per_cycle += number_of_arith_op_per_cycle

            ratio_compute       = float(total_layer_compute_cycles)             / float(total_layer_cycles)
            ratio_load_param    = float(total_layer_load_param_cycles)          / float(total_layer_cycles)
            ratio_load_data     = float(total_layer_load_data_cycles)           / float(total_layer_cycles)
            ratio_load          = float(total_layer_load_cycles)                / float(total_layer_cycles)
            ratio_store         = float(total_layer_store_data_cycles)          / float(total_layer_cycles)
            ratio_multiplier    = float(total_multiplication_sequential_cycles) / float(total_layer_cycles)
            ratio_adder         = float(total_addition_sequential_cycles)       / float(total_layer_cycles)
            ratio_divider       = float(total_division_sequential_cycles)       / float(total_layer_cycles)
            ratio_activation    = float(total_activation_sequential_cycles)     / float(total_layer_cycles)

            #Print Statics for Layer
            f_out.writelines('Layer' + str(layer_id) + ': ' + record_layer_type.pop() + '\n')

            f_out.writelines('Operations\n')
            f_out.writelines("Number of Data Loads      : {0:21d} [ops]\n".format(int(number_of_data_loads)))
            f_out.writelines("Number of Param Loads     : {0:21d} [ops]\n".format(int(number_of_param_loads)))
            f_out.writelines("Number of Stores          : {0:21d} [ops]\n".format(int(number_of_data_stores)))
            f_out.writelines("Number of Multiplications : {0:21d} [ops]\n".format(int(number_of_multiplies)))
            f_out.writelines("Number of Additions       : {0:21d} [ops]\n".format(int(number_of_additions)))
            f_out.writelines("Number of Divisions       : {0:21d} [ops]\n".format(int(number_of_divisions)))
            f_out.writelines("Number of Activations     : {0:21d} [ops]\n".format(int(number_of_activations)))
            f_out.writelines("Number of Arithmetics     : {0:21d} [ops]\n\n".format(int(total_arithmetics)))

            f_out.writelines('Operations per Cycle\n')
            f_out.writelines("Multiplications           : {: 3.18f}\t[ops/cycle]\n".format(number_of_mlt_op_per_cycle))
            f_out.writelines("Additions                 : {: 3.18f}\t[ops/cycle]\n".format(number_of_add_op_per_cycle))
            f_out.writelines("Divisions                 : {: 3.18f}\t[ops/cycle]\n".format(number_of_div_op_per_cycle))
            f_out.writelines("Activations               : {: 3.18f}\t[ops/cycle]\n".format(number_of_act_op_per_cycle))
            f_out.writelines("Arithmetics               : {: 3.18f}\t[ops/cycle]\n\n".format(number_of_arith_op_per_cycle))

            f_out.writelines("Execution Cycles\n")
            f_out.writelines("Data Load                 : {0:21d} [cycles]\n".format(int(total_layer_load_data_cycles)))
            f_out.writelines("Param Load                : {0:21d} [cycles]\n".format(int(total_layer_load_param_cycles)))
            f_out.writelines("Data Store                : {0:21d} [cycles]\n".format(int(total_layer_store_data_cycles)))
            f_out.writelines("Multiplication            : {0:21d} [cycles]\n".format(int(total_multiplication_sequential_cycles)))
            f_out.writelines("Addition                  : {0:21d} [cycles]\n".format(int(total_addition_sequential_cycles)))
            f_out.writelines("Division                  : {0:21d} [cycles]\n".format(int(total_division_sequential_cycles)))
            f_out.writelines("Activation                : {0:21d} [cycles]\n".format(int(total_activation_sequential_cycles)))
            f_out.writelines("Arithmetic                : {0:21d} [cycles]\n".format(int(total_layer_compute_cycles)))
            f_out.writelines("Total                     : {0:21d} [cycles]\n\n".format(int(total_layer_cycles)))

            f_out.writelines('Execution Cycles Breakdown\n')
            f_out.writelines("Data Load                 : {: 3.18f}\t[%]\n".format(ratio_load_data  * 100.0))
            f_out.writelines("Param Load                : {: 3.18f}\t[%]\n".format(ratio_load_param * 100.0))
            f_out.writelines("Data Store                : {: 3.18f}\t[%]\n".format(ratio_store      * 100.0))
            f_out.writelines("Multiplication            : {: 3.18f}\t[%]\n".format(ratio_multiplier * 100.0))
            f_out.writelines("Addition                  : {: 3.18f}\t[%]\n".format(ratio_adder      * 100.0))
            f_out.writelines("Division                  : {: 3.18f}\t[%]\n".format(ratio_divider    * 100.0))
            f_out.writelines("Activation                : {: 3.18f}\t[%]\n".format(ratio_activation * 100.0))
            f_out.writelines("Arithmetic                : {: 3.18f}\t[%]\n\n".format(ratio_compute    * 100.0))

            f_out.writelines("Execution Time\n")
            total_layer_time    = total_layer_compute_cycles / execution_clock_frequency + total_layer_load_data_cycles / load_clock_frequency + total_layer_load_param_cycles / load_clock_frequency + total_layer_store_data_cycles / store_clock_frequency
            f_out.writelines("Data Load                 : {: 3.18f}\t[msec]\n".format(1000 * total_layer_load_data_cycles / load_clock_frequency))
            f_out.writelines("Param Load                : {: 3.18f}\t[msec]\n".format(1000 * total_layer_load_param_cycles / load_clock_frequency))
            f_out.writelines("Data Store                : {: 3.18f}\t[msec]\n".format(1000 * total_layer_store_data_cycles / store_clock_frequency))
            f_out.writelines("Multiplication            : {: 3.18f}\t[msec]\n".format(1000 * total_multiplication_sequential_cycles / execution_clock_frequency))
            f_out.writelines("Addition                  : {: 3.18f}\t[msec]\n".format(1000 * total_addition_sequential_cycles / execution_clock_frequency))
            f_out.writelines("Division                  : {: 3.18f}\t[msec]\n".format(1000 * total_division_sequential_cycles / execution_clock_frequency))
            f_out.writelines("Activation                : {: 3.18f}\t[msec]\n".format(1000 * total_activation_sequential_cycles / execution_clock_frequency))
            f_out.writelines("Arithmetic                : {: 3.18f}\t[msec]\n".format(1000 * total_layer_compute_cycles / execution_clock_frequency))
            f_out.writelines("Total                     : {: 3.18f}\t[msec]\n\n".format(1000 * total_layer_time))

            f_out.writelines("Execution Time Breakdown\n")
            f_out.writelines("Data Load                 : {: 3.18f}\t[%]\n".format(100 * total_layer_load_data_cycles / load_clock_frequency / total_layer_time))
            f_out.writelines("Param Load                : {: 3.18f}\t[%]\n".format(100 * total_layer_load_param_cycles / load_clock_frequency / total_layer_time))
            f_out.writelines("Data Store                : {: 3.18f}\t[%]\n".format(100 * total_layer_store_data_cycles / store_clock_frequency / total_layer_time))
            f_out.writelines("Multiplication            : {: 3.18f}\t[%]\n".format(100 * total_multiplication_sequential_cycles / execution_clock_frequency / total_layer_time))
            f_out.writelines("Addition                  : {: 3.18f}\t[%]\n".format(100 * total_addition_sequential_cycles / execution_clock_frequency / total_layer_time))
            f_out.writelines("Division                  : {: 3.18f}\t[%]\n".format(100 * total_division_sequential_cycles / execution_clock_frequency / total_layer_time))
            f_out.writelines("Activation                : {: 3.18f}\t[%]\n".format(100 * total_activation_sequential_cycles / execution_clock_frequency / total_layer_time))
            f_out.writelines("Arithmetic                : {: 3.18f}\t[%]\n".format(100 * total_layer_compute_cycles / execution_clock_frequency / total_layer_time))
            f_out.writelines("Total                     : {: 3.18f}\t[%]\n\n".format(100 * total_layer_time / total_layer_time))

            f_out.writelines("Energy Consumption\n")
            total_energy_data_read  = float(number_of_data_loads   * energy_dram_read)
            total_energy_param_read = float(number_of_param_loads  * energy_dram_read)
            total_energy_data_write = float(number_of_data_stores  * energy_dram_write)
            total_energy_multiplier = float(number_of_multiplies   * energy_multiplier)
            total_energy_adder      = float(number_of_additions    * energy_adder)
            total_energy_divider    = float(number_of_divisions    * energy_divider)
            total_energy_activation = float(number_of_activations  * energy_activation)
            layer_total_energy      = total_energy_data_read + total_energy_data_write + total_energy_param_read + total_energy_multiplier + total_energy_adder + total_energy_divider + total_energy_activation
            total_energy            += layer_total_energy

            f_out.writelines("Energy on Data Load       : {: 3.18f}\t[mJ]\n".format(total_energy_data_read  * 1000.0))
            f_out.writelines("Energy on Param Load      : {: 3.18f}\t[mJ]\n".format(total_energy_param_read * 1000.0))
            f_out.writelines("Energy on Data Store      : {: 3.18f}\t[mJ]\n".format(total_energy_data_write * 1000.0))
            f_out.writelines("Energy on Multipliers     : {: 3.18f}\t[mJ]\n".format(total_energy_multiplier * 1000.0))
            f_out.writelines("Energy on Adders          : {: 3.18f}\t[mJ]\n".format(total_energy_adder      * 1000.0))
            f_out.writelines("Energy on Dividers        : {: 3.18f}\t[mJ]\n".format(total_energy_divider    * 1000.0))
            f_out.writelines("Energy on Activations     : {: 3.18f}\t[mJ]\n".format(total_energy_activation * 1000.0))
            f_out.writelines("Total Energy              : {: 3.18f}\t[mJ]\n\n".format(layer_total_energy    * 1000.0))

            f_out.writelines("Energy Breakdown\n")
            f_out.writelines("Data Load                 : {: 3.18f}\t[%]\n".format(total_energy_data_read   / layer_total_energy * 100.0))
            f_out.writelines("Param Load                : {: 3.18f}\t[%]\n".format(total_energy_param_read  / layer_total_energy * 100.0))
            f_out.writelines("Data Store                : {: 3.18f}\t[%]\n".format(total_energy_data_write  / layer_total_energy * 100.0))
            f_out.writelines("Multipliers               : {: 3.18f}\t[%]\n".format(total_energy_multiplier  / layer_total_energy * 100.0))
            f_out.writelines("Adders                    : {: 3.18f}\t[%]\n".format(total_energy_adder       / layer_total_energy * 100.0))
            f_out.writelines("Dividers                  : {: 3.18f}\t[%]\n".format(total_energy_divider     / layer_total_energy * 100.0))
            f_out.writelines("Activations               : {: 3.18f}\t[%]\n\n".format(total_energy_activation/ layer_total_energy * 100.0))

            power                   = (total_energy_multiplier + total_energy_adder + total_energy_divider + total_energy_activation) * execution_clock_frequency + (total_energy_data_read + total_energy_param_read) * load_clock_frequency + total_energy_data_write * store_clock_frequency

            ops                     = number_of_arith_op_per_cycle * execution_clock_frequency

            f_out.writelines("Total Power Consumption   : {: 3.18f}\t[W]\n".format(power))
            f_out.writelines("Operations per Second     : {: 3.18f}\t[ops/second]\n".format(ops))
            f_out.writelines("Power-Efficiency          : {: 3.18f}\t[GOPS/W]\n\n\n".format(ops / power / 1000000000.0))


            #Recording
            total_load_data_energy[layer_id]        = total_energy_data_read
            total_load_param_energy[layer_id]       = total_energy_param_read
            total_store_data_energy[layer_id]       = total_energy_data_write
            total_multiplication_energy[layer_id]   = total_energy_multiplier
            total_addition_energy[layer_id]         = total_energy_adder
            total_division_energy[layer_id]         = total_energy_divider
            total_activation_energy[layer_id]       = total_energy_activation
            total_layer_energy[layer_id]            = layer_total_energy

            total_exec_load_data_cycles[layer_id]       = total_layer_load_data_cycles
            total_exec_load_param_cycles[layer_id]      = total_layer_load_param_cycles
            total_exec_store_data_cycles[layer_id]      = total_layer_store_data_cycles
            total_exec_multiplication_cycles[layer_id]  = total_multiplication_sequential_cycles
            total_exec_addition_cycles[layer_id]      = total_addition_sequential_cycles
            total_exec_division_cycles[layer_id]        = total_division_sequential_cycles
            total_exec_activation_cycles[layer_id]      = total_activation_sequential_cycles
            total_exec_cycles[layer_id]                 = total_layer_cycles

    f_out.writelines("\n")

    #Total Statics
    f_out.writelines("3.Total Statictics\n")

    #Execution Time
    total_execution_time        = float(total_cycles) / float(execution_clock_frequency)

    #Total Number of Arithmetic Operations
    total_number_of_arith_op    = total_number_of_multiplies + total_number_of_additions + total_number_of_divisions + total_number_of_activations
    total_number_of_load_op     = total_number_of_data_loads + total_number_of_param_loads
    total_number_of_store_op    = total_number_of_data_stores
    total_operations            = total_number_of_arith_op + total_number_of_load_op + total_number_of_store_op

    ratio_total_loads_data      = float(total_number_of_data_loads)     / float(total_operations)
    ratio_total_loads_param     = float(total_number_of_param_loads)    / float(total_operations)
    ratio_total_stores          = float(total_number_of_data_stores)    / float(total_operations)
    ratio_multiplications       = float(total_number_of_multiplies)     / float(total_operations)
    ratio_additions             = float(total_number_of_additions)      / float(total_operations)
    ratio_divisions             = float(total_number_of_divisions)      / float(total_operations)
    ratio_activations           = float(total_number_of_activations)    / float(total_operations)

    f_out.writelines("Data Loads                : {0:21d} [ops]\n".format(int(total_number_of_data_loads)))
    f_out.writelines("Param Loads               : {0:21d} [ops]\n".format(int(total_number_of_param_loads)))
    f_out.writelines("Stores                    : {0:21d} [ops]\n".format(int(total_number_of_data_stores)))
    f_out.writelines("Multiply                  : {0:21d} [ops]\n".format(int(total_number_of_multiplies)))
    f_out.writelines("Addition                  : {0:21d} [ops]\n".format(int(total_number_of_additions)))
    f_out.writelines("Division                  : {0:21d} [ops]\n".format(int(total_number_of_divisions)))
    f_out.writelines("Activation                : {0:21d} [ops]\n".format(int(total_number_of_activations)))
    f_out.writelines("Total Arithmetic          : {0:21d} [ops]\n".format(int(total_number_of_arith_op)))
    f_out.writelines("Total Execution Operations: {0:21d} [ops]\n\n".format(int(total_operations)))

    f_out.writelines("Operations Breakdown\n")
    f_out.writelines("Data Loads                : {: 3.18f}\t[%]\n".format(ratio_total_loads_data   * 100.0))
    f_out.writelines("Param Loads               : {: 3.18f}\t[%]\n".format(ratio_total_loads_param  * 100.0))
    f_out.writelines("Stores                    : {: 3.18f}\t[%]\n".format(ratio_total_stores       * 100.0))
    f_out.writelines("Multiply                  : {: 3.18f}\t[%]\n".format(ratio_multiplications    * 100.0))
    f_out.writelines("Addition                  : {: 3.18f}\t[%]\n".format(ratio_additions          * 100.0))
    f_out.writelines("Division                  : {: 3.18f}\t[%]\n".format(ratio_divisions          * 100.0))
    f_out.writelines("Activation                : {: 3.18f}\t[%]\n".format(ratio_activations        * 100.0))
    f_out.writelines("Total Arithmetics         : {: 3.18f}\t[%]\n".format(total_number_of_arith_op / total_operations * 100.0))

    ops                         = total_number_of_arith_op_per_cycle * execution_clock_frequency
    TOPS                        = ops / 1000000000000.0
    f_out.writelines("TOPS                      : {: 3.18f}\t[TOPS]\n\n".format(TOPS))

    f_out.writelines('Operations per Cycle\n')
    f_out.writelines("Multiplications           : {: 3.18f}\t[ops/cycle]\n".format(total_number_of_multiplies / total_cycles))
    f_out.writelines("Additions                 : {: 3.18f}\t[ops/cycle]\n".format(total_number_of_additions / total_cycles))
    f_out.writelines("Divisions                 : {: 3.18f}\t[ops/cycle]\n".format(total_number_of_divisions / total_cycles))
    f_out.writelines("Activations               : {: 3.18f}\t[ops/cycle]\n".format(total_number_of_activations / total_cycles))
    f_out.writelines("Arithmetics               : {: 3.18f}\t[ops/cycle]\n\n".format(total_number_of_arith_op / total_cycles))

    #Execution Cycle Breakdown
    total_mem_operations        = (total_number_of_data_loads + total_number_of_param_loads) * (execution_clock_frequency / load_clock_frequency) + total_number_of_data_stores * (execution_clock_frequency / store_clock_frequency)

    ratio_total_loads_data      = float(total_number_of_data_loads)     / float(total_cycles)
    ratio_total_loads_param     = float(total_number_of_param_loads)    / float(total_cycles)
    ratio_total_stores          = float(total_number_of_data_stores)    / float(total_cycles)
    ratio_multiplications       = float(total_multiplication_cycles)    / float(total_cycles)
    ratio_additions             = float(total_addition_cycles)          / float(total_cycles)
    ratio_divisions             = float(total_division_cycles)          / float(total_cycles)
    ratio_activations           = float(total_activation_cycles)        / float(total_cycles)
    ratio_total_compute         = ratio_multiplications + ratio_additions + ratio_divisions + ratio_activations
    f_out.writelines("Execution Cycle\n")
    f_out.writelines("Data Loads                : {0:21d} [cycles]\n".format(int(total_load_data_cycles)))
    f_out.writelines("Param Loads               : {0:21d} [cycles]\n".format(int(total_load_param_cycles)))
    f_out.writelines("Stores                    : {0:21d} [cycles]\n".format(int(total_store_data_cycles)))
    f_out.writelines("Multiply                  : {0:21d} [cycles]\n".format(int(total_multiplication_cycles)))
    f_out.writelines("Addition                  : {0:21d} [cycles]\n".format(int(total_addition_cycles)))
    f_out.writelines("Division                  : {0:21d} [cycles]\n".format(int(total_division_cycles)))
    f_out.writelines("Activation                : {0:21d} [cycles]\n".format(int(total_activation_cycles)))
    f_out.writelines("Total Execution Cycles    : {0:21d} [cycles]\n".format(int(total_cycles)))
    f_out.writelines("Execution Time            : {: 3.18f}\t[msec]\n\n".format(total_execution_time * 1000.0))

    f_out.writelines("Execution Cycle Breakdown\n")
    f_out.writelines("Data Loads                : {: 3.18f}\t[%]\n".format(ratio_total_loads_data   * 100.0))
    f_out.writelines("Param Loads               : {: 3.18f}\t[%]\n".format(ratio_total_loads_param  * 100.0))
    f_out.writelines("Stores                    : {: 3.18f}\t[%]\n".format(ratio_total_stores       * 100.0))
    f_out.writelines("Multiply                  : {: 3.18f}\t[%]\n".format(ratio_multiplications    * 100.0))
    f_out.writelines("Addition                  : {: 3.18f}\t[%]\n".format(ratio_additions          * 100.0))
    f_out.writelines("Division                  : {: 3.18f}\t[%]\n".format(ratio_divisions          * 100.0))
    f_out.writelines("Activation                : {: 3.18f}\t[%]\n".format(ratio_activations        * 100.0))
    f_out.writelines("Total Arithmetics         : {: 3.18f}\t[%]\n\n\n".format(ratio_total_compute      * 100.0))


    f_out.writelines("4.Implementation Requirement\n")
    prerequisist_total_exexcution_time      = config_hard['prerequisist_total_exexcution_time']
    prerequisist_clock_frequency            = config_hard['prerequisist_clock_frequency']
    execution_clock_frequency_needed        = float(total_cycles) / float(prerequisist_total_exexcution_time)
    number_of_cycles_needed                 = float(prerequisist_total_exexcution_time) * float(prerequisist_clock_frequency)
    number_of_multiply_cycles_needed        = number_of_cycles_needed * ratio_multiplications
    number_of_addition_cycles_needed        = number_of_cycles_needed * ratio_additions
    number_of_divition_cycles_needed        = number_of_cycles_needed * ratio_divisions
    number_of_activation_cycles_needed      = number_of_cycles_needed * ratio_activations

    f_out.writelines("Prerequisists Latency     : {: 3.18f}\t[sec] needing of:\n".format(float(prerequisist_total_exexcution_time)))
    f_out.writelines("Clock Frequency           : {: 3.18f}\t[MHz]\n".format(execution_clock_frequency_needed / 1000000.0))
    f_out.writelines("Prerequisists Clock Freq. : {: 3.18f}\t[Hz]  needing of:\n".format(float(prerequisist_clock_frequency)))
    f_out.writelines("Data-Level Parallelism    : {: 3.18f}\t[MADs]\n\n\n".format(float(total_multiplication_cycles + total_addition_cycles + total_division_cycles + total_activation_cycles) / float(number_of_multiply_cycles_needed + number_of_addition_cycles_needed)))


    f_out.writelines("5.Energy & Power Consumptions\n")

    #Total Number of Arithmetic Operations
    total_number_of_arith_op    = total_number_of_multiplies + total_number_of_additions + total_number_of_divisions + total_number_of_activations
    total_number_of_load_op     = total_number_of_data_loads + total_number_of_param_loads
    total_number_of_store_op    = total_number_of_data_stores
    total_operations            = total_number_of_arith_op + total_number_of_load_op + total_number_of_store_op

    ratio_total_loads_data      = float(total_number_of_data_loads)     / float(total_operations)
    ratio_total_loads_param     = float(total_number_of_param_loads)    / float(total_operations)
    ratio_total_stores          = float(total_number_of_data_stores)    / float(total_operations)
    ratio_multiplications       = float(total_number_of_multiplies)     / float(total_operations)
    ratio_additions             = float(total_number_of_additions)      / float(total_operations)
    ratio_divisions             = float(total_number_of_divisions)      / float(total_operations)
    ratio_activations           = float(total_number_of_activations)    / float(total_operations)


    total_energy_data_read  = ratio_total_loads_data    * energy_dram_read   * (float(load_clock_frequency) / float(execution_clock_frequency))
    total_energy_param_read = ratio_total_loads_param   * energy_dram_read   * (float(load_clock_frequency) / float(execution_clock_frequency))
    total_energy_data_write = ratio_total_stores        * energy_dram_write  * (float(store_clock_frequency) / float(execution_clock_frequency))
    total_energy_multiplier = ratio_multiplications     * energy_multiplier
    total_energy_adder      = ratio_additions           * energy_adder
    total_energy_divider    = ratio_divisions           * energy_divider
    total_energy_activation = ratio_activations         * energy_activation

    total_energy_load       = total_energy_data_read + total_energy_param_read
    total_energy_store      = total_energy_data_write
    total_energy_arithmetic = total_energy_multiplier + total_energy_adder + total_energy_divider + total_energy_activation
    total_energy            = total_energy_load + total_energy_store + total_energy_arithmetic

    f_out.writelines("Data Load                 : {: 3.18f}\t[mJ]\n".format(total_energy_data_read  * 1000.0))
    f_out.writelines("Data Store                : {: 3.18f}\t[mJ]\n".format(total_energy_data_write * 1000.0))
    f_out.writelines("Param Load                : {: 3.18f}\t[mJ]\n".format(total_energy_param_read * 1000.0))
    f_out.writelines("Multipliers               : {: 3.18f}\t[mJ]\n".format(total_energy_multiplier * 1000.0))
    f_out.writelines("Adders                    : {: 3.18f}\t[mJ]\n".format(total_energy_adder      * 1000.0))
    f_out.writelines("Dividers                  : {: 3.18f}\t[mJ]\n".format(total_energy_divider    * 1000.0))
    f_out.writelines("Activations               : {: 3.18f}\t[mJ]\n".format(total_energy_activation * 1000.0))
    f_out.writelines("Total                     : {: 3.18f}\t[mJ]\n\n".format(total_energy          * 1000.0))

    f_out.writelines("Energy Breakdown\n")
    f_out.writelines("Data Load                 : {: 3.18f}\t[%]\n".format(total_energy_data_read   / total_energy * 100.0))
    f_out.writelines("Data Store                : {: 3.18f}\t[%]\n".format(total_energy_data_write  / total_energy * 100.0))
    f_out.writelines("Param Load                : {: 3.18f}\t[%]\n".format(total_energy_param_read  / total_energy * 100.0))
    f_out.writelines("Multipliers               : {: 3.18f}\t[%]\n".format(total_energy_multiplier  / total_energy * 100.0))
    f_out.writelines("Adders                    : {: 3.18f}\t[%]\n".format(total_energy_adder       / total_energy * 100.0))
    f_out.writelines("Dividers                  : {: 3.18f}\t[%]\n".format(total_energy_divider     / total_energy * 100.0))
    f_out.writelines("Activations               : {: 3.18f}\t[%]\n\n".format(total_energy_activation/ total_energy * 100.0))

    Wattage                 = (total_energy_load * load_clock_frequency)+ (total_energy_store * store_clock_frequency) + total_energy_arithmetic * float(execution_clock_frequency)
    f_out.writelines("Total Power Consumption   : {: 3.18f}\t[W]\n".format(Wattage))
    f_out.writelines("Power-Efficiency          : {: 3.18f}\t[TOPS/W]\n\n\n".format(TOPS / Wattage))


    total_multiplication_cycles     = 0
    total_addition_cycles           = 0
    total_division_cycles           = 0
    total_activation_cycles         = 0
    total_compute_cycles            = 0
    total_load_cycles               = 0
    total_store_cycles              = 0
    total_cycles_                   = 0


    f_out.writelines("6.Summary\n")
    f_out.writelines("                        ")
    f_out.writelines("Load Data                                                                                     ")
    f_out.writelines("Load Param                                                                                      ")
    f_out.writelines("Store Data                                                                                      ")
    f_out.writelines("Multiply                                                                                        ")
    f_out.writelines("Addition                                                                                        ")
    f_out.writelines("Division                                                                                        ")
    f_out.writelines("Activation                                                                                     ")
    f_out.writelines("Layer\n")
    f_out.writelines("         layer type:    ")
    f_out.writelines("ops          ratio,          cycles          ratio,           energy [pJ]   ratio,            ")
    f_out.writelines("ops            ratio,          cycles          ratio,          energy [pJ]    ratio,            ")
    f_out.writelines("ops            ratio,          cycles          ratio,          energy [pJ]    ratio,            ")
    f_out.writelines("ops            ratio,          cycles          ratio,          energy [pJ]    ratio,            ")
    f_out.writelines("ops            ratio,          cycles          ratio,          energy [pJ]    ratio,            ")
    f_out.writelines("ops            ratio,          cycles          ratio,          energy [pJ]    ratio,            ")
    f_out.writelines("ops            ratio,          cycles          ratio,          energy [pJ]    ratio,           energy [pJ]    ratio\n")

    percent                         = 100.0
    scale                           = 1000000000000.0
    total_energy_                   = 0.0

    for layer_id in range(number_of_layers):
        if layer_id > 0:
            layer_energy_total                      = total_layer_energy[layer_id]
            total_energy_                           += layer_energy_total

    for layer_id in range(number_of_layers):
        if layer_id > 0:
            total_layer_data_loads                  = statics_total_number_of_loads_data[layer_id]
            total_layer_param_loads                 = statics_total_number_of_loads_param[layer_id]
            total_layer_data_stores                 = statics_total_number_of_stores_data[layer_id]
            total_layer_multiplies                  = statics_total_number_of_multiplies[layer_id]
            total_layer_additions                   = statics_total_number_of_additions[layer_id]
            total_layer_divisions                   = statics_total_number_of_divisions[layer_id]
            total_layer_activations                 = statics_total_number_of_activations[layer_id]
            total_layer_operations                  = total_layer_data_loads + total_layer_param_loads + total_layer_data_stores + total_layer_multiplies + total_layer_additions + total_layer_divisions + total_layer_activations

            total_layer_load_data_cycles            = total_exec_load_data_cycles[layer_id]
            total_layer_load_param_cycles           = total_exec_load_param_cycles[layer_id]
            total_layer_store_data_cycles           = total_exec_store_data_cycles[layer_id]
            total_layer_multiplication_cycles       = total_exec_multiplication_cycles[layer_id]
            total_layer_addition_cycles             = total_exec_addition_cycles[layer_id]
            total_layer_division_cycles             = total_exec_division_cycles[layer_id]
            total_layer_activation_cycles           = total_exec_activation_cycles[layer_id]
            total_layer_cycles                      = total_exec_cycles[layer_id]

            total_energy_data_read                  = total_load_data_energy[layer_id]
            total_energy_param_read                 = total_load_param_energy[layer_id]
            total_energy_data_write                 = total_store_data_energy[layer_id]
            total_energy_multiplier                 = total_multiplication_energy[layer_id]
            total_energy_adder                      = total_addition_energy[layer_id]
            total_energy_divider                    = total_division_energy[layer_id]
            total_energy_activation                 = total_activation_energy[layer_id]
            layer_energy_total                      = total_layer_energy[layer_id]

            f_out.writelines('Layer\t{0:3d}\t({1:})\t{2:12d}\t{3:3.6f}\t[%],\t{4:12d}\t{5:3.6f}\t[%],\t{6:3.6f}\t{7:3.6f}\t[%],\t{8:12d}\t{9:3.6f}\t[%],\t{10:12d}\t{11:3.6f}\t[%],\t{12:3.6f}\t{13:3.6f}\t[%],\t{14:12d}\t{15:3.6f}\t[%],\t{16:12d}\t{17:3.6f}\t[%],\t{18:3.6f}\t{19:3.6f}\t[%],\t{20:12d}\t{21:3.6f}\t[%],\t{22:12d}\t{23:3.6f}\t[%],\t{24:3.6f}\t{25:3.6f}\t[%],\t{26:12d}\t{27:3.6f}\t[%],\t{28:12d}\t{29:3.6f}\t[%],\t{30:3.6f}\t{31:3.6f}\t[%],\t{32:12d}\t{33:3.6f}\t[%],\t{34:12d}\t{35:3.6f}\t[%],\t{36:3.6f}\t{37:3.6f}\t[%],\t{38:12d}\t{39:3.6f}\t[%],\t{40:12d}\t{41:3.6f}\t[%],\t{42:3.6f}\t{43:3.6f}\t[%],\t{44:3.6f}\t{45:3.6f}\t[%]\n'.format(layer_id, record_layer_type_[layer_id][:11], int(total_layer_data_loads), percent * total_layer_data_loads / total_layer_operations, int(total_layer_load_data_cycles), percent * total_layer_load_data_cycles / total_layer_cycles, scale * total_energy_data_read, percent * total_energy_data_read / layer_energy_total, int(total_layer_param_loads), percent * total_layer_param_loads / total_layer_operations, int(total_layer_load_param_cycles), percent * total_layer_load_param_cycles / total_layer_cycles, scale * total_energy_param_read, percent * total_energy_param_read / layer_energy_total, int(total_layer_data_stores), percent * total_layer_data_stores / total_layer_operations, int(total_layer_store_data_cycles), percent * total_layer_store_data_cycles / total_layer_cycles, scale * total_energy_data_write, percent * total_energy_data_write / layer_energy_total, int(total_layer_multiplies), percent * total_layer_multiplies / total_layer_operations, int(total_layer_multiplication_cycles), percent * total_layer_multiplication_cycles / total_layer_cycles, scale * total_energy_multiplier, percent * total_energy_multiplier / layer_energy_total, int(total_layer_additions), percent * total_layer_additions / total_layer_operations, int(total_layer_addition_cycles), percent * total_layer_addition_cycles / total_layer_cycles, scale * total_energy_adder, percent * total_energy_adder / layer_energy_total, int(total_layer_divisions), percent * total_layer_divisions / total_layer_operations, int(total_layer_division_cycles), percent * total_layer_division_cycles / total_layer_cycles, scale * total_energy_divider, percent * total_energy_divider / layer_energy_total, int(total_layer_activations), percent * total_layer_activations / total_layer_operations, int(total_layer_activation_cycles), percent * total_layer_activation_cycles / total_layer_cycles, scale * total_energy_activation, percent * total_energy_activation / layer_energy_total, scale * layer_energy_total, percent * layer_energy_total / total_energy_, total_layer_cycles))

    f_out.close()
