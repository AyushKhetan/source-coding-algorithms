# Source Coding Algorithms using Python

A Python implementation of D-ary source coding algorithms developed as part of the **Information Theory & Coding** course at BITS Pilani.

The project implements multiple source coding techniques, compares their coding efficiency, verifies theoretical bounds, performs Huffman decoding, and generates graphical representations of Huffman and Shannon-Fano coding trees.

---

## Features

- D-ary Huffman Coding
- D-ary Shannon-Fano Coding
- Shannon Coding
- Shannon-type Coding
- Huffman Decoding
- Entropy Computation
- Expected Code Length Analysis
- Coding Efficiency Comparison
- Entropy Bound Verification
- Kraft Inequality Verification
- Automatic Huffman Tree Generation
- Automatic Shannon-Fano Tree Generation

---

## Repository Structure

```
source-coding-algorithms/

├── src/
│   ├── Final.py
│   ├── Huffman.py
│   ├── Fano.py
│   └── Shannon.py
│
├── docs/
│   └── report.pdf
│
├── results/
│   ├── huffman_tree.png
│   └── fano_tree.png
│
├── README.md
├── LICENSE
└── requirements.txt
```

---

## Source Files

| File | Description |
|------|-------------|
| Final.py | Unified implementation comparing all source coding algorithms |
| Huffman.py | D-ary Huffman Coding implementation |
| Fano.py | D-ary Shannon-Fano Coding implementation |
| Shannon.py | Shannon and Shannon-type Coding implementation |

---

## Results

The implementation computes and compares

- Entropy
- Expected code length
- Coding efficiency
- Entropy bounds
- Kraft inequality

It also supports

- Huffman decoding
- Graphical Huffman tree generation
- Graphical Shannon-Fano tree generation

---

## Concepts Implemented

- D-ary Huffman Coding
- D-ary Shannon-Fano Coding
- Shannon Coding
- Shannon-type Coding
- Source Entropy
- Kraft Inequality
- Prefix-Free Codes
- Source Coding Efficiency

---

## Tools Used

- Python
- Graphviz
- Heap Queue (heapq)

---

## Future Improvements

Possible extensions include

- Arithmetic Coding
- Adaptive Huffman Coding
- Adaptive Arithmetic Coding
- Lempel-Ziv Compression
- Compression Ratio Analysis
- GUI-based Code Visualizer

---

## License

MIT License
