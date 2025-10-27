from playfair_cypher import playfair_encrypt, playfair_decrypt, create_playfair_matrix, print_matrix, prepare_text, find_position

def separator(title=""):
    if title:
        print("\n" + "=" * 75)
        print(f"  {title}")
        print("=" * 75)
    else:
        print("-" * 75)

def test_rule(rule_num, rule_name, message, key, description):
    print(f"\nREGULA {rule_num}: {rule_name}")
    print(f"   {description}")
    separator()
    
    # Prepare and encrypt
    prepared = prepare_text(message)
    encrypted = playfair_encrypt(message, key)
    decrypted = playfair_decrypt(encrypted, key)
    
    print(f"Mesaj original:  '{message}'")
    print(f"Mesaj preparat:  '{prepared}'")
    
    # Show first pair details
    if len(prepared) >= 2:
        matrix = create_playfair_matrix(key)
        char1, char2 = prepared[0], prepared[1]
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        print(f"\nPrima pereche:   '{char1}{char2}'")
        print(f"  → '{char1}' la poziția [linie {row1}, coloană {col1}]")
        print(f"  → '{char2}' la poziția [linie {row2}, coloană {col2}]")
        
        if row1 == row2:
            print(f"  → ACEEAȘI LINIE → shift dreapta")
        elif col1 == col2:
            print(f"  → ACEEAȘI COLOANĂ → shift jos")
        else:
            print(f"  → DREPTUNGHI → schimb colțuri")
    
    print(f"\nCriptogramă:     '{encrypted}'")
    print(f"Decriptat:       '{decrypted}'")
    
    # Verification
    if decrypted == prepared:
        print("Status:          CORECT (criptare/decriptare reversibilă)")
    else:
        print("Status:          EROARE")
    
    return decrypted == prepared


# =============================================================================
# START TESTE
# =============================================================================

separator("TEST CIFRUL PLAYFAIR - LIMBA ROMÂNĂ (31 litere)")
print("\nCheia folosită pentru toate testele: 'CRIPTOGRAFIE'")
print("Matrice 5×6 (30 poziții, J → I)\n")

key = "CRIPTOGRAFIE"
matrix = create_playfair_matrix(key)
print_matrix(matrix)

print("\n" + "=" * 75)
print("  DEMONSTRAREA CELOR 3 REGULI PLAYFAIR")
print("=" * 75)

all_tests_passed = True

# =============================================================================
# REGULA 1: Same Row - Litere pe aceeași linie
# =============================================================================
# Need to find two letters on the same row in the matrix
# Let's use letters from the first row
letter1 = matrix[0][0]  # First letter in row 0
letter2 = matrix[0][2]  # Third letter in row 0
test_message1 = f"{letter1}{letter2}AB"

result1 = test_rule(
    1,
    "Litere pe ACEEAȘI LINIE (Same Row)",
    test_message1,
    key,
    "Când două litere sunt pe aceeași linie:\n" +
    "   • Criptare: fiecare literă se mută la DREAPTA (cu wrap-around)\n" +
    "   • Decriptare: fiecare literă se mută la STÂNGA"
)
all_tests_passed = all_tests_passed and result1

# =============================================================================
# REGULA 2: Same Column - Litere pe aceeași coloană
# =============================================================================
# Find two letters in the same column
letter3 = matrix[0][0]  # First column, row 0
letter4 = matrix[2][0]  # First column, row 2
test_message2 = f"{letter3}{letter4}AB"

result2 = test_rule(
    2,
    "Litere pe ACEEAȘI COLOANĂ (Same Column)",
    test_message2,
    key,
    "Când două litere sunt pe aceeași coloană:\n" +
    "   • Criptare: fiecare literă se mută în JOS (cu wrap-around)\n" +
    "   • Decriptare: fiecare literă se mută în SUS"
)
all_tests_passed = all_tests_passed and result2

# =============================================================================
# REGULA 3: Rectangle - Litere formând dreptunghi
# =============================================================================
result3 = test_rule(
    3,
    "Litere formând DREPTUNGHI (Rectangle)",
    "MASA",
    key,
    "Când două litere sunt pe linii și coloane diferite:\n" +
    "   • Se schimbă coloanele (fiecare literă ia coloana celeilalte)\n" +
    "   • Aceeași regulă pentru criptare și decriptare"
)
all_tests_passed = all_tests_passed and result3

# =============================================================================
# REGULI SPECIALE
# =============================================================================

separator("REGULI SPECIALE DE PRELUCRARE")

# =============================================================================
# REGULA 4: Repeating Letters - Litere repetate
# =============================================================================
result4 = test_rule(
    4,
    "Litere REPETATE (Repeating Letters)",
    "ALLEE",
    key,
    "Când două litere identice apar consecutiv:\n" +
    "   • Se inserează 'X' între ele pentru a le separa\n" +
    "   • Exemplu: 'LL' devine 'LXL', 'EE' devine 'EXE'"
)
all_tests_passed = all_tests_passed and result4

# =============================================================================
# REGULA 5: Odd Length - Lungime impară
# =============================================================================
result5 = test_rule(
    5,
    "Lungime IMPARĂ (Odd Length Padding)",
    "ROMAN",
    key,
    "Când mesajul are un număr impar de litere:\n" +
    "   • Se adaugă 'X' la final pentru a completa ultima pereche\n" +
    "   • Exemplu: 'ROMAN' (5 litere) devine 'ROMANX' (6 litere)"
)
all_tests_passed = all_tests_passed and result5

# =============================================================================
# REGULA 6: J → I Replacement
# =============================================================================
result6 = test_rule(
    6,
    "Înlocuire J → I (Traditional Playfair)",
    "JURNAL",
    key,
    "Toate literele 'J' sunt înlocuite cu 'I':\n" +
    "   • Reduce alfabetul de la 31 la 30 litere\n" +
    "   • Permite crearea matricei 5×6\n" +
    "   • Regulă tradițională Playfair"
)
all_tests_passed = all_tests_passed and result6

separator("TESTE COMPLEXE - LIMBA ROMÂNĂ")

# =============================================================================
# TEST 7: Romanian diacritics
# =============================================================================
result7 = test_rule(
    7,
    "DIACRITICE ROMÂNEȘTI (Ă, Â, Î, Ș, Ț)",
    "ȘCOALĂ ȘI ȘTIINȚĂ",
    key,
    "Suport complet UTF-8 pentru toate diacriticele românești:\n" +
    "   • Ă, Â, Î, Ș, Ț sunt procesate corect\n" +
    "   • Nu se face normalizare ASCII"
)
all_tests_passed = all_tests_passed and result7

# =============================================================================
# TEST 8: Long text with all rules
# =============================================================================
result8 = test_rule(
    8,
    "TEXT LUNG cu TOATE REGULILE",
    "ACEASTA ESTE O PROPOZIȚIE ÎN LIMBA ROMÂNĂ",
    key,
    "Text complex care combină:\n" +
    "   • Litere repetate\n" +
    "   • Diacritice\n" +
    "   • Lungime variată\n" +
    "   • Toate cele 3 reguli Playfair"
)
all_tests_passed = all_tests_passed and result8

# =============================================================================
# TEST 9: Mix of J and special cases
# =============================================================================
result9 = test_rule(
    9,
    "COMBINAȚIE J + LITERE DUBLE",
    "JOJO SI JAZZ",
    key,
    "Combină mai multe reguli:\n" +
    "   • J → I (toate J-urile devin I)\n" +
    "   • Litere duble (JJ, ZZ)\n" +
    "   • X inserat între ele"
)
all_tests_passed = all_tests_passed and result9

# =============================================================================
# VERIFICARE RECIPROCITATE
# =============================================================================

separator("VERIFICARE RECIPROCITATE")

print("\nTestare reciprocitate: Encrypt(Decrypt(text)) = text\n")
test_messages = [
    "BUNĂ ZIUA",
    "COMPUTERE ȘI REȚELE",
    "JURNAL DE JOCURI",
    "MATEMATICĂ APPLIED",
    "SECURITATE CIBERNETICĂ"
]

reciprocity_passed = True
for i, msg in enumerate(test_messages, 1):
    encrypted = playfair_encrypt(msg, key)
    decrypted = playfair_decrypt(encrypted, key)
    prepared = prepare_text(msg)
    
    status = "v" if decrypted == prepared else "X"
    if decrypted != prepared:
        reciprocity_passed = False
    
    print(f"{status} Test {i}: '{msg}'")
    print(f"   Criptat: {encrypted}")
    print(f"   Decriptat: {decrypted}\n")

all_tests_passed = all_tests_passed and reciprocity_passed
