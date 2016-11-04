from datetime import datetime
from Angle import Angle
import xml.etree.ElementTree as ET
import sys
import math
import os.path
import time
import pytz

class Fix:
    def __init__(self,logFile="log.txt"):
        self.log = logFile
        self.sight = None
        if (not(isinstance(self.log,str))):
            raise ValueError("{}.{}:  log file input is not a string\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if len(self.log) < 1:
            raise ValueError("{}.{}:  log file input is Empty\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
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

        if self.sight == None:
            raise ValueError("{}.{}:  sightingFile input is None\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        if(not(isinstance(self.sight,str))):
            raise ValueError("{}.{}:  sightingFile input is not a string.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        part = sighting.split('.')
        if len(part) == 1 :
            raise ValueError("{}.{}:  sighting file doesn't have extenstion\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if len(part[0]) <= 1:
            raise ValueError("{}.{}:  sighting file length is not greate than 1.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if part[1] != "xml":
            raise ValueError("{}.{}:  sighting file extension is not xml.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        if os.path.exists(self.sight):
            f = open(self.sight)
            try:
                tmp = f.read()
            except:
                raise IOError("{}.{}:  sighting file can not be open.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
            f.close()
        else:
            raise IOError("{}.{}:  sighting file doesn't exist.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

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
        return self.sight

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

            if child.find('body').text ==  None :
                raise ValueError("{}.{}:  body text is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            string = child.find('body').text
            if len(string) == 0:
                raise ValueError("{}.{}:  body text is invalid.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if child.find('date') == None :
                raise ValueError("{}.{}:  date tag is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if len(child.find('date').text) ==  0 :
                raise ValueError("{}.{}:  date text is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            string = child.find('date').text.split('-')
            if int(string[1]) >12 or int(string[1]) < 01 or int(string[2]) > 31:
                raise ValueError("{}.{}:  date text is invalid .\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if child.find('time') == None :
                raise ValueError("{}.{}:  time tag is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if len(child.find('time').text) ==  0 :
                raise ValueError("{}.{}:  time text is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            string = child.find('time').text.split(':')
            if len(string) == 1:
                raise ValueError("{}.{}:  time  text is invalid.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))


            if child.find('observation') == None :
                raise ValueError("{}.{}:  observation tag is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if len(child.find('observation').text) ==  0 :
                raise ValueError("{}.{}:  observation text is missing.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            string = child.find('observation').text.lstrip(' ').rstrip(' ')
            string = string.lstrip(' ')
            string = string.rstrip(' ')

            if string.find("d") == -1:
                raise ValueError("{}.{}:  observation text is invalid.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if child.find('temperature') != None and child.find('temperature').text != None and (int(child.find('temperature').text) < -20 or int(child.find('temperature').text) > 120 ):
                raise ValueError("{}.{}:  temperature text is invalid.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if child.find('horizon') != None and child.find('horizon').text != None and ( child.find('horizon').text.lower() != 'artificial' and child.find('horizon').text.lower() != 'natural' ):
                raise ValueError("{}.{}:  horizon text is invalid.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if child.find('height') != None and child.find('height').text != None and child.find('height').text.find(".") == -1:
                raise ValueError("{}.{}:  height text is invalid.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

            if child.find('pressure') != None and child.find('pressure').text != None and child.find('pressure').text.find(".") != -1:
                raise ValueError("{}.{}:  pressure text is invalid.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

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
            elif float(item.find('height').text) > 0:
                tempList.append(item.find('height').text)
            else:
                tempList.append(0)

            if item.find('temperature') == None:
                tempList.append(5*float(72-32)/9)
            elif int(item.find('temperature').text) > -20 and int(item.find('temperature').text) < 120:
                tempList.append(5*(float(item.find('temperature').text)-32)/9)
            else:
                tempList.append(5*float(72-32)/9)

            if item.find('pressure') == None:
                tempList.append(1010)
            elif int(item.find('pressure').text) > 100 and int(item.find('temperature').text) < 1100:
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

            if item[3][4].lower() == "natural":
                dip = (-0.97*math.sqrt(float(item[3][1])))/60
            else:
                dip = 0

            refraction  = (-0.00452*float(item[3][3]))/(273+float(item[3][2]))/math.tan(math.radians(obsevedAltitude))

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
