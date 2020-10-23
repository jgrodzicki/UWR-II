import re
import numpy as np
from tqdm import tqdm, trange


def load_sample_corpus():
    return set(re.sub(r'\W', ' ', open('data/polish_corpora_mln.txt', 'r').read().lower()).split())


def preprocess_text(text):
    text = text.lower().strip()
    text = text.replace('\n', ' ')
    text = re.sub(r'\d', '', text)
    # text = re.sub(r'[^ a-zA-Zęóąśłżźć]', ' ', text)
    text = re.sub(r'[„”()>?,\.:]', ' ', text)
    text = re.sub(r'\ +', ' ', text)
    return text.strip()


def reconstruct_max_match(text, corpus):
    res = ''
    idx = 0
    new_idx = 0
    max_word_len = np.max(list(map(lambda w: len(w), corpus)))

    while idx < len(text):
        for end in range(idx+max_word_len+2, idx+1, -1):
            if text[idx:end] in corpus:
                res += text[idx:end] + ' '
                new_idx = end
                break

        if idx == new_idx:
            res += text[idx] + ' '
            new_idx += 1
        idx = new_idx
    return res


def reconstruct_max_squared_word_len(text, corpus):
    res = text
    
    idx_word_start = [[] for _ in range(len(text)+1)]
    idx_word_start[0] = [(0, 0)]
    
    # for end in range(len(text)+1):
    #     if text[:end] in corpus:
    #         idx_word_start[end].append((0, (end+1)**2))
        
    max_word_len = np.max(list(map(lambda w: len(w), corpus)))

    for start in range(len(text)):
        if len(idx_word_start[start]) == 0:
            continue
        max_len = np.max([list(map(lambda sv: sv[1], idx_word_start[start]))])
        
        for end in range(start+1, min(start+1+max_word_len, len(text)+1)):
            if text[start:end] in corpus:
                idx_word_start[end].append((start, max_len+(end-start+1)**2))
                
    print(idx_word_start)
    idx = len(text)
    while idx > 0:
        best_start, best_value = -1, -1
        for start, value in idx_word_start[idx]:
            if value > best_value:
                best_start, best_value = start, value
        idx = best_start
        res = res[:idx] + ' ' + res[idx:]
        return res


def compute_similarity(produced, original):
    """
    Measures similarity as a ratio of correct spaces to total number of spaces in original text.
    """
    no_spaces_good = 0
    i_prod, i_og = 0, 0
    while i_prod < len(produced) and i_og < len(original):
        if produced[i_prod] == original[i_og] == ' ':
            no_spaces_good += 1
        if produced[i_prod] == ' ' and original[i_og] != ' ':
            i_prod += 1
        elif produced[i_prod] != ' ' and original[i_og] == ' ':
            i_og += 1
        else:
            i_prod += 1
            i_og += 1
    return no_spaces_good / (len(produced.split()) - 1)


def main():
    corpus = load_sample_corpus()
    original_text = preprocess_text(open('data/input_task1.txt', 'r').read())
    no_spaces = original_text.replace(' ', '')
    after_max_match = reconstruct_max_match(no_spaces, corpus)
    print(after_max_match)
    print('Similarity max_match: ', compute_similarity(after_max_match, original_text))

    # after_reconstruct = reconstruct_max_squared_word_len(no_spaces, corpus)
    # print(after_reconstruct)
    # print('Similarity max squared: ', compute_similarity(after_reconstruct, original_text))


if __name__ == '__main__':
    main()
