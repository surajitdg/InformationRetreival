import json
import math
import operator


class IBM1:

    def __init__(self):
        self.sentence_alignment = []
        self.sentence_alignment_index = []

    # Routine to uniformly initialize word translation probabilities in t hash

    def initialize_probability(self, t, init_value, en_words, fr_words):
        for foreign_word in fr_words:
            for english_word in en_words:
                tup = (english_word, foreign_word)
                t[tup] = init_value


    # Generate Alignment for all sentences in the corpus
    def generate_alignment(self, file_path):
        with open(file_path) as file:
            data = json.load(file)

        fr_sentences = []
        en_sentences = []

        fr_en_dic = {}

        for i in range(len(data)):
            fr_sentences.append(data[i]['fr'])
            en_sentences.append(data[i]['en'])
            fr_en_dic[data[i]['fr']] = data[i]['en']

        print(fr_sentences)
        print(en_sentences)

        fr_words = []
        en_words = []

        fr_count = {}
        en_count = {}

        fr_sent_list = []
        en_sent_list = []

        for sent in fr_sentences:
            fr_sent = []
            for word in sent.split(" "):
                fr_sent.append(word)
            fr_sent_list.append(fr_sent)

        for sent in en_sentences:
            en_sent = []
            for word in sent.split(" "):
                en_sent.append(word)
            en_sent_list.append(en_sent)

        print(fr_sent_list)
        print(en_sent_list)

        sentence_pairs = []

        for i in range(len(fr_sentences)):
            list_of_sent = []
            list_of_sent.append(fr_sent_list[i])
            list_of_sent.append(en_sent_list[i])
            sentence_pairs.append(list_of_sent)

        print(sentence_pairs)


        for sent in fr_sentences:
            for word in sent.split(" "):
                if word not in fr_words:
                    fr_words.append(word)
                if word in fr_count:
                    fr_count[word] += 1
                else:
                    fr_count[word] = 1

        for sent in en_sentences:
            for word in sent.split(" "):
                if word not in en_words:
                    en_words.append(word)
                if word in en_count:
                    en_count[word] += 1
                else:
                    en_count[word] = 1

        print('English words in corpus: ', en_words)
        print('Foreign words in corpus: ', fr_words)

        num_en_words = len(en_words)
        num_fr_words = len(fr_words)
        print('*****************************************************************************')

        print('english_vocab_size: ', num_en_words)
        print('foreign_vocab_size: ', num_fr_words)

        print('*****************************************************************************')

        fr_words_set = set(fr_words)

        iteration_count = 0
        s_total = {}
        repeat_flag = True
        initial_convergence = True
        check_convergence_list = []

        # Initialize probabilities uniformly
        t = {}
        init_value = 1.0 / num_fr_words
        self.initialize_probability(t, init_value, en_words, fr_words)

        print('No. of foreign/english word pairs: ', len(t))
        print('Initialized Probability: ', t)
        print('*****************************************************************************')
        print()

        # Loop while not converged
        #for iter in range(num_iterations):
        while repeat_flag:

            # Initialize
            count = {}
            total = {}
            iteration_count += 1
            for foreign_word in fr_words:
                total[foreign_word] = 0.0
                for english_word in en_words:
                    count[(english_word, foreign_word)] = 0.0

            for sp in sentence_pairs:

                # Compute normalization
                for english_word in sp[1]:
                    s_total[english_word] = 0.0
                    for foreign_word in sp[0]:
                        s_total[english_word] += t[(english_word, foreign_word)]

                # Collect counts
                for english_word in sp[1]:
                    for foreign_word in sp[0]:
                        count[(english_word, foreign_word)] += t[(english_word, foreign_word)] / s_total[english_word]
                        total[foreign_word] += t[(english_word, foreign_word)] / s_total[english_word]

            # Estimate probabilities
            for foreign_word in fr_words:
                for english_word in en_words:
                    t[(english_word, foreign_word)] = count[(english_word, foreign_word)] / total[foreign_word]
                    if initial_convergence:
                        check_convergence_list.append(t[(english_word, foreign_word)])

            print('*****************************************************************************')

            for foreign_word in fr_words:
                for english_word in en_words:
                    print('t(', english_word, '|', foreign_word, ')', t[(english_word, foreign_word)])
            print('*****************************************************************************')

            list_counter = 0
            equal_count = 0

            for foreign_word in fr_words:
                for english_word in en_words:
                    if math.isclose(t[(english_word, foreign_word)], check_convergence_list[list_counter], abs_tol=0.001):
                        equal_count += 1
                    list_counter += 1

            print("Equal count = ", equal_count)
            print("Iteration Count = ", iteration_count)

            if equal_count == len(t) and initial_convergence is False:
                repeat_flag = False
                sorted_d = sorted(t.items(), key=operator.itemgetter(1), reverse=True)

                new_fr_set = set()
                french_english_dict = {} #Dictionary for the entire corpus

                for tup in sorted_d:
                    french_word = tup[0][1]
                    english_word = tup[0][0]
                    if french_word not in new_fr_set:
                        new_fr_set.add(french_word)
                        french_english_dict[french_word] = english_word
                        diff_set = fr_words_set.difference(new_fr_set)
                        if len(diff_set) == 0:
                            break

                print("Alignment of words in the entire corpus= ")
                print(french_english_dict)

                itr = 0
                for fr_sentence in fr_sent_list:
                    align_list = []
                    new_dict = {}
                    for word in fr_sentence:
                        if word not in new_dict:
                            new_dict[word] = french_english_dict[word]
                            x = fr_sentence.index(word)
                            y = en_sent_list[itr].index(french_english_dict[word])
                            align_tuples = (y, x)
                            align_list.append(align_tuples)

                    self.sentence_alignment_index.append(sorted(align_list))
                    self.sentence_alignment.append(new_dict)
                    itr += 1

                print("Alignment for each sentence in the corpus = ")

                #for i in range(len(list_sent_dict)):
                #    print(list_sent_dict[i])

            else:
                list_counter = 0
                equal_count = 0

                for foreign_word in fr_words:
                    for english_word in en_words:
                        check_convergence_list[list_counter] = t[(english_word, foreign_word)]
                        list_counter += 1

                initial_convergence = False


