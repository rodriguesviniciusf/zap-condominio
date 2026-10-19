[app]
title = Zap do Condominio
package.name = zapcondominio
package.domain = org.zap
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,wav
source.exclude_dirs = tests,.github,.git,__pycache__
source.exclude_patterns = build_events.py,calendar_content.py,build.log
version = 0.5.0
requirements = python3,kivy==2.3.0,pyjnius
icon.filename = assets/icone.png
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,VIBRATE
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
