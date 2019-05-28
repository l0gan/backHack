#! /usr/bin/python
import os
from os.path import expanduser
import tarfile
from distutils.version import LooseVersion
import subprocess
from subprocess import check_output
from argparse import ArgumentParser
import platform
import time
from datetime import datetime
import pytz
import glob
import sqlite3


parser = ArgumentParser(description='Hacking some Android apps! Use backHack to perform Android Application File System Analysis on non-rooted devices. Running without arguments will run in interactive mode.')
parser.add_argument('--app', '-a', help='Application name (e.g. com.niantic.pokemongo)')
parser.add_argument('--listapps', '-l', action="store_true", help='List apps on device')
parser.add_argument('--backup', '-b', action="store_true", help='Backup app')
parser.add_argument('--restore', '-r', action="store_true", help='Restore app')
parser.add_argument('--ios', '-i', action="store_true", help='iOS mode. Uses a iTunes backup file to extract data from the specified app.')
parser.add_argument('--apk', action="store_true", help='Download App APK')

ver = "3.1"

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    print("""
/$$                           /$$       /$$   /$$                     /$$
| $$                          | $$      | $$  | $$                    | $$
| $$$$$$$   /$$$$$$   /$$$$$$$| $$   /$$| $$  | $$  /$$$$$$   /$$$$$$$| $$   /$$
| $$__  $$ |____  $$ /$$_____/| $$  /$$/| $$$$$$$$ |____  $$ /$$_____/| $$  /$$/
| $$  \ $$  /$$$$$$$| $$      | $$$$$$/ | $$__  $$  /$$$$$$$| $$      | $$$$$$/
| $$  | $$ /$$__  $$| $$      | $$_  $$ | $$  | $$ /$$__  $$| $$      | $$_  $$
| $$$$$$$/|  $$$$$$$|  $$$$$$$| $$ \  $$| $$  | $$|  $$$$$$$|  $$$$$$$| $$ \  $$
|_______/  \_______/ \_______/|__/  \__/|__/  |__/ \_______/ \_______/|__/  \__/

                                                                    Version: """ + ver + """





""")

def mainmenu():
    appName = ''
    andVer = ''
    mainMenu = {}
    mainMenu['1']="Select App Package"
    mainMenu['2']="Backup and Extract App"
    mainMenu['3']="Repack and Restore App"
    mainMenu['99']="Exit"
    cls()
    while True:
        logo()
        options=mainMenu.keys()
        options.sort()
        for entry in options:
            print(entry, mainMenu[entry])

        selection=raw_input("[*]  Please select an option:  ")
        if selection == "1":
            cls()
            appSelectMenu = {}
            appSelectMenu['1']="List Apps on Device"
            appSelectMenu['2']="Search for App"
            appSelectMenu['3']="Type in App Name"
            appSelectMenu['99']="Go Back"
            while True:
                logo()
                options=appSelectMenu.keys()
                options.sort()
                for entry in options:
                    print(entry, appSelectMenu[entry])

                selection=raw_input("[*]  Please select an option:  ")
                if selection == "1":
                    cls()
                    packs = listApps()
                    appnumber = raw_input("[*] Enter number corresponding with the app you want to use: ")
                    appName = packs[int(appnumber)]
                    cls()
                    print("[!] Your chosen app:  " + appName)
                    break
                elif selection == "2":
                    cls()
                    appSearch=raw_input("[*]  Type in part of the name to search for: ")
                    print("")
                    packs = check_output('adb shell pm list packages | find /I "' + appSearch + '"' if os.name == 'nt' else "adb shell pm list packages |  grep -i " + appSearch + " | cut -d: -f2", shell=True)
                    packs = packs.split(":")
                    packs = [i.split('\r\n', 1)[0] for i in packs]
                    i = 0
                    for pack in packs:
                        print str(i) + ": " + pack
                        i = i+1
                    print("")
                    appnumber = raw_input("[*] Enter number corresponding with the app you want to use: ")
                    appName = packs[int(appnumber)]
                    appName = appName.strip("\n")
                    cls()
                    print("[!] Your chosen app:  " + appName)
                    break
                elif selection == "3":
                    cls()
                    appName=raw_input("[*]  Please type in the package name:")
                    cls()
                    print("[!] Your chosen app:  " + appName)
                    break
                elif selection == "99":
                    cls()
                    break
                else:
                    cls()
                    print("[-] Invalid Selection")
        elif selection == "2":
            cls()
            if appName:
                backupApp(appName)
            else:
                print("[-] You have not selected an app.  Please use option 1 to set your app.")

        elif selection == "3":
            cls()
            andVer = andVerCheck()
            if appName:
                restoreApp(andVer, appName)
            else:
                print("[-] You have not selected an app.  Please use option 1 to set your app.")
        elif selection =="99":
            cls()
            cleanup(appName)
            break
        else:
            cls()
            print("[-] Invalid Selection")

def apkDownloader(appName):
    apkLoc = check_output('adb shell pm list packages -f | find /I "' + appName + '"' if os.name == 'nt' else "adb shell pm list packages -f |  grep -i " + appName , shell=True)
    apkLoc = (apkLoc.split(':')[1]).split('=')[0]
    os.system('adb pull ' + apkLoc + ' ' + appName + '.apk') 

def andVerCheck():
    andVerNum = subprocess.check_output("adb.exe shell getprop ro.build.version.release" if os.name == 'nt' else "adb shell getprop ro.build.version.release", shell=True)
    andVerNum = str(andVerNum)[:5]
    if LooseVersion(str(andVerNum)) > LooseVersion("4.4.2"):
        andVer = "pack-kk"
    else:
        andVer = "pack"
    return andVer

def restoreApp(andVer, appName):
    print("[*] Repacking " + appName)
    tar = tarfile.open(appName + "-rest.tar", "w", format=tarfile.USTAR_FORMAT)
    retar = open("fileList.txt", 'r')
    for name in retar.readlines():
        tar.add(name.strip('\n'))
    retar.close()
    tar.close()
    os.system("java -jar abe.jar "+ andVer + " " + appName + "-rest.tar " + appName + "-rest.ab")
    cls()
    print("[*] Repacking complete.")
    print("[*] Restoring " + appName)
    os.system("adb.exe restore " + appName + "-rest.ab" if os.name == 'nt' else "adb restore " + appName + "-rest.ab")

def cleanup(appName):
    print("[*] Cleaning Up")
    os.system("del fileList.txt "+ appName + ".* " + appName + "-* " if os.name == 'nt' else "rm fileList.txt "+ appName + ".* " + appName + "-* " if appName != '' else "echo Nothing to remove")
    os.system("rd /S /Q apps" if os.name == 'nt' else "rm -rf apps")

def listApps():
    packs = check_output("adb.exe shell pm list packages" if os.name == 'nt' else "adb shell pm list packages", shell=True)
    #packs = os.popen("adb.exe shell pm list packages" if os.name == 'nt' else "adb shell pm list packages").read()
    packs = packs.split(":")
    packs = [i.split('\r\n', 1)[0] for i in packs]
    i = 0
    for pack in packs:
        print str(i) + ": " + pack
        i = i+1
    return packs


def backupApp(appName):
    print("[*] Backing up " + appName)
    os.system("adb.exe backup -f " + appName + ".ab " + appName if os.name == 'nt' else "adb backup -f " + appName + ".ab " + appName)
    print("[*] Extracting " + appName + ".")
    try:
        os.system("java -jar abe.jar unpack " + appName + ".ab " + appName + ".tar")
        tar = tarfile.open(appName + ".tar")
        tar.extractall()
        tarList = open("fileList.txt", 'w')
        for member in tar.getmembers():
            tarList.write(str(member.name) + '\n')
            tarList.close()
        statinfo = os.stat('fileList.txt')
        if statinfo.st_size == 0:
            print("[-] Extraction failed. Did the backup complete properly? Try again but use a password to encrypt.")
        else:
            print("[*] Extraction Complete.  Please review files under apps folder.")
    except Exception as e:
        print("[-] An error occured. Are you encrpyting? ")
        print e

def main():
    cls()
    mainmenu()

def iosBackup(itunesdir):
    try:
        newest = max(glob.iglob(itunesdir + '/*'), key=os.path.getctime)
        conn = sqlite3.connect(newest + '/Manifest.db')
        c = conn.cursor()
        print "[+] Files accessible: (" + newest + ")"
        print "+" + "-" * 120 + "+"
        print "|  " + "GUID".ljust(50) + "|  " + "LocalDB".ljust(65) + "|"
        print "+" + "-" * 120 + "+"
        sqlcmd = "SELECT DISTINCT fileID, domain, relativePath  from Files WHERE domain LIKE '%" + args.app + "%';"
        #sqlcmd = "SELECT * from Files"
        for row in c.execute(sqlcmd):
            if "." in row[2]:
                filename = newest + "/" + row[0][:2]
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(filename):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                        if total_size > 65:
                            print "|",row[0].ljust(50), "|", row[2].ljust(65), "|"
        print "+" + "-" * 120 + "+"
    except ValueError:
        print "[-] No Backups found. Have you performed a backup with iTunes?"

if __name__ == '__main__':
    args = parser.parse_args()
    parser.set_defaults(listapps=False)
    parser.set_defaults(backup=False)
    parser.set_defaults(restore=False)
    osType =  platform.system()
    home = expanduser("~")
    if args.ios:
        cls()
        logo()
        print "[*] Let's try some iOS fun...."
        macDir = home + '/Library/Application Support/MobileSync/Backup/'
        winDir = home + r'\AppData\Roaming\Apple Computer\MobileSync\Backup'
        if osType == "Darwin":
            print "[*] Running on a Mac huh?"
            print "[*] Looking for backup data at: " + macDir
            itunesdir = macDir
            iosBackup(itunesdir)
        elif osType == "Windows":
            print "[*] Ugh, Windows huh?"
            print "[*] Looking for backup data at: " + winDir
            itunesdir = winDir
            iosBackup(itunesdir)
        elif osType == "Linux":
            print "[-] iOS on Linux? Are you nuts? iTunes doesn't work on Linux! Go grab a Mac or a Windows system..."
        else:
            print "[-] I don't know what this is: " + osType
    elif args.app:
        if args.backup:
            backupApp(args.app)
        elif args.restore:
            andVer = andVerCheck()
            restoreApp(andVer, args.app)
            cleanup = raw_input("[*]  Would you like to cleanup? WARNING: This will DELETE all folders associated with the application backup/restore process. (y/n)")
            if cleanup == "y":
                cleanup(args.app)
            else:
                print("[-] Leaving artifacts as they are. Manually cleanup if you need.")
        elif args.apk:
            apkDownloader(args.app)
        else:
            print "[-] Missing backup or restore argument."
    elif args.listapps == True:
        listApps()
    else:
        main()
