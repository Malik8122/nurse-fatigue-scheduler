# engine/nsga2.py
import numpy as np
import random
from engine.fatigue_model import compute_fatigue_score

SHIFTS = ["Early", "Day", "Late", "Night", "Off"]
FORBIDDEN = {
    "Night": ["Early", "Day", "Late"],
    "Late":  ["Early"],
    "Day":   [],
    "Early": [],
    "Off":   []
}

def random_schedule(nurses, total_days):
    return {nid: [random.choice(SHIFTS) for _ in range(total_days)] for nid in nurses}

def count_violations(schedule, scenario, week_demands, total_days):
    violations = 0
    nurses = scenario["nurses"]
    shift_types = list(scenario["shift_types"].keys())
    num_weeks = total_days // 7

    for week_idx in range(num_weeks):
        wd = week_demands[week_idx % len(week_demands)]
        for day in range(7):
            abs_day = week_idx * 7 + day
            for shift in shift_types:
                for skill, day_reqs in wd["demands"].get(shift, {}).items():
                    mn, mx = day_reqs[day]
                    count = sum(
                        1 for nid, shifts in schedule.items()
                        if shifts[abs_day] == shift and skill in nurses[nid]["skills"]
                    )
                    if count < mn:
                        violations += (mn - count) * 2
                    if count > mx:
                        violations += (count - mx)

    for nid, shifts in schedule.items():
        contract = scenario["contracts"][nurses[nid]["contract"]]
        consec = 0
        for s in shifts:
            consec = consec + 1 if s != "Off" else 0
            if consec > contract["max_consec_work"]:
                violations += 1
        for i in range(len(shifts) - 1):
            if shifts[i + 1] in FORBIDDEN.get(shifts[i], []):
                violations += 2

    return violations

def evaluate(schedule, scenario, week_demands, total_days):
    fatigue_scores = [compute_fatigue_score(shifts) for shifts in schedule.values()]
    avg_fatigue = np.mean(fatigue_scores)
    violations = count_violations(schedule, scenario, week_demands, total_days)
    return avg_fatigue, violations

def mutate(schedule, mutation_rate=0.02):
    new_schedule = {}
    for nid, shifts in schedule.items():
        new_shifts = shifts[:]
        for i in range(len(new_shifts)):
            if random.random() < mutation_rate:
                new_shifts[i] = random.choice(SHIFTS)
        new_schedule[nid] = new_shifts
    return new_schedule

def crossover(s1, s2):
    child = {}
    nurse_ids = list(s1.keys())
    point = random.randint(1, len(nurse_ids) - 1)
    for i, nid in enumerate(nurse_ids):
        child[nid] = s1[nid][:] if i < point else s2[nid][:]
    return child

def dominates(a, b):
    return all(x <= y for x, y in zip(a, b)) and any(x < y for x, y in zip(a, b))

def fast_non_dominated_sort(population, objectives):
    n = len(population)
    domination_count = [0] * n
    dominated_by = [[] for _ in range(n)]
    fronts = [[]]
    rank = [0] * n

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if dominates(objectives[i], objectives[j]):
                dominated_by[i].append(j)
            elif dominates(objectives[j], objectives[i]):
                domination_count[i] += 1
        if domination_count[i] == 0:
            fronts[0].append(i)
            rank[i] = 0

    f = 0
    while fronts[f]:
        next_front = []
        for i in fronts[f]:
            for j in dominated_by[i]:
                domination_count[j] -= 1
                if domination_count[j] == 0:
                    rank[j] = f + 1
                    next_front.append(j)
        fronts.append(next_front)
        f += 1

    return fronts[:-1], rank

def run_nsga2(scenario, week_demands, total_days=28, pop_size=30, generations=50):
    nurses = scenario["nurses"]
    population = [random_schedule(nurses, total_days) for _ in range(pop_size)]
    best_schedule = None
    best_score = float("inf")

    for gen in range(generations):
        objectives = [evaluate(ind, scenario, week_demands, total_days) for ind in population]

        fronts, ranks = fast_non_dominated_sort(population, objectives)

        for i, (f, v) in enumerate(objectives):
            if v == 0 and f < best_score:
                best_score = f
                best_schedule = population[i]

        new_pop = []
        while len(new_pop) < pop_size:
            i1, i2 = random.sample(range(pop_size), 2)
            parent1 = population[i1] if ranks[i1] <= ranks[i2] else population[i2]
            i3, i4 = random.sample(range(pop_size), 2)
            parent2 = population[i3] if ranks[i3] <= ranks[i4] else population[i4]
            child = mutate(crossover(parent1, parent2))
            new_pop.append(child)

        population = new_pop

    if best_schedule is None:
        best_schedule = population[0]

    return best_schedule, objectives