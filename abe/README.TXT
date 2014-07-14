LAW WARNING
If you are working with password encrypted adb backups, you need to download these two files:
- local_policy.jar
- US_export_policy.jar
from http://www.oracle.com/technetwork/java/javase/downloads/jce-7-download-432124.html
and put them in the lib/security folder of all your Java SE 7 installations, for example:
--Windows:
C:\Program Files\Java\jdk1.7.0_60\jre\lib\security\
C:\Program Files\Java\jre7\lib\security\
C:\Program Files (x86)\Java\jdk1.7.0_60\jre\lib\security\
C:\Program Files (x86)\Java\jre7\lib\security\
--Linux:
/usr/local/jdk1.7/jre/lib/security/
--BSD:
/usr/lib/jvm/java-7-openjdk-*/jre/lib/security/
--OS X:
/Library/Java/JavaVirtualMachines/jdk1.7.0_60.jdk/Contents/Home/jre/lib/security/
Won't work if you supply them with the application, you must have them installed onto your system.

Author: Nikolay Elenkov
Packager: dragomerlin
Format: runnable jar file
IDE: Kepler Service Release 2 Build id: 20140224-0627
Java SE 1.7.0_60
Bouncy Castle version: bcprov-jdk15on-150

Application name: Android Backup Extractor
Original source code: https://github.com/nelenkov/android-backup-extractor
Website documentation: http://nelenkov.blogspot.com/2012/06/unpacking-android-backups.html
Full local backup infrastructure: https://android.googlesource.com/platform/frameworks/base/+/4a627c71ff53a4fca1f961f4b1dcc0461df18a06

Usage:
	info:	java -jar abe.jar info <backup.ab> [password]
	unpack:	java -jar abe.jar unpack <backup.ab> <backup.tar> [password]
	pack:	java -jar abe.jar pack <backup.tar> <backup.ab> [password]
	pack-kk:	java -jar abe.jar pack-kk <backup.tar> <backup.ab> [password]
	
*pack-kk is to create version 2 backups for android kitkat 4.4.3+.
If you don't specify a password the backup archive won't be encrypted but only compressed.
Option to create unencrypted and uncompressed backups it's not available.

Requirements for compilation:
- Bouncy Castle java release "JCE with provider and lightweight API"
  http://www.bouncycastle.org/latest_releases.html
- Oracle Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files 7
  http://www.oracle.com/technetwork/java/javase/downloads/jce-7-download-432124.html
- Java Standard Edition version 7
- IDE Eclipse (optional but recommended)

Description and scope:
- Android Backup Extractor is an application written in Java that can extract and create android adb backups. It doesn't edit directly.
- Android Backup Splitter is a bash script called adb-split.sh that creates individual adb backups for each app from the full one, so you can restore apps individually. Same encryption is preserved to them, if any. It also informs if any apk is missing.
- The adb backups (usually with .ab extension) can be password protected or not. If the device is encrypted this is mandatory and the password must be the same.
- The adb backups are extracted to tar format, and are created from the tar format as well.
- The files and folders inside the tar archive must be in some specific order, not necessarily alphabetical like tar does by default. Such order is listed in "Full local backup infrastructure". The easiest way is to repackage a tar archive from an already existing one; for example a subpart of an archive, and repackage it following the same order as files are listed in the original. If we don't have the original archive, we have to guess out the order.

Considerations:
- The tar archives may be extracted and created on filesystems that respect tar's content's permissions, although seems to work in any case.
- Directories inside tar archives must not contain trailing slashes. Since GNU tar doesn't have this option, the use of star or pax is necessary. For Ubuntu star is included.
- star is recommended instead of pax, which supports path length only up to 100 characters, so will fail in some cases. This usually happens with browsers history.
- Java 7 or higher is required because of SYNC_FLUSH mode for the Deflater.
- If the backup contains apk+data for an app, restore will work. If contains only the data, you must install the app first on the device and then restore. Installing the app later won't work.
- If you want a full backup use a nandroid backup with Clockworkmod or TWRP instead of ADB. Nandroid backup has the disadvantage that is not always 100% compatible between devices. ADB backup intends to be.
- Some apps include a policy where the apk is never backed up even if specified.
- Some applications or its data can't be restored on a different device, because may be set specific for the device's id or because are not compatible.
- Android debugging bridge is very slow: about 1 MBps if the backup is password encrypted, 1.6 MBps if not, so consider that backing and restoring may take a long time.
- When adding or removing files for an app you may need to edit _manifest so adb restore accepts the changes.
- ADB backups are not a replacement for a Nandroid backup. The whole /data partition is not backed up, only a part of it. Also, other partitions like /system, /preload, /cache, modem, RIL, efs, kernel or recovery are never backed up because are not user data. This is to prevent issues when restoring on a different device. It has also the biggest advantage that doesn't require root to operate, so is totally compatible with stock roms, locked bootloaders and device encryption.
- If you have the device encrypted with a password, you must use that particular one for backup creation and restore. You can't create a backup without password or a different one in that particular case, or if you try to restore will fail.
- star for cygwin for windows is attached (move it to C:\cygwin\bin\star.exe) since there is no package available. It can be compiled from the schily (ftp://ftp.berlios.de/pub/schily/).
- The best way to test if an adb backup has errors, is to convert it to tar and then check.


Example of quick backup editing:
Here is an example on how to make a custom adb backup from a complete one, for the game Grand Theft Auto III from Rockstar Games, installed on the Nexus 7.

1) Unpack the original adb backup:
$ java -jar abe.jar unpack nexus7.ab nexus7.tar <password>

2) Extract the contents of the tar archive. This may be done on a filesystem where the permissions of the files inside the tar are preserved, for example using linux, mac or bsd. Up to two folders may appear, apps and shared:
$ tar -xvf nexus7.tar

3) Make a list of all the contents of the original archive in the order they are archived:
$ tar -tf nexus7.tar > nexus7.list

4) Create a new list only with the files and folders you want, in proper order. For example for the GTA 3 (you can try savegames instead of all data):
$ cat nexus7.list | grep com.rockstar.gta3 > gta3.list

5) Create the new tar archive. The directories stored on tar mustn't contain trailing slashes, so I use star instead of tar. Pax works also if paths are up to 100 of length:
$ star -c -v -f gta3.tar -no-dirslash list=gta3.list
OR
$ cat gta3.list | pax -wd > gta3.tar

6) Create the adb backup from the tar archive. Password is optional except if the device is encrypted:
$ java -jar abe.jar pack gta3.tar gta3.ab <password>

Note: if the backup is not encrypted zlib can be used instead for both unpack and pack the ab archive:
- Quick unpacking:
$ dd if=nexus7.ab bs=24 skip=1 | openssl zlib -d > nexus7.tar
- Quick packing:
$ dd if=nexus7.ab bs=24 count=1 of=gta3.ab ; openssl zlib -in gta3.tar >> gta3.ab


Example of adb splitting to create an individual adb backup for each app:
Use ADB Backup Splitter (is a shell script). Works on Cygwin also:
sh adb-split.sh backup.ab [password if needed]
Resulting files go in app-ab folder.
Missing apk are listed in apk-missing.html

# ADB Backup Splitter:
#
# This bash script utility generates an adb backup for each item
# on apps/ folder. That equals to generating an adb backup for
# each app.
#
# shared/0 and shared/1 (sdcards) are ignored, so that means that
# external data and OBB files, although may be backed up, may not
# be restored. For doing so backup the folder Android of the sdcards.
# Creating a backup with -shared flag has know issues (corruption)
# so is not recommended. Future releases of this script may add
# the option to automatically detect things from sdcards inside
# the adb backup file.
#
# This script works on Cygwin also, and in general where star does. 
#
# There may be apps in the backup that don't include the apk. In that
# particular case, the data won't be restored, so the individual backup
# is generated for testing purposes only. Installing the apk afterwards won't work.
# There is generated an html file called apk-missing.html so you can open it and
# install all applications from Play Store on any of your devices.

Little changelog:
(Initial)
(6 June 2014)
- Changed "enabled" to "allowed" and "not enabled" to "not allowed" relating to strong AES encryption because some user complained
- JDK updated to 1.7.0_60, mixed mode
- Added support for android 4.4 encrypted backups
- Removed bcprov-jdk15on documentation
- Updated Bouncy Castle source (JCE with provider and lightweight API) from 1.48 to 1.50
- Updated adb-split.sh to add "${SCRIPT_DIR}/" before abe.jar
- Eclipse updated from 20130225-0426 to 20140224-0627
(15 June 2014)
- Updated program to create version 2 backups for android 4.4.3+.
(30 June 2014)
- Added backup version 3 for android L. No real code changes.