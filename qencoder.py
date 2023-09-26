from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

circuit = QuantumCircuit(1, 1)

# 0: Base rectilínea (|0⟩, |1⟩)
# 1: Base diagonal (|+⟩, |-⟩)
import random
aliceBasis = random.choice([0, 1])

if aliceBasis == 0:
    aliceBit = random.choice([0, 1])
    if aliceBit == 1:
        circuit.x(0)  # Aplicar una puerta X para cambiar |0⟩ a |1⟩
else:
    circuit.h(0)  # Aplicar una puerta Hadamard para preparar |+⟩
    aliceBit = random.choice([0, 1])
    if aliceBit == 1:
        circuit.z(0)  # Aplicar una puerta Z para cambiar |+⟩ a |-⟩

simulator = Aer.get_backend('qasm_simulator')
circuit.measure(0, 0)
result = execute(circuit, simulator, shots=1).result()
alice_measurement = int(list(result.get_counts().keys())[0])

bobBasis = random.choice([0, 1])

if bobBasis != aliceBasis:
    circuit.h(0)  # Cambiar a la base correcta si es necesario
circuit.measure(0, 0)
result = execute(circuit, simulator, shots=1).result()
bob_measurement = int(list(result.get_counts().keys())[0])

if aliceBasis == bobBasis:
    shared_key = aliceBit  # Comparten el bit si las bases coinciden
else:
    shared_key = None  # Descartan el resultado si las bases difieren

print(f"Alice chose the base {aliceBasis} and measured {alice_measurement}")
print(f"Bob chose the base {bobBasis} and measured {bob_measurement}")

if shared_key is not None:
    print(f"Alice and Bob share the bit {shared_key} as a quantum key.")
else:
    print("Couldn't set the quantum key.")
