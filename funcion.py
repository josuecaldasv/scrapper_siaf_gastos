## LIBRARIES
# ---

# Selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# For scraping
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Options driver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

# Dataframes
import pandas as pd
import itertools
import os

# Simulating human behavior
import datetime
import time
from time import sleep
import random

# Clear data
import unidecode

# Json files
import json
import re
import numpy as np
import itertools
from pandas import json_normalize

# To use explicit waits
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Download files
import urllib.request
import requests
from openpyxl import Workbook

## FUNCTION:
# ---------

def scrapper_siaf_gastos( anio, ruta_registro ):
    
    # Fijar tiempo
    start_time = time.time()
    
    # Fijar opciones
    options = Options()
    options.add_argument( '--start-maximized' )

    service = Service( ChromeDriverManager().install( ) )
    driver = webdriver.Chrome( service = service )
    driver.maximize_window()

    url = 'https://apps5.mineco.gob.pe/transparencia/Navegador/default.aspx?y=2007&ap=ActProy'
    driver.get( url )

    wait = WebDriverWait( driver, 300 )

    frame = driver.find_element( By.ID, "frame0" )
    driver.switch_to.frame( frame )

    # Lista de tablas
    all_tables = []
    
    # Seleccionar boton de año
    
    seleccionar_anio = Select( driver.find_element( By.ID, "ctl00_CPH1_DrpYear" ) )
    seleccionar_anio.select_by_value( f'{ anio }' )
    
    if anio != '2007':
        frame = driver.find_element( By.ID, "frame0" )
        driver.switch_to.frame( frame )
    else:
        pass
    
    with open( ruta_registro, 'w' ) as f:    

        # Seleccionar botones de niveles de gobierno y gobiernos locales
        niveles_gobierno  = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnTipoGobierno"]' ) ) )
        niveles_gobierno.click()

        gobiernos_locales = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_RptData_ctl02_TD0"]' ) ) )
        gobiernos_locales.click()

        # Iterar sobre regiones
        regiones_boton = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnDepartamento"]' ) ) )
        regiones_boton.click()
        regiones_lista = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )

        for region_index in range( len( regiones_lista ) ):
            region = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )[ region_index ]
            region_nombre = region.find_element( By.XPATH, './td[2]' ).text.strip()
            region.click()
            time.sleep( 2 )
            print( f'REGIÓN: { region_nombre }' )
            f.write(f'REGIÓN: { region_nombre }\n' )

            # Iterar sobre municipalidades
            municipalidades_boton   = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnMunicipalidad"]' ) ) )
            municipalidades_boton.click()
            municipalidades_lista   = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )

            for municipalidad_index in range( len( municipalidades_lista ) ):

                try:                
                    last_region_index        = region_index
                    last_municipalidad_index = municipalidad_index

                    municipalidad = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )[ municipalidad_index ]
                    municipalidad_nombre = municipalidad.find_element( By.XPATH, './td[2]' ).text.strip()
                    municipalidad.click()
                    time.sleep( 2 )
                    print( f'\nMUNICIPALIDAD: { municipalidad_nombre }\n' )
                    f.write(f'\nMUNICIPALIDAD: { municipalidad_nombre }\n' )

                    # Iterar sobre genericas de gasto
                    genericas_gasto_boton   = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnGrupoGasto"]' ) ) )
                    genericas_gasto_boton.click()
                    genericas_gasto_lista   = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )

                    for generica_gasto_index in range( len( genericas_gasto_lista ) ):
                        generica_gasto = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )[ generica_gasto_index ]
                        generica_gasto_nombre = generica_gasto.find_element( By.XPATH, './td[2]' ).text.strip()
                        generica_gasto.click()
                        time.sleep( 2 )
                        print( f'GENERICA DE GASTO: { generica_gasto_nombre }' )
                        f.write(f'GENERICA DE GASTO: { generica_gasto_nombre }\n' )

                        # Iterar sobre fuentes
                        fuentes_boton   = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnFuenteAgregada"]' ) ) )
                        fuentes_boton.click()
                        fuentes_lista   = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )

                        for fuente_index in range( len( fuentes_lista ) ):
                            fuente = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )[ fuente_index ]
                            fuente_nombre = fuente.find_element( By.XPATH, './td[2]' ).text.strip()
                            fuente.click()
                            time.sleep( 2 )
                            print( f'FUENTE: { fuente_nombre }' )
                            f.write(f'FUENTE: { fuente_nombre }\n' )

                            # Iterar sobre funciones
                            funciones_boton   = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnFuncion"]' ) ) )
                            funciones_boton.click()
                            funciones_lista   = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )

                            for funcion_index in range( len( funciones_lista ) ):
                                funcion = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )[ funcion_index ]
                                funcion_nombre = funcion.find_element( By.XPATH, './td[2]' ).text.strip()
                                funcion.click()
                                time.sleep( 2 )
                                print( f'FUNCIÓN: { funcion_nombre }' )
                                f.write(f'FUNCIÓN: { funcion_nombre }\n' )

                                # Iterar sobre rubros
                                rubro_boton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_CPH1_BtnRubro"]')))
                                rubro_boton.click()
                                rubros_lista = driver.find_elements(By.XPATH, "//tr[contains(@id, 'tr')]")

                                for rubro_index in range( len( rubros_lista ) ):
                                    rubro = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )[ rubro_index ]
                                    nombre_rubro = rubro.find_element( By.XPATH, './td[2]' ).text.strip()
                                    rubro.click()
                                    time.sleep( 2 )
                                    print( f'RUBRO: { nombre_rubro }' )
                                    f.write(f'RUBRO: { nombre_rubro }\n' )

                                    # Botón de programa
                                    programa_boton = wait.until(EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnPrograma"]' ) ) )
                                    programa_boton.click()

                                    # Extraer tabla html
                                    table_element = wait.until( EC.presence_of_element_located( ( By.XPATH, "//table[@class='Data']" ) ) )
                                    table_html = table_element.get_attribute( 'outerHTML' )
                                    table_df = pd.read_html( table_html )[ 0 ]

                                    # Agregar columna "rubro"
                                    table_df[ 'region' ]            = region_nombre
                                    table_df[ 'municipalidad' ]     = municipalidad_nombre
                                    table_df[ 'generica_de_gasto' ] = generica_gasto_nombre                            
                                    table_df[ 'fuente' ]            = fuente_nombre                            
                                    table_df[ 'funcion' ]           = funcion_nombre
                                    table_df[ 'rubro' ]             = nombre_rubro

                                    # Renombrar columnas                       
                                    table_df = table_df.rename( columns = {   
                                                        0: 'marca',
                                                        1: 'programa',
                                                        2: 'pia',
                                                        3: 'pim',
                                                        4: 'ejecucion_compromiso',
                                                        5: 'ejecucion_devengado',
                                                        6: 'ejecucion_grado',
                                                        7: 'porcentaje_avance',
                                                        'rubro_': 'rubro',
                                                        'funcion_': 'funcion',
                                                        'fuente_': 'fuente',
                                                        'generica_de_gasto_': 'generica_de_gasto',
                                                        'region_': 'region',
                                                        'municipalidad_': 'municipalidad' 
                                    } )

                                    # Crear ubigeo
                                    table_df[ 'ubigeo' ] = table_df[ 'municipalidad' ].str.split( ':' ).str[ 0 ].str[ :6 ]

                                    # Reordenar columnas
                                    table_df = table_df[ [ 'ubigeo', 'municipalidad', 'region', 'generica_de_gasto',
                                                           'fuente', 'funcion', 'rubro', 'programa', 'porcentaje_avance', 
                                                           'ejecucion_grado', 'ejecucion_devengado', 'ejecucion_compromiso',
                                                           'pim', 'pia' ] ]

                                    # Crear nombres para el directorio
                                    region_p                = region_nombre.split( ':' )[ 0 ].strip()
                                    ubigeo_p                = municipalidad_nombre.strip().split( ':' )[ 0 ][ :6 ]
                                    generica_p              = 'GN' + generica_gasto_nombre.split( ':' )[ 0 ].strip()
                                    fuente_p                = 'FT' + fuente_nombre.split( ':' )[ 0 ].strip()
                                    funcion_p               = 'FN' + funcion_nombre.strip().split( ':' )[ 0 ].strip()
                                    rubro_p                 = 'RB' + nombre_rubro.strip().split( ':' )[ 0 ].strip()
                                                                                                             
                                    # Guardar files
                                    folder_path = os.path.join( f'data_{ anio }', region_p, ubigeo_p )
                                    os.makedirs( folder_path, exist_ok = True )
                                    file_path   = os.path.join( folder_path, f'{ generica_p }_{ fuente_p }_{ funcion_p }_{ rubro_p }.xlsx' )
                                    table_df.to_excel( file_path )
                                    
                                    print( f'ARCHIVO: { file_path }' )
                                    f.write(f'ARCHIVO: { file_path }\n' )

                                    # Volver a rubro                      
                                    volver_rubro_boton = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_RptHistory_ctl08_TD0"]' ) ) )
                                    volver_rubro_boton.click()

                                # Volver a funciones:
                                volver_funciones_boton = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_RptHistory_ctl07_TD0"]' ) ) )
                                volver_funciones_boton.click()

                            # Volver a fuentes
                            volver_fuentes_boton = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_RptHistory_ctl06_TD0"]' ) ) )
                            volver_fuentes_boton.click()

                        # Volver a generica de gasto
                        volver_generica_gasto_boton = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_RptHistory_ctl05_TD0"]' ) ) )
                        volver_generica_gasto_boton.click()

                    # Volver a municipalidades
                    volver_municipalidades_boton = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_RptHistory_ctl04_TD0"]') ) )
                    volver_municipalidades_boton.click()

                except Exception as e:

                    print( '\nLa página web colapsó', str( e ) )
                    print( 'Reiniciando desde la última municipalidad scrapeada.\n' )
                    f.write('\nLa página web colapsó ' + str( e ) + '\n' ) 
                    f.write('Reiniciando desde la última municipalidad scrapeada.\n' ) 

                    # Cerrar sesión y reiniciar el navegador
                    driver.quit()
                    time.sleep( 600 )
                    driver = webdriver.Chrome(service = service )
                    driver.maximize_window()
                    driver.get( url )
                    wait = WebDriverWait( driver, 300 )

                    frame = driver.find_element( By.ID, "frame0" )
                    driver.switch_to.frame( frame )

                    # Volver a seleccionar el año y navegar hasta la última región scrappeada
                    seleccionar_anio = Select(driver.find_element( By.ID, "ctl00_CPH1_DrpYear" ) )
                    seleccionar_anio.select_by_value(f'{ anio }')

                    if anio != '2007':
                        frame = driver.find_element( By.ID, "frame0" )
                        driver.switch_to.frame( frame )

                    # Seleccionar botones de niveles de gobierno y gobiernos locales
                    niveles_gobierno  = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnTipoGobierno"]' ) ) )
                    niveles_gobierno.click()

                    gobiernos_locales = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_RptData_ctl02_TD0"]' ) ) )
                    gobiernos_locales.click()

                    # Navegar hasta la última región scrappeada
                    regiones_boton = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnDepartamento"]' ) ) )
                    regiones_boton.click()
                    regiones_lista = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )
                    for i in range( last_region_index + 1 ):
                        region = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]")[ i ]
                        region_nombre = region.find_element( By.XPATH, './td[2]' ).text.strip()
                        region.click()
                        time.sleep( 2 )
                        print(f'REGIÓN (Exception): { region_nombre }')
                        f.write(f'REGIÓN (Exception): { region_nombre }\n' )

                    # Navegar hasta la última municipalidad scrappeada
                    municipalidades_boton = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnMunicipalidad"]' ) ) )
                    municipalidades_boton.click()
                    municipalidades_lista = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )
                    for i in range( last_municipalidad_index + 1 ):
                        municipalidad = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]")[ i ]
                        municipalidad_nombre = municipalidad.find_element( By.XPATH, './td[2]' ).text.strip()
                        time.sleep( 2 )
                        print( f'\nMUNICIPALIDAD (Exception): { municipalidad_nombre }\n' )
                        f.write( f'\nMUNICIPALIDAD (Exception): { municipalidad_nombre }\n' )

                    continue

            # Volver a regiones
            volver_regiones_boton = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_RptHistory_ctl03_TD0"]' ) ) )
            volver_regiones_boton.click()
        
    # Cerrar sesión del driver
    f.close()
    driver.quit()