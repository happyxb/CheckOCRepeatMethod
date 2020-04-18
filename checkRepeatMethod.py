#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys

class OCMethod(object):
    """docstring for OCMethod"""
    def __init__(self, methodType, methodName, categoryName):
        super(OCMethod, self).__init__()
        self.methodType = methodType
        self.methodName = methodName
        self.categoryName = categoryName


    def __str__(self):
        name = "{}[{}] ({})".format(self.methodType, self.methodName, self.categoryName)
        return name

    def __eq__(self, other):
        return self.methodName == other.methodName and self.methodType == other.methodType and self.categoryName == other.categoryName

class OCClass(object):
    """docstring for OCClass"""
    
    def __init__(self, className):
        super(OCClass, self).__init__()
        self.className = className
        self.methodList = []

    def addMethod(self, newMethod):
        if newMethod not in self.methodList:
            self.methodList.append(newMethod)

    def checkMethod(self):
        methodMap = {}
        for method in self.methodList:
            methodKey = method.methodType + method.methodName
            if methodKey in methodMap:
                mapList = methodMap[methodKey]
            else:
                mapList = []
            mapList.append(method)
            methodMap[methodKey] = mapList

        # print(methodMap)
        for mapList in list(methodMap.values()):
            if len(mapList) > 1:
                for method in mapList:
                    name = "{}[{} {}] ({})".format(method.methodType, self.className, method.methodName, method.categoryName)
                    print(name)

        
def searchFile(fileName):
    classMap = {}
    f = open(fileName, "r")
    for line in f.readlines():
        # print ("读取的数据为: %s" % (line))
        methodType = line[0]
        pattern = re.compile(r'\[.*\(')
        className = pattern.search(line).group(0)[1:-1]
        pattern = re.compile(r'\(.*\)')
        categoryName = pattern.search(line).group(0)[1:-1]
        pattern = re.compile(r' .*\]$')
        methodName = pattern.search(line).group(0)[1:-1]
        # print(methodType, className, categoryName, methodName)

        if className in classMap:
            currentClass = classMap[className]
        else:
            currentClass = OCClass(className)
        # print(currentClass.className, len(currentClass.methodList))

        newMethod = OCMethod(methodType, methodName, categoryName)
        currentClass.addMethod(newMethod)
        # print(currentClass.className, len(currentClass.methodList))
        classMap[className] = currentClass

    f.close()

    for currentClass in list(classMap.values()):
        currentClass.checkMethod()



fileName = sys.argv[1]
# print("fileName", fileName)
searchFile(fileName)