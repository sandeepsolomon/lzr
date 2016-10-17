#!/opt/local/bin/python
import xml.etree.ElementTree as ET

#tree = ET.parse("country_data.xml")
#root = tree.getroot()
#print root.tag
#print root.attrib
#for child in root:
#    print child.tag, child.attrib
#for neighbor in root.iter('neighbor'):
#    print neighbor.attrib
#
#
#for country in root.findall('country'):
#    rank = country.find('rank').text
#    name = country.get('name')
#    print name, rank
#
tree = ET.parse("sightingFile.xml")
root = tree.getroot()
print root.tag
print root.attrib
sortchildrenby(root,'
for child in root.findall('sighting'):
    print child.find('body').text
    print child.find('date').text
    print child.find('time').text
    print child.find('observation').text
    print child.find('height').text
    print child.find('temperature').text
    print child.find('pressure').text
    print child.find('horizon').text

def sortchildrenby(parent, attr):
        parent[:] = sorted(parent, key=lambda child: child.get(attr))
