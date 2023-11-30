import MyFileExplorer

from tkinter import *
from tkinter import ttk

def main():
    root = Tk()
    root.option_add('*tearOff', False)
    myFileExplorer = MyFileExplorer.MyFileExplorer(root)
    root.mainloop()

if __name__ == "__main__": main()