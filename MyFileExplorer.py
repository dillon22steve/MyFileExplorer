import os
from os import path
from pathlib import Path
import shutil

from tkinter import *
from tkinter import ttk

class MyFileExplorer():

    def __init__(self, root):

        root.geometry("800x400")
        root.title("My File Explorer!")

        #Creates the frame that will hold the tree storing the home directory
        homeDirFrame = ttk.Frame(root)
        homeDirFrame.place(x = 10, y = 55, width = 200, height = 300)
        homeDirFrame.config(relief=RIDGE)

        #Creates the frame that will hold the tree storing the current directory
        currDirFrame = ttk.Frame(root)
        currDirFrame.place(x = 220, y = 55, width = 570, height = 300)
        currDirFrame.config(relief=RIDGE)

        
        homeDirLabel = ttk.Label(root, text="Home Directory", font = ("Bookman Old Style", 10))
        homeDirLabel.place(x = 50, y = 30, width = 125, height = 20)
        currDirLabel = ttk.Label(root, text="Current Directory", font = ("Bookman Old Style", 10))
        currDirLabel.place(x = 450, y = 30, width = 150, height = 20)


        #The text box that displays the directory path to the user so they can copy it
        dirTextBox = Text(root, font = ("Bookman Old Style", 10))
        dirTextBox.place(x = 100, y = 5, width = 600, height = 20)


        #Initializes the current directory to the user's home directory and inserts that directory
        #into the text box
        homeDir = os.path.expanduser("~")
        os.chdir(homeDir)
        currDir = os.getcwd()
        dirTextBox.insert('1.0', currDir)


        #thisDir stores the name of the directory that the images are in. The following two lines
        #load the images into the folder and fileImg variables.
        thisDir = os.path.dirname(os.path.abspath(__file__))
        folder = PhotoImage(file = (thisDir + '\\FileFolder2.gif'))
        fileImg = PhotoImage(file = (thisDir + '\\File.gif'))


        #Initialize the tree that displays the files and subdirectories in the user's home directory.
        homeDirTree = ttk.Treeview(homeDirFrame)
        homeDirTree.place(x = 0, y = 0, width = 190, height = 300)
        homeDirTree.config(selectmode="browse")

        #Initializes the scrollbar that the user can use to scroll through the filed and subdirectories
        #in their home directory.
        hdtScrollbar = ttk.Scrollbar(homeDirFrame, orient="vertical", command=homeDirTree.yview)
        hdtScrollbar.place(x = 190, y = 0, width = 10, height = 300)
        homeDirTree.config(yscrollcommand = hdtScrollbar.set)



        #Initialize the tree that displays the files and subdirectories in the current directory.
        currDirTree = ttk.Treeview(currDirFrame)
        currDirTree.place(x = 0, y = 0, width = 560, height = 300)
        currDirTree.config(selectmode='browse')

        #Initializes the scrollbar that the user can use to scroll through the filed and subdirectories
        #in their current directory.
        cdtScrollbar = ttk.Scrollbar(currDirFrame, orient="vertical", command=currDirTree.yview)
        cdtScrollbar.place(x = 560, y = 0, width = 10, height = 300)
        currDirTree.config(yscrollcommand = cdtScrollbar.set)


        #Loops through the files and subdirectories in the user's home directory and displays them in
        #the homeDirTree
        def initHomeDir():
            i = 0
            for file in os.scandir(homeDir):
                fileName = file.name
                path = homeDir + "\\" + file.name
                
                #If file is a directory, it displays the folder image next to it, else it displays a file image.
                if os.path.isdir(path):
                    homeDirTree.insert('', i, i, text = fileName, image = folder)
                    i = i + 1
                else:
                    homeDirTree.insert('', 'end', i, text=fileName, image = fileImg)
                    i = i + 1



        def updateHomeDirTree(event):
            updateCwd(True)
        def updateCurrDirTree(event):
            updateCwd(False)

        #When the user clicks a folder, it updates the current directory to that folder
        #and then reconfigures the tree to display the new directory's contents
        def updateCwd(isHomeDir):
            fileName = ""

            #If the user clicks a folder in their home directory, updates currDir to the
            #home directory, else it updates currDir to the new directory
            if isHomeDir == True:
                currItem = homeDirTree.focus()
                fileName = homeDirTree.item(currItem).get("text")
                currDir = os.path.expanduser("~")
            else:
                currItem = currDirTree.focus()
                fileName = currDirTree.item(currItem).get("text")
                currDir = os.getcwd()

            #If the item clicked is a file, return. Else, change the directory.
            if path.isfile(fileName):
                return
            else:
                #Gets the new directory and chdir's into the new directory.
                nextDir = currDir + "\\" + fileName
                os.chdir(nextDir)
                currDir = os.getcwd()

                replaceCurrDirTree(nextDir)

                #Update the text box that displays the path to the directory.
                dirTextBox.delete('1.0', '1.0 lineend')
                dirTextBox.insert('1.0', currDir)
        
        #Updates the tree to display the new directories files and subdirectories
        def replaceCurrDirTree(newDir):
            #Deletes the current contents of the tree.
            for item in currDirTree.get_children():
                currDirTree.delete(item)

            i = 0
            for file in os.scandir(newDir):
                fileName = file.name
                path = newDir + "\\" + fileName

                #If file is a directory, it displays the folder image next to it, else it displays a file image.
                if os.path.isdir(path):
                    currDirTree.insert('', 'end', i, text=fileName, image=folder)
                    i = i + 1
                else:
                    currDirTree.insert('', 'end', i, text=fileName, image=fileImg)
                    i = i + 1




        initHomeDir()

        #When the user clicks a folder in the tree, it updates the tree
        homeDirTree.bind('<<TreeviewSelect>>', updateHomeDirTree)
        currDirTree.bind('<<TreeviewSelect>>', updateCurrDirTree)


        def createNewFile():
            print("Created new file")
        def createNewFolder():
            print("New folder")
            


        fileMenu = Menu(root)
        root.config(menu = fileMenu)

        newMenu = Menu(fileMenu)
        fileMenu.add_cascade(menu = newMenu, label="New")

        newMenu.add_command(label = "File", command=createNewFile)
        newMenu.add_separator()
        newMenu.add_command(label = "Folder", command = createNewFolder)