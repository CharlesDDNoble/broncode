import string
import os
import random

def make_dir():
    alpha_num = string.ascii_letters + string.digits
    dir_name = ''.join(random.choices(alpha_num, k = 32))
    os.mkdir(dir_name)
    return dir_name


name = make_dir()
print("Made directory: "+name)
print("Deleting directory: "+name)
os.rmdir(name)
