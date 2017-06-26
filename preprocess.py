

def main():
    import optparse, json, TextCat, Ngrams, Utils
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', default='sample.json')
    parser.add_option('-o', '--output', default='preprocessed.json')
    options, args = parser.parse_args()

    text_cat = TextCat.Predictor()

    o = ((d['id'], d['text'], d['lang'], text_cat.predict(d['text']), Ngrams.generate(d['text'])) for d in Utils.read_json(options.input))
    o = (d for d in o if len(d[4]) >= 3)
    Utils.write_json(options.output, o)

    
if __name__ == '__main__':
    main()
