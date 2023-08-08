import pandas as pd

table = pd.read_csv('./food/dish.csv', delimiter=',')
del table['isPiece']
table.to_csv("./food/dish.csv", sep=",")
print(table)