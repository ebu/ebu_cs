# app.py
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tree_viewer import visualize_xml

def select_file(local_files_path):
    def on_select(event):
        selected_file = file_menu.get()
        print("📄 File selected from dropdown:", selected_file)
        if selected_file.endswith('.xml'):
            root.destroy()  # Close file selector window before launching viewer
            visualize_xml(os.path.join(local_files_path, selected_file))

    root = tk.Tk()
    root.title("Select XML File")

    full_file_list = sorted([f for f in os.listdir(local_files_path) if f.endswith('.xml')])
    if not full_file_list:
        messagebox.showwarning("No XML Files", f"No .xml files found in: {local_files_path}")
        root.destroy()
        return

    filtered_file_list = full_file_list.copy()

    def update_dropdown(*args):
        keyword = file_search_var.get().strip().lower()
        filtered = [f for f in full_file_list if keyword in f.lower()]
        if not filtered:
            filtered = ["No XML files found"]
        file_menu['values'] = filtered
        file_menu.set(filtered[0])

    file_search_var = tk.StringVar()
    file_search_var.trace_add('write', update_dropdown)

    tk.Label(root, text="Search files:").pack(pady=(10, 0))
    tk.Entry(root, textvariable=file_search_var, width=50).pack(pady=5)

    tk.Label(root, text="Select an XML file:").pack(pady=(10, 0))
    file_menu = ttk.Combobox(root, values=filtered_file_list, state="readonly",
                             width=max(30, len(max(full_file_list, key=len)) + 2))
    file_menu.pack(pady=5)
    file_menu.bind("<<ComboboxSelected>>", on_select)

    def refresh_file_list():
        nonlocal full_file_list, filtered_file_list
        full_file_list = sorted([f for f in os.listdir(local_files_path) if f.lower().endswith('.xml')])
        print("📂 XML files found:", full_file_list)
        filtered_file_list = full_file_list.copy()
        file_menu['values'] = filtered_file_list
        if filtered_file_list:
            file_menu.set(filtered_file_list[0])

    tk.Button(root, text="Refresh File List", command=refresh_file_list).pack(pady=10)
    root.mainloop()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        local_files_path = sys.argv[1]
    else:
        local_files_path = './cs'

    print("✅ XML Viewer launched with folder:", local_files_path)
    select_file(local_files_path)
