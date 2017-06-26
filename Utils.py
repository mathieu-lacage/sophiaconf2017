def read_json(filename):
    import json
    with open(filename) as i:
        for line in i:
            try:
                d = json.loads(line)
                yield d
            except:
                continue

def write_json(filename, rows):
    import json
    with open(filename, 'w') as o:
        for row in rows:
            o.write('%s\n' % json.dumps(row))
        o.flush()


def select_kbest(k):
    from sklearn.feature_selection import SelectKBest
    from sklearn.feature_selection import chi2
    select = SelectKBest(chi2, k=k)
    return select

def naive_bayes():
    from sklearn.naive_bayes import MultinomialNB
    classifier = MultinomialNB()
    return classifier

def kbest_naive_bayes(k):
    from sklearn.pipeline import Pipeline
    kbest = select_kbest(k)
    nb = naive_bayes()
    pipeline = Pipeline([('kbest', kbest), ('nb', nb)])
    return pipeline

class Predictor:
    def __init__(self, model, features, classes):
        from sklearn.externals import joblib
        self._features_by_name = dict(read_json(features))
        self._classes_by_id = dict((id, name) for name, id in read_json(classes))
        self._model = joblib.load(model)
        
    def predict(self, content):
        import Ngrams
        import numpy
        vector = [0] * len(self._features_by_name)
        ngrams = Ngrams.generate(content)
        for ngram, count in ngrams:
            if ngram in self._features_by_name:
                vector[self._features_by_name[ngram]] = count
        x = numpy.array([vector])
        pred = self._model.predict(x)
        return self._classes_by_id[pred[0]]
