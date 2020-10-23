from collections import defaultdict
from tqdm import tqdm, trange
import numpy as np
import random

MIN_N = 2


def load_ngrams_and_create_mapping(filename):
    mapping = defaultdict(set)
    
    pbar = tqdm(desc='Creating successor mapping')
    with open(filename, 'r') as f:
        row = f.readline().strip()
        while row:
            pbar.update(1)
            if type(row) is str:
                row = row.split()
            if int(row[0]) < MIN_N:
                row = f.readline()
                continue
            
            word = row[1:-1]
            if len(word) == 1:
                word = word[0]
            else:
                word = tuple(word)
            rest = row[-1]
            
            mapping[word].add(rest)
            
            row = f.readline().strip()
    pbar.close()
    return mapping


def create_sentences_for_bigram(successor_mapping, length):
    pbar = tqdm(desc='Creating sentence', total=length)
    
    sentences = []
    last_word = random.sample(list(successor_mapping.keys()), 1)[0]
    text = last_word + ' '
    length -= 1
    pbar.update(1)

    while length:
        if last_word in successor_mapping:
            new_word = random.sample(successor_mapping[last_word], 1)[0]
        else:
            sentences.append(text + '.')
            text = ''
            new_word = random.sample(list(successor_mapping.keys()), 1)[0]

        text += new_word + ' '
        last_word = new_word

        length -= 1
        pbar.update(1)
    
    pbar.close()
    sentences.append(text)

    return sentences


def create_sentences_for_trigram(successor_mapping, length):
    pbar = tqdm(desc='Creating sentence', total=length)
    
    sentences = []
    last_words = tuple(random.sample(list(successor_mapping.keys()), 1))[0]
    print(last_words)
    text = ' '.join(last_words) + ' '
    length -= 1
    pbar.update(1)

    while length:
        if last_words in successor_mapping:
            new_word = random.sample(successor_mapping[last_words], 1)[0]
            text += new_word + ' '
            last_words = (last_words[1], new_word)
        else:
            sentences.append(text + '.')
            last_words = tuple(random.sample(list(successor_mapping.keys()), 1))[0]
            text = ' '.join(last_words) + ' '

        length -= 1
        pbar.update(1)
    
    pbar.close()
    sentences.append(text)

    return sentences


if __name__ == '__main__':
    # successor_mapping_bigram = load_ngrams_and_create_mapping('data/poleval_2grams.txt', 2)
    # sentences = create_sentences_for_bigram(successor_mapping_bigram, 100)
    # print('From bigrams')
    # print('\n'.join(sentences))
    # open('results/task2_bigram.txt', 'w+').writelines('\n'.join(sentences))
    
    # print('-'*100)
    
    successor_mapping_trigram = load_ngrams_and_create_mapping('data/poleval_3grams.txt', 3)
    sentences = create_sentences_for_trigram(successor_mapping_trigram, 100)
    print('From trigrams')
    print('\n'.join(sentences))
    open('results/task2_trigram.txt', 'w+').writelines('\n'.join(sentences))
    
    