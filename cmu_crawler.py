from textblob import TextBlob

class prosody():
    def __init__(self, sentence):
        self.s = sentence
        self.markedup = []
        s_tagged = TextBlob(

    def s_to_p(self, s):
        s = s.upper()
        s_list = s.split()[:-1]
        last_w = s.split()[-1]
        last_w = last_w.replace(last_w[-1], "")
        s_list.append(last_w)
        pron_list = []
        for w in s_list:
            pron_list.append(crawler(w))
        return " ".join(pron_list)

    def pronoun_markup(self, s):
        for w in s:
            if w in ['I', 'you', 'he', 'she', 'it', 'we', 'they']:
                self.markedup.append('<pronoun>' + w + '</pronoun')
            else:
                self.markedup.append(w)
        return self.markedup

    
        

def crawler(w):
    cmu = open("cmudict.0.7a.txt", 'r')
    cmu_coop = open("cmu_extracted.txt", 'r+')
    index = 0
    for i in range(115):
        index += 1
        cmu.next()

    for line in cmu:
        if line.split()[0] == w:
            pronunciation = line.split()[1:]
            break
    cmu_coop.close()
    cmu.close()
    pronunciation = ''.join(pronunciation)
    return pronunciation


def ui():
    s = raw_input("Enter the sentence you want to be converted to phonemes: ")
    s_list = s.split()
    output = s_to_p(s)
    output_list = output.split()
    print output
    print output_list
    print s_list

ui()
