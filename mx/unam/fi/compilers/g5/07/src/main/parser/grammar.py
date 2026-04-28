import tkinter as tk
from tkinter import scrolledtext

class Grammar:
    def __init__(self):
        # 1. Terminales
        self.terminals = {
            'id', 'constant', 'literal', 'int', 'float', 'double', 'char', 'void',
            'if', 'else', 'return', '=', ';', ',', '(', ')', '{', '}',
            '+', '-', '*', '/', '%', '==', '!=', '>', '>=', '<', '<=', '&&', '||', '!'
        }

        # 2. No Terminales
        self.non_terminals = {
            'PROGRAM', 'GLOBAL_LIST', 'GLOBAL', 'TYPE', 'GLOBAL_REST',
            'STMT_LIST', 'STMT', 'STMT_ID_REST', 'IF_STMT', 'ELSE_PART',
            'OPT_E', 'OPT_ASSIGN_LOCAL', 'ARG_LIST_OPT', 'ARG_LIST', 'ARG_LIST_PRIME',
            'E', 'LOGIC_OR', 'LOGIC_OR_PRIME', 'LOGIC_AND', 'LOGIC_AND_PRIME',
            'EQUALITY', 'EQUALITY_PRIME', 'COMPARISON', 'COMPARISON_PRIME',
            'TERM', 'TERM_PRIME', 'FACTOR', 'FACTOR_PRIME', 'UNARY', 
            'PRIMARY', 'PRIMARY_ID_REST'
        }

        self.start_symbol = 'PROGRAM'

        # 3. Producciones (Diccionario NoTerminal -> Lista de Listas)
        self.productions = {
            'PROGRAM': [['GLOBAL_LIST']],
            'GLOBAL_LIST': [['GLOBAL', 'GLOBAL_LIST'], ['epsilon']],
            'GLOBAL': [['TYPE', 'id', 'GLOBAL_REST']],
            'TYPE': [['int'], ['float'], ['double'], ['char'], ['void']],
            'GLOBAL_REST': [['(', ')', '{', 'STMT_LIST', '}'], ['OPT_ASSIGN', ';']],
            'STMT_LIST': [['STMT', 'STMT_LIST'], ['epsilon']],
            'STMT': [['IF_STMT'], ['return', 'OPT_E', ';'], ['TYPE', 'id', 'OPT_ASSIGN_LOCAL', ';'], ['id', 'STMT_ID_REST']],
            'STMT_ID_REST': [['=', 'E', ';'], ['(', 'ARG_LIST_OPT', ')', ';']],
            'IF_STMT': [['if', '(', 'E', ')', '{', 'STMT_LIST', '}', 'ELSE_PART']],
            'ELSE_PART': [['else', '{', 'STMT_LIST', '}'], ['epsilon']],
            'ARG_LIST_OPT': [['ARG_LIST'], ['epsilon']],
            'ARG_LIST': [['E', 'ARG_LIST_PRIME']],
            'ARG_LIST_PRIME': [[',', 'E', 'ARG_LIST_PRIME'], ['epsilon']],
            'E': [['LOGIC_OR']],
            'LOGIC_OR': [['LOGIC_AND', 'LOGIC_OR_PRIME']],
            'LOGIC_OR_PRIME': [['||', 'LOGIC_AND', 'LOGIC_OR_PRIME'], ['epsilon']],
            'LOGIC_AND': [['EQUALITY', 'LOGIC_AND_PRIME']],
            'LOGIC_AND_PRIME': [['&&', 'EQUALITY', 'LOGIC_AND_PRIME'], ['epsilon']],
            'EQUALITY': [['COMPARISON', 'EQUALITY_PRIME']],
            'EQUALITY_PRIME': [['==', 'COMPARISON', 'EQUALITY_PRIME'], ['!=', 'COMPARISON', 'EQUALITY_PRIME'], ['epsilon']],
            'COMPARISON': [['TERM', 'COMPARISON_PRIME']],
            'COMPARISON_PRIME': [['op_rel', 'TERM', 'COMPARISON_PRIME'], ['epsilon']],
            'TERM': [['FACTOR', 'TERM_PRIME']],
            'TERM_PRIME': [['+', 'FACTOR', 'TERM_PRIME'], ['-', 'FACTOR', 'TERM_PRIME'], ['epsilon']],
            'FACTOR': [['UNARY', 'FACTOR_PRIME']],
            'FACTOR_PRIME': [['*', 'UNARY', 'FACTOR_PRIME'], ['/', 'UNARY', 'FACTOR_PRIME'], ['%', 'UNARY', 'FACTOR_PRIME'], ['epsilon']],
            'UNARY': [['!', 'UNARY'], ['-', 'UNARY'], ['PRIMARY']],
            'PRIMARY': [['id', 'PRIMARY_ID_REST'], ['constant'], ['literal'], ['(', 'E', ')']],
            'PRIMARY_ID_REST': [['(', 'ARG_LIST_OPT', ')'], ['epsilon']]
        }

    def display_in_window(self):
        """ Crea una ventana de Tkinter para mostrar la gramática """
        root = tk.Tk()
        root.title("Especificación de Gramática C-Pure - Equipo 7")
        root.geometry("600x700")

        # Título
        label = tk.Label(root, text="Gramática Formal (BNF)", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        # Área de texto con scroll
        text_area = scrolledtext.ScrolledText(root, width=70, height=35, font=("Courier New", 10))
        text_area.pack(padx=20, pady=10)

        # Formatear las reglas para que se vean bien
        grammar_text = f"Initial Symbol: {self.start_symbol}\n"

        for nt, prods in self.productions.items():
            formatted_prods = " | ".join([" ".join(p) for p in prods])
            grammar_text += f"<{nt}> ::= {formatted_prods}\n\n"

        text_area.insert(tk.INSERT, grammar_text)
        text_area.configure(state='disabled') # Hacerlo solo lectura

        root.mainloop()

if __name__ == "__main__":
    g = Grammar()
    g.display_in_window()