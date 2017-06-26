def main():
    import optparse, sys, numpy
    from sklearn.externals import joblib
    import Utils, Ngrams
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', default=None)
    parser.add_option('-f', '--features', default='features.json')
    parser.add_option('-c', '--classes', default='classes.json')
    parser.add_option('-m', '--model', default='model.pkl')
    options, args = parser.parse_args()

    if options.input is None:
        input = unicode(sys.stdin.read(), encoding='utf-8')
    else:
        with open(options.input) as i:
            input = i.read()

    predictor = Utils.Predictor(options.model, options.features, options.classes)
    print predictor.predict(input)

if __name__ == '__main__':
    main()
