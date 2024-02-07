#Calculation on Layers
import numpy
import forward_conv         as fwd_conv
import forward_pool         as fwd_pool
import forward_batchnorm    as fwd_bnorm
import forward_fullconnect  as fwd_fconnect


def calc_layers(args, config_layers, config_hard):

	f_out = open(args.out_file_name, 'w')

	print("Start Layer Calculation.")

	number_of_layers= len(config_layers)

	#Statics Variables
	statics_total_number_of_loads_data	= numpy.zeros(number_of_layers + 1)
	statics_total_number_of_loads_param	= numpy.zeros(number_of_layers + 1)
	statics_total_number_of_stores_data	= numpy.zeros(number_of_layers + 1)
	statics_total_number_of_inputs		= numpy.zeros(number_of_layers + 1)
	statics_total_number_of_params		= numpy.zeros(number_of_layers + 1)
	statics_total_number_of_outputs		= numpy.zeros(number_of_layers + 1)
	statics_total_number_of_multiplies	= numpy.zeros(number_of_layers + 1)
	statics_total_number_of_additions	= numpy.zeros(number_of_layers + 1)
	statics_total_number_of_divisions	= numpy.zeros(number_of_layers + 1)
	statics_total_number_of_activations	= numpy.zeros(number_of_layers + 1)

	active_func_type					= []
	record_layer_type					= []
	execution_type						= config_hard['execution_type']

	f_out.writelines("1.Network Topology\n")

	for layer_id in range(number_of_layers):
		for pres_counter in range(number_of_layers):

			config_pres_layer = config_layers[pres_counter]

			if (layer_id == int(config_pres_layer['layer'])):
				if (layer_id == 0):

					config_prev_layer		= config_pres_layer

					number_of_output_parallel_kernels	= int(config_pres_layer['number_of_parallel_kernels'])

					dim						= int(config_pres_layer['dimension'])
					output_length			= numpy.zeros(dim)
					layer_type				= config_pres_layer['layer_type']
					act_type				= config_pres_layer['activation_type']

					pass
				elif (layer_id > 0):

					for prev_counter in range(number_of_layers):

						config_prev_layer		= config_layers[prev_counter]
						prev_layer_id			= int(config_prev_layer['layer'])

						#Number of Channels
						number_of_input_parallel_kernels		= number_of_output_parallel_kernels
						number_of_output_parallel_kernels		= int(config_pres_layer['number_of_parallel_kernels'])

						if ((prev_layer_id == (layer_id - 1)) & (execution_type == 'sequential')):

							dim						= int(config_pres_layer['dimension'])
							layer_type				= config_pres_layer['layer_type']
							act_type				= config_pres_layer['activation_type']

							# Cost Calculation Body
							f_out.writelines("\n" + layer_type + " Layer" + "\n")

							f_out.writelines("Total In  Channels :{0:22d}\n".format(number_of_input_parallel_kernels))
							f_out.writelines("Total Out Channels :{0:22d}\n".format(number_of_output_parallel_kernels))

							#Convolution
							if ((layer_type == 'convolution') | (layer_type == 'transposed_convolution')):
								statics_total_number_of_loads_data[layer_id], \
									statics_total_number_of_loads_param[layer_id], \
									statics_total_number_of_stores_data[layer_id], \
									statics_total_number_of_inputs[layer_id], \
									statics_total_number_of_params[layer_id], \
									statics_total_number_of_outputs[layer_id], \
									statics_total_number_of_multiplies[layer_id], \
									statics_total_number_of_additions[layer_id], \
									statics_total_number_of_divisions[layer_id], \
									statics_total_number_of_activations[layer_id], \
									output_length   = fwd_conv.forward_conv(args, f_out, config_hard, config_prev_layer, config_pres_layer, dim, output_length)

							#Pooling
							elif (layer_type == 'max_pooling'):
								statics_total_number_of_loads_data[layer_id], \
									statics_total_number_of_loads_param[layer_id], \
									statics_total_number_of_stores_data[layer_id], \
									statics_total_number_of_inputs[layer_id], \
									statics_total_number_of_params[layer_id], \
									statics_total_number_of_outputs[layer_id], \
									statics_total_number_of_multiplies[layer_id], \
									statics_total_number_of_additions[layer_id], \
									statics_total_number_of_divisions[layer_id], \
									statics_total_number_of_activations[layer_id], \
									output_length   = fwd_pool.forward_pool(args, f_out, config_hard, config_prev_layer, config_pres_layer, dim, output_length)

							#Batch Normalization
							elif (layer_type == 'batch_normalization'):
								statics_total_number_of_loads_data[layer_id], \
									statics_total_number_of_loads_param[layer_id], \
									statics_total_number_of_stores_data[layer_id], \
									statics_total_number_of_inputs[layer_id], \
									statics_total_number_of_params[layer_id], \
									statics_total_number_of_outputs[layer_id], \
									statics_total_number_of_multiplies[layer_id], \
									statics_total_number_of_additions[layer_id], \
									statics_total_number_of_divisions[layer_id], \
									statics_total_number_of_activations[layer_id], \
									output_length   = fwd_bnorm.forward_batchnorm(args, f_out, config_hard, config_prev_layer, config_pres_layer, dim, output_length)

							#Full Connection
							elif (layer_type == 'full_connection'):
								statics_total_number_of_loads_data[layer_id], \
									statics_total_number_of_loads_param[layer_id], \
									statics_total_number_of_stores_data[layer_id], \
									statics_total_number_of_inputs[layer_id], \
									statics_total_number_of_params[layer_id], \
									statics_total_number_of_outputs[layer_id], \
									statics_total_number_of_multiplies[layer_id], \
									statics_total_number_of_additions[layer_id], \
									statics_total_number_of_divisions[layer_id], \
									statics_total_number_of_activations[layer_id], \
									output_length   = fwd_fconnect.forward_fullconnect(args, f_out, config_hard, config_prev_layer, config_pres_layer, dim, output_length)
							else:
								print("WARNING: Not Defined Layer {} is used.".format(layer_type))

							break

				#Collect Statics
				record_layer_type.append(layer_type)
				active_func_type.append(act_type)

	print("End   Layer Calculation.")

	return f_out, \
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
			statics_total_number_of_activations
