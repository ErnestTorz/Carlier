# Carlier

from operator import itemgetter
import copy
import timeit
import time
class PriorityQueue:

    def __init__(self, key, rev, list):
        self._key = key
        self._rev = rev
        if len(list) == 0:
            self._list = []
        else:
            self._list = list.sort(key=key, reverse=rev)

    def delete(self):
        self._list.pop(-1)

    def add(self, val):
        self._list.append(val)
        self._list.sort(key=self._key, reverse=self._rev)

    def is_empty(self):
        if len(self._list) == 0:
            return True
        else:
            return False

    def get_element(self):
        return self._list[-1]

    def get_r(self, nb):
        return self._list[-1][1]

def schrage(data):
    t = 0
    k = 0
    b = 0 # indeks zadania z cmaxem w permutacji
    N = PriorityQueue(itemgetter(1), True, [])
    G = PriorityQueue(itemgetter(3), False, [])

    C_max = 0
    pi = []

    for i in range(0, len(data)):
        N.add([int(data[i][0]), int(data[i][1]), int(data[i][2]), int(data[i][3])])

    while G.is_empty() is False or N.is_empty() is False:  
        while N.is_empty() is False and int(N.get_r(0)) <= t:  
            e = N.get_element()
            G.add(e)
            N.delete()
        if G.is_empty() is True:                                     
            t = int(N.get_r(0))                                   
        else:
            e = G.get_element()
            G.delete()
            pi.append(e)
            t += int(e[2])
            if C_max <= int(t+int(e[3])):
                C_max = int(t+int(e[3]))
                b = k
            k += 1
            
    return pi,C_max,b

def schrage_div(data):
    n = len(data)
    t = 0                                           # total time
    N = PriorityQueue(itemgetter(1), True, [])      # list of unordered tasks
    G = PriorityQueue(itemgetter(3), False, [])     # list of ready to implementation tasks

    C_max = 0
    pi = []
   

    for i in range(0, n):
        N.add([int(data[i][0]), int(data[i][1]), int(data[i][2]), int(data[i][3])])

    onMachine=[0, 0, 0, 999999]                    # current task initialization

    while G.is_empty() is False or N.is_empty() is False:   # check if at least one OR lists isn't empty
        while N.is_empty() is False and int(N.get_r(0)) <= t:  # check if N isn't empty AND availability time is less than total time
            e = N.get_element()                                # ready task
            G.add(e)
            N.delete()
            if e[3] > onMachine[3]:                            # check if time to complete ready task is higher than time on machine
                onMachine[2] = t - e[1]
                t = e[1]
                if onMachine[2] > 0:
                    G.add(onMachine)

        if G.is_empty() is True:                                     
            t = int(N.get_r(0))                                    
        else:
            e = G.get_element()
            G.delete()
            onMachine = e
            pi.append(e)
            t += int(e[2])
            C_max = max(C_max, int(t+int(e[3])))


    return C_max

def findA(lst, b, Cmax):
    sum = a = 0
    for i in range(0, b + 1):
        sum += lst[i][2]

    while a < b and not Cmax == (lst[a][1] + lst[b][3] + sum):
        sum -= lst[a][2]
        a += 1
    return a

def findC(lst, a, b):
    for i in range(b - 1, a - 1, -1):
        if lst[i][3] < lst[b][3]:
            return i
    return None

def findRPQprim(lst, b, c):
    rprim = lst[c + 1][1]
    pprim = 0
    qprim = lst[c + 1][3]

    for i in range(c + 1, b + 1):
        if lst[i][1] < rprim:
            rprim = lst[i][1]
        if lst[i][3] < qprim:
            qprim = lst[i][3]
        pprim += lst[i][2]

    return rprim, pprim, qprim

def carlier(lst):
    lst, Cmax, b = schrage(copy.deepcopy(lst)) # lst - permutacja zadań, C-max - górne oszacowanie, b - pozycja ostatniego w ścieżce krytycznej
    a = findA(lst, b, Cmax) # pozycja pierwszego zadania w ścieżce krytycznej
    c = findC(lst, a, b) # zadanie o jak najwyższej pozycji ale z mniejszym q_pi_j < q_pi_b
    if not c: # jeśli nie znaleziono takiego to c_max jest roziwązaniem optymalnym
        return Cmax,lst 

    rprim, pprim, qprim = findRPQprim(lst, b, c) # min r, max q, suma czasów wykonania zadań - w bloku (c+1, b)
    r_saved = lst[c][1] # zapisz r
    lst[c][1] = max(lst[c][1], rprim + pprim) # modyfikacja terminu dostępności zadania c, wymusi to jego późniejszą realizację, za wszystkimi zadaniami w bloku(c+1, b)
    LB = schrage_div(copy.deepcopy(lst)) # sprawdzamy dolne ograniczenie schrage z podziałem  - dla wszystkich permutacji spełniających to wymaganie

    if LB < Cmax: # sprawdź czy rozwiązanie jest obiecujące
        pomCmax, pomlst = carlier(lst)
        Cmax = min(Cmax, pomCmax) # wywołaj carliera jeszcze raz dla nowego problemu

    lst[c][1] = r_saved # odtwórz r

    q_saved = lst[c][3]
    lst[c][3] = max(lst[c][3], pprim + qprim) # wymuszenie aby zadanie c było wykonywane przed wszystkimi zadaniami w bloku (c+1, b)
    LB = schrage_div(copy.deepcopy(lst)) # sprawdź czy taki problem jest obiecujący

    if LB < Cmax:
        pomCmax, pomlst = carlier(lst)
        Cmax = min(Cmax, pomCmax)

    lst[c][3] = q_saved # przywróc q

    return Cmax,lst 


if __name__ == '__main__':
    tasks=[
    #   nr, r , p, q
        [1, 28, 5, 7], 
        [2, 13, 6, 26], 
        [3, 11, 7, 24], 
        [4, 20, 4, 21], 
        [5, 30, 3, 8], 
        [6, 0, 6, 17], 
        [7, 30, 2, 0]
    ]
    print("Dane wejsciowe, w formacie [nr, r, p, q] :")
    print (*tasks, sep = "\n")
    start_time = time.time()
    Cmax, result = carlier(tasks)
    execution_time = time.time() - start_time
    print()
    print("Wynik: "+" CMAX = " + str(Cmax)+"  Czas: " + str(execution_time)+" s" )
    print("Dane wyjsciowe, w formacie [nr, r, p, q] :")
    print(*result, sep="\n")