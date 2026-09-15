from pathlib import Path
import sys

from controller import Robot

RAIZ_PROJETO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ_PROJETO / "src"))

from robotica.robos.omni3 import RoboOmni3


# ----------------------------------------------------------------------
# Configuração do Webots
# ----------------------------------------------------------------------

sim = Robot()
TIME_STEP = int(sim.getBasicTimeStep())

motores = [
    sim.getDevice("wheel1"),
    sim.getDevice("wheel2"),
    sim.getDevice("wheel3")
]

for motor in motores:
    motor.setPosition(float("inf"))
    motor.setVelocity(0.0)

pen = sim.getDevice("pen")
pen.write(True)


# ----------------------------------------------------------------------
# Modelo cinemático
# ----------------------------------------------------------------------

robo = RoboOmni3(
    raio_roda=0.05,
    distancia_centro=0.10,
    angulos_rodas=(0.0, 120.0, 240.0)
)


def aplicar_velocidade(vx, vy, omega):
    """Converte a velocidade do robô em velocidades das rodas."""
    velocidades = robo.cinematica_inversa(vx, vy, omega)

    for i in range(len(motores)):
        motores[i].setVelocity(velocidades[i])


# duração, vx, vy, omega
TESTES = [
    (2.0, 0.20, 0.00, 0.00, 'frente'),  
    (1.0, 0.00, 0.00, 0.00, 'parado'),  
    (2.0, 0.00, 0.20, 0.00, 'lateral'), 
    (1.0, 0.00, 0.00, 0.00, 'parado'),   
    (2.0, 0.14, 0.14, 0.00, 'diagonal'),
    (1.0, 0.00, 0.00, 0.00, 'parado'),
    (2.0, 0.00, 0.00, 0.80, 'giro')
]


indice_teste = 0
inicio_teste = sim.getTime()
duracao, vx, vy, omega, nome_teste = TESTES[indice_teste]        
print(nome_teste)

while sim.step(TIME_STEP) != -1 and  indice_teste < len(TESTES):
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
