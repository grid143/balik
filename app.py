import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic GUI App")

        # MongoDB connection
        self.client = MongoClient("mongodb+srv://itcc33_database:anonymouse143214.@itcc33.bd1ay5a.mongodb.net/")
        self.db = self.client["XOB_Database"]

        # GUI components
        self.label = tk.Label(root, text="Database Management")
        self.label.pack(pady=10)

        # Dropdown for selecting collection
        self.collection_var = tk.StringVar()
        self.collection_var.set(self.get_collection_names()[0])  # Set the default collection
        self.collection_dropdown = ttk.Combobox(root, textvariable=self.collection_var, values=self.get_collection_names())
        self.collection_dropdown.pack(pady=5)
        self.collection_dropdown.bind("<<ComboboxSelected>>", lambda event: self.refresh_gui())

        # Entry fields for adding/updating document
        self.entry_widgets = {}  # Dictionary to store entry widgets dynamically
        self.create_entry_fields()

        # Buttons for CRUD operations
        self.add_button = tk.Button(root, text="Add Document", command=self.add_document)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Document", command=self.update_document)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Document", command=self.delete_document)
        self.delete_button.pack(pady=5)

        self.refresh_button = tk.Button(root, text="Refresh List", command=self.refresh_gui)
        self.refresh_button.pack(pady=5)

        # Listbox for displaying documents
        self.document_listbox = tk.Listbox(root)
        self.document_listbox.pack(pady=10)
        self.document_listbox.bind("<<ListboxSelect>>", self.show_selected_document)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Populate the document list
        self.refresh_list()

    def get_collection_names(self):
        # Get the names of all collections in the database
        return self.db.list_collection_names()

    def create_entry_fields(self):
        # Clear existing entry fields and labels
        for widget in self.entry_widgets.values():
            widget.destroy()
        self.entry_widgets = {}

        # Create entry fields and labels based on the fields in the selected collection
        selected_collection = self.collection_var.get()
        sample_document = self.db[selected_collection].find_one()
        if sample_document:
            self.label_widgets = []  # Keep track of labels to destroy later
            for field in sample_document.keys():
                label = tk.Label(self.root, text=field)
                label.pack(pady=5, side=tk.LEFT)
                entry = tk.Entry(self.root, width=30)
                entry.pack(pady=5, side=tk.LEFT)
                entry.insert(0, f"{sample_document[field]}")
                self.entry_widgets[field] = entry
                self.label_widgets.append(label)

    def refresh_list(self):
        # Clear existing items
        self.document_listbox.delete(0, tk.END)

        # Fetch documents from MongoDB and add to the listbox
        selected_collection = self.collection_var.get()
        documents = self.db[selected_collection].find()

        if documents:  # Check if documents is not None
            for document in documents:
                document_str = " - ".join(f"{field}: {document.get(field, 'N/A')}" for field in self.entry_widgets.keys())
                self.document_listbox.insert(tk.END, document_str)

    def show_selected_document(self, event):
        # Display information of the selected document in the entry fields
        selected_index = self.document_listbox.curselection()
        if selected_index:
            selected_document = self.db[self.collection_var.get()].find()[selected_index[0]]
            for field, entry in self.entry_widgets.items():
                entry.delete(0, tk.END)
                entry.insert(0, f"{selected_document.get(field, 'N/A')}")

    def add_document(self):
        # Add new document to MongoDB
        selected_collection = self.collection_var.get()
        new_document = {field: entry.get() for field, entry in self.entry_widgets.items()}
        self.db[selected_collection].insert_one(new_document)
        self.refresh_list()
        self.clear_entry_fields()

    def update_document(self):
        # Update selected document in MongoDB
        selected_index = self.document_listbox.curselection()
        if selected_index:
            selected_document = self.db[self.collection_var.get()].find()[selected_index[0]]
            updated_document = {field: entry.get() for field, entry in self.entry_widgets.items()}

            # Print debugging information to the console
            print("Selected Document:", selected_document)
            print("Updated Document:", updated_document)

            update_query = {"$set": updated_document}

            result = self.db[self.collection_var.get()].update_one({"_id": selected_document["_id"]}, {"$set": updated_document})

            print("Update Result:", result.raw_result)

            self.refresh_list()
            self.clear_entry_fields()


    def delete_document(self):
        # Delete selected document from MongoDB
        selected_index = self.document_listbox.curselection()
        if selected_index:
            selected_document = self.db[self.collection_var.get()].find()[selected_index[0]]
            self.db[self.collection_var.get()].delete_one({"_id": selected_document["_id"]})
            self.refresh_list()

    def refresh_gui(self):
        # Refresh the GUI by recreating entry fields based on the selected collection
        self.clear_labels()
        self.create_entry_fields()
        self.refresh_list()

    def clear_entry_fields(self):
        # Clear entry fields
        for entry in self.entry_widgets.values():
            entry.delete(0, tk.END)

    def clear_labels(self):
        # Clear labels
        for label in self.label_widgets:
            label.destroy()

    def on_close(self):
        # Close MongoDB connection and exit the application
        self.client.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()