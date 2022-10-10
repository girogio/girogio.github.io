---
title: "kvant"
showToc: false
TocOpen: false
draft: false
hidemeta: true
# alias: ['/kvant']
comments: false
hideSummary: true
searchHidden: false
ShowReadingTime: false
ShowBreadCrumbs: false
ShowPostNavLinks: false
---
> *We all know that quantum computing is the future, so in order to practice my quantum computing skills, I have built my own encoding scheme, then I used it to hide the flag, can you recover it!*

  -  <a download href='/challenges/misc/kvant/kvant.py'>kvant.py</a>
  -  <a download href='/challenges/misc/kvant/enc.txt'>enc.txt</a> 
---

This challenge was in the misc category of the first GDG Algiers CTF due to involving quantum computing. In my opinion, a well founded knowledge of cryptography is useful in this challenge as shown later.

Thanks to the basics track of the Qalypso Summer School I was able to fully understand the challenge and use the intended solution.

---
## kvant.py
The first function in `kvant.py` is basically the application of the ket notation on a binary number.

```py
def get_state(x):
    l = [0] * 2**len(x)
    l[int(x, 2)] = 1
    return l
```
In mathematical terms, it maps a binary number string $b$ of length $n$ (corresponding to a decimal number $x$) to an array of size $2^n$ whose entries are all $0$ except for the $x^ \text{th}$ one, which is $1$. An example:
$$\verb|get_state('01')| = \ket{01} = \begin{pmatrix}0\\\\1\\\\0\\\\0\end{pmatrix} = \verb|[0, 1, 0, 0]|$$

The next two functions should be self explanatory:

```py
def str2bin(s):
    return ''.join(bin(ord(i))[2:].zfill(8) for i in s)

def bin2str(a):
    return ''.join(chr(int(a[i:i+8], 2)) for i in range(0, len(a), 8))
```
<br/>

### `encode_1()`


Now comes the interesting part. The following function expects an initial state vector and creates a single qubit quantum circuit. Thus the initial state must be an array of size $2^1$.

```py
def encode_1(initial_state):
    qc = QuantumCircuit(1)
    qc.initialize(initial_state)
    qc.x(0)
    qc.save_statevector()
    qobj = assemble(qc)
    state = sim.run(qobj).result()
    return list(state.get_statevector().real.astype(int))
```
It is to be noted that the above circuit performs the Qiskit `.x()` gate (`NOT`) on the $0^\text{th}$ qubit of the circuit, returning the resultant state vector. Given our definitions of $\ket{0}$ and $\ket{1}$, the possible results can be as follows:

$$\verb|NOT| \ket{0} = \verb|NOT| \begin{pmatrix} 1\\\\0\end{pmatrix} = \begin{pmatrix} 0\\\\1\end{pmatrix} = \ket{1}$$

$$\verb|NOT| \ket{1} = \verb|NOT| \begin{pmatrix} 0\\\\1\end{pmatrix} = \begin{pmatrix} 1\\\\0\end{pmatrix} = \ket{0}$$

<br/>

### `encode_2()`

The second encoding function happens to be a 2-qubit circuit, hence expecting a state vector of size $2^2$ as an input.

```py
def encode_2(initial_state):
    qc = QuantumCircuit(2)
    qc.initialize(initial_state)
    qc.cx(0, 1)
    qc.save_statevector()
    qobj = assemble(qc)
    state = sim.run(qobj).result()
    return list(state.get_statevector().real.astype(int))
```
This time however, a `.cx()` gate (`CNOT`) is being applied to the 2 qubits – the 0th and 1st bit being the target and control bits respectively (*damn qiskit for inverting their order*). The `CNOT` gate simply flips the target bit, only if the control bit is set to 1 and does nothing otherwise. Fortunately, mathematics comes to the rescue with a handy matrix definition for the `CNOT` gate:

$$\verb|CNOT| := \begin{pmatrix} 1&0&0&0\\\\0&0&0&1\\\\0&0&1&0\\\\0&1&0&0\\\\\end{pmatrix}$$

Its effect on a $1\times 4$ matrix $M$ is replicable by swapping the $1^\text{st}$ and $3^\text{rd}$  entries of $M$ (*starting from 0*), i.e.

$$\verb|CNOT| \begin{pmatrix}a\\\\b\\\\c\\\\d\end{pmatrix} = \begin{pmatrix} 1&0&0&0\\\\0&0&0&1\\\\0&0&1&0\\\\0&1&0&0\\\\\end{pmatrix} \begin{pmatrix}a\\\\b\\\\c\\\\d\end{pmatrix}= \begin{pmatrix}a\\\\d\\\\c\\\\b\end{pmatrix}$$

An example with a prepared state $\ket{11}$:

$$\verb|CNOT| \ket{11} = \verb|CNOT| \begin{pmatrix}0\\\\0\\\\0\\\\1\end{pmatrix} = \begin{pmatrix}0\\\\1\\\\0\\\\0\end{pmatrix} = \verb|[0,1,0,0]|$$

### `encode_3()`

The third encoding function is a 3-qubit circuit, hence expecting a state vector of size $2^3$ as an input.

```py
def encode_3(initial_state):
    qc = QuantumCircuit(3)
    qc.initialize(initial_state)
    qc.ccx(0, 1, 2)
    qc.save_statevector()
    qobj = assemble(qc)
    state = sim.run(qobj).result()
    return list(state.get_statevector().real.astype(int))
```

The last encoding function is a `.ccx()` gate (`CCNOT`), that acts on 3 qubits. The `CCNOT` gate is a controlled version of the `CNOT` gate, i.e. it flips the target bit only if **both control bits** are set to 1 and does nothing otherwise. The `CCNOT` gate is defined as follows:

$$\verb|CCNOT| = \begin{pmatrix}
1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\\\
0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\\\
0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\\\
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\\\
0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\\\
0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\\\
0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\\\\end{pmatrix}$$

Again, it can be seen as swapping the last and second to last entries of a $1\times 8$ matrix $M$ like so:

$$\verb|CCNOT| \begin{pmatrix}a\\\\b\\\\c\\\\d\\\\e\\\\f\\\\g\\\\h\end{pmatrix} = \begin{pmatrix}
1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\\\
0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\\\
0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\\\
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\\\
0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\\\
0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\\\
0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\\\\end{pmatrix} \begin{pmatrix}a\\\\b\\\\c\\\\d\\\\e\\\\f\\\\g\\\\h\end{pmatrix}= \begin{pmatrix}a\\\\b\\\\c\\\\d\\\\e\\\\f\\\\h\\\\g\end{pmatrix}$$ 

### encrypt_1/2/3()

The `encrypt_1/2/3()` functions are the ones that actually perform the encryption. The first one iterates over every bit, applying the `encode_1()` to it and concatenating all the entries of the resulting state vectors. The second and third functions do the same, but with the `encode_2()` and `encode_3()` functions over every pairs and triples of bits respectively.

**Note:** At every step, the length of the encrypted message doubles!

Consider the encryption with the following string – `'a'`


```text
'a' 
```

↓ str2bin()
```text
01100001 
```

↓ encode_1()

```text
not |0> not |1> not |1> not |0> not |0> not |0> not |0> not |1>
```

↓ computing!
```text
|1> |0> |0> |1> |1> |1> |1> |0> 
```

↓ expanding the states!
```text
01 10 10 01 01 01 01 10 
```

↓ encode_2() `remember, first bit is target and second bit is control`
```text
cnot |01> cnot |10> cnot |10> ...
```

↓text computing!
```text
|11> |10> |10> ...
```

↓ expanding the states!
```text
0001 0010 0010 0001 0001 0001 0001 0010
```

↓ group every 3 bits (*last one is wrong due to the short length of the message*)
```text
000 100 100 010 000 100 010 001 000 100 10  
```

↓ encode_3()
```text
ccnot |000> ccnot |100> ccnot |100> ...
```

↓ computing!
```text
|000> |100> |100> ...
```

↓ expanding the states!
```text
10000000 00001000 0000100 ...
```
## Solution!

The output here observed matches exactly the `str2bin()` of the encrypted message. The encryption is reversible! All we need to do is go backwards, swap the right entries, collapse the states, use `bin2str()` and we're done!

## decrypt_3()

