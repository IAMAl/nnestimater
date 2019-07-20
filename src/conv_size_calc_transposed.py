# Feature Size Calculation
import numpy


def conv_size_calc_transposed(out_base_size, kernel_size, padding_size1, padding_size2, delite_size, stride_size):
    
    if stride_size <= 0:
        print('ERROR: Stride Value is equal to or less than Zero.')
        stride_size     = 1
    elif stride_size == None:
        print('ERROR: Stride Value is Not Dedfined.')
        stride_size     = 1

    in_base_size      = out_base_size +  ((kernel_size - 1) * delite_size + 1) - (padding_size1 + padding_size2)

    #Debug
    if (numpy.mod(out_base_size, stride_size) != 0.0):
        print('ERROR: ({} - (({} - 1) * {} + 1) + {} + {}) mod {} != 0'.format(input_size, kernel_size, delite_size, padding_size1, padding_size2, stride_size))

    input_size   = (in_base_size - 1) * stride_size

    return input_size
