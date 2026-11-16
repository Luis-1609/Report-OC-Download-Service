import pandas as pd

def procesarReporte(ruta,categorias,compradores):
    #con header=1 ignora la primera fial (fila=0) y establece a la fila 1 como encabezados
    df = pd.read_excel(ruta,header=1)
    #Filtro y me quedo solo con las filas que correspondan a categorias dti y a compradores asociados a dti
    df = df.loc[ 
        df["Descripción Categoría"].isin(categorias) | 
        df["Comprador"].isin(compradores) 
    ]

    return df