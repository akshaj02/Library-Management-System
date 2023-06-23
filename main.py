import tkinter as tk
import subprocess

# Create a window object.
window = tk.Tk()
window.title("Library Management System")

# Set window size and position.
window.geometry("900x600")

# Create a canvas to place the image.
canvas = tk.Canvas(window, width=500, height=500)
canvas.pack()

#Make the background color white.
canvas.configure(bg="white")

# # Add an image to the canvas.
image = tk.PhotoImage(file="library.png")
canvas.create_image(0, 0, anchor='nw', image=image)

# Create a frame for the options.
options_frame = tk.Frame(window)
options_frame.pack(anchor="center", pady=20)

# Create the buttons.
def add_book():
    subprocess.call(["python", "Add_book.py"])

button_add_book = tk.Button(options_frame, text="Add Book", command=add_book)
button_add_book.pack(side="left", padx=10)

def checkout_book():
    subprocess.call(["python", "Checkout_book.py"])

button_checkout_book = tk.Button(options_frame, text="Check Out Book", command=checkout_book)
button_checkout_book.pack(side="left", padx=10)

def new_borrower():
    subprocess.call(["python", "New_Borrower.py"])

button_new_borrower = tk.Button(options_frame, text="New Borrow", command=new_borrower)
button_new_borrower.pack(side="left", padx=10)

def book_info():
    subprocess.call(["python", "Book_info.py"])

button_book_info = tk.Button(options_frame, text="Book Info", command=book_info)
button_book_info.pack(side="left", padx=10)

def book_loan():
    subprocess.call(["python", "Book_Loan_info.py"])

button_book_loan = tk.Button(options_frame, text="Book Loan Info", command=book_loan)
button_book_loan.pack(side="left", padx=10)

def late_fee():
    subprocess.call(["python", "Late_fee_View.py"])

button_late_fee = tk.Button(options_frame, text="Late Fee", command=late_fee)
button_late_fee.pack(side="left", padx=10)

def book_View():
    subprocess.call(["python", "Book_view.py"])

button_book_view = tk.Button(options_frame, text="Book View", command=book_View)
button_book_view.pack(side="left", padx=10)

# Run the program.
window.mainloop()
