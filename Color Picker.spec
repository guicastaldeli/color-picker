# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/casta/OneDrive/Desktop/vscode/color-picker/main/main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/casta/OneDrive/Desktop/vscode/color-picker/assets', 'assets'), ('C:/Users/casta/OneDrive/Desktop/vscode/color-picker/assets/img/ctm-cursor.png', 'assets/img/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
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
    name='Color Picker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\casta\\OneDrive\\Desktop\\vscode\\color-picker\\assets\\icon\\icon.ico'],
)
