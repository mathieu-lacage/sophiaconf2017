def main():
    import optparse, Ngrams, Utils
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', default='preprocessed.json')
    parser.add_option('-c', '--classes', default='classes.json')
    parser.add_option('-f', '--features', default='features.json')
    parser.add_option('-x', default='X.mtx')
    parser.add_option('-y', default='y')
    parser.add_option('--y-textcat', default='y-textcat')
    options, args = parser.parse_args()

    class Ids:
        def __init__(self):
            self._ids = dict()
        def get(self, name):
            id = self._ids.get(name, None)
            if id is None:
                id = len(self._ids)
                self._ids[name] = id
            return id
        def all(self):
            return self._ids.items()
    
    features = Ids()
    classes = Ids()

    y = []
    y_textcat = []
    indptr = [0]
    indices = []
    data = []

    for id, text, lang, text_cat_lang, ngrams in Utils.read_json(options.input):
        y.append(classes.get(lang))
        y_textcat.append(classes.get(text_cat_lang))
        for ngram, count in ngrams:
            indices.append(features.get(ngram))
            data.append(count)
        indptr.append(len(indices))

    Utils.write_json(options.classes, classes.all())
    Utils.write_json(options.features, features.all())
    
    from scipy import sparse, io
    import numpy
    x = sparse.csr_matrix((data, indices, indptr), dtype = int)
    io.mmwrite(options.x, x)
    numpy.save(options.y, y)
    numpy.save(options.y_textcat, y_textcat)

if __name__ == '__main__':
    main()
