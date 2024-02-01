# converts the .txt tables to a .csv table that can be used for evaluation
import pandas as pd
from pathlib import Path

def createTable(pieceName):
    tableFile = open("tables/" + pieceName + "Table.txt", 'r')
    table = tableFile.readlines()
    for index, row in enumerate(table):
        table[index] = row.strip(" \n,")
    table.reverse()
    finalTable = []
    for row in table:
        for val in row.split(","):
            finalTable.append(int(val))
    return finalTable

dict = {}
pieces = ["pawn", "knight", "bishop", "rook", "queen", "king1", "king2"]
for piece in pieces:
    table = createTable(piece)
    dict[piece] = table

table = pd.DataFrame(data = dict)
filepath = Path('tables/table.csv')  
table.to_csv(filepath)