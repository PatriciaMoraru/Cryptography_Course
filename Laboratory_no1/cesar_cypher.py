alphabet_low = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alphabet_upp = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def normalize_text(text):
    result = []
    for chr in text:
        if chr == ' ':
            continue
        if chr in alphabet_upp:
            result.append(chr)
        elif chr in alphabet_low:
            idx = alphabet_low.index(chr)
            result.append(alphabet_upp[idx])
        else:
            return None, "Error: Text must contain only A–Z or a–z letters. Spaces are allowed."
    if not result:
        return None, "Error: Text cannot be empty."
    return ''.join(result), None

def read_key():
    key_input = input("Enter the numeric key k1 (1-25): ")
    if not key_input.isdigit():
        print("Error: Key must be a number between 1 and 25!")
        return None
    key = int(key_input)
    if not (1 <= key <= 25):
        print("Error: Key must be between 1 and 25!")
        return None
    return key

def read_key2_or_none(mode):
    if mode == "simple":
        return None
    key2 = input("Enter the text key k2 (only letters, length >= 7): ").strip()
    if len(key2) < 7:
        print("Error: Key2 must have at least 7 letters.")
        return None
    up_chars = []
    for chr in key2:
        if chr in alphabet_upp:
            up = chr
        elif chr in alphabet_low:
            up = alphabet_upp[alphabet_low.index(chr)]
        else:
            print("Error: key2 must contain only Latin letters.")
            return None
        if up not in up_chars:  # keep first occurrence only
            up_chars.append(up)
    return ''.join(up_chars)

def build_alphabet(key2_up_or_none):
    if key2_up_or_none is None:
        return alphabet_upp[:]  # simple Caesar
    perm = list(key2_up_or_none)
    for chr in alphabet_upp:
        if chr not in perm:
            perm.append(chr)
    return perm
def cesar_encrypt(text, key, alph):
    encrypted_text = []
    for chr in text:
        idx = alph.index(chr)
        new_index = (idx + key) % len(alph)
        encrypted_text.append(alph[new_index])
    return ''.join(encrypted_text)

def cesar_decrypt(text, key, alph):
    decrypted_text = []
    for chr in text:
        idx = alph.index(chr)
        new_idx = (idx - key) % len(alph)
        decrypted_text.append(alph[new_idx])
    return ''.join(decrypted_text)

def main():
    while True:
        version = input("Choose version (simple/two/exit): ").strip().lower()
        if version == "exit":
            print("Goodbye!")
            break
        if version not in ["simple", "two"]:
            print("Invalid choice. Please choose 'simple', 'two' or 'exit'.")
            continue

        choice = input("Choose operation (encrypt/decrypt): ").strip().lower()
        if choice not in ["encrypt", "decrypt"]:
            print("Invalid choice. Please choose 'encrypt' or 'decrypt'.")
            continue

        text = input("Enter the text (for decrypt enter the cryptogram): ").strip()
        norm, err = normalize_text(text)
        if err:
            print(err)
            continue

        key = read_key()
        if key is None:
            continue

        key2_up = read_key2_or_none("simple" if version == "simple" else "two")
        if version == "two" and key2_up is None:
            continue

        alph = build_alphabet(key2_up)

        if choice == "encrypt":
            cryptogram = cesar_encrypt(norm, key, alph)
            print("Encrypted text:", cryptogram)
        else:
            message = cesar_decrypt(norm, key, alph)
            print("Decrypted text:", message)

if __name__ == "__main__":
    main()