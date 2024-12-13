# -*- mode: python ; coding: utf-8 -*-

# 自动收集 scraper 包的所有子模块
hiddenimports = [
                    'scraper.__init__',
                    'scraper.progress',
                    'scraper.scroller',
                    'scraper.tweet',
                    'scraper.twitter_scraper'
]

a = Analysis(
    ['scraper/__main__.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ts',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,
)