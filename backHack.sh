#! /bin/bash
mkdir $1
cd $1
../adb/adb backup -f $1.ab $1
java -jar ../abe/abe.jar unpack $1.ab $1.tar
tar -xvf $1.tar
tar -tf $1.tar > fileList.txt
read -p "Press Enter after all changes are completed and you are ready to restore your app"
cat fileList.txt | pax -wd > new.tar
java -jar ../abe/abe.jar pack new.tar new.ab
../adb/adb restore new.ab
echo "Restore complete! We will clean up now..."
cd ..
rm -rf $1
