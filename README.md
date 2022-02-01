# Logik Vereinfacher

## Funktionen

Aus einer eingegebenen Formel können folgende Dinge erstellt werden:

1. Ein vereinfachter Term
2. Kanonische DNF & KNF
3. KV Diagramm
4. Wahrheitstabelle

## Anwendung

```python
import parser
formel = parser.parse("<Formel>")
```

### Term vereinfachen
```python
formel.simplify()
```

### DNF
```python
formel.()
```

### KNF - coming soon