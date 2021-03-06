import copy
from operator import attrgetter


class Task:
    def __init__(self, nr, r, p, q):
        self.nr = nr
        self.r = r
        self.p = p
        self.q = q

    def __str__(self):
        return f'Task nr: {self.nr} r:{self.r} p:{self.p} q:{self.q}'


class Maszyna:
    def __init__(self, tasks):
        # list of Task classes representing problems
        self._tasks = tasks
        self.Cmax, self.pi = self._carlier(self._tasks)

    def _schrage(self, tasks):
        # końcowa kolejka wykonywania zadań na maszynie
        pi = []
        k = 0
        Cmax = 0
        # zbiór gotowych zadań do realizacji
        G = []
        N = copy.deepcopy(tasks)
        def get_min_task_r(): return min(N, key=attrgetter('r'))
        def get_max_task_q(): return max(G, key=attrgetter('q'))
        t = get_min_task_r().r

        while G or N:
            while N and get_min_task_r().r <= t:
                j_prime = N.index(get_min_task_r())
                G.append(N.pop(j_prime))
            if G:
                j_prime = G.index(get_max_task_q())
                element = G.pop(j_prime)
                pi.append(element)
                t += pi[k].p
                if Cmax <= (t + element.q):
                    Cmax = t + element.q
                    b = k
                k += 1
            else:
                t = get_min_task_r().r

        return pi, Cmax, k

    def _schrage_pmtn(self, tasks):
        Cmax = 0
        G = []
        N = copy.deepcopy(tasks)
        t = 0
        # zmienna pomocnicza do przetrzymywania tasku
        help2 = Task(-1, 0, 0, float('inf'))

        def get_min_task_r(): return min(N, key=attrgetter('r'))
        def get_max_task_q(): return max(G, key=attrgetter('q'))

        while G or N:
            while N and get_min_task_r().r <= t:
                j_prime = N.index(get_min_task_r())
                help = N.pop(j_prime)
                G.append(help)
                if help.q > help2.q:
                    help2.p = t - help.r
                    t = help.r
                    if help2.p > 0:
                        G.append(help)
            if G:
                j_prime = G.index(get_max_task_q())
                help2 = G.pop(j_prime)
                t += help2.p
                Cmax = max(Cmax, t + help2.q)
            else:
                t = get_min_task_r().r

        return Cmax

    def _compute_a(self, pi, b, Cmax):  # sourcery skip: avoid-builtin-shadow
        a = 0
        s = 0
        s = sum(pi[i].p for i in range(b))
        while a < b and Cmax != pi[a].r + pi[b-1].q + s:
            s -= pi[a].p
            a += 1
        return a

    def _compute_c(self, pi, a, b):
        b -= 1
        for i in range(b - 1, a - 1, -1):
         
            if pi[i].q < pi[b].q:
                return i
        return None
        # return next((i for i in range(b - 2, a - 1, -1) if pi[i].q < pi[b].q), None)

    def _compute_rpq_prime(self, pi, b, c):
        r_prim = pi[c + 1].r
        p_prim = 0
        q_prim = pi[c + 1].q

        for i in range(c + 1, b + 1):
            if pi[i][1] < r_prim:
                r_prim = pi[i].r
            if pi[i][3] < q_prim:
                q_prim = pi[i].q
            p_prim += pi[i].p

        return r_prim, p_prim, q_prim

    def _carlier(self, tasks):
        # pi - permutacja zadań, C-max - górne oszacowanie, b - pozycja ostatniego w ścieżce krytycznej
        pi, Cmax, b = self._schrage(tasks)
        # pozycja pierwszego zadania w ścieżce krytycznej
        a = self._compute_a(pi, b, Cmax)
        # zadanie o jak najwyższej pozycji ale z mniejszym q_pi_j < q_pi_b
        c = self._compute_c(pi, a, b)
        if not c:  # jeśli nie znaleziono takiego to c_max jest roziwązaniem optymalnym
            return Cmax, pi

        # min r, max q, suma czasów wykonania zadań - w bloku (c+1, b)
        rprim, pprim, qprim = self._find_rpq_prim(pi, b, c)
        r_saved = pi[c].r  # zapisz r
        # modyfikacja terminu dostępności zadania c, wymusi to jego późniejszą realizację, za wszystkimi zadaniami w bloku(c+1, b)
        pi[c].r = max(pi[c].r, rprim + pprim)
        # sprawdzamy dolne ograniczenie schrage z podziałem  - dla wszystkich permutacji spełniających to wymaganie
        LB = self._schrage_pmtn(pi)

        if LB < Cmax:  # sprawdź czy rozwiązanie jest obiecujące
            pomCmax, pompi = self._carlier(pi)
            # wywołaj carliera jeszcze raz dla nowego problemu
            Cmax = min(Cmax, pomCmax)

        pi[c].r = r_saved  # odtwórz r

        q_saved = pi[c].q
        # wymuszenie aby zadanie c było wykonywane przed wszystkimi zadaniami w bloku (c+1, b)
        pi[c].q = max(pi[c].q, pprim + qprim)
        LB = self._schrage_pmtn(pi)  # sprawdź czy taki problem jest obiecujący

        if LB < Cmax:
            pomCmax, pompi = self._carlier(pi)
            Cmax = min(Cmax, pomCmax)

        pi[c].q = q_saved  # przywróc q

        return Cmax, pi


# tasks=[
#     [1, 28, 5, 7],
#     [2, 13, 6, 26],
#     [3, 11, 7, 24],
#     [4, 20, 4, 21],
#     [5, 30, 3, 8],
#     [6, 0, 6, 17],
#     [7, 30, 2, 0]
# ]

# tasks = [[1, 32, 69, 465],
#          [2, 657, 997, 818],
#          [3, 653, 66, 688],
#          [4, 704, 305, 623],
#          [5, 946, 221, 266],
#          [6, 357, 922, 821],
#          [7, 982, 882, 584],
#          [8, 542, 434, 856],
#          [9, 16, 970, 278],
#          [10, 354, 178, 241]
#          ]

tasks = [
    [1, 833, 65, 79],
    [2, 366, 98, 1706],
    [3, 863, 57, 1288],
    [4, 361, 15, 1444],
    [5, 319, 20, 1097],
    [6, 1234, 48, 969],
    [7, 877, 34, 284],
    [8, 798, 23, 285],
    [9, 1013, 57, 1294],
    [10, 1156, 23, 159],
    [11, 1119, 59, 483],
    [12, 676, 92, 1338],
    [13, 1216, 39, 1627],
    [14, 888, 10, 19],
    [15, 1498, 7, 76],
    [16, 1678, 99, 740],
    [17, 293, 70, 456],
    [18, 1448, 97, 595],
    [19, 1615, 73, 1344],
    [20, 1119, 66, 1135],
    [21, 1366, 68, 1441],
    [22, 1552, 80, 1454],
    [23, 1041, 46, 1462],
    [24, 1599, 3, 1847],
    [25, 146, 73, 678],
    [26, 967, 16, 1461],
    [27, 1632, 73, 1767],
    [28, 653, 56, 751],
    [29, 580, 75, 938],
    [30, 957, 99, 145],
    [31, 3, 33, 472],
    [32, 710, 13, 1589],
    [33, 1456, 21, 677],
    [34, 1308, 84, 846],
    [35, 775, 4, 555],
    [36, 1367, 38, 1614],
    [37, 1674, 88, 1450],
    [38, 268, 66, 778],
    [39, 910, 8, 1185],
    [40, 1229, 15, 1418],
    [41, 934, 38, 837],
    [42, 1799, 58, 161],
    [43, 1620, 18, 1561],
    [44, 188, 80, 1146],
    [45, 530, 28, 1372],
    [46, 28, 20, 571],
    [47, 1067, 30, 1451],
    [48, 1652, 24, 167],
    [49, 838, 63, 1260],
    [50, 274, 52, 1271]
]

if __name__ == '__main__':
    list_of_tasks = [Task(*task) for task in tasks]
    run_machine = Maszyna(list_of_tasks)

    Cmax, pi = run_machine.Cmax, run_machine.pi

    print(Cmax)
    print(*pi, sep='\n')
