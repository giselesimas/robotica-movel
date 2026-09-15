from pathlib import Path
import sys

from controller import Robot

RAIZ_PROJETO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ_PROJETO / "src"))

from robotica.robos.diferencial import RoboDiferencial


# ----------------------------------------------------------------------
# Configuração do Webots
# ----------------------------------------------------------------------

sim = Robot()
TIME_STEP = int(sim.getBasicTimeStep())

motor_esq = sim.getDevice("left wheel motor")
motor_dir = sim.getDevice("right wheel motor")

motor_esq.setPosition(float("inf"))
motor_dir.setPosition(float("inf"))

motor_esq.setVelocity(0.0)
motor_dir.setVelocity(0.0)

pen = sim.getDevice("pen")
pen.write(True)


# ----------------------------------------------------------------------
# Modelo cinemático
# ----------------------------------------------------------------------

robo = RoboDiferencial(
    raio_roda=0.033,
    distancia_rodas=0.160
)


def aplicar_velocidade(vx, vy, omega):
    """Converte a velocidade do robô em velocidades das rodas."""
    w_esq, w_dir = robo.cinematica_inversa(vx, vy, omega)

    motor_esq.setVelocity(w_esq)
    motor_dir.setVelocity(w_dir)


# duração, vx, vy, omega, nome
TESTES = [
    (2.5, 0.12, 0.00, 0.00, 'frente'),
    (1.0, 0.00, 0.00, 0.00, 'parado'),
    (2.0, 0.00, 0.00, 0.70, 'giro'),
    (1.0, 0.00, 0.00, 0.00, 'parado'),
    (2.5, 0.12, 0.00, 0.00, 'frente')
]


indice_teste = 0
inicio_teste = sim.getTime()
duracao, vx, vy, omega, nome_teste = TESTES[indice_teste]
print(nome_teste)

while sim.step(TIME_STEP) != -1 and indice_teste < len(TESTES):
    tempo_decorrido = sim.getTime() - inicio_teste
    if tempo_decorrido < duracao:
        aplicar_velocidade(vx, vy, omega)
    else:
        aplicar_velocidade(0.0, 0.0, 0.0)
        indice_teste = indice_teste + 1
        inicio_teste = sim.getTime()
        if indice_teste < len(TESTES):
            duracao, vx, vy, omega, nome_teste = TESTES[indice_teste]
            print(nome_teste)
        else:
            print('Testes concluídos.')

aplicar_velocidade(0.0, 0.0, 0.0)
