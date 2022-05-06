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
        self._carlier()

    def _schrage(self):
        # końcowa kolejka wykonywania zadań na maszynie
        pi = []
        k = 0
        # zbiór gotowych zadań do realizacji
        G = []
        N = self._tasks
        get_min_task_r = lambda: min(N, key=attrgetter('r'))
        get_max_task_q = lambda: max(G, key=attrgetter('q'))
        t = get_min_task_r().r

        while G or N:
            while N and get_min_task_r().r <= t:
                j_prime = N.index(get_min_task_r())
                G.append(N.pop(j_prime))
            if G:
                j_prime = G.index(get_max_task_q())
                pi.append(G.pop(j_prime))
                t = t + pi[k].p
                k += 1
                print(t)
            else:
                t = get_min_task_r().r

        return pi

    def _schrage_pmtn(self):
        Cmax = 0
        G = []
        N = self._tasks
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
                t = t + help2.p
                Cmax = max(Cmax, t + help2.q)
            else:
                t = get_min_task_r().r

        return Cmax


        


    
    def _carlier(self):
        Cmax = self._schrage_pmtn()
        print(Cmax)
        # print(*pi, sep='\n')

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
    run_machine = Maszyna([Task(*task) for task in tasks])
