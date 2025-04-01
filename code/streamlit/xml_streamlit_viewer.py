import streamlit as st
import os
import xml.etree.ElementTree as ET
import re
from io import StringIO

# Utility functions
def load_xml(file_path):
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except Exception as e:
        st.error(f"Error loading XML: {e}")
        return None

def parse_term(term, namespaces, node_refs, parent_key=""):
    term_id = term.get("termID", "No ID")
    name_element = term.find("Name[@xml:lang='en']", namespaces=namespaces)
    name = name_element.text.strip() if name_element is not None and name_element.text else "No Name"

    desc_element = term.find("Definition[@xml:lang='en']", namespaces=namespaces)
    description = desc_element.text.strip() if desc_element is not None and desc_element.text else "No Description"

    full_key = f"{parent_key}/{term_id}" if parent_key else term_id
    display_key = f"{term_id} {name}"

    node_refs[full_key] = {
        "term_id": term_id,
        "label": name,
        "display_key": display_key,
        "description": description,
        "children": [],
        "key": full_key,
        "parent": parent_key
    }

    for child in term.findall("Term", namespaces=namespaces):
        child_key = parse_term(child, namespaces, node_refs, full_key)
        node_refs[full_key]["children"].append(child_key)

    return full_key

def render_tree(node_key, node_refs, keyword, depth=0):
    node = node_refs[node_key]
    matched = keyword.lower() in node["label"].lower() or keyword.lower() in node["description"].lower()

    indent = "\u2003" * depth
    if matched or keyword == "":
        key_id = f"btn_{node['key']}"
        if st.button(f"{indent}{node['display_key']}", key=key_id):
            if node['key'] in st.session_state.expanded_nodes:
                st.session_state.expanded_nodes.remove(node['key'])
            else:
                st.session_state.expanded_nodes.add(node['key'])

        if node['key'] in st.session_state.expanded_nodes:
            st.markdown(f"{indent}  _Description_: {node['description']}")
            for child_key in node["children"]:
                render_tree(child_key, node_refs, keyword, depth + 1)

def get_repositories_and_files(base_path):
    subfolders = []
    folder_files = {}
    for root, dirs, files in os.walk(base_path):
        rel_root = os.path.relpath(root, base_path)
        if rel_root == ".":
            rel_root = ""  # root folder

        xmls = [f for f in files if f.endswith(".xml")]
        if xmls:
            subfolders.append(rel_root)
            folder_files[rel_root] = sorted(xmls)
    return sorted(subfolders), folder_files

# Streamlit app
def main():
    st.set_page_config(layout="wide")
    st.title("📂 XML Tree Viewer")

    # Sidebar repo & file selector
    st.sidebar.header("🗂️ XML File Selection")
    local_files_path = '../../metadata'

    repositories, files_by_repo = get_repositories_and_files(local_files_path)
    if not repositories:
        st.sidebar.warning("No XML files found in the directory.")
        st.stop()

    selected_repo = st.sidebar.selectbox("📁 Choose repository:", repositories)

    if not selected_repo:
        st.stop()

    repo_files = files_by_repo[selected_repo]
    search_query = st.sidebar.text_input("🔍 Search filenames:", "")
    filtered_files = [f for f in repo_files if search_query.lower() in f.lower()]

    if not filtered_files:
        st.sidebar.warning("No matching files in selected repository.")
        st.stop()

    selected_file = st.sidebar.selectbox("📄 Choose an XML file:", filtered_files)

    if not selected_file:
        st.info("Please select an XML file.")
        st.stop()

    full_path = os.path.join(local_files_path, selected_repo, selected_file)
    keyword = st.text_input("🔎 Search for term or description", "")

    root = load_xml(full_path)
    if root is None:
        return

    namespaces = {'xml': 'http://www.w3.org/XML/1998/namespace'}

    uri = root.attrib.get('uri', 'No URI')
    version = root.attrib.get('versionDate', 'No Version')
    alias = root.findtext('Alias', default="No Alias")

    st.markdown(f"**📄 File**: `{os.path.join(selected_repo, selected_file)}`")
    st.markdown(f"**URN**: `{uri}`")
    st.markdown(f"**Version Date**: `{version}`")
    st.markdown(f"**Alias**: `{alias}`")

    if "expanded_nodes" not in st.session_state:
        st.session_state.expanded_nodes = set()

    node_refs = {}
    for term in root.findall("Term", namespaces=namespaces):
        parse_term(term, namespaces, node_refs)

    st.markdown("### 🌳 Terms Tree")
    for top_key in [k for k in node_refs.keys() if k.count("/") == 0]:
        render_tree(top_key, node_refs, keyword)

if __name__ == "__main__":
    main()
