#Forward-Pooling
import numpy
import layer_compression_ratio      as layer_comp_ratio
import forward_window_param_extract as fwd_win_extract


def forward_pool(\
	args, \
	f_out, \
	config_hard, \
	config_prev_layer, \
	config_pres_layer, \
	dim, \
	input_length_\
	):

	#dwidth_of_pres_inputs   = int(config_pres_layer['dwidth_of_inputs'])
	#dwidth_of_pres_outputs  = int(config_pres_layer['dwidth_of_outputs'])
	#dwidth_of_prev_inputs   = int(config_prev_layer['dwidth_of_inputs'])
	#dwidth_of_prev_outputs  = int(config_prev_layer['dwidth_of_outputs'])

	#Compression Ratio Extraction
	zero_ratio_op, \
		zero_ratio_ma, \
		compress_ratio_act_prev, \
		compress_ratio_par_prev = layer_comp_ratio.layer_compression_ratio(args, config_prev_layer)

	zero_ratio_op, \
		zero_ratio_ma, \
		compress_ratio_act_pres, \
		compress_ratio_par_pres = layer_comp_ratio.layer_compression_ratio(args, config_pres_layer)

	input_length	= numpy.zeros(dim)
	output_length	= numpy.zeros(dim)
	window_length	= numpy.zeros(dim)
	delite			= numpy.zeros(dim)
	stride			= numpy.zeros(dim)
	padding1		= numpy.zeros(dim)
	padding2		= numpy.zeros(dim)

	frame_length	= numpy.zeros(dim)

	input_size		= 1
	output_size		= 1
	window_size		= 1

	aspect_ratio	= 1.0

	for no_dim in range(dim):
		input_length[no_dim]	= int(config_pres_layer['input_dim'+str(no_dim)])

		output_length[no_dim], \
			window_length[no_dim], \
			delite[no_dim], \
			stride[no_dim], \
			padding1[no_dim], \
			padding2[no_dim]	= fwd_win_extract.forward_window_param_extract(config_pres_layer, no_dim)

		frame_length[no_dim]	= input_length[no_dim]

		input_size				*= frame_length[no_dim]
		output_size				*= output_length[no_dim]
		window_size				*= window_length[no_dim]

		aspect_ratio			*= numpy.ceil(float(frame_length[no_dim] / stride[no_dim]))

	#Sequential 2D-Convolution (per Channel)
	number_of_parallel_kernels	= int(config_pres_layer['number_of_parallel_kernels'])
	total_number_of_multiplies	= 0
	total_number_of_additions	= output_size * (window_size - 1) * number_of_parallel_kernels * (1 - zero_ratio_op)
	total_number_of_divisions	= 0
	total_number_of_activations	= 0

	#Number of Input Data
	total_number_of_inputs		= input_size

	#Number of Input Activations
	number_of_loads_data		= number_of_parallel_kernels * input_size

	#Number of Loads Activations
	total_number_of_loads_data	= numpy.ceil((1 - compress_ratio_act_prev) * (1 - zero_ratio_ma) * number_of_loads_data)

	#Number of Cycles for Loading Activations
	#total_load_sequential_cycles            = statics_load_cycles_sequential(config_hard,  total_number_of_loads_data)

	#Number of Input Parameters
	number_of_parallel_loads	= int(config_hard['number_of_parallel_loads'])
	total_number_of_params		= 0

	#Number of Parameters (including Biases)
	number_of_parameters		= 0

	#Number of Input Parameters
	number_of_loads_parameter	= numpy.ceil(float(number_of_parameters) / float(number_of_parallel_loads))

	#Number of Loads Parameters
	total_number_of_loads_param	= numpy.ceil((1 - compress_ratio_par_pres) * (1 - zero_ratio_ma) * number_of_loads_parameter)

	#Number of Cycles for Loading Parameters
	#total_load_param_sequential_cycles     = statics_load_cycles_sequential(config_hard, total_number_of_loads_parameter)

	#Number of Output Data
	total_number_of_outputs		= output_size

	#Number of Output Activations
	number_of_stores_data		= number_of_parallel_kernels * output_size

	#Number of Stores Activations
	total_number_of_stores_data	= numpy.ceil((1 - compress_ratio_act_pres) * (1 - zero_ratio_ma) * number_of_stores_data)

	#Number of Cycles for Activation Store
	#total_store_sequential_cycles           = statics_store_cycles_sequential(config_hard, number_of_stores_data)

	f_out.writelines("In  Activation     :  ")
	for no_dim in range(dim):
		f_out.writelines("{0:9d}, ".format(int(input_length[no_dim])))

	f_out.writelines("\n")
	f_out.writelines("Out Activation     :  ")
	for no_dim in range(dim):
		f_out.writelines("{0:9d}, ".format(int(output_length[no_dim])))

	f_out.writelines("\n")
	f_out.writelines("Param              :  ")
	for no_dim in range(dim):
		f_out.writelines("{0:9d}, ".format(int(window_length[no_dim])))

	f_out.writelines("\n")
	for no_dim in range(dim):
		f_out.writelines("Padding-{0:d}          :        {1:3d},       {2:3d}\n".format(no_dim, int(padding1[no_dim]), int(padding2[no_dim])))

	f_out.writelines("Stride             : ")
	for no_dim in range(dim):
		f_out.writelines("       {0:3d},".format(int(stride[no_dim])))

	f_out.writelines("\n")
	f_out.writelines("Total Inputs/Ch    :{0:22d}\n".format(int(total_number_of_inputs)))
	f_out.writelines("Total Params/Ch    :{0:22d}\n".format(int(total_number_of_params)))
	f_out.writelines("Total Outputs/Ch   :{0:22d}\n".format(int(total_number_of_outputs)))

	return total_number_of_loads_data, \
			total_number_of_loads_param, \
			total_number_of_stores_data, \
			total_number_of_inputs, \
			total_number_of_params, \
			total_number_of_outputs, \
			total_number_of_multiplies, \
			total_number_of_additions, \
			total_number_of_divisions, \
			total_number_of_activations, \
			output_length
