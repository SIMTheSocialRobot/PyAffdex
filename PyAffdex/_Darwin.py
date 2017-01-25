import objc, os
from . import *
from Foundation import NSObject

AFFDEX_FRAMEWORK = "Affdex.framework"
AFFDEX_FRAMEWORK_PATHS = [ "/Library/Frameworks", "/System/Library/Frameworks", "~/Library/Frameworks", "./" ]
AFFDEX_FRAMEWORK_PATH = None
AFFDEX_LIB = "%s/%s" % (AFFDEX_FRAMEWORK, "Affdex")

bundle = None
frameworkPath = None

def findAndLoadAffdexFramework():
    frameworkPath = _findAffdexFramework()
    _loadAffdexFramework(frameworkPath)

def _findAffdexFramework():
    found = False

    for path in AFFDEX_FRAMEWORK_PATHS:
        print("Checking for %s in %s... " % (AFFDEX_FRAMEWORK, path), end='')
        libpath = os.path.expanduser("%s/%s"%(path, AFFDEX_LIB))
        fwpath = os.path.expanduser("%s/%s"%(path, AFFDEX_FRAMEWORK))

        if os.path.isfile(libpath):
            print("found")
            frameworkPath = fwpath
            
            found = True
            break
        else:
            print("not found")

    if not found:
        raise ImportError("Cound not find `Affdex.framework` in any of these locations: %s" % AFFDEX_FRAMEWORK_PATHS)
    else:
        return frameworkPath

def _loadAffdexFramework(fwPath):
    AFFDEX_BUNDLE = objc.initFrameworkWrapper(\
        "Affdex", \
        frameworkIdentifier = "com.affectiva.Affdex", \
        frameworkPath = objc.pathForFramework(fwPath), \
        globals = globals())

class PyAFDXDetector:
    def __init__(self, *args, **kwargs):
        if (len(args) > 0):
            raise ValueError("All arguments must be named.")
        
        self._detector = AFDXDetector.alloc().init()

        #ObjC provides 7 different init methods
        if (len(kwargs) is 4 and 'discreteImages' in kwargs and 'maximumFaces' in kwargs and 'faceMode' in kwargs and 'delegate' in kwargs):
            self._instance = self._detector.initWithDelegate_discreteImages_maximumFaces_faceMode_(kwargs.get('delegate'), kwargs.get('discreteImages'), kwargs.get('maximumFaces'), kwargs.get('faceMode'))
            self._delegate = kwargs.get('delegate')

    def detectAllEmotions(self, bool):
        self._detector.setDetectAllEmotions_(bool)

    def detectAllExpressions(self, bool):
        self._detector.setDetectAllExpressions_(bool)

    def detectAllEmojis(self, bool):
        self._detector.setDetectEmojis_(bool)

    # reaaalllly dont want to write these all out....
    def joy(self):
        return self._detector.joy() == 1

    def isRunning(self):
        return self._detector.isRunning() == 1

    def start(self):
        started = self._detector.start()
        if started is not None:
            raise ValueError("oops")

    def stop(self):
        stopped = self._detector.stop()
        if stopped is not None:
            raise ValueError("oops")

    def reset(self):
        reset = self._detector.reset()
        if reset is not None:
            raise ValueError("oops")

    def processImage(self, pathToPicture):
        if os.path.isfile(pathToPicture):
            image = NSImage.alloc().initWithContentsOfFile_(pathToPicture)
            self._detector.processImage_(image)
        else:
            raise ValueError("%s not found" % (pathToPicture))

    def delegate(self):
        return self._delegate

# This should be overridden by the client. Also provides more 'Pythonic' class function names
class PyAFDXDetectorDelegate():

    def detectorDidFinishProcessing_(self, detector):
        if hasattr(self, "didFinishProcessing"):
            self.didFinishProcessing(detector, face)
        else:
            print(">> PyAFDXDetectorDelegate.detectorDidFinishProcessing (default implementation)")

    def detector_didStartDetectingFace_(self, detector, face):
        if "didStartDetectingFace" in dir(self):
            self.didStartDetectingFace(detector, face)
        else:
            print(">> PyAFDXDetectorDelegate.didStartDetectingFace (default implementation)")

    def detector_didStopDetectingFace_(self, detector, face):
        if "didStopDetectingFace" in dir(self):
            self.didStopDetectingFace(detector, face)
        else:
            print(">> PyAFDXDetectorDelegate.didStopDetectingFace (default implementation)")

    def detector_hasResults_forImage_atTime_(self, detector, faces, image, time):
        if "hasResults" in dir(self):
            self.hasResults(detector, faces, image, time)
        else:
            print(">> PyAFDXDetectorDelegate.hasResults (default implementation)")