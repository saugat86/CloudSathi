# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for CloudSathi CLI."""

block_cipher = None

a = Analysis(
    ['cli/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'cli',
        'cli.commands',
        'cli.commands.aws',
        'cli.commands.azure',
        'cli.commands.recommend',
        'cli.utils',
        'cli.utils.api_client',
        'cli.utils.config',
        'cli.utils.display',
        'typer',
        'rich',
        'requests',
        'yaml',
        'pyyaml',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='cloudsathi',
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
)
