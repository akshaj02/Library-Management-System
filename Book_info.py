from sqlite3 import Connection, Cursor
import tkinter as tk

# Create a window object.

connection = Connection("library.db")
cursor = connection.cursor()

Book_info_window = tk.Tk()
Book_info_window.title("Book info")

# Set window size and position.
Book_info_window.geometry("700x600+400+50")

# Add labels and text boxes to the window.
label_book_title = tk.Label(Book_info_window, text="Book Title")
label_book_title.pack(pady=10)
text_book_title = tk.Entry(Book_info_window)
text_book_title.pack()

button_submit = tk.Button(Book_info_window, text="Submit ✔")
button_submit.pack(pady=20)

button_back = tk.Button(Book_info_window, text="Back")
button_back.pack(pady=10)
button_back.config(command=Book_info_window.destroy)
# Get the book title and borrower ID from the text boxes.

def book_info():
    
    book_title = text_book_title.get()
    # Execute the SQL query to get the number of copies loaned out per branch
    sql = """
    SELECT library_branch.branch_name, COUNT(book_loans.book_id) as num_copies_loaned
    FROM book_loans
    JOIN library_branch ON book_loans.branch_id = library_branch.branch_id
    JOIN book ON book_loans.book_id = book.book_id
    WHERE book.title = ?
    GROUP BY library_branch.branch_name
    """
    cursor.execute(sql, (book_title,))
    results = cursor.fetchall()

    text_results = tk.Text(Book_info_window, height=7, width=70)
    text_results.pack(pady=10)
    text_results.insert(tk.END, f"Book Title: {book_title}\n\n")
    for i, result in enumerate(results):
        branch_name = result[0]
        num_copies_loaned = result[1]
        text_results.insert(tk.END, f"Branch Name: {branch_name}\n")
        text_results.insert(tk.END, f"Copies Loaned: {num_copies_loaned}\n\n")
        
button_submit.config(command=book_info)


# Run the program.
Book_info_window.mainloop()