import platform, os, sys

_DARWIN = False
_WINDOWS = False
_LINUX = False

sys.tracebacklimit = 0

if platform.system() == "Darwin":
    from ._Darwin import findAndLoadAffdexFramework
    findAndLoadAffdexFramework()
    _DARWIN = True
    # import all the OSX-specifics
    from . import _Darwin
    from ._Darwin import PyAFDXDetectorDelegate

elif platform.system() == "Windows":
    #raise ImportError("Not yet implemented")
    _WINDOWS = True
    pass
else:
    raise ImportError("Unsupported System: %s" % platform.system())

#
# API Functions
#
def createPyAFDXFaceFromAFDXFace():
    return None

#
# API Classes
#

class PyAFDXFace(object):
    def __init__(self, id):
        self._id = id
        self._orientation = None

    def id(self):
        return self._id

    def orientation(self, orientation=None):
        return self._orientation

class PyAFDXOrientation(object):

    def __init__(self, yaw=None, pitch=None, roll=None, interocularDistance=None):
        self._yaw = yaw
        self._pitch = pitch
        self._roll = roll
        self._interocularDistance = interocularDistance

#
# Platform-specific Wrapper Classes
#

if _DARWIN:
    class PyAFDXDetector(_Darwin.PyAFDXDetector):
        pass

elif _WINDOWS:
    from . import _Windows

    class PyAFDXDetector(_Windows.PyAFDXDetector):
        pass