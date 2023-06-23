import datetime
import random
from sqlite3 import Connection, Cursor
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

# Create a window object.

connection = Connection("library.db")
cursor = connection.cursor()

new_borrower_window = tk.Tk()
new_borrower_window.title("New Borrower")

# Set window size and position.
new_borrower_window.geometry("700x600+400+50")

# Add labels and text boxes to the window.
label_borrower_name = tk.Label(new_borrower_window, text="Borrower Name")
label_borrower_name.pack(pady=10)
text_borrower_name = tk.Entry(new_borrower_window)
text_borrower_name.pack()

label_borrower_address = tk.Label(new_borrower_window, text="Borrower Address")
label_borrower_address.pack(pady=10)
text_address = tk.Entry(new_borrower_window)
text_address.pack()

label_borrower_phone = tk.Label(new_borrower_window, text="Borrower Phone")
label_borrower_phone.pack(pady=10)
text_phone = tk.Entry(new_borrower_window)
text_phone.pack()

button_checkout = tk.Button(new_borrower_window, text="Submit ✔")
button_checkout.pack(pady=20)

button_back = tk.Button(new_borrower_window, text="Back")
button_back.pack(pady=10)
button_back.config(command=new_borrower_window.destroy)
# Get the book title and borrower ID from the text boxes.


def add_borrower():
    # Get the borrower name, address, and phone from the text boxes.
    borrower_name = text_borrower_name.get()
    address = text_address.get()
    phone = text_phone.get()
    
    #Change phone number to - format
    phone = phone[:3] + "-" + phone[3:6] + "-" + phone[6:]

    # Generate a random 6-digit card number and check if it already exists in the database.
    while True:
        card_no = random.randint(100000, 999999)
        sql = "SELECT COUNT(*) FROM BORROWER WHERE Card_No = ?"
        cursor.execute(sql, (card_no,))
        if cursor.fetchone()[0] == 0:
            break

    # Add the borrower to the database with the generated card number.
    sql = """
    INSERT INTO BORROWER (Card_No, Name, Address, Phone) 
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(sql, (card_no, borrower_name, address, phone))
    connection.commit()

    text_result = tk.Text(new_borrower_window, height=5, width=70)
    text_result.pack(pady=10)
    text_result.insert(tk.END, f"Borrower added successfully. Card number: {card_no}")
     
        
button_checkout.config(command=add_borrower)

# Run the program.
new_borrower_window.mainloop()