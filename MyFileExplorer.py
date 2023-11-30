import os
from os import path
import shutil

from tkinter import *
from tkinter import ttk

class MyFileExplorer():

    def __init__(self, root):

        homeDirFrame = ttk.Frame(root)
        homeDirFrame.grid(row=2, column=0)
        homeDirFrame.config(width=100, height=400)
        homeDirFrame.config(relief=RIDGE)

        currDirFrame = ttk.Frame(root)
        currDirFrame.grid(row=2, column=1)
        currDirFrame.config(width=500, height=400)
        currDirFrame.config(relief=RIDGE)


        homeDirLabel = ttk.Label(root, text="Home Directory")
        homeDirLabel.grid(row=1, column=0)
        currDirLabel = ttk.Label(root, text="Current Directory")
        currDirLabel.grid(row=1, column=1)


        dirTextBox = Text(root, width = 50, height = 1)
        dirTextBox.grid(row=0, column=0, columnspan=2)


        homeDir = os.path.expanduser("~")
        os.chdir(homeDir)
        currDir = os.getcwd()
        dirTextBox.insert('1.0', currDir)


        folder = PhotoImage("FileFolder.gif").subsample(5, 5)


        homeDirTree = ttk.Treeview(homeDirFrame)
        homeDirTree.grid(row=0, column=0, rowspan=10)
        homeDirTree.config(selectmode="browse")

        hdtScrollbar = ttk.Scrollbar(homeDirFrame, orient="vertical", command=homeDirTree.yview)
        hdtScrollbar.grid(row=0, column=1, rowspan=10, sticky='ns')
        homeDirTree.config(yscrollcommand = hdtScrollbar.set)




        currDirTree = ttk.Treeview(currDirFrame)
        currDirTree.grid(row=0, column=0, rowspan=10)
        currDirTree.config(selectmode='browse')

        cdtScrollbar = ttk.Scrollbar(currDirFrame, orient="vertical", command=currDirTree.yview)
        cdtScrollbar.grid(row=0, column=1, rowspan=10, sticky='ns')
        currDirTree.config(yscrollcommand = cdtScrollbar.set)



        def initHomeDir():
            i = 0
            for file in os.scandir(homeDir):
                if file.is_dir:
                    fileName = file.name
                    homeDirTree.insert('', 'end', i, text=fileName, image=folder)
                    i = i + 1
                else:
                    fileName = file.name
                    homeDirTree.insert('', 'end', i, text=fileName)
                    i = i + 1

            desktop = currDir + "\\Desktop"
            replaceCurrDirTree(desktop)
            os.chdir(desktop)



        def updateHomeDirTree(event):
            updateCwd(True)
        def updateCurrDirTree(event):
            updateCwd(False)

        def updateCwd(isHomeDir):
            fileName = ""
            if isHomeDir == True:
                currItem = homeDirTree.focus()
                fileName = homeDirTree.item(currItem).get("text")
                currDir = os.path.expanduser("~")
            else:
                currItem = currDirTree.focus()
                fileName = currDirTree.item(currItem).get("text")
                currDir = os.getcwd()

            if path.isfile(fileName):
                return
            else:
                nextDir = currDir + "\\" + fileName
                os.chdir(nextDir)

                replaceCurrDirTree(nextDir)

                dirTextBox.delete('1.0', '1.0 lineend')
                dirTextBox.insert('1.0', nextDir)
        
        def replaceCurrDirTree(newDir):
            for item in currDirTree.get_children():
                currDirTree.delete(item)

            i = 0
            for file in os.scandir(newDir):
                if file.is_dir:
                    fileName = file.name
                    currDirTree.insert('', 'end', i, text=fileName, image=folder)
                    i = i + 1
                else:
                    fileName = file.name
                    currDirTree.insert('', 'end', i, text=fileName)
                    i = i + 1




        initHomeDir()

        homeDirTree.bind('<<TreeviewSelect>>', updateHomeDirTree)
        currDirTree.bind('<<TreeviewSelect>>', updateCurrDirTree)


        homeDirFrame.rowconfigure(10, weight = 1)
        homeDirFrame.columnconfigure(2, weight = 1)
        currDirFrame.rowconfigure(10, weight=1)
        currDirFrame.columnconfigure(2, weight=1)


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