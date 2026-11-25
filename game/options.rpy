#------------------AMINU-EDIT------------------#
# Ensuring the script doesn't break in Ren'Py 7
define config.script_version = (6, 99, 14)

# define config.language = "arabic"         # this is just for debugging, so keep it commented

# Granting necessary permissions on Android
define build.android_permissions = [
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.MANAGE_EXTERNAL_STORAGE"
]

define config.name = _("Doki Doki Literature Club! RE")
#----------------------------------------------#

define gui.show_name = False

#------------------AMINU-EDIT------------------#
define config.version = "1.1.1\nRE_Patch_v1.0.7"

define build.directory_name = "DDLCRE_1.0.7"
#----------------------------------------------#

define gui.about = _("")

#------------------AMINU-EDIT------------------#
define build.name = "DDLCRE"
#----------------------------------------------#

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

define config.main_menu_music = audio.t1

define config.enter_transition = Dissolve(.2)
define config.exit_transition = Dissolve(.2)

define config.after_load_transition = None

define config.end_game_transition = Dissolve(.5)

define config.window = "auto"

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

default preferences.text_cps = 50

default preferences.afm_time = 15

default preferences.music_volume = 0.75
default preferences.sfx_volume = 0.75

#------------------AMINU-EDIT------------------#
define config.save_directory = "DDLCr"

define config.window_icon = "gui2/window_icon.png"

# Android ports of Ren'Py games have this weird thing where they autoload you to where you left off immediately after reopening the game. The lines below are to disable that behavior
define config.autoreload = False
define config.save_on_mobile_background = False
# define config.quit_on_mobile_background = True
#----------------------------------------------#
define config.allow_skipping = True
define config.has_autosave = False
define config.autosave_on_quit = False
define config.autosave_slots = 0
define config.layers = [ 'master', 'transient', 'screens', 'overlay', 'front' ]
define config.image_cache_size = 64
define config.predict_statements = 50
define config.rollback_enabled = config.developer
define config.menu_clear_layers = ["front"]
define config.gl_test_image = "white"


init python:
    if len(renpy.loadsave.location.locations) > 1: del(renpy.loadsave.location.locations[1])
    renpy.game.preferences.pad_enabled = False
    def replace_text(s):
        s = s.replace('--', u'\u2014') 
        s = s.replace(' - ', u'\u2014') 
        return s
    config.replace_text = replace_text

    def game_menu_check():
        if quick_menu: renpy.call_in_new_context('_game_menu')

    config.game_menu_action = game_menu_check

    def force_integer_multiplier(width, height):
        if float(width) / float(height) < float(config.screen_width) / float(config.screen_height):
            return (width, float(width) / (float(config.screen_width) / float(config.screen_height)))
        else:
            return (float(height) * (float(config.screen_width) / float(config.screen_height)), height)

#------------------AMINU-EDIT------------------#
init python:

    build.archive("scripts", "all")
    build.archive("images", "all")
    build.archive("audio", "all")
    build.archive("fonts", "all")

    build.classify("game/gui/**.png", "images")
    build.classify("game/gui/**.jpg", "images")
    build.classify("game/gui/**.webp", "images")
    build.classify("game/gui/**.ico", "images")
    build.classify("game/images/**.png", "images")
    build.classify("game/images/**.jpg", "images")
    build.classify("game/images/**.webp", "images")
    build.classify("game/images/**.ico", "images")
    build.classify("game/hxppy thxughts.png", "images")

    build.classify("game/*.rpy", None)
    build.classify("game/*.rpyc", "scripts")
    build.classify("game/*.txt", "scripts")
    build.classify("game/*.chr", "scripts")

    build.classify("game/bgm/**.wav", "audio")
    build.classify("game/bgm/**.mp3", "audio")
    build.classify("game/bgm/**.ogg", "audio")
    build.classify("game/bgm/**.m4a", "audio")
    build.classify("game/sfx/**.wav", "audio")
    build.classify("game/sfx/**.mp3", "audio")
    build.classify("game/sfx/**.ogg", "audio")
    build.classify("game/sfx/**.m4a", "audio")
    build.classify("game/gui/**.wav", "audio")
    build.classify("game/gui/**.mp3", "audio")
    build.classify("game/gui/**.ogg", "audio")
    build.classify("game/gui/**.m4a", "audio")

    build.classify("game/gui/**.ttf", "fonts")
    build.classify("game/gui/**.otf", "fonts")

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('**.psd', None)
    build.classify('**.sublime-project', None)
    build.classify('**.sublime-workspace', None)
    build.classify('/music/*.*', None)
    build.classify('script-regex.txt', None)
    build.classify('/game/10', None)
    build.classify('/game/cache/*.*', None)

    build.documentation('*.html')
    build.documentation('*.txt')

    build.include_old_themes = False

define build.itch_project = "amineoussous/ddlcre"
#----------------------------------------------#

# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
