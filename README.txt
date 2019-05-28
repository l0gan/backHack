
            /$$                           /$$       /$$   /$$                     /$$
            | $$                          | $$      | $$  | $$                    | $$
            | $$$$$$$   /$$$$$$   /$$$$$$$| $$   /$$| $$  | $$  /$$$$$$   /$$$$$$$| $$   /$$
            | $$__  $$ |____  $$ /$$_____/| $$  /$$/| $$$$$$$$ |____  $$ /$$_____/| $$  /$$/
            | $$  \ $$  /$$$$$$$| $$      | $$$$$$/ | $$__  $$  /$$$$$$$| $$      | $$$$$$/
            | $$  | $$ /$$__  $$| $$      | $$_  $$ | $$  | $$ /$$__  $$| $$      | $$_  $$
            | $$$$$$$/|  $$$$$$$|  $$$$$$$| $$ \  $$| $$  | $$|  $$$$$$$|  $$$$$$$| $$ \  $$
            |_______/  \_______/ \_______/|__/  \__/|__/  |__/ \_______/ \_______/|__/  \__/








backHack 3.1
v3.1: Download APK from device
v3.0: iOS Backup Parsing!
v2.5: Allow for easier app selection.
v2.0: Run straight from the command line!
v1.6: WINDOWS Support has been added!

by: Kirk Hayes(l0gan)
Twitter:  @kirkphayes

To run from command line (new in v2.0):

command:  python backHack.py --app com.app.android
            --app APPNAME, -a APPNAME (name of app to backup/analyze/restore)
            --listapps, -l (List apps installed on device)

iOS Mode (1):
          python backHack.py --ios --app appname (iOS mode. Specify app name and backHack will parse all backups from iTunes for which files may be of interest)

NEW: To download APK:
          python backHack.py --app appname --apk (will save the apk with the name of the app you enter)

To run interactively:

command:  python backHack.py


1 Select App Package
2 Backup and Extract App
3 Repack and Restore App
99 Exit
Please select an option:

SUBMENU 1:
1 List Apps on Device
2 Search for App
3 Type in App Name
99 Go Back
Please select an option:

(1): Have not tested encrypted backups yet....

** adb must be installed and set in your PATH.
*** If using a password on your backups, you must have Java JCE Unlimited Strength Jurisdiction Policy installed (http://www.oracle.com/technetwork/java/javase/downloads/jce-7-download-432124.html)
**** On Google Pixel you may HAVE to use encryption.

Use at your own risk!!
