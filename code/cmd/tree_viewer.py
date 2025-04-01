# tree_viewer.py
import tkinter as tk
from tkinter import ttk
from xml_utils import parse_xml, extract_metadata, safe_text, format_description

def populate_tree(tree, node, parent="", namespaces=None, node_refs=None):
    if namespaces is None:
        namespaces = {'xml': 'http://www.w3.org/XML/1998/namespace'}
    if node_refs is None:
        node_refs = {}

    current_id = node.get('termID', 'No ID')
    name_element = node.find("Name[@xml:lang='en']", namespaces=namespaces)
    if name_element is None:
        name_element = node.find("Name")  # fallback if no xml:lang match
    name = name_element.text if name_element is not None else 'No Name'

    description_element = node.find("Definition[@xml:lang='en']", namespaces=namespaces)
    if description_element is None:
        description_element = node.find("Definition")
    description = safe_text(description_element)

    print(f"🧾 Parsed term → ID: {current_id}, Name: {name}, Description: {description[:60]}...")

    node_text = f"{current_id}: {name}"
    tree_id = tree.insert(parent, 'end', text=node_text, open=True)

    node_refs[tree_id] = {'text': node_text.lower(), 'desc': description.lower()}
    tree.item(tree_id, values=(description,))

    for element in node.findall("Term", namespaces=namespaces):
        populate_tree(tree, element, tree_id, namespaces, node_refs)

def visualize_xml(xml_path):
    print("📥 Parsing:", xml_path)
    root = tk.Tk()
    root.title("XML Tree View")

    style = ttk.Style()
    style.configure("Treeview", rowheight=30)

    search_frame = tk.Frame(root)
    search_frame.pack(fill='x', padx=10, pady=5)

    tk.Label(search_frame, text="Search:").pack(side='left')
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, width=50)
    search_entry.pack(side='left', padx=5)

    tree = ttk.Treeview(root, show='tree')
    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    vsb.pack(side='right', fill='y')
    hsb.pack(side='bottom', fill='x')
    tree.pack(fill='both', expand=True)

    root_xml = parse_xml(xml_path)
    print("🧩 Root tag:", root_xml.tag)
    terms = root_xml.findall("Term")
    print("🔍 Found Term count:", len(terms))

    uri, version, alias = extract_metadata(root_xml)

    header_id = tree.insert('', 'end', text=f"URN: {uri}", open=True)
    tree.insert(header_id, 'end', text=f"Version Date: {version}", open=True)
    tree.insert(header_id, 'end', text=f"Alias: {alias}", open=True)

    node_refs = {}
    for term in terms:
        print("🔠 Term attributes:", term.attrib)
        populate_tree(tree, term, header_id, node_refs=node_refs)

    description_box = tk.Text(root, height=10, width=80, wrap='word')
    description_box.pack(side='bottom', fill='x', padx=10, pady=10)

    def update_description(event):
        selected_item = tree.focus()
        values = tree.item(selected_item, 'values')
        if not values:
            return
        description = format_description(values[0])
        description_box.delete('1.0', 'end')
        description_box.insert('1.0', description)

    tree.bind('<<TreeviewSelect>>', update_description)

    def on_search(*args):
        keyword = search_var.get().strip().lower()
        if not keyword:
            return
        for item in tree.get_children(''):
            tree.item(item, open=True)

        found = False
        for item_id, content in node_refs.items():
            if keyword in content['text'] or keyword in content['desc']:
                tree.see(item_id)
                tree.selection_set(item_id)
                tree.focus(item_id)
                found = True
                break
        if not found:
            tree.selection_remove(tree.selection())

    search_var.trace_add('write', on_search)
    root.mainloop()