# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Jumper Frog.

Build with:
    pyinstaller jumper_frog.spec
"""

import os

ROOT = os.path.abspath(".")

a = Analysis(
    ["src/main.py"],
    pathex=[ROOT],
    datas=[
        ("assets/background", "assets/background"),
        ("assets/frogs", "assets/frogs"),
        ("assets/icons", "assets/icons"),
    ],
    hiddenimports=[
        "src",
        "src.game",
        "src.core",
        "src.core.settings",
        "src.core.game_loop",
        "src.core.renderer",
        "src.core.input_handler",
        "src.core.collision",
        "src.core.progress",
        "src.core.hot_reloader",
        "src.entities",
        "src.entities.entity",
        "src.entities.frog",
        "src.entities.wall",
        "src.entities.moving_platform",
        "src.entities.trophy",
        "src.scenes",
        "src.scenes.scene",
        "src.scenes.menu_scene",
        "src.scenes.commands_scene",
        "src.scenes.levels_scene",
        "src.scenes.game_scene",
        "src.levels",
        "src.levels.level",
        "src.levels.level_registry",
        "src.levels.level_1",
        "src.levels.level_2",
        "src.levels.level_3",
        "src.manager",
        "src.manager.scene_manager",
        "src.ui",
        "src.ui.button",
        "src.ui.back_button",
        "src.ui.textbox",
        "src.ui.pause_overlay",
        "src.ui.victory_overlay",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="JumperFrog",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="assets/icons/frog.ico",
)
