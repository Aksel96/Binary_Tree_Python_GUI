# Aksel Villela
# MIT License
# 10/23/2023

import tkinter as tk


class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1


class AVL:
    def __init__(self):
        self.raiz = None

    def altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def balance(self, nodo):
        if nodo is None:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

    def rotacion_izquierda(self, nodo):
        nueva_raiz = nodo.derecha
        nodo.derecha = nueva_raiz.izquierda
        nueva_raiz.izquierda = nodo
        nodo.altura = 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))
        nueva_raiz.altura = 1 + max(self.altura(nueva_raiz.izquierda), self.altura(nueva_raiz.derecha))
        return nueva_raiz

    def rotacion_derecha(self, nodo):
        nueva_raiz = nodo.izquierda
        nodo.izquierda = nueva_raiz.derecha
        nueva_raiz.derecha = nodo
        nodo.altura = 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))
        nueva_raiz.altura = 1 + max(self.altura(nueva_raiz.izquierda), self.altura(nueva_raiz.derecha))
        return nueva_raiz

    def insertar(self, nodo, valor):
        if nodo is None:
            return NodoAVL(valor)
        if valor < nodo.valor:
            nodo.izquierda = self.insertar(nodo.izquierda, valor)
        else:
            nodo.derecha = self.insertar(nodo.derecha, valor)
        nodo.altura = 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))
        balance = self.balance(nodo)

        if balance > 1:
            if valor < nodo.izquierda.valor:
                return self.rotacion_derecha(nodo)
            else:
                nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
                return self.rotacion_derecha(nodo)
        if balance < -1:
            if valor > nodo.derecha.valor:
                return self.rotacion_izquierda(nodo)
            else:
                nodo.derecha = self.rotacion_derecha(nodo.derecha)
                return self.rotacion_izquierda(nodo)
        return nodo

    def eliminar(self, nodo, valor):
        if nodo is None:
            return nodo

        if valor < nodo.valor:
            nodo.izquierda = self.eliminar(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self.eliminar(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda

            temp = self.nodo_menor_valor(nodo.derecha)
            nodo.valor = temp.valor
            nodo.derecha = self.eliminar(nodo.derecha, temp.valor)

        if nodo is None:
            return nodo

        nodo.altura = 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))
        balance = self.balance(nodo)

        if balance > 1:
            if valor < nodo.izquierda.valor:
                return self.rotacion_derecha(nodo)
            else:
                nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
                return self.rotacion_derecha(nodo)
        if balance < -1:
            if valor > nodo.derecha.valor:
                return self.rotacion_izquierda(nodo)
            else:
                nodo.derecha = self.rotacion_derecha(nodo.derecha)
                return self.rotacion_izquierda(nodo)
        return nodo

    def nodo_menor_valor(self, nodo):
        if nodo.izquierda is None:
            return nodo
        return self.nodo_menor_valor(nodo.izquierda)


def eliminar_nodo():
    valor = int(entry.get())
    avl_tree.raiz = avl_tree.eliminar(avl_tree.raiz, valor)
    tree_visualizer.canvas.delete("all")  # Borra el lienzo actual
    tree_visualizer.draw_tree(avl_tree.raiz, 600, 50, 200)


def insertar_nodo():
    valor = int(entry.get())
    avl_tree.raiz = avl_tree.insertar(avl_tree.raiz, valor)
    tree_visualizer.canvas.delete("all")  # Borra el lienzo actual
    tree_visualizer.draw_tree(avl_tree.raiz, 600, 50, 200)


class TreeVisualizer:
    def __init__(self, root, avl_tree):
        self.root = root
        self.avl_tree = avl_tree
        self.canvas = tk.Canvas(root, width=1200, height=600)
        self.canvas.pack()
        self.canvas.configure(background="black")
        self.draw_tree(avl_tree.raiz, 600, 50, 200)

    def draw_tree(self, nodo, x, y, horizontal_spacing):
        if nodo:
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white")
            self.canvas.create_text(x, y, text=str(nodo.valor))
            if nodo.izquierda:
                x_left = x - horizontal_spacing
                y_left = y + 50
                self.canvas.create_line(x, y, x_left, y_left, fill="white")
                self.draw_tree(nodo.izquierda, x_left, y_left, horizontal_spacing / 2)
            if nodo.derecha:
                x_right = x + horizontal_spacing
                y_right = y + 50
                self.canvas.create_line(x, y, x_right, y_right, fill="white")
                self.draw_tree(nodo.derecha, x_right, y_right, horizontal_spacing / 2)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Árbol Binario AVL")
    avl_tree = AVL()
    root.configure(bg="black")

    valores = [15, 6, 50, 4, 23, 7, 72, 5, 71, 73, 74]
    for valor in valores:
        avl_tree.raiz = avl_tree.insertar(avl_tree.raiz, valor)

    tree_visualizer = TreeVisualizer(root, avl_tree)
    entry = tk.Entry(root)
    entry.pack()

    agregar_nodo_button = tk.Button(root, text="Agregar Nodo", command=insertar_nodo)
    agregar_nodo_button.pack()

    eliminar_nodo_button = tk.Button(root, text="Eliminar Nodo", command=eliminar_nodo)
    eliminar_nodo_button.pack()

    root.mainloop()
