from collections import defaultdict
from tqdm import tqdm, trange
import numpy as np
import random
import pickle
from itertools import permutations

SENTENCE_LIMIT = 6  # max number of printed possible permutations of the sentence


def load_ngrams_consisting_words_and_create_mapping(filename, words_in_sentences, n):
    mapping = defaultdict(set)
    mapping_count = defaultdict(int)
    
    total = 0
    if n == 2:
        total = 59134225
    elif n == 3:
        total = 179473348
    pbar = tqdm(desc='Creating successor mapping', total=total)
    with open(filename, 'r') as f:
        row = f.readline().lower().strip()
        
        while row:
            pbar.update(1)
            if type(row) is str:
                row = row.split()
            
            cnt = int(row[0])
            words = row[1:-1]
            rest = row[-1]
            
            if cnt < 2:
                row = f.readline().lower().strip()
                continue
            
            if all([sent_word not in words for sent_word in words_in_sentences]):
                row = f.readline().lower().strip()
                continue
            
            if len(words) == 1:
                words = words[0]
            else:
                words = tuple(words)
            
            mapping[words].add(rest)
            mapping_count[(words, rest)] += cnt
            
            row = f.readline().lower().strip()
    pbar.close()
    return mapping, mapping_count


def load_input():
    return open('data/input_task4.txt', 'r').read().lower().split('\n')


def compute_naturalness_bigram(sentence, mapping, mapping_count):
    """
    Being sum of occurrences of sequences of words in the mapping.
    """
    prev_word = sentence[0]
    
    naturalness = 0
    
    for word in sentence[1:]:
        occurences = mapping_count[(prev_word, word)]
        naturalness += occurences
        prev_word = word
        
    return naturalness


def compute_naturalness_trigram(sentence, mapping, mapping_count):
    """
    Being sum of occurrences of sequences of words in the mapping.
    """
    prev_word = tuple(sentence[:2])
    
    naturalness = 0
    
    for word in sentence[2:]:
        occurences = mapping_count[(prev_word, word)]
        naturalness += occurences
        prev_word = prev_word[1:] + tuple(word)
        
    return naturalness


def reconstruct_sentence(words, mapping, mapping_count, compute_naturalness_func):
    possible_sentences = np.array(list(permutations(words)))
    possible_naturalness = np.array(
        list(map(
            lambda sent: 
                compute_naturalness_func(
                    sentence=sent, 
                    mapping=mapping, 
                    mapping_count=mapping_count,), 
            tqdm(possible_sentences, desc='Computing naturalness')))
    )
    
    ordering = np.argsort(possible_naturalness)[::-1]
    
    return possible_sentences[ordering], possible_naturalness[ordering]


def print_results(sentence, possible_sentences, possible_naturalness):
    total_naturalness = np.sum(possible_naturalness)
    
    print(f'Original: {sentence}')
    print('Reconstructed')
    for i, pos_sent in enumerate(possible_sentences):
        if i >= SENTENCE_LIMIT:
            break
        print(' '.join(pos_sent), f' --- score: {possible_naturalness[i] / total_naturalness}')
    print('-'*100)


def main():
    sentences = load_input()
    words_in_sentences = set(' '.join(sentences).split())
    # bigram_mapping, bigram_mapping_count = load_ngrams_consisting_words_and_create_mapping('data/poleval_2grams.txt', words_in_sentences, 2)
    
    # positions = []
    # print('-'*40, 'BIGRAM', '-'*40)
    # for sentence in sentences:
    #     sentence = sentence.strip()
    #     words = sentence.split()
    #     possible_sentences, possible_naturalness = reconstruct_sentence(
    #         words=words, 
    #         mapping=bigram_mapping, 
    #         mapping_count=bigram_mapping_count,
    #         compute_naturalness_func=compute_naturalness_bigram,
    #     )
    #     possible_sentences = list(map(lambda words: ' '.join(words), possible_sentences))
    #     position = np.nonzero(np.array(possible_sentences) == sentence)[0][0]
    #     positions.append(position)
    #     # print_results(sentence, possible_sentences, possible_naturalness)
    # print(f'result: {np.mean(1 / (np.array(positions)+1))}\ngood ones: {np.count_nonzero(np.array(positions) == 0)}')
# result: 0.2547829169450466
# good ones: 14
    
    
    trigram_mapping, trigram_mapping_count = load_ngrams_consisting_words_and_create_mapping('data/poleval_3grams.txt', words_in_sentences, 3)
    
    positions = []
    print('-'*40, 'TRIGRAM', '-'*40)
    for sentence in sentences:
        sentence = sentence.strip()
        words = sentence.split()
        possible_sentences, possible_naturalness = reconstruct_sentence(
            words=words,
            mapping=trigram_mapping, 
            mapping_count=trigram_mapping_count,
            compute_naturalness_func=compute_naturalness_trigram,
        )
        # print_results(sentence, possible_sentences, possible_naturalness)
        possible_sentences = list(map(lambda words: ' '.join(words), possible_sentences))
        position = np.nonzero(np.array(possible_sentences) == sentence)[0][0]
        positions.append(position)
    print(f'result: {np.mean(1 / (np.array(positions) + 1))}\ngood ones: {np.count_nonzero(np.array(positions) == 0)}')
# result: 0.0957230449955125
# good ones: 5
        
if __name__ == '__main__':
    main()