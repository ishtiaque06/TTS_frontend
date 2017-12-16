#The following line imports the textblob python library that is supposed to have been installed into the system.
from textblob import TextBlob

#This class handles sentence level prosody in the limited domain specified.
class Prosody():

    #The init function initializes the core variables and calls upon other functions in the class to apply prosodic markings.
    def __init__(self, sentence):
        self.s = sentence #Sentence in question. String type.
        self.pron_list = [] #List of sequence of pronunciation. List type. 
        self.s_type = self.what_type(self.s) #Determines the type of sentence. String type. 
        self.s_tagged = TextBlob(self.s).tags #This makes use of textblob to make a list of tuples.
        self.pron_string = '' #The string of pronunciation will be built from the CMU dictionary
        self.phon_s = self.s_to_p(self.s)#This stores the pronunciation string for use in the methods in the class. 
        self.phon_s_stressed = '' #This stores the stressed forms of the phoneme strings compared to the base stress present in individual words.
        self.sentence_prosody(self.s)#This method returns the final sentence with prosodic markings.

    #The following method converts every word present in a string to its corresponding phoneme mapping
    #and concatenates those individual words to form a "phonetic" sentence mapping.
    def s_to_p(self, s):
        s = s.upper()
        s_list = s.split()[:-1]
        last_w = s.split()[-1]
        last_w = last_w.replace(last_w[-1], "")
        s_list.append(last_w)
        for w in s_list:
            self.pron_list.append(crawler(w))
        self.pron_string = " ".join(self.pron_list)
        return self.pron_string

    #This method determines what type of sentence a given sentence is.
    def what_type(self, s):
        if s[-1] == '?':
            return "question"
        elif s[-1] == '!':
            return "exclamation"
        else:
            return "statement"

    #This method applies prosodic markings to the phonetic representation of the sentence.
    def sentence_prosody(self, s):
        print self.phon_s #Prints the initial phonetic sentence out.

        #If the sentence is a question, then this method increases stress on nouns, pronouns and cardinal numbers
        #and adds an addition stress on the last vowel of the sentence to indicate intonation rise.
        if self.s_type == "question":
            index = 0
            while index < len(self.s_tagged):
                if self.s_tagged[index][1] in [u'PRP', u'NN', u'NNS', u'CD']:
                    #print self.pron_list[index]
                    self.phon_s_stressed += " " + self.stress_word(self.pron_list[index])
                else:
                    self.phon_s_stressed += " " + self.pron_list[index]
                index += 1
            last_word = self.phon_s_stressed.split()[-1]
            sentence_minus_last_w = self.phon_s_stressed.split()
            sentence_minus_last_w = sentence_minus_last_w[:-1]
            stressed_last_word = self.stress_last_v(last_word)
            sentence_minus_last_w.append(stressed_last_word)
            self.phon_s_stressed = " ".join(sentence_minus_last_w)
            self.phon_s = self.phon_s_stressed
            return self.phon_s

        #If the sentence is an exclamation, then this method increases the stress level of every vowel by 2.
        elif self.s_type == "exclamation":
            index = 0
            while index < len(self.s_tagged):
                s_w = self.stress_word(self.pron_list[index])
                self.phon_s_stressed += " " + self.stress_word(s_w)
                index += 1
            self.phon_s = self.phon_s_stressed
            return self.phon_s

        #In the last case, the sentence is a statement and thus the nouns will receive the regular stress and
        #the last word will receive a decrease in stress by 1. 
        else:
            index = 0
            while index < len(self.s_tagged):
                if self.s_tagged[index][1] in [u'PRP', u'NN', u'NNS', u'CD']:
                    self.phon_s_stressed += " " + self.stress_word(self.pron_list[index])
                else:
                    self.phon_s_stressed += " " + self.pron_list[index]
                index += 1
            last_word = self.phon_s_stressed.split()[-1]
            sentence_minus_last_w = self.phon_s_stressed.split()
            sentence_minus_last_w = sentence_minus_last_w[:-1]
            stressed_last_word = self.destress_last_v(last_word)
            destressed_last_word = self.destress_last_v(stressed_last_word)
            sentence_minus_last_w.append(destressed_last_word)
            self.phon_s_stressed = " ".join(sentence_minus_last_w)
            self.phon_s = self.phon_s_stressed
            return self.phon_s
        
            
    #This method increases the stress level of vowels in a word by 1.                
    def stress_word(self, w):
        for c in w:
            if c in '0123456789':
                c_num = int(c)
                c_num += 1
                c_new = str(c_num)
                w_new = w.replace(c, c_new)
        return w_new

    #This method increases the stress level of the last vowel in a word by 1.
    def stress_last_v(self, w):
        w_new = w[::-1]
        for c in w_new:
            if c in '0123456789':
                c_num = int(c)
                c_num += 1
                c_new = str(c_num)
                w_new_stressed = w_new.replace(c, c_new)
        w = w_new_stressed[::-1]
        return w

    #This method decreases the stress level of the last vowel in a word by 1. 
    def destress_last_v(self, w):
        w_new = w[::-1]
        for c in w_new:
            if c in '0123456789':
                c_num = int(c)
                c_num = c_num - 1
                c_new = str(c_num)
                w_new_stressed = w_new.replace(c, c_new)
        w = w_new_stressed[::-1]
        return w
            
            
    #The repr function returns the phonetic string when the print function is called upon the Prosody object.    
    def __repr__(self):
        return self.phon_s

#This crawler scans through the CMU Dictionary to find mapping of a word to its phonetic representation.
def crawler(w):
    cmu = open("cmudict.0.7a.txt", 'r')
    index = 0
    for i in range(115):
        index += 1
        cmu.next()

    for line in cmu:
        if line.split()[0] == w:
            pronunciation = line.split()[1:]
            break
        else:
            print "the word ", w, " isn't in the CMU dictionary."
            break
    cmu.close()
    pronunciation = ''.join(pronunciation)
    return pronunciation


#Simple UI to input a sentence and return its phonetic representation.
def ui():
    y_or_n = "y"
    while y_or_n == "y":
        s = raw_input("Enter the sentence you want to be converted to phonemes: ")
        s_list = s.split()
        output = Prosody(s)
        print output
        y_or_n = raw_input("Do you want to test another sentence?(y/n)")
    
ui()
