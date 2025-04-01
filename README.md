# EBU Classification Scheme Viewer

This repository contains the [EBU Metadata Classification Schemes](https://tech.ebu.ch/MetadataReferenceData) in XML format, along with a tool to explore and navigate them using a visual interface.

> 🔗 Try the online tool: [ebu-cs-xml.streamlit.app](https://ebu-cs-xml.streamlit.app/)

---

## 📚 Context

The European Broadcasting Union (EBU) provides a set of reference classification schemes for metadata modeling, standardization, and data interoperability across media organizations.

These classification schemes are part of the documentation described on:
👉 [https://tech.ebu.ch/MetadataReferenceData](https://tech.ebu.ch/MetadataReferenceData)

The XML files represent controlled vocabularies for terms such as roles, media types, content genres, rights, and more.

---

## 📁 Repository Structure

The repository is structured as follows:


Each XML file defines a `ClassificationScheme` and a hierarchy of `Term` elements with multilingual support.

---

## 🌐 How to Use the Online Viewer

👉 Open the app: [ebu-cs-xml.streamlit.app](https://ebu-cs-xml.streamlit.app/)

### Features:
- Browse all XML classification schemes grouped by repository.
- Filter files and search within terms by label or definition.
- Click terms to explore hierarchical children and read definitions.

No installation required. Just visit the URL!

---

## 🧑‍💻 How to Run Locally


### 🟦 Option 1: Run the Tkinter Command-Line App

This version uses a GUI built with `tkinter` to browse and search XML classification schemes.

📁 Source code: [`code/cmd`](https://github.com/ebu/ebu_cs/tree/main/code/cmd)

#### ✅ Requirements

- Python **3.12 or higher** is required (due to improved `tkinter` behavior).
- `tkinter` must be installed (already included in most Python 3.12 installs).

#### 🚀 To run:

```bash
cd code/cmd
python run.py
```

📝 By default, it loads XML files from `../../metadata/cs` or lets you browse your own.

---

### 🟩 Option 2: Run the Streamlit Web App Locally

This version provides a modern browser-based interface using [Streamlit](https://streamlit.io/).

📁 Source code: [`code/streamlit`](https://github.com/ebu/ebu_cs/tree/main/code/streamlit)

#### ✅ Setup steps:

1. **Navigate to the app directory**:

```bash
cd code/streamlit
```

2. **Create and activate a virtual environment** (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install required packages**:

```bash
pip install -r requirements.txt
```

4. **Launch the app**:

```bash
streamlit run xml_streamlit_viewer.py
```

The app will open at: [http://localhost:8501](http://localhost:8501)
