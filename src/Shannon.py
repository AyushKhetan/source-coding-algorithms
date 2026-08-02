import math
import heapq

# =====================================================
# ------------------ COMMON UTILITIES -----------------
# =====================================================

def entropy(symbols, base):
    H = 0
    for p in symbols.values():
        if p > 0:
            H -= p * math.log(p, base)
    return H


def expected_length(symbols, codebook):
    return sum(symbols[s] * len(codebook[s]) for s in symbols)


# =====================================================
# -------------------- HUFFMAN ------------------------
# =====================================================

class HuffmanNode:
    def __init__(self, prob, symbol=None):
        self.prob = prob
        self.symbol = symbol
        self.children = []

    def __lt__(self, other):
        return self.prob < other.prob


def huffman(symbols, D):
    heap = []

    for s, p in symbols.items():
        heapq.heappush(heap, HuffmanNode(p, s))

    n = len(heap)
    if D > 1:
        remainder = (n - 1) % (D - 1)
        if remainder != 0:
            needed = (D - 1) - remainder
            for i in range(needed):
                heapq.heappush(heap, HuffmanNode(0, f"dummy{i}"))

    while len(heap) > 1:
        smallest = []
        for _ in range(D):
            if heap:
                smallest.append(heapq.heappop(heap))

        new_node = HuffmanNode(sum(n.prob for n in smallest))
        new_node.children = smallest
        heapq.heappush(heap, new_node)

    root = heap[0]
    return root


def generate_codes_tree(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node.symbol is not None and not node.symbol.startswith("dummy"):
        codebook[node.symbol] = prefix
        return codebook

    for i, child in enumerate(node.children):
        generate_codes_tree(child, prefix + str(i), codebook)

    return codebook


# =====================================================
# ----------------- SHANNON-FANO ----------------------
# =====================================================

class FanoNode:
    def __init__(self, value, symbol=None):
        self.value = value
        self.symbol = symbol
        self.children = []


def split_into_d_groups(symbol_list, D):
    groups = []
    remaining = symbol_list.copy()
    remaining_groups = D

    while remaining_groups > 1 and remaining:
        total = sum(p for _, p in remaining)
        target = total / remaining_groups

        current_group = []
        current_sum = 0
        i = 0

        while i < len(remaining):
            symbol, prob = remaining[i]
            if current_sum + prob <= target:
                current_group.append((symbol, prob))
                current_sum += prob
                i += 1
            else:
                if abs((current_sum + prob) - target) < abs(current_sum - target):
                    current_group.append((symbol, prob))
                    i += 1
                break

        if not current_group:
            current_group.append(remaining[0])
            i = 1

        groups.append(current_group)
        remaining = remaining[i:]
        remaining_groups -= 1

    if remaining:
        groups.append(remaining)

    while len(groups) < D:
        groups.append([])

    return groups


def build_fano(symbol_list, D):
    total = sum(p for _, p in symbol_list)
    node = FanoNode(total)

    if len(symbol_list) == 1:
        node.symbol = symbol_list[0][0]
        return node

    groups = split_into_d_groups(symbol_list, D)

    for group in groups:
        if group:
            child = build_fano(group, D)
            node.children.append(child)

    return node


# =====================================================
# --------------------- SHANNON -----------------------
# =====================================================

def shannon(symbols, D):
    sorted_symbols = sorted(symbols.items(), key=lambda x: x[1], reverse=True)

    codebook = {}
    cumulative = 0

    for s, p in sorted_symbols:
        Li = math.ceil(-math.log(p, D))

        Fi = cumulative
        Ci = ""
        temp = Fi

        for _ in range(Li):
            temp *= D
            digit = int(temp + 1e-12)
            Ci += str(digit)
            temp -= digit

        codebook[s] = Ci
        cumulative += p

    return codebook


# =====================================================
# ---------------------- DECODE -----------------------
# =====================================================

def decode(encoded, root):
    decoded = []
    current = root

    for digit in encoded:
        current = current.children[int(digit)]
        if current.symbol is not None:
            decoded.append(current.symbol)
            current = root

    return decoded


# =====================================================
# ------------------------ MAIN -----------------------
# =====================================================

if __name__ == "__main__":

    print("\n=== Unified D-ary Coding Comparison ===")

    D = int(input("Enter D (2=Binary, 3=Ternary, ...): "))
    n = int(input("Enter number of symbols: "))

    symbols = {}
    print("\nEnter probabilities (must sum to 1):")
    for i in range(n):
        p = float(input(f"Probability S{i}: "))
        symbols[f"S{i}"] = p

    H = entropy(symbols, D)

    # Huffman
    h_root = huffman(symbols, D)
    h_codes = generate_codes_tree(h_root)
    L_h = expected_length(symbols, h_codes)

    # Fano
    sorted_symbols = sorted(symbols.items(), key=lambda x: x[1], reverse=True)
    f_root = build_fano(sorted_symbols, D)
    f_codes = generate_codes_tree(f_root)
    L_f = expected_length(symbols, f_codes)

    # Shannon
    s_codes = shannon(symbols, D)
    L_s = expected_length(symbols, s_codes)

    print("\n--- Results ---")

    
    print("\n--- Huffman Codes ---")
    for s in sorted(symbols):
        print(f"{s}: {h_codes[s]}")

    print("\n--- Shannon-Fano Codes ---")
    for s in sorted(symbols):
        print(f"{s}: {f_codes[s]}")

    print("\n--- Shannon Codes ---")
    for s in sorted(symbols):
        print(f"{s}: {s_codes[s]}")
        
    print(f"Entropy (base {D}) = {H:.4f}\n")

    print("Method\t\tExpected Length\tEfficiency")
    print(f"Huffman\t\t{L_h:.4f}\t\t{H/L_h:.4f}")
    print(f"Shannon-Fano\t{L_f:.4f}\t\t{H/L_f:.4f}")
    print(f"Shannon\t\t{L_s:.4f}\t\t{H/L_s:.4f}")