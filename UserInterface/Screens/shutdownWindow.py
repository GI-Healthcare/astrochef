#!/usr/bin/env python3

import customtkinter as ctk
import rospy
from std_msgs.msg import String
import subprocess
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
ShutdownLogo = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/logo/shutdownLogo.png"), size=(280, 70))
imageIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/shutdownIcon.png"), size=(200, 200))

buttonFont = ctk.CTkFont(family="Inter", size=40, weight="bold")

class ShutdownWindow(ctk.CTkFrame):
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
                                   command=lambda: master.switch_frame("SlotWindow")
                                   )
        backButton.place(relx=0.025, rely=0.02)

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

        shutdownIconLabelLabel = ctk.CTkLabel(self, 
                                              text="",
                                              fg_color="transparent",
                                              image = ShutdownLogo
                                              )
        shutdownIconLabelLabel.place(relx=0.2, rely=0.02)

        imageIconLabel = ctk.CTkLabel(self, 
                                      text="",
                                      fg_color="transparent",
                                      image = imageIcon
                                      )
        imageIconLabel.place(relx=0.3, rely=0.2)

        shutdownYesButton = ctk.CTkButton(self,
                                          text="Yes",
                                          font=buttonFont,
                                          border_width=3,
                                          width=200,
                                          height=30,
                                          border_color="white",
                                          fg_color="transparent",
                                          hover_color=buttonColour,
                                          text_color="white",
                                          corner_radius=50,
                                          command=lambda: self.quitApplication(master)
                                              )
        shutdownYesButton.place(relx=0.3, rely=0.6)

        shutdownCancelButton = ctk.CTkButton(self,
                                             text="Cancel",
                                             font=buttonFont,
                                             border_width=3,
                                             width=200,
                                             height=30,
                                             border_color="white",
                                             fg_color="transparent",
                                             hover_color=buttonColour,
                                             text_color="white",
                                             corner_radius=50,
                                             command=lambda: master.switch_frame("MainWindow")
                                             )
        shutdownCancelButton.place(relx=0.3, rely=0.75)

    def quitApplication(self, master):
        # sudo apt-get install xdotool
        master.destroy()
        subprocess.run(["xdotool", "key", "ctrl+c"])