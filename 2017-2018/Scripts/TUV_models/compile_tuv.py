import os
name = "tuv_DRDM.out"
files = {
    "tuv": "tuv_DM.f",
    "savout": "savout.f",
    "setaer": "setaer.f",
    "functs": "functs.f",
    "grids": "grids.f",
    "la_srb": "la_srb.f",
    "newlst": "newlst.f",
    "numer": "numer.f",
    "odo3": "odo3.f",
    "odrl": "odrl.f",
    "orbit": "orbit.f",
    "qys": "qys.f",
    "rdetfl": "rdetfl.f",
    "rdinp": "rdinp.f",
    "rdxs": "rdxs.f",
    "rtrans": "rtrans.f",
    "rxn": "rxn.f",
    "setalb": "setalb.f",
    "setcld": "setcld.f",
    "setno2": "setno2.f",
    "seto2": "seto2.f",
    "setsnw": "setsnw.f",
    "setso2": "setso2.f",
    "sphers": "sphers.f",
    "swbiol": "swbiol.f",
    "swchem": "swchem.f",
    "swdom": "swdom.f",
    "swphys": "swphys.f",
    "terint": "terint.f",
    "vpair": "vpair.f",
    "vpo3": "vpo3.f",
    "vptmp": "vptmp.f",
    "waters": "waters.f",
    "wrflut": "wrflut.f",
    "wshift": "wshift.f"
}
comand = "gfortran "
for key in files:
    comand += files[key]+" "
comand += "-o "+name
os.system(comand)
