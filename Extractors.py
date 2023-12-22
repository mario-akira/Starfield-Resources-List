import tkinter as tk
from tkinter import ttk
import json

# Carregar dados do arquivo JSON
with open('extratores.json', 'r') as json_file:
    extratores = json.load(json_file)

# Função para adicionar ingredientes


def adicionar_ingredientes():
    # Obter os valores selecionados nas caixas de combinação
    extrator_nome = extrator_combobox.get()
    tipo_selecionado = tipo_combobox.get()
    quantidade = quantidade_entry.get()

    # Verificar se a quantidade é um número inteiro
    try:
        quantidade = int(quantidade)
    except ValueError:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, "Quantidade deve ser um número inteiro.")
        return

    # Obter os ingredientes do extrator selecionado e do tipo selecionado
    extrator_key = f"{extrator_nome} - {tipo_selecionado}"
    ingredientes = extratores[extrator_key]['ingredients']

    # Adicionar a quantidade correspondente de cada ingrediente aos ingredientes totais
    for ingrediente, valor in ingredientes.items():
        total_ingredientes[ingrediente] = total_ingredientes.get(
            ingrediente, 0) + quantidade * valor

    # Adicionar a quantidade de itens à lista de itens adicionados
    total_itens_adicionados[extrator_key] = total_itens_adicionados.get(
        extrator_key, 0) + quantidade

    # Atualizar a exibição dos ingredientes e itens
    mostrar_ingredientes(total_ingredientes)
    mostrar_itens_adicionados(total_itens_adicionados)

    # Atualizar o rótulo de power total
    power_total = calcular_power_total()
    power_total_label.config(text=f"Power Total: {power_total}")

    # Atualizar os rótulos de tipo e extrator selecionados
    tipo_selecionado_label.config(
        text=f"Tipo Selecionado: {tipo_combobox.get()}")
    extrator_selecionado_label.config(
        text=f"Extrator Selecionado: {extrator_combobox.get()}")

# Função para calcular a energia total com base nas seleções
def calcular_power_total():
    power_total = 0
    for extrator, quantidade in total_itens_adicionados.items():
        extrator_nome, extrator_tipo = extrator.split(' - ')
        power_total += quantidade * extratores[extrator]['power']
    return power_total


# Função para exibir os ingredientes na interface gráfica


def mostrar_ingredientes(ingredientes):
    ingredientes_text.delete(1.0, tk.END)  # Limpar qualquer texto anterior
    for ingrediente, quantidade in ingredientes.items():
        ingredientes_text.insert(tk.END, f"{ingrediente}: {quantidade}\n")


# Função para exibir os itens adicionados na interface gráfica
def mostrar_itens_adicionados(itens):
    itens_text.delete(1.0, tk.END)  # Limpar qualquer texto anterior
    for extrator, quantidade in itens.items():
        extrator_nome, extrator_tipo = extrator.split(' - ')
        itens_text.insert(
            tk.END, f"{extrator_nome} - Tipo: {extrator_tipo}: {quantidade}\n")


# Criar a janela principal
janela = tk.Tk()
janela.title("Starfield - Resources List ")

# Definir largura e altura da janela
largura_janela = 652
altura_janela = 280
janela.geometry(f"{largura_janela}x{altura_janela}")

# Variáveis para armazenar os ingredientes totais
total_ingredientes = {}
total_itens_adicionados = {}

# Variáveis para armazenar o tipo e o extrator selecionados
tipo_selecionado = tk.StringVar()
extrator_selecionado = tk.StringVar()

# Criar uma lista única de tipos de extratores
tipos_extratores = list(
    set(extr.split(' - ')[0] for extr in extratores.keys()))

# Criar widgets
extrator_combobox = ttk.Combobox(janela, values=tipos_extratores)
extrator_combobox.set(tipos_extratores[0])
extrator_combobox.grid(column=0, row=0)

tipo_combobox = ttk.Combobox(
    janela, values=["Standard", "Commercial", "Industrial"])
tipo_combobox.set("Standard")
tipo_combobox.grid(column=1, row=0)

quantidade_label = tk.Label(janela, text="Quantidade:")
quantidade_label.grid(column=2, row=0)

quantidade_entry = tk.Entry(janela)
quantidade_entry.grid(column=3, row=0)

adicionar_button = tk.Button(
    janela, text="Adicionar", command=adicionar_ingredientes)
adicionar_button.grid(column=4, row=0)

# Rótulos para mostrar o tipo e o extrator selecionados
tipo_selecionado_label = tk.Label(janela, text="Tipo Selecionado: Standard")
tipo_selecionado_label.grid(column=1, row=2, columnspan=2)

extrator_selecionado_label = tk.Label(
    janela, text="Extrator Selecionado: Aldumite")
extrator_selecionado_label.grid(column=2, row=2, columnspan=3)

power_total_label = tk.Label(janela, text="Power Total: 0")
power_total_label.grid(column=0, row=4, columnspan=5)


# Resultado dos ingredientes
ingredientes_text = tk.Text(janela, height=10, width=40)
ingredientes_text.grid(column=0, row=3, columnspan=2)

# Itens adicionados
itens_text = tk.Text(janela, height=10, width=40)
itens_text.grid(column=2, row=3, columnspan=3)

# Iniciar a interface gráfica
janela.mainloop()
