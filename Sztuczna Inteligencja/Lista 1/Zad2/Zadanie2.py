def convert_line(line):
    global dict

    line = " " + line

    in_dict = [0 for _ in range(len(line))]
    in_dict[0] = 1

    start_index = [[] for _ in range(len(line))]

    for i in range(1, len(line)):
        if line[1:i+1] in dict:
            in_dict[i] = 1

    for i in range(1, len(line)):
        for j in range(i + 1):
            if in_dict[j - 1] and line[j:i+1] in dict:
                in_dict[i] = 1
                start_index[i].append(j)

    max_word = [[0, []] for _ in range(len(line))]
    valid = [False for _ in range(len(line))]
    valid[-1] = True

    for i in reversed(range(1, len(line))):
        if valid[i]:
            for j in range(len(start_index[i])):
                start_word = start_index[i][j]
                val = max_word[i][0] + (start_word - i + 1) ** 2
                if val > max_word[start_word-1][0]:
                    max_word[start_word - 1] = [val, [start_word] + max_word[i][1]]
                    valid[start_word - 1] = True

    res = list(line)

    for ind in reversed(max_word[0][1]):
        res.insert(ind, " ")

    f = open("zad2_output.txt", "a")
    f.write(''.join(res[2:]) + "\n")
    f.close()
    print(''.join(res[2:]))


def load():
    global dict, text
    dict = set(open("words_for_ai1.txt", "r").read().split("\n"))
    text = open("zad2_input.txt", "r").read().split("\n")


def convert():
    for line in text:
        convert_line(line)

open("zad2_output.txt", "w").close()
load()
convert()