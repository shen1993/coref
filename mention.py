from nltk.corpus import namesfrom nltk.corpus import stopwordsmale = [name for name in names.words("male.txt")]female = [name for name in names.words("female.txt")]class Mention(object):    def __init__(self, tokens, sentenceID, span, label):        self.tokens = tokens        self.sentenceID = sentenceID        self.span = span        self.label = label        self.feat = None    def features(self):        f = {}        f['text'] = ' '.join([t.annotations['Word itself'] for t in self.tokens])        f['NE'] = self.tokens[0].annotations['Named Entities'].strip('(*)')        f['sentenceID'] = self.sentenceID        # f['definite'] = 1 if f['text'].split(' ')[0] == 'the' else 0        # f['demonstrative'] = 1 if f['text'].split(' ')[0] in {'this', 'that', 'these', 'those'} else 0        f['pronoun'] = self.is_pronoun()        f['male'] = self.is_male(f['pronoun'], f['text'])        f['female'] = self.is_female(f['pronoun'], f['text'])        f['modifier'] = 1 if f['text'].split(' ')[0].islower() and f['text'].split(' ')[0] not in stopwords.words(            'english') and len(f['text'].split(' ')) > 1 else 0        f['singular'] = 1 if f['text'].split(' ')[0] in {'one', 'a', 'an', 'this'} else 0        f['plural'] = 1 if f['text'].split(' ')[0] in {'two', 'three', 'four', 'five', 'these', 'some'} else 0        self.feat = f    def get_features(self):        if not self.feat:            self.features()        return self.feat    def is_pronoun(self):        if len(self.tokens) == 1:            if self.tokens[0].annotations['POS'].startswith('PRP'):                return 1        return 0    def is_male(self, is_pronoun, text):        if is_pronoun:            word = self.tokens[0].annotations['Word itself'].lower()            if word in {'he', 'him', 'his'}:                return 1            else:                return 0        else:            for t in text.split():                if t in male:                    return 1                else:                    return 0        return 0    def is_female(self, is_pronoun, text):        if is_pronoun:            word = self.tokens[0].annotations['Word itself'].lower()            if word in {'she', 'her', 'hers'}:                return 1            else:                return 0        else:            for t in text.split():                if t in female:                    return 1                else:                    return 0        return 0    def write_results(self, clusterID):        self.tokens[0].predicted_coref['start'].add(clusterID)        self.tokens[-1].predicted_coref['end'].add(clusterID)