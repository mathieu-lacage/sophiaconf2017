# -*- coding: utf-8
URL = 1
SMILEY = 2
DATE = 3
VERSION = 4
MENTION = 5
HASHTAG = 6
WORD = 7
MONEY = 8 

def _ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])
def _remove_numbers(question):
    import re
    question  = re.sub('[^\w]\d+[^\w]', ' ', question)
    question  = re.sub('[^\w]\d+$', ' ', question)
    question  = re.sub('^\d+[^\w]', ' ', question)
    question  = re.sub('^\d+$', ' ', question)
    return question
def _remove_uids(question):
    import re
    question  = re.sub('[^\w][a-zA-Z0-9]*([0-9]+[a-zA-Z]+)|([a-zA-Z]+[0-9]+)[a-zA-Z0-9]*[^\w]', ' ', question)
    question  = re.sub('[^\w][a-zA-Z0-9]*([0-9]+[a-zA-Z]+)|([a-zA-Z]+[0-9]+)[a-zA-Z0-9]*$', ' ', question)
    question  = re.sub('^[a-zA-Z0-9]*([0-9]+[a-zA-Z]+)|([a-zA-Z]+[0-9]+)[a-zA-Z0-9]*[^\w]', ' ', question)
    question  = re.sub('^[a-zA-Z0-9]*([0-9]+[a-zA-Z]+)|([a-zA-Z]+[0-9]+)[a-zA-Z0-9]*$', ' ', question)
    return question
def _remove_duplicate_chars(question):
    import re
    question = question.replace('...', '. ')
    return re.sub(r'([a-zA-Z\.\?!;\'\",\:\>\<])\1{2,}', r'\1', question)

def _remove_phone_numbers(question):
    import re
    cleansed_question = re.sub(r'(\d{2}\W*\d{2}\W*\d{2}\W*\d{2}\W*\d{2})', ' ', question, flags=re.MULTILINE)
    return cleansed_question.strip()
def _remove_emails(question):
    import re
    cleansed_question = re.sub(r'([A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]+)', '', question, flags=re.MULTILINE)
    return cleansed_question.strip()
def _remove_twitter_at(question):
    ats = [at for at in question.split() if at.startswith('@')]
    cleansed_question = question
    for at in ats:
        cleansed_question = cleansed_question.replace(at, '')
    return cleansed_question.strip()

def _remove_twitter_rw(question):
    import re
    twitter_rw = ['rt', 'dm']
    cleansed_question = ' ' + question + ' '
    for rw in twitter_rw:
        cleansed_question = re.sub(r'\W(?:%s)\W' % rw, ' ', cleansed_question, flags=re.IGNORECASE)
    return cleansed_question.strip()

def _remove_urls(question):
    import re
    cleansed_question = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', question, flags=re.MULTILINE)
    return cleansed_question.strip()

def _remove_smilies(question):
    import re
    smileys = [': /+','>:[+', ':-(+', ':(+', ':-c', ':-<+', ':-[+', ':{', '>.>', ':o',
               '<.<', '>.<', ':\\+', ':\\\'(+', ':\\\'(+', ':\'(+', ';\'(+', '>:\\', '>:/+',
               ':-/+', ':-.', ':\\+', '=/+', '=\\+', ':S', ':/+', ':$', '\*cry\*', '-_-',
               ';-)+', ':D', ';D', ';;)+', ':-x', ':x', '^-^', 'x)', 'è_é','haha','hehe', 'u_u',
               '0:-)', ':o)', ':*', ':-*', '8-}', '=P~', '>:D<', '<:-P', ';))', 
               'xD', '>.<','u_u',
               '>:]+', ':3', ':c', ':>', '=]', '8)+', '=)+', ':}+', ':^)+', '>:D', ':-D', '8-D', 'x-D', 'X-D', '=-D', '=D', '=-3', '8-)+',
               '>;]+', '*-)+', '*)+', ';-]+', ';]+', ';^)+', '>:P', ':-P', ':P', 'X-P', ':-p', '=p', ':-Þ', ':Þ', ':-b', '>:o', '>:O', ':-O',
               '°o°', '°O°', 'o_O', 'o.O', '8-0', 'o_O', 'x)+', '^^+', ':=)', '((?::|;|=)(?:-)?(?:\)|D|P))']
    regex = '|'.join(['(\s%s\s)' % i for i in [re.escape(smiley) for smiley in smileys]])

    cleansed_question = re.sub(regex, ' ', question, flags=re.MULTILINE|re.I)
    return cleansed_question.strip()

def _remove_hashtags(question):
    import re
    question = question.strip()
    hash_tags = [tag for tag in question.split() if tag.startswith('#')]
    if not hash_tags:
        return question
    # check the position of the hash tags within the question and decide whether to clean and keep it 
    # or to remove it
    import sys
    last_question_mark_pos = sys.maxint if question.rfind('?') == -1 else question.rfind('?')
    # remove all hash tags being after the last question mark
    for tag in hash_tags:
        tag_pos = question.find(tag)
        if tag_pos > last_question_mark_pos:
            # completely remove hashtag if they are after the last qm or just at the beginning of the tweet
            question = question.replace(tag, ' ')
            question = question.strip()
            last_question_mark_pos = question.rfind('?')
        else:
            # just remove the hashtag sign 
            question = question.replace(tag, tag[1:])
            last_question_mark_pos = sys.maxint if question.rfind('?') == -1 else question.rfind('?')
    # remove extra spaces and return
    pattern = re.compile(r'\s+')
    question = re.sub(pattern, ' ', question.strip())
    return question

def find_urls(content, scheme):
    current = content.find(scheme)
    while current != -1:
        end = content.find(' ', current)
        if end == -1:
            end = content.find('\n', current)
            if end == -1:
                end = len(content)
        while content[end-1] in [',', '.', ';', ':', '?']:
            end -= 1
        yield (current, end)
        current = end
        current = content.find(scheme, current)

class SmileyParser:
    def __init__(self):
        import re
        western_smileys = [
            # from http://en.wikipedia.org/wiki/List_of_emoticons
            ':-)', ':)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}', ':^)',
            ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D', '=-3', '=3', 'B^D',
            ':-))',
            '>:[', ':-(', ':(',  ':-c', ':c', ':-<',  ':<', ':-[', ':[', ':{',
            ':-||', ':@', '>:(',
            ":'-(", ":'(",
            ":'-)", ":')",
            'D:<', 'D:', 'D8', 'D;', 'D=', 'DX', 'v.v', "D-':",
            '>:O', ':-O', ':O', '8-0',
            ':*', ':^*',
            ';-)', ';)', '*-)', '*)', ';-]', ';]', ';D', ';^)', ':-,',
            '>:P', ':-P', ':P', 'X-P', 'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b',
            '>:\\', '>:/', ':-/', ':-.', ':/', ':\\', '=/', '=\\', ':L', '=L', ':S', '>.<',
            ':|', ':-|',
            ':$',
            ':-X', ':X', ':-#', ':#',
            'O:-)', '0:-3', '0:3', '0:-)', '0:)', '0;^)',
            '>:)', '>;)', '>:-)',
            '}:-)', '}:)', '3:-)', '3:)',
            'o/\o', '^5', '>_>^', '^<_<',
            '|;-)', '|-O',
            ':-&', ':&',
            '#-)',
            '%-)', '%)',
            ':-###..', ':###..',
            '\\o/', '/o\\'
            '*\\0/*',
            # additional
            ':=)', ';=)', ';))', ':))', ';;)'
            ]

        eastern_smileys = [
            # from http://en.wikipedia.org/wiki/List_of_emoticons
            ]
        unicode_smileys = [
            # from http://en.wikipedia.org/wiki/List_of_emoticons
            u'\u2639', u'\u263a', u'\u263b',
            u'\u1f600', u'\u1f601', u'\u1f602', u'\u1f603', u'\u1f604', u'\u1f605', u'\u1f606', u'\u1f607', 
            u'\u1f608', u'\u1f609', u'\u1f60a', u'\u1f60b', u'\u1f60c', u'\u1f60d', u'\u1f60e', u'\u1f60f',
            
            u'\u1f610', u'\u1f611', u'\u1f612', u'\u1f603', u'\u1f614', u'\u1f615', u'\u1f616', u'\u1f617', 
            u'\u1f618', u'\u1f619', u'\u1f61a', u'\u1f60b', u'\u1f61c', u'\u1f61d', u'\u1f61e', u'\u1f61f',

            u'\u1f620', u'\u1f621', u'\u1f622', u'\u1f603', u'\u1f624', u'\u1f625', u'\u1f626', u'\u1f627', 
            u'\u1f628', u'\u1f629', u'\u1f62a', u'\u1f60b', u'\u1f62c', u'\u1f62d', u'\u1f62e', u'\u1f62f',

            u'\u1f630', u'\u1f631', u'\u1f632', u'\u1f633', u'\u1f634', u'\u1f635', u'\u1f636', u'\u1f637',
            u'\u1f638', u'\u1f639', u'\u1f63a', u'\u1f63b', u'\u1f63c', u'\u1f63d', u'\u1f63e', u'\u1f63f',

            u'\u1f640',                                                 u'\u1f645', u'\u1f646', u'\u1f647', 
            u'\u1f648', u'\u1f649', u'\u1f64a', u'\u1f64b', u'\u1f64c', u'\u1f64d', u'\u1f64e', u'\u1f64f',
            ]
        # try to generate rotated smileys
        invert = {
            # ltr to rtl
            ')' : '(',
            '(' : ')',
            ']' : '[',
            '[' : ']',
            '{' : '}',
            '}' : '{',
            '<' : '>',
            '>' : '<',
            '/' : '\\',
            '\\' : '/',
            # does not change
            'o' : 'o',
            'x' : 'x',
            'v' : 'v',
            '0' : '0',
            '8' : '8',
            '|' : '|',
            ':' : ':',
            ';' : ';',
            ',' : ',',
            "'" : "'",
            '*' : '*',
            '%' : '%'
            }
        def reverse_smiley(smiley):
            output = []
            for c in reversed(smiley):
                if c in invert:
                    output.append(invert[c])
                else:
                    return None
            return ''.join(output)
    
        smileys = western_smileys + \
            filter(lambda x:not x is None, [reverse_smiley(smiley) for smiley in western_smileys]) + \
            eastern_smileys + \
            unicode_smileys
    
        self._regex = re.compile('|'.join(['(?:%s)' % i for i in [re.escape(smiley) for smiley in smileys]]), re.I | re.U)

    def parse(self, content):
        for i in self._regex.finditer(content):
            start, end = i.span()
            yield (start, end)


def _tokenize(content):
    import re
    tokens = []
    # urls
    for scheme in ['http', 'https', 'ftp']:
        for start,end in find_urls(content, '%s://' % scheme):
            tokens.append((start, end, URL))

    def untokenized(tokens):
        current = 0
        for start, end, type in sorted(tokens):
            yield (current, start)
            current = end
        yield (current, -1)
    # smileys
    smileys = SmileyParser()
    for start, end in untokenized(tokens):
        for s,e in smileys.parse(content[start:end]):
            tokens.append((start+s, start+e, SMILEY))
    
    # dates
    for start, end in untokenized(tokens):
        for m in re.finditer(r'\b([0-9]{1,2}/[0-9]{1,2}(/[0-9]{2,4})?)\b', content[start:end]):
            s, e = m.span()
            tokens.append((start + s, start + e, DATE))
    # Money
    for start, end in untokenized(tokens):
        #if content[start:end].find(u'€') != -1:
        #    print 'MONEY: ', content[start:end]
        for m in re.finditer(ur'([0-9.,]+[£\$€])', content[start:end], re.U):
            s, e = m.span()
            tokens.append((start + s, start + e, MONEY))

    # versions
    for start, end in untokenized(tokens):
        for m in re.finditer(r'\b((?:[0-9.])+\w?)\b', content[start:end], re.U):
            s, e = m.span()
            tokens.append((start + s, start + e, VERSION))

    # mentions
    for start, end in untokenized(tokens):
        for m in re.finditer(r'(@[a-zA-Z0-9_]{1,15})\b', content[start:end]):
            s, e = m.span()
            tokens.append((start + s, start + e, MENTION))

    # hashtags
    for start, end in untokenized(tokens):
        for m in re.finditer(r'(#[a-zA-Z0-9_]+)\b', content[start:end]):
            s, e = m.span()
            tokens.append((start + s, start + e, HASHTAG))

    # whitespace-separated words
    for start, end in untokenized(tokens):
        for m in re.finditer(r'\b\w+\b', content[start:end], re.U):
            s, e = m.span()
            tokens.append((start + s, start + e, WORD))

    return sorted(tokens)


def _clean(content):
    content = content.lower()
    content = _remove_smilies(content)
    content = _remove_hashtags(content)
    content = _remove_urls(content)
    content = _remove_twitter_rw(content)
    content = _remove_twitter_at(content)
    content = _remove_emails(content)
    content = _remove_phone_numbers(content)
    content = _remove_duplicate_chars(content)
    content = _remove_numbers(content)
    content = _remove_uids(content)
    tokens = _tokenize(content)
    content = ' '.join([content[start:end] for start, end, type in tokens])
    return content

def generate(content):
    import collections
    freq_dist = collections.defaultdict(int)
    content = _clean(content)
    if content == '':
        return []
    content_chars = [' ']
    content_chars += list(content)
    content_chars.append(' ')
    ngrams = [x for x in _ngrams(content_chars, 1) if ''.join(list(x)) != ' ']
    ngrams += _ngrams(content_chars, 2)
    ngrams += _ngrams(content_chars, 3)
    ngrams += _ngrams(content_chars, 4)
    ngrams += _ngrams(content_chars, 5)
    for ngram in ngrams:
        freq_dist[''.join(list(ngram))] += 1
    import operator
    return sorted(freq_dist.iteritems(), key=operator.itemgetter(1), reverse=True)
