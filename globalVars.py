import random

#common vars
colors = {'bg': '#e6ebf5',
          'seacell': '#8ecae9',
          'shipcell': '#928641',
          'hiddencell': '#c0c0c0',
          'button': '#c0c0c0'}

cell_size = 20

turn = True
game = True

#common functions

#get all neighbours of ship with or without corners
def all_ship_neighbours(ship_cells, matrix, skip_corners=False):
    possible_neighbours = []
    for i,j in ship_cells:
        possible_neighbours.extend([(i-1,j), (i+1,j), (i,j-1), (i,j+1)])
        if (not skip_corners):
            possible_neighbours.extend([(i+1,j+1), (i+1,j-1), (i-1,j-1), (i-1,j+1)])
    neighbours = []
    for i,j in possible_neighbours:
        if (i >= 0 and i < len(matrix) and j >= 0 and j < len(matrix)
            and (i,j) not in ship_cells and (i,j) not in neighbours):
            neighbours.append((i, j))
    return neighbours

#check that all neighbours of ship is sea
def check_ship_cells(ship_cells, matrix):
    sea_neighbours = all_ship_neighbours(ship_cells, matrix)
    for i,j in sea_neighbours:
        if (matrix[j][i] != '@'):
            return False
    return True

#check that all neighbours of ship is sea - for column
def check_ship_cells_column(ship_cells, matrix):
    sea_neighbours = all_ship_neighbours(ship_cells, matrix)
    for i,j in sea_neighbours:
        if (matrix[i][j] != '@'):
            return False
    return True

#check rows and columns of matrix for ship - count
def check_line_on_ship(ship_type, ships, line, j, matrix, is_column):
    if (line.count(ship_type) > 0):
        idx_start = 0
        found = line.find(ship_type, idx_start)
        while (found >= 0):
            ship_cells = []
            for i in range(len(ship_type)):
                ship_cells.append((found+i, j))
            if (not is_column and check_ship_cells(ship_cells, matrix)):
                ships[ship_type] += 1
            if (is_column and check_ship_cells_column(ship_cells, matrix)):
                ships[ship_type] += 1
            idx_start = found + 1
            found = line.find(ship_type, idx_start)
    return ships

#check matrix for ships - count
def check_line_on_ships(line, j, matrix, is_column):
    ships = {"#":0, "##":0, "###":0, "####":0}
    for key in ships.keys():
        ships = check_line_on_ship(key, ships, line, j, matrix, is_column)
    return ships

#check matrix for ships - main        
def check_field(matrix):
    ships = {"#":0, "##":0, "###":0, "####":0}
    for i in range(len(matrix)):
        #by row
        line = "".join([matrix[i][j] for j in range(len(matrix))])
        ships_line = check_line_on_ships(line, i, matrix, False)
        for key in ships.keys():
            ships[key] += ships_line[key]
        #by column
        line = "".join([matrix[j][i] for j in range(len(matrix))])
        ships_line = check_line_on_ships(line, i, matrix, True)
        for key in ships.keys():
            if (key != "#"):
                ships[key] += ships_line[key]
    #check counts
    for key in ships.keys():
        if (ships[key] != 5 - len(key)):
            return False
    return True

#fill field with needed ships randomly
def random_ships(battle_size=10):
    ships = ["####", "###", "##", "#"]
    new_matrix = [['@'] * battle_size for i in range(battle_size)]
    for ship in ships:
        for i in range(5-len(ship)):
            while (True):
                x = random.randint(0,10-len(ship))
                y = random.randint(0,10-len(ship))
                d = random.choice([True, False])
                ship_cells = []
                if d:
                    for j in range(len(ship)):
                        ship_cells.append((x+j,y))
                else:
                    for j in range(len(ship)):
                        ship_cells.append((x,y+j))
                if (check_ship_cells(ship_cells, new_matrix)):
                    for x,y in ship_cells:
                        new_matrix[y][x] = '#'
                    break
    return new_matrix

#get all ship in line by type
def get_line_ship(ship_type, ships, line, j, matrix, is_column):
    if (line.count(ship_type) > 0):
        idx_start = 0
        found = line.find(ship_type, idx_start)
        while (found >= 0):
            ship_cells = []
            for i in range(len(ship_type)):
                ship_cells.append((found+i, j))
            if (not is_column and check_ship_cells(ship_cells, matrix)):
                ships[ship_type].append([(j, i) for (i, j) in ship_cells])
            if (is_column and check_ship_cells_column(ship_cells, matrix)):
                ships[ship_type].append(ship_cells)
            idx_start = found + 1
            found = line.find(ship_type, idx_start)
    return ships

#get all ships in line
def get_line_ships(line, j, matrix, is_column):
    ships = {"#":[], "##":[], "###":[], "####":[]}
    for key in ships.keys():
        ships = get_line_ship(key, ships, line, j, matrix, is_column)
    return ships

#get all ships on matrix
def get_all_ships(matrix):
    ships = {"#":[], "##":[], "###":[], "####":[]}
    for i in range(len(matrix)):
        #by row
        line = "".join([matrix[i][j] for j in range(len(matrix))])
        ships_line = get_line_ships(line, i, matrix, False)
        for key in ships.keys():
            ships[key].extend(ships_line[key])
        #by column
        line = "".join([matrix[j][i] for j in range(len(matrix))])
        ships_line = get_line_ships(line, i, matrix, True)
        for key in ships.keys():
            if (key != "#"):
                ships[key].extend(ships_line[key])
    return ships


