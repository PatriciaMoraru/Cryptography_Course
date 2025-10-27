# Romanian alphabet: 31 letters with diacritics
# A Ă Â B C D E F G H I Î J K L M N O P Q R S Ș T Ț U V W X Y Z
# For 5x6 matrix (30 positions), we replace J with I (traditional Playfair approach)

ROMANIAN_ALPHABET = "AĂÂBCDEFGHIÎKLMNOPQRSȘTȚUVWXYZ"  # J is replaced with I (30 letters)

def normalize_romanian_char(char):
    char = char.upper()
    if char == 'J':
        return 'I'
    return char


def validate_input_text(text):
    for char in text:
        if char.isspace():
            continue
        # Check if character is a valid Romanian letter (with diacritics preserved)
        normalized = char.upper()
        if normalized not in ROMANIAN_ALPHABET and normalized != 'J':
            return False, f"Caracterul '{char}' nu este valid. Folosiți doar litere românești: A-Z, Ă, Â, Î, Ș, Ț (majuscule sau minuscule)"
    return True, ""


def validate_key(key):
    if len(key) < 7:
        return False, f"Cheia trebuie să conțină cel puțin 7 caractere. Lungimea actuală: {len(key)}"
    
    is_valid, error = validate_input_text(key)
    if not is_valid:
        return False, error
    
    return True, ""


def create_playfair_matrix(key):
    normalized_key = ""
    for char in key.upper():
        if char.isalpha():
            normalized_key += normalize_romanian_char(char)
    
    alphabet = ROMANIAN_ALPHABET
    
    key_string = normalized_key + alphabet
    
    seen = set()
    unique_key = ""
    for char in key_string:
        if char not in seen:
            seen.add(char)
            unique_key += char
    
    # Create 5x6 matrix (5 rows, 6 columns = 30 positions)
    matrix = []
    for i in range(5):
        row = [unique_key[i * 6 + j] for j in range(6)]
        matrix.append(row)
    
    return matrix


def print_matrix(matrix):
    print("\nMatricea Playfair:")
    for row in matrix:
        print(" ".join(row))
    print()


def find_position(matrix, char):
    char = normalize_romanian_char(char)
    for i in range(5):
        for j in range(6):
            if matrix[i][j] == char:
                return i, j
    return None, None


def prepare_text(text):
    prepared = ""
    for char in text.upper():
        if char.isalpha():
            prepared += normalize_romanian_char(char)
    
    result = ""
    i = 0
    while i < len(prepared):
        result += prepared[i]
        if i + 1 < len(prepared) and prepared[i] == prepared[i + 1]:
            result += 'X'
        i += 1
    
    # Add 'X' if odd length
    if len(result) % 2 == 1:
        result += 'X'
    
    return result


def playfair_encrypt(message, key):
    matrix = create_playfair_matrix(key)
    prepared_message = prepare_text(message)
    ciphertext = ""
    
    # Process each digraph (pair of letters)
    for i in range(0, len(prepared_message), 2):
        char1 = prepared_message[i]
        char2 = prepared_message[i + 1]
        
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        if row1 == row2:  # Same row
            # Move right, wrap around with modulo 6 (6 columns)
            ciphertext += matrix[row1][(col1 + 1) % 6]
            ciphertext += matrix[row2][(col2 + 1) % 6]
        elif col1 == col2:  # Same column
            # Move down, wrap around with modulo 5 (5 rows)
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else:  # Rectangle
            # Swap columns
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]
    
    return ciphertext


def playfair_decrypt(ciphertext, key):
    matrix = create_playfair_matrix(key)
    ciphertext = "".join(ciphertext.upper().split())
    plaintext = ""
    
    # Process each digraph (pair of letters)
    for i in range(0, len(ciphertext), 2):
        char1 = normalize_romanian_char(ciphertext[i])
        char2 = normalize_romanian_char(ciphertext[i + 1])
        
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        if row1 == row2:  # Same row
            # Move left, wrap around with modulo 6 (6 columns)
            plaintext += matrix[row1][(col1 - 1) % 6]
            plaintext += matrix[row2][(col2 - 1) % 6]
        elif col1 == col2:  # Same column
            # Move up, wrap around with modulo 5 (5 rows)
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:  # Rectangle
            # Swap columns
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]
    
    return plaintext


def main():
    print("=" * 60)
    print("CIFRUL PLAYFAIR PENTRU LIMBA ROMÂNĂ (31 de litere)")
    print("Suport complet UTF-8 pentru diacritice")
    print("=" * 60)
    print("\nMatricea: 5x6 (litera J este înlocuită cu I)")
    print("Alfabetul: A Ă Â B C D E F G H I Î K L M N O P Q R S Ș T Ț U V W X Y Z")
    print("Notă: J -> I (conform regulilor tradiționale Playfair)")
    print("=" * 60)
    
    while True:
        print("\nAlegeți operația:")
        print("1. Criptare")
        print("2. Decriptare")
        print("3. Ieșire")
        
        choice = input("\nIntroduceți opțiunea (1/2/3): ").strip()
        
        if choice == '3':
            print("\nLa revedere!")
            break
        
        if choice not in ['1', '2']:
            print("Opțiune invalidă! Alegeți 1, 2 sau 3.")
            continue
        
        # Get and validate key
        while True:
            key = input("\nIntroduceți cheia (minim 7 caractere): ").strip()
            is_valid, error_msg = validate_key(key)
            if is_valid:
                break
            print(f"Eroare: {error_msg}")
        
        # Show matrix
        matrix = create_playfair_matrix(key)
        print_matrix(matrix)
        
        if choice == '1':  # Encryption
            while True:
                message = input("Introduceți mesajul pentru criptare: ").strip()
                if not message:
                    print("Mesajul nu poate fi gol!")
                    continue
                is_valid, error_msg = validate_input_text(message)
                if is_valid:
                    break
                print(f"Eroare: {error_msg}")
            
            ciphertext = playfair_encrypt(message, key)
            print(f"\nMesaj original: {message}")
            print(f"Mesaj preparat: {prepare_text(message)}")
            print(f"Criptogramă: {ciphertext}")
            
        else:  # Decryption
            while True:
                ciphertext = input("Introduceți criptograma pentru decriptare: ").strip()
                if not ciphertext:
                    print("Criptograma nu poate fi goală!")
                    continue
                is_valid, error_msg = validate_input_text(ciphertext)
                if is_valid:
                    break
                print(f"Eroare: {error_msg}")
            
            plaintext = playfair_decrypt(ciphertext, key)
            print(f"\nCriptogramă: {ciphertext}")
            print(f"Mesaj decriptat: {plaintext}")
            print("\nNotă: Adăugați manual spațiile în funcție de logica mesajului.")


if __name__ == "__main__":
    main()