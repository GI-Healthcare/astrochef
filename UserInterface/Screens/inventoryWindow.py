#!/usr/bin/env python3

import customtkinter as ctk
import rospy
from std_msgs.msg import String
import time
import os
from PIL import Image, ImageTk
from io import BytesIO
import sqlite3
import requests
import tkinter as tk
from tkinter import ttk

import sys
sys.path.append('..')
from app import App

import getpass
user = getpass.getuser()

buttonColour = "#1E272C"
backIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/back.png"), size=(60, 60))
homeIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/home.png"), size=(60, 60))
InventoryLogo = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/logo/inventoryLogo.png"), size=(280, 70))
dbPath = "/home/"+user+"/catkin_ws/src/astrochef/UserInterface/database/AstroChefDB.db"
table1 = "vegetable"
table2 = "meat"
table3 = "dairy"

buttonFont = ctk.CTkFont(family="Inter", size=40, weight="bold")
tabFont = ctk.CTkFont(family="Inter", size=15, weight="bold")
labelFont = ctk.CTkFont(family="Inter", size=17, weight="bold")

class InventoryWindow(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        self.pack_propagate(0) 
        self.configure(width=480, height=800, fg_color="black")
        self.inventoryDict = dict()
        self.vegetableButtonList =[] 
        self.meatButtonList =[] 
        self.dairyButtonList =[] 

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

        inventoryLogoLabel = ctk.CTkLabel(self, 
                                          text="",
                                          fg_color="transparent",
                                          image = InventoryLogo
                                          )
        inventoryLogoLabel.place(relx=0.2, rely=0.02)

        ############# add inventory data here ##############

        scrollable_frame = ctk.CTkScrollableFrame(self, width=430, height=590)
        scrollable_frame.place(relx=0.03, rely=0.12)

        style = ttk.Style()
        style.configure("Vertical.TNotebook", tabposition="wn", background="black")
        style.configure("Vertical.TNotebook.Tab", background="#ff8503", foreground="black", font=tabFont)
        style.map("Vertical.TNotebook.Tab", background=[("selected", "#d53600")])

        notebook = ttk.Notebook(scrollable_frame, style="Vertical.TNotebook", width=430, height=590)
        notebook.pack(side="left", fill="both", expand=True)

         # create tabs
        vegetable = tk.Frame(notebook)
        meat = tk.Frame(notebook)
        dairy = tk.Frame(notebook)

        # add tabs to notebook
        notebook.add(vegetable, text="Vegetable")
        notebook.add(meat,      text="Meat     ")
        notebook.add(dairy,     text="Dairy    ")

        ############# add inventory data here ##############
        
        # Vegetable
        self.vegetableScrollFrame = ctk.CTkScrollableFrame(vegetable, width=430, height=680)
        self.vegetableScrollFrame.pack(side="left", fill="both", expand=True)
        self.addVegetableButtons(master)

        # Meat
        self.meatScrollFrame = ctk.CTkScrollableFrame(meat, width=430, height=680)
        self.meatScrollFrame.pack(side="left", fill="both", expand=True)
        self.addMeatButtons(master)

        # Dairy
        self.dairyScrollFrame = ctk.CTkScrollableFrame(dairy, width=430, height=680)
        self.dairyScrollFrame.pack(side="left", fill="both", expand=True)
        self.addDairyButtons(master)

        ############# add inventory data here ##############

        inventoryContinueButton = ctk.CTkButton(self,
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
                                                command=lambda: master.switch_frame("AllergyWindow", inventory=self.inventoryDict)
                                                )
        inventoryContinueButton.place(relx=0.04, rely=0.9)

    def addVegetableButtons(self, master):
        i=0
        j=0
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table1+""" (inventoryId TEXT, inventoryName TEXT, inventoryLink TEXT)""")

        cursor.execute("SELECT * FROM "+table1)
        results = cursor.fetchall()
        conn.close()

        for row in results:
            inventoryID = row[0]
            inventoryName = row[1]
            inventoryImageURL = row[2]
            response = requests.get(inventoryImageURL)
            img = Image.open(BytesIO(response.content))
            img = img.resize((150, 150), Image.ANTIALIAS)
            inventoryImage = ctk.CTkImage(dark_image=img, size=(125, 125))

            if j%2==0:
                i+=2
                j=0
            
            self.addVegetableButton(inventoryID, inventoryName, inventoryImage, i, j, master)
            j+=1       
    
    def addVegetableButton(self, inventoryID, inventoryName, inventoryImage, row, column, master):
        self.vegetableList = []
        vegetableButton = ctk.CTkButton(self.vegetableScrollFrame,
                                    text="",
                                    width=30,
                                    height=30,
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    corner_radius=50,
                                    image=inventoryImage,
                                    command=lambda: self.vegetableProcess(inventoryID, inventoryName)
                                    )
        vegetableButton.grid(row = row, column = column, pady = 2, padx = 2)

        self.vegetableButtonList.append(vegetableButton)

        foodLabel = ctk.CTkLabel(self.vegetableScrollFrame, text=str(inventoryName), font=labelFont)
        foodLabel.grid(row = (row+1), column = column, pady = 2, padx = 2)

    def vegetableProcess(self,vegetableID, vegetableName):
        if vegetableName not in self.vegetableList:
            self.vegetableButtonList[int(vegetableID)-1].configure(fg_color="orange", hover_color="orange")
            self.vegetableList.append(vegetableName)
        else:
            self.vegetableButtonList[int(vegetableID)-1].configure(fg_color="transparent", hover_color=buttonColour)
            self.vegetableList.remove(vegetableName)

        self.inventoryDict["vegetable"] = self.vegetableList

    def addMeatButtons(self, master):
        i=0
        j=0
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table2+""" (inventoryId TEXT, inventoryName TEXT, inventoryLink TEXT)""")

        cursor.execute("SELECT * FROM "+table2)
        results = cursor.fetchall()
        conn.close()

        for row in results:
            inventoryID = row[0]
            inventoryName = row[1]
            inventoryImageURL = row[2]
            response = requests.get(inventoryImageURL)
            img = Image.open(BytesIO(response.content))
            img = img.resize((150, 150), Image.ANTIALIAS)
            inventoryImage = ctk.CTkImage(dark_image=img, size=(125, 125))

            if j%2==0:
                i+=2
                j=0
            
            self.addMeatButton(inventoryID, inventoryName, inventoryImage, i, j, master)
            j+=1
            
    def addMeatButton(self, inventoryID, inventoryName, inventoryImage, row, column, master):
        self.meatList = []
        meatButton = ctk.CTkButton(self.meatScrollFrame,
                                    text="",
                                    width=30,
                                    height=30,
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    corner_radius=50,
                                    image=inventoryImage,
                                    command=lambda: self.meatProcess(inventoryID, inventoryName)
                                    )
        meatButton.grid(row = row, column = column, pady = 2, padx = 2)

        self.meatButtonList.append(meatButton)
        
        foodLabel = ctk.CTkLabel(self.meatScrollFrame, text=str(inventoryName), font=labelFont)
        foodLabel.grid(row = (row+1), column = column, pady = 2, padx = 2)

    def meatProcess(self,meatID, meatName):
        if meatName not in self.meatList:
            self.meatButtonList[int(meatID)-1].configure(fg_color="orange", hover_color="orange")
            self.meatList.append(meatName)
        else:
            self.meatButtonList[int(meatID)-1].configure(fg_color="transparent", hover_color=buttonColour)
            self.meatList.remove(meatName)

        self.inventoryDict["meat"] = self.meatList
    
    def addDairyButtons(self, master):
        i=0
        j=0
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table3+""" (inventoryId TEXT, inventoryName TEXT, inventoryLink TEXT)""")

        cursor.execute("SELECT * FROM "+table3)
        results = cursor.fetchall()
        conn.close()

        for row in results:
            inventoryID = row[0]
            inventoryName = row[1]
            inventoryImageURL = row[2]
            response = requests.get(inventoryImageURL)
            img = Image.open(BytesIO(response.content))
            img = img.resize((150, 150), Image.ANTIALIAS)
            inventoryImage = ctk.CTkImage(dark_image=img, size=(125, 125))

            if j%2==0:
                i+=2
                j=0
            
            self.addDairyButton(inventoryID, inventoryName, inventoryImage, i, j, master)
            j+=1
            
    def addDairyButton(self, inventoryID, inventoryName, inventoryImage, row, column, master):
        self.dairyList = []
        dairyButton = ctk.CTkButton(self.dairyScrollFrame,
                                    text="",
                                    width=30,
                                    height=30,
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    corner_radius=50,
                                    image=inventoryImage,
                                    command=lambda: self.dairyProcess(inventoryID, inventoryName)
                                    )
        dairyButton.grid(row = row, column = column, pady = 2, padx = 2)

        self.dairyButtonList.append(dairyButton)
        
        foodLabel = ctk.CTkLabel(self.dairyScrollFrame, text=str(inventoryName), font=labelFont)
        foodLabel.grid(row = (row+1), column = column, pady = 2, padx = 2)

    def dairyProcess(self,dairyID, dairyName):
        if dairyName not in self.dairyList:
            self.dairyButtonList[int(dairyID)-1].configure(fg_color="orange", hover_color="orange")
            self.dairyList.append(dairyName)
        else:
            self.dairyButtonList[int(dairyID)-1].configure(fg_color="transparent", hover_color=buttonColour)
            self.dairyList.remove(dairyName)

        self.inventoryDict["dairy"] = self.dairyList