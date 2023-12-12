#!/usr/bin/env python3

import customtkinter as ctk
import rospy
from std_msgs.msg import String
import time
import os
from PIL import Image
import tkinter
import openai
import re

import sys
sys.path.append('..')
from app import App

import getpass
user = getpass.getuser()

buttonColour = "#1E272C"
backIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/back.png"), size=(60, 60))
homeIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/home.png"), size=(60, 60))
RecipeLogo = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/logo/recipeLogo.png"), size=(280, 70))

buttonFont = ctk.CTkFont(family="Inter", size=40, weight="bold")
labelFont = ctk.CTkFont(family="Inter", size=17, weight="bold")

class ChatGPTWindow(ctk.CTkFrame):
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
                                   command=lambda: master.switch_frame("AllergyWindow", inventory=master.inventory)
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

        chatGPTLogoLabel = ctk.CTkLabel(self, 
                                        text="",
                                        fg_color="transparent",
                                        image = RecipeLogo
                                        )
        chatGPTLogoLabel.place(relx=0.2, rely=0.02)

        ############# add chatGPT data here ############## (chatgpt not working quota limitation)


        #recipeNameLabel = ctk.CTkLabel(self, 
        #                               width=350,
        #                               text=self.recipeName,
        #                                fg_color="transparent",
        #                                wraplength=300, 
        #                                justify="center"
        #                                )
        #recipeNameLabel.place(relx=0.1, rely=0.2)

       

        ############# add chatGPT data here ##############

        chatGPTContinueButton = ctk.CTkButton(self,
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
                                              command=lambda: master.switch_frame("SlotWindow")
                                              )
        chatGPTContinueButton.place(relx=0.04, rely=0.9)

    def chatGPTQuery(self, master):
        inventoryDict = master.inventory
        vegetable  = ""
        meat = ""
        dairy = ""
        allergy = ""

        if "vegetable" in inventoryDict:
            l = inventoryDict["vegetable"]
            if not l:
                vegetable = ""
            else:
                vegetable = ','.join(l)

        if "meat" in inventoryDict:
            l = inventoryDict["meat"]
            if not l:
                meat = ""
            else:
                meat = ','.join(l)

        if "dairy" in inventoryDict:
            l = inventoryDict["dairy"]
            if not l:
                dairy = ""
            else:
                dairy = ','.join(l)

        if "allergy" in inventoryDict:
            l = inventoryDict["allergy"]
            if not l:
                allergy = "no allergy"
            else:
                allergy = ','.join(l)

        elif "allergy" not in inventoryDict:
            allergy = "no allergy"

        else:
            pass

        query = "Give a name to a recipe and write the steps to make a recipe with "+vegetable+" , "+meat+" , "+dairy+" and with allergy to "+allergy+" and give the nutritional values like calories, fats, carbohydrates, protein, sugar for 100gms of the food in vertical colon separated format"

        return query
    



