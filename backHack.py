#! /bin/python
import os
import tarfile

def cls():
	os.system('cls' if os.name == 'nt' else 'clear')

appName = ''


mainMenu = {}
mainMenu['1']="Select App Package"
mainMenu['2']="Backup App"
mainMenu['3']="Extract App"
mainMenu['4']="Repack App"
mainMenu['5']="Restore App"
mainMenu['99']="Exit"
cls()
while True:
	options=mainMenu.keys()
	options.sort()
	for entry in options:
		print entry, mainMenu[entry]
			
	selection=raw_input("Please select an option:")
	if selection == "1":
		cls()
		appSelectMenu = {}
		appSelectMenu['1']="List Apps on Device"
		appSelectMenu['2']="Type in App Name"
		appSelectMenu['99']="Go Back"
		while True:
			options=appSelectMenu.keys()
			options.sort()
			for entry in options:
				print entry, appSelectMenu[entry]
					
			selection=raw_input("Please select an option:")
			if selection == "1":
				cls()
				print("1")
			elif selection == "2":
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
			os.system("adb.exe backup -f " + appName + ".ab " + appName if os.name == 'nt' else "./adb.exe backup -f " + appName + ".ab " + appName)
		else:
			print("You have not selected an app.  Please use option 1 to set your app.")
		
	elif selection == "3":
		cls()
		if appName:
			print("Extracting " + appName + ".")
			os.system("java -jar abe.jar unpack " + appName + ".ab " + appName + ".tar")
			tar = tarfile.open(appName + ".tar")
			tar.extractall()
			tar.pax_headers
			tar.close()
			cls()
			print("Extraction Complete.  Please review files under Apps.")
		else:
			print("You have not selected an app.  Please use option 1 to set your app.")
	elif selection == "4":
		cls()
		if appName:
			print("Repacking " + appName)
			tar = tarfile.open(appName + "-rest.tar", "w")
			for name in ["apps"]:
				tar.add(name)
			tar.close
			os.system("java -jar abe.jar pack " + appName + "-rest.tar " + appName + "-rest.ab")
			cls()
			print("Repacking complete.  You can now restore your backup file")
		else:
			print("You have not selected an app.  Please use option 1 to set your app.")
	elif selection == "5":
		cls()
		if appName:
			print("Restoring " + appName)
			os.system("adb.exe restore " + appName + "-rest.ab" if os.name == 'nt' else "./adb.exe restore " + appName + "-rest.ab")
		else:
			print("You have not selected an app.  Please use option 1 to set your app.")
		
	elif selection =="99":
		cls()
		break
	else:
		cls()
		print("Invalid Selection")
		
	

		
def main():
	cls()
	mainMenu
			
if __name__ == '__main__':
        main()
