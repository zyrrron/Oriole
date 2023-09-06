import csv
import matplotlib.pyplot as plt
import numpy as np

x, y = [], []

# Opening the CSV file in read mode
with open('../results/bionetwork/chris_group/chris_new_requirement/plot_data.csv', 'r') as file:

    # Creating a CSV reader object
    reader = csv.DictReader(file)

    # Looping through each row in the CSV file
    for row in reader:
        column_headers = list(reader.fieldnames)

        # Removing the row header
        column_headers.remove('gates\edges')
        countstart = 1
        int_y = []
        flag = True

        # Converting each element in the row to an integer
        for column in column_headers:
            if row[column] == 'inf':
                if flag:
                    countstart += 1
                else:
                    break
            else:
                int_y.append(int(row[column]))
                flag = False

        x.append(range(countstart, countstart+len(int_y)))
        y.append(int_y)
        # Printing the integer row
        print(int_y)

plt.figure(1)
plt.figure(figsize=(10,10))
plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)
# Plotting the graph: color means gate number, x means max cell-cell edge
n = 10
colors = plt.cm.Set1(np.linspace(0, 1, n))
row_names = [8, 12, 16, 20, 40]
for i in range(len(y)):
    plt.plot(x[i], y[i], color=colors[i], label=f'{row_names[i]} gates')


# Adding labels to the graph
plt.rc('legend', fontsize=20)
plt.xlabel('Max # of channels', fontsize=40)
plt.ylabel('# of cells', fontsize=40)
plt.title('channels <-> cells', fontsize=40)

# Adding a legend
plt.legend()
plt.savefig('../results/bionetwork/chris_group/chris_new_requirement/channels-cells.png')

plt.show()