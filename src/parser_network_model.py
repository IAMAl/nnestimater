# Network Model Parser
def parser_network_model(f_lines):
	print("Start Network  Model Parser.")
	config_layers = {}

	token_number	= 0
	cnt_layer		= 0
	config_layer	= {}

	for line in f_lines:
		tokens	= line.split()

		item	= ''
		for token in tokens:
			if (token != 'layer_end'):
				if ((token_number & 1) == 0): 
					item = token
				
				if ((token_number & 1) == 1): 
					if (token != 'None'):
						config_layer.update({item:token})
					else:
						config_layer.update({item:token})

				token_number	+= 1

			else:
				config_layers.update({cnt_layer:config_layer})
				config_layer	= {}
				cnt_layer		+= 1
				token_number	= 0

	print("End   Network  Model Parser.")
	return config_layers
