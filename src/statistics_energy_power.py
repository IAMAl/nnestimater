def statistics_energy_power(
        f_out, \
            total_number_of_data_loads, \
            total_number_of_param_loads, \
            total_number_of_data_stores, \
            total_number_of_multiplies, \
            total_number_of_additions, \
            total_number_of_divisions, \
            total_number_of_activations, \
            load_clock_frequency, \
            store_clock_frequency, \
            execution_clock_frequency, \
            energy_dram_read, \
            energy_dram_write, \
            energy_multiplier, \
            energy_adder, \
            energy_divider, \
            energy_activation, \
            TOPS
    ):

	f_out.writelines("5.Energy & Power Consumptions\n")

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


	total_energy_data_read				= ratio_total_loads_data    * energy_dram_read   * (float(load_clock_frequency) / float(execution_clock_frequency))
	total_energy_param_read				= ratio_total_loads_param   * energy_dram_read   * (float(load_clock_frequency) / float(execution_clock_frequency))
	total_energy_data_write				= ratio_total_stores        * energy_dram_write  * (float(store_clock_frequency) / float(execution_clock_frequency))
	total_energy_multiplier				= ratio_multiplications     * energy_multiplier
	total_energy_adder					= ratio_additions           * energy_adder
	total_energy_divider				= ratio_divisions           * energy_divider
	total_energy_activation				= ratio_activations         * energy_activation

	total_energy_load					= total_energy_data_read + total_energy_param_read
	total_energy_store					= total_energy_data_write
	total_energy_arithmetic				= total_energy_multiplier + total_energy_adder + total_energy_divider + total_energy_activation
	total_energy						= total_energy_load + total_energy_store + total_energy_arithmetic

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

	Wattage                             = (total_energy_load * load_clock_frequency)+ (total_energy_store * store_clock_frequency) + total_energy_arithmetic * float(execution_clock_frequency)
	f_out.writelines("Total Power Consumption   : {: 3.18f}\t[W]\n".format(Wattage))
	f_out.writelines("Power-Efficiency          : {: 3.18f}\t[TOPS/W]\n\n\n".format(TOPS / Wattage))
 
	return ratio_total_loads_data, \
			ratio_total_loads_param, \
			ratio_total_stores, \
			ratio_multiplications, \
			ratio_additions, \
			ratio_divisions, \
			ratio_activations