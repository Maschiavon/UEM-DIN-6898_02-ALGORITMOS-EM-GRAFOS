import math
from dataclasses import dataclass
from typing import Union, List
import random
import collections
import os
import time


# Alunos: Matheus Augusto Schiavon Parise - 107115
#         Gabriel de melo Osório - 107862

# Um Vertice é uma estrutura que possui um numero um identificador unico,
# uma lista de numeros de adjacencia Adj, d um numero de descoberta,
# um pai que pode ser o numero do vertice que descobriu ele ou None
# e uma cor uma string podendo ser 'branca', 'cinza' ou 'preta'
@dataclass
class Vertice:
    def __init__(self, Numero, Adj=Union[None, List[int]], d=Union[None, int], Pai=Union[None, 'Vertice'],
                 Cor=Union[None, str], AdjPeso=Union[None, List[float]]):
        self.Numero = Numero
        if Adj is None:
            Adj = []
        self.Adj = Adj
        if d is None:
            d = 0
        self.d = d
        self.Pai = Pai
        if Cor is None:
            Cor = 'branco'
        self.Cor = Cor
        if AdjPeso is None:
            AdjPeso = []
        self.AdjPeso = AdjPeso

    def _repr_(self):
        return f'Link({self.Numero}, {self.Adj}, {self.d}, {self.Pai}, {self.Cor}, {self.AdjPeso})'


# Exemplos de vertices
# Verices são automaticamente enumerados de acordo com a posição
# Na lista do grafo antes de qualquer operação ou modificação
V0 = Vertice(0, [1, 2])
V1 = Vertice(1, [0], 2, V0, "branco")
V2 = Vertice(2, [0, 3], 3, V0, "branco")
V3 = Vertice(3, [2], 4, V2, "branco")

V4 = Vertice(0, [1, 2], 4, None, "branco")
V5 = Vertice(1, [0, 2], 4, None, "branco")
V6 = Vertice(2, [0, 1], 4, None, "branco")

V7 = (Vertice(0, [], 0, None, "branco"))

V8 = (Vertice(0, [1, 2], 0, None, "branco"))
V9 = (Vertice(1, [0, 2], 0, None, "branco"))
V10 = (Vertice(2, [0, 1], 0, None, "branco"))
V11 = (Vertice(3, [4], 0, None, "branco"))
V12 = (Vertice(4, [3], 0, None, "branco"))


@dataclass
class Aresta:
    v1: Vertice
    v2: Vertice
    w: float

    def _repr_(self):
        return f'Link({self.v1}, {self.v2}, {self.w})'


# Exemplos de aresta
A1 = Aresta(V0, V1, 1)
A2 = Aresta(V0, V2, 2)
A3 = Aresta(V2, V3, 3)

A4 = Aresta(V4, V5, 3)
A5 = Aresta(V5, V6, 3)
A6 = Aresta(V4, V6, 3)

A8 = Aresta(V8, V9, 6)
A9 = Aresta(V8, V10, 7)
A10 = Aresta(V9, V10, 1)
A11 = Aresta(V11, V12, 2)


@dataclass
class Grafo:
    V: List[Vertice]
    E: List[Aresta]

    def AdicionarAresta(self, vert1: Vertice, vert2: Vertice, w: float):
        self.V[vert1.Numero].Adj.append(vert2.Numero)
        self.V[vert2.Numero].Adj.append(vert1.Numero)
        self.V[vert1.Numero].AdjPeso.append(w)
        self.V[vert2.Numero].AdjPeso.append(w)
        self.E.append(Aresta(vert1, vert2, w))

    def _repr_(self):
        return f'Link({self.V}, {self.E})'


# Um grafo G é um lista de vertices com pelo menos 1 elemento
# Uma árvore é um grafo não orientado conexo e acíclico.
Grafo1 = Grafo([V0, V1, V2, V3], [A1, A2, A3])
Grafo2 = Grafo([V4, V5, V6], [A4, A5, A6])  # Grafo2 não é arvore pois tem um ciclo
Grafo3 = Grafo([V7], [])
Grafo4 = Grafo([V8, V9, V10, V11, V12], [A8, A9, A10, A11])  # Grafo desconexo com ciclo


# Dado um grafo G e um vertice inicial qualquer s
# o BFS faz uma busca em largura a partir de s
# até descobrir cada vertice acessivel do grafo
# quando um vertice v é descoberto BFS insere seu valor de
# descoberta em v.d onde o valor de d tem com base o valor d
# de seu atributo "pai" que o foi responsavel por sua descoberta,
# o bfs também muda a cor de v para cinza ao descobrir e preto quando
# terminar de verificar seus adjacentes
# s começa com d = 0 pois ele é o ponto de partida,
# s não tem pai e como já foi descoberto começa com a cor cinza.
# Em uma analise de tempo o BFS é O(V+E), Considerando V a lista de
# todos os vertices e E a lista de arestas.
def BFS(G: Grafo, s: int):
    Lista = list(range(len(G.V)))  # list é O(n)
    Lista.remove(s)
    for v in Lista:
        G.V[v].d = -1
        G.V[v].Pai = None
        G.V[v].Cor = "branco"
    G.V[s].d = 0
    G.V[s].Pai = None
    G.V[s].Cor = "cinza"

    # Aqui Q é um deque (fila dupla) que é representado
    # internamente como uma lista duplamente vinculada
    Q = collections.deque()
    Q.append(G.V[s])  # Enqueue do deque com tempo O(1)

    while Q:
        u = Q.popleft()  # Dequeue do deque com tempo O(1)
        for vert in u.Adj:
            if G.V[vert].Cor == "branco":
                G.V[vert].Cor = "cinza"
                G.V[vert].d = u.d + 1
                G.V[vert].Pai = u
                Q.append(G.V[vert])  # Enqueue do deque com tempo O(1)
        u.cor = "preto"


# Exemplos, Como BFS não retorna informações, apenas
# modifica o grafo existente é necessario excutar a
# verificação após a excução do codigo
ve0 = Vertice(0, [1, 2], 0, None, 'cinza')
ve1 = Vertice(1, [0], 1, ve0, 'cinza')
ve2 = Vertice(2, [0, 3], 1, ve0, 'cinza')
ve3 = Vertice(3, [2], 0, None, 'cinza')

ve4 = Vertice(2, [0, 3], 1, ve3, 'cinza')
ve5 = Vertice(0, [1, 2], 2, ve4, 'cinza')

BFS(Grafo1, 0)
assert Grafo1.V == [ve0, ve1, ve2, ve3]

BFS(Grafo1, 3)
assert Grafo1.V == [Vertice(0, [1, 2], 2, ve4, 'cinza'),
                    Vertice(1, [0], 3, ve5, 'cinza'),
                    ve4,
                    ve3]

BFS(Grafo2, 0)
assert Grafo2.V == [ve0,
                    Vertice(1, [0, 2], 1, ve0, 'cinza'),
                    Vertice(2, [0, 1], 1, ve0, 'cinza')]

BFS(Grafo3, 0)
assert Grafo3.V == [Vertice(0, [], 0, None, 'cinza')]

BFS(Grafo4, 0)
assert Grafo4.V == [ve0,
                    Vertice(1, [0, 2], 1, ve0, 'cinza'),
                    Vertice(2, [0, 1], 1, ve0, 'cinza'),
                    Vertice(3, [4], -1, None, 'branco'),
                    Vertice(4, [3], -1, None, 'branco')]


# Recebe T um Grafo que precisa ser uma arvore e devolve o diametro
# de uma arvore que é o maior distancia entre 2 vertice de uma arvore
# Diameter tem tempo de O(V) pois as arestas em uma arvore são
# iguais aos vertices - 1 ou seja E = V - 1
# dai o BFS no diameter teria tempo O(V+V-1),
# -1 e 2V é engolido por V então O(V).
# Caso T não seja uma arvore o resultado será impreciso.
def Diameter(T: Grafo):
    s = random.randint(0, len(T.V) - 1)

    t1 = T
    BFS(t1, s)

    a = Vertice(-1, [], -1, None, 'branco')
    for v in t1.V:
        if v.d > a.d:
            a = v

    BFS(t1, a.Numero)
    b = Vertice(-1, [], -1, None, 'branco')
    for j in t1.V:
        if j.d > b.d:
            b = j

    return b.d


# Exemplos do Diameter
d1 = Diameter(Grafo1)
d3 = Diameter(Grafo3)
assert d1 == 3
assert d3 == 0


# Recebe um grafo e retorna True se for uma arvore
# e false caso contrario
# conexo, acíclico e com v-1 arestas.
def Verifica_Arvore(G: Grafo):
    if len(G.E) == len(G.V) - 1:
        s = random.randint(0, len(G.E))
        BFS(G, s)
        paiNull = 0
        for v in G.V:
            if v.Pai is None:
                paiNull += 1
        if paiNull == 1:
            return True
    if len(G.E) == len(G.V) == 0:
        return True
    return False


# Exemplos
assert Verifica_Arvore(Grafo1)
assert not Verifica_Arvore(Grafo2)
assert Verifica_Arvore(Grafo3)
assert not Verifica_Arvore(Grafo4)


# Recebe n um numero e inteiro e cria um grafo
# com n vertices, o tempo é O(n).
def Cria_Grafo(n):
    Gr = Grafo([], [])
    ListV = []
    i = 0
    while i < n:
        vert = Vertice(i, [], 0, None, 'branco', [])
        ListV.append(vert)
        i += 1

    Gr.V = ListV
    return Gr


# Exemplos
assert Cria_Grafo(0) == Grafo([], [])
assert Cria_Grafo(1) == Grafo([Vertice(0, [], 0, None, 'branco')], [])
assert Cria_Grafo(5) == Grafo([Vertice(0, [], 0, None, 'branco'),
                               Vertice(1, [], 0, None, 'branco'),
                               Vertice(2, [], 0, None, 'branco'),
                               Vertice(3, [], 0, None, 'branco'),
                               Vertice(4, [], 0, None, 'branco')], [])


# Recebe n um numero e inteiro e cria um grafo
# completo com n vertices. O(n2)
def Cria_Grafo_Completo(n):
    G = Cria_Grafo(n)
    Lista = list(range(n))

    for v in G.V:
        for i in Lista:
            if v.Numero == i:
                G.V[i].AdjPeso.append(0)
            if v.Numero < i:
                G.AdicionarAresta(v, G.V[i], random.random())

    return G


# Exemplos
assert Cria_Grafo_Completo(0) == Grafo([], [])
assert Cria_Grafo_Completo(1) == Grafo([Vertice(0, [], 0, None, 'branco')], [])
gc5 = Cria_Grafo_Completo(5)
gc5resp = Grafo([Vertice(0, [1, 2, 3, 4], 0, None, 'branco', gc5.V[0].AdjPeso),
                 Vertice(1, [0, 2, 3, 4], 0, None, 'branco', gc5.V[1].AdjPeso),
                 Vertice(2, [0, 1, 3, 4], 0, None, 'branco', gc5.V[2].AdjPeso),
                 Vertice(3, [0, 1, 2, 4], 0, None, 'branco', gc5.V[3].AdjPeso),
                 Vertice(4, [0, 1, 2, 3], 0, None, 'branco', gc5.V[4].AdjPeso)],
                [Aresta(Vertice(0, [1, 2, 3, 4], 0, None, 'branco', gc5.V[0].AdjPeso),
                        Vertice(1, [0, 2, 3, 4], 0, None, 'branco', gc5.V[1].AdjPeso), gc5.E[0].w),
                 Aresta(Vertice(0, [1, 2, 3, 4], 0, None, 'branco', gc5.V[0].AdjPeso),
                        Vertice(2, [0, 1, 3, 4], 0, None, 'branco', gc5.V[2].AdjPeso), gc5.E[1].w),
                 Aresta(Vertice(0, [1, 2, 3, 4], 0, None, 'branco', gc5.V[0].AdjPeso),
                        Vertice(3, [0, 1, 2, 4], 0, None, 'branco', gc5.V[3].AdjPeso), gc5.E[2].w),
                 Aresta(Vertice(0, [1, 2, 3, 4], 0, None, 'branco', gc5.V[0].AdjPeso),
                        Vertice(4, [0, 1, 2, 3], 0, None, 'branco', gc5.V[4].AdjPeso), gc5.E[3].w),

                 Aresta(Vertice(1, [0, 2, 3, 4], 0, None, 'branco', gc5.V[1].AdjPeso),
                        Vertice(2, [0, 1, 3, 4], 0, None, 'branco', gc5.V[2].AdjPeso), gc5.E[4].w),
                 Aresta(Vertice(1, [0, 2, 3, 4], 0, None, 'branco', gc5.V[1].AdjPeso),
                        Vertice(3, [0, 1, 2, 4], 0, None, 'branco', gc5.V[3].AdjPeso), gc5.E[5].w),
                 Aresta(Vertice(1, [0, 2, 3, 4], 0, None, 'branco', gc5.V[1].AdjPeso),
                        Vertice(4, [0, 1, 2, 3], 0, None, 'branco', gc5.V[4].AdjPeso), gc5.E[6].w),

                 Aresta(Vertice(2, [0, 1, 3, 4], 0, None, 'branco', gc5.V[2].AdjPeso),
                        Vertice(3, [0, 1, 2, 4], 0, None, 'branco', gc5.V[3].AdjPeso), gc5.E[7].w),
                 Aresta(Vertice(2, [0, 1, 3, 4], 0, None, 'branco', gc5.V[2].AdjPeso),
                        Vertice(4, [0, 1, 2, 3], 0, None, 'branco', gc5.V[4].AdjPeso), gc5.E[8].w),

                 Aresta(Vertice(3, [0, 1, 2, 4], 0, None, 'branco', gc5.V[3].AdjPeso),
                        Vertice(4, [0, 1, 2, 3], 0, None, 'branco', gc5.V[4].AdjPeso), gc5.E[9].w)])

assert gc5 == gc5resp


# Recebe como entrada um número maior que 0 e produz uma
# árvore aleatória com n vértices se n for 0 ou negativo
# o programa emitira uma exception do tipo ValueError.
def Random_Tree_Random_Walk(n: int):
    G = Cria_Grafo(n)
    for v in G.V:
        v.cor = "branco"
        v.Pai = None
    u = random.randint(0, len(G.V) - 1)
    G.V[u].Cor = "cinza"
    e = 0
    while e < n - 1:
        vert = random.randint(0, n - 1)
        if G.V[vert].Cor == "branco":
            G.V[vert].Pai = G.V[u]
            G.V[vert].Cor = "cinza"
            G.AdicionarAresta(G.V[u], G.V[vert], 0)

            e += 1
        u = vert
    return G


# Exemplos para caso UNICO, ou seja,
# ele PRECISA ser uma arvore.
rtrw1 = Random_Tree_Random_Walk(1)
rtrw5 = Random_Tree_Random_Walk(5)

assert Verifica_Arvore(rtrw1)
assert Verifica_Arvore(rtrw5)


# A operação Make_Set recebe um vertice v zera do valor d
# e coloca v como seu proprio pai.
def Make_Set(v: Vertice):
    v.Pai = v
    v.d = 0
    return v


# Exemplos
Vteste = Vertice(1, [0, 2, 3], 12, None, 'branco')
Make_Set(Vteste)
assert Vteste == Vertice(1, [0, 2, 3], 0, Vteste, 'branco')


# A operação Find_Set recebe um vertice v e atravez dele acha
# sua propria raiz.
def Find_Set(v: Vertice):
    if v.Numero != v.Pai.Numero:
        v.Pai = Find_Set(v.Pai)
    return v.Pai


# Exemplos
Vex0 = Vertice(0, [1], 0, None, 'branco')
Make_Set(Vex0)
Vex1 = Vertice(1, [0], 1, Vex0, 'branco')
assert Find_Set(Vex1) == Vex0


# Link é uma sub-rotina de MakeUnion, recebe 2 vertices
# e compara eles se x.rank(no caso rank vai ser o d) for maior
# que y.rank então x vira pai de y, caso contrario
# y vira pai de x e se o valor do d de x e y forem iguais
# incrementa y.d em 1.
def Link(x: Vertice, y: Vertice):
    if x.d > y.d:
        y.Pai = x
    else:
        x.Pai = y
        if x.d == y.d:
            y.d += 1


# Recebe 2 vertices x e y e faz a união dos vertices
# verificando se eles possuem a mesma raiz
def MakeUnion(x: Vertice, y: Vertice):
    Link(Find_Set(x), Find_Set(y))


# Exemplo
vt1 = Vertice(0, [], 0, None, 'branco')
vt2 = Vertice(1, [], 0, None, 'branco')
vt3 = Vertice(2, [], 2, None, 'branco')
Make_Set(vt1)
Make_Set(vt2)
Make_Set(vt3)
MakeUnion(vt1, vt2)
MakeUnion(vt3, vt2)

assert vt1.Pai == vt2
assert vt3.Pai == vt2


# Recebe n um numero inteiro maior que 0 e retorna
# uma arvore com n vertices produzido por MST-Kruskal
def Random_Tree_Kruskal(n: int):
    G = Cria_Grafo_Completo(n)
    resp = MST_Kruskal(G)
    return resp


# Sub-rotina de Random Tree Kruskal, recebe um grafo
# completo G e faz as ligações aleatoriamente para gerar
# uma arvore de com len(G.V) vertices e len(G.V)-1 arestas.
def MST_Kruskal(G: Grafo):
    A = Grafo([], [])
    for v in G.V:
        vert0 = Vertice(0, [], 0, None, "branco", [])
        vert0.Numero = v.Numero
        Make_Set(vert0)
        A.V.append(vert0)

    for a in G.E:
        if a.v1.Pai is None:
            Make_Set(a.v1)
        if a.v2.Pai is None:
            Make_Set(a.v2)

    G.E = sorted(G.E, key=lambda aresta: aresta.w)
    for e in G.E:
        v1 = Find_Set(e.v1)
        v2 = Find_Set(e.v2)
        bol = v1.Numero != v2.Numero

        if bol:
            MakeUnion(v1, v2)
            A.AdicionarAresta(v1, v2, e.w)

        if len(A.E) == len(G.V) - 1:
            break
    return A


# Exemplos para Random Tree Kruskal
# caso UNICO aleatorio, ou seja, ele PRECISA ser uma arvore.
rtk0 = Random_Tree_Kruskal(0)
rtk1 = Random_Tree_Kruskal(1)
rtk5 = Random_Tree_Kruskal(5)
rtk250 = Random_Tree_Kruskal(250)
assert Verifica_Arvore(rtk0)
assert Verifica_Arvore(rtk1)
assert Verifica_Arvore(rtk5)
assert Verifica_Arvore(rtk250)

# Exemplos para MST_Kruskal
gKrs0 = MST_Kruskal(Cria_Grafo_Completo(0))
gKrs0r = Grafo([], [])
gKrs1 = MST_Kruskal(Cria_Grafo_Completo(1))
gKrs1r = Grafo([Vertice(0, [], 0, None, 'branco')], [])
gKrs4 = MST_Kruskal(Cria_Grafo_Completo(4))
gKrs4r = Grafo([Vertice(0, [1, 2, 3], 0, None, 'branco', gKrs4.V[0].AdjPeso),
                Vertice(1, [0, 2, 3], 0, None, 'branco', gKrs4.V[1].AdjPeso),
                Vertice(2, [0, 1, 3], 0, None, 'branco', gKrs4.V[2].AdjPeso),
                Vertice(3, [0, 1, 2], 0, None, 'branco', gKrs4.V[3].AdjPeso)],
               [Aresta(gKrs4.V[0], gKrs4.V[1], gKrs4.E[0].w),
                Aresta(gKrs4.V[0], gKrs4.V[2], gKrs4.E[1].w),
                Aresta(gKrs4.V[0], gKrs4.V[3], gKrs4.E[2].w)])
assert gKrs0 == gKrs0r
assert gKrs1 == gKrs1r
assert gKrs4 == gKrs4r


# Recebe uma lista de vertices e devolve o vertice com
# O menor d que ainda está na lista.
def Extract_min(V: List[Vertice]):
    if len(V) == 0:
        return None
    lst = []
    for v in V:
        if v.Cor == "False":
            lst.append(v.d)
        else:
            lst.append(math.inf)
    re = min(lst)
    re_i = lst.index(re)

    return V[re_i]


# Exemplos Extract_Min
extr0 = []
extr1 = [Vertice(0, [], 0, None, "False")]
extr4 = [Vertice(0, [], 0, None, "False"),
         Vertice(1, [], 5, None, "False"),
         Vertice(2, [], -1, None, "False"),
         Vertice(3, [], math.inf, None, "False")]

assert Extract_min(extr0) is None
assert Extract_min(extr1) == Vertice(0, [], 0)
assert Extract_min(extr4) == Vertice(2, [], -1)


# Recebe n um numero inteiro maior que 0 e retorna
# uma arvore com n vertices produzido por MST-Prim
def Random_Tree_Prim(n: int):
    G = Cria_Grafo_Completo(n)
    if n > 0:
        s = random.randint(0, len(G.V) - 1)
        G = MST_Prim(G, G.V[s])
    return G


# Sub-rotina de Random Tree Prim, recebe um grafo
# completo G e R um vertice aleatorio de G, atraves de r
# faz as ligações aleatoriamente para gerar
# uma arvore de com len(G.V) vertices e len(G.V)-1 arestas.
def MST_Prim(G: Grafo, r: Vertice):
    A = Grafo([], [])
    for u in G.V:
        u.d = math.inf
        u.Pai = None
        u.Cor = "False"
    r.d = 0
    for z in G.V:
        vert = Vertice(z.Numero, [], z.d, z.Pai, z.Cor, [])
        A.V.append(vert)

    for count in range(len(G.V)):  # while len(A.E) < len(A.V) - 1: #
        u = Extract_min(G.V)
        u.Cor = "True"

        if u.Pai is not None:
            A.AdicionarAresta(u.Pai, u, u.d)

        for v in u.Adj:
            vertAdj = G.V[v]
            cond1 = vertAdj.d > u.AdjPeso[v]
            cond2 = vertAdj.Cor == "False"
            if cond1 and cond2:
                vertAdj.Pai = u
                vertAdj.d = u.AdjPeso[v]
    return A


# Exemplos para Random Tree Prim
gprim0 = Random_Tree_Prim(0)
gprim1 = Random_Tree_Prim(1)
gprim5 = Random_Tree_Prim(5)
assert Verifica_Arvore(gprim0)
assert Verifica_Arvore(gprim1)
assert Verifica_Arvore(gprim5)

# Exemplos Para MST_kruskal
gc1 = Cria_Grafo_Completo(1)
gc4 = Cria_Grafo_Completo(4)
gMst_p1 = MST_Prim(gc1, gc1.V[0])
gMst_p4 = MST_Prim(gc4, gc4.V[0])

assert gMst_p1 == Grafo([Vertice(0)], [])
assert gMst_p4 == Grafo([Vertice(0, gMst_p4.V[0].Adj, gMst_p4.V[0].d, gMst_p4.V[0].Pai, 'True', gc4.V[0].AdjPeso),
                         Vertice(1, gMst_p4.V[1].Adj, gMst_p4.V[1].d, gMst_p4.V[1].Pai, 'True', gc4.V[1].AdjPeso),
                         Vertice(2, gMst_p4.V[2].Adj, gMst_p4.V[2].d, gMst_p4.V[2].Pai, 'True', gc4.V[2].AdjPeso),
                         Vertice(3, gMst_p4.V[3].Adj, gMst_p4.V[3].d, gMst_p4.V[3].Pai, 'True', gc4.V[3].AdjPeso)],
                        gMst_p4.E)


# Função auxiliar de Testar() usada para o teste de random tree random walk
def TestarRTRW():
    n = 250
    tempoTotal = 0
    print("///Testando Random Tree Random Walk///")
    f = open("randomwalk.txt", "w")

    while n <= 2000:
        start = time.time()
        diametro = 0
        for x in range(500):
            arv = Random_Tree_Random_Walk(n)
            if Verifica_Arvore(arv):
                diametro += Diameter(arv)
            else:
                raise Exception("Erro não é arvore")
        diametro /= 500
        end = time.time()

        print("Para n = ", n, "\nA media do diametro é ", diametro)
        print("tempo consumido = ", end - start)

        tempoTotal += end - start
        f.write(str(n) + " " + str(diametro) + "\n")
        n += 250
    print("\nTempo Total:", tempoTotal, " segundos")
    f.close()
    os.system('python3 plot.py randomwalk <  "randomwalk.txt"')
    return True


# Função auxiliar de Testar() usada para o teste de random tree kruskal
def TestarRTK():
    n = 250
    tempoTotal = 0
    print("///Testando Random Tree Kruskal///")
    f = open("kruskal.txt", "w")

    while n <= 2000:
        start = time.time()
        diametro = 0
        for x in range(500):
            arv = Random_Tree_Kruskal(n)
            if Verifica_Arvore(arv):
                diametro += Diameter(arv)
            else:
                raise Exception("Erro não é arvore")
        diametro /= 500
        end = time.time()

        print("Para n = ", n, "\nA media do diametro é ", diametro)
        print("tempo consumido = ", end - start)

        tempoTotal += end - start
        f.write(str(n) + " " + str(diametro) + "\n")
        n += 250
    print("\nTempo Total:", tempoTotal, " segundos")
    f.close()
    os.system('python3 plot.py kruskal <  "kruskal.txt"')
    return True


# Função auxiliar de Testar() usada para o teste de random tree prim
def TestarPrim():
    n = 250
    tempoTotal = 0
    print("///Testando Random Tree Prim///")
    f = open("prim.txt", "w")

    while n <= 2000:
        start = time.time()
        diametro = 0
        for x in range(500):
            arv = Random_Tree_Prim(n)
            if Verifica_Arvore(arv):
                diametro += Diameter(arv)
            else:
                raise Exception("Erro não é arvore")
        diametro /= 500
        end = time.time()

        print("Para n = ", n, "\nA media do diametro é ", diametro)
        print("tempo consumido = ", end - start)

        tempoTotal += end - start
        f.write(str(n) + " " + str(diametro) + "\n")
        n += 250
    print("\nTempo Total:", tempoTotal, " segundos")
    f.close()
    os.system('python3 plot.py prim <  "prim.txt"')
    return True


# Exemplo
# Está função é uma forma utilizada para testar as funções geradoras de arvores aleatorias
# ela não recebe parametros, mas pergunta qual função testar, se receber uma informação que não
# seja o nome de uma função termina o processo, caso receba um nome valido verifica
# se a media do diametro de 500 arvores aleatorias geradas pelo algoritmo especificado
# para os valores de n de [250 até 2000], incrementando de 250 em 250
# o resultado da media do diametro para cada valor de n tem que ser aproximadamente
# O(sqrt(n)), está função gera um text chamado "randomwalk.txt" e executa o arquivo
# plot.py auxiliar que foi fornecido para gerar um grafico nesse trabalho.
def Testar():
    def Pergunta():
        print("Qual função deseja testar ?: 'randomwalk','kruskal' ou 'prim' \n"
              "(digite exatamente o nome de uma das funções acima ou qualquer outra coisa para sair.)\n")
        text = input("resposta = ")
        return text

    text = Pergunta()
    continuar = True

    while continuar:
        if text == "randomwalk":
            TestarRTRW()
            text = Pergunta()
        elif text == "kruskal":
            TestarRTK()
            text = Pergunta()
        elif text == "prim":
            TestarPrim()
            text = Pergunta()
        else:
            continuar = False
            print("Terminando...")


# Exemplos
Testar()
