import turtle
import time
import random
from typing import List


class BinarySearchVisualizer:
    """Visualizador gráfico da busca binária usando Turtle."""

    # Configurações visuais
    SQUARE_SIZE = 40
    SPACING = 10
    MAX_PER_ROW = 15  # Máximo de elementos por linha
    TITLE_Y = 250
    INFO_Y = 220
    INTERVAL_Y = 190
    START_Y = 100

    COLORS = {
        "middle": "orange",
        "left": "lightgreen",
        "right": "lightpink",
        "inside": "lightblue",
        "outside": "gray",
        "found": "purple",
    }

    def __init__(self, values: List[int], target: int, delay: float = 1.5):
        self.values = sorted(values)
        self.target = target
        self.delay = delay
        self.screen = turtle.Screen()
        self.t = turtle.Turtle()

        self._setup_screen()

    def _setup_screen(self):
        """Configura a janela e o turtle."""
        self.screen.setup(1000, 700)
        self.screen.bgcolor("lightgray")
        self.screen.title("Busca Binária Visual com Turtle")
        self.screen.tracer(0)

        self.t.speed(0)
        self.t.hideturtle()

    def _draw_square(self, x: float, y: float, size: int, color: str, value: int, index: int):
        """Desenha um quadrado colorido com valor e índice."""
        t = self.t

        # Quadrado preenchido
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.fillcolor(color)
        t.begin_fill()
        for _ in range(4):
            t.forward(size)
            t.right(90)
        t.end_fill()

        # Borda
        t.pencolor("black")
        for _ in range(4):
            t.forward(size)
            t.right(90)

        # Valor
        t.penup()
        t.goto(x + size / 2, y + size / 2 - 8)
        t.write(str(value), align="center", font=("Arial", 12, "bold"))

        # Índice
        t.goto(x + size / 2, y - 20)
        t.write(str(index), align="center", font=("Arial", 10, "normal"))

    def _draw_info(self, step: int, left: int, right: int, middle: int):
        """Escreve informações do passo atual."""
        t = self.t
        t.penup()

        t.goto(0, self.TITLE_Y)
        t.write("BUSCA BINÁRIA VISUAL", align="center", font=("Arial", 20, "bold"))

        t.goto(0, self.INFO_Y)
        t.write(f"Alvo: {self.target} | Passo: {step}", align="center", font=("Arial", 16, "normal"))

        t.goto(0, self.INTERVAL_Y)
        t.write(
            f"Intervalo: [{left}, {right}] | Meio: {middle} = {self.values[middle]}",
            align="center",
            font=("Arial", 14, "normal"),
        )

    def _get_coordinates(self, index: int) -> tuple:
        """Retorna a coordenada (x, y) para desenhar o quadrado com base no índice."""
        row = index // self.MAX_PER_ROW
        col = index % self.MAX_PER_ROW

        total_cols = min(len(self.values), self.MAX_PER_ROW)
        total_width = total_cols * (self.SQUARE_SIZE + self.SPACING)

        x_start = -(total_width / 2) + self.SQUARE_SIZE / 2
        x = x_start + col * (self.SQUARE_SIZE + self.SPACING)
        y = self.START_Y - row * (self.SQUARE_SIZE + 60)  # descendo a cada linha

        return x, y

    def _draw_all(self, left: int, right: int, middle: int):
        """Desenha todos os quadrados representando a lista."""
        self.t.clear()

        for i, value in enumerate(self.values):
            x, y = self._get_coordinates(i)

            if i == middle:
                color = self.COLORS["middle"]
            elif i == left:
                color = self.COLORS["left"]
            elif i == right:
                color = self.COLORS["right"]
            elif left <= i <= right:
                color = self.COLORS["inside"]
            else:
                color = self.COLORS["outside"]

            self._draw_square(x, y, self.SQUARE_SIZE, color, value, i)

        self.screen.update()

    def run(self):
        """Executa a busca binária com visualização."""
        left, right = 0, len(self.values) - 1
        step = 0

        while left <= right:
            step += 1
            middle = (left + right) // 2

            self._draw_all(left, right, middle)
            self._draw_info(step, left, right, middle)
            self.screen.update()
            time.sleep(self.delay)

            if self.values[middle] == self.target:
                # Destacar alvo encontrado
                x, y = self._get_coordinates(middle)
                self._draw_square(x, y, self.SQUARE_SIZE, self.COLORS["found"], self.values[middle], middle)

                self.t.goto(0, -250)
                self.t.write(
                    f"🎯 ALVO ENCONTRADO! Posição: {middle}",
                    align="center",
                    font=("Arial", 18, "bold"),
                )

                self.screen.update()
                time.sleep(3)
                break

            elif self.values[middle] < self.target:
                left = middle + 1
            else:
                right = middle - 1

        self.screen.mainloop()


if __name__ == "__main__":
    # Gera lista aleatória
    tamanho = random.randint(10, 50)
    lista = random.sample(range(1, 1000), tamanho)  # valores únicos
    alvo = random.choice(lista)  # alvo garantido dentro da lista

    print(f"Lista ({tamanho} elementos): {sorted(lista)}")
    print(f"Alvo escolhido: {alvo}")

    visualizer = BinarySearchVisualizer(lista, alvo, delay=1.2)
    visualizer.run()
