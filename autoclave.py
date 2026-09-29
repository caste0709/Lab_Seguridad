import re
import unicodedata

ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
N = len(ALFABETO)


def normalizar(texto):
    texto = texto.replace("~N", "Ñ").replace("~n", "ñ")
    texto = texto.upper().replace("Ñ", "\0")
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.replace("\0", "Ñ")
    return re.sub(r"[^A-ZÑ]", "", texto)


def cifrar_autoclave(claro, clave):
    claro, clave = normalizar(claro), normalizar(clave)
    k = [ALFABETO.index(c) for c in clave]
    cifrado = []
    for i, ch in enumerate(claro):
        m = ALFABETO.index(ch)
        cifrado.append(ALFABETO[(m + k[i]) % N])
        k.append(m)
    return "".join(cifrado)


def descifrar_autoclave(cifrado, clave):
    cifrado, clave = normalizar(cifrado), normalizar(clave)
    k = [ALFABETO.index(c) for c in clave]
    claro = []
    for i, ch in enumerate(cifrado):
        m = (ALFABETO.index(ch) - k[i]) % N
        claro.append(ALFABETO[m])
        k.append(m)
    return "".join(claro)


if __name__ == "__main__":
    CLAVE = "UNODELOSMASGRANDESCRIPTOGRAFOS"
    TEXTO_CIFRADO = """XHGDQESDMPK~NDEEDKNGJZPFJSUIFZOLFCINFJCESVZTGBFXCIUDAYNUUDIZYWWZBEYNVQWIVUN
KZEPHDODQUZZLBDNDRWTHQSER~NIVMLERCMGIFLSORZXTSDIGLOXQSDJHWVCIWQXQJCKMBPOK
MPSKMUVIMNJDNBLCSZHXHNYYUIXDBSOXHZLXWVGDJGXHWLTDWK~NSAQIMZLNBVMLXHUOQQXI
QGWGUFTWKZKMOKUDNINSIFJDUOZIJBSVVOWFAIE~NGYOWPSOAP"""

    claro = descifrar_autoclave(TEXTO_CIFRADO, CLAVE)
    print("\nTEXTO CLARO:\n", claro)

    # Comprobación: al volver a cifrar debe salir el criptograma original
    assert cifrar_autoclave(claro, CLAVE) == normalizar(TEXTO_CIFRADO)
    print("\nComprobación cifrar(descifrar(x)) == x  ->  OK")