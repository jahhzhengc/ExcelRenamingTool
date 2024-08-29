import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class RenamingApp(tk.Tk):  

    def select_folder(self): 
        self.folder_path = filedialog.askdirectory()

        if not self.folder_path:
            return  
        self.current_folder_path.config(text = self.folder_path)
        file_names = []
 
        for file in os.listdir(self.folder_path):
            extension = os.path.splitext(file)[1]
            # its a folder
            if not extension: 
                continue 
            
            # its a hidden file
            if not file.startswith('.'):
                file_names.append(file)
                print(file)

        file_names.sort() # sort them alphebetically
        # split them into array of arrays
        self.file_names = [file_names[i:i+ self.max_per_page] for i in range(0, len(file_names), self.max_per_page)]

        self.current_page = 0
        self.update_btns()

    def update_btns(self):  

        self.prev_page_btn['state'] = "disabled" if self.current_page == 0 else "normal"
        self.next_page_btn['state'] = "disabled" if self.current_page == len(self.file_names) - 1 else "normal"

        self.current_page_label.config(text= f"{self.current_page + 1} .. {len(self.file_names)}")
        # print(self.file_names[self.current_page])

        for i in self.tree.get_children():
            self.tree.delete(i)

        for widget in self.entry_widgets:
            widget.destroy()

        self.entry_widgets.clear()

        if(len(self.file_names) > 0):
            for idx, file_name in enumerate(self.file_names[self.current_page]):
                self.tree.insert("", "end", text=str(idx+1), values=(file_name,))
                entry = tk.Entry(self.entries_frame)
                entry.insert(0, file_name)
                entry.pack(side= "top") 
                self.entry_widgets.append(entry)
 
    def next_page(self):
        self.current_page += 1
        self.update_btns()

    def prev_page(self):
        self.current_page -= 1
        self.update_btns()

    def __init__(self):
        super().__init__()
        
        self.current_page = 0
        self.max_per_page = 4
        self.folder_path = ""  
        self.entry_widgets = []
        self.file_names = []
        
        button_frame = tk.Frame(self)
        button_frame.pack(side="top", anchor ="n")

        buttons_frame = tk.Frame(button_frame)
        buttons_frame.pack(side="top", anchor ="n")

        texts_frame = tk.Frame(button_frame)
        texts_frame.pack(fill= "x", side="top", anchor ="n")

        self.current_folder_path = tk.Label(texts_frame, text="Current folder is empty")
        self.current_folder_path.pack()

        select_button = tk.Button(buttons_frame, text="Select Folder", command=self.select_folder)
        select_button.pack(side="left", padx=5)

        update_button = tk.Button(buttons_frame, text="Update Treeview", command=self.update_treeview)
        update_button.pack(side="left", padx=5)

        below_frame =tk.Frame(self)
        below_frame.pack(fill="x", side="bottom", anchor="s")

        self.next_page_btn = tk.Button(below_frame, text =">", command=self.next_page)
        self.next_page_btn.pack(side ="right", anchor="e")
        self.prev_page_btn = tk.Button(below_frame, text ="<",command=self.prev_page)
        self.prev_page_btn.pack(side ="right", anchor="e")

        self.current_page_label = tk.Label(below_frame)
        self.current_page_label.pack(side="left", anchor="w")
        # btm frame, that holds onto tree-view on left, entries on right
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side="bottom", anchor="s")

        left_frame = tk.Frame(bottom_frame)
        left_frame.pack(side="left", anchor="w")
 
        self.tree = ttk.Treeview(left_frame, columns=('Name',), show='headings', height=15)
        self.tree.heading('Name', text='File Name') 
        self.tree.pack() 
        self.entries_frame = tk.Frame(bottom_frame)
        self.entries_frame.pack(side="right",anchor="e", fill='both') 
        tk.Label(self.entries_frame, text="To change file name", borderwidth=2, relief="groove").pack(anchor="n", side="top")

    def update_treeview(self):  
        merged_list = []

        for l in self.file_names:
            merged_list += l

        for idx, item in enumerate(self.tree.get_children()):
            new_file = self.entry_widgets[idx].get()
            old_file = self.tree.item(item=item)['values'][0] 

            # if its the same, ignores
            if(old_file == new_file): 
                continue
            
            # gets the index of the merged list
            index = idx + self.current_page  * self.max_per_page 

            skip = False
            # had to use new variable names
            for idx_, item_ in enumerate(merged_list):
                # specifically had to enumerate the merged list,
                # cause originally the merged list would have the existing filename anyway
                # so i had to check for every other 
                if(idx_ == index):
                    continue

                if(item_ == new_file): 
                    skip = True
                    break 

            new_extension = os.path.splitext(new_file)[1]
            old_extension = os.path.splitext(old_file)[1]
            
            # if its empty or changed extension, revert
            if(not new_file or new_extension != old_extension or skip):   
                # insert literally only inserts, must delete first
                self.entry_widgets[idx].delete(0, 'end')
                self.entry_widgets[idx].insert(0, old_file)
                continue
            
            new_value = new_file
            old_file = os.path.join(self.folder_path, old_file)
            new_file = os.path.join(self.folder_path, new_file)  

            self.tree.item(item, values=(new_value,)) # this is meant for immediate update on the tree view
            self.file_names[self.current_page][idx] = new_value # this is to update the original file
            merged_list[index] = new_value # so that if there's multiple file names changed to the same name, it would be recognised as well
            os.rename(old_file, new_file)


"""
    Test case 1: change name with empty string ("") 
    Test case 3: change multiple names with same name 
    Test case 4: change extensions for new names
    Test case 5; change to other file's name 
"""
if __name__ == "__main__":
    app = RenamingApp()
    app.resizable(False,False)
    app.mainloop()
