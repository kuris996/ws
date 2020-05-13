import pandas as pd
import numpy as np

class Chart:
    def read(self, file_name, sheet):
        xl = pd.ExcelFile(file_name)
        print(xl.sheet_names)
        df1 = xl.parse('region_premia')
        for row in df1.iterrows():
            print(row)