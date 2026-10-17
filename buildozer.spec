[app]

# (str) Title of your application
title = Zap do Condominio

# (str) Package name
package.name = zapcondominio

# (str) Package domain (needed for android/ios packaging)
package.domain = org.zap

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presumed orientation ("portrait", "landscape" or "all")
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
#android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (int) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip try to update the android sdk information
android.accept_sdk_license = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 =  false, 1 = true)
warn_on_root = 1
