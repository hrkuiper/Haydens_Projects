import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # creating main window
        self.geometry('1100x600')
        # creating top frame
        self._frame = None
        self.switch_frame(SportCard)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class database(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # setting title for window
        global tree
        global SEARCH
        SEARCH = StringVar()
        # creating frame
        TopViewForm = tk.Frame(self, width=600, bd=1, relief=SOLID)
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = tk.Frame(self, width=600)
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = tk.Frame(self, width=600)
        MidViewForm.pack(side=RIGHT)
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('verdana', 15))
        lbl_txtsearch.pack(side=TOP, anchor=W)

        search = Entry(LeftViewForm, textvariable=SEARCH, font=('verdana', 15), width=10)
        search.pack(side=TOP, padx=10, fill=X)
        btn_search = Button(LeftViewForm, text="Search", command=lambda: self.SearchRecord(tree))
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_search = Button(LeftViewForm, text="View All", command=self.DisplayData)
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)

        # switch window button
        switch = Button(LeftViewForm, text='Switch back to main window', command=lambda: master.switch_frame(SportCard))
        switch.pack(side=TOP, padx=10, pady=10, fill=X)

        # setting scrollbar
        scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
        tree = ttk.Treeview(MidViewForm,
                            columns=("Card Id", "Player Name", "Team Name", "Jersey Number", "Player Position",
                                     "Card Condition", "Sport", "Type"),
                            selectmode="extended", height=100, yscrollcommand=scrollbary.set,
                            xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)

        # setting headings for the columns
        tree.heading('Card Id', text="Card Id", anchor=W)
        tree.heading('Player Name', text="Player Name", anchor=W)
        tree.heading('Team Name', text="Team Name", anchor=W)
        tree.heading('Jersey Number', text="Jersey Number", anchor=W)
        tree.heading('Player Position', text="Player Position", anchor=W)
        tree.heading('Card Condition', text="Card Condition", anchor=W)
        tree.heading('Sport', text="Sport", anchor=W)
        tree.heading('Type', text="Type", anchor=W)

        # setting width of the columns
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=100)
        tree.column('#2', stretch=NO, minwidth=0, width=150)
        tree.column('#3', stretch=NO, minwidth=0, width=80)
        tree.column('#4', stretch=NO, minwidth=0, width=120)
        tree.pack()
        self.DisplayData()

        # Function that searches the database

    def SearchRecord(self, ttk_frame):
        # checking search text is empty or not
        if SEARCH.get() != "":
            # clearing current display data
            for item in ttk_frame.get_children():
                ttk_frame.delete(item)
            # open database
            conn = sqlite3.connect('SportsCardDB.db')
            # select query with where clause
            cursor = conn.execute("SELECT * FROM Card WHERE Card.PlayerName LIKE ?",
                                  ('%' + str(SEARCH.get()) + '%',))

            # fetch all matching records
            fetch = cursor.fetchall()
            # loop for displaying all records into GUI
            for data in fetch:
                tree.insert('', 'end', values=(data))
            cursor.close()
            conn.close()

        # Function that displays all data

    def DisplayData(self):
        # clear current data
        tree.delete(*tree.get_children())
        # open database
        conn = sqlite3.connect('SportsCardDB.db')
        # select query
        cursor = conn.execute("SELECT * FROM Card")
        # fetch all data from database
        fetch = cursor.fetchall()
        # loop for displaying all data in GUI
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()


class SportCard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Main title
        tk.Label(self, text='Select the first option if you want to add/update/delete a row or click the second option to,'
                            'search the entire database.') \
            .pack()

        # switch buttons
        tk.Button(self, text='Add new card ', command=lambda: master.switch_frame(SportCardSearch)).pack()
        tk.Button(self, text='Switch to Grid search', command=lambda: master.switch_frame(database)).pack()

        tk.Button(self, text='quit', )


class SportCardSearch(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Use 'root' for tk instance
        self.sportcardframe = Toplevel()
        # Open tkinter so it fills the screen
         # self.sportcardframe.geometry("2000x2000")
        # Set background color to black
        self.sportcardframe.configure(background='black')



        # Pulls all data from the database
        def all_data():
            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            # Create to database
            conn = sqlite3.connect('SportsCardDB.db')

            # Create a cursor instance
            c = conn.cursor()
            # Select all data from the table
            c.execute("SELECT rowid, * FROM Card")
            records = c.fetchall()

            # Add our data to the screen
            global count
            count = 0

            # for record in records:
            #  print(record)
            for record in records:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end', text='',
                                   values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                           record[7], record[8]))

                else:
                    my_tree.insert(parent='', index='end', text='',
                                   values=(record[1], record[2], record[3], record[4], record[5], record[6],
                                           record[7], record[8]))
                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # Connect to database
        conn = sqlite3.connect('SportsCardDB.db')

        # Create a cursor instance
        c = conn.cursor()

        # Add Menu
        my_menu = Menu(self.sportcardframe)
        self.sportcardframe.config(menu=my_menu)

        # Create a Treeview Frame
        tree_frame = Frame(self.sportcardframe)
        tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = (
        "Card ID", "Player Name", "Team Name", "Jersey Number", "Position", "Condition", "Sport", "Type")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Card ID", anchor=W, width=140)
        my_tree.column("Player Name", anchor=W, width=140)
        my_tree.column("Team Name", anchor=CENTER, width=100)
        my_tree.column("Jersey Number", anchor=CENTER, width=140)
        my_tree.column("Position", anchor=CENTER, width=140)
        my_tree.column("Condition", anchor=CENTER, width=140)
        my_tree.column("Sport", anchor=CENTER, width=140)
        my_tree.column("Type", anchor=CENTER, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Card ID", text="Card ID", anchor=W)
        my_tree.heading("Player Name", text="Player Name", anchor=W)
        my_tree.heading("Team Name", text="Team Name", anchor=CENTER)
        my_tree.heading("Jersey Number", text="Jersey Number", anchor=CENTER)
        my_tree.heading("Position", text="Position", anchor=CENTER)
        my_tree.heading("Condition", text="Condition", anchor=CENTER)
        my_tree.heading("Sport", text="Sport", anchor=CENTER)
        my_tree.heading("Type", text="Type", anchor=CENTER)

        # Add Record Entry Boxes
        data_frame = LabelFrame(self.sportcardframe, text="Record", )
        data_frame.pack(fill="x", expand=1, padx=10)

        id_label = Label(data_frame, text="Card ID:", fg="white")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry = Entry(data_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        pname_label = Label(data_frame, text="Player Name:", fg="white")
        pname_label.grid(row=0, column=2, padx=10, pady=10)
        pname_entry = Entry(data_frame)
        pname_entry.grid(row=0, column=3, padx=10, pady=10)

        tname_label = Label(data_frame, text="Team Name:", fg="white")
        tname_label.grid(row=0, column=4, padx=10, pady=10)
        tname_entry = Entry(data_frame)
        tname_entry.grid(row=0, column=5, padx=10, pady=10)

        jnumber_label = Label(data_frame, text="Jersey Number:", fg="white")
        jnumber_label.grid(row=1, column=0, padx=10, pady=10)
        jnumber_entry = Entry(data_frame)
        jnumber_entry.grid(row=1, column=1, padx=10, pady=10)

        p_label = Label(data_frame, text="Position:", fg="white")
        p_label.grid(row=1, column=2, padx=10, pady=10)
        p_entry = Entry(data_frame)
        p_entry.grid(row=1, column=3, padx=10, pady=10)

        condition_label = Label(data_frame, text="Condition:", fg="white")
        condition_label.grid(row=1, column=4, padx=10, pady=10)
        condition_entry = Entry(data_frame)
        condition_entry.grid(row=1, column=5, padx=10, pady=10)

        sport_label = Label(data_frame, text="Sport:", fg="white")
        sport_label.grid(row=0, column=6, padx=10, pady=10)
        sport_entry = Entry(data_frame)
        sport_entry.grid(row=0, column=7, padx=10, pady=10)

        type_label = Label(data_frame, text="Type:", fg="white")
        type_label.grid(row=1, column=6, padx=10, pady=10)
        type_entry = Entry(data_frame)
        type_entry.grid(row=1, column=7, padx=10, pady=10)

        # Function for deleting a row
        def delete_row():

            x = my_tree.selection()[0]
            my_tree.delete(x)

            # Connect database
            con = sqlite3.connect('SportsCardDB.db')

            # Create a cursor instance
            cursor = con.cursor()

            # Delete From Database
            cursor.execute('DELETE FROM Card WHERE SportsCardID= ?', (id_entry.get(),))

            # Commit changes
            con.commit()

            # Close our connection
            con.close()

            clear_entries()

            messagebox.showinfo("Your Record Has Been Deleted!")

        # Fucntion that clears all entries
        def clear_entries():
            # Function to clear entry boxes after executing
            id_entry.delete(0, END)
            pname_entry.delete(0, END)
            tname_entry.delete(0, END)
            jnumber_entry.delete(0, END)
            p_entry.delete(0, END)
            condition_entry.delete(0, END)
            sport_entry.delete(0, END)
            type_entry.delete(0, END)

        def select_record(e):
            # Clear entry boxes
            id_entry.delete(0, END)
            pname_entry.delete(0, END)
            tname_entry.delete(0, END)
            jnumber_entry.delete(0, END)
            p_entry.delete(0, END)
            condition_entry.delete(0, END)
            sport_entry.delete(0, END)
            type_entry.delete(0, END)

            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')

            # Outputs to entry boxes
            id_entry.insert(0, values[0])
            pname_entry.insert(0, values[1])
            tname_entry.insert(0, values[2])
            jnumber_entry.insert(0, values[3])
            p_entry.insert(0, values[4])
            condition_entry.insert(0, values[5])
            sport_entry.insert(0, values[6])
            type_entry.insert(0, values[7])

        # Update row
        def update_row():
            # Grab the row
            selected = my_tree.focus()
            # Update row
            my_tree.item(selected, text="", values=(id_entry.get(), pname_entry.get(), tname_entry.get(),
                                                    jnumber_entry.get(), p_entry.get(),
                                                    condition_entry.get(), sport_entry.get(),
                                                    type_entry.get(),))

            # Connect to database
            conn = sqlite3.connect('SportsCardDB.db')

            # Create a cursor instance
            c = conn.cursor()

            # SQL script
            c.execute("""UPDATE Card SET
                PlayerName = :pname,
                TeamName = :tname,
                JerseyNumber = :jnumber,
                "Position " = :position,
                Condition = :condition,
                Sport = :sport,
                Type = :type

                WHERE SportsCardID = :id""",
                      {
                          'pname': pname_entry.get(),
                          'tname': tname_entry.get(),
                          'jnumber': jnumber_entry.get(),
                          'position': p_entry.get(),
                          'condition': condition_entry.get(),
                          'sport': sport_entry.get(),
                          'type': type_entry.get(),
                          'id': id_entry.get()
                      })

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            clear_entries()

            messagebox.showinfo("Your Record Has Been Updated!")

        # Function that adds a row to the database
        def add_row():
            # Connect to database
            conn = sqlite3.connect('SportsCardDB.db')

            # Create a cursor instance
            c = conn.cursor()

            # Add new row
            c.execute("INSERT INTO Card VALUES (:id, :pname, :tname, :jnumber, :position, :condition, :sport, :type)",
                      {
                          'id': id_entry.get(),
                          'pname': pname_entry.get(),
                          'tname': tname_entry.get(),
                          'jnumber': jnumber_entry.get(),
                          'position': p_entry.get(),
                          'condition': condition_entry.get(),
                          'sport': sport_entry.get(),
                          'type': type_entry.get()
                      })

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Clear entry boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            all_data()

        # Button frames
        button_frame = LabelFrame(self.sportcardframe, text="Commands")
        button_frame.pack(fill="x", expand=1, padx=20)

        # Update button
        update_button = Button(button_frame, text="Update Row", command=update_row)
        update_button.grid(row=0, column=0, padx=10, pady=10)

        # Add button
        add_button = Button(button_frame, text="Add Row", command=add_row)
        add_button.grid(row=0, column=1, padx=10, pady=10)

        # Delete button
        delete_button = Button(button_frame, text="Delete Row", command=delete_row)
        delete_button.grid(row=0, column=3, padx=10, pady=10)

        # switch button
        switch_button = Button(button_frame, text="Switch", command=lambda: self.switch_frame(SportCard))
        switch_button.grid(row=0, column=5, padx=10, pady=10)

        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_record)

        # Run to pull data from database on start
        all_data()

        # Runs the main loop
        self.sportcardframe.mainloop()


if __name__ == '__main__':
    app = SampleApp()
    app.mainloop()