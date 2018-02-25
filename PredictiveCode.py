class Predictor:
    def __init__(self, wordlist='common.txt'):
        self.wordlist = open(wordlist).read().split('\n')
    def predict(self, prefix):
        if prefix == "":
            return []
        output = []
        for word in self.wordlist:
            if prefix in word[:len(prefix)]:
                output.append(word)
        return output
    def add_word(self, word):
        self.wordlist.append(word.lower())

if __name__ == "__main__":
    #k = Predictor()
    #print k.predict("d")
    pass
