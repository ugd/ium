import argparse
import queue
import sys
import time
import threading
import os
import PIL
import multiprocessing
import tkinter as tk
from tkinter import IntVar
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import speech_recognition as sr
from matplotlib.animation import FuncAnimation
from speech_recognition import AudioData


from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class App:
    def __init__(self, root):
        # setting title
        root.title("Proiect IUM")
        # setting window size
        width = 800
        height = 600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.AppsStoredFilePathsDisk = './AppsStoredFilePaths.txt'
        self.VoiceCommandsStoredFilePathsDisk = './VoiceCommandsStoredFilePaths.txt'
        self.AppsPaths = []
        self.LiveInput = IntVar()
        self.currentItemFilePath = ""
        self.currentItemVocalCommand = ""

        self.LastCommandLabel = tk.Label(root)
        self.LastCommandLabel["anchor"] = "center"
        ft = tkFont.Font(family='Montseratt', size=20)
        self.LastCommandLabel["font"] = ft
        self.LastCommandLabel["fg"] = "#0e9dd5"
        self.LastCommandLabel["justify"] = "center"
        self.LastCommandLabel["text"] = "Last command"
        self.LastCommandLabel["relief"] = "flat"
        self.LastCommandLabel.place(x=10, y=10, width=780, height=35)

        # Here should plot be placed
        self.fig = Figure(figsize=(3, 2), dpi=50)
        self.t = np.arange(0, 3, .01)
        self.ax = self.fig.add_subplot()
        #self.arr = np.genfromtxt('./ium.txt', delimiter=',')
        data = np.genfromtxt('./ium.txt', delimiter=',')
        x, y = data.T
        self.ax.plot(x,y)
        self.ax.set_xlabel("time [s]")
        self.ax.set_ylabel("f(t)")
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT , expand=1)
        self.canvas.get_tk_widget().place(x=30, y=170, width=300, height=220)


        # Here should be the listbox with the apps

        self.LoadedAppsListbox = tk.Listbox(root)
        self.LoadedAppsListbox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Montseratt', size=10)
        self.LoadedAppsListbox["font"] = ft
        self.LoadedAppsListbox["fg"] = "#c4afc9"
        self.LoadedAppsListbox["justify"] = "left"
        # self.LoadedAppsListbox["text"] = "here will be the paths to the programs used or the system controls that will have voice commands assigned"
        self.LoadedAppsListbox.place(x=340, y=80, width=200, height=440)
        self.LoadedAppsListbox.bind("<<ListboxSelect>>", self.TriggerUpdateFileButtonOn)
        
        # Here should be the LoadApp Button

        LoadAppButton = tk.Button(root)
        LoadAppButton["bg"] = "#045c8c"
        # LoadAppButton["cursor"] = "watch"
        ft = tkFont.Font(family='Montseratt', size=10)
        LoadAppButton["font"] = ft
        LoadAppButton["fg"] = "#ffffff"
        LoadAppButton["justify"] = "center"
        LoadAppButton["text"] = "Load shortcut"
        LoadAppButton.place(x=340, y=560, width=200, height=30)
        LoadAppButton["command"] = self.LoadFile



        # Here should be the Reload App Button
        self.ReLoadAppButton = tk.Button(root)
        self.ReLoadAppButton["bg"] = "#045c8c"
        # LoadAppButton["cursor"] = "watch"
        ft = tkFont.Font(family='Montseratt', size=10)
        self.ReLoadAppButton["font"] = ft
        self.ReLoadAppButton["fg"] = "#ffffff"
        self.ReLoadAppButton["justify"] = "center"
        self.ReLoadAppButton['state'] = "disabled"
        self.ReLoadAppButton["text"] = "Reselect shortcut"
        self.ReLoadAppButton.place(x=340, y=45, width=200, height=30)
        self.ReLoadAppButton["command"] = self.ReplaceSelectedItemFilePath

        # Here should be the Delete App Button
        self.DeleteCurrentApp = tk.Button(root)
        self.DeleteCurrentApp["bg"] = "#045c8c"
        # LoadAppButton["cursor"] = "watch"
        ft = tkFont.Font(family='Montseratt', size=10)
        self.DeleteCurrentApp["font"] = ft
        self.DeleteCurrentApp["fg"] = "#ffffff"
        self.DeleteCurrentApp["justify"] = "center"
        self.DeleteCurrentApp['state'] = "disabled"
        self.DeleteCurrentApp["text"] = "Delete shortcut"
        self.DeleteCurrentApp.place(x=340, y=525, width=200, height=30)
        self.DeleteCurrentApp["command"] = self.DeleteSelectedItemApp

        # Here should be the Delete Voice Command Button
        self.DeleteVocalButton = tk.Button(root)
        self.DeleteVocalButton["bg"] = "#91529c"
        ft = tkFont.Font(family='Montseratt', size=10)
        self.DeleteVocalButton["font"] = ft
        self.DeleteVocalButton["fg"] = "#ffffff"
        self.DeleteVocalButton["justify"] = "center"
        self.DeleteVocalButton["state"] = "disabled"
        self.DeleteVocalButton["text"] = "Delete selected vocal command"
        self.DeleteVocalButton.place(x=580, y=525, width=200, height=30)
        self.DeleteVocalButton["command"] = self.DeleteSelectedItemVocalCommand


        # Here should be the Voice Commands Listbox
        self.VocalQuerriesListbox = tk.Listbox(root)
        self.VocalQuerriesListbox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Montseratt', size=10)
        self.VocalQuerriesListbox["font"] = ft
        self.VocalQuerriesListbox["fg"] = "#333333"
        self.VocalQuerriesListbox["justify"] = "left"
        # self.VocalQuerriesListbox["text"] = "here will be the aliases of the vocal commands"
        self.VocalQuerriesListbox.place(x=580, y=80, width=200, height=440)
        self.VocalQuerriesListbox.bind("<<ListboxSelect>>", self.TriggerUpdateVoiceCommandButtonOn)

        # Here should be the Load Voice Command Button
        self.AssignVocalButton = tk.Button(root)
        self.AssignVocalButton["bg"] = "#91529c"
        ft = tkFont.Font(family='Montseratt', size=10)
        self.AssignVocalButton["font"] = ft
        self.AssignVocalButton["fg"] = "#ffffff"
        self.AssignVocalButton["justify"] = "center"
        self.AssignVocalButton["text"] = "Assign vocal command"
        self.AssignVocalButton.place(x=580, y=560, width=200, height=30)
        self.AssignVocalButton["command"] = self.AssignVocalCommand

        # Here should be the Reload Voice Command Button
        self.ReAssignVocalButton = tk.Button(root)
        self.ReAssignVocalButton["bg"] = "#91529c"
        ft = tkFont.Font(family='Montseratt', size=10)
        self.ReAssignVocalButton["font"] = ft
        self.ReAssignVocalButton["fg"] = "#ffffff"
        self.ReAssignVocalButton["justify"] = "center"
        self.ReAssignVocalButton["state"] = "disabled"
        self.ReAssignVocalButton["text"] = "Replace selected vocal command"
        self.ReAssignVocalButton.place(x=580, y=45, width=200, height=30)
        self.ReAssignVocalButton["command"] = self.ReplaceSelectedItemVocalCommand

        # Here should be the Live Input Button
        self.LiveInputCheckbox = tk.Checkbutton(root)
        self.ft = tkFont.Font(family='Montseratt', size=10)
        self.LiveInputCheckbox["font"] = ft
        self.LiveInputCheckbox["fg"] = "#333333"
        self.LiveInputCheckbox["justify"] = "center"
        self.LiveInputCheckbox["text"] = "Live input"
        self.LiveInputCheckbox.place(x=30, y=30, width=70, height=25)
        self.LiveInputCheckbox["offvalue"] = "0"
        self.LiveInputCheckbox["onvalue"] = "1"
        self.LiveInputCheckbox["variable"] = self.LiveInput
        self.LiveInputCheckbox["command"] = self.LiveRecognizeCommand

    

        # load file paths from disk
        try:
            with open(self.AppsStoredFilePathsDisk, 'r', encoding="utf8") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    self.LoadedAppsListbox.insert(0, os.path.split(line.strip('\n'))[-1].split(".")[0])
                for line in lines:
                    self.AppsPaths.append(line.strip('\n'))
                f.close()
        except FileNotFoundError:
            print("File not found")
        try:
            with open(self.VoiceCommandsStoredFilePathsDisk, 'r', encoding="utf8") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    self.VocalQuerriesListbox.insert(0, line.strip('\n'))
                f.close()
        except FileNotFoundError:
            print("File not found")

    def TriggerUpdateFileButtonOn(self, x):
        self.ReLoadAppButton["state"] = "normal"
        self.DeleteCurrentApp["state"] = "normal"


    def TriggerUpdateVoiceCommandButtonOn(self, x):
        print("status live input", self.LiveInput.get())
        if self.LiveInput.get() == 1:
            self.ReAssignVocalButton["state"] = "disabled"
            self.DeleteVocalButton["state"] = "disabled"
        else:
            self.ReAssignVocalButton["state"] = "normal"
            self.DeleteVocalButton["state"] = "normal"
            self.DeleteVocalButton["bg"] = "#91529c"
            self.DeleteVocalButton["fg"] = "#ffffff"
            self.ReAssignVocalButton["bg"] = "#91529c"
            self.ReAssignVocalButton["fg"] = "#ffffff"

    # Delete the selected item from self.VoiceCommandsListbox
    def DeleteSelectedItemVocalCommand(self):
        try:
            self.VocalQuerriesListbox.delete(self.VocalQuerriesListbox.curselection())
            with open(self.VoiceCommandsStoredFilePathsDisk, 'w', encoding="utf8") as f:
                for line in self.VocalQuerriesListbox.get(0, tk.END):
                    f.write(line + '\n')
                f.close()
        except:
            print("No item selected")

    # Delete the selected item from self.LoadedAppsListbox
    def DeleteSelectedItemApp(self):
        try:
            print("inainte de stergere", self.AppsPaths)
            self.AppsPaths.pop(self.LoadedAppsListbox.index(tk.ACTIVE))
            self.LoadedAppsListbox.delete(self.LoadedAppsListbox.curselection())
            print("dupa stergere",self.AppsPaths)
            with open(self.AppsStoredFilePathsDisk, 'w', encoding="utf8") as f:
                for line in self.AppsPaths:
                    f.write(line + '\n')
                f.close()
        except Exception as e:
            print("No item selected")
            print(e)

    # Replace the selected item in the listbox with the new file path
    def ReplaceSelectedItemFilePath(self):
        filename = askopenfilename()
        # if filename is empty, exit the function
        if filename == "":
            return
        self.AppsPaths[self.LoadedAppsListbox.index(tk.ACTIVE)] = filename
        self.LoadedAppsListbox.insert(tk.ACTIVE, os.path.split(filename)[-1].split(".")[0])
        self.LoadedAppsListbox.delete(self.LoadedAppsListbox.index(tk.ACTIVE))

        # open self.LoadedAppsListbox in update mode and select index row assigned to index of tk.ACTIVE in self.LoadedAppsListbox and rewrite with new self.LoadedAppsListbox
        # then close the file
        try:
            with open(self.AppsStoredFilePathsDisk, 'r+', encoding="utf8") as f:
                f.truncate(0)
                f.seek(0)
                for path in self.AppsPaths:
                    f.write(path + "\n")
                f.close()
        except FileNotFoundError:
            print("File not found")

    # Replace the selected item in the listbox with the new vocal command
    def ReplaceSelectedItemVocalCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            voice_data = r.recognize_google(
                audio, language="ro-RO", show_all=False)
            if voice_data not in self.VocalQuerriesListbox.get(0, tk.END):
                self.VocalQuerriesListbox.delete(tk.ACTIVE)
                self.VocalQuerriesListbox.insert(tk.ACTIVE, voice_data)   
                # open self.VoiceCommandsStoredFilePathsDisk in update mode and select index row assigned to index of tk.ACTIVE in self.VocalQuerriesListbox and rewrite with new self.VocalQuerriesListbox
                # then close the file
                try:
                    with open(self.VoiceCommandsStoredFilePathsDisk, 'r+', encoding="utf8") as f:
                        f.truncate(0)
                        f.seek(0)
                        for i in range(len(self.VocalQuerriesListbox.get(0, tk.END))):
                            f.write(self.VocalQuerriesListbox.get(i) + '\n')
                        f.close()
                except FileNotFoundError:
                    print("File not found")
            else:
                print(voice_data, " command already exists")
            print(voice_data)
        except Exception as e:
            print("except: ", e)
            pass

    def LoadFile(self):
        filename = askopenfilename()
        self.LoadedAppsListbox.insert(
            tk.END, os.path.split(filename)[-1].split(".")[0])
        self.AppsPaths.append(filename)
        # insert filename into self.AppsStoredFilePathsDisk file
        try:
            with open(self.AppsStoredFilePathsDisk, 'a', encoding="utf8") as f:
                f.write(filename + '\n')
                f.close()
        except FileNotFoundError:
            print("Could not open file")
        print(filename)

    def LiveRecognizeCommand(self):
        print("Status", self.LiveInput.get())
        if self.LiveInput.get() == 1:
            try:
                self.thread = threading.Thread(target=self.VoiceRecognition)
                self.thread.start()
            except Exception as e:
                print("Error: unable to start thread; ", e)

    def Execute(self, filename):
        os.startfile(filename)

    def VoiceRecognition(self):
        r = sr.Recognizer()
        self.AssignVocalButton["state"] = "disabled"
        self.ReAssignVocalButton["state"] = "disabled"
        while True:
            with sr.Microphone() as source:
                audio = r.listen(source)
                audio_raw = audio.get_raw_data()
                audio_data = np.frombuffer(audio_raw, np.int16)

                # self.ax.plot(x, y)
                try:
                    if self.LiveInput.get() == 0:
                        print("stop")
                        self.AssignVocalButton["state"] = "normal"
                        break
                    voice_data = r.recognize_google(
                        audio, language="ro-RO", show_all=False)
                    self.LastCommandLabel["text"] = voice_data
                    if voice_data == "stop live input":
                        self.AssignVocalButton["state"] = "normal"
                        self.LiveInput.set(0)
                        break
                    if voice_data in self.VocalQuerriesListbox.get(0, tk.END):
                        self.Execute(self.AppsPaths[self.VocalQuerriesListbox.get(
                            0, tk.END).index(voice_data)])
                    print(voice_data)

                except Exception as e:
                    print("except: ", e)
                    continue  # to avoid stopping the program if the voice data has not been recognized as a valid utterance

    def AssignVocalCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            voice_data = r.recognize_google(
                audio, language="ro-RO", show_all=False)
            if voice_data not in self.VocalQuerriesListbox.get(0, tk.END):
                self.VocalQuerriesListbox.insert(tk.END, voice_data)
                # insert voice_data into a list into self.VoiceCommandsStoredFilePathsDisk
                try:
                    with open(self.VoiceCommandsStoredFilePathsDisk, "a", encoding="utf8") as f:
                        f.write(voice_data + "\n")
                        f.close()
                except Exception as e:
                    print("error?: ", e)
            else:
                print(voice_data, " command already exists")
            print(voice_data)
        except Exception as e:
            print("Exception:", e)
            pass
        # print("command")




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
