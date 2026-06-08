from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import WeightedAdder
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import math

#To compute the sum of the integers in our set we use WeightedAdder  from qiskit.circuit.library.
#It is a Quantum Circuit that computes a weighted sum of binary variables.

def oracle(set, target):
    add = WeightedAdder(len(set), set)

    n_control = add.num_control_qubits
    n_sum = add.num_sum_qubits
    n_work = add.num_carry_qubits

    q = QuantumRegister(len(set), "q")
    s = QuantumRegister(n_sum, "s")
    w = QuantumRegister(n_work, "w")
    c = QuantumRegister(n_control, "c")
    a = QuantumRegister(1, "a")

    qc = QuantumCircuit(q, s, w, c, a, name="Oracle")

    adder_gate = add.to_gate(label="Sum")

    qc.append(adder_gate, q[:] + s[:] + w[:] + c[:])


    target_bits = format(target, f"0{n_sum}b")[::-1]

    for i, bit in enumerate(target_bits):
        if bit == "0":
            qc.x(s[i])

    qc.mcx(s[:], a[0])
    qc.z(a[0])
    qc.mcx(s[:], a[0])

    for i, bit in enumerate(target_bits):
        if bit == "0":
            qc.x(s[i])

    qc.append(adder_gate.inverse(), q[:] + s[:] + w[:] + c[:])

    return qc


def add_diffuser(grover_circuit, n):
    grover_circuit.h(list(range(n)))
    grover_circuit.x(list(range(n)))

    grover_circuit.h(n - 1)
    grover_circuit.mcx(list(range(n - 1)), n - 1)
    grover_circuit.h(n - 1)

    grover_circuit.x(list(range(n)))
    grover_circuit.h(list(range(n)))


def bitstring_to_subset(bitstring, set):
    bits = bitstring[::-1]
    subset = []

    for i, bit in enumerate(bits):
        if bit == "1":
            subset.append(set[i])

    return subset


benchmark_examples = [
    ([2, 3, 5, 7], 7),
    ([1, 2, 4, 7], 6),
    ([1, 3, 4, 6], 10),
    ([1, 2, 3, 4], 5),
    ([2, 4, 6, 7], 3),
]

for set, target in benchmark_examples:
    print("\n==============================")
    print("Set:", set)
    print("Target:", target)

    n = len(set)

    oracle_circuit = oracle(set, target)
    oracle_gate = oracle_circuit.to_gate(label="Oracle")

    grover_circuit = QuantumCircuit(*oracle_circuit.qregs)

    grover_circuit.h(list(range(n)))

    iterations = round((math.pi / 4) * math.sqrt(2 ** n))

    for _ in range(iterations):
        grover_circuit.append(oracle_gate, grover_circuit.qubits)
        add_diffuser(grover_circuit, n)

    creg = ClassicalRegister(n, "meas")
    grover_circuit.add_register(creg)
    grover_circuit.measure(list(range(n)), creg)

    sim = AerSimulator()
    compiled = transpile(grover_circuit, sim)
    result = sim.run(compiled, shots=1024).result()
    counts = result.get_counts()

    best_bitstring = max(counts, key=counts.get)
    answer = bitstring_to_subset(best_bitstring, set)

    print("Best bitstring:", best_bitstring)
    print("Subset:", answer)


    if sum(answer) == target:
        print("Result: Solution found!")
    else:
        print("Result: No solution found with high probability.")

