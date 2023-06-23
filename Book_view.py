from sqlite3 import Connection, Cursor
import tkinter as tk

# Create a window object.
connection = Connection("library.db")
cursor = connection.cursor()

Book_view_window = tk.Tk()
Book_view_window.title("Book View")

# Set window size and position.
Book_view_window.geometry("700x600+400+50")

# Add labels and text boxes to the window.
label_book_info = tk.Label(Book_view_window, text="Enter Book ID, Book Title, Part of the Title or leave it blank to see all:")
label_book_info.pack(pady=10)
text_book_info = tk.Entry(Book_view_window)
text_book_info.pack()

button_submit = tk.Button(Book_view_window, text="Submit ✔")
button_submit.pack(pady=20)

button_back = tk.Button(Book_view_window, text="Back")
button_back.pack(pady=10)
button_back.config(command=Book_view_window.destroy)

# Get the book title and book ID from the text boxes.
def book_view(filter=None):
    filter = text_book_info.get()
    sql_query = '''
    SELECT 
        BOOK_LOANS.Book_Id AS Book_ID, 
        vBookLoanInfo.Book_Title AS Book_Title,
    CASE
        WHEN vBookLoanInfo.LateFeeBalance IS NULL THEN 'Non-Applicable'
        ELSE ('$' || printf("%.2f", LateFeeBalance))
    END AS Late_Fee
    FROM 
        vBookLoanInfo
        JOIN BOOK ON vBookLoanInfo.Book_Title = BOOK.Title
        JOIN BOOK_LOANS ON BOOK.Book_Id = BOOK_LOANS.Book_Id
    WHERE 
        vBookLoanInfo.Book_Title LIKE '%' || COALESCE(?, vBookLoanInfo.Book_Title) || '%'
        OR BOOK_LOANS.Book_Id = COALESCE(?, BOOK_LOANS.Book_Id)
    ORDER BY 
    LateFeeBalance DESC NULLS LAST;

    '''
    cursor.execute(sql_query, (filter, filter))
    results = []
    for row in cursor.fetchall():
        result = {}
        result['Book_ID'] = row[0]
        result['Book_Title'] = row[1]
        result['Late_Fee'] = row[2]
        results.append(result)
         
    
    #Display using text results
    text_results = tk.Text(Book_view_window, height=30, width=70)
    text_results.pack()
    text_results.insert(tk.END, "Book ID\t\tBook Title\t\t\t\tLate Fee\n")
    text_results.insert(tk.END, "----------------------------------------------------------\n")
    for row in results:
        text_results.insert(tk.END, "{}\t\t{}\t\t\t\t{}\n".format(row['Book_ID'], row['Book_Title'], row['Late_Fee']))
    

button_submit.config(command=book_view)

# Run the program.
Book_view_window.mainloop()
