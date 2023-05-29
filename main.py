import tkinter as tk
import mysql.connector
from datetime import datetime

import mysql.connector
dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE marvel")

connection = mysql.connector.connect(
    host="localhost",
    database="marvel",
    user="root",
    password="your_password",
)
if connection.is_connected():
    print("Connected to MySQL")

    create_table_query = """CREATE TABLE IF NOT EXISTS marvel_table (
                                ID INT,
                                MOVIE VARCHAR(255),
                                DATE DATE,
                                MCU_PHASE VARCHAR(255)
                            )"""
    cursor = connection.cursor()
    cursor.execute(create_table_query)

    with open("Marvel.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.strip().split()
            id = int(data[0])
            movie = data[1]
            try:
                date = datetime.strptime(data[2], "%B%d,%Y").date()
            except ValueError:

                date = datetime.strptime("January1,2000", "%B%d,%Y").date()
            phase = " ".join(data[3:])

            insert_query = "INSERT INTO marvel_table (ID, MOVIE, DATE, MCU_PHASE) VALUES (%s, %s, %s, %s)"
            values = (id, movie, date, phase)
            cursor.execute(insert_query, values)

    connection.commit()
    print("Table populated successfully.")
else:
    print("Failed to connect to MySQL.")


window = tk.Tk()
window.title("Marvel Database")
window.geometry("600x450")
window.resizable(False, False)

text_box = tk.Text(window, height=20, width=60)
text_box.pack()

dropdown_var = tk.StringVar(window)
dropdown = tk.OptionMenu(window, dropdown_var, "")
dropdown.pack()

def populate_dropdown():
    cursorObject.execute("USE marvel")

    cursorObject.execute("SELECT ID FROM marvel_table")
    ids = cursorObject.fetchall()

    dropdown["menu"].delete(0, "end")

    for id in ids:
        dropdown["menu"].add_command(label=id[0], command=tk._setit(dropdown_var, id[0]))

populate_dropdown()

def display_data():
    text_box.delete("1.0", tk.END)

    cursorObject.execute("USE marvel")

    cursorObject.execute("SELECT * FROM marvel_table WHERE ID = %s", (int(dropdown_var.get()),))
    result = cursorObject.fetchall()

    for row in result:
        text_box.insert(tk.END, f"ID: {row[0]}\n")
        text_box.insert(tk.END, f"Movie: {row[1]}\n")
        text_box.insert(tk.END, f"Date: {row[2]}\n")
        text_box.insert(tk.END, f"MCU Phase: {row[3]}\n")
        text_box.insert(tk.END, "--------------------\n")

def dropdown_changed(*args):
    display_data()

dropdown_var.trace("w", dropdown_changed)

def add_button_clicked():
    add_window = tk.Toplevel(window)

    add_window.title("Add Entry")

    add_text_box = tk.Text(add_window, height=1, width=50)
    add_text_box.pack()

    def ok_button_clicked():
        entry = add_text_box.get("1.0", tk.END).strip()

        data = entry.split()
        id = int(data[0])
        movie = data[1]
        date = datetime.strptime(data[2], "%B%d,%Y").date()
        phase = " ".join(data[3:])

        cursorObject.execute("INSERT INTO marvel_table (ID, MOVIE, DATE, MCU_PHASE) VALUES (%s, %s, %s, %s)",
                             (id, movie, date, phase))
        connection.commit()

        populate_dropdown()

        add_window.destroy()

    ok_button = tk.Button(add_window, text="Ok", command=ok_button_clicked)
    ok_button.pack()

    cancel_button = tk.Button(add_window, text="Cancel", command=add_window.destroy)
    cancel_button.pack()

add_button = tk.Button(window, text="Add", command=add_button_clicked)
add_button.pack()

def list_all_button_clicked():
    text_box.delete("1.0", tk.END)

    cursorObject.execute("USE marvel")

    cursorObject.execute("SELECT * FROM marvel_table")
    result = cursorObject.fetchall()

    for row in result:
        text_box.insert(tk.END, f"ID: {row[0]}\n")
        text_box.insert(tk.END, f"Movie: {row[1]}\n")
        text_box.insert(tk.END, f"Date: {row[2]}\n")
        text_box.insert(tk.END, f"MCU Phase: {row[3]}\n")
        text_box.insert(tk.END, "--------------------\n")

list_all_button = tk.Button(window, text="LIST ALL", command=list_all_button_clicked)
list_all_button.pack()

window.mainloop()