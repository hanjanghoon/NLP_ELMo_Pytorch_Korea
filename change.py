def changelist(sentence):
    sen_morph=[]#여기에 원래형식대로 맞춰줌
    mem_morph = [0 for _ in range(10)]
    wordidx=0
    for word in sentence:
        mem_morph[wordidx] = 1
        wordidx+=len(word)
        mem_morph[wordidx] = 1
        for morph in word:
            sen_morph.append(morph)

    mem_morph.append = k
    e=sent2elmo(sen_morph)
    for idx in range(len(mem_moprh)):
        add=torch.cat(e[mem_morph[idx],e[mem_morph[idx+1]-1])
        new=torch.cat(new,add)
    return new