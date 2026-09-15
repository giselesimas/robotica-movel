import math

from .robo import Robo


class RoboOmni4(Robo):
    """
    Modelo cinemático de um robô omnidirecional com quatro rodas.

    As rodas são consideradas igualmente espaçadas em torno do robô.
    O ângulo de cada roda é dado em graus.
    """

    def __init__(
        self,
        raio_roda,
        distancia_centro,
        angulos_rodas=(45.0, 135.0, 225.0, 315.0)
    ):
        super().__init__(raio_roda)

        if distancia_centro <= 0:
            raise ValueError(
                "A distância das rodas ao centro deve ser maior que zero."
            )

        if len(angulos_rodas) != 4:
            raise ValueError(
                "O robô Omni4 deve possuir exatamente quatro ângulos de roda."
            )

        self.distancia_centro = float(distancia_centro)
        self.angulos_rodas = tuple(angulos_rodas)

    def cinematica_inversa(self, vx, vy, omega):
        """
        Calcula as velocidades angulares das quatro rodas.

        Retorna as velocidades na mesma ordem de angulos_rodas.
        """

        r = self.raio_roda
        L = self.distancia_centro

        velocidades = []

        for angulo_graus in self.angulos_rodas:
            angulo = math.radians(angulo_graus)

            velocidade = (
                -math.sin(angulo) * vx
                + math.cos(angulo) * vy
                + L * omega
            ) / r

            velocidades.append(velocidade)

        return tuple(velocidades)

    def cinematica_direta(self, w1, w2, w3, w4):
        """
        Calcula (vx, vy, omega) a partir das velocidades das rodas.

        Esta expressão considera quatro rodas igualmente espaçadas
        em 90 graus.
        """

        velocidades = (w1, w2, w3, w4)

        soma_vx = 0.0
        soma_vy = 0.0
        soma_omega = 0.0

        for i in range(4):
            angulo = math.radians(self.angulos_rodas[i])
            w = velocidades[i]

            soma_vx = soma_vx - math.sin(angulo) * w
            soma_vy = soma_vy + math.cos(angulo) * w
            soma_omega = soma_omega + w

        r = self.raio_roda
        L = self.distancia_centro

        vx = r * soma_vx / 2.0
        vy = r * soma_vy / 2.0
        omega = r * soma_omega / (4.0 * L)

        return vx, vy, omega
