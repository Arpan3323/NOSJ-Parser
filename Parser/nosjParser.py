#!/usr/bin/python3
'''
Created on August 20, 2023

@author: Arpan Srivastava
'''
import subprocess
import sys
import re
import urllib.parse

def readFile(fileContents):
    writeToStdout = "begin-map\n"
    for key, value in unpackObject(fileContents).items():
        if checkEmptyMap(key, value):
            writeToStdout += ""
        elif validateKey(key):
            if validateMap(value):
                writeToStdout += f"{key} -- map -- " + "\n"
                writeToStdout += readFile(value)
            elif validateNum(value):
                parsedNum = unpackNum(value)
                writeToStdout += f"{key} -- num -- {parsedNum}" + "\n"
            elif validateSimpleString(value):
                parsedString = unpackSimpleString(value)
                writeToStdout += f"{key} -- string -- {parsedString}" + "\n"
            elif validateComplexString(value):
                parsedString = unpackComplexString(value)
                writeToStdout += f"{key} -- string -- {parsedString}" + "\n"
            else:
                sys.stderr.write(f"ERROR -- Invalid data format with key: {key} and value: {value}\n")
                exit(66)
        else:
            sys.stderr.write(f"ERROR -- Invalid key found: {key}\n")
            exit(66)
    writeToStdout += "end-map\n"
    return writeToStdout

def writeToStdout(parsedObject):
    parsedObject += parsedObject 

def validateKey(key):
    pattern = r'^[a-z]+$'
    return bool(re.match(pattern, key))

def validateNum(num):
    pattern = r'^f-?[0-9]+\.[0-9]+f$'
    return bool(re.match(pattern, num))
    
def unpackNum(num):
    numWithoutFIdentifier = num.replace('f', '')
    separateNumByDot = numWithoutFIdentifier.split('.')
    if all(nums == '0' for nums in separateNumByDot[1]):
        return separateNumByDot[0]
    return numWithoutFIdentifier

def validateSimpleString(simpleString):
    pattern = r'^[a-zA-Z0-9\s\t]*s$'
    return bool(re.match(pattern, simpleString))

def unpackSimpleString(simpleString):
    return "" if simpleString == "s" else simpleString[:-1]

def unpackComplexString(complexString):
    return urllib.parse.unquote(complexString)

def validateMap(map):
    pattern = r'^<<.*>>$'
    return bool(re.match(pattern, map))

def validateComplexString(complexString):
    pattern = r'%[0-9A-F]{2}'
    searchIndexes = []
    if complexString.count("<") > 0 or complexString.count(">") > 0:
        return False
    if '%' in complexString:
        for i in range(len(complexString)):
            if complexString[i:i+1] == '%':
                searchIndexes.append(i)
        for index in searchIndexes:
            if index + 3 > len(complexString):
                return False
            
            match = re.match(pattern, complexString[index:index+3])
            if not match:
                return False
        
        return True

def unpackObject(fileContents):
    if not validateMap(fileContents):
        sys.stderr.write(f"ERROR -- Invalid value found: {fileContents}\n")
        exit(66)
    contentDictionary = {}
    removedTopMap = re.sub(r'^<<(.*)>>$', r'\1', fileContents)
    if ',' in removedTopMap:
        return unpackCommaSeparatedPairs(removedTopMap)
    if removedTopMap == "":
        contentDictionary[""] = removedTopMap
    else:
        keyValuePairs = removedTopMap.split(':', 1)
        if len(keyValuePairs) != 2:
            sys.stderr.write(f"ERROR -- Invalid value map formatting found\n")
            exit(66)
        contentDictionary[keyValuePairs[0]] = keyValuePairs[1]
    return contentDictionary
    
def unpackCommaSeparatedPairs(removedTopMap):
    commaSeparatedContent = {}
    keyValuePairs = splitCommasButPreserveMaps(removedTopMap)
    uniqueKeys = set()
    for pair in keyValuePairs:
        if pair == "" or len(pair) < 2:
            sys.stderr.write(f"ERROR -- Invalid value found: {pair}\n")
            exit(66)
        key, value = pair.split(':', 1)
        if key in uniqueKeys:
            sys.stderr.write(f"ERROR -- Duplicate key found: {key}\n")
            exit(66)
        uniqueKeys.add(key)
        commaSeparatedContent[key] = value
    return commaSeparatedContent

def splitCommasButPreserveMaps(text):
    keyValuePairs = []
    current = ''
    stack = []
    for char in text:
        current += char
        if char == ',' and not stack:
            keyValuePairs.append(current.strip().replace(',', ''))
            current = ''
        if char == '<':
            stack.append(char)
        elif char == '>':
            if stack:
                stack.pop()
    if current:
        keyValuePairs.append(current.strip())
    return keyValuePairs

def checkEmptyMap(key, value):
    if key == "" and value == "":
        return True

def main():
    error = sys.stderr
    output = sys.stdout
    if len(sys.argv) != 2:
       error.write("ERROR -- Invalid number of arguments\n")
       exit(66)
    fileToRead = sys.argv[1]
    try:
        file = open(fileToRead, "r")
        fileContents = file.read()
    except Exception as e:
        error.write(f"ERROR -- Invalid file. Please re-check the file and try again.\n")
        exit(66)
    
    #outputFile = open("tc-1.output", "w")
    #outputFile.write(readFile(fileContents.strip()))
    output.write(readFile(fileContents.strip()))
        
if __name__ == "__main__":
    main()