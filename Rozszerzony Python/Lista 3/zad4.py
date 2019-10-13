import itertools
import random


def simplify(txt, max_len, max_no_words):
    txt = [w for w in txt.split(" ") if len(w) <= max_len]
    if len(txt) > max_no_words:
        to_delete = random.choice(list(itertools.combinations([i for i in range(len(txt))], len(txt) - max_no_words)))

        for to_del in reversed(to_delete):
            txt.remove(txt[to_del])
    return txt


t = "Podział peryklinalny inicjałów wrzecionowatych kambium charakteryzuje się ścianą podziałową inicjowaną w płaszczyźnie maksymalnej."
print(simplify(t, max(len(w) for w in t.split(" ")), len(t)))
print(simplify(t, 10, 5))
