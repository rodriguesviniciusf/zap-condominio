[app]
title = Zap do Condominio
package.name = zapcondominio
package.domain = org.zap
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_dirs = tests,.github,.git,__pycache__
version = 0.2.0
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.debug_artifact = apk
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
