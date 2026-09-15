class Robo:
    """Classe base para os modelos cinemáticos dos robôs móveis."""

    def __init__(self, raio_roda):
        if raio_roda <= 0:
            raise ValueError("O raio da roda deve ser maior que zero.")

        self.raio_roda = float(raio_roda)

    def cinematica_direta(self, *velocidades_rodas):
        """Calcula (vx, vy, omega) a partir das velocidades das rodas."""
        raise NotImplementedError(
            "A cinemática direta deve ser implementada pela classe derivada."
        )

    def cinematica_inversa(self, vx, vy, omega):
        """Calcula as velocidades das rodas a partir de (vx, vy, omega)."""
        raise NotImplementedError(
            "A cinemática inversa deve ser implementada pela classe derivada."
        )
