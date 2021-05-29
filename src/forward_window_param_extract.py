#Window Size Extraction
import numpy
import conv_size_calc               as conv_size_fd
import conv_size_calc_transposed    as conv_size_tr

def forward_window_param_extract(config_pres_layer, dim):

    layer_type      = config_pres_layer['layer_type']
    input_size      = int(config_pres_layer['input_dim'+str(dim)])
    kernel_size     = int(config_pres_layer['kernel_dim'+str(dim)])

    if ( 'padding_dim'+str(dim)+"_1" in config_pres_layer ):
        padding_size1   = int(config_pres_layer['padding_dim'+str(dim)+'_0'])
        padding_size2   = int(config_pres_layer['padding_dim'+str(dim)+'_1'])
    else:
        padding_size1   = int(config_pres_layer['padding_dim'+str(dim)+'_0'])
        padding_size2   = padding_size1
        print("WARNING: Second Pad is not Defined, Use of First Pad as Second Pad.")

    delite_size     = int(config_pres_layer['delite_dim'+str(dim)])
    stride_size     = int(config_pres_layer['stride_dim'+str(dim)])

    if ((layer_type == 'convolution') | (layer_type == 'max_pooling')):
        feature_size    = conv_size_fd.conv_size_calc(input_size, kernel_size, padding_size1, padding_size2, delite_size, stride_size)
    else:
        feature_size    = conv_size_tr.conv_size_calc_transposed(input_size, kernel_size, padding_size1, padding_size2, delite_size, stride_size)

    return feature_size, \
            kernel_size, \
            delite_size, \
            stride_size, \
            padding_size1, \
            padding_size2
