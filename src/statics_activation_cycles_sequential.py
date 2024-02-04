# Sequential Activation
def statics_activation_cycles_sequential(activation_type, config_hard):

	#Number of Cycles for Activation Function
	if (activation_type == 'softmax'):
		number_of_cycles_for_activation_function	= int(config_hard['number_of_cycles_for_act_softmax'])
	elif (activation_type == 'ReLU'):
		number_of_cycles_for_activation_function	= int(config_hard['number_of_cycles_for_act_ReLU'])
	elif (activation_type == 'LReLU'):
		number_of_cycles_for_activation_function	= int(config_hard['number_of_cycles_for_act_LReLU'])
	elif (activation_type == 'PReLU'):
		number_of_cycles_for_activation_function	= int(config_hard['number_of_cycles_for_act_PReLU'])
	elif (activation_type == 'tanh'):
		number_of_cycles_for_activation_function	= int(config_hard['number_of_cycles_for_act_tanh'])
	elif (activation_type == 'sigmoid'):
		number_of_cycles_for_activation_function	= int(config_hard['number_of_cycles_for_act_sigmoid'])
	else:
		number_of_cycles_for_activation_function	= 0

	return number_of_cycles_for_activation_function
