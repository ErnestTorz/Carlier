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
        get_min_task_r = lambda: min(N, key=attrgetter('r'))
        get_max_task_q = lambda: max(G, key=attrgetter('q'))
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

        get_min_task_r = lambda: min(N, key=attrgetter('r'))
        get_max_task_q = lambda: max(G, key=attrgetter('q'))

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
        return next((i for i in range(b - 1, a - 1, -1) if pi[i].q < pi[b].q), None)

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
        pi, Cmax, b = self._schrage(tasks) # pi - permutacja zadań, C-max - górne oszacowanie, b - pozycja ostatniego w ścieżce krytycznej
        a = self._compute_a(pi, b, Cmax) # pozycja pierwszego zadania w ścieżce krytycznej
        c = self._compute_c(pi, a, b) # zadanie o jak najwyższej pozycji ale z mniejszym q_pi_j < q_pi_b
        if not c: # jeśli nie znaleziono takiego to c_max jest roziwązaniem optymalnym
            return Cmax,pi 

        rprim, pprim, qprim = self._find_rpq_prim(pi, b, c) # min r, max q, suma czasów wykonania zadań - w bloku (c+1, b)
        r_saved = pi[c].r # zapisz r
        pi[c].r = max(pi[c].r, rprim + pprim) # modyfikacja terminu dostępności zadania c, wymusi to jego późniejszą realizację, za wszystkimi zadaniami w bloku(c+1, b)
        LB = self._schrage_pmtn(pi) # sprawdzamy dolne ograniczenie schrage z podziałem  - dla wszystkich permutacji spełniających to wymaganie

        if LB < Cmax: # sprawdź czy rozwiązanie jest obiecujące
            pomCmax, pompi = self._carlier(pi)
            Cmax = min(Cmax, pomCmax) # wywołaj carliera jeszcze raz dla nowego problemu

        pi[c].r = r_saved # odtwórz r

        q_saved = pi[c].q
        pi[c].q = max(pi[c].q, pprim + qprim) # wymuszenie aby zadanie c było wykonywane przed wszystkimi zadaniami w bloku (c+1, b)
        LB = self._schrage_pmtn(pi) # sprawdź czy taki problem jest obiecujący

        if LB < Cmax:
            pomCmax, pompi = self._carlier(pi)
            Cmax = min(Cmax, pomCmax)

        pi[c].q = q_saved # przywróc q

        return Cmax,pi 
            


tasks=[
    [1, 28, 5, 7], 
    [2, 13, 6, 26], 
    [3, 11, 7, 24], 
    [4, 20, 4, 21], 
    [5, 30, 3, 8], 
    [6, 0, 6, 17], 
    [7, 30, 2, 0]
]   


if __name__ == '__main__':
    list_of_tasks = [Task(*task) for task in tasks]
    run_machine = Maszyna(list_of_tasks)

    Cmax, pi = run_machine.Cmax, run_machine.pi

    print(Cmax)
    print(*pi, sep='\n')
