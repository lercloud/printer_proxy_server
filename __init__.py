import os, sys

# Add the local Python libraries to the Python path.
def update_path():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(cur_dir + "/lib/python2.7/site-packages")

update_path()


