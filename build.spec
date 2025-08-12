# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    [ 'run.py'],
    pathex=[],
    binaries=[],
    datas=[ ("bookkeeper/desktop/templates/*" , "bookkeeper/desktop/templates"),  ("bookkeeper/desktop/static/*" , "bookkeeper/desktop/static")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Bookkeeper',
    version="version.txt",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    version="version.txt",
    strip=False,
    upx=False,
    name='Bookkeeper',
)

app = BUNDLE(
    exe,
    name='Bookkeeper.app',
)