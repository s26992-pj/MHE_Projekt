# MHE_Projekt



# Installation

```bash
git clone https://github.com/s26992-pj/MHE_Projekt.git
```
# Struktura Projektu
```python
├── Algorithms/
│ └── bruteForce.py
│ └── genetic.py
│ └── hillClimb.py
│ └── simulatedAnnealing.py
│ └── tabu.py
├── Core/
│ └── cel.py
│ └── generateNeighbours.py
│ └── loadData.py
│ └── randomSolution.py
├── data.txt
├── testAll.py
└── subsetSumComandLine.py
```
# Usage

Moim Tematem jest Subset sum problem 

Opis problemu: Subset Sum Problem (SSP)
Problem podzbioru sumy (Subset Sum Problem) polega na znalezieniu takiego podzbioru elementów z danego zbioru liczb całkowitych, którego suma jest równa zadanej wartości docelowej (target sum). Formalnie:

Dane:
Zbiór liczb całkowitych:
𝑆
=
{
𝑠
1
,
𝑠
2
,
.
.
.
,
𝑠
𝑛
}
S={s 
1
​
 ,s 
2
​
 ,...,s 
n
​
 }

Wartość docelowa:
𝑇
∈
𝑍
T∈Z

 Pytanie:
Czy istnieje taki podzbiór 
𝑆
′
⊆
𝑆
S 
′
 ⊆S, że:

∑
𝑥
∈
𝑆
′
𝑥
=
𝑇
x∈S 
′
 
∑
​
 x=T
🔍 Przykład:
= {3, 34, 4, 12, 5, 2}

T = 9

Rozwiązanie: Tak, bo podzbiór {4, 5} daje sumę 9

# Funkcja Celu
#### Funkcja Celu im bliżej cel tym lepszy wynik. Zwraca wartość minusową dzięki czemu kara którą zaimplementowałem z powodu na długość rozwiązania jest naliczana lepiej.
```Python

def funkcjaCelu(zbiorLiczb, cel):
    return -abs(sum(zbiorLiczb) - cel) - 0.5 * len(zbiorLiczb)
```

```python
#Commands

#Test All with Suppress function
python testAll.py --file data.txt --target 150 --suppress 1


#Base
python subsetSumComandLine.py base --file data.txt --target 100       
#Tabu
python subsetSumComandLine.py tabu --file data.txt --target 20 --size 5
#simulated
python subsetSumComandLine.py simulated --file data.txt --target 100 --schedule exponential --alpha 0.95
#genetic
python subsetSumComandLine.py genetic --file data.txt --target 100 --pop 10 --cross one_point --mut add_remove --stop no_improve --elite 0
#bruteForce
python subsetSumComandLine.py bruteforce --file data.txt --target 100
#hillClimb
python subsetSumComandLine.py hillclimb --file data.txt --target 100 --mode random
python subsetSumComandLine.py hillclimb --file data.txt --target 100 --mode best  
```

# Zaimplementowane Algorytmy
##  Brute Force
Opis: Przegląda wszystkie możliwe podzbiory zbioru wejściowego. \
Złożoność: O(2ⁿ), gdzie n to liczba elementów. \
Zalety: Gwarantuje znalezienie rozwiązania (jeśli istnieje). \
Wady: Bardzo nieefektywny przy dużych zbiorach

## Algorytm Genetyczny (Genetic Algorithm)
Opis: Populacja losowych rozwiązań (osobników) ewoluuje poprzez selekcję, krzyżowanie i mutację. \
Zalety: Może znaleźć dobre (choć niekoniecznie optymalne) rozwiązanie w rozsądnym czasie. \
Wady: Parametry (rozmiar populacji, szansa mutacji, itp.) silnie wpływają na jakość i czas działania.

## Hill Climbing
Opis: Zaczyna od jednego rozwiązania i iteracyjnie przechodzi do najlepszego sąsiada. \
Zalety: Szybki i prosty. \
Wady: Może utkwić w lokalnym maksimum/minimum (czyli podzbiorze, który jest lepszy od sąsiadów, ale nie najlepszy globalnie).

## Simulated Annealing
Opis: Podobny do hill climbing, ale dopuszcza „gorsze” ruchy z pewnym prawdopodobieństwem, które maleje z czasem (temperatura).  
Zalety: Może ominąć lokalne minima. \
Wady: Wymaga dostrojenia harmonogramu chłodzenia; dłuższy czas działania niż hill climbing. 

## Tabu Search
Opis: Wyszukiwanie lokalne z pamięcią – zapamiętuje ostatnie odwiedzone stany (lista tabu), aby unikać cykli. \
Zalety: Potrafi omijać lokalne minima lepiej niż hill climbing. \
Wady: Wymaga zarządzania listą tabu; parametry mają wpływ na skuteczność.

## Wybór Mutacji 
### mutate_add_remove:
Mutacja dodania lub usunięcia elementu
Opis:
Ta mutacja dodaje nowy element do rozwiązania lub usuwa istniejący, z pewnym prawdopodobieństwem (mutation_rate). 
#### Zaleta: Pozwala się wyłamać prze usunięcie, Dodanie elementu
### mutate_swap: 
Mutacja typu zamiana miejscami
Opis:
Ta mutacja zamienia miejscami dwa losowe elementy w rozwiązaniu. \
#### Zaleta: Nie usuwa Elementów a jedynie kolejność

