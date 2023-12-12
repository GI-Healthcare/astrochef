#!/usr/bin/env python3

import customtkinter as ctk
import rospy
from std_msgs.msg import String
import time
import os
from PIL import Image
import tkinter

import sys
sys.path.append('..')
from app import App

import getpass
user = getpass.getuser()

buttonColour = "#1E272C"
backIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/back.png"), size=(60, 60))
homeIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/home.png"), size=(60, 60))
imageIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/imageIcon1.png"), size=(360, 300))

buttonFont = ctk.CTkFont(family="Inter", size=50, weight="bold")

class CusAvaWindow(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        self.pack_propagate(0) 
        self.configure(width=480, height=800, fg_color="black")

        backButton = ctk.CTkButton(self, 
                                   text="",
                                   image=backIcon,
                                   corner_radius=10,
                                   width=20,
                                   height=20,
                                   fg_color="transparent",
                                   hover_color="#1E272C",
                                   command=lambda: master.switch_frame("MainWindow")
                                   )
        backButton.place(relx=0.03, rely=0.02)

        homeButton = ctk.CTkButton(self, 
                                   text="",
                                   image=homeIcon,
                                   corner_radius=30,
                                   fg_color="transparent",
                                   hover_color="#1E272C",
                                   width=20,
                                   height=20,
                                   command=lambda: master.switch_frame("MainWindow")
                                   )
        homeButton.place(relx=0.8, rely=0.02)

        imageIconLabel = ctk.CTkLabel(self, 
                                      text="",
                                      fg_color="transparent",
                                      image = imageIcon
                                      )
        imageIconLabel.place(relx=0.11, rely=0.2)

        availableButton = ctk.CTkButton(self,
                                        text="Available Dish",
                                        font=buttonFont,
                                        border_width=3,
                                        width=440,
                                        height=30,
                                        border_color="white",
                                        fg_color="transparent",
                                        hover_color=buttonColour,
                                        text_color="white",
                                        corner_radius=50,
                                        command=lambda: master.switch_frame("AvailableDishWindow")
                                        )
        availableButton.place(relx=0.04, rely=0.7)

        customButton = ctk.CTkButton(self,
                                     text="Custom Dish",
                                     font=buttonFont,
                                     border_width=3,
                                     width=440,
                                     height=30,
                                     border_color="white",
                                     fg_color="transparent",
                                     hover_color=buttonColour,
                                     text_color="white",
                                     corner_radius=50,
                                     command=lambda: master.switch_frame("InventoryWindow")
                                     )
        customButton.place(relx=0.04, rely=0.85)
