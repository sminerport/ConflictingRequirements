import sqlite3
import re
import inspect
from plantuml import PlantUML
from os.path import abspath
from PIL import Image
import os

class Database():
    
    def createConnection(self):
        try:
            sqliteConnection = sqlite3.connect('SoftwareReq.db')
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
        
    def createTables(self):
        try:
            sqliteConnection = sqlite3.connect('SoftwareReq.db')
            cursor = sqliteConnection.cursor()
            sqlite_create_table_query = """CREATE TABLE if not exists USERS
                                                            (
                                                                id INTEGER PRIMARY KEY,
                                                                email text,
                                                                pin int
                                                            )"""
            cursor.execute(sqlite_create_table_query)
            sqlite_create_table_query = """CREATE TABLE if not exists SPECIFICATIONS
                                                            (
                                                                userID int NOT NULL,
                                                                vTabs INT,
                                                                hTabs INT,
                                                                menuFile INT,
                                                                menuRepository INT,
                                                                menuCommand INT,
                                                                menuTools INT,
                                                                menuView INT,
                                                                menuNavigate INT,
                                                                menuPlugins INT,
                                                                menuHelp INT,
                                                                menuItemCount INT,
                                                                toolbar INT,
                                                                CONSTRAINT PK_Specifications PRIMARY KEY (userID),
                                                                CONSTRAINT FK_Specifications_Users FOREIGN KEY (userID)
                                                                REFERENCES USERS (id)
                                                                ON DELETE CASCADE
                                                                ON UPDATE CASCADE
                                                            )   
                                                            """;                                                                        
            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                
    def userAvailable(self, email):
        try:
            sqliteConnection = sqlite3.connect("SoftwareReq.db")
            sqlite_select_query = "SELECT count(*) FROM users WHERE email =?"
            cursor = sqliteConnection.cursor()
            cursor.execute(sqlite_select_query, (email.lower(),))
            data=cursor.fetchone()[0]
            if data==0:
                return True
            else:
                return False
            cursor.close()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                
    def insertUserAndPin(self, email, pin):
        try:
            sqliteConnection = sqlite3.connect("SoftwareReq.db")
            sqlite_insert_statement = "INSERT INTO users (email, pin) VALUES (?, ?)"
            cursor = sqliteConnection.cursor()
            cursor.execute(sqlite_insert_statement, (email.lower(), pin))
            sqliteConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Error while inserting into user table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                
    def insertSpecification(self, email, software):
        try:
            sqliteConnection = sqlite3.connect("SoftwareReq.db")
            sqlite_select_statement = "SELECT id FROM users WHERE email =?"
            cursor = sqliteConnection.cursor()
            cursor.execute(sqlite_select_statement, (email.lower(),))
            result = cursor.fetchone()
            result = result[0]
            sqlite_insert_statement = """INSERT or REPLACE into specifications (userid, vtabs, htabs, menuFile, menuRepository, menuCommand,
                                                        menuTools, menuView, menuNavigate, menuPlugins, menuHelp, menuItemCount, toolbar) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(sqlite_insert_statement, (result, software.getVTabs(), software.getHTabs(),
                                                     software.getMenuFile(), software.getMenuRepo(), software.getMenuComm(),
                                                     software.getMenuTools(), software.getMenuView(), software.getMenuNav(),
                                                     software.getMenuPlug(), software.getMenuHelp(), software.getMenuItemCount(), software.getToolbar()))
            sqliteConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
                print("Error while inserting into specifications table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                
    def validPin(self, email, inputPin):
        try:
            sqliteConnection = sqlite3.connect("SoftwareReq.db")
            sqlite_select_query = "SELECT pin FROM users WHERE email=?"
            cursor = sqliteConnection.cursor()
            result = cursor.execute(sqlite_select_query, (email.lower(), ))
            try:
                dbPin = next(result)
                if dbPin[0] == inputPin:
                    cursor.close()
                    return True
                else:
                    cursor.close()
                    return False
            except StopIteration as e:
                cursor.close()
                return False
        except sqlite3.Error as error:
            print("Error while searching the database", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()

class User():
    
    def __init__(self):
        self._email = None
        self._pin = None
        self._pinString = None
        self._option = None
        self._menu = Menu()
        self._software = Software()
        self._file = File()
        
    def getEmail(self):
        return self._email
    
    def getPin(self):
        return self._pin
    
    def getPinString(self):
        return self._pinString
    
    def getOption(self):
        return self._option
    
    def getMenu(self):
        return self._menu
    
    def getSoftware(self):
        return self._software
    
    def getFile(self):
        return self._file
    
    def setEmail(self, x):
        self._email = x
        
    def setPin(self, x):
        self._pin = x
        
    def setPinString(self, x):
        self._pinString = x
        
    def setOption(self, x):
        self._option = x
        
    def setFile(self, x):
        self._file = x
        
    def getLoginOption(self):
        while self.getOption() != 0:
            #try to convert user input to a number
            try:
                print(self.getMenu().getLoginMenu())
                self.setOption(int(input("Enter your option: ")))
                if self.getOption() == 0:
                    print()
                    break;
                elif self.getOption() == 1:
                    self.setOption(self.register())
                    if self.getOption() == 0:
                        self.setOption(None)
                        continue
                elif self.getOption() == 2:
                    self.setOption(self.logIn())
                    if self.getOption() == 0:
                        self.setOption(None)
                        continue
                    elif self.getOption() != 0:
                        self.getMenuRequirementOption()
                        if self.getOption() == 0:
                            self.setOption(None)
                            continue
                        self.getTabRequirementOption()
                        if self.getOption() == 0:
                            self.setOption(None)
                            continue
                        self.getToolbarRequirementOption()
                        if self.getOption() == 0:
                            self.setOption(None)
                            continue
                        self.getFile().createDirectory(self.getEmail())
                        self.getFile().createPlantUMLSource(self.getSoftware())
                        self.getFile().createImage()
                        print(self.getMenu().getCreatingImageMessage())
                        self.getFile().showImage()
                else:
                    print()
                    print("Invalid option.")
            #if user does not input a number, this error is thrown      
            except ValueError:
                print()
                print("Input must be a number.")
        print("Thanks for using this program! Goodbye!")
        
    def getMenuRequirementOption(self):
        while self.getOption() != 0:
            try:
                print(self.getMenu().getMenuRequirementMenu())
                self.setOption(int(input("Enter your option: ")))
                if self.getOption() == 0:
                    return 0
                if self.getOption() == 1:
                    self.getSoftware().setMenuFile(True)
                    self.getSoftware().setMenuRepo(True)
                    self.getSoftware().setMenuComm(True)
                    self.getSoftware().setMenuTools(False)
                    self.getSoftware().setMenuView(False)
                    self.getSoftware().setMenuNav(False)
                    self.getSoftware().setMenuPlug(False)
                    self.getSoftware().setMenuHelp(True)
                    self.getSoftware().setMenuItemCount(4)
                    return 1
                elif self.getOption() == 2:
                    self.getSoftware().setMenuFile(True)
                    self.getSoftware().setMenuRepo(True)
                    self.getSoftware().setMenuComm(True)
                    self.getSoftware().setMenuTools(True)
                    self.getSoftware().setMenuView(False)
                    self.getSoftware().setMenuNav(False)
                    self.getSoftware().setMenuPlug(True)
                    self.getSoftware().setMenuHelp(True)
                    self.getSoftware().setMenuItemCount(6)
                    return 2
                elif self.getOption() == 3:
                    self.getSoftware().setMenuFile(True)
                    self.getSoftware().setMenuRepo(True)
                    self.getSoftware().setMenuComm(True)
                    self.getSoftware().setMenuTools(True)
                    self.getSoftware().setMenuView(True)
                    self.getSoftware().setMenuNav(True)
                    self.getSoftware().setMenuPlug(True)
                    self.getSoftware().setMenuHelp(True)
                    self.getSoftware().setMenuItemCount(8)
                    return 3
                else:
                    print()
                    print("Invalid option.")
            #if user does not input a number, this error is thrown      
            except ValueError:
                print()
                print("Input must be a number.")
        return 0
                
    def getTabRequirementOption(self):
        while self.getOption() != 0:
            try:
                print(self.getMenu().getTabRequirementMenu())
                self.setOption(int(input("Enter your option: ")))
                if self.getOption() == 0:
                    return 0
                elif self.getOption() == 1:
                    self.getSoftware().setVTabs(True)
                    self.getSoftware().setHTabs(False)
                    return 1
                elif self.getOption() == 2:
                    self.getSoftware().setVTabs(False)
                    self.getSoftware().setHTabs(True)
                    return 2
                else:
                    print()
                    print("Invalid option.")
            #if user does not input a number, this error is thrown      
            except ValueError:
                print()
                print("Input must be a number.")

    def getToolbarRequirementOption(self):
        while self.getOption() != 0:
            try:
                print(self.getMenu().getToolbarRequirementMenu())
                self.setOption(int(input("Enter your option: ")))
                if self.getOption() == 0:
                    return 0
                elif self.getOption() == 1:
                    self.getSoftware().setToolbar(True)
                    db = Database()
                    db.insertSpecification(self.getEmail(), self.getSoftware())
                    return 1
                elif self.getOption() == 2:
                    self.getSoftware().setToolbar(False)
                    db = Database()
                    db.insertSpecification(self.getEmail(), self.getSoftware())
                    return 2
                else:
                    print()
                    print("Invalid option.")
            #if user does not input a number, this error is thrown      
            except ValueError:
                print()
                print("Input must be a number.")

    def register(self):
        print()
        print("**********************************************")
        print("*           Registering a new user            *")
        print("**********************************************")
        #database object to check if user is available
        db = Database()
        print()
        self.setEmail(input("Enter your email (0 to exit): "))
        if self.getEmail() == '0':
            return 0
        while not (self.validEmail(self.getEmail())):
            print()
            print("Email must be valid.")
            print()
            self.setEmail(input("Enter your email (0 to exit): "))
            if self.getEmail() == '0':
                return 0
        if db.userAvailable(self.getEmail()):
            print()
            print("Username is available.")
            self.setPin(self.getUserPin())
            if self.getPin() == 0:
                return 0
            print()
            db.insertUserAndPin(self.getEmail(), self.getPin())
            print("**********************************************")
            print("*           New User Added                     *")
            print("**********************************************")
        else:
            print()
            print("User already exists.")
            print("Please choose a new username or log in.")
    
    def validEmail(self, email):
        regex = '^[A-Za-z0-9]+[\._]?[A-Za-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex,email):
            return True
        else:
            return False
    
    def getUserPin(self):
            while (True):
                print()
                self.setPinString(input("Enter your 4-digit pin number (0 to exit): "))
                try:
                    self.setPin(int(self.getPinString()))
                    if (self.getPin() == 0):
                        break;
                    if len(self.getPinString()) < 4 or len(self.getPinString()) > 4:
                        print()
                        print("Pin must contain four digits.")
                    elif len(self.getPinString()) == 4:
                        break;
                except ValueError:
                    print()
                    print("Pin numbers can only contain digits.")
            return self.getPin()
    
    def logIn(self):
        print()
        print("**********************************************")
        print("*                  Log in Screen                   *")
        print("**********************************************")
        print()
        self.setEmail(None)
        self.setEmail(input("Enter your email (0 to exit): "))
        if (self.getEmail() == '0'):
            return 0
        while not (self.validEmail(self.getEmail())):
            print()
            print("Email must be valid.")
            print()
            self.setEmail(input("Enter your email (0 to exit): "))
            if (self.getEmail() == '0'):
                return 0
        self.setPin(self.getUserPin())
        if (self.getPin() == 0):
            return 0
        db = Database()
        while not (db.validPin(self.getEmail(), self.getPin())):
            print()
            print("Pin does not match pin on file.")
            print("Please try again.")
            self.setPin(self.getUserPin())
            if (self.getPin() == 0):
                return 0
        return
    
class Software():
    def __init__ (self):
        self._vtabs = 0
        self._htabs = 0
        self._menuFile = 0
        self._menuRepo = 0
        self._menuComm = 0
        self._menuTools = 0
        self._menuView = 0
        self._menuNav = 0
        self._menuPlug = 0
        self._menuHelp = 0
        self._menuItemCount = 0
        self._toolbar = 0
        
    def setHTabs (self, x):
        self._htabs = x
        
    def setVTabs (self, x):
        self._vtabs = x
        
    def setMenuFile (self, x):
        self._menuFile = x
        
    def setMenuRepo (self, x):
        self._menuRepo = x
        
    def setMenuComm (self, x):
        self._menuComm = x
        
    def setMenuTools (self, x):
        self._menuTools = x
        
    def setMenuView (self, x):
        self._menuView = x
        
    def setMenuNav (self, x):
        self._menuNav = x
        
    def setMenuPlug (self, x):
        self._menuPlug = x
        
    def setMenuHelp (self, x):
        self._menuHelp = x
        
    def setMenuItemCount (self, x):
        self._menuItemCount = x
        
    def setToolbar (self, x):
        self._toolbar = x
      
    def getHTabs (self):
        return self._htabs
        
    def getVTabs (self):
        return self._vtabs
        
    def getMenuFile (self):
        return self._menuFile
        
    def getMenuRepo (self):
        return self._menuRepo
        
    def getMenuComm (self):
        return self._menuComm
        
    def getMenuTools (self):
        return self._menuTools
        
    def getMenuView (self):
        return self._menuView
        
    def getMenuNav (self):
        return self._menuNav
        
    def getMenuPlug (self):
       return self._menuPlug
        
    def getMenuHelp (self):
        return self._menuHelp
    
    def getMenuItemCount(self):
        return self._menuItemCount
    
    def getToolbar(self):
        return self._toolbar
    
class File():
    
    def __init__(self):
        self._directory = None
        self._parentDirectory = "./"
        self._path = None
        self._plantUMLText = None
        
    def getDirectory(self):
        return self._directory
    
    def getParentDirectory(self):
        return self._parentDirectory
    
    def getPath(self):
        return self._path
    
    def getPlantUMLText(self):
        return self._plantUMLText
    
    def setDirectory(self, x):
        self._directory = x
        
    def setPath(self, x):
        self._path = x
        
    def setPlantUMLText(self, x):
        self._plantUMLText = x
        
    def createDirectory(self, email):
        self.setDirectory(email)
        self.setPath(os.path.join(self.getParentDirectory(), self.getDirectory()))
        if not os.path.isdir(self.getPath()):
            os.mkdir(self.getPath())
            
    def createPlantUMLSource(self, software):
        if software.getHTabs() and software.getMenuItemCount() == 4 and software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Help }
{!                        
{/ Commit | Diff | <b>File Tree</b> | Console} { Toolbar:    <&home> <&folder> <&plus> <&chevron-left> <&chevron-right> <&clipboard> <&terminal> <&fork> <&transfer> <&loop-circular> <&cog> <&question-mark>}
{T 
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | *
Branches: | ^Master^ | *
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel]|[Ok]} 
}
} 
@endsalt""")
            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())
                
        elif software.getHTabs() and software.getMenuItemCount() == 4 and not software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Help }
{!                        
{/ Commit | Diff | <b>File Tree</b> | Console}
{T 
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | *
Branches: | ^Master^ | *
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel]|[Ok]} 
}
} 
@endsalt""")
            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())    
            
        elif  software.getHTabs() and software.getMenuItemCount() == 6 and software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Plugins | Tools | Help }
{!                        
{/ Commit | Diff | <b>File Tree</b> | Console} { Toolbar:    <&home> <&folder> <&plus> <&chevron-left> <&chevron-right> <&clipboard> <&terminal> <&fork> <&transfer> <&loop-circular> <&cog> <&question-mark>}
{T 
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | *
Branches: | ^Master^ | *
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel]|[Ok]} 
}
} 
@endsalt""")
            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())
                
        elif software.getHTabs() and software.getMenuItemCount() == 6 and not software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Plugins | Tools | Help }
{!                        
{/ Commit | Diff | <b>File Tree</b> | Console}
{T 
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | *
Branches: | ^Master^ | *
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel]|[Ok]} 
}
} 
@endsalt""")
            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())
                
        elif  software.getHTabs() and software.getMenuItemCount() == 8 and software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Plugins | Tools | View | Navigate | Help }
{!                        
{/ Commit | Diff | <b>File Tree</b> | Console} { Toolbar:    <&home> <&folder> <&plus> <&chevron-left> <&chevron-right> <&clipboard> <&terminal> <&fork> <&transfer> <&loop-circular> <&cog> <&question-mark>}
{T 
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | *
Branches: | ^Master^ | *
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel]|[Ok]} 
}
} 
@endsalt""")
            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())
                
        elif  software.getHTabs() and software.getMenuItemCount() == 8 and not software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Plugins | Tools | View | Navigate | Help }
{!                        
{/ Commit | Diff | <b>File Tree</b> | Console} 
{T 
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | *
Branches: | ^Master^ | *
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel]|[Ok]} 
}
} 
@endsalt""")
            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())                

        elif software.getVTabs() and software.getMenuItemCount() == 4 and software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Help | <&home> <&folder> <&plus> <&chevron-left> <&chevron-right> <&clipboard> <&terminal> <&fork> <&transfer> <&loop-circular> <&cog> <&question-mark>}
{                         
{/
Commit
Diff 
<b>File Tree</b>
Console
} | 
{T 
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | *
Branches: | ^Master^ | *
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel]|[Ok]} 
}
} 
@endsalt""")
            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())
                
        elif software.getVTabs() and software.getMenuItemCount() == 4 and not software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Help }
{                         
{/
Commit
Diff 
<b>File Tree</b>
Console
} | 
{T 
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | *
Branches: | ^Master^ | *
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel]|[Ok]} 
}
} 
@endsalt""")
            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())
                
        elif software.getVTabs() and software.getMenuItemCount() == 6 and software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Plugins | Tools | Help | <&home> <&folder> <&plus> <&chevron-left> <&chevron-right> <&clipboard> <&terminal> <&fork> <&transfer> <&loop-circular> <&cog> <&question-mark>}
{                         
{/
Commit
Diff 
<b>File Tree</b>
Console
} | 
{T 
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | *
Branches: | ^Master^ | *
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel]|[Ok]} 
}
} 
@endsalt""")

            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())
                
        elif software.getVTabs() and software.getMenuItemCount() == 6 and not software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Plugins | Tools | Help }
{                         
{/
Commit
Diff 
<b>File Tree</b>
Console
} | 
{T 
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | *
Branches: | ^Master^ | *
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel]|[Ok]} 
}
} 
@endsalt""")

            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())

        if software.getVTabs() and software.getMenuItemCount() == 8 and software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Plugins | Tools | View | Navigate | Help | }
{ 
{/
Commit
Diff 
<b>File Tree</b>
Console
} | 
{T
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | <&home> <&folder> <&plus> <&chevron-left> <&chevron-right> <&clipboard> 
Branches: | ^Master^  | <&terminal> <&fork> <&transfer><&loop-circular> <&cog> <&question-mark> 
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel] |[Ok]} 
}
} 
@endsalt""")
            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())
            
        elif software.getVTabs() and software.getMenuItemCount() == 8 and not software.getToolbar():
            self.setPlantUMLText("""@startsalt
scale 5
{+
{* File | Repository | Command | Plugins | Tools | View | Navigate | Help | }
{ 
{/
Commit
Diff 
<b>File Tree</b>
Console
} | 
{T
+My Computer
++ Local Disk (C:)
+++ Users
++++ YourName
++++ Documents
++++ Desktop
++++ OneDrive
+++++ Documents
++++++ Development Files} |
{ Search: | "testFile.py" | *
Branches: | ^Master^  | *
Command:  | (X) init | () push 
|.| () pull | () merge
|.| () fetch | *
Include: | [X] readme.md | [X] .gitignore
|.|[Cancel] |[Ok]} 
}
} 
@endsalt""")
            with open(abspath(self.getPath() + '/plant-uml.txt'), 'w') as writer:
                writer.write(self.getPlantUMLText())
                
    def createImage(self):                  

        # create a server object to call for your computations
        server = PlantUML(url='http://www.plantuml.com/plantuml/img/',
                                  basic_auth={},
                                  form_auth={}, http_opts={}, request_opts={})
    
        # Send and compile your diagram files to/with the PlantUML server
        server.processes_file(abspath(self.getPath() + '/plant-uml.txt'))
        
    def showImage(self):
        im = Image.open(abspath(self.getPath() + '/plant-uml.png'))
        im.show()
        
class Menu():

    def __init__ (self):
        self._loginMenu = """
Welcome to the Software Specifications Application.
Please choose from the choices below.
    
*************************************
*                                              *
*   [1] Register New User         *
*   [2] Log in                             *
*   [0] Exit the program             *
*                                               *
*************************************
"""
        self._menuRequirementMenu = """
***************************************************    
* Welcome to the Specification Questions  *
***************************************************

1. How many menu options should the program contain?
    
****************************************************************************************
*                                                                                                                   *
*   [1] 4 (File, Repository, Command, Help)                                                  *
*   [2] 6 (File, Repository, Command, Tools, Plugins, Help)                          *
*   [3] 8 (File, Repository, Command, Tools, View, Navigate, Plugins, Help) *
*   [0] Exit the Program                                                                                 *
*                                                                                                                   *
****************************************************************************************
"""
        self._tabRequirementMenu ="""
2. Do you want the program to contain horizontal or vertical tabs?
    
*************************************
*                                               *
*   [1] Vertical                           *
*   [2] Horizontal                       *
*   [0] Exit the program             *
*                                               *
*************************************
"""
        self._toolbarRequirementMenu = """
3. Should the application contain a toolbar?
    
*************************************
*                                               * 
*   [1] Yes                                 *
*   [2] No                                  *
*   [0] Exit the Program             *
*                                               *
*************************************
"""

        self._creatingImageMessage = """
*********************************************************
*   Creating and opening specifications image...  *      
*********************************************************

Returning to main menu..."""

    def getLoginMenu(self):
        return self._loginMenu
    
    def getMenuRequirementMenu(self):
        return self._menuRequirementMenu
    
    def getTabRequirementMenu(self):
        return self._tabRequirementMenu
    
    def getToolbarRequirementMenu(self):
        return self._toolbarRequirementMenu
    
    def getCreatingImageMessage(self):
        return self._creatingImageMessage
    
      
def main():
    db = Database()
    db.createConnection()
    db.createTables()
    user = User()
    user.getLoginOption()
    
if __name__ == "__main__": main()