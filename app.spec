# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('data', 'data')]
datas += collect_data_files('gradio_client')
datas += collect_data_files('gradio')
datas += collect_data_files('safehttpx')
datas += collect_data_files('groovy')
datas += collect_data_files('modelscope_studio')

a = Analysis(
    ['app.py', 'gradio_ui\gr_dps.py', 'gradio_ui\gr_equipment.py', 'gradio_ui\gr_glyph.py', 'gradio_ui\gr_main.py', 'gradio_ui\gr_others.py', 'gradio_ui\gr_rune.py', 'gradio_ui\gr_skin.py', 'gradio_ui\gr_surplus_level.py', 'gradio_ui\gr_warning_check.py', 'gradio_ui\save_load.py', 'src\dps_func.py', 'src\equipment_func.py', 'src\glyph_func.py', 'src\main_calculate.py', 'src\others_func.py', 'src\percent_calculate.py', 'src\player_base_func.py', 'src\\rune_func.py', 'src\skin_func.py', 'src\surplus_func.py', 'src\\tool_func.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    module_collection_mode={'gradio': 'py', 'modelscope_studio': 'py'}
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
