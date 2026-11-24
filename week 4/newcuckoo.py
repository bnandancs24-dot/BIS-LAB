
import numpy as np
import matplotlib.pyplot as plt
import math

# =====================================
# 1. SOLAR PV SYSTEM
# =====================================

V_MIN = 0
V_MAX = 50

# Illustrative partially shaded PV power curve
def pv_power(V):

    peaks = [
        (110, 12, 3),
        (250, 27, 4),
        (390, 39, 3)
    ]

    power = 0

    for height, center, width in peaks:
        power += height * np.exp(
            -((V - center) / width) ** 2
        )

    return power


# =====================================
# 2. CUCKOO SEARCH PARAMETERS
# =====================================

N_NESTS = 20
MAX_ITER = 100
PA = 0.25
ALPHA = 0.5
BETA = 1.5


# =====================================
# 3. LEVY FLIGHT
# =====================================

def levy_flight():

    sigma = (
        (
            math.gamma(1 + BETA)
            * math.sin(math.pi * BETA / 2)
        )
        /
        (
            math.gamma((1 + BETA) / 2)
            * BETA
            * 2 ** ((BETA - 1) / 2)
        )
    ) ** (1 / BETA)

    u = np.random.normal(0, sigma)
    v = np.random.normal(0, 1)

    return u / (abs(v) ** (1 / BETA) + 1e-12)


# =====================================
# 4. FITNESS FUNCTION
# =====================================

def fitness(V):

    return pv_power(V)


# =====================================
# 5. CUCKOO SEARCH
# =====================================

def cuckoo_search():

    nests = np.random.uniform(
        V_MIN, V_MAX, N_NESTS
    )

    scores = np.array([
        fitness(v) for v in nests
    ])

    best_index = np.argmax(scores)

    best_nest = nests[best_index]
    best_power = scores[best_index]

    history = []

    for iteration in range(MAX_ITER):

        for i in range(N_NESTS):

            new_solution = (
                nests[i]
                + ALPHA * levy_flight()
                * (nests[i] - best_nest)
            )

            new_solution = np.clip(
                new_solution, V_MIN, V_MAX
            )

            new_power = fitness(new_solution)

            j = np.random.randint(N_NESTS)

            if new_power > scores[j]:

                nests[j] = new_solution
                scores[j] = new_power

        # Abandon worst nests
        count = max(1, int(PA * N_NESTS))

        worst = np.argsort(scores)[:count]

        for j in worst:

            nests[j] = np.random.uniform(
                V_MIN, V_MAX
            )

            scores[j] = fitness(nests[j])

        # Update best solution
        best_index = np.argmax(scores)

        if scores[best_index] > best_power:

            best_power = scores[best_index]
            best_nest = nests[best_index]

        history.append(best_power)

    return best_nest, best_power, history


# =====================================
# 6. EXECUTE ALGORITHM
# =====================================

best_voltage, max_power, history = cuckoo_search()

print("\nSOLAR MPPT RESULTS")

print("Optimal Voltage:",
      round(best_voltage, 4), "V")

print("Maximum Power:",
      round(max_power, 4), "W")


# =====================================
# 7. PLOT PV CHARACTERISTICS
# =====================================

voltages = np.linspace(V_MIN, V_MAX, 500)

powers = [pv_power(v) for v in voltages]

plt.figure(figsize=(9, 4))

plt.plot(voltages, powers,
         label="PV Power Curve")

plt.scatter(best_voltage, max_power,
            color="red", label="CSA Maximum Power")

plt.xlabel("Voltage (V)")
plt.ylabel("Power (W)")
plt.title("Cuckoo Search Based Solar MPPT")

plt.legend()
plt.grid()
plt.show()


# =====================================
# 8. CONVERGENCE GRAPH
# =====================================

plt.figure(figsize=(9, 4))

plt.plot(history, color="green")

plt.xlabel("Iterations")
plt.ylabel("Maximum Power (W)")

plt.title("CSA Convergence Curve")

plt.grid()
plt.show()
