
## LIBRARIES:
# ----------


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

def scrapper_siaf_gastos( anio ):
    
    # Fijar opciones
    options = Options()
    options.add_argument( '--start-maximized' )

    service = Service( ChromeDriverManager().install( ) )
    driver = webdriver.Chrome( service = service )
    driver.maximize_window()

    url = 'https://apps5.mineco.gob.pe/transparencia/Navegador/default.aspx?y=2007&ap=ActProy'
    driver.get( url )

    wait = WebDriverWait( driver, 60 )

    frame = driver.find_element( By.ID, "frame0" )
    driver.switch_to.frame( frame )
    
    # Crear el directorio en caso no exista
    try:
        os.mkdir( f'siaf_datos_{ anio }' )
    except:
        pass

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
        region.click()
        time.sleep( 2 )
        region_nombre = region.find_element( By.XPATH, './td[2]' ).text.strip()
        print( f'REGIONES: { region_nombre }' )

        # Iterar sobre municipalidades
        municipalidades_boton   = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnMunicipalidad"]' ) ) )
        municipalidades_boton.click()
        municipalidades_lista   = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )

        for municipalidad_index in range( len( municipalidades_lista ) ):
            municipalidad = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )[ municipalidad_index ]
            municipalidad.click()
            time.sleep( 2 )
            municipalidad_nombre = municipalidad.find_element( By.XPATH, './td[2]' ).text.strip()
            print( f'MUNICIPALIDADES { municipalidad_nombre }' )

            # Iterar sobre genericas de gasto
            genericas_gasto_boton   = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnGrupoGasto"]' ) ) )
            genericas_gasto_boton.click()
            genericas_gasto_lista   = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )

            for generica_gasto_index in range( len( genericas_gasto_lista ) ):
                generica_gasto = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )[ generica_gasto_index ]
                generica_gasto.click()
                time.sleep( 2 )
                generica_gasto_nombre = generica_gasto.find_element( By.XPATH, './td[2]' ).text.strip()
                print( f'GENERICAS DE GASTO: { generica_gasto_nombre }' )

                # Iterar sobre fuentes
                fuentes_boton   = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnFuenteAgregada"]' ) ) )
                fuentes_boton.click()
                fuentes_lista   = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )

                for fuente_index in range( len( fuentes_lista ) ):
                    fuente = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )[ fuente_index ]
                    fuente.click()
                    time.sleep( 2 )
                    fuente_nombre = fuente.find_element( By.XPATH, './td[2]' ).text.strip()
                    print( f'FUENTES: { fuente_nombre }' )

                    # Iterar sobre funciones
                    funciones_boton   = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnFuncion"]' ) ) )
                    funciones_boton.click()
                    funciones_lista   = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )

                    for funcion_index in range( len( funciones_lista ) ):
                        funcion = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )[ funcion_index ]
                        funcion.click()
                        time.sleep( 2 )
                        funcion_nombre = funcion.find_element( By.XPATH, './td[2]' ).text.strip()
                        print( f'FUNCIONES: { funcion_nombre }' )

                        # Iterar sobre rubros
                        rubro_boton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_CPH1_BtnRubro"]')))
                        rubro_boton.click()
                        rubros_lista = driver.find_elements(By.XPATH, "//tr[contains(@id, 'tr')]")

                        for rubro_index in range( len( rubros_lista ) ):
                            rubro = driver.find_elements( By.XPATH, "//tr[contains(@id, 'tr')]" )[ rubro_index ]
                            rubro.click()
                            time.sleep( 2 )
                            nombre_rubro = rubro.find_element( By.XPATH, './td[2]' ).text.strip()
                            print( f'RUBROS: { nombre_rubro }' )

                            # Botón de programa
                            programa_button = wait.until(EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_BtnPrograma"]' ) ) )
                            programa_button.click()

                            # Extraer tabla html
                            table_element = wait.until( EC.presence_of_element_located( ( By.XPATH, "//table[@class='Data']" ) ) )
                            table_html = table_element.get_attribute( 'outerHTML' )
                            table_df = pd.read_html( table_html )[ 0 ]

                            # Agregar columna "rubro"
                            table_df[ 'rubro' ]             = nombre_rubro
                            table_df[ 'funcion' ]           = funcion_nombre
                            table_df[ 'fuente' ]            = fuente_nombre
                            table_df[ 'generica_de_gasto' ] = generica_gasto_nombre
                            table_df[ 'region' ]            = region_nombre
                            table_df[ 'municipalidad' ]     = municipalidad_nombre

                            # Agregar tabla al listado
                            all_tables.append( table_df )

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

        # Volver a regiones
        volver_regiones_boton = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//*[@id="ctl00_CPH1_RptHistory_ctl03_TD0"]' ) ) )
        volver_regiones_boton.click()

    # Concatenar todas las tablas
    final_table = pd.concat( all_tables, axis = 0 ).reset_index( drop = True )

    final_table = final_table.rename( columns = {   0: 'marca',
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
                                                    'municipalidad_': 'municipalidad' } )

    final_table[ 'ubigeo' ] = final_table[ 'municipalidad' ].str.split( ':' ).str[ 0 ].str[ :6 ]

    final_table = final_table[ [ 'ubigeo', 'municipalidad', 'region', 'generica_de_gasto',
                                 'fuente', 'funcion', 'rubro', 'programa', 'porcentaje_avance', 
                                 'ejecucion_grado', 'ejecucion_devengado', 'ejecucion_compromiso',
                                 'pim', 'pia' ] ]
    
    final_table.to_excel( f'siaf_datos_{ anio }/siaf_datos{ anio }.xlsx' )