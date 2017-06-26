def main():
    import optparse
    import numpy
    from scipy import io
    import Utils
    
    parser = optparse.OptionParser()
    parser.add_option('-x', default='X.mtx')
    parser.add_option('-y', default='y.npy')
    parser.add_option('--min', type='int', default=50)
    parser.add_option('--max', type='int', default=15000)
    parser.add_option('--step', type='int', default=50)
    options, args = parser.parse_args()

    X = io.mmread(options.x)
    y = numpy.load(options.y)

    from sklearn.model_selection import cross_val_score

    for k in range(options.min, options.max, options.step):
        classifier = Utils.kbest_naive_bayes(k)
        scores = cross_val_score(classifier, X, y)
        print k, scores.mean()

if __name__ == '__main__':
    main()
