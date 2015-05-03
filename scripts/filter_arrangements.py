# -*- encoding: utf-8 -*-

import subprocess

try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

ITERM_BUNDLE_ID = "com.googlecode.iterm2"
WINDOW_ARRANGEMENTS_KEY = "Window Arrangements"

class DefaultsProcessError(Exception):
    pass

def render_xml(arrangements):
    items = ET.Element('items')

    for arrangement in arrangements:
        item = ET.SubElement(items, 'item',
                    uid=arrangement,
                    arg=arrangement,
                    valid='YES',
                    autocomplete=arrangement)

        title = ET.SubElement(item, 'title')
        title.text = arrangement

    return ET.tostring(items, encoding='utf-8', method='xml')

# defaults export com.googlecode.iterm2 -
def get_defaults_xml():
    defaults_cmd = ["defaults", "export", ITERM_BUNDLE_ID, "-"]

    try:
        return subprocess.check_output(defaults_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        raise DefaultsProcessError("command 'defaults' returned an error: %s" % err.output)

def parse_defaults_xml(xml):
    plist = ET.fromstring(xml)
    root_dict = plist.find("dict")
    children = list(root_dict)
    arrangements = None

    for i in xrange(len(children)):
        child = children[i]
        if child.tag == 'key' and child.text.strip() == WINDOW_ARRANGEMENTS_KEY:
            arrangements = children[i+1]
            break

    if arrangements is None:
        return []

    return [e.text for e in arrangements.findall("key")]

def print_arrangements(query=None):
    xml = get_defaults_xml()
    arrangements = parse_defaults_xml(xml)
    if query is not None:
        arrangements = [i for i in arrangements if i.find(query) > -1]
    print(render_xml(arrangements))

if __name__ == '__main__':
    query = "{query}"
    print_arrangements(query=query)
