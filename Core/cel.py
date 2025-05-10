#Funckja Celu im bliżej cel tym lepszy wynik.

def funkcjaCelu(zbiorLiczb, cel):
    return -abs(sum(zbiorLiczb) - cel) - 0.1 * len(zbiorLiczb)

# Mapowanie 0/1 na konkretne liczby
def funkcjaCeluMapowana(genotype, all_numbers, cel):
    selected = [num for bit, num in zip(genotype, all_numbers) if bit == 1]
    suma = sum(selected)
    return -abs(suma - cel)

