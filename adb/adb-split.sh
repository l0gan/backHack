###############################################################
#
# Name: ADB Backup Splitter
# Author: dragomerlin
# License: GPL v3
#
###############################################################
#
# Description:
#
# This bash script utility generates an adb backup for each item
# on apps/ folder. That equals to generating an adb backup for
# each app.
#
# shared/0 and shared/1 (sdcards) are ignored, so that means that
# external data and OBB files, although should be backed up, may not
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
#
# As requested by SF user now ${SCRIPT_DIR}/ is used for abe.jar
#
###############################################################

##1 Test for needed applications.
# pax is not suitable instead of star because only can handle paths of up to 100 characters.
command -v tar >/dev/null 2>&1 || { echo "tar is required but is not installed. Aborting." >&2; exit 1; }
command -v star >/dev/null 2>&1 || { echo "star is required but is not installed. Aborting." >&2; exit 1; }
command -v mkdir >/dev/null 2>&1 || { echo "mkdir is required but is not installed. Aborting." >&2; exit 1; }
command -v cat >/dev/null 2>&1 || { echo "cat is required but is not installed. Aborting." >&2; exit 1; }
command -v grep >/dev/null 2>&1 || { echo "grep is required but is not installed. Aborting." >&2; exit 1; }
command -v rm >/dev/null 2>&1 || { echo "rm is required but is not installed. Aborting." >&2; exit 1; }
command -v ls >/dev/null 2>&1 || { echo "ls is required but is not installed. Aborting." >&2; exit 1; }

##2 Require java 7 or higher because of SYNC_FLUSH mode for the Deflater
# If you are going to use ab encryption you need also Java Cryptography Extension (JCE)
command -v java >/dev/null 2>&1 || { echo "java is not installed, 1.7 or higher required. Aborting." >&2; exit 1; }
JAVA_VER=$(java -version 2>&1 | sed 's/java version "\(.*\)\.\(.*\)\..*"/\1\2/; 1q')
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ "$JAVA_VER" -lt 17 ]; then
	echo "java 1.7 or higher is required. Aborting."
	exit 1
fi

###############################################################

# $1 = name with extension of the adb backup file which must be provided
# $2 = in case the backup is encrypted there should go the password
##3 Test if any argument is given, and if, test for files existence.

if [ -z $1 ]; then 
	echo "Usage: sh adb-split.sh backup.ab [password if needed]"
	echo "Resulting files go in app-ab folder"
	exit 1
fi
if [ ! -f $1 ]; then
	echo "File $1 doesn't exist on present dir. Aborting."
	exit 1
fi
### if [ ! -f abe.jar ]; then
if [ ! -f ${SCRIPT_DIR}/abe.jar ]; then
	echo "abe.jar doesn't exist on present dir. Aborting."
	exit 1
fi

# Backup file, abe and needed software exist
	##4 Convert the ab backup to tar archive, and detect if fails.
	# It can fail for 3 reasons: JCE is not present when necessary, password is incorrect or backup is corrupt.
	TARFILE=$1.tar
	echo "Extracting ab archive..."
	### java -jar abe.jar unpack $1 $TARFILE $2
	java -jar ${SCRIPT_DIR}/abe.jar unpack $1 $TARFILE $2
	if [ $? -ne 0 ]; then
		echo "Java failed to extract the ab archive. Aborting."
		exit 1
	fi
	echo "Done"
	##5 Extract tar archive with two possible folders: apps and shared
	echo "Extracting tar archive..."
	tar -xf $TARFILE
	# Sometimes tar may be corrupt even if ab is not. This may happen when making backups with -shared option,
	# when cancelling backup creation at the middle of the process or for other reasons.
	if [ $? -ne 0 ]; then
		echo "Tar extraction failed. Aborting."
		exit 1
	fi
	echo "Done"
	##6 Create list of all files
	tar -tf $TARFILE > list
	mkdir app-list
	mkdir app-tar
	mkdir app-ab
	##7 Check if apps folder exists. If not, exit.
	echo "Checking for apps folder..."
	if [ ! -d apps ]; then 
		echo "apps folder doesn't exist. Nothing to do. Aborting."
		exit 1
	fi
	echo "Done"
	##8 Check if apps folder is not empty. If so, exit.
	echo "Checking if apps folder is not empty..."
	if [ ! "$(ls -A apps)" ]; then
		echo "apps folder is empty. Nothing to do. Aborting."
		exit 1
	fi
	echo "Done"
	##9 For each folder in apps/ inside the tar archive, list it. There should be only folders.
	echo "Generating list of contents for each app..."
	for i in apps/* ; do cat list | grep $i/ > app-list/`basename $i`.list ; done
	echo "Done"
	##10 Create a tar archive for each app
	echo "Creating individual tar archives..."
	for i in apps/* ; do 
		star -c -f app-tar/`basename $i`.tar -no-dirslash list=app-list/`basename $i`.list > /dev/null 2>&1
		if [ $? -ne 0 ]; then
			echo "star compression failed at `basename $i`. Aborting."
			exit 1
		fi
	done
	echo "Done"
	echo "Creating individual adb backups..."
	##11 Convert tar to adb and encrypt with password (if any)
	for i in app-tar/* ; do 
		### java -jar abe.jar pack $i app-ab/`basename $i .tar`.ab $2 > /dev/null
		java -jar ${SCRIPT_DIR}/abe.jar pack $i app-ab/`basename $i .tar`.ab $2 > /dev/null
		if [ $? -ne 0 ]; then
			echo "java failed to compress at `basename $i`. Aborting."
			exit 1
		fi
	done
	echo "Done"
	##12 Check for apk existence, and if not warn and add to html file
	echo "Checking for apk existence..."
	echo "<HTML><BODY>" > apk-missing.html
	for i in app-list/* ; do
		grep .apk$ $i > /dev/null
		if [ $? -ne 0 ] ; then
			echo "Warning: apk not found in `basename $i .list`"
			echo "<A HREF=\"https://play.google.com/store/apps/details?id=`basename $i .list`\">" >> apk-missing.html
			echo "`basename $i .list`</A><BR>" >> apk-missing.html
		fi
	done
	echo "</BODY></HTML>" >> apk-missing.html
	grep google apk-missing.html > /dev/null && echo "There are one or more apk missing. Generating apk-missing.html"
	##13 Remove temporal files and apk-missing.html if has no links.
	echo "Cleaning temporal files..."
	grep google apk-missing.html > /dev/null || rm apk-missing.html
	rm $TARFILE
	rm -rf app-list
	rm -rf app-tar
	rm -rf apps
	rm -rf shared
	rm list
	echo "Done"
echo "Backup splitting complete."
