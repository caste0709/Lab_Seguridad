ALFABETO_27 = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"


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


def cesar_cifrar(texto_claro, desplazamiento):
    texto_claro = normalizar_mod27(texto_claro)
    n = len(ALFABETO_27)
    resultado = []
    for m in texto_claro:
        mi = ALFABETO_27.index(m)
        ci = (mi + desplazamiento) % n
        resultado.append(ALFABETO_27[ci])
    return ''.join(resultado)


def cesar_descifrar(texto_cifrado, desplazamiento):
    n = len(ALFABETO_27)
    resultado = []
    for c in texto_cifrado:
        ci = ALFABETO_27.index(c)
        mi = (ci - desplazamiento) % n
        resultado.append(ALFABETO_27[mi])
    return ''.join(resultado)


def inverso_modular(a, n):
    a = a % n
    for x in range(1, n):
        if (a * x) % n == 1:
            return x
    raise ValueError(f"{a} no tiene inverso módulo {n} (no son coprimos).")


def afin_cifrar(texto_claro, a, b):
    texto_claro = normalizar_mod27(texto_claro)
    n = len(ALFABETO_27)
    resultado = []
    for m in texto_claro:
        mi = ALFABETO_27.index(m)
        ci = (a * mi + b) % n
        resultado.append(ALFABETO_27[ci])
    return ''.join(resultado)


def afin_descifrar(texto_cifrado, a, b):
    n = len(ALFABETO_27)
    a_inv = inverso_modular(a, n)
    resultado = []
    for c in texto_cifrado:
        ci = ALFABETO_27.index(c)
        mi = (a_inv * (ci - b)) % n
        resultado.append(ALFABETO_27[mi])
    return ''.join(resultado)


TEXTO = (
    "Creer que es posible es el paso número uno hacia el éxito. "
    "Despertarse y pensar en algo positivo puede cambiar el transcurso "
    "de todo el día. No eres lo suficientemente viejo como para no "
    "iniciar un nuevo camino hacia tus sueños. Levántate cada mañana "
    "creyendo que vas a vivir el mejor día de tu vida."
)


if __name__ == "__main__":
    print("=== ACTIVIDAD 4 ===")

    print("\n-- César (desplazamiento = 3) --")
    c_cesar = cesar_cifrar(TEXTO, 3)
    print("Cifrado :", c_cesar)
    print("Verificación:", cesar_descifrar(c_cesar, 3))

    print("\n-- Afín (a=5, b=8) --")
    c_afin = afin_cifrar(TEXTO, a=5, b=8)
    print("Cifrado :", c_afin)
    print("Verificación:", afin_descifrar(c_afin, a=5, b=8))