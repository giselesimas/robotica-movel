from .robo import Robo


class RoboMecanum(Robo):
    """
    Modelo cinemático de um robô com quatro rodas Mecanum.

    Ordem das rodas utilizada nesta implementação:

        1. frente-direita
        2. frente-esquerda
        3. traseira-direita
        4. traseira-esquerda

    Essa ordem corresponde aos motores wheel1, wheel2, wheel3 e wheel4
    do KUKA youBot usado no projeto.
    """

    def __init__(self, raio_roda, lx, ly):
        super().__init__(raio_roda)

        if lx <= 0:
            raise ValueError("lx deve ser maior que zero.")

        if ly <= 0:
            raise ValueError("ly deve ser maior que zero.")

        self.lx = float(lx)
        self.ly = float(ly)

    def cinematica_inversa(self, vx, vy, omega):
        """
        Calcula as velocidades angulares das quatro rodas.

        Retorna:
            (w_fd, w_fe, w_td, w_te)
        """

        r = self.raio_roda
        k = self.lx + self.ly

        w_fd = (vx + vy + k * omega) / r
        w_fe = (vx - vy - k * omega) / r
        w_td = (vx - vy + k * omega) / r
        w_te = (vx + vy - k * omega) / r

        return w_fd, w_fe, w_td, w_te

    def cinematica_direta(self, w_fd, w_fe, w_td, w_te):
        """
        Calcula a velocidade do robô a partir das velocidades das rodas.

        Retorna:
            (vx, vy, omega)
        """

        r = self.raio_roda
        k = self.lx + self.ly

        vx = r * (w_fd + w_fe + w_td + w_te) / 4.0

        vy = r * (
            w_fd
            - w_fe
            - w_td
            + w_te
        ) / 4.0

        omega = r * (
            w_fd
            - w_fe
            + w_td
            - w_te
        ) / (4.0 * k)

        return vx, vy, omega
