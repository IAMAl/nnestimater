def statistics_summary(
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
	):

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
			layer_energy_total					= total_layer_energy[layer_id]
			total_energy_ 						+= layer_energy_total

	for layer_id in range(number_of_layers):
		if layer_id > 0:
			total_layer_data_loads 				= statics_total_number_of_loads_data[layer_id]
			total_layer_param_loads				= statics_total_number_of_loads_param[layer_id]
			total_layer_data_stores				= statics_total_number_of_stores_data[layer_id]
			total_layer_multiplies				= statics_total_number_of_multiplies[layer_id]
			total_layer_additions				= statics_total_number_of_additions[layer_id]
			total_layer_divisions				= statics_total_number_of_divisions[layer_id]
			total_layer_activations				= statics_total_number_of_activations[layer_id]
			total_layer_operations				= total_layer_data_loads + total_layer_param_loads + total_layer_data_stores + total_layer_multiplies + total_layer_additions + total_layer_divisions + total_layer_activations

			total_layer_load_data_cycles		= total_exec_load_data_cycles[layer_id]
			total_layer_load_param_cycles		= total_exec_load_param_cycles[layer_id]
			total_layer_store_data_cycles		= total_exec_store_data_cycles[layer_id]
			total_layer_multiplication_cycles	= total_exec_multiplication_cycles[layer_id]
			total_layer_addition_cycles			= total_exec_addition_cycles[layer_id]
			total_layer_division_cycles			= total_exec_division_cycles[layer_id]
			total_layer_activation_cycles		= total_exec_activation_cycles[layer_id]
			total_layer_cycles					= total_exec_cycles[layer_id]

			total_energy_data_read 				= total_load_data_energy[layer_id]
			total_energy_param_read				= total_load_param_energy[layer_id]
			total_energy_data_write				= total_store_data_energy[layer_id]
			total_energy_multiplier				= total_multiplication_energy[layer_id]
			total_energy_adder					= total_addition_energy[layer_id]
			total_energy_divider				= total_division_energy[layer_id]
			total_energy_activation				= total_activation_energy[layer_id]
			layer_energy_total					= total_layer_energy[layer_id]

			f_out.writelines('Layer\t{0:3d}\t({1:})\t{2:12d}\t{3:3.6f}\t[%],\t{4:12d}\t{5:3.6f}\t[%],\t{6:3.6f}\t{7:3.6f}\t[%],\t{8:12d}\t{9:3.6f}\t[%],\t{10:12d}\t{11:3.6f}\t[%],\t{12:3.6f}\t{13:3.6f}\t[%],\t{14:12d}\t{15:3.6f}\t[%],\t{16:12d}\t{17:3.6f}\t[%],\t{18:3.6f}\t{19:3.6f}\t[%],\t{20:12d}\t{21:3.6f}\t[%],\t{22:12d}\t{23:3.6f}\t[%],\t{24:3.6f}\t{25:3.6f}\t[%],\t{26:12d}\t{27:3.6f}\t[%],\t{28:12d}\t{29:3.6f}\t[%],\t{30:3.6f}\t{31:3.6f}\t[%],\t{32:12d}\t{33:3.6f}\t[%],\t{34:12d}\t{35:3.6f}\t[%],\t{36:3.6f}\t{37:3.6f}\t[%],\t{38:12d}\t{39:3.6f}\t[%],\t{40:12d}\t{41:3.6f}\t[%],\t{42:3.6f}\t{43:3.6f}\t[%],\t{44:3.6f}\t{45:3.6f}\t[%]\n'.format(layer_id, record_layer_type_[layer_id][:11], int(total_layer_data_loads), percent * total_layer_data_loads / total_layer_operations, int(total_layer_load_data_cycles), percent * total_layer_load_data_cycles / total_layer_cycles, scale * total_energy_data_read, percent * total_energy_data_read / layer_energy_total, int(total_layer_param_loads), percent * total_layer_param_loads / total_layer_operations, int(total_layer_load_param_cycles), percent * total_layer_load_param_cycles / total_layer_cycles, scale * total_energy_param_read, percent * total_energy_param_read / layer_energy_total, int(total_layer_data_stores), percent * total_layer_data_stores / total_layer_operations, int(total_layer_store_data_cycles), percent * total_layer_store_data_cycles / total_layer_cycles, scale * total_energy_data_write, percent * total_energy_data_write / layer_energy_total, int(total_layer_multiplies), percent * total_layer_multiplies / total_layer_operations, int(total_layer_multiplication_cycles), percent * total_layer_multiplication_cycles / total_layer_cycles, scale * total_energy_multiplier, percent * total_energy_multiplier / layer_energy_total, int(total_layer_additions), percent * total_layer_additions / total_layer_operations, int(total_layer_addition_cycles), percent * total_layer_addition_cycles / total_layer_cycles, scale * total_energy_adder, percent * total_energy_adder / layer_energy_total, int(total_layer_divisions), percent * total_layer_divisions / total_layer_operations, int(total_layer_division_cycles), percent * total_layer_division_cycles / total_layer_cycles, scale * total_energy_divider, percent * total_energy_divider / layer_energy_total, int(total_layer_activations), percent * total_layer_activations / total_layer_operations, int(total_layer_activation_cycles), percent * total_layer_activation_cycles / total_layer_cycles, scale * total_energy_activation, percent * total_energy_activation / layer_energy_total, scale * layer_energy_total, percent * layer_energy_total / total_energy_, total_layer_cycles))