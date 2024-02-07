def statistics_layers(
		f_out, \
			number_of_layers, \
			config_layers, \
			config_hard, \
			record_layer_type, \
			statics_total_number_of_loads_data, \
			statics_total_number_of_loads_param, \
			statics_total_number_of_stores_data, \
			statics_total_number_of_multiplies, \
			statics_total_number_of_additions, \
			statics_total_number_of_divisions, \
			statics_total_number_of_activations, \
			load_dtype, \
			store_dtype, \
			statics_ld_cycles, \
			statics_st_cycles, \
			dwidth_for_multiplication, \
			number_of_cycles_for_multiplication, \
			number_of_cycles_for_addition, \
			number_of_cycles_for_division, \
			number_of_activations, \
			active_func_type, \
			statics_act_cycles, \
			pipeline, \
			execution_clock_frequency, \
			load_clock_frequency, \
			store_clock_frequency, \
			energy_dram_read, \
			energy_dram_write, \
			energy_multiplier, \
			energy_adder, \
			energy_divider, \
			energy_activation, \
			total_load_data_energy, \
			total_load_param_energy, \
			total_store_data_energy, \
			total_multiplication_energy, \
			total_addition_energy, \
			total_division_energy, \
			total_activation_energy, \
			total_layer_energy, \
			total_exec_load_data_cycles, \
			total_exec_load_param_cycles, \
			total_exec_store_data_cycles, \
			total_exec_multiplication_cycles, \
			total_exec_addition_cycles, \
			total_exec_division_cycles, \
			total_exec_activation_cycles, \
			total_exec_cycles
		):
	
	f_out.writelines("\n\n\n2.Statistics for Layers\n")

	total_number_of_data_loads = 0
	total_number_of_param_loads = 0
	total_number_of_data_stores = 0
	total_number_of_multiplies = 0
	total_number_of_additions = 0
	total_number_of_divisions = 0
	total_number_of_activations = 0
	total_load_data_cycles = 0
	total_load_param_cycles = 0
	total_store_data_cycles = 0
	total_multiplication_cycles = 0
	total_addition_cycles = 0
	total_division_cycles = 0
	total_activation_cycles = 0
	total_number_of_arith_op_per_cycle = 0
	total_cycles, = 0
	total_energy = 0.0

	for layer_id in range(number_of_layers):

		if layer_id > 0 :
			config_prev_layer					= config_layers[layer_id - 1]
			number_of_parallel_in				= int(config_prev_layer['number_of_parallel_kernels'])
			config_pres_layer					= config_layers[layer_id]
			number_of_parallel_out				= int(config_pres_layer['number_of_parallel_kernels'])

			#Number of Operations
			number_of_data_loads				= statics_total_number_of_loads_data[layer_id] * (dwidth_for_multiplication / load_dtype)
			total_number_of_data_loads			+= number_of_data_loads

			number_of_param_loads				= statics_total_number_of_loads_param[layer_id] * (dwidth_for_multiplication / load_dtype)
			total_number_of_param_loads			+= number_of_param_loads

			number_of_data_stores				= statics_total_number_of_stores_data[layer_id] * (dwidth_for_multiplication / store_dtype)
			total_number_of_data_stores			+= number_of_data_stores

			number_of_multiplies				= statics_total_number_of_multiplies[layer_id]
			total_number_of_multiplies			+= number_of_multiplies

			number_of_additions					= statics_total_number_of_additions[layer_id]
			total_number_of_additions			+= number_of_additions

			number_of_divisions					= statics_total_number_of_divisions[layer_id]
			total_number_of_divisions			+= number_of_divisions

			number_of_activations				= statics_total_number_of_activations[layer_id]
			total_number_of_activations			+= number_of_activations


			total_layer_load_data_cycles		= statics_ld_cycles.statics_load_cycles_sequential(config_hard, number_of_data_loads)
			total_load_data_cycles				+= total_layer_load_data_cycles

			total_layer_load_param_cycles		= statics_ld_cycles.statics_load_cycles_sequential(config_hard, number_of_param_loads)
			total_load_param_cycles				+= total_layer_load_param_cycles

			total_layer_load_cycles				= total_layer_load_data_cycles + total_layer_load_param_cycles

			total_layer_store_data_cycles		= statics_st_cycles.statics_store_cycles_sequential(config_hard, number_of_data_stores)
			total_store_data_cycles				+= total_layer_store_data_cycles

			total_multiplication_sequential_cycles	= number_of_multiplies * number_of_cycles_for_multiplication
			total_multiplication_cycles			+= total_multiplication_sequential_cycles

			total_addition_sequential_cycles	= number_of_additions * number_of_cycles_for_addition
			total_addition_cycles				+= total_addition_sequential_cycles

			total_division_sequential_cycles	= number_of_divisions * number_of_cycles_for_division
			total_division_cycles				+= total_division_sequential_cycles

			number_of_cycles_for_activation		= statics_act_cycles.statics_activation_cycles_sequential(active_func_type[layer_id], config_hard)
			total_activation_sequential_cycles	= number_of_activations * number_of_cycles_for_activation
			total_activation_cycles				+= total_activation_sequential_cycles

			if pipeline == 'off':
				total_layer_compute_cycles			= total_multiplication_sequential_cycles + total_addition_sequential_cycles + total_division_sequential_cycles + total_activation_sequential_cycles
			elif (number_of_cycles_for_multiplication > number_of_cycles_for_addition):
				total_layer_compute_cycles			= total_multiplication_sequential_cycles + total_division_sequential_cycles + total_activation_sequential_cycles + 1
			elif (number_of_cycles_for_multiplication <= number_of_cycles_for_addition):
				total_layer_compute_cycles			= total_addition_sequential_cycles + total_division_sequential_cycles + total_activation_sequential_cycles + 1

			total_layer_cycles					= total_layer_load_data_cycles + total_layer_load_param_cycles + total_layer_store_data_cycles + total_layer_compute_cycles
			total_cycles 						+= total_layer_cycles

			total_arithmetics					= int(number_of_multiplies + number_of_additions + number_of_divisions + number_of_activations)
			total_mem_accesses					= int(number_of_data_loads + number_of_param_loads + number_of_data_stores)

			number_of_mlt_op_per_cycle			= number_of_multiplies    / total_layer_cycles
			number_of_add_op_per_cycle			= number_of_additions     / total_layer_cycles
			number_of_div_op_per_cycle			= number_of_divisions     / total_layer_cycles
			number_of_act_op_per_cycle			= number_of_activations   / total_layer_cycles

			number_of_arith_op_per_cycle		= number_of_mlt_op_per_cycle + number_of_add_op_per_cycle + number_of_div_op_per_cycle + number_of_act_op_per_cycle

			total_number_of_arith_op_per_cycle += number_of_arith_op_per_cycle

			ratio_compute						= float(total_layer_compute_cycles)             / float(total_layer_cycles)
			ratio_load_param 					= float(total_layer_load_param_cycles)          / float(total_layer_cycles)
			ratio_load_data						= float(total_layer_load_data_cycles)           / float(total_layer_cycles)
			ratio_load							= float(total_layer_load_cycles)                / float(total_layer_cycles)
			ratio_store							= float(total_layer_store_data_cycles)          / float(total_layer_cycles)
			ratio_multiplier					= float(total_multiplication_sequential_cycles) / float(total_layer_cycles)
			ratio_adder							= float(total_addition_sequential_cycles)       / float(total_layer_cycles)
			ratio_divider						= float(total_division_sequential_cycles)       / float(total_layer_cycles)
			ratio_activation					= float(total_activation_sequential_cycles)     / float(total_layer_cycles)

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
			total_energy_data_read						= float(number_of_data_loads   * energy_dram_read)
			total_energy_param_read						= float(number_of_param_loads  * energy_dram_read)
			total_energy_data_write						= float(number_of_data_stores  * energy_dram_write)
			total_energy_multiplier						= float(number_of_multiplies   * energy_multiplier)
			total_energy_adder							= float(number_of_additions    * energy_adder)
			total_energy_divider						= float(number_of_divisions    * energy_divider)
			total_energy_activation						= float(number_of_activations  * energy_activation)
			layer_total_energy							= total_energy_data_read + total_energy_data_write + total_energy_param_read + total_energy_multiplier + total_energy_adder + total_energy_divider + total_energy_activation
			total_energy								+= layer_total_energy

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

			power										= (total_energy_multiplier + total_energy_adder + total_energy_divider + total_energy_activation) * execution_clock_frequency + (total_energy_data_read + total_energy_param_read) * load_clock_frequency + total_energy_data_write * store_clock_frequency

			ops											= number_of_arith_op_per_cycle * execution_clock_frequency

			f_out.writelines("Total Power Consumption   : {: 3.18f}\t[W]\n".format(power))
			f_out.writelines("Operations per Second     : {: 3.18f}\t[ops/second]\n".format(ops))
			f_out.writelines("Power-Efficiency          : {: 3.18f}\t[GOPS/W]\n\n\n".format(ops / power / 1000000000.0))


			#Recording
			total_load_data_energy[layer_id]			= total_energy_data_read
			total_load_param_energy[layer_id]			= total_energy_param_read
			total_store_data_energy[layer_id]			= total_energy_data_write
			total_multiplication_energy[layer_id]		= total_energy_multiplier
			total_addition_energy[layer_id]				= total_energy_adder
			total_division_energy[layer_id]				= total_energy_divider
			total_activation_energy[layer_id]			= total_energy_activation
			total_layer_energy[layer_id]				= layer_total_energy

			total_exec_load_data_cycles[layer_id]		= total_layer_load_data_cycles
			total_exec_load_param_cycles[layer_id]		= total_layer_load_param_cycles
			total_exec_store_data_cycles[layer_id]		= total_layer_store_data_cycles
			total_exec_multiplication_cycles[layer_id]	= total_multiplication_sequential_cycles
			total_exec_addition_cycles[layer_id]		= total_addition_sequential_cycles
			total_exec_division_cycles[layer_id]		= total_division_sequential_cycles
			total_exec_activation_cycles[layer_id]		= total_activation_sequential_cycles
			total_exec_cycles[layer_id]					= total_layer_cycles

	f_out.writelines("\n")
 
	return total_load_data_energy, \
			total_load_param_energy, \
			total_store_data_energy, \
			total_multiplication_energy, \
			total_addition_energy, \
			total_division_energy, \
			total_activation_energy, \
			total_layer_energy, \
			total_exec_load_data_cycles, \
			total_exec_load_param_cycles, \
			total_exec_store_data_cycles, \
			total_exec_multiplication_cycles, \
			total_exec_addition_cycles, \
			total_exec_division_cycles, \
			total_exec_activation_cycles, \
			total_exec_cycles, \
			total_number_of_data_loads, \
			total_number_of_param_loads, \
			total_number_of_data_stores, \
			total_number_of_multiplies, \
			total_number_of_additions, \
			total_number_of_divisions, \
			total_number_of_activations, \
			total_load_data_cycles, \
			total_load_param_cycles, \
			total_store_data_cycles, \
			total_multiplication_cycles, \
			total_addition_cycles, \
			total_division_cycles, \
			total_activation_cycles, \
			total_number_of_arith_op_per_cycle, \
			total_cycles, \
    	   	total_energy