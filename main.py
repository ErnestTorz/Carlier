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



def schrage(data):
    t = 0
    k = 0
    b = 0 # indeks zadania z cmaxem w permutacji
    N = PriorityQueue(lambda i: i[0], True, [])
    G = PriorityQueue(lambda i: i[2], False, [])

    C_max = 0
    pi = []

    for i in range(0, len(data)):
        N.add([int(data[i][0]), int(data[i][1]), int(data[i][2])])

    while G.is_empty() is False or N.is_empty() is False:  # 2
        while N.is_empty() is False and int(N.get_element()[0]) <= t:  # 3
            e = N.get_element()
            G.add(e)
            N.delete()
        if G.is_empty() is True:                                     # 5
            t = int(N.get_element()[0])                                    # 6
        else:
            e = G.get_element()
            G.delete()
            pi.append(e)
            t += int(e[1])
            if C_max <= int(t+int(e[2])):
                C_max = int(t+int(e[2]))
                b = k
            k += 1
            


    return pi,C_max,b

def schrage_div(data):
    n = len(data)
    t = 0                                           # total time
    N = PriorityQueue(lambda i: i[0], True, [])      # list of unordered tasks
    G = PriorityQueue(lambda i: i[0], False, [])     # list of ready to implementation tasks

    C_max = 0
    pi = []
   

    for i in range(0, n):
        N.add([int(data[i][0]), int(data[i][1]), int(data[i][2])])

    onMachine=[0, 0, 999999]                    # current task initialization

    while G.is_empty() is False or N.is_empty() is False:   # check if at least one OR lists isn't empty
        while N.is_empty() is False and int(N.get_element()[0]) <= t:  # check if N isn't empty AND availability time is less than total time
            e = N.get_element()                                # ready task
            G.add(e)
            N.delete()
            if e[2] > onMachine[2]:                            # check if time to complete ready task is higher than time on machine
                onMachine[1] = t - e[0]
                t = e[0]
                if onMachine[1] > 0:
                    G.add(onMachine)

        if G.is_empty() is True:                                     # 5
            t = int((N.get_element())[0])                                    # 6
        else:
            e = G.get_element()
            G.delete()
            onMachine = e
            pi.append(e)
            t += int(e[1])
            C_max = max(C_max, int(t+int(e[2])))


    return C_max

def findA(list, b, Cmax):
    sum = a = 0
    for i in range(0, b + 1):
        sum += list[i][1]

    while a < b and not Cmax == (list[a][0] + list[b][2] + sum):
        sum -= list[a][1]
        a += 1
    return a

def findC(list, a, b):
    for i in range(b - 1, a - 1, -1):
        if list[i][2] < list[b][2]:
            return i
    return None

def findRPQprim(list, b, c):
    rprim = list[c + 1][0]
    pprim = 0
    qprim = list[c + 1][2]

    for i in range(c + 1, b + 1):
        if list[i][0] < rprim:
            rprim = list[i][0]
        if list[i][2] < qprim:
            qprim = list[i][2]
        pprim += list[i][1]

    return rprim, pprim, qprim

def carlier(list):
    list=sorted(list, key=lambda i: i[0]) # sortowanie po r
    list, Cmax, b = schrage(copy.deepcopy(list)) # list - permutacja zadań, C-max - górne oszacowanie, b - pozycja ostatniego w ścieżce krytycznej
    a = findA(list, b, Cmax) # pozycja pierwszego zadania w ścieżce krytycznej
    c = findC(list, a, b) # zadanie o jak najwyższej pozycji ale z mniejszym q_pi_j < q_pi_b
    if not c: # jeśli nie znaleziono takiego to c_max jest roziwązaniem optymalnym
       
        return Cmax, list

    rprim, pprim, qprim = findRPQprim(list, b, c) # min r, max q, suma czasów wykonania zadań - w bloku (c+1, b)
    r_saved = list[c][0] # zapisz r
    list[c][0] = max(list[c][0], rprim + pprim) # modyfikacja terminu dostępności zadania c, wymusi to jego późniejszą realizację, za wszystkimi zadaniami w bloku(c+1, b)
    LB = schrage_div(copy.deepcopy(list)) # sprawdzamy dolne ograniczenie schrage z podziałem  - dla wszystkich permutacji spełniających to wymaganie

    if LB < Cmax: # sprawdź czy rozwiązanie jest obiecujące
        Cmaxi,pom = carlier(list)
        Cmax = min(Cmax, Cmaxi) # wywołaj carliera jeszcze raz dla nowego problemu

    list[c][0] = r_saved # odtwórz r

    q_saved = list[c][2]
    list[c][2] = max(list[c][2], pprim + qprim) # wymuszenie aby zadanie c było wykonywane przed wszystkimi zadaniami w bloku (c+1, b)
    LB = schrage_div(copy.deepcopy(list)) # sprawdź czy taki problem jest obiecujący

    if LB < Cmax:
        Cmaxi,pom = carlier(list)
        Cmax = min(Cmax, Cmaxi)

    list[c][2] = q_saved # przywróc q

    return Cmax, list

if __name__=="__main__":
    tasks = []
    with open('data.txt') as f:
        for i in f:
            x, y, z = i.split()
            tasks.append([int(x), int(y), int(z)])
        start_time = time.time()
        Cmax, result = carlier(tasks)
        execution_time = time.time() - start_time
        print(result)
        print('Carlier | Cmax: ' + str(Cmax)  + ' | Czas: ' + str(execution_time)+'s')
