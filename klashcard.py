import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import tkinter.messagebox as messagebox
import random
import csv

# Initialize the database dictionary to store flashcards
database = {}
# Define the file path to the CSV file that contains the flashcard data
file_path = "D:/Engg/Codes/Python/CIP'24 Final Project/Klashcard/database.csv"

# Define the main application class for the Klashcard app
class KlashcardApp:
    def __init__(self, root):
        # Set up the main window properties
        self.root = root
        self.root.title("Klashcard")
        self.center_window(400, 300)
        self.root.resizable(False, False)
        self.file_reading()  # Load flashcards from the CSV file into the database
        self.main_menu()  # Display the main menu

    # Clear all widgets from the current window
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Center the application window on the screen
    def center_window(self, width=300, height=200):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    # Display the main menu with options
    def main_menu(self):
        self.clear_frame()
        ctk.CTkLabel(self.root, text="Welcome to Klashcard", font=("Comic Sans MS", 25, 'bold')).pack(pady=35)
        ctk.CTkButton(self.root, text="Practice", command=self.practice_menu).pack(pady=13)
        ctk.CTkButton(self.root, text="Modify Card", command=self.modify_menu).pack(pady=13)
        ctk.CTkButton(self.root, text="Exit", command=self.root.quit).pack(pady=13)

    # Read data from the CSV file and store them in the database
    def file_reading(self):
        with open(file_path) as file:
            reader = csv.reader(file)
            for eng, ban in reader:
                database[eng] = ban

    # Display the practice menu
    def practice_menu(self):
        self.clear_frame()
        random_key = random.choice(list(database.keys()))
        random_keys_value = database[random_key]

        # Function to check the user's answer
        def check_answer():
            answer = entry.get().strip().lower()            
            if answer == random_keys_value:
                msg = CTkMessagebox(title="Klashcard", message="Correct", icon="check", font=("Comic Sans MS", 20, 'bold'), sound=True)
                if msg.get() == "OK":
                    self.practice_menu()
            else:
                CTkMessagebox(title="Klashcard", message=f"Incorrect!!\nCorrect answer is: {random_keys_value}", font=("Comic Sans MS", 20, 'bold'))
            entry.delete(0, ctk.END)
            
        ctk.CTkLabel(self.root, text="^_^").pack(pady=5)
        ctk.CTkLabel(self.root, text=f'What is the Bangla meaning of', font=("Comic Sans MS", 17)).pack(pady=5)
        ctk.CTkLabel(self.root, text=f'{random_key}'.upper(), font=("Impact", 30)).pack(pady=5)
        entry = ctk.CTkEntry(self.root)
        entry.pack(pady=20)
        ctk.CTkButton(self.root, text="Submit", command=check_answer).pack(pady=10)
        ctk.CTkButton(self.root, text="End Session", command=self.main_menu).pack(pady=10)
    #----PRACTICE MENU END----#

    # Display the menu to modify flashcards
    def modify_menu(self):
        self.clear_frame()
        ctk.CTkLabel(self.root, text="Modify Card", font=("Comic Sans MS", 20, "bold")).pack(pady=20)
        ctk.CTkButton(self.root, text="Add Card", command=self.add_card_menu).pack(pady=8)
        ctk.CTkButton(self.root, text="Delete Card", hover_color="#FA8072", command=self.delete_card_menu).pack(pady=8)
        ctk.CTkButton(self.root, text="Update Card", command=self.update_card_menu).pack(pady=8)
        ctk.CTkButton(self.root, text="Show All Cards", command=self.show_cards).pack(pady=8)
        ctk.CTkButton(self.root, text="Go Back", command=self.main_menu).pack(pady=8)
    #----MODIFY MENU END----#

    # Display the add card menu
    def add_card_menu(self):
        self.clear_frame()

        # Function to add a new flashcard
        def add_card():
            key = key_entry.get().strip()
            value = value_entry.get().strip()
            
            if key in database:
                messagebox.showerror("Error", "This key already exists.")
            elif key and value:
                database[key] = value
                self.update_csv()
                msg = CTkMessagebox(title="Success", message="Card Added Successfully!", icon="check")
                if msg.get() == "OK":
                    self.modify_menu()
            else:
                messagebox.showerror("Error", "Key and Value cannot be empty.")

        ctk.CTkLabel(self.root, text="Add New Card", font=("Comic Sans MS", 25, "bold")).pack(pady=10)
        ctk.CTkLabel(self.root, text="Key:").pack(pady=5)
        key_entry = ctk.CTkEntry(self.root)
        key_entry.pack(pady=5)
        ctk.CTkLabel(self.root, text="Value:").pack(pady=5)
        value_entry = ctk.CTkEntry(self.root)
        value_entry.pack(pady=5)
        ctk.CTkButton(self.root, text="Add Card", command=add_card).pack(pady=5)
        ctk.CTkButton(self.root, text="Go Back", command=self.modify_menu).pack(pady=5)
    #----ADD CARD MENU END----#

    # Display the delete card menu
    def delete_card_menu(self):
        self.clear_frame()

        # Function to delete a flashcard
        def delete_card():
            key = key_entry.get().strip()
            if key in database:
                del database[key]
                self.update_csv()
                msg = CTkMessagebox(title="Success", message="Card Deleted Successfully!")
                if msg.get() == "OK":
                    self.modify_menu()
            else:
                messagebox.showerror("Error", "Key does not exist.")

        ctk.CTkLabel(self.root, text="Delete Card", font=("Comic Sans MS", 25, "bold")).pack(pady=10)
        ctk.CTkLabel(self.root, text="Key:").pack(pady=5)
        key_entry = ctk.CTkEntry(self.root)
        key_entry.pack(pady=5)
        ctk.CTkButton(self.root, text="Delete Card", hover_color="#FA8072", command=delete_card).pack(pady=5)
        ctk.CTkButton(self.root, text="Go Back", command=self.modify_menu).pack(pady=5)
    #----DELETE CARD MENU END----#

    # Display the update card menu
    def update_card_menu(self):
        self.clear_frame()

        # Function to update an existing flashcard
        def update_card():
            key = key_entry.get().strip().lower()
            new_value = value_entry.get().strip().lower()
            
            if key in database:
                database[key] = new_value
                self.update_csv()
                msg = CTkMessagebox(title="Success", message="Card Updated Successfully!", icon="check")
                if msg.get() == "OK":
                    self.modify_menu()
            else:
                messagebox.showerror("Error", "Invalid Key or Value.")

        ctk.CTkLabel(self.root, text="Update Card", font=("Comic Sans MS", 25, "bold")).pack(pady=10)
        ctk.CTkLabel(self.root, text="Key:").pack(pady=5)
        key_entry = ctk.CTkEntry(self.root)
        key_entry.pack(pady=5)
        ctk.CTkLabel(self.root, text="New Value:").pack(pady=5)
        value_entry = ctk.CTkEntry(self.root)
        value_entry.pack(pady=5)
        ctk.CTkButton(self.root, text="Update Card", command=update_card).pack(pady=5)
        ctk.CTkButton(self.root, text="Go Back", command=self.modify_menu).pack(pady=5)
    #----UPDATE CARD MENU END----#

    # Display all flashcards in the database
    def show_cards(self):
        self.clear_frame()
        ctk.CTkLabel(self.root, text="All Cards", font=("Comic Sans MS", 25, "bold")).pack(pady=10)
        ctk.CTkButton(self.root, text="Go Back", command=self.modify_menu).pack(pady=5)
        scrollable_frame = ctk.CTkScrollableFrame(self.root, width=380, height=100)
        scrollable_frame.pack(padx=10, pady=10, expand=False)
        for key, value in database.items():
            ctk.CTkLabel(scrollable_frame, text=f"{key} -> {value}", font=("Comic Sans MS", 18)).pack(pady=5)
    #----SHOW CARDS END----#

    # Update the CSV file with the current state of the database
    def update_csv(self):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for key, value in database.items():
                writer.writerow([key, value])
    #----UPDATE CSV END----#

# Initialize the Klashcard application
if __name__ == "__main__":
    root = ctk.CTk()
    app = KlashcardApp(root)
    root.mainloop()
