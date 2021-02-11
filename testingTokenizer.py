import unittest
from tokenizer import Tokenizer
from bs4 import BeautifulSoup

class TestStringMethods(unittest.TestCase):
    # Just the function itself without tokenizing
    def testLemmatize(self):
        index = Tokenizer()
        self.assertEquals(index.lemmatize("cars"), 'car')
        self.assertEquals(index.lemmatize("OcToPi"), 'octopus')
        self.assertEquals(index.lemmatize("informatics"), 'informatics')
        self.assertEquals(index.lemmatize("cars"), 'car')
        self.assertEquals(index.lemmatize("caresses"), 'caress')
        self.assertEquals(index.lemmatize("ponies"), 'pony')
        self.assertEquals(index.lemmatize("mass"), 'mass')
        self.assertEquals(index.lemmatize("gas"), 'gas')

    def testLemmatizeWithTokeinze(self):
        index = Tokenizer()
        tmp = ["cars'", "car's", "cars"]
        self.assertEquals(index.tokenize(tmp), ["car", "car", "car"])
    
    def testLemmatizeWithTokeinze2(self):
        index = Tokenizer()
        tmp = ["donkeys's"]
        self.assertEquals(index.tokenize(tmp), ["donkey"])

    def testLemmatizeWithStopWorks(self):
        index = Tokenizer()
        tmp = ["s", "the"]
        self.assertEquals(index.tokenize(tmp), [])

    def testComputeFreq1(self):
        index = Tokenizer()
        tmp = ["chicken" , "chicken" , "chicken", "chicken", "chicken"]
        self.assertEquals(index.computeWordFrequencies(tmp), {'chicken' : 5})       

    def testComputeFreq2(self):
        index = Tokenizer()
        tmp = ["nuggets" , "chicken" , "chicken", "chicken", "chicken"]
        self.assertEquals(index.computeWordFrequencies(tmp), {'chicken' : 4, 'nuggets' : 1 })

    def testComputeFreq3(self):
        index = Tokenizer()
        tmp = ["didnt" , "didn't" , "didn't", "didn't","didn't", "didnt'"]
        some_list = index.tokenize(tmp)
        self.assertEquals(index.computeWordFrequencies(some_list), {}) 

    def testComputeFreq4(self):
        index = Tokenizer()
        tmp = ["Alexs", "Alex's"]
        some_list = index.tokenize(tmp)
        self.assertEquals(index.computeWordFrequencies(some_list), {"Alex's" : 1})          
        
    def testComputeFreq5(self):
        index = Tokenizer()
        tmp = ["can't" , "cant" , "cant'"]
        some_list = index.tokenize(tmp)
        self.assertEquals(index.computeWordFrequencies(some_list), {"cant" : 2})
    
    def badCharacters(self):
        r = """BloxExpV01  �ObjSStch   T   	c  c  c  c  c  c  c  c  	c  
            c  c  c  
            c  c  c  c  c  	   	thumbnail# � x c  c  	   
            os-version	   1093	   author	    	   language	   en	   history	   H2011-2-1 10:25:17	save	Tag Game		
            2014-6-21 15:23:55	save	TagGame (2)		
                scratch-version	   3.1.1 (19-May-11)	   	penTrails"�h  c  	   keepOnStage	   platform	   Mac OS  ^����>>>>�>>>>/>>>�>>>>/!>>>>/�>/>!>>!�>!!!>!/!>>>�>>
            >>!>/!/>>>�>>/!!>>>/>>�>>/>>>/9>>>>,>>U>/>>!>>>1>>>>>>>>>U>!4!>>5>>>>	>>>>U>>!>>!>>>>/>->>>>a>>!#>>>>>>>>!!->>>>a>(>>>>/!//�>/>>>>>/>>/>>>�>!/>>>>>>>>>/>>5>>>,>M>!>>>>>/>>>>>>>/>>
            !>5>>>>I>#>>>+63>>>!!>>>>>>>>>>>
            
            !>5>>>>I>>> 	$!/	>>>!>>/>!/>>5>>>>I>>>760/>	>>>>/!!->>,>>	>>>>I>>>*)3>>>>>>>>>>/>>/!!!>->>>>	>>>>I>>>!!>>>	>!/>>>->>>>	>>>>I>>> !>!!>>>>>>>>>!>>>>>>!!->>>M>>>"!>/>>>>>/!!!!>>>>>>>!�>>>>/!!>>>>!>	>>/!/>>>�>!>>!>>>!!>>	>>!>>>�>>>>!>
            >>>	>>>99>>�>>/>>>/>>>	>>>!!!/>>�>>>>/M>>A>>!!!!>>M>>>>>>>>>>>A>!/!!>>M>>>>>>>>>>>=>>>>/>>>!!>M>>>>>>>>>>>=>>>>!!/>>!>M>>>>>>>>>>>=>>>>/9>>!>>>>>I>>>>>>>>>>>A>/>>!->>I>>>>>>>>>>>E>>>/!!!>>I>>>>>>>>>>>�>>>>>>>>>>>�>>>>>>>>>>>�>>,	�>>>>'!>>>y>>%1%'>>>>,�>2122112>�>>2>>;1'>>>>y>>>>&;;1>>>>>>>y>>>2;>;1'>>
            >>>>	>>>>e>>>	>>>%>>';;2>>>>2	>>>>	>>>>y>>>>'>>>;;>>>%	>>>>	>>>>y>>>>;2>;;;>>1'>>>>>>>>>>	>>>>y>>>>%;2>;;;;&>;>>>>>>>>>>	>>>>y>>>>;;1	;>>>>>>>>>>	>>>>y>>%
            ;>>>>>>>>>>	>>>>y>>;;
            ;1'>>>>>>>>>�>>>;
            ;;>>>>>>>>>�>>>'1
            ;;%2>>>>>>,}>>>>%
            ;;;>y>>>	>>>2%
            ;;;1>�>>>;
            ;;;;�>>';;
            ;;;;%�>>;;;;;;;;8;;2>>>�>2%;;1%;;::;;;.;112>>�>>>>21;;;;;;;88;;;;<5=;%;>>�>>>>%;;;
            ;;;;;%>>�>>>;;;;
            ;;;11;;>>�>>>;;;	;;%%;;;''1%>>�>>>2%>>
            ;%>>�>>>>2;;;%;;;;;�>1;%;%%'>>�>;%2;&2;>>>�>>2%'>>>>>�	>>>	>>>�>>>>	>>>>�>>>>	>>>>�>>>>	>>>>�>>>>	>>>>�>>>>	>>>>�>>>>	>>>>�>>>>	>>>>�>>>>	>>>>�>>>>	>>>>�>>>	,>>>�>   c  c  c  c  c  c  c  c  c  c  c   c  !c  "c  #c  $c  %c  &c  'c  (c  )c  *c  +c  ,c  -c  .c  /c  0c  1c  2c  3c  4c  5c  6c  7c  8c  9c  :c  ;c  <c  =c  >c  ?c  @c  Ac  Bc  Cc  Dc  Ec  Fc  Gc  Hc  Ic  Jc  Kc  Lc  Mc  Nc  Oc  Pc  Qc  Rc  Sc  Tc  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c  c    
"""
        soup = BeautifulSoup(r, "html.parser")
        unprocessed_list = list(soup.getText().lower().split())
        index = Tokenizer()
        self.assertEquals(index.tokenize(unprocessed_list), [])



if __name__ == '__main__':
    unittest.main()