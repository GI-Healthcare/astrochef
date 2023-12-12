#!/usr/bin/env python3

import customtkinter as ctk
import rospy
from std_msgs.msg import String
import time
import os
from PIL import Image
import tkinter as tk

import sys
sys.path.append('..')
from app import App


import getpass
user = getpass.getuser()

logoIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/logo/logo.png"), size=(480, 70))
signOutIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/signOut.png"), size=(60, 60))
startIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/start.png"), size=(220, 120))
menuIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/menuIcon.png"), size=(60, 60))

buttonFont = ctk.CTkFont(family="Inter", size=50, weight="bold")

class MainWindow(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        self.pack_propagate(0) 
        self.configure(width=480, height=800, fg_color="black")

        signOutButton= ctk.CTkButton(self, 
                                     text="",
                                     image=signOutIcon,
                                     corner_radius=30,
                                     fg_color="transparent",
                                     hover_color="#1E272C",
                                     width=40,
                                     height=60,
                                     command=lambda: master.switch_frame("ShutdownWindow")
                                     )  
        signOutButton.place(relx=0.73, rely=0.02)

        menuButton = ctk.CTkButton(self, 
                                   text="",
                                   image=menuIcon,
                                   corner_radius=30,
                                   fg_color="transparent",
                                   hover_color="#1E272C",
                                   width=20,
                                   height=20,
                                   command=lambda: master.switch_frame("SelectDatabase")
                                   )
        menuButton.place(relx=0.025, rely=0.02)
        
        logoIconLabel = ctk.CTkLabel(self, 
                                     text="",
                                     fg_color="transparent",
                                     image = logoIcon
                                     )
        logoIconLabel.place(relx=0, rely=0.4)

        startButton = ctk.CTkButton(self,
                                    text="",
                                    image=startIcon,
                                    fg_color="transparent",
                                    hover_color="#1E272C",
                                    text_color="black",
                                    corner_radius=50,
                                    command=lambda: master.switch_frame("CusAvaWindow")
                                    )
        startButton.place(relx=0.25, rely=0.75)
        