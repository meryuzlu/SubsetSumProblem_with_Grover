
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister,transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import math

def controlled_increment(qc, control, s):
    m = len(s)

    for j in reversed(range(1, m)):
        controls = [control] + list(s[:j])
        qc.mcx(controls, s[j])

    qc.cx(control, s[0])

def controlled_add_number(qc, control, s, number):
    for _ in range(number):
        controlled_increment(qc, control, s)


def compute_subset_sum(qc, q, s, numbers):
    for i, number in enumerate(numbers):
        controlled_add_number(qc, q[i], s, number)

def controlled_decrement(qc, control, s):
    m = len(s)

    qc.cx(control, s[0])

    for j in range(1, m):
        controls = [control] + list(s[:j])
        qc.mcx(controls, s[j])

def controlled_subtract_number(qc, control, s, number):
    for _ in range(number):
        controlled_decrement(qc, control, s)

def uncompute_subset_sum(qc, q, s, numbers):
    for i in reversed(range(len(numbers))):
        controlled_subtract_number(qc, q[i], s, numbers[i])


def comparison(qc, s, flag, target):
    m = len(s)
    target_bits = format(target, f"0{m}b")[::-1]

    for j, bit in enumerate(target_bits):
        if bit == "0":
            qc.x(s[j])

    qc.mcx(list(s), flag[0])


    for j, bit in enumerate(target_bits):
        if bit == "0":
            qc.x(s[j])

def oracle(numbers, target):
    n = len(numbers)
    m = math.ceil(math.log2(sum(numbers) + 1))

    q = QuantumRegister(n, "q")
    s = QuantumRegister(m, "sum")
    flag = QuantumRegister(1, "flag")

    qc = QuantumCircuit(q, s, flag, name="Oracle")

    compute_subset_sum(qc, q, s, numbers)

    if target < 2 ** m:
        comparison(qc, s, flag, target)

    uncompute_subset_sum(qc, q, s, numbers)

    return qc

def add_diffuser(qc, q):
    n = len(q)

    qc.h(q)
    qc.x(q)

    qc.h(q[n - 1])
    qc.mcx(list(q[:n - 1]), q[n - 1])
    qc.h(q[n - 1])

    qc.x(q)
    qc.h(q)

def bitstring_to_subset(bitstring, numbers):
    bitstring = bitstring[::-1]
    subset = []

    for i, bit in enumerate(bitstring):
        if bit == "1":
            subset.append(numbers[i])

    return subset




def run_grover(numbers, target):
    n = len(numbers)
    iterations=math.floor((math.pi / 4) * math.sqrt(2 ** n))
    m = math.ceil(math.log2(sum(numbers) + 1))

    q = QuantumRegister(n, "q")
    s = QuantumRegister(m, "sum")
    flag = QuantumRegister(1, "flag")

    c = ClassicalRegister(n, "c")

    qc = QuantumCircuit(q, s, flag, c)

    qc.x(flag[0])
    qc.h(flag[0])

    qc.h(q)

    oracle_gate = oracle(numbers, target).to_gate(label="Oracle")

    for _ in range(iterations):
        qc.append(oracle_gate, q[:] + s[:] + flag[:])
        add_diffuser(qc, q)

    qc.measure(q, c)


    sim = AerSimulator()
    compiled = transpile(qc, sim)
    result = sim.run(compiled, shots=1024).result()
    counts = result.get_counts()












    best_bitstring = max(counts, key=counts.get)
    subset = bitstring_to_subset(best_bitstring, numbers)

    print("\n==============================")
    print("Set:", numbers)
    print("Target:", target)
    print("Subset found:", subset)


    if sum(subset) == target:
        print("Result: Solution found!")
    else:
        print("Result: No solution found with high probability.")

    plot_histogram(counts, title=f"Set={numbers}, Target={target}")
    plt.show()

    return qc, counts


benchmark_examples = [
    ([2, 3, 5, 7], 7),
    ([1, 2, 4, 7], 6),
    ([1, 3, 4, 6], 10),
    ([1, 2, 3, 4], 5),
    ([2, 4, 6, 7], 3),
]


for numbers, target in benchmark_examples:
    run_grover(numbers, target)