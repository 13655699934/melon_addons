# -*- coding: utf-8 -*-
import platform
import sys
if platform.system() == 'Linux':
    sys.path.append('/mnt')
else:
    pass

from . import  controllers,wizard
