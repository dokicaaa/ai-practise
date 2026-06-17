# Genetic Algorithms — Problems Overview

---

## Table of Contents

1. [MuseumCameras](#1-museumcameras)
2. [MaxCrops](#2-maxcrops)
3. [CityPark](#3-citypark)
4. [ConstructSites](#4-constructsites)
5. [ProductionLine](#5-productionline)
6. [FactoryMaintenance](#6-factorymaintenance)
7. [ServerLoadBalancer](#7-serverloadbalancer)
8. [FactoryProductionPlan](#8-factoryproductionplan)
9. [ParamOptimisation](#9-paramoptimisation)
10. [SmartHomeScheduler](#10-smarthomescheduler)
11. [EVChargingSchedule](#11-evchargingschedule)
12. [CookingSchedule](#12-cookingschedule)

---

## 1. MuseumCameras

Целта на оваа вежба е оптимизација на поставување безбедносни камери во музеј со користење на Генетски алгоритми.

Музејот се состои од повеќе изложбени простории поврзани меѓусебно. Секоја просторија содржи артефакти и експонати со различни проценети вредности. Управата на музејот сака да постави ограничен број безбедносни камери со цел да ја максимизира вкупната заштитена вредност на музејот.

Museum

Во почетниот код, променливата rooms е дадена со информации за имињата на просториите, листа од соседни простории и паричната вредност што ја претставува важноста на експонатите во просторијата.

Во прикажаната слика, просториите означени со црвен текст се сметаат за големи простории, додека просториите означени со црн текст се сметаат за мали простории.

Камера поставена во просторија ја зголемува безбедносната покриеност на таа просторија и делумно придонесува кон покриеноста на соседните простории.

Мала просторија станува целосно покриена (100% покриеност) доколку во неа е поставена барем една камера. Дополнителни камери поставени во истата мала просторија не ја зголемуваат дополнително покриеноста и се бескорисни/нефункционални.

Големите простории бараат дополнителен надзор. Една камера обезбедува 60% покриеност, додека 2 камери обезбедуваат 100% покриеност. Дополнителни камери по втората не ја зголемуваат понатаму покриеноста на просторијата и се нефункционални.

Доколку просторијата содржи камери, тие делумно ја зголемуваат и покриеноста на соседните простории. Секоја камера поставена во просторија придонесува со +10% покриеност на секоја соседна просторија. Вредностите за покриеност никогаш не смеат да надминат 100%.

Заштитената вредност на една просторија е пропорционална на процентот на нејзината покриеност. Вкупната заштитена вредност на музејот е еднаква на збирот од заштитените вредности на сите простории.

На пример, просторија со вредност 200 и покриеност 100% придонесува со 200 заштитени единици, додека просторија со вредност 200 и покриеност 60% придонесува со 200 * 60% = 120 заштитени единици.

Од стандарден влез се чита фиксен број K на безбедносни камери.

Со користење на Генетски алгоритам имплементиран со библиотеката pygad, определете како да се распределат камерите низ музејот со цел да се максимизира вкупната заштитена вредност.

Испечатете ја најдобрата проценета вкупна заштитена вредност.

Забелешка: Локално, направете го следниот повик `ga.best_solution(ga.last_generation_fitness)` за да го добиете оптималното решение пронајдено во текот на сите генерации. Дополнително, можни се неконзистентности на типот (листа/numpy низа) на променливата chromosome/solution.

### Starter code

```python
import pygad
import random
random.seed(0)

rooms = {
    1: {'name': 'Modern & Contemporary Art', 'adjacent': [2, 7], 'value': 110},
    2: {'name': 'European History', 'adjacent': [1, 3, 4, 5, 7], 'value': 130},
    3: {'name': 'Seasonal Exhibitions', 'adjacent': [2], 'value': 100},
    4: {'name': 'Prehistory', 'adjacent': [2, 6, 10], 'value': 140},
    5: {'name': 'Medieval Times', 'adjacent': [2, 6, 9], 'value': 120},
    6: {'name': 'Arms and Armor', 'adjacent': [4, 5], 'value': 150},
    7: {'name': 'Arts of Africa, Oceania and the Americas', 'adjacent': [1, 2, 8], 'value': 90},
    8: {'name': 'Greek and Roman History', 'adjacent': [7, 9], 'value': 180},
    9: {'name': 'The Great Hall', 'adjacent': [5, 8, 10], 'value': 30},
    10: {'name': 'Egyptian History', 'adjacent': [4, 9], 'value': 200}
}

K = int(input())

large_rooms = [2, 8, 9, 10]
def fitness_func(ga, solution, idx):
    solution = [int(x) for x in solution]
        # Death penalty e poivekoje od pokrienst od 100 procenti i ako ima povekje od K kameri

    # Kreirame dictariony od vid {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    counts = {i: 0 for i in range(1, 11)}
    for room in solution:
        counts[int(room)] += 1

    total_protected_value = 0.0
    for room_id, info in rooms.items():
        cams_in_room = counts[room_id]

        base_cov = 0.0
        if room_id in large_rooms:
            if cams_in_room == 1:
                base_cov = 0.6
            elif cams_in_room >= 2:
                base_cov = 1.0
        else:
            if cams_in_room >= 1:
                base_cov = 1.0

        ajd_cov = 0.0
        for adj_id in info['adjacent']:
            cams_in_adj = counts[adj_id]
            ajd_cov += (cams_in_adj * 0.10)

        total_cov = min(1.0, base_cov + ajd_cov)

        total_protected_value += info['value'] * total_cov

    return total_protected_value

params = {
    'num_generations': 1000,
    'sol_per_pop': 100,
    'num_parents_mating': 40,

    # Genot - list so golemina na 10, za sekoja ima 0, 1, 2 kameri
    # brojt na kameri vo ednas oba mozhe da e od 0 do K
    'num_genes': K,
    'gene_space': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'fitness_func': fitness_func,

    'mutation_num_genes': 1,
}

if K > 0:
    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()
    best_fitness = fitness_func(ga, best_solution, 0)

    print(f'Optimal protected value: {best_fitness}M$')
else:
    print('Optimal protected value: 0.0M$')
```

### Test cases

| Input | Result |
|-------|--------|
| `3` | `Optimal protected value: 471.0M$` |

```
- 1 camera in Prehistory
- 1 camera in Medieval Times
- 1 camera in Arts of Africa, Oceania and the Americas
```

---

## 2. MaxCrops

Фармер треба да постави прскалки на својата нива за да ги наводнува посевите.

Нивата е претставена како мрежа со димензии M × N. Нивата се состои од полиња со посеви кои може да се наводнуваат, и полиња кои се блокирани/неупотребливи. Бројот на неупотребливи полиња, како и нивните позиции, се дадени во влезот на самиот крај.

Фармерот располага со K прскалки. Може да се постават произволен број прскалки до максимум K, а прскалките може да се постават на било кое поле. Доколку прскалка се постави на поле со посеви, тие посеви се уништуваат. Прскалката ги наводнува сите блиски полиња во форма на ромб (♦), односно ги наводнува сите 8 соседни полиња, како и 4-те полиња кои се на растојание 2 лево, горе, десно или долу од прскалката.

Со користење на генетски алгоритам, максимизирајте го бројот на наводнети посеви. Доколку повеќе решенија наводнуваат ист број посеви, треба да се избере решението кое користи помал број прскалки.

Испечатете го бројот на наводнети посеви, како и бројот на искористени прскалки и нивните позиции.

### Starter code

```python
import pygad


def read_input():
    M, N = map(int, input().split())
    K = int(input())
    B = int(input())

    unusable = set()
    for _ in range(B):
        r, c = map(int, input().split())
        unusable.add((r, c))

    return M, N, K, unusable


def fitness_func(ga_instance, solution, solution_idx):
    ...  # TODO: implement fitness function


if __name__ == "__main__":
    M, N, K, unusable = read_input()

    params = {
        'num_generations': 100,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': ...,  # TODO: fill empty params
        'gene_space': ...,
        'fitness_func': fitness_func,
        'mutation_num_genes': 1
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()

    ...  # TODO: Print required data
```

### Test cases

```
5 5
2
3
1 1
2 2
4 0
```

```
15 20
8
25
0 3
0 7
1 5
1 12
2 2
2 18
3 9
4 4
4 15
5 1
5 10
6 6
6 17
7 8
7 13
8 0
8 19
9 5
10 11
11 3
11 16
12 7
13 14
14 2
14 18
```

---

## 3. CityPark

Градот сака да постави клупи во парк со димензии M × N. Паркот е претставен како мрежа од полиња. Секое поле може да содржи клупа или да биде блокирано (езерце, дрво, цветна градина). Бројот на блокирани полиња, како и нивните позиции, се дадени во влезот. Градот располага со K клупи. Секоја клупа опслужува свое поле и сите полиња на Менхетен растојание помало или еднакво на D од неа. Менхетен растојание помеѓу две полиња (r1, c1) и (r2, c2) се дефинира како \|r1 - r2\| + \|c1 - c2\|. Клупите не смеат да се поставуваат на блокирани полиња. Доколку клупа се постави на блокирано поле, таа е неважечка и не опслужува ништо. Полињата кои се блокирани не можат да бидат опслужени (дури и ако се во опсег на клупа). Не е задолжително да се искористат сите K клупи (може да се постават помалку). Доколку две или повеќе клупи го опслужуваат исто поле, тоа поле се брои само еднаш.

Со користење на Генетски алгоритам имплементиран со библиотеката pygad, максимизирајте го бројот на уникатни опслужени полиња. Доколку повеќе решенија опслужуваат ист број полиња, треба да се преферира решението кое користи помалку клупи. За таа цел, fitness функцијата треба да содржи мала казна за секоја искористена клупа.

Од стандарден влез се чита: M, N, K, D – димензии, број на клупи и радиус; B – број на блокирани полиња; B линии, секоја со два цели броја – редица и колона на блокирано поле.

Испечатете го бројот на опслужени полиња, бројот на искористени клупи, и за секоја клупа нејзината позиција.

### Starter code

```python
import pygad


def read_input():
    M, N, K, D = map(int, input().split())
    B = int(input())
    blocked = set()
    for _ in range(B):
        r, c = map(int, input().split())
        blocked.add((r, c))
    return M, N, K, D, blocked


def fitness_func(ga_instance, solution, solution_idx):
    ...  # TODO: implement fitness function


if __name__ == "__main__":
    M, N, K, D, blocked = read_input()

    gene_space = [-1]
    for r in range(M):
        for c in range(N):
            if (r, c) not in blocked:
                gene_space.append(r * N + c)

    params = {
        'num_generations': 150,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': ...,  # TODO: fill empty params
        'gene_space': gene_space,
        'fitness_func': fitness_func,
        'mutation_num_genes': 1
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()

    ...  # TODO: Print required data
```

### Test cases

**Тест 1:**

Влез:
```
4 4 2 1
2
0 0
3 3
```

Очекуван излез:
```
9
2
Bench at (1, 2)
Bench at (3, 1)
```

**Тест 2:**

Влез:
```
5 5 3 1
3
1 1
2 2
3 3
```

Очекуван излез:
```
12
3
Bench at (0, 2)
Bench at (2, 4)
Bench at (4, 2)
```

---

## 4. ConstructSites

Градежна компанија треба да организира N градилишта со K тимови. Секое градилиште има одредена тежина (complexity/difficulty) која го претставува времето потребно за работа на тоа градилиште. Тимовите се еднакво способни, но доколку две соседни градилишта се доделени на различни тимови, потребна е дополнителна координација (трошок за превоз на опрема и материјали помеѓу градилиштата). Секој тим мора да добие најмалку 2 градилишта. Вкупното време за еден тим е еднакво на збирот од тежините на сите градилишта доделени на тој тим. Доколку две градилишта се соседни (постои врска меѓу нив) и се доделени на различни тимови, трошокот за координација е еднаков на збирот од нивните тежини.

Целта е да се минимизира вкупниот трошок, кој се пресметува како:
```
вкупен_трошок = најголемо_време_на_тим + збир_на_координациски_трошоци
```

Со користење на Генетски алгоритам имплементиран со библиотеката pygad, определете како да се распределат градилиштата на тимовите со цел да се минимизира вкупниот трошок.

Од стандарден влез се чита: N, K – број на градилишта и број на тимови; N линии, секоја со еден цел број – тежина на градилиштето; M – број на соседства (врски); M линии, секоја со два цели броја – индекс на две градилишта кои се соседни.

Испечатете го минималниот вкупен трошок, како и за секое градилиште на кој тим е доделено.

### Starter code

```python
import pygad
import numpy as np


def read_input():
    N, K = map(int, input().split())
    difficulties = [int(input()) for _ in range(N)]
    M = int(input())
    adjacencies = [tuple(map(int, input().split())) for _ in range(M)]
    return N, K, difficulties, adjacencies


def fitness_func(ga_instance, solution, solution_idx):
    SOLUTION + [2, 3, 5, 1, 2, 3] - kade indeksot na sekoj item vo nizata ni se construction ID dodeka vrednosta e teamID


if __name__ == "__main__":
    N, K, difficulties, adjacencies = read_input()

    params = {
        'num_generations': 200,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': N,
        'gene_space': K,
        'fitness_func': fitness_func,
        'mutation_num_genes': 1
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()

    ...  # TODO: Print required data
```

### Test cases

**Тест 1:**

Влез:
```
4 2
5
3
8
2
2
0 1
2 3
```

Очекуван излез:
```
10
Site 0 -> Team 0
Site 1 -> Team 0
Site 2 -> Team 1
Site 3 -> Team 1
```

**Тест 2:**

Влез:
```
6 2
10
7
9
12
5
11
4
0 1
1 4
2 3
3 5
```

Очекуван излез:
```
32
Site 0 -> Team 0
Site 1 -> Team 0
Site 2 -> Team 1
Site 3 -> Team 1
Site 4 -> Team 0
Site 5 -> Team 1
```

---

## 5. ProductionLine

Фабрика треба да распореди N производствени задачи на K паралелни машини. Секоја задача има време на обработка (processing time). Секоја машина има брзина (speed) – машината ја обработува задачата за време = време_на_задача / брзина_на_машина. Машините обработуваат задачи последователно (една по една). Сите задачи мора да бидат доделени на машините. Целта е да се минимизира вкупното време за завршување на сите задачи (makespan), кое се дефинира како најголемо вкупно време на работа помеѓу сите машини.

Со користење на Генетски алгоритам имплементиран со библиотеката pygad, определете како да се распределат задачите на машините со цел да се минимизира makespan-от.

Од стандарден влез се чита: N, K – број на задачи и број на машини; N линии, секоја со еден цел број – време на обработка на задачата; K линии, секоја со еден реален број – брзина на машината.

Испечатете го минималниот makespan (заокружен на 1 децимала), како и за секоја машина листа од индексите на задачите доделени на неа.

### Starter code

```python
import pygad
import numpy as np


def read_input():
    N, K = map(int, input().split())
    times = [int(input()) for _ in range(N)]
    speeds = [float(input()) for _ in range(K)]
    return N, K, times, speeds


def fitness_func(ga_instance, solution, solution_idx):
    solution - [2, 3, 1, 4] index ke ni e task_id a value ke ni e machine_id
    makespan =
    return -makespan


if __name__ == "__main__":
    N, K, times, speeds = read_input()

    params = {
        'num_generations': 200,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': ...,  # TODO: fill empty params
        'gene_space': ...,
        'fitness_func': fitness_func,
        'mutation_num_genes': 1
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()

    ...  # TODO: Print required data
```

### Test cases

**Тест 1:**

Влез:
```
4 2
4
6
5
3
1.0
2.0
```

Очекуван излез:
```
6.0
Machine 0: 1
Machine 1: 0 2 3
```

**Тест 2:**

Влез:
```
6 3
8
3
10
6
5
7
0.8
1.2
1.0
```

Очекуван излез:
```
13.3
Machine 0: 2
Machine 1: 0 1 4
Machine 2: 3 5
```

---

## 6. FactoryMaintenance

Фабрика треба да организира задачи за одржување на машините со користење на тимови за поправка.

Фабриката содржи N машини. Секоја машина има време на поправка ti и тип на машина ci. Информациите за сите машини се дадени во влезот.

Машините се поделени во тимови од точно 4 машини. Секоја машина мора да припаѓа на точно еден тим.

Вообичаено, времетраењето на смената на еден тим е еднакво на максималното време на поправка меѓу 4-те доделени машини.

Сепак, пред почетокот на одржувањето, менаџментот избира еден префериран тип на машина P. Ако сите 4 машини доделени на еден тим се од преферираниот тип P, техничарите можат поефикасно да ги користат алатките и калибрациите, па времетраењето на тој тим станува минималното време на поправка меѓу 4-те машини. Сите останати тимови сè уште го користат нормалното правило (максимално време).

Со користење на генетски алгоритам, определете како да се поделат машините во тимови од 4 и кој тип на машина треба да биде избран како префериран, така што вкупното време за одржување на сите тимови ќе биде минимално.

Испечатете го минималното вкупно време за одржување, избраниот префериран тип на машина, како и тимовите и машините доделени во секој тим.

### Starter code

```python
import pygad
import numpy as np


def fitness_func(ga_instance, solution, solution_idx):
    ...


if __name__ == '__main__':
    ... # TODO: Read input

params = {
    'num_generations': 300,
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': ...,  # TODO: fill empty params
    'gene_space': ...,
    'fitness_func': fitness_func,
    'mutation_num_genes': 1
}

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()

    ...  # TODO: Print required data
```

### Test cases

```
12
10 A
12 A
8 A
9 A
15 B
6 B
11 B
7 B
14 C
13 C
5 C
9 C
```

```
24
10 A
12 A
8 A
9 A
15 A
7 A
11 A
13 A
20 B
18 B
17 B
16 B
21 B
19 B
14 B
15 B
5 C
6 C
7 C
8 C
9 D
10 D
11 D
12 D
```

---

## 7. ServerLoadBalancer

Целта на оваа вежба е оптимизација на оптоварување на облак сервери со користење на Генетски алгоритми.

Даден е клауд провајдер со S сервери, секој со различен капацитет (CPU јадра, RAM меморија, Bandwidth) и фиксна цена на работа по час. Провајдерот треба да прифати N апликации, каде секоја апликација бара одредени ресурси (CPU, RAM, BW) и носи профит. Секоја апликација мора да биде доделена на точно еден сервер.

Ако серверот е недоволно искористен (сите ресурси под капацитет), апликациите работат со полно оптоварување и носат целосен профит. Ако серверот е преоптоварен во било која димензија (CPU, RAM или BW), сите апликации на тој сервер се успоруваат пропорционално – соодносот на услужување (throughput) е еднаков на 1 / max(load_ratio), каде load_ratio = max(CPU_used/CPU_cap, RAM_used/RAM_cap, BW_used/BW_cap). Профитот од секој сервер се пресметува како збир на профитите на апликациите на него помножен со соодносот на услужување.

Серверот плаќа цена на работа само доколку има барем една апликација доделена на него. Ако серверот е неискористен, неговата цена е 0.

Вкупната добивка = збир(профит_на_сервер * throughput_ratio) - збир(цена_на_активни_сервери)

На пример, сервер со CPU=8, RAM=16, BW=10 и цена=5 на кој се доделени апликации со вкупно CPU=10, RAM=8, BW=6: max_ratio = max(10/8, 8/16, 6/10) = max(1.25, 0.5, 0.6) = 1.25. Throughput = 1/1.25 = 0.8. Ако апликациите носат профит 20, тогаш придонес = 20 * 0.8 - 5 = 11.

Од стандарден влез се чита N – број на апликации, а потоа N линии со по 4 броја: CPU, RAM, BW, profit за секоја апликација.

Со користење на Генетски алгоритам имплементиран со библиотеката pygad, определете како да се распределат апликациите на серверите со цел да се максимизира вкупната добивка.

Испечатете ја максималната вкупна добивка (заокружена на 2 децимали).

Забелешка: За да го добиете најдоброто решение во текот на сите генерации, користете `ga.best_solution(ga.last_generation_fitness)`.

### Starter code

```python
import pygad
import random
random.seed(0)

servers = {
    0: {'cpu': 8, 'ram': 16, 'bw': 10, 'cost': 5},
    1: {'cpu': 12, 'ram': 8, 'bw': 5, 'cost': 7},
    2: {'cpu': 6, 'ram': 12, 'bw': 8, 'cost': 4}
}

N = int(input())
apps = []
for _ in range(N):
    cpu, ram, bw, profit = map(int, input().split())
    apps.append({'cpu': cpu, 'ram': ram, 'bw': bw, 'profit': profit})

def fitness_func(ga, solution, idx):
    ...  # TODO: implement fitness function

params = {
    'num_generations': 300,
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': ...,  # TODO: fill empty params
    'gene_space': ...,
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,
}

ga = pygad.GA(**params)
ga.run()

best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
best_fitness = fitness_func(ga, best_solution, 0)

print(f'{best_fitness:.2f}')
```

### Test cases

| Input | Result |
|-------|--------|
| `2` `4 2 3 10` `2 8 1 6` | `7.00` |

```
App1 (CPU=4,RAM=2,BW=3,profit=10) -> Server 0
App2 (CPU=2,RAM=8,BW=1,profit=6) -> Server 1
```

| Input | Result |
|-------|--------|
| `3` `4 2 3 10` `3 6 2 8` `5 4 4 12` | `21.00` |

```
App1,App2 -> Server 0
App3 -> Server 2
```

| Input | Result |
|-------|--------|
| `5` `4 2 3 10` `3 6 2 8` `5 4 4 12` `2 8 1 6` `4 4 3 9` | `29.00` |

```
App1,App2 -> Server 0
App3 -> Server 1
App4,App5 -> Server 2
```

---

## 8. FactoryProductionPlan

Целта на оваа вежба е оптимизација на производствен план со користење на Генетски алгоритми.

Фабрика произведува N производи. Секој производ бара време на две машини (A и B), материјал, работни часови и носи профит по единица. Доколку производот се произведува (количина > 0), се плаќа фиксен трошок за подесување (setup cost). Фабриката има ограничени ресурси неделно: машина A (макс часови), машина B (макс часови), материјали (буџет), складишен простор (единици) и работни часови. Доколку количината на еден производ го надмине прагот за попуст (bulk_threshold), профитот по единица за тој производ се зголемува за 25%.

Генот претставува количина на производ (0 до 15). Хромозомот има N гени, по еден за секој производ. Ова е прв пат да користите целобројно количинско кодирање (integer quantity encoding) наместо селекција или доделување – вредноста на генот директно кажува КОЛКУ единици од тој производ да се произведат.

Вкупниот профит се пресметува:
```
профит = збир(количина * (profit_per_unit * (1.25 ако количина >= bulk_threshold, инаку 1)) - setup_cost(ако > 0))
```

Од стандарден влез се чита: N – број на производи; N линии со 6 броја: profit_per_unit, machine_A, machine_B, material, setup_cost, labor; 5 линии со ресурсни ограничувања: mA_max, mB_max, materials_max, storage_max, labor_max; еден број – bulk_threshold.

Со користење на Генетски алгоритам имплементиран со библиотеката pygad, определете ги количините на секој производ со цел да се максимизира вкупниот профит без да се надминат ресурсните ограничувања. Решенијата кои ги надминуваат ограничувањата треба да се казнат.

Испечатете ја максималната вкупна добивка (заокружена на 2 децимали).

Забелешка: За да го добиете најдоброто решение во текот на сите генерации, користете `ga.best_solution(ga.last_generation_fitness)`. Возможно е да има неконзистентност на типот (list/numpy низа) на променливата chromosome/solution.

### Starter code

```python
import pygad
import random
random.seed(0)


def read_input():
    N = int(input())
    products = []
    for _ in range(N):
        profit, mA, mB, mat, setup, labor = map(int, input().split())
        products.append({'profit': profit, 'mA': mA, 'mB': mB, 'mat': mat, 'setup': setup, 'labor': labor})
    mA_max, mB_max, materials_max, storage_max, labor_max = map(int, input().split())
    bulk_threshold = int(input())
    return N, products, mA_max, mB_max, materials_max, storage_max, labor_max, bulk_threshold


def fitness_func(ga, solution, idx):
    ...  # TODO: implement fitness function


if __name__ == "__main__":
    N, products, mA_max, mB_max, materials_max, storage_max, labor_max, bulk_threshold = read_input()

    params = {
        'num_generations': 300,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': ...,  # TODO: fill empty params
        'gene_space': ...,
        'fitness_func': fitness_func,
        'mutation_num_genes': 1,
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
    best_fitness = fitness_func(ga, best_solution, 0)

    print(f'{best_fitness:.2f}')
```

### Test cases

| Input | Result |
|-------|--------|
| `2` `10 2 1 3 4 2` `20 3 2 5 7 3` `30 20 50 15 18` `4` | `119.00` |

```
Product 0 (qty=3, profit=30, no bulk)
Product 1 (qty=4, bulk, profit=25/unit)
```

| Input | Result |
|-------|--------|
| `4` `12 2 1 3 5 2` `18 1 3 5 8 3` `10 3 2 2 4 1` `25 4 2 7 10 4` `45 35 120 25 40` `8` | `259.00` |

```
Product 0 (qty=8, bulk, profit=15/unit)
Product 1 (qty=7, no bulk, profit=18/unit)
Product 2 (qty=3, no bulk, profit=10/unit)
```

| Input | Result |
|-------|--------|
| `3` `8 1 1 2 3 1` `15 2 2 4 6 2` `12 3 1 3 5 2` `35 25 80 20 28` `6` | `229.00` |

```
Product 1 (qty=8, bulk, profit=18.75/unit)
Product 2 (qty=6, bulk, profit=15.00/unit)
```

---

## 9. ParamOptimisation

Во оваа задача, треба да користите Генетски Алгоритам имплементиран со библиотеката pygad со цел да ги оптимизирате хиперпараметрите на DecisionTreeClassifier.

Податочното множество дадено во почетниот код е претставено како листа од листи, каде што класната ознака се наоѓа на последната позиција од секој ред. Податочното множество треба да се подели на тренинг и тест множество така што првите 75% од податоците ќе припаѓаат во тренинг множеството, а останатите во тест множеството.

Генетскиот Алгоритам треба да ги оптимизира следните хиперпараметри со нивните соодветни кандидат вредности:

- criterion: 'gini', 'entropy'
- max_depth: 5, 10, 15, 20, 25
- min_samples_split: 2, 3, 4, 5, 10
- max_leaf_nodes: 5, 10, 15, 20, 25

Fitness функцијата треба првенствено да ја максимизира точноста на класификација врз тест множеството. Сепак, кога два модели постигнуваат слична точност, треба да се преферираат помали дрва. Поради тоа, fitness функцијата треба благо да ги казнува поголемите вредности на max_depth и max_leaf_nodes.

Пополнете ги деловите што недостасуваат во почетниот код. Откако Генетскиот Алгоритам ќе заврши, земете го најдоброто решение и испечатете ги најдобрите параметри за decision tree моделот.

Потоа, креирајте го најдобриот decision tree модел, тренирајте го и испечатете ја неговата финална точност врз тест множеството.

### Starter code

```python
import pygad
from sklearn.tree import DecisionTreeClassifier


dataset = [
    [2, 3, 1, 7, 0],
    [5, 6, 4, 3, 1],
    [1, 1, 2, 8, 1],
    [7, 8, 6, 4, 1],
    [3, 2, 1, 9, 0],
    [8, 7, 5, 2, 1],
    [4, 5, 2, 6, 1],
    [1, 3, 1, 9, 0],
    [9, 8, 7, 2, 1],
    [2, 2, 3, 8, 0]
]

... # TODO: Split dataset here


def fitness_func(ga_instance, solution, solution_idx):
    ...  # TODO: Define fitness function


ga_instance = pygad.GA(
    num_generations=40,
    sol_per_pop=50,
    num_parents_mating=25,
    fitness_func=fitness_func,
    num_genes=...,  # TODO: Define missing params
    gene_space=...,
    mutation_num_genes=1
)

ga_instance.run()
best_solution, _, _ = ga_instance.best_solution()

...  # TODO: Print best params and accuracy of best model
```

---

## 10. SmartHomeScheduler

Целта на оваа вежба е оптимизација на закажување на домашни уреди со користење на Генетски алгоритми.

Паметна куќа има N уреди кои треба да се закажат за работа во текот на денот (24 часа). Секој уред има потрошувачка (Watts), времетраење на работа (часови), и временски прозорец во кој може да работи (earliest_start, latest_end). Куќата има сопствен соларен систем кој произведува струја во текот на денот со врв напладне. Кога соларната продукција не е доволна, куќата купува струја од мрежата по динамични цени – поскапа во шпиц (8-11, 17-20 часот, $0.30/kWh) и поевтина во останато време ($0.15/kWh). Мрежата има лимит од 5000W во секој час.

Генот претставува почетен час на работа на уредот (0-23). Хромозомот има N гени, по еден за секој уред. Ова е прв пат да користите временско закажување (temporal scheduling) – вредноста на генот кажува КОГА да стартува уредот, а фитнесот симулира цел ден.

Соларна продукција по часови (Watts):
```
solar = [0, 0, 0, 0, 0, 0, 0, 500, 1200, 2000, 2700, 3000, 3000, 2700, 2000, 1200, 500, 0, 0, 0, 0, 0, 0, 0]
```

Цена на струја по часови ($/kWh):
```
peak_hours = [8, 9, 10, 11, 17, 18, 19, 20]
```

Вкупниот трошок се пресметува: за секој час, net = max(0, вкупна_потрошувачка - соларна_продукција), трошок += net / 1000 * цена[час].

Од стандарден влез се чита N – број на уреди, а потоа N линии со 5 броја: Watts, runtime_hours, earliest_start, latest_end, priority.

Со користење на Генетски алгоритам имплементиран со библиотеката pygad, определете ги почетните часови на секој уред со цел да се минимизира вкупниот трошок без да се прекршат временските прозорци и лимитот на мрежата. Решенијата кои ги прекршуваат ограничувањата треба да се казнат.

Испечатете го минималниот вкупен трошок (заокружен на 2 децимали).

Забелешка: За да го добиете најдоброто решение во текот на сите генерации, користете `ga.best_solution(ga.last_generation_fitness)`. Возможно е да има неконзистентност на типот (list/numpy низа) на променливата chromosome/solution.

### Starter code

```python
import pygad
import random
random.seed(0)

solar = [0, 0, 0, 0, 0, 0, 0, 500, 1200, 2000, 2700, 3000, 3000, 2700, 2000, 1200, 500, 0, 0, 0, 0, 0, 0, 0]
price = [0.15] * 24
for h in [8, 9, 10, 11, 17, 18, 19, 20]:
    price[h] = 0.30
GRID_LIMIT = 5000

N = int(input())
appliances = []
for _ in range(N):
    watts, runtime, earliest, latest, priority = map(int, input().split())
    appliances.append({'watts': watts, 'runtime': runtime, 'earliest': earliest, 'latest': latest})


def fitness_func(ga, solution, idx):
    ...  # TODO: implement fitness function


params = {
    'num_generations': 200,
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': ...,  # TODO: fill empty params
    'gene_space': ...,
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,
}

ga = pygad.GA(**params)
ga.run()

best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
best_fitness = fitness_func(ga, best_solution, 0)

print(f'{-best_fitness:.2f}')
```

### Test cases

| Input | Result |
|-------|--------|
| `3` `2000 2 8 16 0` `1500 3 9 14 0` `3000 1 18 22 0` | `0.45` |

```
A0(2000W,2h)@12, A1(1500W,3h)@9, A2(3000W,1h)@21
```

| Input | Result |
|-------|--------|
| `2` `2000 1 10 14 0` `3000 1 20 22 0` | `0.45` |

```
A0(2000W,1h)@10, A1(3000W,1h)@21
```

| Input | Result |
|-------|--------|
| `3` `1500 2 9 11 0` `2000 3 12 17 0` `3000 1 21 22 0` | `0.45` |

```
A0(1500W,2h)@9, A1(2000W,3h)@12, A2(3000W,1h)@21
```

---

## 11. EVChargingSchedule

Целта на оваа вежба е оптимизација на закажување на полнење на електрични возила (EV) со користење на Генетски алгоритми.

Полначка станица има N електрични возила кои треба да се закажат за полнење во текот на денот (24 часа). Секое возило има потреба од одредена количина на енергија (kWh), час на пристигнување и час на заминување (најдоцна кога возилото мора да биде готово). Станицата има 10kW полначи, па потребниот број на часови за полнење на секое возило е ceil(kWh / 10).

Станицата има сопствен соларен систем кој произведува струја во текот на денот (kW). Кога соларната продукција не е доволна, станицата купува струја од мрежата по динамични цени – поскапа во шпиц (8-11, 17-20 часот, $0.30/kWh) и поевтина во останато време ($0.15/kWh). Врската со мрежата е ограничена на 40kW во секој час.

Генот претставува почетен час на полнење на возилото (0-23). Хромозомот има N гени, по еден за секое возило.

Вкупниот трошок се пресметува: за секој час, net = max(0, вкупна_моќност - соларна_продукција), трошок += net * цена[час].

Од стандарден влез се чита N – број на возила, а потоа N линии со 3 броја: kWh, arrival_hour, departure_hour.

Со користење на Генетски алгоритам имплементиран со библиотеката pygad, определете ги почетните часови на полнење на секое возило со цел да се минимизира вкупниот трошок без да се прекршат временските прозорци и лимитот на мрежата. Решенијата кои ги прекршуваат ограничувањата треба да се казнат.

Испечатете го минималниот вкупен трошок (заокружен на 2 децимали).

Забелешка: За да го добиете најдоброто решение во текот на сите генерации, користете `ga.best_solution(ga.last_generation_fitness)`. Возможно е да има неконзистентност на типот (list/numpy низа) на променливата chromosome/solution.

### Starter code

```python
import pygad
import random
import math
random.seed(0)

charger_power = 10
grid_capacity = 40
solar = [0, 0, 0, 0, 0, 0, 0, 3, 7, 12, 15, 16, 16, 15, 12, 7, 3, 0, 0, 0, 0, 0, 0, 0]
price = [0.15] * 24
for h in [8, 9, 10, 11, 17, 18, 19, 20]:
    price[h] = 0.30

N = int(input())
kwh = []
arrival_hour = []
departure_hour = []
for _ in range(N):
    k, a, d = map(int, input().split())
    kwh.append(k)
    arrival_hour.append(a)
    departure_hour.append(d)

hours_needed = [math.ceil(k / charger_power) for k in kwh]


def fitness_func(ga, solution, idx):
    ...  # TODO: implement fitness function


params = {
    'num_generations': 200,
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': ...,  # TODO: fill empty params
    'gene_space': ...,
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,
}

ga = pygad.GA(**params)
ga.run()

best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
best_fitness = fitness_func(ga, best_solution, 0)

print(f'{-best_fitness:.2f}')
```

### Test cases

| Input | Result |
|-------|--------|
| `3` `10 8 17` `10 9 14` `10 20 22` | `1.50` |

```
EV0@13, EV1@12, EV2@21
```

| Input | Result |
|-------|--------|
| `3` `20 9 16` `20 9 16` `10 20 22` | `1.95` |

```
EV0@12, EV1@14, EV2@21
```

| Input | Result |
|-------|--------|
| `4` `10 8 12` `10 8 12` `10 8 12` `10 20 22` | `2.40` |

```
EV0@9, EV1@10, EV2@11, EV3@21
```

---

## 12. CookingSchedule

Целта на оваа вежба е оптимизација на распоред на готвење во професионална кујна со користење на Генетски алгоритми.

Кујна има N јадења кои треба да се подготват. Секое јадење минува низ две фази: подготовка (prep) која бара готвач, и печење/готвење (cook) кое ја користи рерната. Кујната има 1 готвач и 1 рерна – готвачот може да подготвува само едно јадење истовремено, а рерната може да пече само едно јадење истовремено. Готвачот е слободен додека јадењето се пече во рерна и може да подготвува друго јадење. Секое јадење има идеален момент на сервирање (deadline - offset) – доколку заврши порано или подоцна, квалитетот опаѓа линеарно за 20% по час отстапување. Ако отстапувањето е 5 или повеќе часови, квалитетот е 0.

Вкупниот квалитет се пресметува: за секое јадење, finish = start + prep + cook, dev = \|finish - (deadline - offset)\|, quality *= max(0, 1 - 0.2 * dev). Доколку две јадења имаат преклопување во подготовка или печење, се казнува со -1000 по час преклопување. Доколку finish > deadline, решението е неважечко.

Доколку повеќе решенија имаат ист вкупен квалитет, треба да се преферира решението каде јадењата се готови порано. За таа цел, fitness функцијата треба да содржи мала казна.

Од стандарден влез се чита N – број на јадења, а потоа N линии со 5 броја: prep_hours, cook_hours, deadline_hour, best_offset, quality.

Со користење на Генетски алгоритам имплементиран со библиотеката pygad, определете ги почетните часови на подготовка на секое јадење со цел да се максимизира вкупниот квалитет намален за казните за преклопување и доцнење. Решенијата кои го прекршуваат временскиот прозорец треба да се казнат со death penalty.

Испечатете го максималниот вкупен квалитет (заокружен на 2 децимали).

Забелешка: За да го добиете најдоброто решение во текот на сите генерации, користете `ga.best_solution(ga.last_generation_fitness)`. Возможно е да има неконзистентност на типот (list/numpy низа) на променливата chromosome/solution.

### Starter code

```python
import pygad
import random
random.seed(0)

N = int(input())
prep = []
cook = []
deadline = []
offset = []
quality = []
for _ in range(N):
    p, c, d, o, q = map(int, input().split())
    prep.append(p)
    cook.append(c)
    deadline.append(d)
    offset.append(o)
    quality.append(q)


def fitness_func(ga, solution, idx):
    ...  # TODO: implement fitness function


params = {
    'num_generations': 200,
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': ...,  # TODO: fill empty params
    'gene_space': ...,
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,
}

ga = pygad.GA(**params)
ga.run()

best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
best_fitness = fitness_func(ga, best_solution, 0)

print(f'{best_fitness:.2f}')
```

### Test cases

| Input | Result |
|-------|--------|
| `2` `1 2 5 0 8` `1 1 4 1 6` | `12.80` |

```
dish1@0, dish0@2
```

| Input | Result |
|-------|--------|
| `2` `2 1 8 0 10` `1 2 7 3 6` | `10.00` |

```
dish1@1, dish0@2
```

| Input | Result |
|-------|--------|
| `3` `1 2 6 0 7` `2 1 5 2 5` `1 1 4 1 9` | `18.20` |

```
dish2@0, dish1@1, dish0@3
```
