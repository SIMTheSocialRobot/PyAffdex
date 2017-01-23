import platform, os

if platform.system() == "Darwin":
    AFFDEX_FRAMEWORK = "Affdex.framework"
    AFFDEX_LIB = "%s/%s" % (AFFDEX_FRAMEWORK, "Affdex")

    PATHS = [ "/Library/Frameworks", "/System/Library/Frameworks", "~/Library/Frameworks", "./" ]
    found = False

    for path in PATHS:

        print("Checking for %s in %s... " % (AFFDEX_FRAMEWORK, path), end='')
        libpath = os.path.expanduser("%s/%s"%(path, AFFDEX_LIB))
        fwpath = os.path.expanduser("%s/%s"%(path, AFFDEX_FRAMEWORK))

        if os.path.isfile(libpath):
            print("found")

            import objc
            __bundle__ = objc.initFrameworkWrapper(\
                "Affdex", \
                frameworkIdentifier = "com.affectiva.Affdex", \
                frameworkPath = objc.pathForFramework(fwpath), \
                globals = globals())

            found = True

            break
        else:
            print("not found")
    
    if not found:
        raise ImportError("Cound not find `Affdex.framework` in any of these locations: %s" % PATHS)

else:
    raise ImportError("Unsupported System: %s" % platform.system())

# Really want to break these classes into seperate files, but then the types loaded from objc become hidden?

# ---------
# Delegates (Unique to Objective-C)
# ---------
class PyAFDXDetectorDelegate(NSObject):
    def init(self):
        return self

    def detectorDidFinishProcessing_(self, detector):
        print("detectorDidFinishProcessing");

    def detector_didStartDetectingFace_(self, detector, face):
        print("didStartDetectingFace")
        print(detector)
        print(face)

    def detector_didStopDetectingFace_(self, detector, face):
        print("didStopDetectingFace")
        print(detector)
        print(face)

    def detector_hasResults_forImage_atTime_(self, detector, results, image, time):
        print("hasResults")
        print(detector)
        print(results)
        print(image)
        print(time)

# -------
# Classes
# -------
class PyAFDXDetector:
    def __init__(self, *args, **kwargs):
        if (len(args) > 0):
            raise ValueError("All arguments must be named.")

        self._detector = AFDXDetector.alloc().init()

        #ObjC provides 7 different init methods
        if (len(kwargs) is 4 and 'discreteImages' in kwargs and 'maximumFaces' in kwargs and 'faceMode' in kwargs and 'delegate' in kwargs):
            self._instance = self._detector.initWithDelegate_discreteImages_maximumFaces_faceMode_(kwargs.get('delegate'), kwargs.get('discreteImages'), kwargs.get('maximumFaces'), kwargs.get('faceMode'))
            self._instance.setDelegate_(kwargs.get('delegate'))

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