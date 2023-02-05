try:
    from .production import *
except:
    from .development import *
