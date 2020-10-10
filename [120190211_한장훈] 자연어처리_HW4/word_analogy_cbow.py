from train_cbow import CBOW
from train_cbow import word_to_ix
from train_cbow import WINDOW_SIZE,EMBEDDING_DIM
import torch
import torch.nn.functional as F

model = CBOW(len(word_to_ix), EMBEDDING_DIM, WINDOW_SIZE)
model.load_state_dict(torch.load( 'cbow.epoch9.model'))
wordvec=[0,0,0,0]
tmp=0
correct=0
cnt=0
weight_vector=model.embeddings.weight.data
#print(weight_vector.size())
zero_tensor=torch.zeros([1,EMBEDDING_DIM])
#print(word_to_ix)
key_list = []
for w in word_to_ix.keys():
    key_list.append(w)

with open("data/questions_words.txt") as f:
    for line in f.readlines():
        line = line.lower()
        if ":" in line:
            continue
        cnt += 1
        word = line.strip().split(" ")
        for i in range(3):
            if word[i] not in word_to_ix:
                wordvec[i] = zero_tensor
            else:
                wordvec[i] = model.get_word_emdedding(word[i])
        result_vector = wordvec[0] - wordvec[1] + wordvec[2]
        # print(type(result_vector))
        # print(result_vector.size())
        tmp = F.cosine_similarity(weight_vector, result_vector, dim=1)
        # print(tmp.size())
        # print(tmp.argmax())
        # print(list[tmp.argmax()],word[3])
        for index in tmp.argsort(descending=True):
            if (key_list[index] == word[0] or key_list[index] == word[2]):
                continue
            else:
                argmax = index
                break
        #print(list[argmax],word[3])
        if (key_list[argmax] == word[3]):
            #print(list[argmax], word[3])
            correct += 1
        # print(result_vector)
        # print(wordvec[0])
        # print(wordvec[1])
        # print(wordvec[2])

print("accuracy =%.5f" % (correct / cnt))

