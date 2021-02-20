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
        self.email = None
        self.pin = None

    def register(self):
        print()
        print("**********************************************")
        print("*           Registering a new user            *")
        print("**********************************************")
        db = Database()
        print()
        self.email = input("Enter your email (0 to exit): ")
        if self.email == '0':
            return 0
        while not (self.validEmail(self.email)):
            print()
            print("Email must be valid.")
            print()
            self.email = input("Enter your email (0 to exit): ")
            if self.email == '0':
                return 0
        if db.userAvailable(self.email):
            print()
            print("Username is available.")
            self.pin = self.getPin()
            if (self.pin == 0):
                return
            print()
            db.insertUserAndPin(self.email, self.pin)
            print("**********************************************")
            print("*           New User Added                     *")
            print("**********************************************")
        else:
            print()
            print("User already exists.")
            print("Please choose a new username or log in.")
    
    def validEmail(self, email):
        regex = '^[A-Za-z0-9]+[\._]?[A-Za-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex,self.email):
            return True
        else:
            return False
    
    def getPin(self):
            while (True):
                print()
                pinString = input("Enter your 4-digit pin number (0 to exit): ")
                try:
                    pin = int(pinString)
                    if (pin == 0):
                        break;
                    if len(pinString) < 4 or len(pinString) > 4:
                        print()
                        print("Pin must contain four digits.")
                    elif len(pinString) == 4:
                        break;
                except ValueError:
                    print()
                    print("Pin numbers can only contain digits.")
            return pin
    
    def logIn(self):
        print()
        print("**********************************************")
        print("*                  Log in Screen                   *")
        print("**********************************************")
        print()
        self.email = None
        self.email = input("Enter your email (0 to exit): ")
        if (self.email == '0'):
            return self.email
        while not (self.validEmail(self.email)):
            print()
            print("Email must be valid.")
            print()
            self.email = input("Enter your email (0 to exit): ")
            if (self.email == '0'):
                return self.email
        self.pin = self.getPin()
        if (self.pin == 0):
            return self.pin
        db = Database()
        while not (db.validPin(self.email, self.pin)):
            print()
            print("Pin does not match pin on file.")
            print("Please try again.")
            self.pin = self.getPin()
            if (self.pin == 0):
                return self.pin
        print()
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
    
    def __init__(self, software, email):
        self._directory = email
        self._parentDirectory = "./"
        self._path = os.path.join(self._parentDirectory, self._directory)
        if not os.path.isdir(self._path):
            os.mkdir(self._path)
        if software.getHTabs() and software.getMenuItemCount() == 4 and software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""
            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)
                
        elif software.getHTabs() and software.getMenuItemCount() == 4 and not software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""
            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)    
            
        elif  software.getHTabs() and software.getMenuItemCount() == 6 and software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""
            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)
                
        elif  software.getHTabs() and software.getMenuItemCount() == 6 and not software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""
            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)
                
        elif  software.getHTabs() and software.getMenuItemCount() == 8 and software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""
            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)
                
        elif  software.getHTabs() and software.getMenuItemCount() == 8 and not software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""
            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)                

        elif software.getVTabs() and software.getMenuItemCount() == 4 and software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""
            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)
                
        elif software.getVTabs() and software.getMenuItemCount() == 4 and not software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""
            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)
                
        elif software.getVTabs() and software.getMenuItemCount() == 6 and software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""

            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)
                
        elif software.getVTabs() and software.getMenuItemCount() == 6 and not software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""

            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)

        if software.getVTabs() and software.getMenuItemCount() == 8 and software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""
            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)
            
        elif software.getVTabs() and software.getMenuItemCount() == 8 and not software.getToolbar():
            self._specificationsText = """@startsalt
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
@endsalt"""
            with open(abspath(self._path + '/plant-uml.txt'), 'w') as writer:
                writer.write(self._specificationsText)
    def getPath(self):
        return self._path
    
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

    user = User()
    software = Software()
    
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
    
****************************************************************************************
*                                                                                                                   *
*   [1] Yes                                                                                                     *
*   [2] No                                                                                                       *
*   [0] Exit the Program                                                                                 *
*                                                                                                                   *
****************************************************************************************
"""
        self._option = None
    
    def getLoginMenu(self):
        return self._loginMenu
    
    def getMenuRequirementMenu(self):
        return self._menuRequirementMenu
    
    def getTabRequirementMenu(self):
        return self._tabRequirementMenu
    
    def getToolbarRequirementMenu(self):
        return self._toolbarRequirementMenu
    
    def getOption(self):
        return self._option
    
    def setOption(self, x):
        self._option =  x
    
    def getLoginOption(self):
        while self.getOption() != 0:
            #try to convert user input to a number
            try:
                print(self.getLoginMenu())
                self.setOption(int(input("Enter your option: ")))
                if self.getOption() == 0:
                    print()
                    break;
                elif self.getOption() == 1:
                    self.setOption(self.user.register())
                    # Insert Quit Code
                elif self.getOption() == 2:
                    self.setOption(self.user.logIn())
                    if self.getOption() != '0' and self.getOption() != 0:
                        self.getMenuRequirementOption()
                        self.getTabRequirementOption()
                        self.getToolbarRequirementOption()
                        file = File(self.software, self.user.email)
                        file.createImage()
                        file.showImage()
                    else:
                        self.setOption(None)
                        continue
                else:
                    print()
                    print("Invalid option.")
                    print()
            #if user does not input a number, this error is thrown      
            except ValueError:
                print()
                print("Input must be a number.")
                print()
        print("Thanks for using this program! Goodbye!")

    def getMenuRequirementOption(self):
        while self.getOption() != 0:
            try:
                print(self.getMenuRequirementMenu())
                self.setOption(nt(input("Enter your option: ")))
                if self.getOption() == 0:
                    print()
                    break;
                elif self.getOption() == 1:
                    self.software.setMenuFile(True)
                    self.software.setMenuRepo(True)
                    self.software.setMenuComm(True)
                    self.software.setMenuTools(False)
                    self.software.setMenuView(False)
                    self.software.setMenuNav(False)
                    self.software.setMenuPlug(False)
                    self.software.setMenuHelp(True)
                    self.software.setMenuItemCount(4)
                    return
                elif self.getOption() == 2:
                    self.software.setMenuFile(True)
                    self.software.setMenuRepo(True)
                    self.software.setMenuComm(True)
                    self.software.setMenuTools(True)
                    self.software.setMenuView(False)
                    self.software.setMenuNav(False)
                    self.software.setMenuPlug(True)
                    self.software.setMenuHelp(True)
                    self.software.setMenuItemCount(6)
                    return
                elif self.getOption() == 3:
                    self.software.setMenuFile(True)
                    self.software.setMenuRepo(True)
                    self.software.setMenuComm(True)
                    self.software.setMenuTools(True)
                    self.software.setMenuView(True)
                    self.software.setMenuNav(True)
                    self.software.setMenuPlug(True)
                    self.software.setMenuHelp(True)
                    self.software.setMenuItemCount(8)
                    return
                else:
                    print()
                    print("Invalid option.")
                    print()
            #if user does not input a number, this error is thrown      
            except ValueError:
                print()
                print("Input must be a number.")
                print()
                
    def getTabRequirementOption(self):
        while self.getOption() != 0:
            try:
                print(self.getTabRequirementMenu())
                self.setOption(int(input("Enter your option: ")))
                if self.getOption() == 0:
                    print()
                    break;
                elif self.getOption() == 1:
                    self.software.setVTabs(True)
                    self.software.setHTabs(False)
                    return
                elif self.getOption() == 2:
                    self.software.setVTabs(False)
                    self.software.setHTabs(True)
                    return
                else:
                    print()
                    print("Invalid option.")
                    print()
            #if user does not input a number, this error is thrown      
            except ValueError:
                print()
                print("Input must be a number.")
                print()

    def getToolbarRequirementOption(self):
        while self.getOption() != 0:
            try:
                print(self.getToolbarRequirementMenu())
                self.setOption(int(input("Enter your option: ")))
                if self.getOption() == 0:
                    print()
                    break;
                elif self.getOption() == 1:
                    self.software.setToolbar(True)
                    db = Database()
                    db.insertSpecification(self.user.email, self.software)
                    return
                elif self.getOption() == 2:
                    self.software.setToolbar(False)
                    db = Database()
                    db.insertSpecification(self.user.email, self.software)
                    return
                else:
                    print()
                    print("Invalid option.")
                    print()
            #if user does not input a number, this error is thrown      
            except ValueError:
                print()
                print("Input must be a number.")
                print()
      
def main():
    db = Database()
    db.createConnection()
    db.createTables()
    menu = Menu()
    menu.getLoginOption()
    
if __name__ == "__main__": main()