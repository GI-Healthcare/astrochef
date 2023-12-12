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
AllergyLogo = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/logo/databaseLogo.png"), size=(280, 70))

buttonFont = ctk.CTkFont(family="Inter", size=30, weight="bold")

class SelectDatabase(ctk.CTkFrame):
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

        logoLabel = ctk.CTkLabel(self, 
                                        text="",
                                        fg_color="transparent",
                                        image = AllergyLogo
                                        )
        logoLabel.place(relx=0.2, rely=0.02)

        foodDatabase = ctk.CTkButton(self,
                                    text="Food Database",
                                    font=buttonFont,
                                    border_width=3,
                                    width=440,
                                    height=30,
                                    border_color="white",
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    text_color="white",
                                    corner_radius=50,
                                    command=lambda: master.switch_frame("FoodDatabaseWindow")
                                    )
        foodDatabase.place(relx=0.04, rely=0.2)

        vegetableDatabase = ctk.CTkButton(self,
                                    text="Vegetable Database",
                                    font=buttonFont,
                                    border_width=3,
                                    width=440,
                                    height=30,
                                    border_color="white",
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    text_color="white",
                                    corner_radius=50,
                                    command=lambda: master.switch_frame("VegetableDatabaseWindow")
                                    )
        vegetableDatabase.place(relx=0.04, rely=0.3)

        meatDatabase = ctk.CTkButton(self,
                                    text="Meat Database",
                                    font=buttonFont,
                                    border_width=3,
                                    width=440,
                                    height=30,
                                    border_color="white",
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    text_color="white",
                                    corner_radius=50,
                                    command=lambda: master.switch_frame("MeatDatabaseWindow")
                                    )
        meatDatabase.place(relx=0.04, rely=0.4)

        dairyDatabase = ctk.CTkButton(self,
                                    text="Dairy Database",
                                    font=buttonFont,
                                    border_width=3,
                                    width=440,
                                    height=30,
                                    border_color="white",
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    text_color="white",
                                    corner_radius=50,
                                    command=lambda: master.switch_frame("DairyDatabaseWindow")
                                    )
        dairyDatabase.place(relx=0.04, rely=0.5)

        allergyDatabase = ctk.CTkButton(self,
                                    text="Allergy Database",
                                    font=buttonFont,
                                    border_width=3,
                                    width=440,
                                    height=30,
                                    border_color="white",
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    text_color="white",
                                    corner_radius=50,
                                    command=lambda: master.switch_frame("AllergyDatabaseWindow")
                                    )
        allergyDatabase.place(relx=0.04, rely=0.6)

