from datetime import datetime
from datetime import timedelta
import xml.etree.ElementTree as ET
import Angle as Angle
import sys
import os
import time
import pytz
import math
import csv

class Fix:
    def __init__(self,logFile="log.txt"):
        self.log = logFile
        self.sight = None
        self.angle = Angle.Angle()
        self.sightData = None
        self.ariesEntry = []
        self.starEntry = []
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

        logAbsolutePath = os.path.join(os.getcwd(),self.log)
        fp  = open(self.log,'a')
        fp.write("LOG:\t")
        fp.write(timestampString)
        fp.write(":\t")
        fp.write("Log file: ")
        fp.write(logAbsolutePath)
        fp.write("\n")
        fp.close()

    def setSightingFile(self,sightingFile=None):
        self.errorCount = 0
        self.sight = sightingFile
        if self.sight == None:
            raise ValueError("{}.{}:  sightingFile input is None\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if(not(isinstance(self.sight,str))):
            raise ValueError("{}.{}:  sighting file input is not a string.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        part = self.sight.split('.')
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
        sightingAbsolutePath = os.path.join(os.getcwd(),self.sight)
        fp =  open(self.log,'a')
        fp.write("LOG:\t")
        fp.write(timestampString)
        fp.write(":\t")
        fp.write("Sighting file: ")
        fp.write(sightingAbsolutePath)
        fp.write("\n")
        fp.close()

        filetree = ET.parse(self.sight)
        rootNode = filetree.getroot()
        for child in rootNode.findall('sighting'):
            checkFlag=0
            if child.find('body') == None :
                self.errorCount += 1
                rootNode.remove(child)
                continue

            if child.find('body').text ==  None:
                self.errorCount += 1
                rootNode.remove(child)
                continue

            if len(child.find('body').text) == 0 :
                self.errorCount += 1
                rootNode.remove(child)
                continue

            if child.find('date') == None :
                self.errorCount += 1
                rootNode.remove(child)
                continue

            if child.find('date').text == None :
                self.errorCount += 1
                rootNode.remove(child)
                continue

            string = child.find('date').text.split('-')
            if int(string[1]) >12 or int(string[1]) < 01 or int(string[2]) > 31 or int(string[2]) >29 and int(string[1]) ==02 :
                self.errorCount += 1
                rootNode.remove(child)
                continue

            if child.find('time') == None :
                self.errorCount += 1
                rootNode.remove(child)
                continue

            if len(child.find('time').text) ==  0 :
                self.errorCount += 1
                rootNode.remove(child)
                continue

            string = child.find('time').text.split(':')
            if len(string) == 1:
                self.errorCount += 1
                rootNode.remove(child)
                continue


            if child.find('observation') == None :
                self.errorCount += 1
                rootNode.remove(child)
                continue

            if len(child.find('observation').text) ==  0 :
                self.errorCount += 1
                rootNode.remove(child)
                continue

            string = child.find('observation').text.lstrip(' ').rstrip(' ')
            string = string.lstrip(' ')
            string = string.rstrip(' ')

            if string.find("d") == -1:
                self.errorCount += 1
                rootNode.remove(child)
                continue

            if child.find('temperature') != None and child.find('temperature').text != None and (int(child.find('temperature').text) < -20 or int(child.find('temperature').text) > 120 ):
                self.errorCount += 1
                rootNode.remove(child)
                continue

            if child.find('horizon') != None and child.find('horizon').text != None and ( child.find('horizon').text.lower() != 'artificial' and child.find('horizon').text.lower() != 'natural' ):
                self.errorCount += 1
                rootNode.remove(child)
                continue

            if child.find('height') != None and child.find('height').text != None and child.find('height').text.find(".") == -1:
                self.errorCount += 1
                rootNode.remove(child)
                continue

            if child.find('pressure') != None and child.find('pressure').text != None and child.find('pressure').text.find(".") != -1:
                self.errorCount += 1
                rootNode.remove(child)
                continue

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
                tempList.append(float(item.find('height').text))
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
                tempList.append(float(item.find('pressure').text))
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

    def setAriesFile(self,ariesFile=None):
        self.aries = ariesFile
        if self.aries == None:
            raise ValueError("{}.{}:  Aries File None.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if (not(isinstance(self.aries,str))):
            raise ValueError("{}.{}:  Aries File input is not a string.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        newList = self.aries.split('.')
        if len(newList)  == 1:
            raise ValueError("{}.{}:  Aries File is missing extention\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if len(newList[0])  <= 1:
            raise ValueError("{}.{}:  Aries File input is not GE than 1\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if newList[1] !=  "txt" :
            raise ValueError("{}.{}:  Aries File extension is not txt extension\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if os.path.exists(self.aries):
            fp =  open(self.aries,'r')
            data = csv.reader(fp,delimiter='\t')
            for row in data:
                self.ariesEntry.append((row[0],int(row[1]),self.angle.setDegreesAndMinutes(row[2])))
            fp.close()
        else:
            raise ValueError("{}.{}:  Aries File path doesn not exist\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        ariesAbsolutePath = os.path.join(os.getcwd(),self.aries)
        timestamp = os.path.getmtime(self.log)
        timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
        tmpString = timeGMT.isoformat(' ')
        fp = open(self.log,'a')
        fp.write("LOG:\t")
        fp.write(tmpString)
        fp.write(":\t")
        fp.write("Aries file: ")
        fp.write(ariesAbsolutePath)
        fp.write("\n")
        fp.close()

        return ariesAbsolutePath

    def setStarFile(self,starFile=None):
        self.star = starFile
        if self.star == None:
            raise ValueError("{}.{}:  Star File is None .\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        if (not(isinstance(self.star,str))):
            raise ValueError("{}.{}:  Star File input is not a string.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        newList = self.star.split('.')
        if len(newList) == 1:
            raise ValueError("{}.{}:  Star File extention is missing\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if len(newList[0])  <= 1:
            raise ValueError("{}.{}:  Star File input is not GE than 1\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if newList[1] !=  "txt" :
            raise ValueError("{}.{}:  Star File extension is not txt extension\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if os.path.exists(self.star):
            fp =  open(self.star,'r')
            data = csv.reader(fp,delimiter='\t')
            for row in data:
                self.starEntry.append((row[0],row[1],self.angle.setDegreesAndMinutes(row[2]),row[3]))
            fp.close()
        else:
            raise ValueError("{}.{}:  Star File Path doesn't exist\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        self.starEntry.sort()

        starAbsolutePath = os.path.join(os.getcwd(),self.star)
        timestamp = os.path.getmtime(self.log)
        timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
        tmpString = timeGMT.isoformat(' ')

        fp = open(self.log,'a')
        fp.write("LOG:\t")
        fp.write(tmpString)
        fp.write(":\t")
        fp.write("Star file: ")
        fp.write(starAbsolutePath)
        fp.write("\n")
        fp.close()

        return starAbsolutePath

    def getSightings(self):
        self.approximateLatitude = "0d0.0"
        self.approximateLongitude = "0d0.0"

        if (self.sight == None):
            raise ValueError("{}.{}:  sighting file is not set, it's None.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if len(self.ariesEntry) == 0:
            raise ValueError("{}.{}:  Aries file is not set, it's None.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if len(self.starEntry) == 0:
            raise ValueError("{}.{}:  star file is not set, it's None.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        fp = open(self.log,'a')
        for item in self.sightData:
            string = item[3][0].lstrip(' ').rstrip(' ')
            obsevedAltitude = self.angle.setDegreesAndMinutes(string)
            tempAltitude = self.angle.setDegreesAndMinutes("0d0.1")

            if obsevedAltitude < tempAltitude:
                raise ValueError("{}.{}: observedAltitude is LE 0.1 arc minute.\n" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))


            if item[3][4].lower() == "natural":
                dip = (-0.97*math.sqrt(float(item[3][1])))/60
            else:
                dip = 0

            refraction  = (-0.00452*float(item[3][3]))/(273+int(item[3][2]))/math.tan(math.radians(obsevedAltitude))
            adjustedAltitude = obsevedAltitude + dip + refraction
            adjustStr = ""
            adjustStr +=  str(int(adjustedAltitude))
            adjustStr += "d"
            adjustStr += str(round(((adjustedAltitude - int(adjustedAltitude))*60),1))

            timestamp = os.path.getmtime(self.log)
            timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
            tmpString = timeGMT.isoformat(' ')

            fp.write("LOG:\t")
            fp.write(tmpString)
            fp.write(":\t")
            fp.write(item[2])
            fp.write("\t")
            fp.write(item[0])
            fp.write("\t")
            fp.write(item[1])
            fp.write("\t")
            fp.write(adjustStr)
            fp.write("\t")

            index = None
            latitude = "0d0.0"
            longitude = 0.0
            for i in range(len(self.starEntry)):
                Date = datetime.strftime(datetime.strptime(self.starEntry[i][1], "%m/%d/%y").date(),"%Y-%m-%d")
                if self.starEntry[i][0] == item[2]:
                    if Date == item[0]:
                        index = i
                        break
                    elif Date < item[0]:
                        index = i
            if index != None:
                flag = True
                for i in range(len(self.ariesEntry)):
                    Date = datetime.strftime(datetime.strptime(self.ariesEntry[i][0], "%m/%d/%y").date(),"%Y-%m-%d")
                    if  Date == item[0] and int(self.ariesEntry[i][1]) == int(item[1].split(":")[0]) and flag == True:
                        if (int(self.ariesEntry[i][1]) + 1) % 24 == 0:
                            storeHour = 0
                            fixedDate = datetime.strftime((datetime.strptime(self.ariesEntry[i][0], "%m/%d/%y").date() + timedelta(days=1)),"%Y-%m-%d")
                        else:
                            storeHour = int(self.ariesEntry[i][1])+1
                            fixedDate = datetime.strftime(datetime.strptime(self.ariesEntry[i][0], "%m/%d/%y").date(),"%Y-%m-%d")
                        GHA_aries1 = self.ariesEntry[i][2]
                        flag = False
                    if flag == False and Date == fixedDate and int(self.ariesEntry[i][1]) == storeHour:
                        storeHour = self.ariesEntry[i][1]
                        GHA_aries2 = self.ariesEntry[i][2]
                SHA_star = self.starEntry[index][2]
                latitude = self.starEntry[index][3]
                GHA_aries = GHA_aries1 + float(math.fabs(GHA_aries2 - GHA_aries1)) * float((int(item[1].split(":")[1])*60 + int(item[1].split(":")[2])))/3600
                longitude = (SHA_star + GHA_aries) % 360
                string = ""
                string +=  str(int(longitude))
                string += "d"
                string += str(round(((longitude - int(longitude))*60),1))

                fp.write(latitude)
                fp.write("\t")
                fp.write(string)
                fp.write("\n")
            else:
                fp.write("\n")

        timestamp = os.path.getmtime(self.log)
        timeGMT = datetime.fromtimestamp(timestamp, pytz.timezone('Etc/GMT+6'))
        tmpString = timeGMT.isoformat(' ')
        fp.write("LOG:\t")
        fp.write(tmpString)
        fp.write(":\t")
        fp.write("Sighting errors:")
        fp.write("\t")
        fp.write(str(self.errorCount))
        fp.write("\n")

        fp.close()
        return (self.approximateLatitude,self.approximateLongitude)
