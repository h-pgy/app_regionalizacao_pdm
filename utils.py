import pandas as pd
import geopandas as gpd

def metas_por_secretaria(df, secretaria):

    df = df.copy()

    mask = df['secretaria']==secretaria

    return df[mask]['numero_meta'].unique()

def filtrar_por_meta(df, meta_num):

    df = df.copy()

    mask = df['numero_meta']==meta_num
    
    return df[mask]

def merge_subs(df, subs):

    merged = pd.merge(subs, df, left_on='sp_codigo', right_on='codigo_subs', how='left')
    merged['valor'].fillna(0, inplace=True)

    return merged

def merge_zonas(df, zonas):

    merged = pd.merge(zonas, df, left_on='COD_REG_5', right_on='codigo_zonas', how='left')

    merged['valor'].fillna(0, inplace=True)

    return merged

def decidir_plot(df, subs, zonas):

    if df['codigo_subs'].isnull().all():

        return merge_zonas(df, zonas)
    
    return merge_subs(df, subs)

def prep_shapefiles():

    subs = gpd.read_file('mapas/subs/SIRGAS_SHP_subprefeitura_polygon.shp')
    subs.set_crs(epsg='31983', inplace=True)
    subs.to_crs(epsg=4326,inplace=True)
    zonas = gpd.read_file('mapas/regioes/SIRGAS_REGIAO5.shp')
    zonas.set_crs(epsg='31983', inplace=True)
    zonas.to_crs(epsg=4326, inplace=True)

    return subs, zonas

def prep_data():

    #abre dados
    df = pd.read_csv('dados_regionalizacao_pdm.csv', sep = ';')
    #precisa arrumar a coluna para dar merge depois
    df['codigo_subs'] = df['codigo_subs'].apply(lambda x: str(int(x)) if pd.notnull(x) else '')
    df['codigo_zonas'] = df['codigo_zonas'].apply(lambda x: str(int(x)) if pd.notnull(x) else '')

    return df