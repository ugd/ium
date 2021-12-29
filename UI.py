import argparse
import queue
import sys
import os
import time
import threading
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


class App:
    def __init__(self, root):
        # setting title
        root.title("Proiect IUM")
        # setting window size
        width = 800
        height = 600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.AppsPaths = []
        self.LiveInput = IntVar()

        # aici ar trebui sa apara plot-ul
        PlotMessage = tk.Message(root)
        ft = tkFont.Font(family='Montseratt', size=24)
        PlotMessage["font"] = ft
        PlotMessage["fg"] = "#0e9dd5"
        PlotMessage["justify"] = "center"
        PlotMessage["text"] = "PLOT Almost before we knew it, we had left the"
        PlotMessage.place(x=40, y=170, width=193, height=95)

        self.LoadedAppsListbox = tk.Listbox(root)
        self.LoadedAppsListbox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Montseratt', size=10)
        self.LoadedAppsListbox["font"] = ft
        self.LoadedAppsListbox["fg"] = "#c4afc9"
        self.LoadedAppsListbox["justify"] = "left"
        # self.LoadedAppsListbox["text"] = "here will be the paths to the programs used or the system controls that will have voice commands assigned"
        self.LoadedAppsListbox.place(x=340, y=80, width=200, height=440)

        LoadAppButton = tk.Button(root)
        LoadAppButton["bg"] = "#045c8c"
        # LoadAppButton["cursor"] = "watch"
        ft = tkFont.Font(family='Montseratt', size=10)
        LoadAppButton["font"] = ft
        LoadAppButton["fg"] = "#ffffff"
        LoadAppButton["justify"] = "center"
        LoadAppButton["text"] = "Load file"
        LoadAppButton.place(x=340, y=540, width=200, height=30)
        LoadAppButton["command"] = self.LoadFile

        self.VocalQuerriesListbox = tk.Listbox(root)
        self.VocalQuerriesListbox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Montseratt', size=10)
        self.VocalQuerriesListbox["font"] = ft
        self.VocalQuerriesListbox["fg"] = "#333333"
        self.VocalQuerriesListbox["justify"] = "left"
        # self.VocalQuerriesListbox["text"] = "here will be the aliases of the vocal commands"
        self.VocalQuerriesListbox.place(x=580, y=80, width=200, height=440)

        AssignVocalButton = tk.Button(root)
        AssignVocalButton["bg"] = "#91529c"
        ft = tkFont.Font(family='Montseratt', size=10)
        AssignVocalButton["font"] = ft
        AssignVocalButton["fg"] = "#ffffff"
        AssignVocalButton["justify"] = "center"
        AssignVocalButton["text"] = "Assign vocal command"
        AssignVocalButton.place(x=580, y=540, width=200, height=30)
        AssignVocalButton["command"] = self.AssignVocalCommand

        self.LiveInputCheckbox=tk.Checkbutton(root)
        self.ft = tkFont.Font(family='Montseratt',size=10)
        self.LiveInputCheckbox["font"] = ft
        self.LiveInputCheckbox["fg"] = "#333333"
        self.LiveInputCheckbox["justify"] = "center"
        self.LiveInputCheckbox["text"] = "Live input"
        self.LiveInputCheckbox.place(x=30,y=30,width=70,height=25)
        self.LiveInputCheckbox["offvalue"] = "0"
        self.LiveInputCheckbox["onvalue"] = "1"
        self.LiveInputCheckbox["variable"] = self.LiveInput
        self.LiveInputCheckbox["command"] = self.LiveRecognizeCommand

    def LoadFile(self):
        filename = askopenfilename()
        self.LoadedAppsListbox.insert(
            tk.END, os.path.split(filename)[-1].split(".")[0])
        self.AppsPaths.append(filename)
        print(filename)

    def LiveRecognizeCommand(self):
        print("Status", self.LiveInput.get())
        if self.LiveInput.get() == 1:
            try:
                self.thread = multiprocessing.Process(target=self.VoiceRecognition)
                self.thread.start()
            except:
                print ("Error: unable to start thread")
        else:
            try:
                pass
            except IndexError as e:
                print(e) 
    
    def Execute(self, filename):
        os.startfile(filename)

    def VoiceRecognition(self):
        r = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                audio = r.listen(source)
                try:
                    voice_data = r.recognize_google(audio, language="en-US", show_all=False)
                except:
                    print("except")
                    continue    #to avoid stopping the program if the voice data has not been recognized as a valid utterance
                print(voice_data)
                # if self.LiveInput.get() == 0:
                #     print("stop")
                #     break
            

    def AssignVocalCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            voice_data = r.recognize_google(
                audio, language="en-US", show_all=False)
            if voice_data not in self.VocalQuerriesListbox.get(0, tk.END):
                self.VocalQuerriesListbox.insert(tk.END, voice_data)
            else:
                print(voice_data , " command already exists")
            print(voice_data)
        except:
            print("except")
            pass
        # print("command")

    

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
