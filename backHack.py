#! /bin/python
import os
import tarfile
from distutils.version import StrictVersion
import subprocess

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

appName = ''
andVer = ''


mainMenu = {}
mainMenu['1']="Select App Package"
mainMenu['2']="Backup and Extract App"
mainMenu['3']="Repack and Restore App"
mainMenu['99']="Exit"
cls()
while True:
    print """
     /$$                           /$$       /$$   /$$                     /$$
    | $$                          | $$      | $$  | $$                    | $$
    | $$$$$$$   /$$$$$$   /$$$$$$$| $$   /$$| $$  | $$  /$$$$$$   /$$$$$$$| $$   /$$
    | $$__  $$ |____  $$ /$$_____/| $$  /$$/| $$$$$$$$ |____  $$ /$$_____/| $$  /$$/
    | $$  \ $$  /$$$$$$$| $$      | $$$$$$/ | $$__  $$  /$$$$$$$| $$      | $$$$$$/
    | $$  | $$ /$$__  $$| $$      | $$_  $$ | $$  | $$ /$$__  $$| $$      | $$_  $$
    | $$$$$$$/|  $$$$$$$|  $$$$$$$| $$ \  $$| $$  | $$|  $$$$$$$|  $$$$$$$| $$ \  $$
    |_______/  \_______/ \_______/|__/  \__/|__/  |__/ \_______/ \_______/|__/  \__/






                                                                                    """
    options=mainMenu.keys()
    options.sort()
    for entry in options:
        print entry, mainMenu[entry]

    selection=raw_input("Please select an option:")
    if selection == "1":
        cls()
        appSelectMenu = {}
        appSelectMenu['1']="List Apps on Device"
        appSelectMenu['2']="Search for App"
        appSelectMenu['3']="Type in App Name"
        appSelectMenu['99']="Go Back"
        while True:
            print """
     /$$                           /$$       /$$   /$$                     /$$
    | $$                          | $$      | $$  | $$                    | $$
    | $$$$$$$   /$$$$$$   /$$$$$$$| $$   /$$| $$  | $$  /$$$$$$   /$$$$$$$| $$   /$$
    | $$__  $$ |____  $$ /$$_____/| $$  /$$/| $$$$$$$$ |____  $$ /$$_____/| $$  /$$/
    | $$  \ $$  /$$$$$$$| $$      | $$$$$$/ | $$__  $$  /$$$$$$$| $$      | $$$$$$/
    | $$  | $$ /$$__  $$| $$      | $$_  $$ | $$  | $$ /$$__  $$| $$      | $$_  $$
    | $$$$$$$/|  $$$$$$$|  $$$$$$$| $$ \  $$| $$  | $$|  $$$$$$$|  $$$$$$$| $$ \  $$
    |_______/  \_______/ \_______/|__/  \__/|__/  |__/ \_______/ \_______/|__/  \__/






                                                                                    """
            options=appSelectMenu.keys()
            options.sort()
            for entry in options:
                print entry, appSelectMenu[entry]

            selection=raw_input("Please select an option:")
            if selection == "1":
                cls()
                os.system("adb.exe shell pm list packages" if os.name == 'nt' else "adb shell pm list packages")
                print("Review the preceding list then use option 2 to type in the name of the package")
            elif selection == "2":
                cls()
                appSearch=raw_input("Type in part of the name to search for: ")
                print("")
                os.system('adb shell pm list packages | find /I "' + appSearch + '"' if os.name == 'nt' else "adb shell pm list packages |  grep -i " + appSearch + " | cut -d: -f2")
                print("")
                print("Copy the name of the app you want and use selection 3 to specify the app you are hacking")
            elif selection == "3":
                cls()
                appName=raw_input("Please type in the package name:")
                cls()
                print("Your chosen app:  " + appName)
                break
            elif selection == "99":
                cls()
                break
            else:
                cls()
                print("Invalid Selection")
    elif selection == "2":
        cls()
        if appName:
            print("Backing up " + appName)
            os.system("adb.exe backup -f " + appName + ".ab " + appName if os.name == 'nt' else "adb backup -f " + appName + ".ab " + appName)
            print("Extracting " + appName + ".")
            os.system("java -jar abe.jar unpack " + appName + ".ab " + appName + ".tar")
            tar = tarfile.open(appName + ".tar")
            tar.extractall()
            tarList = open("fileList.txt", 'w')
            for member in tar.getmembers():
                tarList.write(str(member.name) + '\n')
            tarList.close()
            tar.close()
            print("Extraction Complete.  Please review files under Apps.")
        else:
            print("You have not selected an app.  Please use option 1 to set your app.")

    elif selection == "3":
        cls()
        #andVerFile = open("andVerFile.txt", "w")
        andVerNum = subprocess.check_output("adb.exe shell getprop ro.build.version.release" if os.name == 'nt' else "adb shell getprop ro.build.version.release", shell=True)
        andVerNum = str(andVerNum)[:5]
        #andVerFile.close()
        #andVerFile = open("andVerFile.txt", "r")
        #andVerNum = andVerFile.read()
        #andVerFile.close()
        if StrictVersion(str(andVerNum)) > StrictVersion("4.4.2"):
            andVer = "pack-kk"
        else:
            andVer = "pack"
        if appName:
            print("Repacking " + appName)
            tar = tarfile.open(appName + "-rest.tar", "w", format=tarfile.USTAR_FORMAT)
            retar = open("fileList.txt", 'r')
            for name in retar.readlines():
                tar.add(name.strip('\n'))
            retar.close()
            tar.close()
            os.system("java -jar abe.jar "+ andVer + " " + appName + "-rest.tar " + appName + "-rest.ab")
            cls()
            print("Repacking complete.")
            print("Restoring " + appName)
            os.system("adb.exe restore " + appName + "-rest.ab" if os.name == 'nt' else "adb restore " + appName + "-rest.ab")
        else:
            print("You have not selected an app.  Please use option 1 to set your app.")
    elif selection =="99":
        cls()
        print("Cleaning Up")
        os.system("echo This is only supported on Linux or Cygwin currently" if os.name == 'nt' else "rm fileList.txt "+ appName + ".* " + appName + "-* " if appName != '' else "echo Nothing to remove")
        os.system("echo This is only supported on Linux or Cygwin currently" if os.name == 'nt' else "rm -rf apps")
        break
    else:
        cls()
        print("Invalid Selection")

def main():
    cls()
    mainMenu

if __name__ == '__main__':
        main()
