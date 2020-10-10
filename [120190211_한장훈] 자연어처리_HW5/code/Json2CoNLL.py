import json
input_file="../data/2016lipexpo_NERcorpus_train.json"
output_file="../data/NER_train.txt"

if __name__=='__main__':
	with open(input_file, 'r', encoding="utf-8") as json_file:
		json_data = json.load(json_file) #load랑 loads 랑 달라
	sentence_list=json_data['sentence']
	with open(output_file, 'w') as fpw:
		for sentence in sentence_list:  #한 sentece 안에 word와 morph와 Ne정보가 담겨있다.
			#print(sentence)
			morphs=[]
			for morph in sentence['morp']:
				morph['ne'] = 'O'
				morphs.append(morph)
				#print("1",morph)
			for ne in sentence['NE']:
				for i in range(ne['begin'],ne['end']+1):
					if i==ne['begin']:
						morphs[i]['ne']='B-%s'%ne['type']
					else:
						morphs[i]['ne']='l-%s'%ne['type']

			for morph in morphs:
				#print(morph)
				data=morph['lemma']+'/'+morph['type']+' '+morph['ne']
				fpw.write(data)
				fpw.write('\n')
			fpw.write('\n')

