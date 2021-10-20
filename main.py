from tkinter import Label, Tk, Button, Toplevel
from PIL import ImageTk, Image
import os

root = Tk()
root.title("Chess")
noConvertImageList = os.listdir('Image')
noConvertImageList.sort()
imageList = []
for k in noConvertImageList:
    imageList.append(ImageTk.PhotoImage(Image.open('Image\\' + k).resize((100, 100), Image.ANTIALIAS)))
noConvertImageList2 = os.listdir('Chosen')
noConvertImageList2.sort()
imageList2 = []
for k in noConvertImageList2:
    imageList2.append(ImageTk.PhotoImage(Image.open('Chosen\\' + k).resize((100, 300), Image.ANTIALIAS)))

powList = [[-4, -2, -3, -5, -6, -3, -2, -4],
           [-1, -1, -1, -1, -1, -1, -1, -1],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [1, 1, 1, 1, 1, 1, 1, 1],
           [4, 2, 3, 5, 6, 3, 2, 4]]

BoardList = []

for rows in range(8):
    tempList = []
    for columns in range(8):
        squaresButton = (Button(command=lambda row=rows, column=columns: move(row, column)))
        tempList.append(squaresButton)
        squaresButton.grid(row=rows, column=columns)
    BoardList.append(tempList)


def print_board():

    switch_case_figure = {
        6: 25,
        5: 23,
        4: 21,
        3: 19,
        2: 17,
        1: 15,
        0: 13,
        -6: 11,
        -5: 9,
        -4: 7,
        -3: 5,
        -2: 3,
        -1: 1
    }

    for row in range(8):
        for column in range(8):
            fast_switch = switch_case_figure[powList[row][column]]
            BoardList[row][column].config(image=imageList[fast_switch-((row+column) % 2)])


faze = 1
TouchFigure = None
possibilityMoveList = []
oldCoordinate = []
enPassant = []


def refresh():
    global faze
    global TouchFigure
    global possibilityMoveList
    global oldCoordinate
    faze = 1
    TouchFigure = None
    possibilityMoveList = []
    oldCoordinate = []
    for ro in range(8):
        for co in range(8):
            BoardList[ro][co].config(bg='white')


def prepare_to_move(row, column):
    global possibilityMoveList
    global oldCoordinate
    for roco in possibilityMoveList:
        BoardList[roco[0]][roco[1]].config(bg='black')
        BoardList[row][column].config(bg='red')
    oldCoordinate = [row, column]


def check_pawns_end():
    global powList

    def ask_window(co, color):
        global powList
        new_window = Toplevel(root)
        image_help = 0
        if color == 1: image_help = 4

        def pawn_rebirth(col, colors, figure):
            global powList
            if colors == 1:
                powList[0][col] = figure
            elif colors == -1:
                powList[7][col] = -1 * figure
            return new_window.destroy()

        Label(new_window, text="Choose your figure").grid(row=0, column=0, columnspan=4)
        Button(new_window, image=imageList2[0 + image_help],
               command=lambda: pawn_rebirth(co, color, 2)).grid(row=1, column=0)
        Button(new_window, image=imageList2[1 + image_help],
               command=lambda: pawn_rebirth(co, color, 3)).grid(row=1, column=1)
        Button(new_window, image=imageList2[2 + image_help],
               command=lambda: pawn_rebirth(co, color, 4)).grid(row=1, column=2)
        Button(new_window, image=imageList2[3 + image_help],
               command=lambda: pawn_rebirth(co, color, 5)).grid(row=1, column=3)

    for fig in (powList[0]):
        if fig == 1:
            ask_window(co=powList[0].index(1), color=1)
    for fig in powList[7]:
        if fig == -1:
            ask_window(co=powList[7].index(-1), color=-1)


def move(row, column):
    global faze
    global TouchFigure
    global possibilityMoveList
    global oldCoordinate
    global powList
    if faze == 1:
        refresh()
        print_board()
        if powList[row][column] > 0:
            colour = 1
        elif powList[row][column] < 0:
            colour = -1
        else:
            return refresh()
        if abs(powList[row][column]) == 6:
            king_move(colour, row, column)
        if abs(powList[row][column]) == 5:
            queen_move(colour, row, column)
        if abs(powList[row][column]) == 4:
            rook_move(colour, row, column)
        if abs(powList[row][column]) == 3:
            bishop_move(colour, row, column)
        if abs(powList[row][column]) == 2:
            knight_move(colour, row, column)
        if abs(powList[row][column]) == 1:
            paws_move(colour, row, column)
    elif faze == 2:
        if [row, column] in possibilityMoveList:
            powList[row][column] = TouchFigure
            powList[oldCoordinate[0]][oldCoordinate[1]] = 0
        check_pawns_end()
        refresh()
        print_board()


def paws_move(colour, row, column):
    global faze
    global possibilityMoveList
    global oldCoordinate
    global TouchFigure

    TouchFigure = colour
    faze = 2
    if powList[row - colour][column] == 0:
        possibilityMoveList.append([row - colour, column])
        if powList[row - 2 * colour][column] == 0 and ((row == 6 and colour == 1) or (row == 1 and colour == -1)):
            possibilityMoveList.append([row - 2 * colour, column])
    try:
        if colour * powList[row - colour][column + 1] < 0:
            possibilityMoveList.append([row - colour, column + 1])
    except Exception:
        pass
    try:
        if colour * powList[row - colour][column - 1] < 0:
            possibilityMoveList.append([row - colour, column - 1])
    except Exception:
        pass
    prepare_to_move(row, column)


def knight_move(colour, row, column):
    global faze
    global possibilityMoveList
    global oldCoordinate
    global TouchFigure
    TouchFigure = colour * 2
    faze = 2
    try:
        if colour * powList[row + 2][column - 1] <= 0:          possibilityMoveList.append([row + 2, column - 1])
    except Exception:
        pass
    try:
        if colour * powList[row + 2][column + 1] <= 0:          possibilityMoveList.append([row + 2, column + 1])
    except Exception:
        pass
    try:
        if colour * powList[row - 2][column - 1] <= 0:          possibilityMoveList.append([row - 2, column - 1])
    except Exception:
        pass
    try:
        if colour * powList[row - 2][column + 1] <= 0:          possibilityMoveList.append([row - 2, column + 1])
    except Exception:
        pass
    try:
        if colour * powList[row + 1][column - 2] <= 0:          possibilityMoveList.append([row + 1, column - 2])
    except Exception:
        pass
    try:
        if colour * powList[row + 1][column + 2] <= 0:          possibilityMoveList.append([row + 1, column + 2])
    except Exception:
        pass
    try:
        if colour * powList[row - 1][column - 2] <= 0:          possibilityMoveList.append([row - 1, column - 2])
    except Exception:
        pass
    try:
        if colour * powList[row - 1][column + 2] <= 0:          possibilityMoveList.append([row - 1, column + 2])
    except Exception:
        pass
    prepare_to_move(row, column)


def bishop_move(colour, row, column):
    global faze
    global possibilityMoveList
    global oldCoordinate
    global TouchFigure
    TouchFigure = colour * 3
    faze = 2
    for m in range(1, min(column, row) + 1):
        if colour * powList[row - m][column - m] == 0:
            possibilityMoveList.append([row - m, column - m])
        elif colour * powList[row - m][column - m] < 0:
            possibilityMoveList.append([row - m, column - m])
            break
        else:
            break
    for n in range(1, min(8 - column, 8 - row)):
        if colour * powList[row + n][column + n] == 0:
            possibilityMoveList.append([row + n, column + n])
        elif colour * powList[row + n][column + n] < 0:
            possibilityMoveList.append([row + n, column + n])
            break
        else:
            break
    for s in range(1, min(column + 1, 8 - row)):
        if colour * powList[row + s][column - s] == 0:
            possibilityMoveList.append([row + s, column - s])
        elif colour * powList[row + s][column - s] < 0:
            possibilityMoveList.append([row + s, column - s])
            break
        else:
            break
    for k in range(1, min(8 - column, row + 1)):
        if colour * powList[row - k][column + k] == 0:
            possibilityMoveList.append([row - k, column + k])
        elif colour * powList[row - k][column + k] < 0:
            possibilityMoveList.append([row - k, column + k])
            break
        else:
            break

    prepare_to_move(row, column)


def rook_move(colour, row, column):
    global faze
    global possibilityMoveList
    global oldCoordinate
    global TouchFigure
    TouchFigure = colour * 4
    faze = 2

    for n in range(1, row + 1):
        if colour * powList[row - n][column] == 0:
            possibilityMoveList.append([row - n, column])
        elif colour * powList[row - n][column] < 0:
            possibilityMoveList.append([row - n, column])
            break
        else:
            break
    for s in range(1, 8 - row):
        if colour * powList[row + s][column] == 0:
            possibilityMoveList.append([row + s, column])
        elif colour * powList[row + s][column] < 0:
            possibilityMoveList.append([row + s, column])
            break
        else:
            break
    for e in range(1, 8 - column):
        if colour * powList[row][column + e] == 0:
            possibilityMoveList.append([row, column + e])
        elif colour * powList[row][column + e] < 0:
            possibilityMoveList.append([row, column + e])
            break
        else:
            break
    for w in range(1, column + 1):
        if colour * powList[row][column - w] == 0:
            possibilityMoveList.append([row, column - w])
        elif colour * powList[row][column - w] < 0:
            possibilityMoveList.append([row, column - w])
            break
        else:
            break

    prepare_to_move(row, column)


def queen_move(colour, row, column):
    global faze
    global possibilityMoveList
    global oldCoordinate
    global TouchFigure
    rook_move(colour, row, column)
    bishop_move(colour, row, column)
    TouchFigure = colour * 5
    faze = 2


def king_move(colour, row, column):
    global faze
    global possibilityMoveList
    global oldCoordinate
    global TouchFigure
    TouchFigure = colour * 6
    faze = 2

    for east_west in range(-1, 2):
        for north_south in range(-1, 2):
            try:
                if east_west == 0 and north_south == 0:
                    continue
                elif colour * powList[row + east_west][column + north_south] <= 0:
                    possibilityMoveList.append([row + east_west, column + north_south])
            except:
                pass

    prepare_to_move(row, column)


print_board()
root.mainloop()


