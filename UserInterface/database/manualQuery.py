#!/usr/bin/env python3

import sqlite3
import os

import getpass
user = getpass.getuser()

dbPath = "/home/"+user+"/catkin_ws/src/astrochef/UserInterface/database/AstroChefDB.db"

conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

query = input("Enter query: ")

cursor.execute(query)
conn.commit()