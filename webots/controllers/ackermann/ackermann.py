from pathlib import Path
import sys

from controller import Robot

RAIZ_PROJETO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ_PROJETO / "src"))

from robotica.robos.ackermann import RoboAckermann


# ----------------------------------------------------------------------
# Configuração do Webots
# ----------------------------------------------------------------------

sim = Robot()
TIME_STEP = int(sim.getBasicTimeStep())

motor_te = sim.getDevice("rear_left_wheel")
motor_td = sim.getDevice("rear_right_wheel")
motor_fe = sim.getDevice("front_left_wheel")
motor_fd = sim.getDevice("front_right_wheel")

direcao_esq = sim.getDevice("left_steer")
direcao_dir = sim.getDevice("right_steer")

motores = [
    motor_te,
    motor_td,
    motor_fe,
    motor_fd
]

for motor in motores:
    motor.setPosition(float("inf"))
    motor.setVelocity(0.0)

pen = sim.getDevice("pen")
pen.write(True)


# ----------------------------------------------------------------------
# Modelo cinemático
# ----------------------------------------------------------------------

robo = RoboAckermann(
    raio_roda=0.08,
    entre_eixos=0.30,
    bitola=0.26
)


def aplicar_velocidade(vx, vy, omega):
    """Converte a velocidade do robô em velocidades e ângulos das rodas."""
    resultado = robo.cinematica_inversa(vx, vy, omega)

    w_te = resultado[0]
    w_td = resultado[1]
    w_fe = resultado[2]
    w_fd = resultado[3]
    delta_esq = resultado[4]
    delta_dir = resultado[5]

    motor_te.setVelocity(w_te)
    motor_td.setVelocity(w_td)
    motor_fe.setVelocity(w_fe)
    motor_fd.setVelocity(w_fd)

    direcao_esq.setPosition(delta_esq)
    direcao_dir.setPosition(delta_dir)


# duração, vx, vy, omega, nome
TESTES = [
    (2.5, 0.20, 0.00,  0.00, 'frente'),
    (1.0, 0.00, 0.00,  0.00, 'parado'),
    (3.0, 0.20, 0.00,  0.45, 'curva à esquerda'),
    (1.0, 0.00, 0.00,  0.00, 'parado'),
    (3.0, 0.20, 0.00, -0.45, 'curva à direita')
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
