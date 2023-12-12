#!/usr/bin/env python3

import customtkinter as ctk
import rospy
from std_msgs.msg import String
import sys
import time
import os

import getpass
user = getpass.getuser()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self._frame = None
        self.switch_frame("MainWindow")
        #self.attributes("-fullscreen", True)
        self.geometry("480x800")
        self.title("AstroChef")

        self.foodID = 0
        self.inventory = {}
        self.response = ""
        self.progressVal = 0

    def switch_frame(self, frame_name, foodID=0, inventory={}):
        self.foodID = foodID
        self.inventory = inventory
        
        if self._frame is not None:
            self._frame.destroy()

        if frame_name == "MainWindow":
            from Screens.mainWindow import MainWindow
            self._frame = MainWindow(self)

        elif frame_name == "CusAvaWindow":
            from Screens.cusAvaWindow import CusAvaWindow
            self._frame = CusAvaWindow(self)

        elif frame_name == "InventoryWindow":
            from Screens.inventoryWindow import InventoryWindow
            self._frame = InventoryWindow(self)

        elif frame_name == "AllergyWindow":
            from Screens.allergyWindow import AllergyWindow
            self._frame = AllergyWindow(self)

        elif frame_name == "ChatGPTWindow":
            from Screens.chatGPTWIndow import ChatGPTWindow
            self._frame = ChatGPTWindow(self)

        elif frame_name == "SlotWindow":
            from Screens.slotWindow import SlotWindow
            self._frame = SlotWindow(self)

        elif frame_name == "CookingWindow":
            from Screens.cookingWindow import CookingWindow
            self._frame = CookingWindow(self)

        elif frame_name == "DescriptionWindow":
            from Screens.descriptionWindow import DescriptionWindow
            self._frame = DescriptionWindow(self)

        elif frame_name == "AvailableDishWindow":
            from Screens.availableDishWindow import AvailableDishWindow
            self._frame = AvailableDishWindow(self)

        elif frame_name == "ShutdownWindow":
            from Screens.shutdownWindow import ShutdownWindow
            self._frame = ShutdownWindow(self)

        elif frame_name == "FoodDatabaseWindow":
            from database.foodDatabaseUI import FoodDatabaseWindow
            self._frame = FoodDatabaseWindow(self)

        elif frame_name == "VegetableDatabaseWindow":
            from database.vegatableDatabaseUI import VegetableDatabaseWindow
            self._frame = VegetableDatabaseWindow(self)

        elif frame_name == "MeatDatabaseWindow":
            from database.meatDatabaseUI import MeatDatabaseWindow
            self._frame = MeatDatabaseWindow(self)

        elif frame_name == "DairyDatabaseWindow":
            from database.dairyDatabaseUI import DairyDatabaseWindow
            self._frame = DairyDatabaseWindow(self)

        elif frame_name == "SelectDatabase":
            from Screens.selectDatabase import SelectDatabase
            self._frame = SelectDatabase(self)
        
        elif frame_name == "AllergyDatabaseWindow":
            from database.allergyDatabaseUI import AllergyDatabaseWindow
            self._frame = AllergyDatabaseWindow(self)

        else:
            raise ValueError(f"Unknown frame name: {frame_name}")
        
        self.previousFrame = frame_name

        self._frame.pack()

    def startCooking(self, foodID):
        #print(foodID)
        self.foodID = foodID
        self.status = "start"
        pub.publish(self.status)

        self.switch_frame("CookingWindow", foodID = foodID)

        self.status = str(self.foodID)+"_cooking"
        pub.publish(self.status)

    def cancelCooking(self):
        self.status = "abort"
        pub.publish(self.status)
        self.switch_frame("MainWindow")

    def setProgress(self, val):
        self.progressVal = val

    def getProgress(self):
        return self.progressVal

if __name__ == "__main__":
    rospy.loginfo(" ||=====|| ||====  =======  ||====||  ||====||       ||====  ||    || ||====  ||====")
    rospy.loginfo(" ||     || ||         ||    ||    ||  ||    ||       ||      ||    || ||      ||    ")
    rospy.loginfo(" ||=====|| ||===||    ||    ||====||  ||    ||  ===  ||      ||====|| ||===   ||=== ")
    rospy.loginfo(" ||     ||      ||    ||    ||   \\   ||    ||       ||      ||    || ||      ||    ")
    rospy.loginfo(" ||     ||  ====||    ||    ||    \\  ||====||       ||====  ||    || ||====  ||    ")

    rospy.loginfo("Initializing Application")
    rospy.init_node("User_Interface")
    pub = rospy.Publisher("ui_cmd", String, queue_size=1)

    app = App()
    app.mainloop()
