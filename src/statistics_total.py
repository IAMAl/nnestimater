def statistics_total(
        f_out, \
            total_cycles, \
            load_clock_frequency, \
            store_clock_frequency, \
            execution_clock_frequency, \
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
            total_number_of_arith_op_per_cycle, \
            total_multiplication_cycles, \
            total_addition_cycles, \
            total_division_cycles, \
            total_activation_cycles
    ):
    
	#Total Statics
	f_out.writelines("3.Total Statictics\n")

	#Execution Time
	total_execution_time				= float(total_cycles) / float(execution_clock_frequency)

	#Total Number of Arithmetic Operations
	total_number_of_arith_op			= total_number_of_multiplies + total_number_of_additions + total_number_of_divisions + total_number_of_activations
	total_number_of_load_op				= total_number_of_data_loads + total_number_of_param_loads
	total_number_of_store_op			= total_number_of_data_stores
	total_operations					= total_number_of_arith_op + total_number_of_load_op + total_number_of_store_op

	ratio_total_loads_data				= float(total_number_of_data_loads)     / float(total_operations)
	ratio_total_loads_param				= float(total_number_of_param_loads)    / float(total_operations)
	ratio_total_stores					= float(total_number_of_data_stores)    / float(total_operations)
	ratio_multiplications				= float(total_number_of_multiplies)     / float(total_operations)
	ratio_additions						= float(total_number_of_additions)      / float(total_operations)
	ratio_divisions						= float(total_number_of_divisions)      / float(total_operations)
	ratio_activations					= float(total_number_of_activations)    / float(total_operations)

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

	ops									= total_number_of_arith_op_per_cycle * execution_clock_frequency
	TOPS								= ops / 1000000000000.0
	f_out.writelines("TOPS                      : {: 3.18f}\t[TOPS]\n\n".format(TOPS))

	f_out.writelines('Operations per Cycle\n')
	f_out.writelines("Multiplications           : {: 3.18f}\t[ops/cycle]\n".format(total_number_of_multiplies / total_cycles))
	f_out.writelines("Additions                 : {: 3.18f}\t[ops/cycle]\n".format(total_number_of_additions / total_cycles))
	f_out.writelines("Divisions                 : {: 3.18f}\t[ops/cycle]\n".format(total_number_of_divisions / total_cycles))
	f_out.writelines("Activations               : {: 3.18f}\t[ops/cycle]\n".format(total_number_of_activations / total_cycles))
	f_out.writelines("Arithmetics               : {: 3.18f}\t[ops/cycle]\n\n".format(total_number_of_arith_op / total_cycles))

	#Execution Cycle Breakdown
	total_mem_operations				= (total_number_of_data_loads + total_number_of_param_loads) * (execution_clock_frequency / load_clock_frequency) + total_number_of_data_stores * (execution_clock_frequency / store_clock_frequency)

	ratio_total_loads_data				= float(total_number_of_data_loads)     / float(total_cycles)
	ratio_total_loads_param				= float(total_number_of_param_loads)    / float(total_cycles)
	ratio_total_stores					= float(total_number_of_data_stores)    / float(total_cycles)
	ratio_multiplications				= float(total_multiplication_cycles)    / float(total_cycles)
	ratio_additions						= float(total_addition_cycles)          / float(total_cycles)
	ratio_divisions						= float(total_division_cycles)          / float(total_cycles)
	ratio_activations					= float(total_activation_cycles)        / float(total_cycles)
	ratio_total_compute					= ratio_multiplications + ratio_additions + ratio_divisions + ratio_activations
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
	f_out.writelines("Total Arithmetics         : {: 3.18f}\t[%]\n\n\n".format(ratio_total_compute  * 100.0))
 
	return TOPS