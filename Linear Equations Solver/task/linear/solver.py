import numpy as np
import argparse
from copy import deepcopy


class LinearSolver:
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.n_variables = None
        self.n_equations = None
        self.n_significant_equations = None
        self.n_significant_variables = 0
        self.system = None
        self.solution = None
        self.is_complex = False
        self.get_infile_content_complex()
        self.a = None
        self.b = None
        self.row_1 = None
        self.row_2 = None
        self.simplify_system()
        self.find_significants()
        self.solve_system()
        self.output_solution()

    def solve_ax_eq_b(self):
        self.a, self.b = np.asarray(list(map(float, input().split())))
        print(self.b / self.a)

    def solve_x_y(self):
        self.row_1 = np.asarray(list(map(float, input().split())))
        self.row_2 = np.asarray(list(map(float, input().split())))

        self.row_2 = self.row_2 - self.row_1 * self.row_2[0] / self.row_1[0]
        y = self.row_2[2] / self.row_2[1]
        x = (self.row_1[2] - self.row_1[1] * y) / self.row_1[0]
        print(x, y)

    def get_infile_content_complex(self):
        with open(self.infile) as infile:
            content = infile.read()

        self.n_variables = int(content.split("\n")[0].split()[0])
        self.n_equations = int(content.split("\n")[0].split()[1])
        self.n_significant_equations = self.n_equations
        self.system = np.asarray([list(map(complex, content.split("\n")[i].split())) for i in range(1, self.n_equations + 1)])

        for equation in self.system:
            if any(x.imag != 0 for x in equation):
                self.is_complex = True
                break

    def simplify_system(self):
        for i in range(self.n_equations):
            for j in range(1, self.n_equations - i):

                if i + j < self.n_equations:
                    if self.system[i][i] == 0:
                        for k in range(i, self.n_equations):
                            if self.system[k][i] != 0:
                                self.system[i], self.system[k] = deepcopy((self.system[k], self.system[i]))
                                break
                    if self.system[i + j][i] == 0:
                        continue
                    self.system[i + j] = self.system[i + j] - self.system[i] * self.system[i + j][i] / self.system[i][i]

    def find_significants(self):
        for e, equation in enumerate(self.system):
            if all([var == 0 for var in equation]):
                self.n_significant_equations -= 1

        for col in self.system.transpose()[0:-1]:
            if any(x != 0 for x in col):
                self.n_significant_variables += 1

        for equation in self.system:
            if all(x == 0 for x in equation[0:-1]) and equation[-1] != 0:
                with open(self.outfile, "w") as outfile:
                    outfile.write("No solutions")
                exit()

        if self.n_significant_equations < self.n_significant_variables:
            with open(self.outfile, "w") as outfile:
                outfile.write(f"Infinitely many solutions\n{self.n_significant_equations, self.n_significant_variables}")
                exit()

    def solve_system(self):
        self.solution = np.array([complex(0) for _ in range(self.n_significant_variables)])
        for i in range(self.n_significant_equations - 1, -1, -1):
            first_term = self.system[i][-1]
            for j in range(self.n_significant_equations - 1, i, -1):
                first_term -= self.system[i][j] * self.solution[j]
            self.solution[i] = first_term / self.system[i][i]

    def output_solution(self):
        with open("out.txt", 'w') as outfile:
            if self.is_complex:
                outfile.write("\n".join(list(map(lambda x: "".join([str(round(x.real, 4)), str(round(x.imag, 4))]) + "j" if x.imag < 0 else "+".join([str(round(x.real, 4)), str(round(x.imag, 4))]) + "j", self.solution))))
            else:
                outfile.write("\n".join(list(map(lambda x: str(x.real), self.solution.tolist()))))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile")
    parser.add_argument("--outfile")
    args = parser.parse_args()
    _ = LinearSolver(args.infile, args.outfile)
