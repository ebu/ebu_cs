import streamlit as st
import xml.etree.ElementTree as ET
import re
import requests
import json
from io import StringIO

# Load JSON index of files from GitHub (raw URL)
INDEX_URL = "https://raw.githubusercontent.com/ebu/ebu_cs/main/metadata/ebu_cs_file_index.json"

@st.cache_data(show_spinner=False)
def load_index():
    try:
        res = requests.get(INDEX_URL)
        return res.json()
    except Exception as e:
        st.error(f"Failed to load file index: {e}")
        return {}

@st.cache_data(show_spinner=False)
def load_xml_from_github(repo: str, filename: str):
    try:
        url = f"https://raw.githubusercontent.com/ebu/ebu_cs/main/metadata/{repo}/{filename}"
        res = requests.get(url)
        res.raise_for_status()
        return ET.fromstring(res.text)
    except Exception as e:
        st.error(f"Error loading XML file from GitHub: {e}")
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
    is_top_level = node['key'].count("/") == 0
    color_prefix = f"<span style='color:blue; font-weight:bold;'>{node['display_key']}</span>" if is_top_level else node['display_key']

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

def main():
    st.set_page_config(layout="wide")
    st.title("📂 XML Tree Viewer (GitHub-hosted)")

    # Load file index
    index_data = load_index()

    if not index_data:
        st.stop()

    # Sidebar: choose repository and file
    st.sidebar.header("📁 File Browser")
    repo_names = sorted(index_data.keys())
    selected_repo = st.sidebar.selectbox("Choose repository:", repo_names)

    file_list = index_data.get(selected_repo, [])
    search_query = st.sidebar.text_input("Search filenames:", "")
    filtered_files = [f for f in file_list if search_query.lower() in f.lower()]

    if not filtered_files:
        st.sidebar.warning("No matching XML files.")
        st.stop()

    selected_file = st.sidebar.selectbox("Choose an XML file:", filtered_files)

    if not selected_file:
        st.info("Please select a file from the sidebar.")
        st.stop()

    # Load and parse XML from GitHub
    root = load_xml_from_github(selected_repo, selected_file)
    if root is None:
        st.stop()

    keyword = st.text_input("🔍 Search term or description:", "")
    namespaces = {'xml': 'http://www.w3.org/XML/1998/namespace'}

    uri = root.attrib.get('uri', 'No URI')
    version = root.attrib.get('versionDate', 'No Version')
    alias = root.findtext('Alias', default="No Alias")

    st.markdown(f"**URN**: `{uri}`")
    st.markdown(f"**Version Date**: `{version}`")
    st.markdown(f"**Alias**: `{alias}`")

    node_refs = {}
    for term in root.findall("Term", namespaces=namespaces):
        parse_term(term, namespaces, node_refs)

    st.markdown("### Terms Tree")
    if "expanded_nodes" not in st.session_state:
        st.session_state.expanded_nodes = set()

    top_level_keys = [k for k in node_refs.keys() if k.count("/") == 0]

    for top_key in top_level_keys:
        render_tree(top_key, node_refs, keyword)

if __name__ == "__main__":
    main()
