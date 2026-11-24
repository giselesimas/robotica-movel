from pathlib import Path
import sys

from controller import Robot

import rclpy
from geometry_msgs.msg import Twist


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


# ----------------------------------------------------------------------
# Configuração do ROS 2
# ----------------------------------------------------------------------

rclpy.init()

node = rclpy.create_node('robo_diferencial')


def callback(msg):
    """Recebe comandos de velocidade do ROS 2."""

    vx = msg.linear.x
    vy = 0.0
    omega = msg.angular.z

    aplicar_velocidade(vx, vy, omega)


subscription = node.create_subscription(
    Twist,
    '/cmd_vel',
    callback,
    10
)

node.get_logger().info(
    'Aguardando comandos no topico /cmd_vel'
)


# ----------------------------------------------------------------------
# Loop principal
# ----------------------------------------------------------------------

try:
    while rclpy.ok() and sim.step(TIME_STEP) != -1:
        rclpy.spin_once(node, timeout_sec=0)

finally:
    node.destroy_node()

    if rclpy.ok():
        rclpy.shutdown()
