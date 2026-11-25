##-------This file is a MESS! I don't even know what everything does-------##
##---------------It's all barely put together with cheap tape--------------##
##-----------I still couldn't get the text to render the way I want it-----##
##-----If anyone knows how to fix this thing, I'd appreciate some help-----##

translate arabic python:
    config.language = "arabic"
    config.rtl = True

    # gui.text_size = 21                 # Adjust the size of the text
    # gui.text_width = None                # Set the width of the text display area (try 920)
    # gui.text_height = None
    gui.text_xpos = 1020                # Set the X-position for the text display
    gui.text_ypos = 50                  # Set the Y-position for the text display
    gui.text_xalign = 1.0
    gui.button_text_xalign = 1.0
    gui.prompt_text_xalign = 1.0
    # gui.navigation_xpos = 240

    gui.name_xalign = 0.5               # Center-align the name
    gui.button_text_xalign = 1.0
    # gui.main_menu_text_xalign = 1.0
    gui.history_name_xalign = 0.0
    gui.history_text_xalign = 1.0
    gui.nvl_name_xalign = 0.0
    gui.nvl_text_xalign = 1.0
    gui.nvl_thought_xalign = 1.0
    gui.nvl_button_xalign = 1.0

    gui.help_label_text_xalign = 0.0

    gui.name_xpos = 950                # Set the X-position for the name display (try 950)
    # gui.name_ypos = -3                  # Set the Y-position for the name display
    gui.history_name_xpos = 763
    gui.history_text_xpos = 748
    gui.nvl_name_xpos = 850
    gui.nvl_text_xpos = 830
    gui.nvl_thought_xpos = 1040
    gui.nvl_button_xpos = 830




translate arabic style normal:
    line_leading 6
    line_overlap_split 2
    layout "greedy"
translate arabic style say_dialogue:
    line_leading 5
translate arabic style splash_text:
    line_leading 5
translate arabic style edited:
    line_leading 5
translate arabic style input:
    line_leading 5
translate arabic style input_prompt:
    line_leading 5
translate arabic style startup_input:
    line_leading 5
translate arabic style say_label:
    yalign 0.7




translate arabic style game_menu_label:
    xalign 1.0
    xoffset -50
# translate arabic style navigation_vbox:
    # xanchor 1.0
translate arabic style return_button:
    xanchor 1.0
translate arabic style radio_button:
    xalign 1.0
translate arabic style radio_label:
    xalign 1.0
translate arabic style check_button:
    xalign 1.0
translate arabic style check_label:
    xalign 1.0
translate arabic style slider_label:
    xpos 350
    xalign 1.0
translate arabic style help_hbox:
    box_reverse True
    xalign 1.0
    spacing 20
translate arabic style help_label_text:
    xalign 0.0
translate arabic style mute_all_button:
    xalign 0.0
