import math, random

DEPOT = (0, 0)
LOCS = [(2, 10), (5, 3), (12, 8), (8, 15), (1, 18), (15, 2)]
NAMES = ["Item A", "Item B", "Item C", "Item D", "Item E", "Item F"]
N, DIM = 25, len(LOCS)

def get_dist(route):
    pts = [DEPOT] + [LOCS[i] for i in route] + [DEPOT]
    return sum(math.hypot(pts[i][0] - pts[i+1][0], pts[i][1] - pts[i+1][1]) for i in range(len(pts) - 1))

def to_route(X):
    return sorted(range(DIM), key=lambda k: X[k])

X = [[random.uniform(-5, 5) for _ in range(DIM)] for _ in range(N)]
V = [[random.uniform(-1, 1) for _ in range(DIM)] for _ in range(N)]
p_best = [list(x) for x in X]
p_scores = [get_dist(to_route(x)) for x in X]

g_best = list(p_best[p_scores.index(min(p_scores))])
g_score = min(p_scores)

for _ in range(100):
    for i in range(N):
        for d in range(DIM):
            r1, r2 = random.random(), random.random()
            V[i][d] = 0.5 * V[i][d] + 1.5 * r1 * (p_best[i][d] - X[i][d]) + 1.5 * r2 * (g_best[d] - X[i][d])
            X[i][d] += V[i][d]
        
        score = get_dist(to_route(X[i]))
        if score < p_scores[i]:
            p_scores[i], p_best[i] = score, list(X[i])
            if score < g_score:
                g_score, g_best = score, list(X[i])

best_route = ["Depot"] + [NAMES[i] for i in to_route(g_best)] + ["Depot"]
print("Optimal Route:", " -> ".join(best_route))
print(f"Distance: {g_score:.2f} m")
