from datetime import datetime
from Angle import Angle
import xml.etree.ElementTree as ET
import sys
import math
import os
import time
import pytz

class Fix:

    def __init__(self,log="log.txt"):

        self.log = log
        self.angle = Angle()
        logAbsolutePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),self.log)

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
        fp.write(logAbsolutePath)
        fp.write("\n")
        fp.close()
        return Fix()

    def setSightingFile(self,sighting=None):
        self.errorCount = 0
        self.sight = sighting

        if(not(isinstance(self.sight,str))):
            raise ValueError("{}.{}:  sighting file input is not a string.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        part = self.sight.split('.')

        if len(part[0]) == 1:
            raise ValueError("{}.{}:  sighting file length is not greate than 1.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if part[1] != "xml":
            raise ValueError("{}.{}:  sighting file extension is not xml.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        timestamp = os.path.getmtime(self.log)
        timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
        timestampString = timeGMT.isoformat(' ')

        sightingAbsolutePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),self.sight)

        fp =  open(self.log,'a')
        fp.write("LOG:\t")
        fp.write(timestampString)
        fp.write(":\t")
        fp.write(sightingAbsolutePath)
        fp.write("\n")
        fp.close()

        filetree = ET.parse(self.sight)
        rootNode = filetree.getroot()
        for child in rootNode.findall('sighting'):
            if child.find('body') == None :
                self.errorCount += 1
                continue

            if len(child.find('body').text) ==  0 :
                self.errorCount += 1
                continue

            if child.find('date') == None :
                self.errorCount += 1
                continue

            if len(child.find('date').text) ==  0 :
                self.errorCount += 1
                continue

            if child.find('time') == None :
                self.errorCount += 1
                continue

            if len(child.find('time').text) ==  0 :
                self.errorCount += 1
                continue

            if child.find('observation') == None :
                self.errorCount += 1
                continue

            if len(child.find('observation').text) ==  0 :
                self.errorCount += 1
                continue

            string = child.find('observation').text.lstrip(' ').rstrip(' ')
            observation = self.angle.setDegreesAndMinutes(string)
        completeList = rootNode.findall("sighting")
 #       completeList = rootNode.findall("sighting")
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
        self.sightData = newList
        return sightingAbsolutePath

    def setAriesFile(self,aries="aries.txt"):
        self.aries = aries
        ariesAbsolutePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),self.aries)

        if (not(isinstance(self.aries,str))):
            raise ValueError("{}.{}:  Aries File input is not a string.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        newList = self.aries.split('.')

        if len(newList[0])  <= 1:
            raise ValueError("{}.{}:  Aries File input is not GE than 1\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if newList[1] !=  "txt" :
            raise ValueError("{}.{}:  Aries File extension is not txt extension\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        self.ariesEntry = []

        fp =  open(self.aries,'r')
        data = csv.reader(fp,delimiter='\t')
        for row in data:
            self.ariesEntry.append([datetime.strptime(row[0],"%m/%d/%y"),int(row[1]),self.angle.setDegreesAndMinutes(row[2])])
        fp.close()

        self.ariesEntry.sort()

        return ariesAbsolutePath

    def setStarFile(self,star="star.txt"):
        self.star = star
        starAbsolutePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),self.star)

        if (not(isinstance(self.star,str))):
            raise ValueError("{}.{}:  Star File input is not a string.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        newList = star.split('.')
        if len(newList[0])  <= 1:
            raise ValueError("{}.{}:  Star File input is not GE than 1\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if newList[1] !=  "txt" :
            raise ValueError("{}.{}:  Star File extension is not txt extension\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        self.starEntry = []
        fp =  open(self.star,'r')
        data = csv.reader(fp,delimiter='\t')
        for row in data:
            self.starEntry.append([row[0],datetime.strptime(row[1],"%m/%d/%y"),self.angle.setDegreesAndMinutes(row[2]),row[3]])
        fp.close()
        self.starEntry.sort()
        return starAbsolutePath

    def getSightings(self):
        self.approximateLatitude = "0d0.0"
        self.approximateLongitude = "0d0.0"
        if (self.sight == None):
            raise ValueError("{}.{}:  sighting file is not set, it's None.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if (self.aries == None):
            raise ValueError("{}.{}:  sighting file is not set, it's None.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if (self.starFile == None):
            raise ValueError("{}.{}:  sighting file is not set, it's None.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
        timestampString = timeGMT.isoformat(' ')
        fp = open(self.log,'a')
        for item in self.sightData:
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

            obsevedAltitude = self.angle.setDegreesAndMinutes(string)

            tempAltitude = self.angle.setDegreesAndMinutes("0d0.1")

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
            for rowStar in self.starEntry:
                if rowStar[0] == item[2] and rowStar[1] == item[0] :
                    break
                SHAstar = rowStar[2]
                latitude = rowStar[3]
            for rowAries in self.ariesEntry:
                if rowAries[0] == item[2] and rowAries[1] == item[1].split(":")[0]:
                    hour  = rowAries[1] + 1
                    GHAaries1 = rowAries[3]
            for rowAries in self.ariesEntry:
                if rowAries[0] == item[2] and rowAries[1] == hour:
                    GHAaries2 = rowAries[3]
            GHAaries = GHAaries1 + math.abs(GHAaries2 - GHAaries1) * (int(item[1].split(":")[1])*60 + int(item[1].split(":")[2]))/3600
            longitude = SHAstar + GHAaries
            fp.write(latitude)
            fp.write("\t")
            newstring = ""
            newstring +=  str(int(longitude))
            newstring += "d"
            newstring += str(round(((longitude - int(longitude))*60),1))
            fp.write(newstring)
            fp.write("\n")

        timestamp = os.path.getmtime(self.log)
        timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
        timestampString = timeGMT.isoformat(' ')
        fp.write("LOG:\t")
        fp.write(timestampString)
        fp.write(":\t")
        fp.write("Sighting errors:")
        fp.write(":\t")
        fp.write(str(self.errorCount))
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
