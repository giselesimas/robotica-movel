from .robo import Robo


class RoboDiferencial(Robo):
    """Modelo cinemático de um robô com duas rodas diferenciais."""

    def __init__(self, raio_roda, distancia_rodas):
        super().__init__(raio_roda)

        if distancia_rodas <= 0:
            raise ValueError(
                "A distância entre as rodas deve ser maior que zero."
            )

        self.distancia_rodas = float(distancia_rodas)

    def cinematica_inversa(self, vx, vy, omega):
        """
        Calcula as velocidades angulares das rodas.

        Parâmetros:
            vx    : velocidade longitudinal do robô [m/s]
            vy    : velocidade lateral do robô [m/s]
            omega : velocidade angular do robô [rad/s]

        Retorna:
            (w_esq, w_dir) em rad/s
        """

        if abs(vy) > 1e-9:
            raise ValueError(
                "Um robô diferencial não realiza movimento lateral puro."
            )

        r = self.raio_roda
        L = self.distancia_rodas

        w_esq = (vx - omega * L / 2.0) / r
        w_dir = (vx + omega * L / 2.0) / r

        return w_esq, w_dir

    def cinematica_direta(self, w_esq, w_dir):
        """
        Calcula a velocidade do robô a partir das velocidades das rodas.

        Retorna:
            (vx, vy, omega)
        """

        r = self.raio_roda
        L = self.distancia_rodas

        vx = r * (w_esq + w_dir) / 2.0
        vy = 0.0
        omega = r * (w_dir - w_esq) / L

        return vx, vy, omega
