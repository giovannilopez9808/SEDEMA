#                           Fecha de creación
#                           08 abril 2020
#                               Creador
#                     Giovanni Gamaliel LÃopez Padilla
from TES_algortihm import *
# <------Valores para interactuar------->
inputs = {
    "hour initial": 8,
    "hour final": 18,
    "hour limit": 21,
    "Dosis Pso": [10000, 15000, 20000, 30000],
    "MED": [200, 250, 300, 450, 600, 1000],
    "Cloud factor": [1, 0.9, 0.6],
    "Filenames": ["Pso1", "Pso1_5", "Pso2", "Pso3"],
    "Phototype names": ["I", "II", "III", "IV", "V", "VI"],
    "TES names": ["dosis", "Max"],
    "Data folders": ["2016", "2017-2018"],
    "Data results": "Data/",
}
TES = TES(inputs["hour initial"],
          inputs["hour final"],
          inputs["hour limit"],
          inputs["Dosis Pso"],
          inputs["MED"],
          inputs["Cloud factor"],
          inputs["Filenames"],
          inputs["Phototype names"],
          inputs["TES names"],
          inputs["Data folders"]
          )
TES.calc_TES()
TES.write_results(inputs["Data results"])
