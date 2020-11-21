import random
from tkinter import *
import tkinter.font

import logic
import constants as c
import sound as s

### 메인 class ###

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        # self.gamelogic = gamelogic
        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left, c.KEY_RIGHT_ALT: logic.right,
                         c.KEY_H: logic.left, c.KEY_L: logic.right,
                         c.KEY_K: logic.up, c.KEY_J: logic.down}
        
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = list()
        self.matrix = logic.add_two(self.matrix)
        self.matrix = logic.add_two(self.matrix)
        self.history_matrixs.append(self.matrix)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key == c.KEY_BACK and len(self.history_matrixs) >= 1:
            if c.COUNT == 0:
                self.history_matrixs.pop()
                c.COUNT = 1
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
            if len(self.history_matrixs)==0:
                print('No more turning back!')
                self.history_matrixs.append(self.matrix)
        elif key in self.commands:
            self.matrix, done = self.commands[repr(event.char)](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                c.COUNT = 0
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                done = False
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    s.endsound()
                    self.game_end()
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    s.endsound()
                    self.game_end()

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

    def game_end(self):
        label = Label(self, text="\n게임이 종료되었습니다.\n\n최종 점수 : " + str(logic.score) + "점" + "\n다시 하시겠습니까?", font=('Helvetica', 12, "bold"))
        label.grid(row=1)
        button = Button(self, text="Restart", command=self.regame, font=('Helvetica', 12, "bold"), background = "#eee4da")
        button.grid(row=2)

    def regame(self):
        self.destroy()
        self.__init__()

### 메인 함수 ####

# 선택된 게임의 크기에 따라 text 출력
def set_grid_len4():
    c.GRID_LEN = 4
    label = Label(root, text="4x4가 선택되었습니다.", font=('Helvetica', 12, "bold"), background = "#eee4da")
    label.place(x=210, y=180)

def set_grid_len5():
    c.GRID_LEN = 5
    label = Label(root, text="5x5가 선택되었습니다.", font=('Helvetica', 12, "bold"), background = "#eee4da")
    label.place(x=210, y=180)

def set_grid_len6():
    c.GRID_LEN = 6
    label = Label(root, text="6x6이 선택되었습니다.", font=('Helvetica', 12, "bold"), background = "#eee4da")
    label.place(x=210, y=180)

# 게임 실행
def start():
    root.destroy()
    gamegrid=GameGrid()

# 게임 종료
def close():
    root.quit()

#도움말 기능
def help():
    ad = Tk()
    ad.title("2048 help")
    ad.geometry("480x260")
    ad.configure(background = "#eee4da")
    label = Label(ad, text="\n◆조작방법◆\nW, A, S, D 를 눌러 상, 하, 좌, 우를 입력하며,\nB를 눌러 되돌리기 기능을 이용할 수 있습니다.\n\n ◆게임규칙◆\n같은 숫자의 타일이 만나게 되면 숫자가 2배로 커지게 되고,\n타일을 이동할 때 마다 새로운 타일이 생성됩니다.\n 최종적으로 2048의 숫자를 만드는 것이 목표입니다.\n\n◆패배조건◆\n타일이 움직일 수 없게 되면 패배합니다.", font=('Helvetica', 13, "bold"), background = "#eee4da")
    label.pack(side="top")

# tk 객체 생성 및 frame 설정
root = Tk()
root.title("2048 Setting")
root.geometry("560x400")
root.configure(background = "#eee4da")
root.resizable(False, False)


# 레이블&버튼 생성
label = Label(root, text="공개SW 프로젝트 9조", font=('Helvetica', 8, "bold"), background = "#eee4da")
label.place(x=0, y=380)
label = Label(root, text="\n게임 2048의 설정을 진행합니다." + "\n게임의 크기를 고른 후, 게임을 실행하세요.", font=('Helvetica', 18, "bold"), background = "#eee4da")
label.pack(side="top")
button1 = Button(root,text="4x4", font=('Helvetica', 18, "bold"), overrelief="solid", command=set_grid_len4, background = "#eee4da")
button1.place(x=180, y=100)
button2 = Button(root,text="5x5", font=('Helvetica', 18, "bold"), overrelief="solid", command=set_grid_len5, background = "#eee4da")
button2.place(x=260, y=100)
button3 = Button(root, text="6x6", font=('Helvetica', 18, "bold"), overrelief="solid", command=set_grid_len6, background = "#eee4da")
button3.place(x=340, y=100)
button4 = Button(root,text="게임 실행", font=('Helvetica', 18, "bold"), overrelief="solid", command=start, background = "#eee4da")
button4.place(x=230, y=220)
button5 = Button(root,text="도움말", font=('Helvetica', 18, "bold"), overrelief="solid", command=help, background = "#eee4da")
button5.place(x=245, y=280)
button6 = Button(root,text="종료", font=('Helvetica', 18, "bold"), overrelief="solid", command=close, background = "#eee4da")
button6.place(x=255, y=340)

#배경 사운드 재생
s.firstsound()

# 메인 화면 표시
root.mainloop()
