from sqlite3 import Connection, Cursor
import tkinter as tk

# Create a window object.

connection = Connection("library.db")
cursor = connection.cursor()

Book_Loan_info_window = tk.Tk()
Book_Loan_info_window.title("Book Loan Info")

# Set window size and position.
Book_Loan_info_window.geometry("700x600+400+50")

# Add labels and text boxes to the window.
label_start_date = tk.Label(Book_Loan_info_window, text="Start Date")
label_start_date.pack(pady=10)
text_start_date = tk.Entry(Book_Loan_info_window)
text_start_date.pack()

label_end_date = tk.Label(Book_Loan_info_window, text="End Date")
label_end_date.pack(pady=10)
text_end_date = tk.Entry(Book_Loan_info_window)
text_end_date.pack()

button_submit = tk.Button(Book_Loan_info_window, text="Submit ✔")
button_submit.pack(pady=20)

button_back = tk.Button(Book_Loan_info_window, text="Back")
button_back.pack(pady=10)
button_back.config(command=Book_Loan_info_window.destroy)

# Get the book title and borrower ID from the text boxes.

def list_late_book_loans():
    # Connect to the database
    start_date = text_start_date.get()
    end_date = text_end_date.get()

    # Execute the SQL query to get the late book loans
    sql = """
    SELECT book_loans.Book_Id, book.Title, borrower.Name, julianday(book_loans.Due_Date) - julianday(book_loans.Returned_Date) as days_late
    FROM book_loans
    JOIN book ON book_loans.Book_Id = book.Book_Id
    JOIN borrower ON book_loans.Card_No = borrower.Card_No
    WHERE book_loans.Returned_Date > book_loans.Due_Date AND
    book_loans.Due_Date >= ? AND book_loans.Due_Date <= ?
    """
    cursor.execute(sql, (start_date, end_date))
    results = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Add a Text widget to the window to display the results.
    text_results = tk.Text(Book_Loan_info_window)
    text_results.pack(pady=20)

    # Print the results
    text_results.delete(1.0, tk.END)
    text_results.insert(tk.END, f"Late Book Loans between {start_date} and {end_date}:\n")
    for result in results:
        book_id = result[0]
        title = result[1]
        borrower_name = result[2]
        days_late = result[3] * -1.0
        text_results.insert(tk.END, f"\nBook ID: {book_id}, \nTitle: {title}, \nBorrower: {borrower_name}, \nDays Late: {days_late} days\n\n")
        
    
button_submit.config(command=list_late_book_loans)

# Run the program.
Book_Loan_info_window.mainloop()
