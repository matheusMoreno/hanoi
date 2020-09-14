"""
EEL470 - Algoritmos e Estruturas de Dados (DEL/POLI/UFRJ)
Atividade Extra - Torre de Hanoi em 3D
Versão B - Salvando a lista de movimentos e animando depois
Autor: Matheus Fernandes Moreno
"""

from vpython import *


# Número de discos na torre de origem
N = 8


def move_disc(start, end):
    """
    Move o disco no topo (último elemento) de 'start' para o topo (último
    elemento) de 'end'.
    Retorna o movimento feito (origem, destino, disco).
    """
    towers[end].append(towers[start].pop())
    return (start, end, towers[end][-1])


def hanoi(n, start, end, extra):
    """
    Resolve o problema da Torre de Hanoi recursivamente, para n discos e
    3 torres: início, fim e de trabalho (extra).
    Retorna uma lista com cada movimento feito pelo algoritmo.
    """
    steps = []
    if n > 0:
        steps += hanoi(n - 1, start, extra, end)
        steps += [move_disc(start, end)]
        steps += hanoi(n - 1, extra, end, start)
    return steps


# Inicializando o dicionário com as torres e resolvendo o problema
towers = {'A': list(range(N, 0, -1)), 'B': [], 'C': []}
moves = hanoi(N, 'A', 'B', 'C')


### O problema original acaba aqui. Abaixo encontra-se o código para animar
### os passos dados com o uso da biblioteca vpython.


# Constantes: vetores de movimento
MOVE_UP = vector(0, 0.001, 0)
MOVE_DOWN = vector(0, -0.001, 0)
MOVE_RIGHT = vector(0.001, 0, 0)
MOVE_LEFT = vector(-0.001, 0, 0)

# Constantes: distância entre torres, raio das torres, altura do movimento,
# altura de cada disco e velocidade de movimento
DIST = N * 2
TOWER_RADIUS = 0.1
MAX_HEIGHT = N + 2
DISC_HEIGHT = 0.5
SPEED = 5e4


# Gerando o canvas para o vpython (cor de fundo, título)
canvas(title=f"Passo-a-passo da Torre de Hanoi para {N} discos",
       width=1000, height=600, center=vector(0, 0, 0), background=color.white)

# Instanciando as torres
for j in [-1, 0, 1]:
    cylinder(
        pos=vector(DIST * j, 0, 0),
        axis=vector(0, MAX_HEIGHT - 1, 0),
        radius=TOWER_RADIUS,
        texture=textures.wood,
        color=color.white
    )

# Instanciando os discos (salvos em variáveis porque serão movidos)
discs = [cylinder(
             pos=vector(-DIST, (N - i) * DISC_HEIGHT, 0),
             axis=vector(0, DISC_HEIGHT, 0),
             radius=i,
             color=color.purple
         ) for i in range(N, 0, -1)]

# Instanciando a base da estrutura
box(pos=vector(0, 0, 0),
    length=3 * DIST + 0.5,
    height=DISC_HEIGHT / 2,
    width=DIST + 0.5,
    texture=textures.wood,
    color=color.white
)

# Esse dict guarda quantos discos estão em uma torre. Essa contagem
# é usada como uma espécie de "hitbox" na hora de decidir a altura para descer
n_discs = {'A': N, 'B': 0, 'C': 0}

for start, end, disc in moves:
    print(f"Movendo o disco {disc} da torre {start} para a torre {end}.")

    # Movendo o disco para cima
    while discs[N - disc].pos.y < MAX_HEIGHT:
        rate(SPEED)
        discs[N - disc].pos += MOVE_UP

    # Movendo o disco para o lado, dependendo do sentido do movimento
    x_pos = discs[N - disc].pos.x + DIST * (ord(end) - ord(start))
    if x_pos > discs[N - disc].pos.x:
        while discs[N - disc].pos.x < x_pos:
            rate(SPEED)
            discs[N - disc].pos += MOVE_RIGHT
    else:
        while discs[N - disc].pos.x > x_pos:
            rate(SPEED)
            discs[N - disc].pos += MOVE_LEFT

    # Movendo o disco para baixo, considerando os discos abaixo dele
    min_height = n_discs[end] * DISC_HEIGHT
    while discs[N - disc].pos.y > min_height:
        rate(SPEED)
        discs[N - disc].pos += MOVE_DOWN

    # Atualizando a quantidade de discos em cada torre
    n_discs[end] += 1
    n_discs[start] -= 1
