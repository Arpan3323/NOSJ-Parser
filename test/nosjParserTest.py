'''
Created on August 20, 2023

@author: Arpan Srivastava
'''

import sys
sys.path.append('.\Project1A')
import unittest
import subprocess
import Parser.nosjParser as njp

#   Analysis: Project1A.nosjParser
#        inputs:
#            file: a nosj formatted input file (passed as the first command line argument)
#        output: 
#            side-effects:
#
#            nominal: 
#                     deserealize the input file and print the description to standard output (stdout). 
#                     The description should be formatted as follows: "key-name -- type -- value" 
#                     (no trailing or leading spaces other than trailing newline).
#                     If the object is a map, In the case that a map is encountered, your implementation MUST leave 
#                     the value field of the above line empty and output a stand-alone line of "begin-map".
#                     When the end of a map is encountered, your implementation MUST output a stand-alone line of "end-map'.
#
#            abnormal: 
#                     if input errors are encountered, print a one line error message to standard error (stderr) and exit with
#                     a status code of 66. The error message must begin with the string "ERROR -- " (and end with a single trailing newline).
#
#   happy path tests:
#                100: valid file with an empty map. print " -- -- " to stdout
#                101: valid file with a nosj num object in a map. print "key-name -- type -- 0.0" to stdout
#                102: return true if the key is valid. map keys MUST be an ascii-string 
#                     consisting of one or more lowercase letters ("a" through "z") only
#                103: determine if the value is a num. num consists of the ascii-character "f", an
#                     optional ascii-dash representing a negative-sign ("-"), one or more
#                     ascii-digits ("0" through "9"), a decimal point, one or more ascii-digits ("0"
#                     through "9"), and the ascii-character "f"
#                104: unpack num and return the key and value
#                105: determine if the value is a simple-string. all ascii letters and numbers, 
#                     spaces (" " / 0x20), and tabs ("\t", 0x09)). Simple-strings are followed by a trailing "s"
#                106: unpack simple-string and return the key and value
#                107: determine if the value is a complex-string. Where as simple-string may only contain a 
#                     restricted set of bytes, complex-strings can encode arbitrary bytes but the marshalled-form MUST include
#                     at least one (1) percent-encoded byte (sometimes called "URL-encoding")
#                108: unpack complex-string and return the key and value
#                109: determine if the value is a map. A map is a sequence of zero or more key-value pairs, A nosj map MUST start with a two left angle-bracket ("<<") and end
#                     with two right angle-bracket (">>") and map keys MUST be an ascii-string
#                     consisting of one or more lowercase letters ("a" through "z") only. Map values
#                     may be any of the three canonical nosj data-types (map, string or num) and
#                     there is no specification-bound on how many maps may be nested within each
#                     other. Though map values are not required to be unique, map keys MUST be unique
#                     within the current map (though they may be duplicated in maps at other levels of "nesting")
#                111: unpack map and return the key and value when top level map has nested map
#                112: unpack nosj object with multiple key-value pairs
#                113: unpack nosj object with multiple key-value pairs and nested map
#                114: capture everything after the "." when a num is unpacked
#
#    sad path tests:
#                901: file not found. print "ERROR -- Invalid file name. Please re-check the file name and try again." to stderr and exit with status code 66
#                902: Catch map with duplicate keys. print "ERROR -- Duplicate key" to stderr and exit with status code 66
#                903: Catch invalid nested map. print "ERROR -- Invalid nested map" to stderr and exit with status code 66
#                904: Catch multiple colons in a key-value pair. print "ERROR -- Invalid key-value pair" to stderr and exit with status code 66
#                905: Catch invalid key. print "ERROR -- Invalid key" to stderr and exit with status code 66
#                906: Catch file with multiple nosj objects. print "ERROR -- Invalid file" to stderr and exit with status code 66
#    evil path test:
#                none


class nosjParserTest(unittest.TestCase):
    
    def test901_invalidFile(self):
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'nosjParserTest901.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print("STDOUT:", result.stdout.decode('utf-8'))
        #print("STDERR:", result.stderr.decode('utf-8'))
        self.assertEqual(result.returncode, 66)
        self.assertEqual(result.stderr.decode('utf-8'), 'ERROR -- Invalid file name. Please re-check the file name and try again.\r\n')

    def test100_emptyMap(self):
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'Project1A\inputs\\nosjParserTest100.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.stdout.decode('utf-8'), 'begin-map\r\n -- -- \r\nend-map\r\n')

    def test101_basicNumObject(self):
        #exceptedResult = sys.stdout.write("key-name -- type -- 0.0\n")
        #actualResult = njp.readFile('<<abc:f0.0f>>')
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'Project1A\inputs\\nosjParserTest101.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.stdout.decode('utf-8'), 'begin-map\r\nabc -- num -- 0.0\r\nend-map\r\n')
        #self.assertEqual(actualResult, exceptedResult)
    
    def test102_validKey(self):
        actualResult = njp.validateKey('abc')
        self.assertEqual(actualResult, True)

    def test102_0_invalidKey(self):
        actualResult = njp.validateKey('ABC')
        self.assertEqual(actualResult, False)

    def test103_validNum(self):
        actualResult = njp.validateNum('f0.0f')
        self.assertEqual(actualResult, True)

    def test103_0_invalidNum(self):
        actualResult = njp.validateNum('f0.0')
        self.assertEqual(actualResult, False)
    
    def test103_1_invalidNum(self):
        actualResult = njp.validateNum('f0.0f0')
        self.assertEqual(actualResult, False)

    def test104_unpackNumAndReturnKeyAndValue(self):
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'Project1A\inputs\\nosjParserTest104.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.stdout.decode('utf-8'), 'begin-map\r\nab -- num -- -5678.0\r\nend-map\r\n')

    def test105_validSimpleString(self):
        actualResult = njp.validateSimpleString('ef ghs')
        self.assertEqual(actualResult, True)

    def test106_unpackSimpleStringAndReturnKeyAndValue(self):
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'Project1A\inputs\\nosjParserTest106.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.stdout.decode('utf-8'), 'begin-map\r\nx -- string -- abcd\r\nend-map\r\n')
    
    def test107_validateComplexString(self):
        actualResult = njp.validateComplexString('ab%2C%00cd')
        self.assertEqual(actualResult, True)

    def test108_unpackComplexStringAndReturnKeyAndValue(self):
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'Project1A\inputs\\nosjParserTest108.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.stdout.decode('utf-8'), 'begin-map\r\nx -- string -- ab,cd\r\nend-map\r\n')

    def test109_validMap(self):
        actualResult = njp.validateMap('<<x:<<y:f1.23f>>>>')
        self.assertEqual(actualResult, True)

    def test110_unpackMapAndReturnKeyAndValueWhenTopLevelMapHasNestedMap(self):
        exceptedResult = {'x': '<<y:f1.23f>>'}
        actualResult = njp.unpackObject('<<x:<<y:f1.23f>>>>')
        self.assertEqual(actualResult, exceptedResult)
    
    def test111_readFileWhenTopLevelMapHasNestedMap(self):
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'Project1A\inputs\\nosjParserTest111.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.stdout.decode('utf-8'), 'begin-map\r\nx -- map --\r\nbegin-map\r\ny -- num -- 1.23\r\nend-map\r\nend-map\r\n')
        
    def test112_unpackNosjObjectWithMultipleKeyAndValuePairs(self):
        actualResult = njp.unpackObject('<<abc:f0.0f,def:t ars>>')
        expectedResult = {'abc':'f0.0f', 'def':'t ars'}
        self.assertEqual(actualResult, expectedResult)

    def test113_unpackNosjObjectWithMultipleKeyAndValuePairsAndNestedMap(self):
        actualResult = njp.unpackObject('<<abc:f0.0f,def:t ars,ghi:<<jkl:f0.0f>>>>')
        expectedResult = {'abc':'f0.0f', 'def':'t ars', 'ghi':'<<jkl:f0.0f>>'}
        self.assertEqual(actualResult, expectedResult)

    def test902_duplicateKey(self):
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'Project1A\inputs\\nosjParserTest902.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 66)
        self.assertEqual(result.stderr.decode('ascii'), 'ERROR -- Duplicate key found: s\r\n')
    
    def test903_invalidNestedMap(self):
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'Project1A\inputs\\nosjParserTest903.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 66)
        self.assertEqual(result.stderr.decode('utf-8'), 'ERROR -- Invalid value found: <<a:09s>\r\n')

    def test904_invalidKeyValuePairs(self):
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'Project1A\inputs\\nosjParserTest904.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 66)
        self.assertEqual(result.stderr.decode('utf-8'), 'ERROR -- Invalid data format with key: a and value: :abcs\r\n')
    
    def test905_invalidKey(self):
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'Project1A\inputs\\nosjParserTest905.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 66)
        self.assertEqual(result.stderr.decode('utf-8'), 'ERROR -- Invalid key found: ABC\r\n')

    def test906_invalidFile(self):
        result = subprocess.run(['python', 'Project1A\Parser\\nosjParser.py', 'Project1A\inputs\\nosjParserTest906.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 66)
        self.assertEqual(result.stderr.decode('utf-8'), 'ERROR -- Invalid file format. Please re-check the file and try again.\r\n')

    def test114_captureEverythingAfterTheDot(self):
        actualResult = njp.unpackNum('f0.0001f')
        self.assertEqual(actualResult, '0001')

    def test115_removeDotAndEverythingAfterIfItAllZeroes(self):
        actualResult = njp.unpackNum('f55.0000f')
        self.assertEqual(actualResult,'55')

    def test000_randomTest(self):
        actualResult = njp.unpackObject('<<abc:f0.0f>>')
        actualResult2 = njp.readFile('<<x:abcds,y:Arpans,goals:<<a:Insterstellar Travels,b:Unlocking314s,x:%3C%61%68%72%65%66%3E,c:<<h:<<>>>>>>>>')

        self.assertEqual(actualResult, ('abc','f0.0f'))

    def test001_randomTest(self):
        #actualResult = njp.unpackObject('<<abc:<<a:f0.0f>>>>')
        #self.assertEqual(actualResult, ('abc','<<a:f0.0f>>'))
        actualResult = njp.validateComplexString('<<abc:<<a:f0.0f>>')


if __name__ == "__main__":
    unittest.main()