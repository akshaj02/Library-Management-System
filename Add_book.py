from sqlite3 import Connection, Cursor
import tkinter as tk

# Create a window object.

connection = Connection("library.db")
cursor = connection.cursor()

add_book_window = tk.Tk()
add_book_window.title("Add Book")

# Set window size and position.
add_book_window.geometry("700x600+400+50")

# Add labels and text boxes to the window.
label_book_title = tk.Label(add_book_window, text="Book Title")
label_book_title.pack(pady=10)
text_book_title = tk.Entry(add_book_window)
text_book_title.pack()

label_publisher = tk.Label(add_book_window, text="Publisher")
label_publisher.pack(pady=10)
text_publisher = tk.Entry(add_book_window)
text_publisher.pack()

label_author = tk.Label(add_book_window, text="Author")
label_author.pack(pady=10)
text_author = tk.Entry(add_book_window)
text_author.pack()

button_submit = tk.Button(add_book_window, text="Submit ✔")
button_submit.pack(pady=20)

button_back = tk.Button(add_book_window, text="Back")
button_back.pack(pady=10)
button_back.config(command=add_book_window.destroy)


def add_book():
    # Get the book title, author, and publisher from the text boxes.
    book_title = text_book_title.get()
    author = text_author.get()
    publisher = text_publisher.get()

    # Get the book id of the book just added
    cursor.execute("SELECT count(*) FROM book")
    result = cursor.fetchone()[0]
    book_id = result

    # Add the book to the database.
    sql = """
    INSERT INTO book (book_id, title, publisher_name)
    VALUES (?, ?, ?)
    """
    cursor.execute(sql, (book_id, book_title, publisher))
    connection.commit()

    # Add the author of the book to the database.
    sql = """
    INSERT INTO book_authors (book_id, author_name)
    VALUES (?, ?)
    """
    cursor.execute(sql, (book_id, author))
    connection.commit()

    # Get the total number of branches
    cursor.execute("SELECT COUNT(*) FROM library_branch")
    result = cursor.fetchone()
    total_branches = result[0]

    # Add the book copies to all branches with 5 copies for each branch
    copies = 5
    for branch_id in range(1, total_branches + 1):
        sql = """
        INSERT INTO book_copies (book_id, branch_id, no_of_copies)
        VALUES (?, ?, ?)
        """
        cursor.execute(sql, (book_id, branch_id, copies))
        connection.commit()

    # messagebox.showinfo("Success", f"Book added successfully to all {total_branches} branches")
    # Display the results using text_result.
    text_result = tk.Text(add_book_window, height=5, width=70)
    text_result.pack(pady=20)
    text_result.insert(tk.END, f"Book added successfully to all {total_branches} branches")
    
        
button_submit.config(command=add_book)

# Run the program.
add_book_window.mainloop()