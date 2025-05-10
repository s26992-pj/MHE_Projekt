#Funckja Celu im bliżej cel tym lepszy wynik.

def funkcjaCelu(zbiorLiczb, cel):
    return -abs(sum(zbiorLiczb) - cel) - 0.5 * len(zbiorLiczb)