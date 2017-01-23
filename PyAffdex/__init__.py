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
