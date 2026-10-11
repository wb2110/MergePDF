# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules


project_dir = Path(SPEC).resolve().parent
vendor_tree = project_dir / 'vendor'
datas = []
if vendor_tree.exists():
    datas.append((str(vendor_tree), 'vendor'))

hiddenimports = []
try:
    hiddenimports += collect_submodules('pypdf')
    datas += collect_data_files('pypdf')
except Exception:
    pass


a = Analysis(
    ['pdf_merge_tool.pyw'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    a.datas,
    [],
    name='PDFMergeToolLatest',
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
)
