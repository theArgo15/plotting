# The purpose of this file is to be able to import these references anywhere in a different file
import pandas as pd

attributeUnits = {"Temp": "($^\circ$C)", "Humidity": "(%)", "Dew Point": "($^\circ$C)"}
LocationDescriptions = pd.read_csv("LocationDescriptions.csv", index_col="Name")
