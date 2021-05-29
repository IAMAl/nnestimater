#!/usr/bin/python
# coding: UTF-8
import datetime
import argparse

import read_src_file                        as rd_file
import parser_hardware_model                as parser_hrd
import parser_network_model                 as parser_net

import layer_compression_ratio              as comp_ratio
import conv_size_calc                       as conv_size_fd
import conv_size_calc_transposed            as conv_size_tr

import statics_load_cycles_sequential       as load_cycles
import statics_store_cycles_sequential      as store_cycles
import statics_activation_cycles_sequential as store_cycles

import forward_window_param_extract         as window_param_extract

import calc_layers                          as calc
import statistics                           as stat


#Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Neural Network Estimater')
    parser.add_argument('--src_file_name',          '-s',   default='./nn_config.txt',      help='network confifguration file name')
    parser.add_argument('--cfg_file_name',          '-c',   default='./hard_config.txt',    help='hardware confifguration file name')
    parser.add_argument('--out_file_name',          '-o',   default='./nn_estimated.txt',   help='output file name')
    parser.add_argument('--stride_effect',          '-se',  default='off',                  help='on: remove stride access cycles')
    parser.add_argument('--zero_skipping_operation','-zso', default='off',                  help='on: enable zero-skipping operation')
    parser.add_argument('--zero_skipping_load',     '-zsl', default='off',                  help='on: enable zero-skipping load')
    parser.add_argument('--compressed_load_act',    '-cla', default='off',                  help='on: enable compression for activations')
    parser.add_argument('--compressed_load_par',    '-clp', default='off',                  help='on: enable compression for parameters')
    parser.add_argument('--pipeline',               '-ppl', default='off',                  help='on: enable pipeline on datapath')
    parser.add_argument('--process',                '-scl', default=0,                      help='semiconductor process [nm]')

    args            = parser.parse_args()
    pipeline        = args.pipeline
    process         = args.process

    print("Start Estimation.")

    src_f_lines     = rd_file.read_src_file(args.src_file_name)
    config_layers   = parser_net.parser_network_model(src_f_lines)

    cfg_f_lines     = rd_file.read_src_file(args.cfg_file_name)
    config_hard     = parser_hrd.parser_hardware_model(cfg_f_lines)

    f_out, record_layer_type, active_func_type, statics_total_number_of_loads_data, statics_total_number_of_loads_param, statics_total_number_of_stores_data,statics_total_number_of_inputs, statics_total_number_of_params, statics_total_number_of_outputs, statics_total_number_of_multiplies,statics_total_number_of_additions, statics_total_number_of_divisions, statics_total_number_of_activations = calc.calc_layers(args, config_layers, config_hard)

    stat.statistics(\
        process, \
        pipeline, \
        config_layers, \
        config_hard, \
        f_out, \
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
        statics_total_number_of_activations\
        )

    print("End   Estimation.")
