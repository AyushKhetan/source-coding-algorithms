import math


# -------------------------------
# Node Class
# -------------------------------

class Node:
    def __init__(self, value, symbol=None):
        self.value = value
        self.symbol = symbol
        self.children = []


# -------------------------------
# Correct D-ary Splitting
# -------------------------------

def split_into_d_groups(symbol_list, D):
    """
    symbol_list: sorted list of (symbol, prob) in descending order
    Returns exactly D groups (some may be empty if D > len(symbol_list))
    """

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
                # Decide whether to include this symbol
                if abs((current_sum + prob) - target) < abs(current_sum - target):
                    current_group.append((symbol, prob))
                    i += 1
                break

        if not current_group:
            # Edge case: largest symbol itself exceeds target
            current_group.append(remaining[0])
            i = 1

        groups.append(current_group)
        remaining = remaining[i:]
        remaining_groups -= 1

    # Last group gets everything remaining
    if remaining:
        groups.append(remaining)

    # If fewer than D groups (when symbols < D)
    while len(groups) < D:
        groups.append([])

    return groups


# -------------------------------
# Recursive Tree Builder
# -------------------------------

def build_shannon_fano_tree(symbol_list, D):
    total_prob = sum(p for _, p in symbol_list)
    node = Node(total_prob)

    # Base case
    if len(symbol_list) == 1:
        node.symbol = symbol_list[0][0]
        return node

    groups = split_into_d_groups(symbol_list, D)

    for group in groups:
        if group:
            child = build_shannon_fano_tree(group, D)
            node.children.append(child)

    return node


# -------------------------------
# Code Generation
# -------------------------------

def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node.symbol is not None:
        codebook[node.symbol] = prefix
        return codebook

    for i, child in enumerate(node.children):
        generate_codes(child, prefix + str(i), codebook)

    return codebook


# -------------------------------
# Decoding
# -------------------------------

def decode(encoded_string, root):
    decoded = []
    current = root

    for digit in encoded_string:
        current = current.children[int(digit)]
        if current.symbol is not None:
            decoded.append(current.symbol)
            current = root

    return decoded


# -------------------------------
# Entropy
# -------------------------------

def entropy(symbols, base):
    H = 0
    for p in symbols.values():
        if p > 0:
            H -= p * math.log(p, base)
    return H


# -------------------------------
# Expected Length
# -------------------------------

def expected_length(symbols, codebook):
    return sum(symbols[s] * len(codebook[s]) for s in symbols)


# -------------------------------
# Main Program
# -------------------------------

if __name__ == "__main__":

    print("--- D-ary Shannon-Fano Coding Program ---")

    D = int(input("Enter value of D (2 for binary, 3 for ternary, etc.): "))
    n = int(input("Enter number of symbols: "))

    symbols = {}
    print("\nEnter probabilities (must sum to 1):")
    for i in range(n):
        p = float(input(f"Probability S{i}: "))
        symbols[f"S{i}"] = p

    # Sort descending
    sorted_symbols = sorted(symbols.items(), key=lambda x: x[1], reverse=True)

    # Build tree
    root = build_shannon_fano_tree(sorted_symbols, D)

    # Generate codes
    codebook = generate_codes(root)

    print("\n--- Shannon-Fano Codes ---")
    print("Index\tProbability\tCode\tLength")
    for symbol, prob in sorted_symbols:
        code = codebook[symbol]
        print(f"{symbol}\t{prob:.4f}\t\t{code}\t{len(code)}")

    # Performance
    H = entropy(symbols, D)
    L = expected_length(symbols, codebook)
    efficiency = H / L

    print("\n--- Performance ---")
    print(f"Entropy (base {D}) = {H:.4f}")
    print(f"Expected Length = {L:.4f}")
    print(f"Efficiency = {efficiency:.4f}")

    # Decoding
    encoded_string = input("\nEnter encoded string to decode (or press Enter to skip): ")
    if encoded_string:
        decoded = decode(encoded_string, root)
        print("Decoded symbols:", decoded)