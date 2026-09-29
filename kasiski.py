import re
import unicodedata
from collections import Counter, defaultdict
from math import gcd
from functools import reduce

ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
N = len(ALFABETO)
AEOS = {"A": 4, "E": 4, "O": 3, "S": 2}


def normalizar(texto):
    texto = texto.replace("~N", "Ñ").replace("~n", "ñ")
    texto = texto.upper().replace("Ñ", "\0")
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.replace("\0", "Ñ")
    return re.sub(r"[^A-ZÑ]", "", texto)


def distancias_repeticiones(cripto, min_len=3):
    pos = defaultdict(list)
    for i in range(len(cripto) - min_len + 1):
        pos[cripto[i:i + min_len]].append(i)
    distancias = []
    for seq, lugares in pos.items():
        if len(lugares) > 1:
            d = [b - a for a, b in zip(lugares, lugares[1:])]
            distancias.append((seq, lugares, d))
    return distancias


def longitud_clave(cripto, max_L=20, verbose=True):
    reps = distancias_repeticiones(cripto)
    todas = [d for _, _, ds in reps for d in ds]
    if verbose:
        print(f"Secuencias de 3 letras repetidas: {len(reps)}  | distancias: {len(todas)}")
        print("mcd de todas las distancias =", reduce(gcd, todas))
    cuenta = {L: sum(1 for d in todas if d % L == 0) for L in range(2, max_L + 1)}
    if verbose:
        print("Factores más frecuentes:", sorted(cuenta.items(), key=lambda x: -x[1])[:5])
    mejor = max(cuenta.values())
    return min(L for L, c in cuenta.items() if c == mejor)


def subcriptogramas(cripto, L):
    return [cripto[i::L] for i in range(L)]


def letra_clave(sub):
    frec = Counter(sub)
    mejor, mejor_score = 0, -1
    for s in range(N):
        score = sum(peso * frec[ALFABETO[(ALFABETO.index(l) + s) % N]]
                    for l, peso in AEOS.items())
        if score > mejor_score:
            mejor, mejor_score = s, score
    return ALFABETO[mejor]


def descifrar_vigenere(cripto, clave):
    k = [ALFABETO.index(c) for c in clave]
    return "".join(ALFABETO[(ALFABETO.index(c) - k[i % len(k)]) % N]
                   for i, c in enumerate(cripto))


def kasiski(criptograma, L=None):
    cripto = normalizar(criptograma)
    print("Longitud del criptograma:", len(cripto))
    if L is None:
        L = longitud_clave(cripto)
    print("Longitud de clave estimada L =", L)
    subs = subcriptogramas(cripto, L)
    clave = ""
    for i, s in enumerate(subs, 1):
        f = Counter(s).most_common(4)
        letra = letra_clave(s)
        clave += letra
        print(f"  Subcriptograma {i}: más frecuentes {f} -> letra de clave: {letra}")
    print("Clave encontrada:", clave)
    return clave, descifrar_vigenere(cripto, clave)


if __name__ == "__main__":
    CRIPTOGRAMA = """MAXYHGAVAPUUGZHEGZQOWOBNIPQKRN~NMEXIGONIICUCAWIGCTEAGMNOLRSZJNLW~NAWWIGLD
DZSNIZDNBIXGZLAYMX~NCVEKIETMOEOPBEWPTNIXCXUIHMECXLNOCECYXEQPBWUFANIIC~NJIKISCZ
UAILBGSOANKBFWUAYWNSCHLCWYDZHDZAQVMPTVGFGPVAJWFVPUOYMXCWERVLQCZWECIFVIT
UZSNCZUAIKBFM~NALIEGLBSZLQUX~NOHWOCGHNYW~NQKDANZUDIFOIMXNPHNUWQOKLMVBNNKR
MKONDPDPNMIKAWOXMEEIVEKGBGSFHVADWPGOYMHOIUEEIPGOLENZBSCHAGKQTZDR~NM~NNWTU
ZI~NCM~NAXKQUWDLVANNIHL~NCQNWGEHIPGZDTZT~NNW~NEEWFUMGI~NXNTWXNVIXCZOAZSOQUVE
NDNFWUSZYHGLRACPGGUGIYWHOTRMZUGQQDDZIZFWHVVSHCUGOGIFKBXAXPBOBRDVDUCMVT
KGIKDRSZLUQSDVPMXVIVEYMFGTEANIMQLHLGPQOHRYWCFEWFOISN~NPUAYINN~NXN~NPGKWGOILQ
GAFOILQTAHEIIDWM~NE~NXNEPRCVDQTURSK"""

    clave, claro = kasiski(CRIPTOGRAMA)
    print("\nTEXTO CLARO:\n", claro)