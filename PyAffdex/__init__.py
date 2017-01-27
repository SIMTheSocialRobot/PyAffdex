import platform, os, sys
from enum import IntEnum

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
    raise ImportError("Not yet implemented")
    _WINDOWS = True
    from . import _Windows
    pass

else:
    raise ImportError("Unsupported System: %s" % platform.system())

#
# API Classes
#
class Age(IntEnum):
    Unknown = 0,
    Under18 = 1,
    Between18and24 = 2
    Between25and34 = 3
    Between35and44 = 4
    Between45and54 = 5
    Between55and64 = 6
    OlderThan65 = 7

class CameraType(IntEnum):
    Front = 1
    Back = 2

class Emoji(IntEnum):
    Disappointed = 128542
    Flushed = 128563
    Kissing = 128535
    Laughing = 128518
    Rage = 128545
    Relaxed = 9786
    Scream = 128561
    Smily = 128515
    Smirk = 128527
    StuckOutTongue = 128539
    StuckOutTongueWinkingEye = 128540
    Unknown = 128528
    Wink = 128521

class Ethnicity(IntEnum):
    BlackAfrican = 2
    Caucasian = 1
    EastAsian = 4
    Hispanic = 5
    SouthAsian = 3
    Unknown = 0

class FaceDetectionMode(IntEnum):
    Large = 0
    Small = 1

class Gender(IntEnum):
    Unknown = 0,
    Male = 1,
    Female = 2

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