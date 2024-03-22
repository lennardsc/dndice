# Example build.spec file for PyInstaller

# Import the required module
import os

# Define the path to the main script
main_script = 'core/main.py'

# Additional files and directories to include
additional_files = [
    ('core', 'analysis.py'),
    ('core', 'charaktersheet.py'),
    ('core', 'roll.py'),
    ('core', 'storage.py'),
    ('core/assets', '*.png')  # Include all PNG files in the assets directory
]

# Specify the PyInstaller options
a = Analysis(
    [main_script],
    pathex=['.'],
    binaries=[],
    datas=additional_files,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=None)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=os.path.splitext(os.path.basename(main_script))[0],
          debug=False,
          strip=False,
          upx=True,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=os.path.splitext(os.path.basename(main_script))[0])
