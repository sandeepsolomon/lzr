import sys
import os
import re

# I CREATE AND INITIALIZE CLASS ANGLE:
class Angle:
#constructor:
    def __init__(self, angle="0d0"):  # Lines 24:29 of manual
        self.angle = angle

#II INSTANCE METHODS:
#setDegrees
    def setDegrees(self, degrees):
        if degrees.isdigit == False:
            raise ValueError("degrees violates the parameter specifications")
        else:
            self.__degrees = float(degrees)%360

#setDegreesAndMinutes
    def setDegreesAndMinutes(self, angleString):
        # when null string:
        if angleString is None:
            raise TypeError("null string")
        #d separator is missing:
        if "d" not in angleString:
            raise ValueError("d separator is missing")

        x, y = angleString.split("d")

        if x.isint() == False:
            raise ValueError("degrees must be an integer")

        if y.isint() == False:
            raise ValueError("degrees must be an integer")

        if y<0:
            raise ValueError("minutes must be positive")

        # missing degrees
        if x is None:
            raise ValueError("missing degrees")
        # missing degrees
        if y is None:
            raise ValueError("null minutes")

        # decimal place exception
        if y[::-1].find('.') > 1:
            raise ValueError("minutes must have only one decimal place")

        else:
            return angleString

#add method
    def __add__(self, angle):
        return self.angle + angle

#subtract method
    def __sub__(self, angle):
        return Angle(angle - self.angle)

#compare method
    def __cmp__(self, angle):
        if self.angle < angle:
            raise ValueError("angle is not a valid instance of Angle")
            return -1
        if self.angle == angle:
            return 0
        if self.angle > angle:
            return 1

#getString method
    def getString(self):
        return self.__String

#getDegrees method
    def getDegrees(self):
        return self.__Degrees