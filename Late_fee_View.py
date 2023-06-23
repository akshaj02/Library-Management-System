from sqlite3 import Connection, Cursor
import tkinter as tk
from tkinter import messagebox

# Create a window object.
connection = Connection("library.db")
cursor = connection.cursor()

Late_fee_window = tk.Tk()
Late_fee_window.title("Late Fee")

# Set window size and position.
Late_fee_window.geometry("700x600+400+50")

# Add labels and text boxes to the window.
label_borrower_info = tk.Label(Late_fee_window, text="Enter Borrower ID, Borrower Name, Part of the name or leave it blank to see all:")
label_borrower_info.pack(pady=10)
text_borrower_info = tk.Entry(Late_fee_window)
text_borrower_info.pack()

button_submit = tk.Button(Late_fee_window, text="Submit ✔")
button_submit.pack(pady=20)

button_back = tk.Button(Late_fee_window, text="Back")
button_back.pack(pady=10)
button_back.config(command=Late_fee_window.destroy)


def late_fee(filter=None):
    filter = text_borrower_info.get()
    # Build the SQL query
    sql = "SELECT vBookLoanInfo.Card_No AS ID, vBookLoanInfo.Borrower_Name AS Name, ROUND(SUM(LateFeeBalance), 2) AS LateFeeBalance " \
          "FROM vBookLoanInfo " \
          "WHERE LateFeeBalance > 0 "
    
    if filter:
        if filter.isdigit():
            sql += "AND vBookLoanInfo.Card_No = {} ".format(filter)
        else:
            sql += "AND vBookLoanInfo.Borrower_Name LIKE '%{}%' ".format(filter)
    
    sql += "GROUP BY vBookLoanInfo.Card_No ORDER BY LateFeeBalance DESC"

    # Execute the query
    cursor.execute(sql)

    # Get the results and convert to US dollars
    results = []
    for row in cursor.fetchall():
        result = {}
        result['ID'] = row[0]
        result['Name'] = row[1]
        result['LateFeeBalance'] = "$" + str(row[2]) if row[2] != 0 else "$0.00"
        results.append(result)

    #Display using text results
    text_results = tk.Text(Late_fee_window, height=10, width=70)
    text_results.pack()
    text_results.insert(tk.END, "ID\t\tName\t\tLate Fee Balance\n")
    text_results.insert(tk.END, "------------------------------------------------------\n")
    for result in results:
        text_results.insert(tk.END, "{}\t\t{}\t\t{}\n".format(result['ID'], result['Name'], result['LateFeeBalance']))
        

        
button_submit.config(command=late_fee)


# Run the program.
Late_fee_window.mainloop()