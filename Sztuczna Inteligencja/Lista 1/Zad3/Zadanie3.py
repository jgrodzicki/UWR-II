import random


def losuj(karty_odrzucone=[]):
    global blot_karty, blot_kolory, fig_karty, fig_kolory
    blot_karty = [0] * 9
    blot_kolory = [0] * 4
    fig_karty = [0] * 4
    fig_kolory = [0] * 4
    pozostale = [i for i in range(35)]

    if karty_odrzucone:
        for karta in karty_odrzucone:
            pozostale.remove(karta)

    for i in range(5):
        r = random.randint(0, len(pozostale)-1)
        k = pozostale.pop(r)

        blot_karty[k // 4] += 1
        blot_kolory[k % 4] += 1

    pozostale = [i for i in range(0, 16)]
    for i in range(5):
        r = random.randint(0, len(pozostale)-1)
        k = pozostale.pop(r)
        fig_karty[k // 4] += 1
        fig_kolory[k % 4] += 1


def max_uklad_fig(karty, kolory):
    max = 0
    karty.sort(reverse=True)
    kolory.sort(reverse=True)

    if karty[0] == 4: #kareta
        max = 7
    elif karty[0] == 3 and karty[2] == 2: #ful
        max = 6
    elif kolory[0] == 4:#kolor
        max = 5
    elif karty[0] == 3: #trójka
        max = 3
    elif karty[0] == karty[1] == 2: #dwie pary
        max = 2
    elif karty[0] == 2: #para
        max = 1

    return max


def max_uklad_blot(karty, kolory):
    max = 0
    kolory.sort(reverse=True)

    if ''.join(str(e) for e in karty).find(str(11111)) != -1: # strit lub poker
        if kolory[0] == 5: # poker
            max = 8
        else: # strit
            max = 4

    karty.sort(reverse=True)

    if karty[0] == 4: #kareta
        max = 7
    elif karty[0] == 3 and karty[2] == 2: #ful
        max = 6
    elif kolory[0] == 4: #kolor
        max = 5
    elif karty[0] == 3: #trójka
        max = 3
    elif karty[0] == karty[1] == 2: #dwie pary
        max = 2
    elif karty[0] == 2: #para
        max = 1

    # print("max: " + str(max))
    return max


def porownaj(karty_odrzucone=[]):
    global  blot_karty, blot_kolory, fig_karty, fig_kolory

    wygrana_fig = 0
    wygrana_blot = 0
    il_rund = 10000
    for _ in range(il_rund):
        losuj(karty_odrzucone)

        if max_uklad_fig(fig_karty, fig_kolory) < max_uklad_blot(blot_karty, blot_kolory):
            wygrana_blot += 1
        else:
            wygrana_fig += 1

    print("Na " + str(il_rund) + " gier: wygrane figuranta: " + str(wygrana_fig) +  "\twygrane blotkarza: " + str(wygrana_blot) + "\t szansa na wygranie blotkarza(%): " + str(wygrana_blot/il_rund*100))


blot_karty = []
blot_kolory =[]
fig_karty = []
fig_kolory = []

porownaj() #wszystkie
porownaj([i for i in range(0, 35, 4)]) #3 kolory
porownaj([i for i in range(30)]) #zawsze kareta
porownaj([i for i in range(0, 35, 2)] + [i for i in range(1, 35, 4)]) #zawsze kolor
porownaj([i for i in range(0, 23)]) # 8, 9, 10
porownaj([i for i in range(0, 27)]) # 9, 10
