from collections import Counter

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


def normalizar_mod191(texto):
    texto = quitar_tildes(texto)
    return texto.replace('ñ', 'n')


def vigenere_cifrar(texto_claro, clave, modulo=27):
    alfabeto = obtener_alfabeto(modulo)
    n = len(alfabeto)

    if modulo == 27:
        texto_claro = normalizar_mod27(texto_claro)
        clave = normalizar_mod27(clave)
    else:
        texto_claro = normalizar_mod191(texto_claro)
        clave = normalizar_mod191(clave)

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


def vigenere_descifrar(texto_cifrado, clave, modulo=27):
    alfabeto = obtener_alfabeto(modulo)
    n = len(alfabeto)

    if modulo == 27:
        clave = normalizar_mod27(clave)
    else:
        clave = normalizar_mod191(clave)

    resultado = []
    for i, c in enumerate(texto_cifrado):
        k = clave[i % len(clave)]
        ci = alfabeto.index(c)
        ki = alfabeto.index(k)
        mi = (ci - ki) % n
        resultado.append(alfabeto[mi])
    return ''.join(resultado)

def frecuencias(texto, modulo=27):
    alfabeto = obtener_alfabeto(modulo)
    conteo = Counter(texto)
    return [(c, conteo.get(c, 0)) for c in alfabeto]


def mostrar_frecuencias(titulo, texto, modulo=27, solo_presentes=True):
    print(f"\n--- {titulo} ---")
    for letra, cant in frecuencias(texto, modulo):
        if solo_presentes and cant == 0:
            continue
        print(f"{letra!r:>5}: {cant:4d}")

TEXTO = (
    "Creer que es posible es el paso número uno hacia el éxito. "
    "Despertarse y pensar en algo positivo puede cambiar el transcurso "
    "de todo el día. No eres lo suficientemente viejo como para no "
    "iniciar un nuevo camino hacia tus sueños. Levántate cada mañana "
    "creyendo que vas a vivir el mejor día de tu vida."
)
CLAVE1 = "POSITIVO"
CLAVE2 = "HIELO"
CLAVE3 = "MAR"

def interfaz_cifrado():
    print("=== Cifrador de Vigenere ===")
    modulo = int(input("Módulo (27 o 191): ").strip())

    cifrado_1 = vigenere_cifrar(TEXTO, CLAVE1, modulo)
    cifrado_2 = vigenere_cifrar(TEXTO, CLAVE2, modulo)
    cifrado_3 = vigenere_cifrar(TEXTO, CLAVE3, modulo)
    print("\nTexto cifrado:")
    print("Clave POSITIVO")
    print(cifrado_1)
    print("Clave HIELO")
    print(cifrado_2)
    print("Clave MAR")
    print(cifrado_3)
    original = normalizar_mod27(TEXTO) if modulo == 27 else normalizar_mod191(TEXTO)
    mostrar_frecuencias("Texto original", original, modulo)
    mostrar_frecuencias("Cifrado con POSITIVO", cifrado_1, modulo)
    mostrar_frecuencias("Cifrado con HIELO", cifrado_2, modulo)
    mostrar_frecuencias("Cifrado con MAR", cifrado_3, modulo)


if __name__ == "__main__":
    interfaz_cifrado()
    