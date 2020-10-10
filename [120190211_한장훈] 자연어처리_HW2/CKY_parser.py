"""
class Cell1():
    def __init__(self):
        self.words=[]
        self.num = []
"""
class Cell():
    def __init__(self, word=None, left=None, right=None, num=None):
        self.word = word
        self.child=[]
        self.right =[]
        self.num =num
        self.child.append((left,right))
        self.right.append(right)

#index=0
def selfmake(grammar_list,Cell_list,fo1,cnt,arr):
    for minicell in Cell_list:
        for gram in grammar_list:
            if minicell.word in gram and len(gram)==2:
                if gram[0] not in minicell.word:
                    Cell_list.append(Cell(word=gram[0],left=minicell.num,right=None,num=cnt))
                    if fo1 is not None:
                        fo1.write(str(cnt) + ' (' + gram[0] + ' , ' + str(minicell.num) + ')' + '\n')
                    if arr is not None:
                        arr.append([gram[0], minicell.num])
                    cnt=cnt+1
    return Cell_list,cnt

def packed_cky_parse(sentence ,grammar_list,fo1):
    Cell_list=[]
    cnt=1;
    for word1 in sentence:
        row_list=[]
        for word2 in sentence:
            col_list=[]
            row_list.append(col_list)
        Cell_list.append(row_list)
    for j in range(len(sentence)):
        for i in reversed(range(0, j+1)):
            if i==j:
                for grammar in grammar_list:
                    if sentence[i] in grammar :
                        Cell_list[i][j].append(Cell(word=grammar[0], left=None, right=None, num=cnt))
                        fo1.write(str(cnt)+' ('+grammar[0]+' , '+grammar[1]+')'+'\n')
                        cnt=cnt+1
                Cell_list[i][j] , cnt = selfmake(grammar_list , Cell_list[i][j] ,fo1,cnt,None)

            else:
                for k in range(i,j):
                    for cell1 in Cell_list[i][k]:
                        for cell2 in Cell_list[k+1][j]:
                            for word in grammar_list:
                                if len(word) < 3:
                                    continue
                                if cell1.word == word[1] and cell2.word == word[2]:
                                    flag=0
                                    for cell3 in Cell_list[i][j]:
                                        if word[0] == cell3.word :#같으면 새로안넣어
                                            cell3.child.append((cell1.num,cell2.num))
                                            flag=1
                                            break
                                    if(flag != 1) :
                                        Cell_list[i][j].append(Cell(word=word[0], left=cell1.num, right=cell2.num, num=cnt))
                                        cnt = cnt + 1
                for cell3 in Cell_list[i][j]:
                    fo1.write( str(cell3.num) + ' (' + cell3.word + ' , ' +str(cell3.child) + ')'+ '\n')
    return Cell_list[i][j]



"""
def printsyntax(num, string,fo,stridx):
    print(stridx)

    global index

    if num is not None:

        print(num)
        print(arr[num][0])
        print(type(arr[num][1]))
        print("인덱스는",index)
        for i in range(index+1):
            print(string[i])
        if type(arr[num][1]) is str:
            print("한개짜리들어옴")
           # print("str or int")
            if arr[num][1].isdigit():
                string[index] = string[index] + "(" + str(arr[num][0])
                printsyntax(arr[num][1]-1, string,fo,stridx)
                string[index] = str(string[index]) + ")"
            else:
                string[index] = string[index] + " (" + arr[num][0] +" , "+arr[num][1] + " "+ ") "
               # fo.write(string[0]+"\n")

            return 1
        if type(arr[num][1]) is int:
            print("한개짜리들어옴")
            string[index] = str(string[index]) + "(" + str(arr[num][0])
            printsyntax(arr[num][1]-1, string,fo,stridx)
            string[index] = str(string[index]) + ")"
            return 1
        idx=0
        idxcnt=0
        savestring=string[index]
       # if len(arr[num][1])>=2:
        #    for i in range(len(arr[num][1])-1):
         #       string.append(string[stridx])
          #      index=index+1
       # stridx=stridx+idxcnt
        sumprecnt=0
        for numtuple in arr[num][1]:
            idx=idx+1
            if(idx>1):
                string.append(savestring)
                #stridx = stridx + 1
                index=index+1
                stridx=index
            #print(str(numtuple))
            num1=numtuple[0]
            string[index] = str(string[index]) + "(" + str(arr[num][0]) + " "
            print("왼쪽 들감")
            print('\n',index, string[index])
            precnt=printsyntax(num1-1, string,fo,stridx)
            print("precnt의 값은? ", precnt)
            if len(numtuple)!=1:
                #if(precnt>=2):
                 #   index-=1;
                for i in range(precnt):

                    num2=numtuple[1]
                    print("오른쪽들감")
                    print("i값",i)
                    print("precnt의 값은? ", precnt)
                    precnt2=printsyntax(num2-1, string,fo,stridx)
                    print("precnt2의 값은? ", precnt2)

                    index=index-precnt+i+1
                    string[index]=string[index]+" ) "
                    sumprecnt+=precnt2
              #  if (precnt>=2):
               #     index += 1
            else :
                print("이게과연나올까 ?")
    return sumprecnt
"""
def print_output(num, fp):
    #print(arr[num])
    if num is not None:
        if len(arr[num]) == 2:
            if type(arr[num][1]) is str:
              #  print("str")
                fp.write("(" + arr[num][0]+" "+arr[num][1] + ")")
                return
            if type(arr[num][1]) is int:
              #  print("int")
                fp.write("(" + str(arr[num][0]) + " ")
                print_output(arr[num][1] - 1, fp)
            return

        fp.write("(" + str(arr[num][0]) + " ")
        print_output(arr[num][1] - 1, fp)
        print_output(arr[num][2] - 1, fp)
        fp.write(")")

        #fp.write(")")
def makealltree(sentence ,grammar_list,arr):
    Cell_list=[]
    cnt=1;
    for word1 in sentence:
        row_list=[]
        for word2 in sentence:
            col_list=[]
            row_list.append(col_list)
        Cell_list.append(row_list)
    for j in range(len(sentence)):
        for i in reversed(range(0, j+1)):
            #print ("카운트",i,j)
            if i==j:
                for grammar in grammar_list:
                    if sentence[i] in grammar :
                        Cell_list[i][j].append(Cell(word=grammar[0], left=None, right=None, num=cnt))
                        arr.append([grammar[0],grammar[1]])
                        cnt=cnt+1
                Cell_list[i][j] , cnt = selfmake(grammar_list , Cell_list[i][j] ,None,cnt,arr)
            else:
                for k in range(i,j):
                    for cell1 in Cell_list[i][k]:
                        for cell2 in Cell_list[k+1][j]:
                            for word in grammar_list:
                                if len(word) < 3:
                                    continue
                                if cell1.word == word[1] and cell2.word == word[2]:
                                        Cell_list[i][j].append(Cell(word=word[0], left=cell1.num, right=cell2.num, num=cnt))
                                        arr.append([word[0], cell1.num,cell2.num])
                                        cnt = cnt + 1
    return Cell_list[i][j]
if __name__ == '__main__':
    grammar_list=[]
    input_list=[]
    #final_cell_list=[]
    #str_list=[]
    #string=""
    #arr=[]
    #newcell=[]
    #precnt=0
    fg=open('grammar.txt','r')

    for line in fg.readlines():
        grammar_list.append(line.strip().replace("->","").split())
  #  print(grammar_list)
    fi=open("input.txt","r")
    fo1 = open('used_grammar.txt', 'w')
    fo2 = open('output.txt', 'w')

    for line in fi.readlines():
        input_list.append(line.strip())
        final_cell_list=packed_cky_parse(line.strip().split(),grammar_list,fo1)
        fo1.write('\n')
        arr=[]
        newcell=makealltree(line.strip().split(),grammar_list,arr)
        #print(arr)
        for cell in newcell:
            if cell.word == 'S':
                print_output(cell.num-1,fo2)
                fo2.write('\n')

        fo2.write('\n')

    fo1.close()
    fo2.close()
        #str_list.append("")
        #precnt = printsyntax(len(arr)-2,str_list,fo2,0)


  #  print(input_list[0])


