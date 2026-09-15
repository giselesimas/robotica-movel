import math

from .robo import Robo


class RoboAckermann(Robo):
    """
    Modelo cinemático de um veículo com direção Ackermann.

    Convenções:
        vx    : velocidade longitudinal do veículo [m/s]
        vy    : velocidade lateral [m/s]
        omega : velocidade angular em torno do eixo vertical [rad/s]
    """

    def __init__(self, raio_roda, entre_eixos, bitola):
        super().__init__(raio_roda)

        if entre_eixos <= 0:
            raise ValueError(
                "A distância entre os eixos deve ser maior que zero."
            )

        if bitola <= 0:
            raise ValueError(
                "A bitola deve ser maior que zero."
            )

        self.entre_eixos = float(entre_eixos)
        self.bitola = float(bitola)

    def cinematica_inversa(self, vx, vy, omega):
        """
        Calcula velocidades das rodas e ângulos de esterçamento.

        Retorna:
            (
                w_traseira_esq,
                w_traseira_dir,
                w_dianteira_esq,
                w_dianteira_dir,
                delta_esq,
                delta_dir
            )
        """

        if abs(vy) > 1e-9:
            raise ValueError(
                "Um veículo Ackermann não realiza movimento lateral puro."
            )

        if abs(vx) < 1e-9 and abs(omega) > 1e-9:
            raise ValueError(
                "Um veículo Ackermann não gira no próprio eixo."
            )

        r = self.raio_roda
        L = self.entre_eixos
        B = self.bitola

        if abs(omega) < 1e-9:
            w = vx / r

            w_te = w
            w_td = w
            w_fe = w
            w_fd = w

            delta_esq = 0.0
            delta_dir = 0.0

        else:
            v_te = vx - omega * B / 2.0
            v_td = vx + omega * B / 2.0

            delta_esq = math.atan(
                omega * L / v_te
            )

            delta_dir = math.atan(
                omega * L / v_td
            )

            v_fe = v_te / math.cos(delta_esq)
            v_fd = v_td / math.cos(delta_dir)

            w_te = v_te / r
            w_td = v_td / r
            w_fe = v_fe / r
            w_fd = v_fd / r

        return (
            w_te,
            w_td,
            w_fe,
            w_fd,
            delta_esq,
            delta_dir
        )

    def cinematica_direta(
        self,
        w_te,
        w_td,
        w_fe=0.0,
        w_fd=0.0,
        delta_esq=0.0,
        delta_dir=0.0
    ):
        """
        Estima (vx, vy, omega) usando as rodas traseiras.

        Os parâmetros das rodas dianteiras são aceitos para manter
        simetria com a saída da cinemática inversa.
        """

        r = self.raio_roda
        B = self.bitola

        v_te = r * w_te
        v_td = r * w_td

        vx = (v_te + v_td) / 2.0
        vy = 0.0
        omega = (v_td - v_te) / B

        return vx, vy, omega
