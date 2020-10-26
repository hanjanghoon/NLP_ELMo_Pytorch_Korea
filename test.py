from elmoformanylangs import Embedder

e = Embedder('korean')

sents = [['배고픈', '하루', '였다'],
['과연','엘모가','잘','될까?']]
# the list of lists which store the sentences
# after segment if necessary.

afterelmo=e.sents2elmo(sents)
print(afterelmo)
# will return a list of numpy arrays
# each with the shape=(seq_len, embedding_size)