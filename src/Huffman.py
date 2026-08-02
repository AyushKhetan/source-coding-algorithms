import heapq
import math


# ---------------------------------
# Node Definition
# ---------------------------------
class Node:
    def __init__(self, value, index=None):
        self.value = value          # probability
        self.index = index          # symbol index (None for internal nodes)
        self.parent = None
        self.code_letter = None
        self.children = []

    def __lt__(self, other):
        return self.value < other.value


# ---------------------------------
# Build Huffman Tree
# ---------------------------------
def build_huffman(probabilities, D):

    heap = []
    leaf_nodes = []

    # Create initial leaf nodes
    for i, prob in enumerate(probabilities):
        node = Node(prob, i)
        heapq.heappush(heap, node)
        leaf_nodes.append(node)

    n = len(heap)

    # Padding condition
    if D > 1:
        remainder = (n - 1) % (D - 1)

        if remainder != 0:
            m = (D - 1) - remainder
            for _ in range(m):
                dummy = Node(0)  # No index
                heapq.heappush(heap, dummy)
                leaf_nodes.append(dummy)

    # Special case: single symbol
    if len(heap) == 1:
        single = heap[0]
        single.code_letter = "0"
        return single, leaf_nodes

    # Build tree
    while len(heap) > 1:

        smallest_nodes = []

        for _ in range(D):
            smallest_nodes.append(heapq.heappop(heap))

        total_prob = sum(node.value for node in smallest_nodes)
        parent = Node(total_prob)

        for index, node in enumerate(smallest_nodes):
            node.parent = parent
            node.code_letter = str(index)
            parent.children.append(node)

        heapq.heappush(heap, parent)

    root = heap[0]
    return root, leaf_nodes


# ---------------------------------
# Generate Codes (Leaf → Root)
# ---------------------------------
def generate_codes(leaf_nodes):

    codebook = {}

    for node in leaf_nodes:

        # Skip dummy nodes
        if node.index is None:
            continue

        current = node
        code = ""

        while current.parent is not None:
            code = current.code_letter + code
            current = current.parent

        if code == "":
            code = "0"

        codebook[node.index] = code

    return codebook


# ---------------------------------
# Entropy
# ---------------------------------
def entropy(probabilities, D):
    return -sum(p * math.log(p, D) for p in probabilities if p > 0)


# ---------------------------------
# Expected Length
# ---------------------------------
def expected_length(codebook, probabilities):
    return sum(probabilities[i] * len(codebook[i])
               for i in codebook)


# ---------------------------------
# Decode (Tree Traversal)
# ---------------------------------
def decode(encoded_string, root):

    decoded_output = []
    current = root

    for digit in encoded_string:

        current = current.children[int(digit)]

        if current.index is not None:
            decoded_output.append(current.index)
            current = root

    return decoded_output


# ---------------------------------
# MAIN PROGRAM
# ---------------------------------
if __name__ == "__main__":

    print("\n--- D-ary Huffman Coding Program ---\n")

    D = int(input("Enter value of D (2 for binary, 3 for ternary, etc.): "))
    n = int(input("Enter number of symbols: "))

    probabilities = []

    print("\nEnter probabilities (must sum to 1):")

    for i in range(n):
        p = float(input(f"Probability p{i}: "))
        probabilities.append(p)

    if abs(sum(probabilities) - 1.0) > 1e-6:
        print("\nWarning: Probabilities do not sum to 1.\n")

    root, leaf_nodes = build_huffman(probabilities, D)
    codebook = generate_codes(leaf_nodes)

    print("\n--- Huffman Codes ---")
    print("Index\tProbability\tCode\tLength")

    for i in sorted(codebook):
        print(f"S{i}\t{probabilities[i]:.4f}\t\t{codebook[i]}\t{len(codebook[i])}")

    H = entropy(probabilities, D)
    L = expected_length(codebook, probabilities)
    efficiency = H / L

    print("\n--- Performance ---")
    print(f"Entropy (base {D}) = {H:.4f}")
    print(f"Expected Length = {L:.4f}")
    print(f"Efficiency = {efficiency:.4f}")

    # Decoding Test
    test = input("\nEnter encoded string to decode (or press Enter to skip): ")

    if test.strip() != "":
        decoded = decode(test, root)
        print("Decoded symbol indices:", decoded)