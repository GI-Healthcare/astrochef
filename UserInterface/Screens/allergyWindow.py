#!/usr/bin/env python3

import customtkinter as ctk
import rospy
from std_msgs.msg import String
import time
import os
from PIL import Image, ImageTk
from io import BytesIO
import sqlite3

import sys
sys.path.append('..')
from app import App

import getpass
user = getpass.getuser()

buttonColour = "#1E272C"
backIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/back.png"), size=(60, 60))
homeIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/home.png"), size=(60, 60))
AllergyLogo = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/logo/allergyLogo.png"), size=(280, 70))
dbPath = "/home/"+user+"/catkin_ws/src/astrochef/UserInterface/database/AstroChefDB.db"
table1 = "allergy"


buttonFont = ctk.CTkFont(family="Inter", size=40, weight="bold")
labelFont = ctk.CTkFont(family="Inter", size=17, weight="bold")

class AllergyWindow(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        self.pack_propagate(0) 
        self.configure(width=480, height=800, fg_color="black")

        self.allergyButtonList =[] 

        backButton = ctk.CTkButton(self, 
                                   text="",
                                   image=backIcon,
                                   corner_radius=10,
                                   width=20,
                                   height=20,
                                   fg_color="transparent",
                                   hover_color="#1E272C",
                                   command=lambda: master.switch_frame("InventoryWindow", inventory=master.inventory)
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

        allergyLogoLabel = ctk.CTkLabel(self, 
                                        text="",
                                        fg_color="transparent",
                                        image = AllergyLogo
                                        )
        allergyLogoLabel.place(relx=0.2, rely=0.02)

        ############# add allergy data here ##############

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=430, height=580)
        self.scrollable_frame.place(relx=0.03, rely=0.12)

        self.addAllergyCheckboxs(master)


        ############# add allergy data here ##############

        allergyContinueButton = ctk.CTkButton(self,
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
                                              command=lambda: master.switch_frame("ChatGPTWindow", inventory=master.inventory)
                                              )
        allergyContinueButton.place(relx=0.04, rely=0.9)

    def addAllergyCheckboxs(self, master):
        i=0
        j=0
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table1+""" (allergyId TEXT, allergyName TEXT)""")

        cursor.execute("SELECT * FROM "+table1)
        results = cursor.fetchall()
        conn.close()

        for row in results:
            allergyID = row[0]
            allergyName = row[1]

            if j%2==0:
                i+=2
                j=0
            
            self.addAllergyCheckbox(allergyID, allergyName, i, j, master)
            j+=1
            
    def addAllergyCheckbox(self, allergyID, allergyName, row, column, master):
        self.allergyList = []
        allergyCheckbox = ctk.CTkCheckBox(self.scrollable_frame, 
                                          text=str(allergyName), 
                                          font=labelFont,
                                          command=lambda: self.allergyProcess(allergyID, allergyName, master)
                                          )
        allergyCheckbox.grid(row = (row+1), column = column, padx=50, pady=10, sticky='nsew')
        self.allergyButtonList.append(allergyCheckbox)

    def allergyProcess(self,allergyID, allergyName, master):

        if allergyName not in self.allergyList:
            self.allergyButtonList[int(allergyID)-1].cget("text")
            self.allergyList.append(allergyName)
        else:
            self.allergyButtonList[int(allergyID)-1].cget("text")
            self.allergyList.remove(allergyName)

        master.inventory["allergy"] = self.allergyList