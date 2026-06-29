[app]

# ---------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------

title = AKM Finance Manager

package.name = akmfinancemanager
package.domain = com.elitefantasy

version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/core/version.py

source.dir = .

# ---------------------------------------------------------------------
# Source files
# ---------------------------------------------------------------------

source.include_exts = py,kv,png,jpg,jpeg,ttf,codepoints,json

source.exclude_dirs = .git,.github,.venv,__pycache__,.kivy,bin,build,logs

source.exclude_patterns = *.db,*.db-journal,*.log,desktop.ini,.DS_Store

# ---------------------------------------------------------------------
# Requirements
# ---------------------------------------------------------------------

requirements = python3,kivy

# ---------------------------------------------------------------------
# App configuration
# ---------------------------------------------------------------------

orientation = portrait

fullscreen = 0

# ---------------------------------------------------------------------
# Android
# ---------------------------------------------------------------------

android.api = 34

android.minapi = 24

android.ndk = 28c

android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

android.release_artifact = apk

android.debug_artifact = apk

# We'll add permissions later when SAF is implemented.
# android.permissions =

# ---------------------------------------------------------------------
# Icon
# ---------------------------------------------------------------------

icon.filename = assets/icon.png

# ---------------------------------------------------------------------
# Splash
# ---------------------------------------------------------------------

presplash.filename = assets/presplash.png

# ---------------------------------------------------------------------
# Buildozer
# ---------------------------------------------------------------------

[buildozer]

log_level = 2

warn_on_root = 1