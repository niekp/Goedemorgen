from os.path import dirname, basename, isfile
import glob

from modules._Module import _Module

files = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in files if isfile(f) and not f.endswith('__init__.py') and not f.endswith('_Module.py')]

#from modules.Afval import Afval
#from modules.Downtime import Downtime
#from modules.Weer import Weer
#from modules.Agenda import Agenda
#from modules.LastFmDisconnected import LastFmDisconnected
#from modules.MarkdownTodo import MarkdownTodo
#from modules.Muspy import Muspy
#from modules.SociaalWerker import SociaalWerker
#from modules.LastFmRecommendation import LastFmRecommendation
#from modules.Syncthing import Syncthing
