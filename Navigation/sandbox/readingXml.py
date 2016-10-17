#!/opt/local/bin/python
import xml.etree.ElementTree as ET

tree = ET.parse("sightingFile.xml")
root = tree.getroot()
print root.tag
print root.attrib
container = root.findall("sighting")
data = []
for elem in container:
    date = elem.find('date').text
    time = elem.find('time').text
    body = elem.find('body').text
    data.append((date,time,body,elem))
data.sort()

#for child in root.findall('sighting'):
#    print child.find('body').text
#    print child.find('date').text
#    print child.find('time').text
#    print child.find('observation').text
#    print child.find('height').text
#    print child.find('temperature').text
#    print child.find('pressure').text
#    print child.find('horizon').text
#
#def sortchildrenby(parent, attr):
#        parent[:] = sorted(parent, key=lambda child: child.get(attr))
