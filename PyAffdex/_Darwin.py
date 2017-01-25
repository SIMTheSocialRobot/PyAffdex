import objc, os
from . import *

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

def _createDictFromAFDXAppearance(afdxAppearance):
    appearance = {
        'age': afdxAppearance.age(),
        'ethnicity': afdxAppearance.ethnicity(),
        'gender': afdxAppearance.gender(),
        'glasses': afdxAppearance.glasses() == 1
    }
    return appearance;

def _createDictFromAFDXEmojis(afdxEmojis):
    emojis = {
        'disappointed': afdxEmojis.disappointed(),
        'dominantEmoji': afdxEmojis.dominantEmoji(),
        'flushed': afdxEmojis.flushed(),
        'kissing': afdxEmojis.kissing(),
        'laughing': afdxEmojis.laughing(),
        'rage': afdxEmojis.rage(),
        'relaxed': afdxEmojis.relaxed(),
        'scream': afdxEmojis.scream(),
        'smiley': afdxEmojis.smiley(),
        'smirk': afdxEmojis.smirk(),
        'stuckOutTongue': afdxEmojis.stuckOutTongue(),
        'stuckOutTongueWinkingEye': afdxEmojis.stuckOutTongueWinkingEye(),
        'wink': afdxEmojis.wink()

    }
    return emojis

def _createDictFromAFDXEmotions(afdxEmotions):
    emotions = {
        'anger': afdxEmotions.anger(),
        'contempt': afdxEmotions.contempt(),
        'disgust': afdxEmotions.disgust(),
        'engagement': afdxEmotions.engagement(),
        'fear': afdxEmotions.fear(),
        'joy': afdxEmotions.joy(),
        'sadness': afdxEmotions.sadness(),
        'surprise': afdxEmotions.surprise(),
        'valence': afdxEmotions.valence()
    }
    return emotions

def _createDictFromAFDXExpressions(afdxExpressions):
    expressions = {
        'attention': afdxExpressions.attention(),
        'browFurrow': afdxExpressions.browFurrow(),
        'browRaise': afdxExpressions.browRaise(),
        'cheekRaise': afdxExpressions.cheekRaise(),
        'chinRaise': afdxExpressions.chinRaise(),
        'dimpler': afdxExpressions.dimpler(),
        'eyeClosure': afdxExpressions.eyeClosure(),
        'eyeWiden': afdxExpressions.eyeWiden(),
        'innerBrowRaise': afdxExpressions.innerBrowRaise(),
        'jawDrop': afdxExpressions.jawDrop(),
        'lidTighten': afdxExpressions.lidTighten(),
        'lipCornerDepressor': afdxExpressions.lipCornerDepressor(),
        'lipPress': afdxExpressions.lipPress(),
        'lipPucker': afdxExpressions.lipPucker(),
        'lipStretch': afdxExpressions.lipStretch(),
        'lipSuck': afdxExpressions.lipSuck(),
        'mouthOpen': afdxExpressions.mouthOpen(),
        'noseWrinkle': afdxExpressions.noseWrinkle(),
        'smile': afdxExpressions.smile(),
        'smirk': afdxExpressions.smirk(),
        'upperLipRaise': afdxExpressions.upperLipRaise(),

    }
    return expressions

def _createDictFromAFDXFace(afdxFace):
    face = {
        'appearance': _createDictFromAFDXAppearance(afdxFace.appearance()),
        'emojis': _createDictFromAFDXEmojis(afdxFace.emojis()),
        'emotions': _createDictFromAFDXEmotions(afdxFace.emotions()),
        'expressions': _createDictFromAFDXExpressions(afdxFace.expressions()),
        'faceBounds': _createDictFromCGRect(afdxFace.faceBounds()),
        'facePoints': _createListFromNSArrayOfNSPoints(afdxFace.facePoints()),
        'id': afdxFace.faceId(),
        'orientation': _createDictFromAFDXOrientation(afdxFace.orientation()),
        'userInfo': afdxFace.userInfo()
    }
    return face;

def _createDictFromAFDXOrientation(afdxOrientation):
    orientation = {
        'interocularDistance': afdxOrientation.interocularDistance(),
        'pitch': afdxOrientation.pitch(),
        'roll': afdxOrientation.roll(),
        'yaw': afdxOrientation.yaw()
    }
    return orientation;

def _createDictFromCGRect(cgRect):
    # pyobjc gives it to us as a tuple
    return cgRect

def _createListFromNSArrayOfNSPoints(nsArray):
    # tuple of NSPoints
    array = []
    for point in nsArray:
        pass
        #NSConcreteValue?
        #array.append(point)
    return array

class PyAFDXDetector:

    def __init__(self, *args, **kwargs):
        if (len(args) > 0):
            raise ValueError("All arguments must be named.")

        self._detector = AFDXDetector.alloc().init()

        if (len(kwargs) is 3 and 'delegate' in kwargs and 'usingCaptureDevice' in kwargs and 'maximumFaces' in kwargs):
            self._instance = self._detector.initWithDelegate_usingCaptureDevice_maximumFaces_(kwargs.get('delegate'), kwargs.get('usingCaptureDevice'), kwargs.get('maximumFaces'))
            self._delegate = kwargs.get('delegate')

        elif (len(kwargs) is 3 and 'delegate' in kwargs and 'usingCamera' in kwargs and 'maximumFaces' in kwargs):
            self._instance = self._detector.initWithDelegate_usingCamera_maximumFaces_(kwargs.get('delegate'), kwargs.get('usingCamera'), kwargs.get('maximumFaces'))
            self._delegate = kwargs.get('delegate')

        elif (len(kwargs) is 4 and 'delegate' in kwargs and 'usingCamera' in kwargs and 'maximumFaces' in kwargs and 'faceMode' in kwargs):
            self._instance = self._detector.initWithDelegate_usingCamera_maximumFaces_faceMode_(kwargs.get('delegate'), kwargs.get('usingCamera'), kwargs.get('maximumFaces'), kwargs.get('faceMode').value)
            self._delegate = kwargs.get('delegate')

        elif (len(kwargs) is 3 and 'delegate' in kwargs and 'usingFile' in kwargs and 'maximumFaces' in kwargs):
            self._instance = self._detector.initWithDelegate_usingFile_maximumFaces_(kwargs.get('delegate'), kwargs.get('usingFile'), kwargs.get('maximumFaces'))
            self._delegate = kwargs.get('delegate')

        elif (len(kwargs) is 4 and 'delegate' in kwargs and 'usingFile' in kwargs and 'maximumFaces' in kwargs and 'faceMode' in kwargs):
            self._instance = self._detector.initWithDelegate_usingFile_maximumFaces_faceMode_(kwargs.get('delegate'), kwargs.get('usingFile'), kwargs.get('maximumFaces'), kwargs.get('faceMode').value)
            self._delegate = kwargs.get('delegate')

        elif (len(kwargs) is 3 and 'delegate' in kwargs and 'discreteImages' in kwargs and 'maximumFaces' in kwargs):
            self._instance = self._detector.initWithDelegate_discreteImages_maximumFaces_(kwargs.get('delegate'), kwargs.get('discreteImages'), kwargs.get('maximumFaces'))
            self._delegate = kwargs.get('delegate')

        elif (len(kwargs) is 4 and 'delegate' in kwargs and 'discreteImages' in kwargs and 'maximumFaces' in kwargs and 'faceMode' in kwargs):
            self._instance = self._detector.initWithDelegate_discreteImages_maximumFaces_faceMode_(kwargs.get('delegate'), kwargs.get('discreteImages'), kwargs.get('maximumFaces'), kwargs.get('faceMode').value)
            self._delegate = kwargs.get('delegate')

        else:
            raise ValueError("Named arguments did not match a initializer.")


    def detectAllEmotions(self, bool):
        self._detector.setDetectAllEmotions_(bool)

    def detectAllExpressions(self, bool):
        self._detector.setDetectAllExpressions_(bool)

    def detectAllEmojis(self, bool):
        self._detector.setDetectEmojis_(bool)

    def detect(self, **kwargs):
        for name in kwargs:
            if hasattr(self._detector, name):
                (getattr(self._detector, "set" + name[0].upper() + name[1:] + "_")(kwargs.get(name)))
                print("Set classifier '%s' to %s" % (name, kwargs.get(name) is 1))

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

# This should be overridden by the client. Also provides supports more 'Pythonic' class function names and parameter types
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
        if "hasResults" in dir(self) and faces is not None:

            facesList = []
            for face in faces:
                facesList.append(_createDictFromAFDXFace(faces[face]))

            self.hasResults(detector, facesList)
        else:
            print(">> PyAFDXDetectorDelegate.hasResults (default implementation)")