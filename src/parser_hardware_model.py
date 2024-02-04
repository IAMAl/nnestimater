# Hardware Model Parser
def parser_hardware_model(f_lines):
	print("Start Hardware Model Parser.")
	token_number = 0

	config_hardware = {}

	for line in f_lines:
		tokens = line.split()

		item = ''
		for token in tokens:
			if ((token_number & 1) == 0): 
				item = str(token)
			if ((token_number & 1) == 1):          
				config_hardware.update({item:token})

			token_number += 1

	print("End   Hardware Model Parser.")
	return config_hardware
