from tkinter import *
import globalVars as gv

class BattleField(Frame):
    #init battle field
    def __init__(self, master=None, visibility=False, modify_enabled=False, matrix=None, cells=10):

        self.battle_size = cells
        self.cells_visibility = visibility
        self.battle_modify = modify_enabled
        #if matrix was empty
        if not matrix:
            matrix = [['@']*self.battle_size for i in range(self.battle_size)]

        self.battle_matrix = matrix

        #set visibility for buttons for game
        self.battle_cells_visible = [[self.cells_visibility]*self.battle_size for i in range(self.battle_size)]
        
        super().__init__(master)
        self.master = master
        
        #for game
        self.cells_click = []
        self.visited = []
        self.last_move = ""

        #create buttons in frames - to make them squared
        for i in range(self.battle_size):
            cells_row = []
            for j in range(self.battle_size):
                f = Frame(master, width=gv.cell_size, height=gv.cell_size)
                color = gv.colors['seacell']
                if (self.battle_matrix[i][j] != '@'):
                    color = gv.colors['shipcell']
                if (not self.cells_visibility):
                    color = gv.colors['hiddencell']
                b = Button(f, background = color)
                b.config(command=lambda f=[b, i, j]:self.pressed(f))
                f.rowconfigure(0, weight=1)
                f.columnconfigure(0, weight=1)
                f.grid_propagate(0)
                f.grid(row=i, column=j)
                b.grid(sticky="NWSE")
                cells_row.append(b)
            self.cells_click.append(cells_row)
        self.all_ships = gv.get_all_ships(self.battle_matrix)
                
    #cells on click reaction
    def pressed(self, args, killed=False):
        button, i, j = args[0], args[1], args[2]
        if ((i, j) in self.visited):
            return
        self.visited.append((i, j))
        #on creation stage - change type of cell
        if (self.battle_modify):
            if (self.battle_matrix[i][j] == '@'):
                self.battle_matrix[i][j] = '#'
                color = gv.colors['shipcell']
            else:
                self.battle_matrix[i][j] = '@'
                color = gv.colors['seacell']
            button.configure(bg = color)
        #on game stage - make visible
        #gamer turn
        elif (not self.battle_modify and not self.battle_cells_visible[i][j] and gv.turn):
            self.battle_cells_visible[i][j] = True
            if self.battle_matrix[i][j] == '#':
                button.configure(bg = gv.colors['shipcell'])
                button.configure(text = 'X')
                self.check_killed_ships()
                self.last_move = "".join((str(i), " x ", str(j)))
            else:
                button.configure(bg = gv.colors['seacell'])
                button.configure(text = '*')
                #do not change turn if there are cells nearby killed ship
                if (not killed):
                    gv.turn = False
                    self.last_move = "".join((str(i), " x ", str(j)))
        #computer turn - no need to change visibility
        elif (not self.battle_modify and self.battle_cells_visible[i][j] and not gv.turn):
            if self.battle_matrix[i][j] == '#':
                button.configure(text = 'X')
                self.check_killed_ships()
            else:
                button.configure(text = '*')
            self.last_move = "".join((str(i), " x ", str(j)))

    #after every hit - check if ship is killed
    def check_killed_ships(self):
        for ship_type in self.all_ships.keys():
            for ship in self.all_ships[ship_type]:
                killed = True
                for (i, j) in ship:
                    if (i, j) not in self.visited:
                        killed = False
                if killed:
                    nb = gv.all_ship_neighbours(ship, self.battle_matrix)
                    for i, j in nb:
                        self.pressed([self.cells_click[i][j], i, j], killed=True)
        if gv.turn:
            gv.turn = False

    #check if game over
    def check_all_killed(self):
        for ship_type in self.all_ships.keys():
            for ship in self.all_ships[ship_type]:
                for (i, j) in ship:
                    if (i, j) not in self.visited:
                        return False
        return True
