import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLineEdit_14=tk.Entry(root)
        GLineEdit_14["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_14["font"] = ft
        GLineEdit_14["fg"] = "#333333"
        GLineEdit_14["justify"] = "center"
        GLineEdit_14["text"] = "here will be the paths to the programs used or the system controls that will have voice commands assigned"
        GLineEdit_14.place(x=330,y=80,width=107,height=337)

        GLineEdit_87=tk.Entry(root)
        GLineEdit_87["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_87["font"] = ft
        GLineEdit_87["fg"] = "#333333"
        GLineEdit_87["justify"] = "center"
        GLineEdit_87["text"] = "here will be the aliases of the vocal commands"
        GLineEdit_87.place(x=450,y=80,width=110,height=337)

        GButton_14=tk.Button(root)
        GButton_14["bg"] = "#ff4a3d"
        GButton_14["cursor"] = "watch"
        ft = tkFont.Font(family='Times',size=10)
        GButton_14["font"] = ft
        GButton_14["fg"] = "#000000"
        GButton_14["justify"] = "center"
        GButton_14["text"] = "Load file"
        GButton_14.place(x=340,y=440,width=94,height=30)
        GButton_14["command"] = self.GButton_14_command

        GMessage_38=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_38["font"] = ft
        GMessage_38["fg"] = "#333333"
        GMessage_38["justify"] = "center"
        GMessage_38["text"] = "EDITME-ADD A VIEW THAT ALLOWS REALTIME GRAPHICS OF THE MIC SIGNAL"
        GMessage_38.place(x=40,y=170,width=193,height=95)

        GButton_846=tk.Button(root)
        GButton_846["bg"] = "#ff4a3d"
        ft = tkFont.Font(family='Times',size=10)
        GButton_846["font"] = ft
        GButton_846["fg"] = "#000000"
        GButton_846["justify"] = "center"
        GButton_846["text"] = "Assign vocal command"
        GButton_846.place(x=460,y=440,width=97,height=31)
        GButton_846["command"] = self.GButton_846_command

    def GButton_14_command(self):
        print("command")


    def GButton_846_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
