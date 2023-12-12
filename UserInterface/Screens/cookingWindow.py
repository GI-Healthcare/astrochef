#!/usr/bin/env python3

import customtkinter as ctk
import rospy
from std_msgs.msg import Float32
import time
import os
from PIL import Image
import tkinter as tk

import sys
sys.path.append('..')
from app import App

import getpass
user = getpass.getuser()

buttonColour = "#1E272C"
backIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/back.png"), size=(60, 60))
homeIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/home.png"), size=(60, 60))
CookingLogo = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/logo/cookingLogo.png"), size=(280, 70))

buttonFont = ctk.CTkFont(family="Inter", size=40, weight="bold")

class CookingWindow(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        self.pack_propagate(0) 
        self.configure(width=480, height=800, fg_color="black")
        
        rospy.Subscriber("progress", Float32, self.progressCallback)

        cookingLogoLabel = ctk.CTkLabel(self, 
                                        text="",
                                        fg_color="transparent",
                                        image = CookingLogo
                                        )
        cookingLogoLabel.place(relx=0.2, rely=0.02)

        
        self.filename = "/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/animatedCooking1.gif"
        self.image = None

        self.animatedCookingLabel = tk.Label(self, bg="black")
        self.animatedCookingLabel.place(relx=0.1, rely=0.2)
        self.load_image(0)

        self.progressbar = ctk.CTkProgressBar(self,
                                         height=50,
                                         width=400,
                                         progress_color="orange",
                                       )
        self.progressbar.place(relx=0.08, rely=0.7)
        self.progressbar.set(0.0)

        ############# add cooking data here ##############

        ############# add cooking data here ##############

        self.cancelButton = ctk.CTkButton(self,
                                        text="Cancel Cooking",
                                        font=buttonFont,
                                        border_width=3,
                                        width=440,
                                        height=30,
                                        border_color="white",
                                        fg_color="transparent",
                                        hover_color=buttonColour,
                                        text_color="white",
                                        corner_radius=50,
                                        command=lambda: master.cancelCooking()
                                        )
        self.cancelButton.place(relx=0.04, rely=0.9)

    def progressCallback(self, msg):
        self.update_progress_bar(msg.data)

    def update_progress_bar(self, value):
        self.progressbar.set(value)
        self.update()
        if value == 1:
            self.cancelButton.configure(text="Finish")
    

    def load_image(self, index):
        """Load an image from the gif file and display it in the label"""
        try:
            self.image = tk.PhotoImage(file=self.filename, format=f"gif -index {index}") # load the image with tkinter
            self.animatedCookingLabel.configure(image=self.image) # update the label
            index += 1 # increment the index
            if index > 61: # change this number according to your gif file frames
                index = 0 # restart from first frame if end of file reached
            self.after(100, lambda: self.load_image(index)) # schedule next frame after 100 ms
        except tk.TclError:
            self.load_image(0) # restart from first frame if error occurred

