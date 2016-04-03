'''
Created on Apr 2, 2016

@author: root
'''

class _const(object):
    
    class ConstError(TypeError): pass
    
    def __setattr__(self, name, value):
        
        if self.__dict__.has_key(name):
            raise self.ConstError("Can't rebind const %s"%name)
        
        self.__dict__[name] = value

CONST = _const()

CONST.RBT_HOST = "127.0.0.1"

CONST.TTYPES = ["abc", "def", "ghi"]

CONST.TASK_EXH = "tasks"
CONST.TASK_QUE = "tasks"

CONST.STAT_QUE = "stats"

import sys
sys.modules[__name__] = CONST
        
        
    
