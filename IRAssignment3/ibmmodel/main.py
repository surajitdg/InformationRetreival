from ibm1 import IBM1

file_path = 'data/data2.json'
ob = IBM1()
ob.generate_alignment(file_path)

#Alignment in the form of dictionary, representing french word as key and english word as value
sentence_alignment = ob.sentence_alignment

#Alignment in the form of index values of the words in french and corresponding english translation
sentence_alignment_index = ob.sentence_alignment_index

for i in range(len(sentence_alignment)):
        print(sentence_alignment[i])

for i in range(len(sentence_alignment_index)):
        print(sentence_alignment_index[i])
