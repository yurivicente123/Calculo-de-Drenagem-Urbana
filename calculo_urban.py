import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import time


class DrenagemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo de Drenagem Urbana")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.parametros_regiao = {
            "Acre": {"a": 700, "b": 15, "n": 0.85},
            "Alagoas": {"a": 850, "b": 10, "n": 0.75},
            "Amapá": {"a": 800, "b": 12, "n": 0.80},
            "Amazonas": {"a": 900, "b": 11, "n": 0.78},
            "Bahia": {"a": 950, "b": 13, "n": 0.82},
            "Ceará": {"a": 850, "b": 9, "n": 0.76},
            "Distrito Federal": {"a": 800, "b": 10, "n": 0.80},
            "Espírito Santo": {"a": 860, "b": 12, "n": 0.77},
            "Goiás": {"a": 880, "b": 14, "n": 0.79},
            "Maranhão": {"a": 900, "b": 15, "n": 0.81},
            "Mato Grosso": {"a": 950, "b": 11, "n": 0.83},
            "Mato Grosso do Sul": {"a": 900, "b": 12, "n": 0.80},
            "Minas Gerais": {"a": 800, "b": 10, "n": 0.78},
            "Pará": {"a": 920, "b": 13, "n": 0.84},
            "Paraíba": {"a": 860, "b": 9, "n": 0.75},
            "Paraná": {"a": 880, "b": 12, "n": 0.79},
            "Pernambuco": {"a": 850, "b": 10, "n": 0.77},
            "Piauí": {"a": 870, "b": 11, "n": 0.76},
            "Rio de Janeiro": {"a": 800, "b": 10, "n": 0.79},
            "Rio Grande do Norte": {"a": 820, "b": 12, "n": 0.78},
            "Rio Grande do Sul": {"a": 850, "b": 13, "n": 0.81},
            "Rondônia": {"a": 900, "b": 14, "n": 0.82},
            "Roraima": {"a": 950, "b": 10, "n": 0.79},
            "Santa Catarina": {"a": 850, "b": 12, "n": 0.80},
            "São Paulo": {"a": 800, "b": 10, "n": 0.8},
            "Sergipe": {"a": 860, "b": 11, "n": 0.77},
            "Tocantins": {"a": 880, "b": 12, "n": 0.79}
        }

        self.regioes = list(self.parametros_regiao.keys())
        
        self._configurar_layout()
        self._configurar_eventos()

    def _configurar_layout(self):
        """Configura o layout da interface gráfica"""
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TEntry", font=("Arial", 10))

        # Frames
        frame_inputs = ttk.LabelFrame(self.root, text="Parâmetros de Entrada", padding=10)
        frame_inputs.pack(fill="x", padx=10, pady=10)

        frame_buttons = ttk.Frame(self.root, padding=10)
        frame_buttons.pack(fill="x", padx=10, pady=10)

        frame_results = ttk.LabelFrame(self.root, text="Resultados", padding=10)
        frame_results.pack(fill="x", padx=10, pady=10)

        # Combobox para selecionar a região
        self.combo_regiao = ttk.Combobox(frame_inputs, values=self.regioes, state="readonly", width=30)
        self.combo_regiao.set("São Paulo")
        self.combo_regiao.grid(row=0, column=1, pady=5, padx=5)

        # Campos de entrada
        self.entry_area = self._criar_entry(frame_inputs, "Área (km²):", 1)
        self.entry_coef = self._criar_entry(frame_inputs, "Coeficiente (C):", 2)
        self.entry_a = self._criar_entry(frame_inputs, "Constante 'a':", 3)
        self.entry_b = self._criar_entry(frame_inputs, "Constante 'b':", 4)
        self.entry_n = self._criar_entry(frame_inputs, "Constante 'n':", 5)
        self.entry_tc = self._criar_entry(frame_inputs, "Tempo de Concentração (h):", 6)

        # Barra de progresso
        self.progress_bar = ttk.Progressbar(frame_results, length=300, mode="determinate")
        self.progress_bar.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
        self.progress_bar.grid_forget()

        # Labels para resultados
        self.result_label = ttk.Label(frame_results, text="Vazão: -", font=("Arial", 12, "bold"))
        self.result_label.grid(row=0, column=0, padx=5, pady=5)

        self.intensidade_label = ttk.Label(frame_results, text="Intensidade: -", font=("Arial", 12, "bold"))
        self.intensidade_label.grid(row=0, column=1, padx=5, pady=5)

        # Botões
        ttk.Button(frame_buttons, text="Calcular", command=self.calcular_vazao).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(frame_buttons, text="Exportar Resultados", command=self.exportar_csv).grid(row=0, column=1, padx=10, pady=10)

    def _criar_entry(self, frame, label_text, row):
        """Método auxiliar para criar labels e campos de entrada de forma reutilizável"""
        ttk.Label(frame, text=label_text).grid(row=row, column=0, padx=5, pady=5)
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def _configurar_eventos(self):
        """Configura eventos, como a atualização dos parâmetros de acordo com a região selecionada"""
        self.combo_regiao.bind("<<ComboboxSelected>>", self.atualizar_parametros)

    def carregar_parametros(self, regiao):
        """Carrega os parâmetros para a região selecionada"""
        return self.parametros_regiao.get(regiao, {"a": 0, "b": 0, "n": 0})

    def atualizar_parametros(self, event):
        """Atualiza os campos de entrada com os parâmetros da região selecionada"""
        regiao = self.combo_regiao.get()
        parametros = self.carregar_parametros(regiao)

        self.entry_a.delete(0, tk.END)
        self.entry_a.insert(0, parametros["a"])

        self.entry_b.delete(0, tk.END)
        self.entry_b.insert(0, parametros["b"])

        self.entry_n.delete(0, tk.END)
        self.entry_n.insert(0, parametros["n"])

    def calcular_vazao(self):
        """Calcula e exibe os resultados"""
        try:
            # Limpar resultados anteriores
            self.result_label.config(text="Vazão: -")
            self.intensidade_label.config(text="Intensidade: -")

            # Exibe a barra de progresso
            self.progress_bar.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
            self.progress_bar["value"] = 0
            self.root.update_idletasks()

            # Simula o cálculo
            time.sleep(1)

            # Obtenção dos dados
            area = float(self.entry_area.get()) * 10**6
            coef = float(self.entry_coef.get())
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            n = float(self.entry_n.get())
            tc = float(self.entry_tc.get())

            # Cálculos
            intensidade = a / ((tc + b) ** n)
            intensidade_m_s = intensidade / 3600
            vazao = coef * intensidade_m_s * area

            # Atualiza os resultados
            self.result_label.config(text=f"Vazão: {vazao:.2f} m³/s")
            self.intensidade_label.config(text=f"Intensidade: {intensidade:.2f} mm/h")

            # Esconde a barra de progresso
            self.progress_bar.grid_forget()

        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida. Verifique os valores inseridos.\n{str(e)}")
    
    def exportar_csv(self):
        """Exporta os resultados para um arquivo CSV"""
        resultado_vazao = self.result_label.cget("text")
        resultado_intensidade = self.intensidade_label.cget("text")
        
        if resultado_vazao == "Vazão: -" or resultado_intensidade == "Intensidade: -":
            messagebox.showwarning("Erro", "Por favor, calcule os resultados antes de exportar.")
            return

        # Salvar em arquivo CSV
        try:
            with filedialog.asksaveasfile(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]) as file:
                writer = csv.writer(file)
                writer.writerow(["Região", "Vazão (m³/s)", "Intensidade (mm/h)"])
                writer.writerow([self.combo_regiao.get(), resultado_vazao.split(": ")[1], resultado_intensidade.split(": ")[1]])
                messagebox.showinfo("Exportado", "Resultados exportados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao exportar os resultados.\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DrenagemApp(root)
    root.mainloop()

