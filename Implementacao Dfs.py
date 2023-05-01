from dataclasses import dataclass
from typing import Union

# Alunos: Matheus Augusto Schiavon Parise - 107115
#         Gabriel de melo Osório - 107862

# Um Vertice é uma estrutura que possui um numero um identificador unico,
# uma lista de numeros de adjacencia Adj, d um numero de descoberta,
# um pai que pode ser o numero do vertice que descobriu ele ou None
# e uma cor uma string podendo ser 'branca', 'cinza' ou 'preta'
@dataclass
class Vertice:
    numero: int
    Adj: list
    d: int
    f: int
    pai: Union[None, int]
    cor: str

    def _repr_(self):
        return f'Link({self.numero}, {self.Adj}, {self.d}, {self.f}, {self.pai}, {self.cor})'


# Exemplos de vertices
# Verices são automaticamente enumerados de acordo com a posição
# Na lista do grafo antes de qualquer operação ou modificação
V0 = Vertice(0, [1, 2], 1, 0, None, "branco")
V1 = Vertice(1, [0], 2, 0, 0, "branco")
V2 = Vertice(2, [0, 3], 3, 0, 0, "branco")
V3 = Vertice(3, [2], 4, 0, 2, "branco")

V4 = Vertice(0, [1, 2], 4, 0, None, "branco")
V5 = Vertice(1, [0, 2], 4, 0, None, "branco")
V6 = Vertice(2, [0, 1], 4, 0, None, "branco")

V7 = (Vertice(0, [], 0, 0, None, "branco"))

V8 = (Vertice(0, [1, 2], 0, 0, None, "branco"))
V9 = (Vertice(1, [0, 2], 0, 0, None, "branco"))
V10 = (Vertice(2, [0, 1], 0, 0, None, "branco"))
V11 = (Vertice(3, [4], 0, 0, None, "branco"))
V12 = (Vertice(4, [3], 0, 0, None, "branco"))

# Um grafo G é um lista de vertices com pelo menos 1 elemento
# Uma árvore é um grafo não orientado conexo e acíclico.
Grafo1 = [V0, V1, V2, V3]
Grafo2 = [V4, V5, V6]  # Grafo2 não é arvore pois tem um ciclo
Grafo3 = [V7]
Grafo4 = [V8, V9, V10, V11, V12]  # Grafo desconexo com ciclo

# O procedimento DFS-Visit recebe um grafo g, um vertice "inicial" u e o tempo
# atual,  é chamado exatamente uma vez para cada vértice do DFS, isto porque DFS-Visit
# é chamado para os vértices brancos, e no início de DFS-Visit o vértice é pintado de cinza
# e seu tempo de descoberta registrado em d com base no tempo atual durante a execução para
# cada vertice adj ele é chamado novamente até não ter mais vertices branco acessiveis
# a partir do mais recentemente escolhido e depois volta registrando a volta do tempo
# ele precisa retornar o tempo para instancia anterior, caso contrario haverá erros nos
# tempos de descoberta e finalização dos vertices
# Como ele é executado um vez para cada aresta o tempo de DFS-Visit é Θ(E)
def DFS_Visit(G: list, u: Vertice, tempo: int):
    tempo += 1
    u.d = tempo
    u.cor = "cinza"
    for v in u.Adj:
        if G[v].cor == "branco":
            G[v].pai = u.numero
            tempo = DFS_Visit(G, G[v], tempo)
    u.cor = "preto"
    tempo += 1
    u.f = tempo
    return tempo


# Receve um grafo G explora todas as arestas a partir de u mais recentemente descoberto
# a busca regressa para explorar as arestas que deixam o vértice a partir do
# qual u foi descoberto, Este processo continua até que todos os vértices acessíveis
# a partir da origem tenham sidos descobertos, Se restarem vértices não descobertos
# a busca se repetirá para estes vértices
# o tempo é Θ(V + E)
def DFS(G: list):
    for v in G:
        v.d = 0
        v.f = 0
        v.cor = "branco"
        v.pai = None
    tempo = 0
    for u in G:
        if u.cor == "branco":
            tempo = DFS_Visit(G, u, tempo)


DFS(Grafo1)
DFS(Grafo2)
DFS(Grafo3)
DFS(Grafo4)

assert Grafo1 == [Vertice(0, [1, 2], 1, 8, None, 'preto'),
                  Vertice(1, [0], 2, 3, 0, 'preto'),
                  Vertice(2, [0, 3], 4, 7, 0, 'preto'),
                  Vertice(3, [2], 5, 6, 2, 'preto')]

assert Grafo2 == [Vertice(0, [1, 2], 1, 6, None, 'preto'),
                  Vertice(1, [0, 2], 2, 5, 0, 'preto'),
                  Vertice(2, [0, 1], 3, 4, 1, 'preto')]

assert Grafo3 == [Vertice(0, [], 1, 2, None, 'preto')]

assert Grafo4 == [Vertice(0, [1, 2], 1, 6, None, "preto"),
                  Vertice(1, [0, 2], 2, 5, 0, "preto"),
                  Vertice(2, [0, 1], 3, 4, 1, "preto"),
                  Vertice(3, [4], 7, 10, None, "preto"),
                  Vertice(4, [3], 8, 9, 3, "preto")]
