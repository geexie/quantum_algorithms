# from qiskit import QuantumProgram
from qiskit import QuantumCircuit, execute, Aer

# Q = QuantumProgram()
# qr = Q.create_quantum_register("qr", 3)
# cr = Q.create_classical_register("cr", 3)
#qc = Q.create_circuit("andgate", [qr], [cr])
qc = QuantumCircuit(3, 3)

def tiffoli1(qc, r0, r1, r2):
    #starting here, we implement a tiffoli gate which flips qr[2] if both qr[0] and qr[1] are 1
    qc.h(r2)
    qc.cx(r1,r2)
    qc.tdg(r2)
    qc.cx(r0,r2)
    qc.t(r2)
    qc.cx(r1,r2)
    qc.tdg(r2)
    qc.cx(r0,r2)
    qc.t(r1)
    qc.t(r2)
    qc.h(r1)
    qc.h(r2)
    qc.cx(r1,r2)
    qc.h(r1)
    qc.h(r2)
    qc.cx(r1,r2)
    qc.cx(r0,r2)
    qc.t(r0)
    qc.h(r1)
    qc.tdg(r2)
    qc.cx(r0,r2)
    qc.cx(r1,r2)
    qc.h(r1)
    qc.h(r2)
    qc.cx(r1,r2)
    qc.h(r1)
    qc.h(r2)
    qc.cx(r1,r2)

def tiffoli2(qc, r0, r1, r2):
    qc.h(r2)
    qc.cx(r1, r2)
    qc.tdg(r2)
    qc.cx(r0, r2)
    qc.t(r2)
    qc.cx(r1, r2)
    qc.tdg(r2)
    qc.cx(r0, r2)
    qc.t(r1)
    qc.t(r2)
    qc.h(r2)
    qc.cx(r1, r2)
    qc.h(r1)
    qc.h(r2)
    qc.cx(r1, r2)
    qc.h(r1)
    qc.h(r2)
    qc.cx(r1, r2)
    qc.cx(r0, r2)
    qc.t(r0)
    qc.tdg(r2)
    qc.cx(r0, r2)
    qc.cx(r1, r2)
    qc.cx(r2, r1)
    qc.cx(r1, r2)

def testtiffolihelper(tiffun, rs):
    Q = QuantumProgram()
    qr = Q.create_quantum_register("qr", 3)
    cr = Q.create_classical_register("cr", 3)
    qc = Q.create_circuit("tiffolitest", [qr], [cr])
    if rs[2] == 1:
        goodresult = str(1 - rs[1] * rs[0]) + str(rs[1]) + str(rs[0])
    else:
        goodresult = str(rs[1] * rs[0]) + str(rs[1]) + str(rs[0])
    for i in range(3):
        if rs[i] == 1:
            qc.x(qr[i])
    tiffun(qc, qr[0], qr[1], qr[2])
    qc.measure(qr, cr)
    result = Q.execute(["tiffolitest"], backend="local_qasm_simulator", shots=100).get_data("tiffolitest")
    return goodresult in result["counts"] and result["counts"][goodresult] == 100

def testtiffoli(tifffun):
    testtiffolihelper(tifffun, [0, 0, 0]) or print("test tiffloi failed at 0")
    testtiffolihelper(tifffun, [0, 0, 1]) or print("test tiffloi failed at 1")
    testtiffolihelper(tifffun, [0, 1, 0]) or print("test tiffloi failed at 2")
    testtiffolihelper(tifffun, [0, 1, 1]) or print("test tiffloi failed at 3")
    testtiffolihelper(tifffun, [1, 0, 0]) or print("test tiffloi failed at 4")
    testtiffolihelper(tifffun, [1, 0, 1]) or print("test tiffloi failed at 5")
    testtiffolihelper(tifffun, [1, 1, 0]) or print("test tiffloi failed at 6")
    testtiffolihelper(tifffun, [1, 1, 1]) or print("test tiffloi failed at 7")

def grover(oracle, qc, x0, x1, q):
    #this implements the oracle
    oracle(qc, x0, x1, q)
    # #now implement the grover operator
    qc.h(x0)
    qc.h(x1)
    qc.x(x0)
    qc.x(x1)
    qc.h(x1)
    qc.cx(x0, x1)
    qc.h(x1)
    qc.x(x0)
    qc.x(x1)
    qc.h(x0)
    qc.h(x1)
    qc.h(q)

# testtiffoli(tiffoli1)
# testtiffoli(tiffoli2)

b0 = 0#qr[0]
b1 = 2#qr[2]
b2 = 1#qr[1]

qc.x(b2)#put b2 in state |1>
qc.h(b0)#put b0 in (|0>+|1>)/sqrt(2)
qc.h(b1)#put b1 in (|0>+|1>)/sqrt(2)
qc.h(b2)#put b2 in state (|0>-|1>)/sqrt(2)
for i in range(1):#apply the oracle/grover operator in a loop
    grover(tiffoli2, qc, b0, b1, b2)
qc.measure([0,1,2], [0,1,2])

# result = Q.execute(["andgate"], backend="local_qasm_simulator", shots=1000)
# print(result)

# Use Aer's qasm_simulator
simulator = Aer.get_backend('qasm_simulator')
# Execute the circuit on the qasm simulator
job = execute(qc, simulator, shots=1000)
# Grab results from the job
result = job.result()

print(result.get_counts())
# print(Q.get_qasm("andgate"))

qc.draw("mpl", filename="andgate.png")

print (qc.depth(), qc.size(), qc.width())
print(qc.qasm())