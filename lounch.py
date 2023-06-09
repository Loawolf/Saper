from tkinter import *
import main

root = Tk()
root.title('Сапер')


def info():
    inf = Toplevel()
    inf.title('Подсказка')

    Label(inf, text='Как правильно играть в игру Сапер?').pack()
    Label(inf, text='Целью игры является открытие всех ячеек, не содержащих мины. Игрок открывает ячейки, стараясь не открыть ячейку с миной.\nЕсли игрок открывает ячейку с миной, он проигрывает. Мины расставляются после первого хода, поэтому в новых версиях проиграть на первом же ходу невозможно.').pack()

    Label(inf, text='Как играть в сапера и что означают цифры?').pack()
    Label(inf, text='Количество не найденных мин отображено в нижнем левом углу. Чтобы начать игру, нужно щелкнуть в произвольном месте на поле.\nГлавная задача здесь - не нарваться сразу на мину. После щелчка откроется некоторый участок поля, на котором появятся цифры.\nВсе эти цифры служат для облегчения поиска установленной мины.').pack()


Label(text='Реализация игры сапер, для игры выберите сложность: ').pack()
Button(text='Легкий', command=lambda: main.game("легкий")).pack()
Button(text='Средний', command=lambda: main.game("средний")).pack()
Button(text='Сложный', command=lambda: main.game("сложный")).pack()
Button(text='Я не умею играть', command=info).pack()
root.mainloop()
