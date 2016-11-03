import sys
import os
import re

# I CREATE AND INITIALIZE CLASS ANGLE:
class Angle:
    def __init__(self):  # Lines 24:29 of manual
        self.angle = 0.0
#II INSTANCE METHODS:
#setDegrees
    def setDegrees(self, degrees=0.0):
        if isinstance(degrees,str):
            raise ValueError("{}.{}:  degrees violates the parameter specifications" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        else:
            degrees = float(degrees)
            if ( degrees < 0):
                self.angle =  360 + (degrees % -360)
            else:
                self.angle = degrees % 360

        return self.angle
#setDegreesAndMinutes
    def setDegreesAndMinutes(self, angleString):
        # when null string:
        if angleString is None:
            raise ValueError("{}.{}:  angleString is not declared or emtry string passed" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        #d separator is missing:
        if "d" not in angleString:
            raise ValueError("{}.{}: d seperator missing in  angleString" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        x, y = angleString.split("d")

        if x == None:
            raise ValueError("{}.{}: degree can't be empty or blank" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        if y == None:
            raise ValueError("{}.{}: minute can't be empty or blank" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        if x.find('.') == True:
            raise ValueError("{}.{}:  degree must be integer" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        # decimal place exception
        if y[::-1].find('.') > 1:
            raise ValueError("{}.{}:  minute must have only one decimal point" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        try:
            x = float(x)
        except:
            raise ValueError("{}.{}:  could not convert string to" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        try:
            y = float(y)
        except:
            raise ValueError("{}.{}:  could not convert string to" .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
            
        if float(y) < 0.0 :
            raise ValueError("{}.{}:  minute must be positve " .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))

        if float(x) < 0.0:
            self.angle = 360 + (float(x) % -360)
            self.angle = self.angle - float(y)/60
        else:
            self.angle = float(x) %360
            self.angle = self.angle + float(y)/60

        return self.angle
#add method
    def add(self, angle=None):
        if (angle == None):
            raise ValueError("{}.{}: angle is not specified while calling this function." .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if (not(isinstance(angle,self.__class__))):
            raise ValueError("{}.{}: angle is not  a instance of Angle Class." .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        self.angle = (self.angle + angle.angle) % 360
        return self.angle

#subtract method
    def subtract(self, angle=None):
        if (angle == None):
            raise ValueError("{}.{}: angle is not specified while calling this function." .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if (not(isinstance(angle,self.__class__))):
            raise ValueError("{}.{}: angle is not  a instance of Angle Class." .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        self.angle = self.angle - angle.angle
        if self.angle < 0:
            self.angle = self.angle +360
        return self.angle

#compare method
    def compare(self, angle=None):
        if (angle == None):
            raise ValueError("{}.{}: angle is not specified while calling this function." .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if (not(isinstance(angle,self.__class__))):
            raise ValueError("{}.{}: angle is not  a instance of Angle Class." .format(self.__class__.__name__ ,sys._getframe().f_code.co_name))
        if self.angle < angle:
            raise ValueError("angle is not a valid instance of Angle")
            return -1
        if self.angle == angle.angle:
            return 0
        if self.angle > angle.angle:
            return 1
        if self.angle < angle.angle:
            return -1

#getString method
    def getString(self):
       return  str(int(self.angle)) + "d" + str(round(((self.angle - int(self.angle))*60),1))

#getDegrees method
    def getDegrees(self):
        return self.angle
