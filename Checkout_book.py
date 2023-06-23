import datetime
from sqlite3 import Connection, Cursor
import tkinter as tk
from tkinter import messagebox

# Create a window object.

connection = Connection("library.db")
cursor = connection.cursor()

checkout_window = tk.Tk()
checkout_window.title("Checkout Book")

# Set window size and position.
checkout_window.geometry("700x600+400+50")

# Add labels and text boxes to the window.
label_book_title = tk.Label(checkout_window, text="Book Title")
label_book_title.pack(pady=10)
text_book_title = tk.Entry(checkout_window)
text_book_title.pack()

label_borrower_id = tk.Label(checkout_window, text="Borrower ID")
label_borrower_id.pack(pady=10)
text_borrower_id = tk.Entry(checkout_window)
text_borrower_id.pack()

label_branch_id = tk.Label(checkout_window, text="Branch ID")
label_branch_id.pack(pady=10)
text_branch_id = tk.Entry(checkout_window)
text_branch_id.pack()

button_checkout = tk.Button(checkout_window, text="Check Out")
button_checkout.pack(pady=20)

button_back = tk.Button(checkout_window, text="Back")
button_back.pack(pady=10)
button_back.config(command=checkout_window.destroy)
# Get the book title and borrower ID from the text boxes.


def check_out_book():
    
    # Get the book title and borrower ID from the text boxes.
    book_title = text_book_title.get()
    borrower_id = text_borrower_id.get()
    branch_id = text_branch_id.get()

    # Ask the user for the branch id of the library.
    # Check if the book is available in the branch.
    sql = """
    SELECT book_copies.no_of_copies, COUNT(book_loans.book_id), book.book_id
    FROM book_copies
    LEFT JOIN book_loans ON book_copies.book_id = book_loans.book_id AND book_copies.branch_id = book_loans.branch_id
    JOIN book ON book_copies.book_id = book.book_id
    WHERE book.title = ? AND book_copies.branch_id = ?
    GROUP BY book_copies.book_id
    """
    cursor.execute(sql, (book_title, branch_id))
    result = cursor.fetchone()

    if not result:
        messagebox.showerror("Error", "Book is not available in the selected branch")
        return

    available_copies, checked_out_copies, book_id = result

    checked_out_copies += 1

    if available_copies == checked_out_copies:
        messagebox.showerror("Error", "All copies of the book are checked out")
        return

    # Check out the book from the library.
    due_date = datetime.date.today() + datetime.timedelta(days=7)
    sql = """
    INSERT INTO book_loans (book_id, branch_id, card_no, date_out, due_date)
    VALUES (?, ?, ?, CURRENT_DATE, ?)
    """
    try:
        cursor.execute(sql, (book_id, branch_id, borrower_id, due_date))
    except:
        messagebox.showerror("Error", "Book is already checked out by the borrower")
        return
    connection.commit()

    # Update the number of copies in the book_copies table.
    sql = """
    UPDATE book_copies SET no_of_copies = no_of_copies - 1
    WHERE book_id = ? AND branch_id = ?
    """
    cursor.execute(sql, (book_id, branch_id))
    connection.commit()

    # Show the updated number of copies in the book_copies table.
    sql = """
    SELECT no_of_copies FROM book_copies
    WHERE book_id = ? AND branch_id = ?
    """
    cursor.execute(sql, (book_id, branch_id))
    result = cursor.fetchone()

    if result:
        if result[0] == 0 or result[0] < 0:
            messagebox.showwarning("Warning", "No copies of the book are available in the branch")
            return
        else: 
            text_result = tk.Text(checkout_window, height=5, width=80)
            text_result.pack(pady=10)
            text_result.insert(tk.END, f"Book checked out successfully. Available copies: {result[0]}. Due date: {due_date}.")
    else:
        messagebox.showwarning("Warning", "Could not retrieve updated number of copies.")
        
button_checkout.config(command=check_out_book)


# Run the program.
checkout_window.mainloop()