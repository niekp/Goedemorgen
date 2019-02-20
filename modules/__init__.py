from os.path import dirname, basename, isfile
import glob

from modules._Module import _Module

files = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in files if isfile(f) and not f.endswith('__init__.py') and not f.endswith('_Module.py')]
