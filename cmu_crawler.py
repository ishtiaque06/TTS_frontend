

from textblob import TextBlob

class Prosody():
    
    def __init__(self, sentence):
        self.s = sentence
        self.pron_list = []
        self.s_type = self.what_type(self.s)
        self.s_tagged = TextBlob(self.s).tags
        self.s_tagged_list = []
        for tuple in self.s_tagged:
            self.s_tagged_list.append(list(tuple))
            #print self.s_tagged_list
        #print self.s_tagged_list
        self.pron_string = ''
        self.phon_s = self.s_to_p(self.s)
        self.phon_s_stressed = ''
        self.sentence_prosody(self.s)
        #print self.phon_s_stressed

    def s_to_p(self, s):
        s = s.upper()
        s_list = s.split()[:-1]
        last_w = s.split()[-1]
        last_w = last_w.replace(last_w[-1], "")
        s_list.append(last_w)
        for w in s_list:
            self.pron_list.append(crawler(w))
        self.pron_string = " ".join(self.pron_list)
        #print self.pron_list
        return self.pron_string

    def what_type(self, s):
        if s[-1] == '?':
            return "question"
        elif s[-1] == '!':
            return "exclamation"
        else:
            return "statement"

    def sentence_prosody(self, s):
        #print self.phon_s
        if self.s_type == "question":
            index = 0
            while index < len(self.s_tagged_list):
                if self.s_tagged_list[index][1] in [u'PRP', u'NN', u'NNS', u'CD']:
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
        elif self.s_type == "exclamation":
            index = 0
            while index < len(self.s_tagged_list):
                s_w = self.stress_word(self.pron_list[index])
                self.phon_s_stressed += " " + self.stress_word(s_w)
                index += 1
            self.phon_s = self.phon_s_stressed
            return self.phon_s
        else:
            index = 0
            while index < len(self.s_tagged_list):
                if self.s_tagged_list[index][1] in [u'PRP', u'NN', u'NNS', u'CD']:
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
        
            
                    
    def stress_word(self, w):
        for c in w:
            if c in '0123456789':
                c_num = int(c)
                c_num += 1
                c_new = str(c_num)
                w_new = w.replace(c, c_new)
        return w_new

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
            
            
            
    def __repr__(self):
        return self.phon_s

def crawler(w):
    cmu = open("cmudict.0.7a.txt", 'r')
    #cmu_coop = open("cmu_extracted.txt", 'r+')
    index = 0
    for i in range(115):
        index += 1
        cmu.next()

    for line in cmu:
        if line.split()[0] == w:
            pronunciation = line.split()[1:]
            break
    #cmu_coop.close()
    cmu.close()
    pronunciation = ''.join(pronunciation)
    return pronunciation


def ui():
    s = raw_input("Enter the sentence you want to be converted to phonemes: ")
    s_list = s.split()
    output = Prosody(s)
    print output
    
ui()
