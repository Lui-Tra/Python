# Logik Vereinfacher

### Parser
Der Parser erkennt zwei Formen:
1. Eine Aussagenlogische Formel mit Formelzeichen ¬, ∧, ∨, ⊕, →, ↔, ITE(a, b, c), nand, nor bzw. not, and, or und xor.
2. Eine Formel in KNF als Menge von Klauseln: {{<Klausel 1>}, {<Klausel 2>}}
```python
import parser
formel = parser.parse("<Formel>")
```

### Term vereinfachen
Bildet die NNF (Negationsnormalform) und multipliziert mit Vereinfachungen aus.
```python
formel.simplify()
```

### DNF und KNF
Es können sowohl kanonische, sowie vereinfachte KNF und DNF erzeugt werden.
```python
formel.canoncial_cnf()
formel.canoncial_dnf()

formel.simple_cnf()
formel.simple_dnf()
```

### KV-Diagramm
Mittels pygame kann ein KV-Diagramm ausgegeben werden.
```python
formel.kv(
    scale=2,                # scale 2 für HiDPI Bildschirme
    order="abc"             # irgendein Iterable, das angibt, in welcher Reihenfolge 
                            # die Variablen angezeigt werden sollen.
)
```

### Wahrheitstafeln
Bunte Wahrheitstafeln können auch ausgegeben werden
```python
formel.print_truth_table()
```

### DPLL
Der DPLL Algorithmus mit graphischer ausgabe erhält man mit:
```python
formel.dpll(scale=2)
```

### Resolventbildung
Normale Resolventenbildung geht mittels:
```python
formel.resolvent(scale=2)
```

Linear Resolventenbildung geht mittels:
```python
formel.linear_resolvent(scale=2)
```
