import tkinter as tk
from solver import parse_expression, solve_polynomial, solve_nonpolynomial, solve_linear_system, verify_roots, \
    generate_initial_guesses, preprocess_expression, calculate_determinant, calculate_inverse, calculate_transpose, \
    calculate_rank, matrix_power, multiply_matrices, calculate_eigenvalues_and_vectors, test_nonlinear_solution, \
    test_linear_solution
import sympy as sp


class EquationSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("多功能计算器")
        self.create_widgets()
        self.update_ui()  # 初始化时调用一次更新UI以设置默认状态

    def create_widgets(self):
        self.mode = tk.StringVar(value="nonlinear")  # 设置默认模式为非线性方程

        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack(pady=10)

        self.nonlinear_radio = tk.Radiobutton(self.mode_frame, text="非线性方程", variable=self.mode, value="nonlinear",
                                              command=self.update_ui)
        self.nonlinear_radio.pack(side=tk.LEFT, padx=10)
        self.linear_radio = tk.Radiobutton(self.mode_frame, text="线性方程组", variable=self.mode, value="linear",
                                           command=self.update_ui)
        self.linear_radio.pack(side=tk.LEFT, padx=10)
        self.matrix_radio = tk.Radiobutton(self.mode_frame, text="矩阵运算", variable=self.mode, value="matrix",
                                           command=self.update_ui)
        self.matrix_radio.pack(side=tk.LEFT, padx=10)

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)

        self.equation_label = tk.Label(self.input_frame, text="输入非线性方程表达式")
        self.equation_label.pack()

        self.equation_text = tk.Text(self.input_frame, width=50, height=10)
        self.equation_text.pack()

        self.linear_dim_frame = tk.Frame(self.input_frame)
        self.linear_var_label = tk.Label(self.linear_dim_frame, text="输入变量个数：")
        self.linear_var_label.pack(side=tk.LEFT)
        self.linear_var_entry = tk.Entry(self.linear_dim_frame, width=5)
        self.linear_var_entry.pack(side=tk.LEFT)
        self.linear_dim_button = tk.Button(self.linear_dim_frame, text="确定", command=self.create_linear_entries)
        self.linear_dim_button.pack(side=tk.LEFT)
        self.linear_dim_frame.pack(pady=10)

        self.linear_frame = tk.Frame(self.input_frame)

        self.matrix_dim_frame = tk.Frame(self.input_frame)
        self.matrix_dim_label = tk.Label(self.matrix_dim_frame, text="输入矩阵维度：")
        self.matrix_dim_label.pack(side=tk.LEFT)
        self.matrix_dim_entry = tk.Entry(self.matrix_dim_frame, width=5)
        self.matrix_dim_entry.pack(side=tk.LEFT)
        self.matrix_dim_button = tk.Button(self.matrix_dim_frame, text="确定", command=self.create_matrix_entries)
        self.matrix_dim_button.pack(side=tk.LEFT)
        self.matrix_dim_frame.pack(pady=10)

        self.matrix_frame = tk.Frame(self.input_frame)
        self.matrix_power_frame = tk.Frame(self.input_frame)
        self.power_label = tk.Label(self.matrix_power_frame, text="输入矩阵幂次：")
        self.power_label.pack(side=tk.LEFT)
        self.power_entry = tk.Entry(self.matrix_power_frame, width=5)
        self.power_entry.pack(side=tk.LEFT)

        self.matrix_multiply_frame = tk.Frame(self.input_frame)
        self.multiply_a_label = tk.Label(self.matrix_multiply_frame, text="输入A矩阵的行数和列数：")
        self.multiply_a_label.pack(side=tk.LEFT)
        self.multiply_a_row_entry = tk.Entry(self.matrix_multiply_frame, width=5)
        self.multiply_a_row_entry.pack(side=tk.LEFT)
        self.multiply_a_col_entry = tk.Entry(self.matrix_multiply_frame, width=5)
        self.multiply_a_col_entry.pack(side=tk.LEFT)
        self.multiply_b_label = tk.Label(self.matrix_multiply_frame, text="输入B矩阵的列数：")
        self.multiply_b_label.pack(side=tk.LEFT)
        self.multiply_b_col_entry = tk.Entry(self.matrix_multiply_frame, width=5)
        self.multiply_b_col_entry.pack(side=tk.LEFT)
        self.multiply_button = tk.Button(self.matrix_multiply_frame, text="确定", command=self.create_matrix_multiply_entries)
        self.multiply_button.pack(side=tk.LEFT)

        self.operation_frame = tk.Frame(self.input_frame)
        self.operation_frame.pack(pady=10)

        self.operation_label = tk.Label(self.operation_frame, text="选择矩阵运算：")
        self.operation_label.pack(side=tk.LEFT)
        self.operation = tk.StringVar(value="determinant")
        self.determinant_radio = tk.Radiobutton(self.operation_frame, text="行列式", variable=self.operation, value="determinant")
        self.determinant_radio.pack(side=tk.LEFT, padx=5)
        self.inverse_radio = tk.Radiobutton(self.operation_frame, text="逆矩阵", variable=self.operation, value="inverse")
        self.inverse_radio.pack(side=tk.LEFT, padx=5)
        self.transpose_radio = tk.Radiobutton(self.operation_frame, text="转置矩阵", variable=self.operation, value="transpose")
        self.transpose_radio.pack(side=tk.LEFT, padx=5)
        self.rank_radio = tk.Radiobutton(self.operation_frame, text="矩阵秩", variable=self.operation, value="rank")
        self.rank_radio.pack(side=tk.LEFT, padx=5)
        self.power_radio = tk.Radiobutton(self.operation_frame, text="矩阵幂", variable=self.operation, value="power")
        self.power_radio.pack(side=tk.LEFT, padx=5)
        self.multiply_radio = tk.Radiobutton(self.operation_frame, text="矩阵乘法", variable=self.operation, value="multiply")
        self.multiply_radio.pack(side=tk.LEFT, padx=5)
        self.eigen_radio = tk.Radiobutton(self.operation_frame, text="特征值和特征向量", variable=self.operation, value="eigen")
        self.eigen_radio.pack(side=tk.LEFT, padx=5)

        self.button_frame = tk.Frame(self.root)
        self.solve_button = tk.Button(self.button_frame, text="求解", command=self.solve)
        self.solve_button.pack(side=tk.LEFT, padx=10)

        self.test_button = tk.Button(self.button_frame, text="测试验证", command=self.test_solution)
        self.test_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(self.button_frame, text="清空", command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.quit_button = tk.Button(self.button_frame, text="退出", command=self.root.quit)
        self.quit_button.pack(side=tk.LEFT, padx=10)

        self.button_frame.pack(pady=10)

        self.output_frame = tk.Frame(self.root)
        self.output_label = tk.Label(self.output_frame, text="输出结果")
        self.output_label.pack()

        self.output_text = tk.Text(self.output_frame, width=50, height=10, state=tk.DISABLED)
        self.output_text.pack()

        self.output_frame.pack()

    def update_ui(self):
        self.clear_text()  # 切换模式时清空输入和输出区域
        self.equation_text.pack_forget()
        self.linear_dim_frame.pack_forget()
        self.linear_frame.pack_forget()
        self.matrix_dim_frame.pack_forget()
        self.matrix_frame.pack_forget()
        self.operation_frame.pack_forget()
        self.matrix_power_frame.pack_forget()
        self.matrix_multiply_frame.pack_forget()

        if self.mode.get() == "nonlinear":
            self.equation_label.config(text="输入非线性方程表达式")
            self.equation_text.pack()
        elif self.mode.get() == "linear":
            self.equation_label.config(text="输入变量个数并填写系数矩阵")
            self.linear_dim_frame.pack()
            self.linear_frame.pack()
        else:
            self.equation_label.config(text="输入矩阵维度并选择运算类型")
            self.matrix_dim_frame.pack()
            self.matrix_frame.pack()
            self.operation_frame.pack()

            operation = self.operation.get()
            if operation == "power":
                self.matrix_power_frame.pack()
            elif operation == "multiply":
                self.matrix_multiply_frame.pack()

    def clear_text(self):
        self.equation_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        for widget in self.linear_frame.winfo_children():
            widget.destroy()
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

    def create_linear_entries(self):
        try:
            var_count = int(self.linear_var_entry.get())
            if var_count <= 0:
                raise ValueError("变量个数必须是正整数。")
            self.linear_entries = []
            for i in range(var_count):
                row_entries = []
                for j in range(var_count + 1):  # 最后一列为常数项
                    if j == var_count:
                        entry_label = tk.Label(self.linear_frame, text="常数项")
                    else:
                        entry_label = tk.Label(self.linear_frame, text=f"变量{j + 1}")
                    entry_label.grid(row=i * 2, column=j, padx=5, pady=5)
                    entry = tk.Entry(self.linear_frame, width=5)
                    entry.grid(row=i * 2 + 1, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                self.linear_entries.append(row_entries)
            self.linear_frame.pack()
        except ValueError as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"错误: {str(e)}\n")
            self.output_text.config(state=tk.DISABLED)

    def create_matrix_entries(self):
        try:
            dim = int(self.matrix_dim_entry.get())
            if dim <= 0:
                raise ValueError("维度必须是正整数。")
            self.matrix_entries = []
            for i in range(dim):
                row_entries = []
                for j in range(dim):
                    entry_label = tk.Label(self.matrix_frame, text=f"a{i + 1}{j + 1}")
                    entry_label.grid(row=i * 2, column=j, padx=5, pady=5)
                    entry = tk.Entry(self.matrix_frame, width=5)
                    entry.grid(row=i * 2 + 1, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)
            self.matrix_frame.pack()
        except ValueError as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"错误: {str(e)}\n")
            self.output_text.config(state=tk.DISABLED)

    def create_matrix_multiply_entries(self):
        try:
            a_rows = int(self.multiply_a_row_entry.get())
            a_cols = int(self.multiply_a_col_entry.get())
            b_cols = int(self.multiply_b_col_entry.get())
            if a_rows <= 0 or a_cols <= 0 or b_cols <= 0:
                raise ValueError("行数和列数必须是正整数。")
            self.matrix_a_entries = []
            self.matrix_b_entries = []
            for i in range(a_rows):
                row_entries = []
                for j in range(a_cols):
                    entry_label = tk.Label(self.matrix_frame, text=f"A{i + 1}{j + 1}")
                    entry_label.grid(row=i * 2, column=j, padx=5, pady=5)
                    entry = tk.Entry(self.matrix_frame, width=5)
                    entry.grid(row=i * 2 + 1, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                self.matrix_a_entries.append(row_entries)
            for i in range(a_cols):
                row_entries = []
                for j in range(b_cols):
                    entry_label = tk.Label(self.matrix_frame, text=f"B{i + 1}{j + 1}")
                    entry_label.grid(row=i * 2 + a_rows * 2, column=j, padx=5, pady=5)
                    entry = tk.Entry(self.matrix_frame, width=5)
                    entry.grid(row=i * 2 + 1 + a_rows * 2, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                self.matrix_b_entries.append(row_entries)
            self.matrix_frame.pack()
        except ValueError as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"错误: {str(e)}\n")
            self.output_text.config(state=tk.DISABLED)

    def get_matrix_from_entries(self, matrix_entries):
        matrix = []
        for row_entries in matrix_entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                try:
                    row.append(float(value))
                except ValueError:
                    row.append(0.0)
            matrix.append(row)
        return matrix

    def display_matrix(self, matrix, entries):
        for i, row in enumerate(matrix.tolist()):
            for j, value in enumerate(row):
                entry = entries[i][j]
                entry.delete(0, tk.END)
                entry.insert(0, str(value))

    def solve(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        try:
            if self.mode.get() == "matrix":
                matrix = self.get_matrix_from_entries(self.matrix_entries)
                operation = self.operation.get()
                if operation == "determinant":
                    result = calculate_determinant(matrix)
                    self.output_text.insert(tk.END, f"行列式的结果为: {result}")
                elif operation == "inverse":
                    result = calculate_inverse(matrix)
                    self.display_matrix(result, self.matrix_entries)
                elif operation == "transpose":
                    result = calculate_transpose(matrix)
                    self.display_matrix(result, self.matrix_entries)
                elif operation == "rank":
                    result = calculate_rank(matrix)
                    self.output_text.insert(tk.END, f"矩阵秩的结果为: {result}")
                elif operation == "power":
                    power = int(self.power_entry.get())
                    result = matrix_power(matrix, power)
                    self.display_matrix(result, self.matrix_entries)
                elif operation == "multiply":
                    matrix_b = self.get_matrix_from_entries(self.matrix_b_entries)
                    result = multiply_matrices(matrix, matrix_b)
                    self.display_matrix(result, self.matrix_a_entries)
                elif operation == "eigen":
                    eigenvalues, eigenvectors = calculate_eigenvalues_and_vectors(matrix)
                    self.output_text.insert(tk.END, f"特征值为: {eigenvalues}\n")
                    self.output_text.insert(tk.END, f"特征向量为: {eigenvectors}")
            else:
                equations = []
                if self.mode.get() == "linear":
                    coefficients = []
                    constants = []
                    for row_entries in self.linear_entries:
                        row = []
                        for j, entry in enumerate(row_entries):
                            value = float(entry.get())
                            if j == len(row_entries) - 1:
                                constants.append(value)
                            else:
                                row.append(value)
                        coefficients.append(row)
                    symbols = sp.symbols(f'x1:{len(coefficients[0]) + 1}')
                    system = [sum(coeff * symbol for coeff, symbol in zip(row, symbols)) - const
                              for row, const in zip(coefficients, constants)]
                    solutions = sp.linsolve(system, *symbols)
                    solutions = list(solutions)[0]
                    results_str = "\n".join([f"{symbol} = {value}" for symbol, value in zip(symbols, solutions)])
                    self.output_text.insert(tk.END, f"方程组的解为:\n{results_str}")
                else:
                    equations_text = self.equation_text.get("1.0", tk.END).strip()
                    equations_lines = equations_text.splitlines()
                    for line in equations_lines:
                        if '=' in line:
                            left, right = line.split('=')
                            eq = sp.sympify(preprocess_expression(f"({left}) - ({right})"))
                        else:
                            eq = sp.sympify(preprocess_expression(line))
                        equations.append(eq)

                    if self.mode.get() == "nonlinear" and len(equations) == 1:
                        expr, symbol, coeffs, is_polynomial = parse_expression(equations_lines[0])

                        if is_polynomial:
                            roots = solve_polynomial(coeffs)
                        else:
                            func = sp.lambdify(symbol, expr, 'numpy')
                            initial_guesses = generate_initial_guesses(50, 0.1, 10)
                            roots = solve_nonpolynomial(func, initial_guesses)

                        verified_roots = verify_roots(roots, expr, symbol)
                        if verified_roots:
                            results_str = "\n".join([f"{symbol}{i + 1}: {root}" for i, root in enumerate(verified_roots)])
                            results_str = results_str.replace('j', 'i')
                            self.output_text.insert(tk.END, f"方程的根为:\n{results_str}")
                        else:
                            self.output_text.insert(tk.END, "方程没有实数根。")
                    else:
                        raise ValueError("请确保输入一个非线性方程或多个线性方程组。")
        except Exception as e:
            self.output_text.insert(tk.END, f"错误: {str(e)}")

        self.output_text.config(state=tk.DISABLED)

    def test_solution(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        try:
            if self.mode.get() == "linear":
                coefficients = []
                constants = []
                for row_entries in self.linear_entries:
                    row = []
                    for j, entry in enumerate(row_entries):
                        value = float(entry.get())
                        if j == len(row_entries) - 1:
                            constants.append(value)
                        else:
                            row.append(value)
                    coefficients.append(row)
                symbols = sp.symbols(f'x1:{len(coefficients[0]) + 1}')
                system = [sum(coeff * symbol for coeff, symbol in zip(row, symbols)) - const
                          for row, const in zip(coefficients, constants)]
                solutions = sp.linsolve(system, *symbols)
                solutions = list(solutions)[0]

                test_results = test_linear_solution(coefficients, constants, solutions)
                results_str = "\n".join([f"方程 {i} {'通过' if passed else '未通过'}" for i, passed in test_results.items()])
                self.output_text.insert(tk.END, f"线性方程组测试结果:\n{results_str}")

            elif self.mode.get() == "nonlinear":
                equations_text = self.equation_text.get("1.0", tk.END).strip()
                equations_lines = equations_text.splitlines()
                if len(equations_lines) != 1:
                    raise ValueError("请确保输入一个非线性方程。")

                expr, symbol, coeffs, is_polynomial = parse_expression(equations_lines[0])

                if is_polynomial:
                    roots = solve_polynomial(coeffs)
                else:
                    func = sp.lambdify(symbol, expr, 'numpy')
                    initial_guesses = generate_initial_guesses(50, 0.1, 10)
                    roots = solve_nonpolynomial(func, initial_guesses)

                verified_roots = verify_roots(roots, expr, symbol)
                test_results = test_nonlinear_solution(expr, symbol, verified_roots)
                results_str = "\n".join([f"根 {root} {'通过' if passed else '未通过'}" for root, passed in test_results.items()])
                self.output_text.insert(tk.END, f"非线性方程测试结果:\n{results_str}")

            else:
                self.output_text.insert(tk.END, "此功能仅适用于非线性方程和线性方程组的测试验证。")

        except Exception as e:
            self.output_text.insert(tk.END, f"错误: {str(e)}")

        self.output_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = EquationSolverApp(root)
    root.mainloop()