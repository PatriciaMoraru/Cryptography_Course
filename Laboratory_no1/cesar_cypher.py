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


def cesar_encrypt(text, key):
    encrypted_text = []

    for chr in text:
        idx = alphabet_upp.index(chr)
        new_index = (idx + key) % len(alphabet_upp)
        encrypted_text.append((alphabet_upp[new_index]))
    return ''.join(encrypted_text)

def cesar_decrypt(text, key):
    decrypted_text = []

    for ch in text:
        idx = alphabet_upp.index(ch)
        new_idx = (idx - key) % len(alphabet_upp)
        decrypted_text.append(alphabet_upp[new_idx])
    return ''.join(decrypted_text)

def read_key():
    key_input = input("Enter the key (1-25): ")

    if not key_input.isdigit():
        print("Error: Key must be a number between 1 and 25!")
        return None

    key = int(key_input)

    if not (1 <= key <= 25):
        print("Error: Key must be between 1 and 25!")
        return None

    return key

def main():
    while True:
        choice = input("Choose operation (encrypt/decrypt/exit): ").strip().lower()

        if choice == "exit":
            print("Goodbye!")
            break

        elif choice in ["encrypt", "decrypt"]:
            text = input("Enter the text (for decrypt enter the cryptogram): ").strip()
            norm, err = normalize_text(text)

            if err:
                print(err)
                continue

            key = read_key()
            if key is None:
                continue

            if choice == "encrypt":
                cryptogram = cesar_encrypt(norm, key)
                print("Encrypted text:", cryptogram)
            else:
                message = cesar_decrypt(norm, key)
                print("Decrypted text:", message)

        else:
            print("Invalid choice. Please chose type 'encrypt', 'decrypt' or 'exit'.")

if __name__ == "__main__":
    main()