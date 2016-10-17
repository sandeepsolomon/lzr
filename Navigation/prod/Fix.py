from datetime import datetime
from Angle import Angle
import xml.etree.ElementTree as ET
import sys
import math
import os.path
import time
import pytz

class Fix:
    def __init__(self,log="log.txt"):
        self.log = log
        if (not(isinstance(self.log,str))):
            raise ValueError("{}.{}:  log file input is not a string\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        part = self.log.split('.')
        if len(part[0]) == 1:
            raise ValueError("{}.{}:  log filename is equal top one character\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if (os.path.exists(self.log)):
            timestamp = os.path.getmtime(self.log)
            timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
            timestampString = timeGMT.isoformat(' ')
        else:
            open(self.log,'w').close()
            timestamp = os.path.getctime(self.log)
            timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
            timestampString = timeGMT.isoformat(' ')
        fp  = open(self.log,'a')
        fp.write("LOG:\t")
        fp.write(timestampString)
        fp.write(":\t")
        fp.write("Start of log\n")
        fp.close()

    def setSightingFile(self,sighting=None):
        self.sight = sighting
        if(not(isinstance(self.sight,str))):
            raise ValueError("{}.{}:  sightingFile input is not a string.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        part = sighting.split('.')
        if len(part[0]) == 1:
            raise ValueError("{}.{}:  sighting file length is not greate than 1.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if part[1] != "xml":
            raise ValueError("{}.{}:  sighting file extension is not xml.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        timestamp = os.path.getmtime(self.log)
        timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
        timestampString = timeGMT.isoformat(' ')
        fp =  open(self.log,'a')
        fp.write("LOG:\t")
        fp.write(timestampString)
        fp.write(":\t")
        fp.write("Start of sighting file: ")
        fp.write(self.sight)
        fp.write("\n")
        fp.close()

    def getSightings(self):
        self.approximateLatitude = "0d0.0"
        self.approximateLongitude = "0d0.0"
        if (self.sight == None):
            raise ValueError("{}.{}:  sighting file is not set, it's None.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        filetree = ET.parse(self.sight)
        rootNode = filetree.getroot()
        angle = Angle()
        for child in rootNode.findall('sighting'):

            if child.find('body') == None :
                raise ValueError("{}.{}:  body tag is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if len(child.find('body').text) ==  0 :
                raise ValueError("{}.{}:  body text is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if child.find('date') == None :
                raise ValueError("{}.{}:  date tag is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if len(child.find('date').text) ==  0 :
                raise ValueError("{}.{}:  date text is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if child.find('time') == None :
                raise ValueError("{}.{}:  time tag is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if len(child.find('time').text) ==  0 :
                raise ValueError("{}.{}:  time text is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if child.find('observation') == None :
                raise ValueError("{}.{}:  observation tag is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if len(child.find('observation').text) ==  0 :
                raise ValueError("{}.{}:  observation text is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            string = child.find('observation').text.lstrip(' ').rstrip(' ')
            observation = angle.setDegreesAndMinutes(string)

        completeList = rootNode.findall("sighting")
        newList = []
        for item in completeList:

            tempList = []

            date = item.find('date').text
            time = item.find('time').text
            body = item.find('body').text

            observation = item.find('observation').text
            tempList.append(observation)

            if item.find('height') == None:
                tempList.append(0)
            elif item.find('height').text > 0:
                tempList.append(item.find('height').text)
            else:
                tempList.append(0)

            if item.find('temperature') == None:
                tempList.append(5*float(72-32)/9)
            elif item.find('temperature').text > -20 and item.find('temperature').text < 120:
                tempList.append(5*(float(item.find('temperature').text)-32)/9)
            else:
                tempList.append(5*float(72-32)/9)

            if item.find('pressure') == None:
                tempList.append(1010)
            elif item.find('pressure').text > 100 and item.find('temperature').text < 1100:
                tempList.append(item.find('pressure').text)
            else:
                tempList.append(1010)

            if item.find('horizon') == None:
                tempList.append("natural")
            else:
                tempList.append(item.find('horizon').text)

            newList.append((date,time,body,tempList))

        newList.sort()

        timestamp = os.path.getmtime(self.log)
        timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
        timestampString = timeGMT.isoformat(' ')
        fp = open(self.log,'a')
        for item in newList:
            fp.write("LOG:\t")
            fp.write(timestampString)
            fp.write(":\t")
            fp.write(item[2])
            fp.write("\t")
            fp.write(item[0])
            fp.write("\t")
            fp.write(item[1])
            fp.write("\t")

            string = item[3][0].lstrip(' ').rstrip(' ')

            obsevedAltitude = angle.setDegreesAndMinutes(string)

            tempAltitude = angle.setDegreesAndMinutes("0d0.1")

            if obsevedAltitude < tempAltitude:
                raise ValueError("{}.{}: observedAltitude is LE 0.1 arc minute.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if item[3][4] == "natural":
                dip = (-0.97*math.sqrt(item[3][1]))/60
            else:
                dip = 0

            refraction  = (-0.00452*item[3][3])/(273+item[3][2])/math.tan(math.radians(obsevedAltitude))

            adjustedAltitude = obsevedAltitude + dip + refraction
            tempString = ""
            tempString +=  str(int(adjustedAltitude))
            tempString += "d"
            tempString += str(round(((adjustedAltitude - int(adjustedAltitude))*60),1))
            fp.write(tempString)
            fp.write("\n")

        timestamp = os.path.getmtime(self.log)
        timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
        timestampString = timeGMT.isoformat(' ')
        fp.write("LOG:\t")
        fp.write(timestampString)
        fp.write(":\t")
        fp.write("End of sighting file: ")
        fp.write(self.sight)
        fp.write("\n")
        fp.close()

        return (self.approximateLatitude,self.approximateLongitude)
