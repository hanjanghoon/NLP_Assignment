import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data as data_utils
from torch.utils.data import Dataset, DataLoader
from collections import Counter
import time

torch.manual_seed(1)


class SkipGram(nn.Module):  # nn.module 상속받음

  def __init__(self, vocab_size, embedding_dim, window_size):  # 초기화
    super(SkipGram, self).__init__()  # 부모 생성
    self.embeddings = nn.Embedding(vocab_size, embedding_dim)  # 임베딩 테이블 초기화.
    self.linear1 = nn.Linear(embedding_dim, vocab_size)  # sizeof input, sizeof output 즉 임베딩 디멘션만큼
    pass

  def forward(self, inputs):  # 인덱스임.
    embeds = self.embeddings(inputs)  # 임베딩 테이블에 텐서
    out = self.linear1(embeds)  # 여기서 복사
    log_probs = F.log_softmax(out, dim=1)  # 마지막 소프트맥스

    return log_probs

  def get_word_emdedding(self, word):
    word = torch.LongTensor([word_to_ix[word]])  # 인덱스로 변환해서
    return self.embeddings(word).view(1, -1)  # 임베딩에 넣어서 리턴을 한다. reshape를 view로 한다.-1에서 1값을 가지도록.


EMBEDDING_DIM = 128
if torch.cuda.is_available():
  VOCAB_SIZE = 30000
else:
  VOCAB_SIZE = 5000

UNK_TOKEN = "<UNK>"
WINDOW_SIZE = 5
BATCH_SIZE = 1024

words = []
with open("data/text8.txt") as f:
  for line in f.readlines():
    words += line.strip().split(" ")

print("total words in corpus: %d" % (len(words)))

word_cnt = Counter()
for w in words:
  if w not in word_cnt:
    word_cnt[w] = 0
  word_cnt[w] += 1

# calculate word coverage of 30k most common words
total = 0
for cnt_tup in word_cnt.most_common(VOCAB_SIZE):
  total += cnt_tup[1]
print("coverage: %.4f " % (total * 1.0 / len(words)))
# 95.94%

# make vocabulary with most common words
word_to_ix = dict()
for i, cnt_tup in enumerate(word_cnt.most_common(VOCAB_SIZE)):#카운터 most_common 튜플 반환 그러니가 cnt_tup[0]은 단어임.
  word_to_ix[cnt_tup[0]] = i            #단어 인덱스

# add unk token to vocabulary
word_to_ix[UNK_TOKEN] = len(word_to_ix)
if __name__ == "__main__":
  # replace rare words in train data with UNK_TOKEN
  train_words = []
  for w in words:     #word에 있는데...
    if w not in word_to_ix: #word_to ix에 없으면 언노운 토큰임.
      train_words += [UNK_TOKEN] #extend랑 똑같고
    else:
      train_words += [w]  #아니면 그냥 리스트에 워드넣음

  # make train samples for CBOW
  train_input = []
  train_target = []
  span = (WINDOW_SIZE - 1) // 2   #이게 양옆이라는 거죠 윈도우 사이즈는 5고. // 이건 뭐지 나눗셈의 몫임 2
  for i in range(span, len(train_words) - span):#2에서 n-2까지 봐야쥬 5개니까//이걸 바꿔야함.
    for j in range(WINDOW_SIZE):#01234
      if j != span:             #2가 아니라면 context에 넣어주고
        train_target.append(word_to_ix[train_words[i + j - span]])# 주변단어. 이걸 target으로한다.
    for k in range(4):
      train_input.append(word_to_ix[train_words[i]])#이게 센터워드 이게 입력

  print("data is generated!")

  # model class

  # set up to train
  losses = []
  loss_function = nn.NLLLoss()  #negativl log likelihood 줄여야 된다
  model = SkipGram(len(word_to_ix), EMBEDDING_DIM, WINDOW_SIZE)         #모델 설정.
  optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)      #옵티마이저설정

  # if gpu is available, then use it
  if torch.cuda.is_available():   #cuda 설정
    model.cuda()

  # make data loader for batch training
  train_input = torch.from_numpy(np.asarray(train_input)).long()        #원래는 input에 인덱스 넣었는데 이걸 텐서로 바꾸는거임
  train_target = torch.from_numpy(np.asarray(train_target)).long()
  dataset_train = data_utils.TensorDataset(train_input, train_target)   #데이터 로더에 넣어줄라고 변환
  train_loader = data_utils.DataLoader(dataset_train, batch_size=BATCH_SIZE, shuffle=True, num_workers=4, pin_memory=False) #배치별로 끊어. 한번에 1024개

  # training loop
  for epoch in range(10): #epoch 10번한다.
    total_loss = 0
    start = time.time()       #컴퓨터 현재시간.
    for i, (context, target) in enumerate(train_loader):#여기서 context랑 타겟 빼낸다.

      if torch.cuda.is_available():
        context = context.cuda()
        target = target.cuda()

      model.zero_grad()       #grad 0으로 초기화.

      log_probs = model(context)        #이게 뭐지? call을 호출하면 거기서 forword나온다.
      #target=torch.reshape(torch.t(target),(-1,1))
      loss = loss_function(log_probs, target) #아까 negative log likelihood. target이 4개야....

      loss.backward()#grad계산함
      optimizer.step()      #빼줌

      total_loss += loss.item() #loss의 스칼라값.

      if (i+1) % 1000 == 0:
        print("loss: %.4f, steps: %dk" % (loss.item(), ((i+1)/1000))) #천번을 한단 이야긴데.. 17000000중에... 그럼 결국 배치사이즈만큼 로스가 더해지는거 아님?
                                                                      #아니다 사실 1000만큼씩 끊어서 17000번 하는거임.. 그래서 약 17번 나오는게된다.
    end = time.time()#시간 멈추고
    print("epochs: %d" % (epoch+1))
    print("time eplased: %d seconds" % (end-start))   #타임
    print("mean loss: %.4f" % (total_loss / (train_input.shape[0] // BATCH_SIZE))) #그래서 17번 나눠줌
    torch.save(model.state_dict(), "skip_gram.epoch{}.model".format(epoch))#모델 결과 저장

  # Here you need to save the model's hidden layer which is V * D word embedding matrix.
  # Then, use the word embedding matrix to get vectors for word
