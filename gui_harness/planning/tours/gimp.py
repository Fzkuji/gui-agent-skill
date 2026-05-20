"""GIMP pre-learning tour: walk through every top-level menu once."""

GIMP_TOUR = [
    {"state": "initial"},
    {"state": "file_menu", "setup": [("hotkey", "alt+f")]},
    {"state": "edit_menu", "setup": [("hotkey", "alt+e")]},
    {"state": "select_menu", "setup": [("hotkey", "alt+s")]},
    {"state": "view_menu", "setup": [("hotkey", "alt+v")]},
    {"state": "image_menu", "setup": [("hotkey", "alt+i")]},
    {"state": "layer_menu", "setup": [("hotkey", "alt+l")]},
    {"state": "colors_menu", "setup": [("hotkey", "alt+c")]},
    {"state": "tools_menu", "setup": [("hotkey", "alt+t")]},
    {"state": "filters_menu", "setup": [("hotkey", "alt+r")]},
    {"state": "windows_menu", "setup": [("hotkey", "alt+w")]},
    {"state": "help_menu", "setup": [("hotkey", "alt+h")]},
]
