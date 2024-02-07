def statistics_implement(
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
    ):
    
	f_out.writelines("4.Implementation Requirement\n")
	prerequisist_total_exexcution_time	= config_hard['prerequisist_total_exexcution_time']
	prerequisist_clock_frequency		= config_hard['prerequisist_clock_frequency']
	execution_clock_frequency_needed	= float(total_cycles) / float(prerequisist_total_exexcution_time)
	number_of_cycles_needed				= float(prerequisist_total_exexcution_time) * float(prerequisist_clock_frequency)
	number_of_multiply_cycles_needed	= number_of_cycles_needed * ratio_multiplications
	number_of_addition_cycles_needed	= number_of_cycles_needed * ratio_additions
	number_of_divition_cycles_needed	= number_of_cycles_needed * ratio_divisions
	number_of_activation_cycles_needed	= number_of_cycles_needed * ratio_activations

	f_out.writelines("Prerequisists Latency     : {: 3.18f}\t[sec] needing of:\n".format(float(prerequisist_total_exexcution_time)))
	f_out.writelines("Clock Frequency           : {: 3.18f}\t[MHz]\n".format(execution_clock_frequency_needed / 1000000.0))
	f_out.writelines("Prerequisists Clock Freq. : {: 3.18f}\t[Hz]  needing of:\n".format(float(prerequisist_clock_frequency)))
	f_out.writelines("Data-Level Parallelism    : {: 3.18f}\t[MADs]\n\n\n".format(float(total_multiplication_cycles + total_addition_cycles + total_division_cycles + total_activation_cycles) / float(number_of_multiply_cycles_needed + number_of_addition_cycles_needed)))
