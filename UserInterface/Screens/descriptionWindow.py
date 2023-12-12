#!/usr/bin/env python3

import customtkinter as ctk
import rospy
from std_msgs.msg import String
import time
import os
from PIL import Image
import tkinter
import sqlite3
from io import BytesIO
import requests

import sys
sys.path.append('..')
from app import App

import getpass
user = getpass.getuser()

buttonColour = "#1E272C"
backIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/back.png"), size=(60, 60))
homeIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/home.png"), size=(60, 60))
DescriptionLogo = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/logo/descriptionLogo.png"), size=(280, 70))
dbPath = "/home/"+user+"/catkin_ws/src/astrochef/UserInterface/database/AstroChefDB.db"
labelFont = ctk.CTkFont(family="Inter", size=30, weight="bold", underline=True)
dataFont = ctk.CTkFont(family="Inter", size=20, weight="bold")

buttonFont = ctk.CTkFont(family="Inter", size=40, weight="bold")

class DescriptionWindow(ctk.CTkFrame):
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
                                   command=lambda: master.switch_frame("AvailableDishWindow")
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

        slotLogoLabel = ctk.CTkLabel(self, 
                                     text="",
                                     fg_color="transparent",
                                     image = DescriptionLogo
                                     )
        slotLogoLabel.place(relx=0.2, rely=0.02)

        ############# add slot data here ##############

        self.addDescription(master)

        ############# add slot data here ##############

        slotContinueButton = ctk.CTkButton(self,
                                           text="Continue",
                                           font=buttonFont,
                                           border_width=3,
                                           width=440,
                                           height=30,
                                           border_color="white",
                                           fg_color="transparent",
                                           hover_color=buttonColour,
                                           text_color="white",
                                           corner_radius=50,
                                           command=lambda: master.switch_frame("SlotWindow", foodID=self.foodID)
                                           )
        slotContinueButton.place(relx=0.04, rely=0.9)

    def addDescription(self, master):
        self.foodID = master.foodID
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS food(foodId TEXT, foodName TEXT, foodLink TEXT, calories TEXT, fats TEXT, carbs TEXT, protein TEXT)""")

        cursor.execute("SELECT * FROM food WHERE foodID="+str(self.foodID)+";")
        results = cursor.fetchall()
        conn.close()

        self.processData(results)

    def processData(self, data):
        for row in data:
            foodName = row[1]
            foodImageURL = row[2]
            response = requests.get(foodImageURL)
            img = Image.open(BytesIO(response.content))
            img = img.resize((300, 300), Image.ANTIALIAS)
            foodImage = ctk.CTkImage(dark_image=img, size=(300, 300))
            calories = row[3]
            fats  = row[4]
            carbs = row[5]
            protein = row[6]

        foodNameLabel = ctk.CTkLabel(self, 
                                     text=foodName,
                                     font=labelFont,
                                     fg_color="transparent",
                                     )
        foodNameLabel.place(relx=0.05, rely=0.12)

        foodImageLabel = ctk.CTkLabel(self, 
                                     text="",
                                     fg_color="transparent",
                                     image = foodImage
                                     )
        foodImageLabel.place(relx=0.19, rely=0.2)

        caloriesLabel = ctk.CTkLabel(self, text="Calories", font=dataFont,fg_color="transparent", )
        caloriesLabel.place(relx=0.22, rely=0.6)
        caloriesDataLabel = ctk.CTkLabel(self, text=(":   "+str(calories)+"gm"), font=dataFont,fg_color="transparent", )
        caloriesDataLabel.place(relx=0.52, rely=0.6)

        fatsLabel = ctk.CTkLabel(self, text="Fats", font=dataFont,fg_color="transparent", )
        fatsLabel.place(relx=0.22, rely=0.68)
        fatsDataLabel = ctk.CTkLabel(self, text=(":   "+str(fats)+"gm"), font=dataFont,fg_color="transparent", )
        fatsDataLabel.place(relx=0.52, rely=0.68)

        carbsLabel = ctk.CTkLabel(self, text="Carbs", font=dataFont,fg_color="transparent", )
        carbsLabel.place(relx=0.22, rely=0.76)
        carbsDataLabel = ctk.CTkLabel(self, text=(":   "+str(carbs)+"gm"), font=dataFont,fg_color="transparent", )
        carbsDataLabel.place(relx=0.52, rely=0.76)

        proteinLabel = ctk.CTkLabel(self, text="Protein", font=dataFont,fg_color="transparent", )
        proteinLabel.place(relx=0.22, rely=0.84)
        proteinDataLabel = ctk.CTkLabel(self, text=(":   "+str(protein)+"gm"), font=dataFont,fg_color="transparent", )
        proteinDataLabel.place(relx=0.52, rely=0.84)
