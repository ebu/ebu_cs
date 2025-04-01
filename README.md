# EBU Classification Scheme Viewer

This repository contains the [EBU Metadata Classification Schemes](https://tech.ebu.ch/MetadataReferenceData) in XML format, along with tools to explore and navigate them using a visual interface.

> 🔗 Try the online tool: [ebu-cs-xml.streamlit.app](https://ebu-cs-xml.streamlit.app/)

---

## Context

The European Broadcasting Union (EBU) provides a set of reference classification schemes for metadata modeling, standardization, and data interoperability across media organizations.

These classification schemes are part of the documentation described on:
👉 [https://tech.ebu.ch/MetadataReferenceData](https://tech.ebu.ch/MetadataReferenceData)

The XML files represent controlled vocabularies for terms such as roles, media types, content genres, rights, and more.

---

## Repository Structure

The project is organized into two repositories:

- **Metadata repo**: Contains XML files that define a `ClassificationScheme` and a structured hierarchy of `Term` elements.
- **Code repo**: Provides tools to browse and search the metadata content.

---

## How to Use the Online Viewer

👉 Open the app: [ebu-cs-xml.streamlit.app](https://ebu-cs-xml.streamlit.app/)

### Features:
- Browse all XML classification schemes grouped by repository.
- Filter files and search within terms by label or definition.
- Click terms to explore hierarchical children and read definitions.

No installation required. Just visit the URL!

---

## How to Run Locally

### Python Version Requirement

The local Streamlit XML viewer requires **Python 3.12 or higher** due to features and compatibility with Streamlit and XML processing libraries.

You can check your current Python version by running:

```bash
python --version
```

If your version is lower than 3.12, follow these instructions to upgrade:

#### macOS (with Homebrew)

```bash
brew install python@3.12
brew link --overwrite python@3.12
```

#### Ubuntu / Debian

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

#### Windows

Download and install the latest Python 3.12.x from the official website:  
👉 https://www.python.org/downloads/windows/

> ⚠️ After installation, make sure `python` and `pip` point to the new version. You might need to run:
>
> ```bash
> python3.12 -m pip install --upgrade pip
> ```

Once Python 3.12+ is installed and available, you can set up and run the project locally using:

```bash

### 🟩 Option 1: Run the Tkinter Command-Line App

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
