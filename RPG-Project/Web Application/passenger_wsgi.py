import sys
import os

INTERP = os.path.expanduser("/var/www/u2666289/data/lastvesion_flask/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from main import application