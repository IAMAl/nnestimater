#Statistics
import numpy
import statics_load_cycles_sequential       as statics_ld_cycles
import statics_store_cycles_sequential      as statics_st_cycles
import statics_activation_cycles_sequential as statics_act_cycles

import statistics_layers
import statistics_total
import statistics_implement
import statistics_energy_power
import statistics_summary


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
	number_of_layers					= len(config_layers)

	#Operation Calculations
	total_number_of_data_loads			= 0
	total_number_of_param_loads			= 0
	total_number_of_data_stores			= 0

	total_number_of_multiplies			= 0
	total_number_of_additions			= 0
	total_number_of_divisions			= 0
	total_number_of_activations			= 0

	#Cycle Calculations
	total_load_data_cycles				= 0
	total_load_param_cycles				= 0
	total_store_data_cycles				= 0

	total_multiplication_cycles			= 0
	total_addition_cycles				= 0
	total_division_cycles				= 0
	total_activation_cycles				= 0

	total_number_of_arith_op_per_cycle	= 0.0

	#Total Cycles
	total_cycles						= 0

	#Total Energy
	total_energy						= 0.0

	#Cost for Multiplication
	number_of_cycles_for_multiplication	= int(config_hard['number_of_cycles_for_multiplication'])
	dwidth_for_multiplication			= int(config_hard['dwidth_for_multiplication'])

	#Cost for Addition
	number_of_cycles_for_addition		= int(config_hard['number_of_cycles_for_addition'])
	dwidth_for_addition					= int(config_hard['dwidth_for_addition'])

	#Cost for Division
	number_of_cycles_for_division		= int(config_hard['number_of_cycles_for_division'])
	dwidth_for_division					= int(config_hard['dwidth_for_division'])

	#Data Width on Memory Interface
	load_dtype							= int(config_hard['load_dtype'])
	store_dtype							= int(config_hard['load_dtype'])

	#Cost for Activation
	number_of_cycles_for_activation		= ''

	#Semiconductor Process
	semi_process						= float(config_hard['semi_process'])

	if process == 0:
		process							= float(config_hard['semi_process'])

	#Scale Factor
	scale_factor						= float(process) / float(semi_process)

	#Energy Consumption on Components
	energy_multiplier					= float(config_hard['energy_multiplier'])   * scale_factor * scale_factor   / 1000000000000.0
	energy_adder 						= float(config_hard['energy_adder'])        * scale_factor                  / 1000000000000.0
	energy_divider						= float(config_hard['energy_divider'])      * scale_factor * scale_factor   / 1000000000000.0
	energy_activation					= float(config_hard['energy_activation'])   * scale_factor                  / 1000000000000.0
	energy_reg_read 					= float(config_hard['energy_reg_read'])     * scale_factor                  / 1000000000000.0
	energy_reg_write					= float(config_hard['energy_reg_write'])    * scale_factor                  / 1000000000000.0
	energy_sram_static					= float(config_hard['energy_reg_write'])    * scale_factor * scale_factor   / 1000000000000.0
	energy_sram_read					= float(config_hard['energy_sram_read'])    * scale_factor                  / 1000000000000.0
	energy_sram_write					= float(config_hard['energy_sram_write'])   * scale_factor                  / 1000000000000.0
	energy_dram_read					= float(config_hard['energy_dram_read'])    / 1000000000000.0
	energy_dram_write					= float(config_hard['energy_dram_write'])   / 1000000000000.0

	#On-Chip Clock Frequency
	execution_clock_frequency			= float(config_hard['exexcution_clock_frequency'])

	#External Memory Load Parameters
	load_clock_frequency				= int(config_hard['load_clock_frequency'])
	load_dwidth							= int(config_hard['load_dtype'])
	number_of_parallel_loads			= int(config_hard['number_of_parallel_loads'])

	#External Memory Store Parameters
	store_clock_frequency				= int(config_hard['store_clock_frequency'])
	store_dwidth						= int(config_hard['store_dtype'])
	number_of_parallel_stores			= int(config_hard['number_of_parallel_stores'])

	#Recording
	total_load_data_energy 				= numpy.zeros(number_of_layers + 1)
	total_load_param_energy				= numpy.zeros(number_of_layers + 1)
	total_store_data_energy				= numpy.zeros(number_of_layers + 1)
	total_multiplication_energy			= numpy.zeros(number_of_layers + 1)
	total_addition_energy				= numpy.zeros(number_of_layers + 1)
	total_division_energy				= numpy.zeros(number_of_layers + 1)
	total_activation_energy				= numpy.zeros(number_of_layers + 1)
	total_layer_energy					= numpy.zeros(number_of_layers + 1)

	total_exec_load_data_cycles			= numpy.zeros(number_of_layers + 1)
	total_exec_load_param_cycles		= numpy.zeros(number_of_layers + 1)
	total_exec_store_data_cycles		= numpy.zeros(number_of_layers + 1)
	total_exec_multiplication_cycles	= numpy.zeros(number_of_layers + 1)
	total_exec_addition_cycles			= numpy.zeros(number_of_layers + 1)
	total_exec_division_cycles			= numpy.zeros(number_of_layers + 1)
	total_exec_activation_cycles        = numpy.zeros(number_of_layers + 1)
	total_exec_cycles					= numpy.zeros(number_of_layers + 1)


	active_func_type					= active_func_type.copy()
	#active_func_type.pop()
	#active_func_type.reverse()

	record_layer_type					= record_layer_type.copy()
	record_layer_type.reverse()
	record_layer_type.pop()


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
		total_energy = statistics_layers(
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
			)


	TOPS = statistics_total(
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
		)

	statistics_implement(
		f_out,
			config_hard,
			total_cycles,
			ratio_multiplications,
			ratio_additions,
			ratio_divisions,
			ratio_activations,
			total_multiplication_cycles,
			total_addition_cycles,
			total_division_cycles,
			total_activation_cycles
		)


	ratio_total_loads_data, \
		ratio_total_loads_param, \
		ratio_total_stores, \
		ratio_multiplications, \
		ratio_additions, \
		ratio_divisions, \
		ratio_activations = statistics_energy_power(
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
		)


	statistics_summary(
		f_out, \
			number_of_layers, \
			statics_total_number_of_loads_data, \
			statics_total_number_of_loads_param, \
			statics_total_number_of_stores_data, \
			statics_total_number_of_multiplies, \
			statics_total_number_of_additions, \
			statics_total_number_of_divisions, \
			statics_total_number_of_activations, \
			total_exec_load_data_cycles, \
			total_exec_load_param_cycles, \
			total_exec_store_data_cycles, \
			total_exec_multiplication_cycles, \
			total_exec_addition_cycles, \
			total_exec_division_cycles, \
			total_exec_activation_cycles, \
			total_exec_cycles, \
			total_layer_energy, \
			total_load_data_energy, \
			total_load_param_energy, \
			total_store_data_energy, \
			total_multiplication_energy, \
			total_addition_energy, \
			total_division_energy, \
			total_activation_energy
		)

	f_out.close()
