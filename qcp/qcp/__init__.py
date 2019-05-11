# TREAT AS PACKAGE

from .chemData import *
from .clean import *
from .energy import *
from .genJob import *
from .genJobCP import *
from .general import *
from .geometry import *
from .inflate import *
from .logFile import *
from .pprint import *
from .runTasks import *
from .separate import *
from .supercomp import *
from .system import *
from .tempInp import *
from .templates import *
from .write import *
from .utils import *

def _get_all_imports():
    """
    Return list of all the imports
    This prevents sub-modules (geoms, stats, utils, ...)
    from being imported into the user namespace by the
    following import statement
        from plotnine import *
    This is because `from Module import Something`
    leads to `Module` itself coming into the namespace!!
    """
    import types
    lst = [name for name, obj in globals().items()
           if not (name.startswith('_') or
                   name == 'absolute_import' or
                   isinstance(obj, types.ModuleType))]
    return lst


__all__ = _get_all_imports()
