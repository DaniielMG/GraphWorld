import pandas as pd
from itertools import combinations
import time

def cargar_y_limpiar_datos(file_path):
    """Carga y limpia el CSV filtrando por compras confirmadas."""
    print(f"1. Cargando datos desde {file_path}...")
    cols = ['listid', 'text', 'element_state']
    try:
        df = pd.read_csv(file_path, sep=';', usecols=cols, 
                         dtype={'listid': 'str', 'text': 'str', 'element_state': 'category'})
        
        df_compras = df[df['element_state'] == 'DEL'].copy()
        df_compras.dropna(subset=['text'], inplace=True)
        df_compras['text'] = df_compras['text'].str.lower().str.strip()
        
        listas = df_compras.groupby('listid')['text'].apply(list).reset_index()
        listas = listas[listas['text'].apply(len) >= 2]
        print(f"   -> {len(listas)} listas de compra procesadas.")
        return listas
    except Exception as e:
        print(f"Error al procesar archivo: {e}")
        return None

def generar_co_ocurrencias(listas_df):
    """Genera aristas basadas en co-ocurrencia de productos."""
    print("2. Generando aristas de co-ocurrencia...")
    start_time = time.time()
    
    pares = listas_df['text'].apply(lambda x: [tuple(sorted(p)) for p in combinations(set(x), 2)]).explode()
    
    frecuencia = pares.value_counts().reset_index()
    frecuencia.columns = ['Par', 'Frecuencia']
    
    frecuencia[['item_a', 'item_b']] = pd.DataFrame(frecuencia['Par'].tolist(), index=frecuencia.index)
    
    df_final = frecuencia[['item_a', 'item_b', 'Frecuencia']]
    print(f"   -> {len(df_final)} aristas únicas generadas en {time.time() - start_time:.2f}s.")
    return df_final