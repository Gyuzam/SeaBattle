from tkinter import *
from globalVars import *
from battleField import *
from battleBoard import *
from tkinter import messagebox

class StartBoard(Frame):
    #start board - for player to arrange ships
    def __init__(self, master=None):
        global colors, cell_size
        super().__init__(master)
        self.master = master
        self.field_checked = False
        
        #info frame
        f = Frame(width=26*cell_size, height=2*cell_size, bg=colors['bg'])
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)
        f.grid_propagate(0)
        l = Label(f, text="Arrange your ships", width=24*cell_size, background=colors['bg'], height=2*cell_size, font=("Helvetica", 16))
        f.grid(row=0, column=0, columnspan=2) 
        l.grid(sticky="NWSE")
        
        #rules frame
        rules_frame = Frame(width=12*cell_size, height=12*cell_size, bg=colors['bg'])
        rules_frame.grid(row=1, column=0, sticky="NWSE")
        rules_main_frame = Frame(rules_frame, width=10*cell_size, height=cell_size, bg=colors['bg'])
        rules_main_frame.grid(row=0, column=0, padx=cell_size, pady=cell_size//3)
        rules_main = Label(rules_main_frame, text="You have four types of ships:", anchor="e", background=colors['bg'], font=("Helvetica", 10))
        rules_main.grid(sticky="NWSE")
        for i in range(4):
            rules_frame_ship = Frame(rules_frame, width=10*cell_size, height=cell_size, bg=colors['bg'])
            rules_frame_ship.grid(row=i+1, column=0, padx=cell_size, pady=cell_size//3, sticky="NWSE")
            for j in range(4-i):
                f = Frame(rules_frame_ship, width=cell_size, height=cell_size)
                b = Button(f, background=colors['shipcell'])
                f.rowconfigure(0, weight=1)
                f.columnconfigure(0, weight=1)
                f.grid_propagate(0)
                f.grid(row=0, column=j)
                b.grid(sticky="NWSE")
            f = Frame(rules_frame_ship, width=3*cell_size, height=cell_size)
            ship_label = Label(f, text=" x "+str(i+1), background=colors['bg'], font=("Helvetica", 10))
            f.rowconfigure(0, weight=1)
            f.columnconfigure(0, weight=1)
            f.grid_propagate(0)
            f.grid(row=0, column=4-i)
            ship_label.grid(sticky = "NWSE")
        rules_end_frame = Frame(rules_frame, width=10*cell_size, height=3*cell_size, bg=colors['bg'])
        rules_end_frame.grid(row=6, column=0, padx=cell_size, pady=cell_size//3)
        rules_main = Label(rules_end_frame, anchor="e", background=colors['bg'], font=("Helvetica", 10),
                           text="They must all be placed on field\nand must not be near each other.")
        rules_main.grid(row=0, sticky="NWSE")

        #battle field frame
        battle_frame = Frame(width=12*cell_size, height=12*cell_size, bg=colors['bg'])
        battle_frame.grid(row=1, column=1, sticky="NWSE")
        battle_frame_board = Frame(battle_frame, width=10*cell_size, height=10*cell_size, bg=colors['bg'])
        battle_frame_board.grid(row=0, column=0, padx=cell_size, pady=cell_size)
        self.battle_frame_board = battle_frame_board
        self.battle_board = BattleField(battle_frame_board, visibility=True, modify_enabled=True)
        button_frame = Frame(width=24*cell_size, height=cell_size, bg=colors['bg'])
        button_frame.grid(row=2, column=0, columnspan=2)

        #buttons on bottom
        f = Frame(button_frame, width=24*cell_size, height=2*cell_size, bg=colors['bg'])
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)
        f.columnconfigure(1, weight=1)
        f.grid_propagate(0)
        
        #start game button 
        b_start = Button(f, text="Start game!", width=10*cell_size, height=cell_size, background=colors['button'], font=("Helvetica", 10))
        b_start.config(command=lambda:self.check_field())
        
        #generate random field button
        b_random = Button(f, text="Arrange randomly", width=10*cell_size, height=cell_size, background=colors['button'], font=("Helvetica", 10))
        b_random.config(command=lambda:self.gen_random_field())
        
        f.grid(row=0, column=0, padx=cell_size, pady=cell_size//3)
        b_start.grid(row=0, column=0, sticky="NWSE")
        b_random.grid(row=0, column=1, sticky="NWSE")

    #check on player's arrangement of ships
    def check_field(self):
        if self.field_checked or gv.check_field(self.battle_board.battle_matrix):
            self.start_battle()
        else:
            messagebox.showerror("Error!", "Not all ships arranged or they arranged incorrectly!")
    
    #generate random field
    def gen_random_field(self):
        new_matrix = gv.random_ships()
        self.field_checked = True
        self.battle_board = BattleField(self.battle_frame_board, visibility=True, modify_enabled=True, matrix=new_matrix)

    #create battle board
    def start_battle(self):
        field = self.battle_board.battle_matrix
        app2 = BattleBoard(master=self.master, gamer_matrix=field)
        app2.mainloop()
