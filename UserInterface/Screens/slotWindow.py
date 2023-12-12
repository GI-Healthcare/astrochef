#!/usr/bin/env python3

import customtkinter as ctk
import os
from PIL import Image
import rospy
from std_msgs.msg import String
import tkinter
import xml.etree.ElementTree as ET

import sys
sys.path.append('..')
from app import App

import getpass
user = getpass.getuser()

buttonColour = "#1E272C"
backIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/back.png"), size=(60, 60))
homeIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/home.png"), size=(60, 60))
SlotLogo = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/logo/slotsLogo.png"), size=(280, 70))

buttonFont = ctk.CTkFont(family="Inter", size=40, weight="bold")
labelFont = ctk.CTkFont(family="Inter", size=20, weight="bold")

class SlotWindow(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        self.pack_propagate(0) 
        self.configure(width=480, height=800, fg_color="black")

        backFrame = ""
        if master.previousFrame == "ChatGPTWindow":
            backFrame = "ChatGPTWindow"
        else: 
            backFrame = "DescriptionWindow"

        backButton = ctk.CTkButton(self, 
                                   text="",
                                   image=backIcon,
                                   corner_radius=10,
                                   width=20,
                                   height=20,
                                   fg_color="transparent",
                                   hover_color="#1E272C",
                                   command=lambda: master.switch_frame(backFrame, foodID=master.foodID)
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
                                     image = SlotLogo
                                     )
        slotLogoLabel.place(relx=0.2, rely=0.02)

        ############# add slot data here ##############

        path = "/home/"+user+"/catkin_ws/src/astrochef/UserInterface/database/Recipes/"
        fn = [filename for filename in os.listdir(path) if filename.startswith(master.foodID)]
        filePath = path+fn[0]
        try:
            tree = ET.parse(filePath)
            root = tree.getroot()
            for ingredients in root.findall("ingredients"):
                x = 0
                for items in ingredients:
                    text = "Slot: "+items.attrib["id"]+" - "+items.attrib["name"]
                    ingredientLabel = ctk.CTkLabel(self, text=text, font=labelFont)
                    ingredientLabel.place(relx=0.05, rely=0.15+x)
                    x+=0.05
                    #print(items.attrib["id"], items.attrib["name"])
        except:
            rospy.logerr("Unable to open "+filePath)
        
        ############# add slot data here ##############

        slotContinueButton = ctk.CTkButton(self,
                                           text="Start Coooking",
                                           font=buttonFont,
                                           border_width=3,
                                           width=440,
                                           height=30,
                                           border_color="white",
                                           fg_color="transparent",
                                           hover_color=buttonColour,
                                           text_color="white",
                                           corner_radius=50,
                                           command=lambda: master.startCooking(foodID=master.foodID)
                                           )
        slotContinueButton.place(relx=0.04, rely=0.9)
