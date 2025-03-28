{
    "name": "Custom User Menu",
    "summary": "Removes all user menu items except 'Log Out'.",
    "version": "18.0",
    "author": "melon",
    "license": "LGPL-3",
    "depends": ["web"],
    'images': ['static/description/img2.png'],
    "assets": {
        "web.assets_backend": [
            "web/static/src/webclient/user_menu/user_menu.js",
            "custom_user_menu/static/src/js/custom_user_menu.js",
        ],
    },
    "installable": True,
    "application": False,
}
