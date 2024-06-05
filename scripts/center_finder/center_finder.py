# file intended to output the center x-, y-, and z- coordinates of a ligand.

import sys

file_path = sys.argv[1]

# variable setup
x_data = []
x_index = 5

y_data = []
y_index = 6

z_data = []
z_index = 7

# extracts x-, y-, and z- data from table and adds to respective lists
with open(file_path, 'r') as file:
    for line in file:
        columns = line.strip().split()
        x_data.append(float(columns[x_index]))
        y_data.append(float(columns[y_index]))
        z_data.append(float(columns[z_index]))

# calculates x-, y-, and z- center coordinates
x_center = min(x_data) + (max(x_data)-min(x_data))*0.5
y_center = min(y_data) + (max(y_data)-min(y_data))*0.5
z_center = min(z_data) + (max(z_data)-min(z_data))*0.5


print(x_center)
print(y_center)
print(z_center)
