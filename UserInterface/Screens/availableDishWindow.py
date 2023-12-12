#!/usr/bin/env python3

import customtkinter as ctk
import rospy
from std_msgs.msg import String
import time
import os
from PIL import Image, ImageTk
from io import BytesIO
import tkinter
import sqlite3
import requests

import sys
sys.path.append('..')
from app import App

import getpass
user = getpass.getuser()

buttonColour = "#1E272C"
backIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/back.png"), size=(60, 60))
homeIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/home.png"), size=(60, 60))
RecipeLogo = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/logo/recipeLogo.png"), size=(280, 70))
dbPath = "/home/"+user+"/catkin_ws/src/astrochef/UserInterface/database/AstroChefDB.db"

buttonFont = ctk.CTkFont(family="Inter", size=40, weight="bold")
labelFont = ctk.CTkFont(family="Inter", size=20, weight="bold")

class AvailableDishWindow(ctk.CTkFrame):
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
                                   command=lambda: master.switch_frame("CusAvaWindow")
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

        availableLogoLabel = ctk.CTkLabel(self, 
                                        text="",
                                        fg_color="transparent",
                                        image = RecipeLogo
                                        )
        availableLogoLabel.place(relx=0.2, rely=0.02)

        ############# add available data here ##############

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=430, height=680)
        self.scrollable_frame.place(relx=0.03, rely=0.12)

        self.addFoodButtons(master)

        ############# add available data here ##############

    def addFoodButtons(self, master):
        i=0
        j=0
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS 
        food(foodId TEXT, foodName TEXT, foodLink TEXT, calories TEXT, fats TEXT, carbs TEXT, protein TEXT)""")

        cursor.execute("SELECT foodId,foodName,foodLink FROM food")
        results = cursor.fetchall()
        conn.close()

        for row in results:
            foodID = row[0]
            foodName = row[1]
            foodImageURL = row[2]
            response = requests.get(foodImageURL)
            img = Image.open(BytesIO(response.content))
            img = img.resize((150, 150), Image.ANTIALIAS)
            foodImage = ctk.CTkImage(dark_image=img, size=(150, 150))

            if j%2==0:
                i+=2
                j=0
            
            self.addFoodButton(foodID, foodName, foodImage, i, j, master)
            j+=1
            
    def addFoodButton(self, foodID, foodName, foodImage, row, column, master):
        foodButton = ctk.CTkButton(self.scrollable_frame,
                                    text="",
                                    width=50,
                                    height=50,
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    corner_radius=50,
                                    image=foodImage,
                                    command=lambda: master.switch_frame("DescriptionWindow", foodID=foodID)
                                    )
        foodButton.grid(row = row, column = column, pady = 2, padx = 2)

        foodLabel = ctk.CTkLabel(self.scrollable_frame, text=str(foodName), font=labelFont)
        foodLabel.grid(row = (row+1), column = column, pady = 2, padx = 2)
        
