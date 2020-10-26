from collections import Counter
import hanja

def read_corpus(path, max_chars=None, max_sent_len=20):
  """
  read raw text file
  :param path: str
  :param max_chars: int
  :param max_sent_len: int
  :return:
  """
  data = []
  with open(path, 'r', encoding='utf-8') as fin:
    for line in fin:
      data.append('<bos>')
      for token in line.strip().split():
        if max_chars is not None and len(token) + 2 > max_chars:
          token = token[:max_chars - 2]
        data.append(token)
      data.append('<eos>')
      #print("이건 read corpus",data)
  dataset = break_sentence(data, max_sent_len)
  #print(dataset)
  return dataset

def read_conll_char_corpus(path, max_chars=None):
  """

  :param path:
  :param max_chars:
  :return:
  """
  dataset = []

  with open(path, 'r', encoding='utf-8') as fin:
    for payload in fin.read().strip().split('\n\n'):
      #print("하하하하핫"+payload)
      data = ['<bos>']

      lines = payload.splitlines()
      body = [line for line in lines if not line.startswith('#')]
      for line in body:
        #print("라인 이다",line)
        fields = line.split('\t')
        num, token = fields[0], fields[1]
        if '-' in num or '.' in num:
          continue
        if '|' in token:
            for i in range(len(token.split('|'))):
                data.append(token.split('|')[i])

      #print("이것은 conll ", data)
      dataset.append(data)
      data.append('<eos>')

  return dataset

def break_sentence(sentence, max_sent_len):
  """
  For example, for a sentence with 70 words, supposing the the `max_sent_len'
  is 30, break it into 3 sentences.

  :param sentence: list[str] the sentence
  :param max_sent_len:
  :return:
  """
  ret = []
  cur = 0
  length = len(sentence)
  while cur < length:
    if cur + max_sent_len + 5 >= length:
      ret.append(sentence[cur: length])
      break
    ret.append(sentence[cur: min(length, cur + max_sent_len)])
    cur += max_sent_len
  return ret
def get_truncated_vocab(dataset, min_count):
  """

  :param dataset:
  :param min_count: int
  :return:
  """
  word_count = Counter()
  for sentence in dataset:
    word_count.update(sentence)

  word_count = list(word_count.items())
  word_count.sort(key=lambda x: x[1], reverse=True)

  i = 0
  for word, count in word_count:
    if count < min_count:
      break
    i += 1

  #logging.info('Truncated word count: {0}.'.format(sum([count for word, count in word_count[i:]])))
  #logging.info('Original vocabulary size: {0}.'.format(len(word_count)))
  return word_count[:i]


numfile=13
train_data=[]
for i in range(1,numfile):
    train_data.extend(read_corpus("data/news_"+str(i)+".txt", 50, 20))
    print(i)
train_data.extend(read_conll_char_corpus("data/train.conllx", 50))
train_data.extend(read_conll_char_corpus("data/test.conllx", 50))
vocab = get_truncated_vocab(train_data,4)

word_lexicon={}
char_lexicon = {}#수정
for special_word in ['<oov>', '<bos>', '<eos>', '<pad>']:
    if special_word not in word_lexicon:
        word_lexicon[special_word] = len(word_lexicon)

for word, _ in vocab:
    hflag=0
    for ch in word:
        if hanja.is_hanja(ch):
            # print(ch)
            hflag=1
            break
        if ch not in char_lexicon:
            char_lexicon[ch] = len(char_lexicon)
    if hflag==1:
        continue
    if word not in word_lexicon:
        word_lexicon[word] = len(word_lexicon)


# Character Lexicon
'''
char_lexicon = {}
for sentence in train_data:
    for word in sentence:
        for ch in word:
            if hanja.is_hanja(ch):
                #print(ch)
                continue
            if ch not in char_lexicon:
                char_lexicon[ch] = len(char_lexicon)
'''
for special_char in ['<bos>', '<eos>', '<oov>', '<pad>', '<bow>', '<eow>']:
    if special_char not in char_lexicon:
        char_lexicon[special_char] = len(char_lexicon)


with open('char.dic', 'w', encoding='utf-8') as fpo:
    for ch, i in char_lexicon.items():
        print('{0}\t{1}'.format(ch, i), file=fpo)

with open('word.dic', 'w', encoding='utf-8') as fpo:
    for w, i in word_lexicon.items():
        print('{0}\t{1}'.format(w, i), file=fpo)
