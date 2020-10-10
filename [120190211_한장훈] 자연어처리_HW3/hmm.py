import math   #로그 사용하기 위해서 import 합니다.
class Cell():
    def __init__(self):         #HMM,viterbi 알고리즘 구현하기위한 2차원 배열
        self.word_prob=0        #확률값 A_j
        self.word_morph=""      #거기서의 어절 사랑/NNG+해/NNG+!/SF 이런꼴
        self.before=0           #그전 어떤 상태에서 Max값이 왔는지를 링크해 놓음

class Word_List():
    def __init__(self):
        self.morph_combi_list=[]    #result.txt 파일을 읽어서 각 어절에 맞게 리스트를 나누어서 넣어놓음.
        self.word=""                #어절

class HMM():
    def __init__(self):
        self.pos_unigram = {}    #pos unigram 사전
        self.pos_bigram = {}     #pos bigram 사전
        self.morph_obs = {}    #observation 인데 morph 하나의 obs 값임,
        self.lexicon = []      #smoothing을 위한 단어 종류 개수 파악하기위해 리스트 만듬.

        self.morph_obs_prob = {} #라플라스 스무딩 후 형태소의 obs확률
        self.morph_transition_prob = {} #스무딩 된 형태소 사이의 전이확률임
def laplace_smoothing(hmm):  #laplace smoothing을 하는 함수.
    hmm.lexcon=list(set(hmm.lexicon))
    for word in hmm.morph_obs.keys():
        hmm.morph_obs_prob[word] = math.log((hmm.morph_obs[word]) + 1) - math.log(hmm.pos_unigram[word.split('|')[1]] + len(hmm.lexcon)) #정확한 계산을 위해 log를 사용
    for word in hmm.pos_bigram.keys():
        hmm.morph_transition_prob[word] = math.log((hmm.pos_bigram[word]) + 1) - math.log(hmm.pos_unigram[word.split('|')[1]] + len(hmm.pos_unigram))

def pos_count(pos_list,hmm):            #품사를 새서 unigram과 bigram 확률을 저장한다.(사전으로 저장)
    for sentence_pos in pos_list:
        for i in range(len(sentence_pos)):
            if i !=0:
                bigram = sentence_pos[i] + '|' + sentence_pos[i-1]
                if bigram not in hmm.pos_bigram:
                    hmm.pos_bigram[bigram] = 0
                hmm.pos_bigram[bigram] += 1
            if sentence_pos[i] not in hmm.pos_unigram:
                hmm.pos_unigram[sentence_pos[i]]=0
            hmm.pos_unigram[sentence_pos[i]] += 1
   #print(hmm.pos_bigram)

def train(hmm):                                 # train.txt 읽어와서 각각 단어들 저장한다.
    f = open("train.txt", 'r', encoding='CP949')
    pos_sentence_list=[]
    for sentence in f.read().split("\n\n"):
        if sentence.strip() == "":
            continue
        pos_sentence=["S"]
        for word in sentence.split("\n"):
            word=word.replace("//","tag!slash").replace("++","plusindent!").replace("+/","plustag!").replace("+","indent!").replace("/","tag!").replace("slash","/").replace("plus","+")        #+와 /로 구별되어 있는데 +/텍스에 포함되는 경우가 있어서 이를 편집해주었다.
            word=word.split("\t")
            #print(word)
            for morph in word[1].split("indent!"):

                tmp=morph.replace("tag!","|")
                if tmp not in hmm.morph_obs:
                    hmm.morph_obs[tmp] = 0
                hmm.morph_obs[tmp] += 1

                morph = morph.split("tag!")
                hmm.lexicon.append(morph[0])
                pos_sentence.append(morph[1])
        pos_sentence.append("/S")
        pos_sentence_list.append(pos_sentence)
   # print(hmm.morph_obs)
    pos_count(pos_sentence_list,hmm)
    laplace_smoothing(hmm)

    f.close()
def make_viterbi(hmm):                      #hmm 테이블을 만들어서 각각의 어절별 obs와 마지막, 앞의 형태소들의 transition prob를 계산하여 viterbi 알고리즘을 수행한다.
    word_comb_list=make_wordlist(hmm)
    last_cell_list=[]
    f = open("output.txt", "w")
    for sentence_list in word_comb_list:        #이건 문장들 여러개를 문장별로 뽑고.
        cell_list = []
        for i,Word_List in enumerate(sentence_list): #이게 문장 기준이다. 여기서 부터 표 만들면됨.너를 사랑해!
            tmp_list=[]
            cell_list.append(tmp_list)
            for j,morph_combi in enumerate(Word_List.morph_combi_list):     #너를 이랑 사랑해! i 가 너를 이면 j는 너를로 만들수있는 여러개의 어절 조합들이다.
                #print(morph_combi)
                maximum = -10000
                idx = -1
                new_cell = Cell()
                if i==0:                    #처음에는 S와 계산해줌.
                    new_cell.word_morph=morph_combi
                    new_cell.word_prob=find_transition('S',morph_combi,hmm)+find_obs(morph_combi,hmm)
                    cell_list[i].append(new_cell)
                else :          #두번째 이상부턴 앞 어절의 마지막 형태소 품사와 현재어절은 첫 형태소 품사끼리의 transition을 계산 해야한다. 앞에 열에있는 모든 값중에 max값을 찾음.
                    #print("진입")
                    prob=0
                    #print(cell_list[i-1])
                    for k,cell in enumerate(cell_list[i-1]):
                        #print("여기도 진입")
                        prob=cell.word_prob+find_transition(cell.word_morph,morph_combi,hmm)+find_obs(morph_combi,hmm)
                        if prob>maximum:
                            maximum=prob
                            idx=k
                    new_cell.word_morph=morph_combi
                    new_cell.word_prob=maximum
                    new_cell.before=cell_list[i-1][idx]
                    cell_list[i].append(new_cell)
            if i == len(sentence_list) - 1:             #다 끝나고 마지막으로 /S와 transtion prob 계산해야한다. 그중 maxr값을 저장해 놓는다.
                for j, morph_combi in enumerate(Word_List.morph_combi_list):
                    for k, cell in enumerate(cell_list[i]):
                        prob = cell.word_prob + find_transition(morph_combi, '/S', hmm)
                        if prob > maximum:
                            maximum = prob
                            idx = k
                    last_cell=Cell()
                    last_cell.word_morph ='/S'
                    last_cell.word_prob = maximum
                    #print(cell_list[i][idx])
                    last_cell.before = cell_list[i][idx]
        #print(last_cell.word_morph)
        #print(sentence_list)
        #print("prob",last_cell.word_prob)
        last_cell_list.append(last_cell)

    return last_cell_list
def make_ouput_file(last_cell_list):        #output 파일을 만든다. 재귀적으로 호출하면서 마지막 저장되있던 cell에서 그전 max값을 타고 들어간다.
    f = open("output.txt", "w")
    for last_cell in last_cell_list:
        print_pos_result(last_cell.before, f)
        f.write("\n")
    f.close()
def print_pos_result(cell,f):               #print하는 재귀함수,
    if(cell.before!=0):
        print_pos_result(cell.before,f)
    #print(cell.word_morph)
    f.write(cell.word_morph)
    f.write(" ")

def find_obs(word,hmm):         #한국어는 영어와는 다르게 어절의 obs를 계산하려면 어절의 형태소들의 obs와 transition을 다 계산해 주어야한다. 그걸 해주는 함수.
    obs=0
    word=word.split('+')
    #print("fdfdfd",word)
    for i,morph in enumerate(word):
        morph=morph.replace("/","|")
        if i > 0:

            if word[i].split("/")[1]+'|'+word[i-1].split("/")[1] in hmm.morph_transition_prob:
                obs+=hmm.morph_transition_prob[word[i].split("/")[1]+'|'+word[i-1].split("/")[1]]
            else:
                obs+=-math.log(hmm.pos_unigram[word[i-1].split("/")[1]] + len(hmm.pos_unigram))
        if morph in hmm.morph_obs_prob:
            #print(morph,hmm.morph_obs_prob[morph])
            obs+=hmm.morph_obs_prob[morph]
        else:
            obs+=-math.log((hmm.pos_unigram[morph.split("|")[1]] + len(hmm.lexicon)))

    return obs

def find_transition(word1,word2,hmm): #transition 확률 계산시 어절의 마지막 형태소와 그다음 어절의 첫번째 형태소의 transition을 구해주는 함수.
    if word1 !='S':
        morph1 = word1.split('+')[0].split('/')[1]
    else:
        morph1=word1
    if word2 !="/S":
        morph2 = word2.split('+')[-1].split('/')[1]
    else:
        morph2 = word2
    if morph2+"|"+morph1 in hmm.morph_transition_prob:
        return hmm.morph_transition_prob[morph2+"|"+morph1]
    else:
        return -math.log(hmm.pos_unigram[morph1]+len(hmm.pos_unigram))


def make_wordlist(hmm):                 #result txt 편집함수이다. 각 어절의 리스트로 만들어 저장한다.
    f=open("result.txt","r")
    word_comb_list=[]

    for sentence_text in f.read().split('\n\n\n'):
        wd = Word_List()
        sentence_list=[]
        #print(sentence_text)
        if sentence_text is None:
            continue
        for word_text in sentence_text.split('\n'):
            #print("tttt",word_text)
            if word_text =="":
                continue
            if not (word_text[0] ==' ' or word_text[0].isdigit()):
                if(wd.morph_combi_list): #처음이 아닐때
                    #print(wd.morph_combi)
                    sentence_list.append(wd)       #넣고
                    wd = Word_List()                #새로 다시만듬
                wd.word = word_text                   #처음들어가는건 똑같음

            else :
                wd.morph_combi_list.append(word_text[4:])
        if(wd.morph_combi_list):
            sentence_list.append(wd)
            #print(wd.morph_combi)
        if (sentence_list):
            word_comb_list.append(sentence_list)
    #for sentence in word_comb_list:
        #for wd in sentence:
            #print(wd.morph_combi_list)
    return word_comb_list


if __name__ == '__main__':
    hmm=HMM()
    train(hmm)
    last_cell_list=make_viterbi(hmm)
    make_ouput_file(last_cell_list)
