import os

with open('files_list.txt', 'w') as f:
    for file in os.listdir('.'):
        f.write(file + '
')