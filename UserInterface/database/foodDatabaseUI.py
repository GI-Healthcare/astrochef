#!/usr/bin/env python3

import customtkinter as ctk
import rospy
from std_msgs.msg import String
import time
import os
from PIL import Image
import tkinter as tk
from tkinter import ttk
import sqlite3

import sys
sys.path.append('..')
from app import App

import getpass
user = getpass.getuser()

buttonColour = "#1E272C"
backIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/back.png"), size=(60, 60))
homeIcon = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/icons/home.png"), size=(60, 60))
DatabaseLogo = ctk.CTkImage(dark_image=Image.open("/home/"+user+"/catkin_ws/src/astrochef/UserInterface/Images/logo/databaseLogo.png"), size=(280, 70))

buttonFont = ctk.CTkFont(family="Inter", size=20, weight="bold")
labelFont = ctk.CTkFont(family="Inter", size=20, weight="bold")

dbPath = "/home/"+user+"/catkin_ws/src/astrochef/UserInterface/database/AstroChefDB.db"
table = "food"

class FoodDatabaseWindow(ctk.CTkFrame):
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
                                   command=lambda: master.switch_frame("SelectDatabase")
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

        databaseLogoLabel = ctk.CTkLabel(self, 
                                         text="",
                                         fg_color="transparent",
                                         image = DatabaseLogo
                                         )
        databaseLogoLabel.place(relx=0.2, rely=0.02)

        self.carbs = ctk.CTkLabel(self, text="Food", font=labelFont)
        self.carbs.place(relx=0.45, rely=0.10)

        ############# add database data here ##############

        self.idLabel = ctk.CTkLabel(self, text="ID", font=labelFont)
        self.idLabel.place(relx=0.05, rely=0.15)
        self.entryId = ctk.CTkEntry(self, width=250, height=25, font=('Arial bold', 15))
        self.entryId.place(relx=0.45, rely=0.15)

        self.foodName = ctk.CTkLabel(self, text="Food Name", font=labelFont)
        self.foodName.place(relx=0.05, rely=0.2)
        self.entryFoodName = ctk.CTkEntry(self, width=250, height=25, font=('Arial bold', 15))
        self.entryFoodName.place(relx=0.45, rely=0.2)

        self.foodLink = ctk.CTkLabel(self, text="Food Link", font=labelFont)
        self.foodLink.place(relx=0.05, rely=0.25)
        self.entryFoodLink = ctk.CTkEntry(self, width=250, height=25, font=('Arial bold', 15))
        self.entryFoodLink.place(relx=0.45, rely=0.25)

        self.calories = ctk.CTkLabel(self, text="Calories", font=labelFont)
        self.calories.place(relx=0.05, rely=0.30)
        self.entryCalories = ctk.CTkEntry(self, width=250, height=25, font=('Arial bold', 15))
        self.entryCalories.place(relx=0.45, rely=0.30)

        self.fat = ctk.CTkLabel(self, text="Fat", font=labelFont)
        self.fat.place(relx=0.05, rely=0.35)
        self.entryFat = ctk.CTkEntry(self, width=250, height=25, font=('Arial bold', 15))
        self.entryFat.place(relx=0.45, rely=0.35)

        self.carbs = ctk.CTkLabel(self, text="Carbs", font=labelFont)
        self.carbs.place(relx=0.05, rely=0.40)
        self.entryCarbs = ctk.CTkEntry(self, width=250, height=25, font=('Arial bold', 15))
        self.entryCarbs.place(relx=0.45, rely=0.40)

        self.protein = ctk.CTkLabel(self, text="Protein", font=labelFont)
        self.protein.place(relx=0.05, rely=0.45)
        self.entryProtein = ctk.CTkEntry(self, width=250, height=25, font=('Arial bold', 15))
        self.entryProtein.place(relx=0.45, rely=0.45)

        self.my_tree = ttk.Treeview(self)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial bold', 10))

        column_width = 72
        self.my_tree['columns'] = ("ID", "Food Name", "Food Link", "Calories", "Fats", "Carbs", "Protein" )
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column("ID", anchor=tk.W, width=20)
        self.my_tree.column("Food Name", anchor=tk.W, width=column_width)
        self.my_tree.column("Food Link", anchor=tk.W, width=column_width)
        self.my_tree.column("Calories", anchor=tk.W, width=column_width)
        self.my_tree.column("Fats", anchor=tk.W, width=column_width)
        self.my_tree.column("Carbs", anchor=tk.W, width=column_width)
        self.my_tree.column("Protein", anchor=tk.W, width=column_width)

        self.my_tree.heading("ID", text="ID", anchor=tk.W)
        self.my_tree.heading("Food Name", text="Food Name", anchor=tk.W)
        self.my_tree.heading("Food Link", text="Food Link", anchor=tk.W)
        self.my_tree.heading("Calories", text="Calories", anchor=tk.W)
        self.my_tree.heading("Fats", text="Fats", anchor=tk.W)
        self.my_tree.heading("Carbs", text="Carbs", anchor=tk.W)
        self.my_tree.heading("Protein", text="Protein", anchor=tk.W)

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.reverse(self.read()):
            self.my_tree.insert(parent='', index='end', text="", values=(result), tag="orow")

        self.my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial bold', 7))
        self.my_tree.place(relx=0.03, rely=0.5)

        self.enterButton = ctk.CTkButton(self,
                                    text="Enter",
                                    font=buttonFont,
                                    border_width=3,
                                    width=100,
                                    height=30,
                                    border_color="white",
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    text_color="white",
                                    command=self.insert_data
                                    )
        self.enterButton.place(relx=0.05, rely=0.94)

        self.updateButton = ctk.CTkButton(self,
                                    text="Update",
                                    font=buttonFont,
                                    border_width=3,
                                    width=100,
                                    height=30,
                                    border_color="white",
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    text_color="white",
                                    command=self.update_data
                                    )
        self.updateButton.place(relx=0.4, rely=0.94)

        self.deleteButton = ctk.CTkButton(self,
                                    text="Delete",
                                    font=buttonFont,
                                    border_width=3,
                                    width=100,
                                    height=30,
                                    border_color="white",
                                    fg_color="transparent",
                                    hover_color=buttonColour,
                                    text_color="white",
                                    command=self.delete_data
                                    )
        self.deleteButton.place(relx=0.75, rely=0.94)

    def reverse(self, tuples):
        new_tup = tuples[::-1]
        return new_tup
    
    def insert(self, id, name, link, calories, fats, carbs, protein):
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table+""" (foodId TEXT, foodName TEXT, foodLink TEXT, calories TEXT, fats TEXT, carbs TEXT, protein TEXT)""")

        cursor.execute("INSERT INTO "+table+" VALUES ('" + str(id) + "','" + str(name) + "','" + str(link) + "','" + str(calories) + "','" + str(fats) + "','" + str(carbs) + "','" + str(protein) + "')")
        conn.commit()


    def delete(self, data):
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table+""" (foodId TEXT, foodName TEXT, foodLink TEXT, calories TEXT, fats TEXT, carbs TEXT, protein TEXT)""")

        cursor.execute("DELETE FROM "+table+" WHERE foodId = '" + str(data) + "'")
        conn.commit()


    def update(self, id, name, link, calories, fats, carbs, protein, idName):
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table+"""(foodId TEXT, foodName TEXT, foodLink TEXT, calories TEXT, fats TEXT, carbs TEXT, protein TEXT)""")

        cursor.execute("UPDATE "+table+" SET foodID = '" + str(id) + "', foodName = '" + str(name) + "', foodLink = '" + str(link) + "', calories = '" + str(calories) + "', fats = '" + str(fats) + "', carbs = '" + str(carbs) + "', protein = '" + str(protein) + "' WHERE foodId='"+str(idName)+"'")
        conn.commit()


    def read(self):
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table+""" (foodId TEXT, foodName TEXT, foodLink TEXT, calories TEXT, fats TEXT, carbs TEXT, protein TEXT)""")

        cursor.execute("SELECT * from "+table)
        results = cursor.fetchall()
        conn.commit()
        return results


    def insert_data(self):
        foodId = str(self.entryId.get())
        foodName = str(self.entryFoodName.get())
        foodLink = str(self.entryFoodLink.get())
        foodCalories = str(self.entryCalories.get())
        foodFat = str(self.entryFat.get())
        foodCarbs = str(self.entryCarbs.get())
        foodProtein = str(self.entryProtein.get())

        if foodId == "" or foodId == " ":
            print("Error Inserting Id")
        if foodName == "" or foodName == " ":
            print("Error Inserting Name")
        if foodLink == "" or foodLink == " ":
            print("Error Inserting Link")
        if foodCalories == "" or foodCalories == " ":
            print("Error Inserting Calories")
        if foodFat == "" or foodFat == " ":
            print("Error Inserting Fats")
        if foodCarbs == "" or foodCarbs == " ":
            print("Error Inserting Carbs")
        if foodProtein == "" or foodProtein == " ":
            print("Error Inserting Protein")
        else:
            self.insert(str(foodId), str(foodName), str(foodLink), str(foodCalories), str(foodFat), str(foodCarbs), str(foodProtein))
            fn = foodName.replace(" ", "")
            fileName = str(foodId)+"_"+str(fn)+".xml"
            path = "/home/"+user+"/catkin_ws/src/astrochef/UserInterface/database/Recipes/"+fileName
            try:
                file = open(path,"w+")
                file.write("<?xml version = \"1.0\" encoding = \"UTF-8\" ?>\n\n<start>\n\t<ingredients>\n\n\t<!--Add your ingredients here-->\n\n\t</ingredients>\n\n\t<recipe name = \""+fn+"\">\n\n\t<!--Start writing your recipe here-->\n\n\t</recipe>\n</start>")
                file.close()
            except:
                rospy.logerr("Recipe xml "+fileName+" already existing")

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.reverse(self.read()):
            self.my_tree.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")

        self.my_tree.tag_configure('orow', background='#EEEEEE')
        self.my_tree.place(relx=0.03, rely=0.5)
        


    def delete_data(self):
        selected_item = self.my_tree.selection()[0]
        foodId = str(self.my_tree.item(selected_item)['values'][0])
        foodName = str(self.my_tree.item(selected_item)['values'][1])
        self.delete(foodId)

        fn = foodName.replace(" ", "")
        fileName = str(foodId)+"_"+str(fn)+".xml"
        path = "/home/"+user+"/catkin_ws/src/astrochef/UserInterface/database/Recipes/"+fileName
        if os.path.exists(path):
            os.remove(path)
        else:
            rospy.logerr("Recipe xml "+fileName+" does not exist")

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.reverse(self.read()):
            self.my_tree.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")

        self.my_tree.tag_configure('orow', background='#EEEEEE')
        self.my_tree.place(relx=0.03, rely=0.5)
        

    def update_data(self):
        selected_item = self.my_tree.selection()[0]
        update_name = self.my_tree.item(selected_item)['values'][0]
        self.update(self.entryId.get(), self.entryFoodName.get(), self.entryFoodLink.get(), self.entryCalories.get(), self.entryFat.get(), self.entryCarbs.get(), self.entryProtein.get(), update_name)

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.reverse(self.read()):
            self.my_tree.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")

        self.my_tree.tag_configure('orow', background='#EEEEEE')
        self.my_tree.place(relx=0.03, rely=0.5)
       
