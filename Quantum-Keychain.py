from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import random

# Función para generar una clave BB84 segura
def generate_bb84_key(length):
    key = ""
    for _ in range(length):
        circuit = QuantumCircuit(1, 1)

        # 0: Base rectilínea (|0⟩, |1⟩)
        # 1: Base diagonal (|+⟩, |-⟩)
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
            continue  # Descartar el resultado si las bases difieren

        circuit.measure(0, 0)
        result = execute(circuit, simulator, shots=1).result()
        bob_measurement = int(list(result.get_counts().keys())[0])

        if aliceBasis == bobBasis:
            shared_bit = aliceBit  # Comparten el bit si las bases coinciden
            key += str(shared_bit)

    return key

# Función para generar una clave RSA segura
def generate_rsa_key_pair(bits=2048):
    key = RSA.generate(bits)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Función para encriptar un mensaje usando una clave pública RSA
def rsa_encrypt(message, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

# Función para desencriptar un mensaje usando una clave privada RSA
def rsa_decrypt(encrypted_message, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message.decode()

# Realizar la comunicación cuántica BB84 para generar una clave segura
bb84_key_length = 128  # Longitud de la clave BB84 (puede ajustarse)
bb84_key = generate_bb84_key(bb84_key_length)

if bb84_key:
    # Generar clave RSA segura
    rsa_private_key, rsa_public_key = generate_rsa_key_pair()
    
    # Encriptar la clave BB84 utilizando RSA
    encrypted_bb84_key = rsa_encrypt(bb84_key, rsa_public_key)
    
    # Solicitar al usuario un mensaje para encriptar
    message = input("Ingrese un mensaje para encriptar: ")
    
    # Encriptar el mensaje usando RSA
    encrypted_message = rsa_encrypt(message, rsa_public_key)
    
    print("BB84 Key:")
    print(bb84_key)
    print("RSA Public Key:")
    print(rsa_public_key.decode())
    print("Mensaje Encriptado (RSA):")
    print(encrypted_message.hex())
    
    # Desencriptar el mensaje usando RSA
    decrypted_message = rsa_decrypt(encrypted_message, rsa_private_key)
    print("Mensaje Desencriptado (RSA):", decrypted_message)
else:
    print("Couldn't set the quantum key.")
