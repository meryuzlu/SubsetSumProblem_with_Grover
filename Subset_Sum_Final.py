"""
Subset Sum Problem using Grover's Algorithm with manual reversible adder implementation
"""



from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector

from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import math



#Compute the subset-sum
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

#Equality Test
def comparison(qc, s, a, target):
    m = len(s)
    target_bits = format(target, f"0{m}b")[::-1]

    for j, bit in enumerate(target_bits):
        if bit == "0":
            qc.x(s[j])

    qc.mcx(list(s), a[0])
    qc.z(a[0])
    qc.mcx(list(s), a[0])

    for j, bit in enumerate(target_bits):
        if bit == "0":
            qc.x(s[j])

#Inverse subset-sum
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

#Construct the oracle
def oracle(numbers, target):
    n = len(numbers)
    m = math.ceil(math.log2(sum(numbers) + 1)) # To compute how many qubits we need to store the sum. We need "+1" just to store 0 that comes from the empty set.

    q = QuantumRegister(n, "q")
    s = QuantumRegister(m, "sum")
    a = QuantumRegister(1, "anc")

    qc = QuantumCircuit(q, s, a, name="Oracle")

    compute_subset_sum(qc, q, s, numbers)

    if target < 2 ** m:
        comparison(qc, s, a, target)


    uncompute_subset_sum(qc, q, s, numbers)

    return qc

#Construct the diffuser
def add_diffuser(qc, q):
    n = len(q)

    qc.h(q)
    qc.x(q)

    qc.h(q[n - 1])
    qc.mcx(list(q[:n - 1]), q[n - 1])
    qc.h(q[n - 1])

    qc.x(q)
    qc.h(q)

#Turn bitstrings into subsets
def bitstring_to_subset(bitstring, set):
    bits = bitstring[::-1]
    subset = []

    for i, bit in enumerate(bits):
        if bit == "1":
            subset.append(set[i])

    return subset

#Put everything together

def run_grover(numbers, target):
    n = len(numbers)
    iterations = math.floor((math.pi / 4) * math.sqrt(2 ** n))
    m = math.ceil(math.log2(sum(numbers) + 1))

    q = QuantumRegister(n, "q")
    s = QuantumRegister(m, "sum")
    a = QuantumRegister(1, "anc")

    qc = QuantumCircuit(q, s, a)

    qc.h(q)

    oracle_gate = oracle(numbers, target).to_gate(label="Oracle")

    for _ in range(iterations):
        qc.append(oracle_gate, q[:] + s[:] + a[:])
        add_diffuser(qc, q)

    # No measurements are used.
    # We use the final statevector to obtain the output distribution
    # of the state qubits.
    state = Statevector.from_instruction(qc)

    probabilities = state.probabilities_dict(qargs=list(range(n)))

    best_bitstring = max(probabilities, key=probabilities.get)
    subset = bitstring_to_subset(best_bitstring, numbers)

    print("\n==============================")
    print("Set:", numbers)
    print("Target:", target)

    if sum(subset) == target:
        print("Most likely solution is:", subset)
    else:
        print("Result: No solution found with high probability.")

    fig = plot_histogram(
        probabilities,
        title=f"Set={numbers}, Target={target}",
        figsize=(12, 5),
        bar_labels=False
    )

    plt.show()

    return qc, probabilities

#Benchmark Examples
benchmark_examples = [
    ([2, 3, 5, 7], 7),
    ([1, 2, 4, 7], 6),
    ([1, 3, 4, 6], 10),
    ([1, 2, 3, 4], 50),
    ([2, 4, 6, 7], 3),
]


for numbers, target in benchmark_examples:
    run_grover(numbers, target)