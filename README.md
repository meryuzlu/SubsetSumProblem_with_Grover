# SUBSET-SUM PROBLEM WITH GROVER'S ALGORITHM


This project implements Grover’s search algorithm to solve small instances of the Subset Sum Problem using Qiskit.

Instead of relying on Qiskit’s built-in WeightedAdder circuit, the subset-sum oracle is constructed manually from elementary reversible quantum gates. The project demonstrates how reversible arithmetic, a phase oracle, and Grover’s diffusion operator can be combined to search for subsets whose elements sum to a specified target.



## Problem Statement 

Given a finite set of positive integers A = {a₀, a₁, ..., aₙ₋₁} and a target value T, the objective is to determine a subset S ⊆ A whose elements satisfy ∑ x = T,   x ∈ S. For example, A = {2, 3, 5, 7} and T = 7 has solutions {7} and {2,5}.


## Algorithm Overview

Each possible subset is represented by a binary string. For example, fo the example above, 1010 means that the 3 and 7 are included in the subset.

The algorithm proceeds as follows:

1. Prepare an equal superposition over all possible subsets.
2. Compute each subset sum using a manually constructed reversible adder.
3. Compare the computed sum with the target and mark valid subsets with a phase flip.
4. Uncompute the auxiliary registers.
5. Apply Grover’s diffuser.
6. Repeat the oracle and diffuser the appropriate number of times.
7. Compute the final statevector and obtain the probability distribution over the candidate subsets.

The subsets with the highest probabilities correspond to the solutions amplified by Grover’s algorithm.



## Repository Contents


*Subset_Sum_Manual_Adder.ipynb	Complete notebook containing the implementation, explanations, circuit construction, and benchmark examples.

*Subset_Sum_Final.py	Python implementation of the same algorithm.

subset_sum_WeightedAdder.ipynb	Earlier implementation using Qiskit’s built-in WeightedAdder circuit for comparison.



## Notes

* This implementation is intended for educational and research purposes.
* Intermediate measurements are not used; the notebook uses Qiskit’s Statevector class to inspect the final probability distribution.
* The implementation is designed for small benchmark instances suitable for quantum circuit simulation.



## References

* Qiskit Documentation: https://qiskit.org/documentation/
* IBM Quantum Learning: https://quantum.cloud.ibm.com/learning



## Example Usage

Open Subset_Sum_Manual_Adder.ipynb in Jupyter Notebook or Google Colab and run the cells sequentially. Alternatively, exacute Subset_Sum_Final.py to run the benchmark examples included in the project. 

To solve the example introduced above, call 

run_grover([2, 3, 5,7], 7)

The program computes the final statevector, displays a histogram of the resulting probability distribution over all candidate subsets, and prints the most likely subset found by Grover's algorithm.


The notebook will

* construct the subset-sum oracle,
* perform the Grover iterations,
* compute the final statevector,
* display the probability distribution over all candidate subsets, and
* print the most likely subset found by the algorithm.


