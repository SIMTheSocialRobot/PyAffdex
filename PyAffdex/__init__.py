import platform, os

if platform.system() == "Darwin":
    AFFDEX_FRAMEWORK = "Affdex.framework"
    AFFDEX_LIB = "%s/%s" % (AFFDEX_FRAMEWORK, "Affdex")

    PATHS = [ "/Library/Frameworks", "/System/Library/Frameworks", "~/Library/Frameworks", "./" ]
    found = False

    for path in PATHS:

        print("Checking for %s in %s... " % (AFFDEX_FRAMEWORK, path), end='')
        searchpath = os.path.expanduser("%s/%s"%(path, AFFDEX_LIB))

        if os.path.isfile(searchpath):
            print("found")

            import objc
            objc.loadBundle("Affdex", globals(), bundle_path="%s/%s" % (path, AFFDEX_FRAMEWORK))
            found = True
            break
        else:
            print("not found")
    
    if not found:
        raise ImportError("Cound not find `Affdex.framework` in any of these locations: %s" % PATHS)

else:
    raise ImportError("Unsupported System: %s" % platform.system())
