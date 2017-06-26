
def main():
    import optparse
    import numpy
    from scipy import io
    from sklearn.externals import joblib
    import Utils

    parser = optparse.OptionParser()
    parser.add_option('-x', default='X.mtx')
    parser.add_option('-y', default='y.npy')
    parser.add_option('-k', default=1000, type='int')
    parser.add_option('-m', '--model', default='model.pkl')
    options, args = parser.parse_args()


    X = io.mmread(options.x)
    y = numpy.load(options.y)

    classifier = Utils.kbest_naive_bayes(options.k)
    classifier.fit(X, y)

    joblib.dump(classifier, options.model)


if __name__ == '__main__':
    main()
