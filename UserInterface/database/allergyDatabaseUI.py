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
table = "allergy"

class AllergyDatabaseWindow(ctk.CTkFrame):
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

        self.carbs = ctk.CTkLabel(self, text="Allergy", font=labelFont)
        self.carbs.place(relx=0.35, rely=0.10)

        ############# add database data here ##############

        self.idLabel = ctk.CTkLabel(self, text="ID", font=labelFont)
        self.idLabel.place(relx=0.05, rely=0.15)
        self.entryId = ctk.CTkEntry(self, width=250, height=25, font=('Arial bold', 15))
        self.entryId.place(relx=0.45, rely=0.15)

        self.inventoryName = ctk.CTkLabel(self, text="Allergy Name", font=labelFont)
        self.inventoryName.place(relx=0.05, rely=0.2)
        self.entryinventoryName = ctk.CTkEntry(self, width=250, height=25, font=('Arial bold', 15))
        self.entryinventoryName.place(relx=0.45, rely=0.2)

        self.my_tree = ttk.Treeview(self)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial bold', 10))

        column_width = 400
        self.my_tree['columns'] = ("ID", "Allergy Name")
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column("ID", anchor=tk.W, width=20)
        self.my_tree.column("Allergy Name", anchor=tk.W, width=column_width)

        self.my_tree.heading("ID", text="ID", anchor=tk.W)
        self.my_tree.heading("Allergy Name", text="Allergy Name", anchor=tk.W)

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
    
    def insert(self, id, name):
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table+""" (allergyId TEXT, allergyName TEXT)""")

        cursor.execute("INSERT INTO "+table+" VALUES ('" + str(id) + "','" + str(name) + "')")
        conn.commit()


    def delete(self, data):
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table+""" (allergyId TEXT, allergyName TEXT)""")

        cursor.execute("DELETE FROM "+table+" WHERE allergyId = '" + str(data) + "'")
        conn.commit()


    def update(self, id, name, idName):
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table+""" (allergyId TEXT, allergyName TEXT)""")

        cursor.execute("UPDATE "+table+" SET allergyId = '" + str(id) + "', allergyName = '" + str(name) + "' WHERE allergyId='"+str(idName)+"'")
        conn.commit()


    def read(self):
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS """+table+""" (allergyId TEXT, allergyName TEXT)""")

        cursor.execute("SELECT * from "+table)
        results = cursor.fetchall()
        conn.commit()
        return results


    def insert_data(self):
        inventoryId = str(self.entryId.get())
        inventoryName = str(self.entryinventoryName.get())

        if inventoryId == "" or inventoryId == " ":
            print("Error Inserting Id")
        if inventoryName == "" or inventoryName == " ":
            print("Error Inserting Name")
        else:
            self.insert(str(inventoryId), str(inventoryName))

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.reverse(self.read()):
            self.my_tree.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")

        self.my_tree.tag_configure('orow', background='#EEEEEE')
        self.my_tree.place(relx=0.03, rely=0.5)
        


    def delete_data(self):
        selected_item = self.my_tree.selection()[0]
        deleteData = str(self.my_tree.item(selected_item)['values'][0])
        self.delete(deleteData)

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.reverse(self.read()):
            self.my_tree.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")

        self.my_tree.tag_configure('orow', background='#EEEEEE')
        self.my_tree.place(relx=0.03, rely=0.5)
        

    def update_data(self):
        selected_item = self.my_tree.selection()[0]
        update_name = self.my_tree.item(selected_item)['values'][0]
        self.update(self.entryId.get(), self.entryinventoryName.get(), update_name)

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.reverse(self.read()):
            self.my_tree.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")

        self.my_tree.tag_configure('orow', background='#EEEEEE')
        self.my_tree.place(relx=0.03, rely=0.5)
       
