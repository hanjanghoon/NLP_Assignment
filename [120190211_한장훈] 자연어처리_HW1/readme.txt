자연어 처리 HW1

120190211 한장훈

사용 언어 PYTHON 3.6
개발환경 JetBrains PyCharm 2018.3.5 x64

제출 파일 
manual_tagging.hwp
grammar.txt
dictionary_TRIE.hwp
POS_tagger.zip
readme.txt

POS_tagger.zip 안에는 tabular parser을 구현한 pos_tagger.py 와, grammar를 만드는 grammar.py
사전을 만드는 dictionary_TRIE.py가 있습니다. 
그리고 그냥 문장이 들어간 original.txt파일과 manual_tagging 정보가 들어간 텍스트 파일이 있습니다.
grammar.txt 와 dictionary_Trie.txt는 각각 py파일 실행후 만들어지는 텍스트로써 문법정보와 사전정보를 가지고 있습니다.
output이 원본 original.txt 파일을 넣었을때 형태소가 분석되어 나온 txt파일입니다.

pos_tagger 실행시 grammar.txt가 없으면 실행되지 않습니다. 먼저 grammar.py 실행후 txt가 만들어지면 그 후에
pos_tagger가 실행됩니다.

자소 단위로 자르지 않고 음절단위로 잘라서 올바른 같은 경우에 올바르+ㄴ이 아닌 올바/른으로 처리했습니다.
조사의 경우 주격,목적격등 격조사는 일괄적으로 격조사로 나타냈으며 보조사는 따로 구분하였습니다.

감사합니다. 