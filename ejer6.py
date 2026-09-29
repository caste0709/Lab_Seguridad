CIFRA_6 = "WPIXHVYYOSRTECSZBEEGHUUFWRWTZGRWUFSRIWESSXVOHAIHOHWWHCWHUZOBOZEAOYBMCRLTEYOTI"
CLAVE_6 = "HIELO"
ALFABETO_27 = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
ALFABETO_191 = ''.join(chr(i) for i in range(32, 223))

def obtener_alfabeto(modulo):
    if modulo == 27:
        return ALFABETO_27
    elif modulo == 191:
        return ALFABETO_191
    else:
        raise ValueError("Módulo no soportado. Usa 27 o 191.")

def quitar_tildes(texto):
    reemplazos = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ü': 'U',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u',
    }
    for a, b in reemplazos.items():
        texto = texto.replace(a, b)
    return texto


def normalizar_mod27(texto):
    texto = quitar_tildes(texto).upper()
    return ''.join(c for c in texto if c in ALFABETO_27)

def vigenere_descifrar(texto_cifrado, clave, modulo=27):
    alfabeto = obtener_alfabeto(modulo)
    n = len(alfabeto)
    clave = normalizar_mod27(clave)
    resultado = []
    for i, c in enumerate(texto_cifrado):
        k = clave[i % len(clave)]
        ci = alfabeto.index(c)
        ki = alfabeto.index(k)
        mi = (ci - ki) % n
        resultado.append(alfabeto[mi])
    return ''.join(resultado)

def vigenere_cifrar(texto_claro, clave, modulo=27):
    alfabeto = obtener_alfabeto(modulo)
    n = len(alfabeto)

    texto_claro = normalizar_mod27(texto_claro)
    clave = normalizar_mod27(clave)


    if len(clave) == 0:
        raise ValueError("La clave no puede quedar vacía tras normalizar.")

    resultado = []
    for i, m in enumerate(texto_claro):
        k = clave[i % len(clave)]
        mi = alfabeto.index(m)
        ki = alfabeto.index(k)
        ci = (mi + ki) % n
        resultado.append(alfabeto[ci])
    return ''.join(resultado)

def ejercicio_6():
    cifra = normalizar_mod27(CIFRA_6)
    texto_claro = vigenere_descifrar(cifra, CLAVE_6, 27)
    print("Cifra:      ", cifra)
    print("Clave:      ", CLAVE_6)
    print("Texto claro:", texto_claro)

    recifrado = vigenere_cifrar(texto_claro, CLAVE_6, 27)

ejercicio_6()