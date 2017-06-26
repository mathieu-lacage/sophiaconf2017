#
# The classic textcat method: it uses a rank distance to compare ngram
# profiles. It performs well on fairly long text.
# Reference: "N-Gram-Based Text Categorization", Cavnar, W. B. and J. M. Trenkle,  1994
#


class Predictor:
    def __init__(self, nngrams = 300):
        import codecs, json
        def filename(lang):
            import os.path
            return os.path.join(os.path.dirname(__file__), '%s_profile' % lang)
        self._profiles = {}
        self._nngrams = nngrams
        for lang in ['fr', 'en']:
            f = codecs.open(filename(lang), 'r')
            self._profiles[lang] = json.loads(f.read())
            f.close()
    def _out_of_place_distance(self, check_profile, target_profile):
        # This is the original out-of-place distance from the textcat paper
        # if no match, we consider the max penalty
        max_penalty = max(len(check_profile), len(target_profile))
        t_pos = 0
        distance = 0
        for te in target_profile:
            c_pos = 0
            for ce in check_profile:
                if te[0] == ce[0]:
                    break
                c_pos += 1 
            if c_pos < len(check_profile):
                # found
                distance += abs(c_pos - t_pos)
            else:
                # not found
                distance += max_penalty
            t_pos += 1
        return distance

    def predict(self, content):
        import Ngrams
        content_ngram_profile = Ngrams.generate(content)
        content_ngram_profile = content_ngram_profile[:self._nngrams]
        languages_distance = {}
        for lang_code, ngram_profile in self._profiles.items():
            ngram_profile = ngram_profile['ngrams']
            distance = self._out_of_place_distance(check_profile=content_ngram_profile, 
                                                   target_profile=ngram_profile
                                                   )
            languages_distance[lang_code] = distance
        import operator
        sorted_languages_distance = sorted(languages_distance.iteritems(), key=operator.itemgetter(1))
        return sorted_languages_distance[0][0]

def _read_json(filename):
    import json
    with open(filename) as f:
        for line in f:
            d = json.loads(line)
            content = d[2]
            tweet_lang = d[7]
            yield content, tweet_lang


def _extract_profiles(args):
    import optparse, os.path, collections, json, Ngrams
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', default='sample.json')
    parser.add_option('-n', '--nngrams', type='int', default=300, help='Max number of ngrams per language profile. Default: %default.')
    options, args = parser.parse_args(args)
    
    counts_by_lang = collections.defaultdict(lambda: collections.defaultdict(int))
    for content, lang in _read_json(options.input):
        counts = counts_by_lang[lang]
        ngrams = Ngrams.generate(content)
        for ngram, count in ngrams:
            counts[ngram] += count
    
    for lang, counts in counts_by_lang.items():
        sorted_counts = sorted(counts.iteritems(), key=lambda i: i[1], reverse=True)
        f = open(os.path.join(os.path.dirname(__file__), '%s_profile' % lang), 'w+')
        f.write(json.dumps({'ngrams' : sorted_counts[:options.nngrams]}))
        f.close()

def _predict(args):
    import optparse, sys
    parser = optparse.OptionParser()
    parser.add_option('-n', '--nngrams', type='int')
    options, args = parser.parse_args(args)

    content = unicode(sys.stdin.read(), encoding='utf-8')
    predictor = Predictor(nngrams = options.nngrams)
    print predictor.predict(content)
  
  
def main():
    import sys, optparse
    parser = optparse.OptionParser(usage = "usage: %prog extract-profiles|predict")
    parser.disable_interspersed_args()
    options, args = parser.parse_args()
    commands = {
        'extract-profiles' : _extract_profiles,
        'predict' : _predict
    }
    if len(args) == 0:
        parser.print_help()
        return
    commands[args[0]](args[1:])    
    
if __name__ == '__main__':
    main()
      
    
