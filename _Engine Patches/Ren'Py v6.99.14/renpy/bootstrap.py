# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function
import os.path
import sys
import subprocess
import io

FSENCODING = sys.getfilesystemencoding() or "utf-8"

# Sets the default encoding to the filesystem encoding.
old_stdout = sys.stdout
old_stderr = sys.stderr

reload(sys)
sys.setdefaultencoding(FSENCODING)  # @UndefinedVariable

sys.stdout = old_stdout
sys.stderr = old_stderr

import renpy.error


# Extra things used for distribution.


def extra_imports():
    import datetime; datetime
    import encodings.ascii; encodings.ascii
    import encodings.utf_8; encodings.utf_8
    import encodings.zlib_codec; encodings.zlib_codec
    import encodings.unicode_escape; encodings.unicode_escape
    import encodings.string_escape; encodings.string_escape
    import encodings.raw_unicode_escape; encodings.raw_unicode_escape
    import encodings.mbcs; encodings.mbcs
    import encodings.utf_16; encodings.utf_16
    import encodings.utf_16_be; encodings.utf_16_be
    import encodings.utf_16_le; encodings.utf_16_le
    import encodings.utf_32_be; encodings.utf_32_be
    import encodings.latin_1; encodings.latin_1
    import encodings.hex_codec; encodings.hex_codec
    import encodings.base64_codec; encodings.base64_codec
    import encodings.idna; encodings.idna
    import math; math
    import glob; glob
    import pickle; pickle
    import difflib; difflib
    import shutil; shutil
    import tarfile; tarfile
    import bz2; bz2  # @UnresolvedImport
    import webbrowser; webbrowser
    import posixpath; posixpath
    import ctypes; ctypes
    import ctypes.wintypes; ctypes.wintypes
    import argparse; argparse
    import compiler; compiler
    import textwrap; textwrap
    import copy; copy
    import urllib; urllib
    import urllib2; urllib2
    import codecs; codecs
    import rsa; rsa
    import decimal; decimal
    import plistlib; plistlib
    import _renpysteam; _renpysteam
    import compileall; compileall
    import cProfile; cProfile
    import pstats; pstats
    import _ssl; _ssl


class NullFile(io.IOBase):
    """
    This file raises an error on input, and IOError on read.
    """

    def write(self, s):
        return

    def read(self, length=None):
        raise IOError("Not implemented.")


def null_files():
    try:
        if sys.stderr.fileno() < 0:
            sys.stderr = NullFile()

        if sys.stdout.fileno() < 0:
            sys.stdout = NullFile()
    except:
        pass


null_files()


trace_file = None
trace_local = None


def trace_function(frame, event, arg):
    fn = os.path.basename(frame.f_code.co_filename)
    print(fn, frame.f_lineno, frame.f_code.co_name, event, file=trace_file)
    return trace_local


def enable_trace(level):
    global trace_file
    global trace_local

    trace_file = file("trace.txt", "w", 1)

    if level > 1:
        trace_local = trace_function
    else:
        trace_local = None

    sys.settrace(trace_function)


def mac_start(fn):
    os.system("open " + fn)

# This code fixes a bug in subprocess.Popen.__del__


def popen_del(self, *args, **kwargs):
    return


def bootstrap(renpy_base):

    global renpy  # W0602

    import renpy.log  # @UnusedImport

    # Remove a legacy environment setting.
    if os.environ.get(b"SDL_VIDEODRIVER", "") == "windib":
        del os.environ[b"SDL_VIDEODRIVER"]

    renpy_base = unicode(renpy_base, FSENCODING, "replace")

    # If environment.txt exists, load it into the os.environ dictionary.
    if os.path.exists(renpy_base + "/environment.txt"):
        evars = { }
        execfile(renpy_base + "/environment.txt", evars)
        for k, v in evars.iteritems():
            if k not in os.environ:
                os.environ[k] = str(v)

    # Also look for it in an alternate path (the path that contains the
    # .app file.), if on a mac.
    alt_path = os.path.abspath("renpy_base")
    if ".app" in alt_path:
        alt_path = alt_path[:alt_path.find(".app")+4]

        if os.path.exists(alt_path + "/environment.txt"):
            evars = { }
            execfile(alt_path + "/environment.txt", evars)
            for k, v in evars.iteritems():
                if k not in os.environ:
                    os.environ[k] = str(v)

    # Get a working name for the game.
    name = os.path.basename(sys.argv[0])

    if name.find(".") != -1:
        name = name[:name.find(".")]

    # Parse the arguments.
    import renpy.arguments
    args = renpy.arguments.bootstrap()

    if args.trace:
        enable_trace(args.trace)

    if args.basedir:
        basedir = os.path.abspath(args.basedir).decode(FSENCODING)
    else:
        basedir = renpy_base

    if not os.path.exists(basedir):
        sys.stderr.write("Base directory %r does not exist. Giving up.\n" % (basedir,))
        sys.exit(1)

    gamedirs = [ name ]
    game_name = name

    while game_name:
        prefix = game_name[0]
        game_name = game_name[1:]

        if prefix == ' ' or prefix == '_':
            gamedirs.append(game_name)

    gamedirs.extend([ 'game', 'data', 'launcher/game' ])

    for i in gamedirs:

        if i == "renpy":
            continue

        gamedir = basedir + "/" + i
        if os.path.isdir(gamedir):
            break
    else:
        gamedir = basedir

    sys.path.insert(0, basedir)

    if renpy.macintosh:
        # If we're on a mac, install our own os.start.
        os.startfile = mac_start

        # Are we starting from inside a mac app resources directory?
        if basedir.endswith("Contents/Resources/autorun"):
            renpy.macapp = True

    # Check that we have installed pygame properly. This also deals with
    # weird cases on Windows and Linux where we can't import modules. (On
    # windows ";" is a directory separator in PATH, so if it's in a parent
    # directory, we won't get the libraries in the PATH, and hence pygame
    # won't import.)
    try:
        import pygame_sdl2
        if not ("pygame" in sys.modules):
            pygame_sdl2.import_as_pygame()
    except:
        print("""\
Could not import pygame_sdl2. Please ensure that this program has been built
and unpacked properly. Also, make sure that the directories containing
this program do not contain : or ; in their names.

You may be using a system install of python. Please run {0}.sh,
{0}.exe, or {0}.app instead.
""".format(name), file=sys.stderr)

        raise

    # If we're not given a command, show the presplash.
    if args.command == "run" and not renpy.mobile:
        import renpy.display.presplash  # @Reimport
        renpy.display.presplash.start(basedir, gamedir)

    # Ditto for the Ren'Py module.
    try:
        import _renpy; _renpy
    except:
        print("""\
Could not import _renpy. Please ensure that this program has been built
and unpacked properly.

You may be using a system install of python. Please run {0}.sh,
{0}.exe, or {0}.app instead.
""".format(name), file=sys.stderr)
        raise

    # Load up all of Ren'Py, in the right order.

    import renpy  # @Reimport
    renpy.import_all()

    renpy.loader.init_importer()

    exit_status = None

    try:
        while exit_status is None:
            exit_status = 1

            try:
                renpy.game.args = args
                renpy.config.renpy_base = renpy_base
                renpy.config.basedir = basedir
                renpy.config.gamedir = gamedir
                renpy.config.args = [ ]

                #------------------AMINU-EDIT------------------#
                # We are now in the bootstrap file, meaning that anything we write here will trigger during startup, before anything else in your game's .rpy files
                if renpy.android:
                    # Requesting storage access in Android devices if needed
                    try:
                        if not renpy.check_permission("android.permission.WRITE_EXTERNAL_STORAGE"):
                            renpy.request_permission("android.permission.WRITE_EXTERNAL_STORAGE")
                    # For compatibility with Ren'Py 6, I make it so that the statement gets ignored if an exception occurs. That's because Ren'Py 6 doesn't recognize this statement
                    except:
                        pass
                    try:
                        if not renpy.check_permission("android.permission.MANAGE_EXTERNAL_STORAGE"):
                            renpy.request_permission("android.permission.MANAGE_EXTERNAL_STORAGE")
                    except:
                        pass

                    # I'll keep these next three lines outside the "try-except" block because we need them for the scoped storage system, a system which has nothing to do with the full access prompt that I'm trying to trigger
                    from jnius import autoclass, cast
                    Environment = autoclass('android.os.Environment')
                    File = autoclass("java.io.File")

                    # I first get the "root" directory (which is, in my case, "/storage/emulated/0")
                    android_root = Environment.getExternalStorageDirectory().getAbsolutePath()

                    # And to check whether or not the phone has full access, I attempt to create a file in root. If it fails, it will flag my "scoped_storage" variable as "True" and use the intended workaround
                    # This check is VERY IMPORTANT, because one of my players reported that the game in his Redmi phone attempted to create folders and succeeded, even though it shouldn't. And when Ren'Py started executing the .rpy files, it failed to create files. In other words, it was a bug in the scoped storage system that causes my workaround to be ignored. We have to make sure the game triggers the INTENTED workaround for Android 10+
                    nullfile0 = os.path.join(android_root, "null.txt")
                    scoped_storage = False
                    try:
                        open(nullfile0, "wb")
                    except:
                        scoped_storage = True

                    if not scoped_storage:
                        renpypath = os.path.join(android_root, "renpy")
                        if not os.path.exists(renpypath):
                            os.makedirs(renpypath)
                        # We can now remove the file because it served its purpose as a failsafe
                        try:
                            os.remove(nullfile0)
                        except:
                            pass

                    else:
                        # The following code is how to make Ren'Py prompt the user to "Allow Management of All Files" on Android
                        try:
                            Intent = autoclass('android.content.Intent')
                            Settings = autoclass('android.provider.Settings')
                            Uri = autoclass('android.net.Uri')
                            # I initially faced issues with this "PythonActivity" line. If you look up online or ask AI, they always tell you to call 'org.kivy.android.PythonActivity' but it won't work. 'org.renpy.android.PythonSDLActivity' is Ren'Py's version of that class and is the one that actually works
                            PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                            current_activity = PythonActivity.mActivity
                            # And now we make it so that when the game starts up, it would ALWAYS ask for full access. And if the user closes the prompt without granting the game full access, the prompt will immediately show up again. It'll never go away until full access is granted
                            if not Environment.isExternalStorageManager():
                                intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                                uri = Uri.fromParts("package", current_activity.getPackageName(), None)
                                intent.setData(uri)
                                current_activity.startActivity(intent)
                            # And this is to make sure the game freezes and NEVER do anything until full access is granted. This is to make sure the code doesn't attempt to use the scoped storage workaround that I have down here in the "if-else" block. I don't want the game to use scoped storage UNLESS it fails to get full access
                            while not Environment.isExternalStorageManager():
                                import time
                                time.sleep(1)
                        # If Google ever fucks up this nice little system somehow in the future, then we can just pass and let the scoped storage system get triggered
                        except:
                            pass

                        # Instead of getting the root, we get "Documents" because it's one of the directories we are allowed to use
                        android_docdir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS)
                        if not android_docdir():
                            android_docdir()
                        relative_path = ""
                        absolute_path = File(android_docdir, relative_path).getAbsolutePath()
                        if not os.path.exists(absolute_path):
                           os.makedirs(absolute_path)
                        renpypath = os.path.join(absolute_path, "renpy")
                        if not os.path.exists(renpypath):
                            os.makedirs(renpypath)

                    gamepath0 = os.path.join(renpypath, "ddlcr6")
                    if not os.path.exists(gamepath0):
                        os.makedirs(gamepath0)

                    # We can redefine the variables we set in "config.py" by giving each one the proper path we managed to get
                    renpy.config.gamepath = gamepath0
                    renpy.config.renpypath = renpypath
                    renpy.config.logdir = os.path.join(renpypath, "ddlcr6/logs")
                    renpy.config.logpath = renpy.config.logdir

                    #                    >>>>>>>>WARNING<<<<<<<<                        #
                    # Make sure you set the name of your game in "renpypath" and "logdir"
                    # Anyways, that's it! We're done relocating where Ren'Py stores its files on Android

                else:
                    renpy.config.logdir = basedir

                if not os.path.exists(renpy.config.logdir):
                    os.makedirs(renpy.config.logdir, 0o777)

                renpy.main.main()
                #----------------------------------------------#

                exit_status = 0

            except KeyboardInterrupt:
                raise

            except renpy.game.UtterRestartException:

                # On an UtterRestart, reload Ren'Py.
                renpy.reload_all()

                exit_status = None

            except renpy.game.QuitException as e:
                exit_status = e.status

                if e.relaunch:
                    if hasattr(sys, "renpy_executable"):
                        subprocess.Popen([sys.renpy_executable] + sys.argv[1:])
                    else:
                        subprocess.Popen([sys.executable, "-EO"] + sys.argv)

            except renpy.game.ParseErrorException:
                pass

            except Exception as e:
                renpy.error.report_exception(e)
                pass

        sys.exit(exit_status)

    finally:

        if "RENPY_SHUTDOWN_TRACE" in os.environ:
            enable_trace(int(os.environ["RENPY_SHUTDOWN_TRACE"]))

        renpy.display.im.cache.quit()

        if renpy.display.draw:
            renpy.display.draw.quit()

        # Prevent subprocess from throwing errors while trying to run it's
        # __del__ method during shutdown.
        subprocess.Popen.__del__ = popen_del
