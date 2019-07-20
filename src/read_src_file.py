# Read Source File
def read_src_file(src_file_name):
    f = open(src_file_name, 'r')
    f_lines = f.readlines()
    f.close()
    return f_lines
