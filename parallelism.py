from multiprocessing import Process
import os


class Matrix:

    def __init__(self, A: str, B: str):
        self.A = self.read_matrix_file(A)
        self.B = self.read_matrix_file(B)
        self.C = [[0 for _ in range(len(self.A))] for _ in range(len(self.A))]
        self.processing()

    @staticmethod
    def read_matrix_file(filename: str) -> list:
        """
        Читаем файл получаем значения матрицы

        :param filename: имя файла
        :return: список значений матрицы
        """
        with open(filename, 'r', encoding='utf-8') as f:
            return [[int(i) for i in line.split(" ")] for line in f]

    def processing(self) -> None:
        """
        Работа с процессами

        :return: None
        """
        processes = []
        cells = []

        for i in range(len(self.A)):
            for j in range(len(self.A)):
                cells.append((i, j))
                
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'matrix_C.txt'))
        except FileNotFoundError:
            pass

        for i, j in cells:
            proc = Process(target=self.element, args=[i, j])
            processes.append(proc)

        for proc in processes:
            # print(proc.name)
            proc.start()
            proc.join()

    def element(self, i: int, j: int) -> list:
        """
        Умножение матрицы и запись значения в файл

        :param i: строка
        :param j: столбец
        :return: получаем матрицу с одним значением, которое вычислял процесс
        """
        self.C[i][j] = sum(self.A[i][m] * self.B[m][j] for m in range(len(self.A[0]) or len(self.B)))

        with open("matrix_C.txt", "a", encoding='utf-8') as f:
            if i == j == 0:
                f.write(str(self.C[i][j]) + " ")
            elif j == 0:
                f.write("\n" + str(self.C[i][j]) + " ")
            else:
                f.write(str(self.C[i][j]) + " ")

        return self.C


if __name__ == '__main__':
    result = Matrix(A="matrix_A.txt", B="matrix_B.txt")
