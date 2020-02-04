from tkinter import *
from tkinter import messagebox
import globalVars as gv 
from battleField import *
from startBoard import *
import random

class BattleBoard(Frame):
    #create battle board with gamer and rival boards
    def __init__(self, master=None, gamer_matrix=None, rival_matrix=None):
        super().__init__(master)
        self.master = master
        #turn info
        f = Frame(width=26*gv.cell_size, height=2*gv.cell_size, bg=gv.colors['bg'])
        f.rowconfigure(0, weight=1)
        f.rowconfigure(1, weight=1)
        f.columnconfigure(0, weight=1)
        f.columnconfigure(1, weight=1)
        f.grid_propagate(0)
        self.sv = StringVar()
        l = Label(f, textvariable=self.sv, width=24*gv.cell_size, background=gv.colors['bg'], height=gv.cell_size, font=("Helvetica", 16))
        #fields info
        l1 = Label(f, text="Rival field:", width=12*gv.cell_size, background=gv.colors['bg'], height=gv.cell_size, font=("Helvetica", 16))
        l2 = Label(f, text="Your field:", width=12*gv.cell_size, background=gv.colors['bg'], height=gv.cell_size, font=("Helvetica", 16))
        l.grid(row=0, column=0, columnspan=2, sticky="NWSE")
        l1.grid(row=1, column=0, sticky="NWSE")
        l2.grid(row=1, column=1, sticky="NWSE")
        f.grid(row=0, column=0, columnspan=2)

        #battle fiels
        if not rival_matrix:
            rival_matrix=gv.random_ships()

        #rival
        rival_frame = Frame(width=12*gv.cell_size, height=12*gv.cell_size, bg=gv.colors['bg'])
        rival_frame.grid(row = 1, column = 0, sticky = "NWSE")
        rival_frame_board = Frame(rival_frame, width=10*gv.cell_size, height=10*gv.cell_size, bg=gv.colors['bg'])
        rival_frame_board.grid(row=0, column=0, padx=gv.cell_size, pady=gv.cell_size)
        self.rival_board = BattleField(rival_frame_board, matrix=rival_matrix)

        #gamer
        gamer_frame = Frame(width=12*gv.cell_size, height=12*gv.cell_size, bg=gv.colors['bg'])
        gamer_frame.grid(row = 1, column = 1, sticky = "NWSE")
        gamer_frame_board = Frame(gamer_frame, width=10*gv.cell_size, height=10*gv.cell_size, bg=gv.colors['bg'])
        gamer_frame_board.grid(row=0, column=0, padx=gv.cell_size, pady=gv.cell_size)
        self.gamer_board = BattleField(gamer_frame_board, visibility=True, matrix=gamer_matrix)

        #last move info
        f = Frame(width=24*gv.cell_size, height=2*gv.cell_size, bg=gv.colors['bg'])
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)
        f.grid_propagate(0)
        self.tv = StringVar()
        l = Label(f, textvariable=self.tv, width=24*gv.cell_size, background=gv.colors['bg'], height=gv.cell_size, font=("Helvetica", 16))
        l.grid(sticky="NWSE")
        f.grid(row=2, column=0, columnspan=2) 

        #to store hits on ships for computer
        self.gamer_ships = []

        #cycled loop
        self.onTimer()

    def onTimer(self):
        
        #all killed on gamer board
        if (self.gamer_board.check_all_killed()):
            messagebox.showinfo("Game over", "You lost!")
            return
        
        #all killed on rival board
        if (self.rival_board.check_all_killed()):
            messagebox.showinfo("Game over", "Congratulations! You won!")
            return

        #game continues
        if gv.turn:
            #gamer turn
            self.sv.set("Your turn!")
            self.tv.set("Last rival move: " + self.gamer_board.last_move)
        else:
            #computer turn
            self.sv.set("Wait for rival move")
            self.tv.set("Your last move: " + self.rival_board.last_move)
            self.rival_move()
            gv.turn = True
        
        self.after(120, self.onTimer)

    #computer strategy
    def rival_move(self):
        #if no hits yet - random in unvisited
        if (not self.gamer_ships):
            i = random.randint(0,9)
            j = random.randint(0,9)
            while ((i, j) in self.gamer_board.visited):
                i = random.randint(0,9)
                j = random.randint(0,9)
            self.gamer_board.pressed([self.gamer_board.cells_click[i][j], i, j])

            #if hit - add to hits to kill ship
            if (self.gamer_board.battle_matrix[i][j] == "#"):
                self.gamer_ships.append((i,j))
        #if there are hits - try to kill it
        else:
            nb = gv.all_ship_neighbours(self.gamer_ships, self.gamer_board.battle_matrix, skip_corners=True)
            #if 2 or more cells hitted - direction known, remove extra neighbours
            if (len(self.gamer_ships) > 1):
                to_del = []
                if self.gamer_ships[0][0] == self.gamer_ships[1][0]:
                    for n in nb:
                        if n[0] != self.gamer_ships[0][0]:
                            to_del.append(n)
                else:
                    for n in nb:
                        if n[1] != self.gamer_ships[0][1]:
                            to_del.append(n)
                for n in to_del:
                    nb.remove(n)
            #random from neighbours withount corners
            i, j = random.choice(nb)
            while ((i, j) in self.gamer_board.visited):
                nb.remove((i, j))
                if (not nb):
                    #if all neighbours visited - random (maybe impossible situation)
                    self.gamer_ships = []
                    i = random.randint(0, 9)
                    j = random.randint(0, 9)
                    break
                i, j = random.choice(nb)
            
            self.gamer_board.pressed([self.gamer_board.cells_click[i][j], i, j])
            #if hit - add to hits to kill ship
            if (self.gamer_board.battle_matrix[i][j] == "#"):
                self.gamer_ships.append((i,j))
        


