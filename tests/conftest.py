import sys
from os.path import abspath, dirname

root_dir = sys.path.append(dirname(dirname(abspath(__file__))))
sys.path.append('cli_app')
