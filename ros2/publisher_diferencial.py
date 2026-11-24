import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

import time
import math

#=================================================================================
class PublisherDiferencial(Node):
    #--------------------------------------------------------------------
    def __init__(self):
        super().__init__('publisher_diferencial')

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

    #--------------------------------------------------------------------
    def movimentar(self, vx, omega, duracao):
        """Publica comandos de velocidade durante um intervalo de tempo."""

        msg = Twist()

        msg.linear.x = float(vx)
        msg.angular.z = float(omega)

        inicio = time.monotonic()

        while rclpy.ok() and time.monotonic() - inicio < duracao:

            self.publisher.publish(msg)

            time.sleep(0.1)

    #--------------------------------------------------------------------
    def parar(self):
        """Interrompe o movimento do robô."""

        self.movimentar(0.0, 0.0, 0.5)


#=================================================================================
def main():

    rclpy.init()

    node = PublisherDiferencial()

    try:
        # Aguarda a descoberta do subscriber
        while rclpy.ok() and node.publisher.get_subscription_count() == 0:
            time.sleep(0.1)

        # Parâmetros da trajetória
        lado = 0.5
        vx = 0.12
        omega = 0.7

        # Duração dos movimentos
        tempo_reta = lado / vx
        tempo_giro = (math.pi / 2) / omega

        # Executa a trajetória quadrada
        for i in range(4):

            node.get_logger().info(f'Executando lado {i + 1}')

            node.movimentar(vx, 0.0, tempo_reta)

            node.parar()

            node.movimentar(0.0, omega, tempo_giro)

            node.parar()

        node.get_logger().info('Trajetoria concluida!')

    except KeyboardInterrupt:
        pass

    finally:
        if rclpy.ok():
            node.parar()

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


#=================================================================================
if __name__ == '__main__':
    main()
