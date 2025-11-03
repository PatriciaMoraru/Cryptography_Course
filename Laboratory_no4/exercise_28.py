import random

P_TABLE = [
    16, 7, 20, 21,
    29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
]

def show_p_table():
    print("=== DES P Permutation Table (32 -> 32) ===")
    print()
    print(" 1 | 16  7  20  21")
    print(" 2 | 29  12  28  17")
    print(" 3 |  1  15  23  26")
    print(" 4 |  5  18  31  10")
    print(" 5 |  2   8  24  14")
    print(" 6 | 32  27   3   9")
    print(" 7 | 19  13  30   6")
    print(" 8 | 22  11   4  25")
    print()


def permute_p(bits32):
    """Apply DES P-permutation on a 32-bit string."""
    result = ''
    for i in P_TABLE:
        result += bits32[i - 1]
    return result

def xor_bits(a, b):
    """XOR two equal-length binary strings."""
    result = ''
    for x, y in zip(a, b):
        result += '1' if x != y else '0'
    return result

def rand_bits(n):
    """Generate n random bits as a string."""
    bits = ''
    for _ in range(n):
        bits += random.choice('01')
    return bits

def group4(bits):
    """Group a bitstring by 4 for nicer printing."""
    grouped = ''
    for i in range(0, len(bits), 4):
        grouped += bits[i:i+4] + ' '
    return grouped.strip()

def read_or_random(label, nbits=32):
    while True:
        print("\nDo you want to:")
        print("  1) enter %s manually" % label)
        print("  2) generate %s randomly (%d bits)" % (label, nbits))
        choice = input("Your choice (1/2): ").strip()
        if choice == '1':
            val = input("Enter %s (%d bits, only 0/1): " % (label, nbits)).strip().replace(" ", "")
            if len(val) == nbits and all(c in "01" for c in val):
                return val
            print("Invalid input. Try again.")
        elif choice == '2':
            val = rand_bits(nbits)
            print("%s generated: %s" % (label, group4(val)))
            return val
        else:
            print("Please choose 1 or 2.")

def main():
    print("==============================================")
    print(" DES Task 2.8 — Compute R_k for round k")
    print(" R_k = L_(k-1) XOR P(S-box_output)")
    print("==============================================\n")

    # 0) Show the P permutation table
    show_p_table()

    # 1) Get inputs
    L_prev = read_or_random("L_(k-1)", 32)
    s_out  = read_or_random("S-box output", 32)

    # 2) Apply P to S-box output
    p_out = permute_p(s_out)

    # 3) Compute R_k
    R_k = xor_bits(L_prev, p_out)

    # 4) Display intermediate results
    print("\n================= INPUTS =================")
    print("L_(k-1):       %s" % group4(L_prev))
    print("S-box output:  %s" % group4(s_out))

    print("\n========= STEP 1: Apply P-permutation =========")
    print("We permute the 32-bit S-box output using the P table.")
    print("P(S-box out):  %s" % group4(p_out))

    print("\n========= STEP 2: XOR with L_(k-1) =========")
    print("R_k = L_(k-1) XOR P(S-box out)")
    print("  L_(k-1):     %s" % group4(L_prev))
    print(" XOR P(S):     %s" % group4(p_out))
    print("  " + "-" * 39)
    print("  R_k:         %s" % group4(R_k))

    print("\n================= RESULT =================")
    print("R_k (32 bits): %s" % R_k)
    print("R_k grouped:   %s" % group4(R_k))
    print("\nDone.")

if __name__ == "__main__":
    main()
