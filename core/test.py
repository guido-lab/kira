import os
import pandas as pd
files = []
for file in os.listdir('media/'):
    if file.endswith(".xlsx"):
        files.append(file)
print(files)