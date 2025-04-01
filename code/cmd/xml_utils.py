import xml.etree.ElementTree as ET
import re
import textwrap

def parse_xml(xml_path):
    """Parses an XML file and returns the root element."""
    tree = ET.parse(xml_path)
    return tree.getroot()

def extract_metadata(root_xml):
    """Extracts URN, version date, and alias from the root element."""
    uri = root_xml.attrib.get('uri', 'No URI')
    version = root_xml.attrib.get('versionDate', 'No Version')
    alias_element = root_xml.find('Alias')
    alias = alias_element.text.strip() if alias_element is not None and alias_element.text else 'No Alias'
    return uri, version, alias

def safe_text(element):
    """Safely retrieves and strips text from an XML element."""
    return element.text.strip() if element is not None and element.text else 'No Description'

def format_description(text):
    """Cleans and wraps text for display in the description box."""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return '\n'.join(textwrap.wrap(text, width=75 * 4))
