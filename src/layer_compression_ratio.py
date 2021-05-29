#Compression Ratio
def layer_compression_ratio(args, config_pres_layer):

    if ((args.zero_skipping_operation == 'on') & ( 'zero_ratio' in config_pres_layer )):
        zero_ratio_op                   = float(config_pres_layer['zero_ratio'])
    else:
        zero_ratio_op                   = 0.0

    if ((args.zero_skipping_load == 'on') & ( 'zero_ratio' in config_pres_layer )):
        zero_ratio_ma                   = float(config_pres_layer['zero_ratio'])
    else:
        zero_ratio_ma                   = 0.0


    if ((args.compressed_load_act == 'on') & ( 'compress_ratio_act' in config_pres_layer )):
        compress_ratio_act               = float(config_pres_layer['compress_ratio_act'])
    else:
        compress_ratio_act               = 0.0

    if ((args.compressed_load_par == 'on') & ( 'compress_ratio_par' in config_pres_layer )):
        compress_ratio_par               = float(config_pres_layer['compress_ratio_par'])
    else:
        compress_ratio_par               = 0.0

    return zero_ratio_op, \
            zero_ratio_ma, \
            compress_ratio_act, \
            compress_ratio_par
