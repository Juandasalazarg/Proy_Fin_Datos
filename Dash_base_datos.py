from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import psycopg2
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

try:
    # Conexión con la base de datos
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'Proyecto_Final'
    )
    app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])  # Creación de la aplicación
    load_figure_template('MORPH')  # Estilo de las gráficas
    cursor = connection.cursor()
    
    # Estilo de la página
    styles = {
        'main container': {  # Estilo del contenedor principal
            'position':'flex',
            'top':'0',
            'left':'0',
            'width': '100%',
        },

        'main column': {  # Estilo de la columna principal
            'border-radius': '20px',
            'margin-top': '1%', 
            'margin-bottom': '1%',
            'margin-left': '15%', 
            'margin-right': '15%',
            'background-color': '#E8F7EB',
            'box-shadow': '0 1px 6px rgba(0, 0, 0, 0.12), 0 1px 4px rgba(0, 0, 0, 0.24)'
        },
        
        'header': {  # Estilo del titulo
            'textAlign': 'center',
            'font-size': '40px',
            'font-weight': 'bold',
            'letter-spacing': '2px',
            'margin-top': '0',
            'border-bottom': '4px solid #C8DFEA'
        },
        
        'subtitle': {  # Estilo del subtitulo
            'font-size': '25px',
            'font-weight': 'bold',
            'margin': '20px'
        },

        'content': {  # Estilo del texto
            'font-size': '18px',
            'line-height': '1.6',
            'padding-left': '25px',
            'padding-right': '25px'
        },
        
        'indentation': {
            'margin-left': '15px',
            'margin-bottom': '0'
        },

        'graph': {  # Estilo de las gráficas
            'box-shadow': '0 2px 5px rgba(0, 0, 0, 0.1)',
            'height': '750px'
        },
        
        'graph container': {  # Estilo del contenedor de las gráficas
            'margin': '0 auto',
            'max-width': '90%',
            'justify-content': 'center', 
            'align-items': 'center'
        }
    }

    # Todas las Consultas
    # Consulta ventas por categoria
    cursor.execute('''
        SELECT
            M.Model_name,
            EC.Electric_type,
            MAX(EC.Electric_range) AS Electric_range,
            MAX(EC.Clean_Alternative_Fuel_Vehicle) AS Clean_Alternative_Fuel_Vehicle
        FROM Electric_Cars_Models M
        JOIN Electric_Cars_Type EC ON M.Model_name = EC.Car_Model_name
        WHERE EC.Electric_type IS NOT NULL
            AND EC.Electric_range IS NOT NULL
            AND EC.Clean_Alternative_Fuel_Vehicle IS NOT NULL
        GROUP BY
            M.Model_name,
            EC.Electric_type;
        ''')
    rows = cursor.fetchall()

    # Visualización de barras
    fig11 = px.bar(rows, x=0,y=2, color=0,
                labels={0: 'Modelo', 1: 'Tipo de Energía Eléctrica', 2: 'Autonomía Eléctrica',},
                title='Eficiencia Energética de Vehículos Eléctricos',
                template='plotly_dark')
    

    
    # Crea el gráfico de barras con los datos filtrados
    fig12 = px.bar(rows, x=2, color=3,
                labels={2: 'Autonomía Eléctrica', 1: 'Tipo de Energía Eléctrica',
                        3: 'Elegibilidad para CAFV'},
                title=' Clean Alternative Fuel Vehicle (CAFV) Eligibility',
                template='plotly_dark')

# Consulta ventas por categoria
    cursor.execute('''WITH VentasPorMarca AS (
    SELECT
        Maker.Maker_Name,
        Vehicle.Id_county,
        Vehicle.City_Name,
        Vehicle.Model_year,
        COUNT(Vehicle.DOL_Vehicle) AS VentasTotales
    FROM
        Vehicle
    JOIN
        Electric_Cars_Models ON Vehicle.Car_Model_name = Electric_Cars_Models.Model_name
    JOIN
        Maker ON Electric_Cars_Models.Id_maker = Maker.Id_Maker
    GROUP BY
        Maker.Maker_Name,
        Vehicle.Id_county,
        Vehicle.City_Name,
        Vehicle.Model_year
    )

    SELECT
        VentasPorMarca.Maker_Name,
        County.County_Name,
        VentasPorMarca.City_Name,
        VentasPorMarca.Model_year,
        VentasPorMarca.VentasTotales
    FROM
        VentasPorMarca
    JOIN
        County ON VentasPorMarca.Id_county = County.Id_county
    WHERE
        VentasPorMarca.VentasTotales > 0; -- Ajusta este criterio según tus necesidades
    ''')
    rows2 = cursor.fetchall()

    # Grafico de barras apiladas
    fig13 = px.bar(rows2, x=0, y=1, color=2,
               labels={1: 'Total de Ventas', 0: 'Marca', 2: 'County_Name'},
               title='Ventas de Vehículos Eléctricos por Marca y Condado',
               template='plotly_dark',
               opacity=0.7)  


    fig14 = px.scatter(rows2, x=0, y=1, color=2,
                 labels={1: 'Total de Ventas', 0: 'Marca', 2: 'Condado'},
                 title='Ventas de Vehículos Eléctricos por Marca y Condado',
                 template='plotly_dark')

    

    fig15 = px.strip(rows2, x=0, y=1, color=2,
              labels={1: 'Ventas Totales', 2: 'Año Modelo', 1: 'Marca'},
              title='Evolución de las Ventas de Vehículos Eléctricos por Marca y Año Modelo',
              template='plotly_dark')



    # Consulta ventas por categoria
    cursor.execute('''
                   SELECT
                        County.County_Name,
                        Electric_Cars_Type.Electric_type,
                        Electric_Cars_Models.Model_name,
                        COUNT(*) AS Cantidad_Preferencias
                    FROM Vehicle
                    JOIN County ON Vehicle.Id_county = County.Id_county
                    JOIN Electric_Cars_Type ON Vehicle.Car_Model_name = Electric_Cars_Type.Car_Model_name
                    JOIN Electric_Cars_Models ON Electric_Cars_Type.Id_maker = Electric_Cars_Models.Id_maker
                    GROUP BY County.County_Name, Electric_Cars_Type.Electric_type, Electric_Cars_Models.Model_name
                    ORDER BY County.County_Name, Cantidad_Preferencias DESC;
    ''')
    rows3 = cursor.fetchall()

    
    fig17 = px.bar(rows3, x=0,y=2, color=1, labels={'0': 'Condado', '1': 'Electric_Type', '2': 'Modelo'},
                       title='Preferencias de Tipo Electrico por Condado y Marca',
                       template='plotly_dark',)
    


    

    fig18 = px.scatter(rows3, x=0,y=2, color=1, labels={'0': 'Condado', '1': 'Electric_Type', '2': 'Modelo'},
                       title='Preferencias de Tipo Electrico por Condado y Marca',
                       template='plotly_dark',)
    
    fig18.update_traces(marker_size=8)

    fig19 = px.pie(rows3, names=0, values=2, color=1,
               labels={'0': 'Condado', '1': 'Electric_Type'},
               title='Preferencias por Condado ',
               template='plotly_dark',
    )
    



    #-----------------------------------------VENTAS POR AÑO--------------------------------#
    cursor.execute('''
                   SELECT
                        Model_year,
                        COUNT(*) AS Cantidad_Vehiculos_Electricos
                    FROM
                        vehicle
                    GROUP BY
                        Model_year
                    ORDER BY
                        Model_year;
    ''')
    rows4 = cursor.fetchall()


    fig20 = px.bar(rows4, x=0, y=1 , labels={'0': 'AÑO', '1': 'Ventas(en unidades)'},
                   title='VENTAS POR AÑO -BARRAS',template='plotly_dark')



    fig21 = px.funnel(rows4, x=0, y=1, labels={'0': 'AÑO', '1': 'Ventas(en unidades)'},
                      title='VENTAS POR AÑO- EMBUDO',template='plotly_dark')


    fig22 = px.scatter(rows4, x=0, y=1, labels={'0': 'AÑO', '1': 'Ventas(en unidades)'},
                       title='VENTAS POR AÑO -DISPERSION',template='plotly_dark')
    fig22.update_traces(marker_size=10)
    



    cursor.execute('''
                   WITH RankedBrands AS (
                    SELECT
                        V.Id_county,
                        M.Maker_Name AS Marca,
                        COUNT(*) AS Cantidad_Vehiculos,
                        ROW_NUMBER() OVER (PARTITION BY V.Id_county ORDER BY COUNT(*) DESC) AS Rank
                    FROM
                        Vehicle V
                        JOIN Electric_Cars_Models ECM ON V.Car_Model_name = ECM.Model_name
                        JOIN Maker M ON ECM.Id_maker = M.Id_Maker
                    GROUP BY
                        V.Id_county, M.Maker_Name
                )
                SELECT
                    Id_county,
                    Marca AS Marca_Mas_Vendida
                FROM
                    RankedBrands
                WHERE
                    Rank = 1;

    ''')
    rows5 = cursor.fetchall()

    fig23 = px.scatter(rows5, x=0, y=1 ,color = 0, labels={'0': 'COUNTY_ID', '1': 'MARCA MAS VENDIDA'},
                   title='MARCA MAS VENDIDA EN EL ESTADO- Dispersion ',template='plotly_dark')

    


    fig24 = px.pie(rows5, names=1, values=0,
                title='Promedio De la marca que mas vende en los estados',
                template='plotly_dark')




    fig25 = px.bar_polar(rows5, theta=1, r=0 ,color = 0, labels={'0': 'COUNTY_ID', '1': 'MARCA MAS VENDIDA'},
                   title='MARCA MAS VENDIDA EN EL ESTADO ',template='plotly_dark')


    app.layout = dbc.Container(
        style= styles['main container'],  #Div para aplicar el estilo a toda la página
        children=html.Div(
            children=[ #Div con toda la información de la columna principal
                
                #Titulo de la página
                html.H1(
                    children='Base De Datos Carros Electricos Washington : Entrega Final - Análisis de escenarios', 
                    style=styles['header'],
                ),
                
                html.Br(),
                
                #Introducción
                html.P(
                    children=['''Este proyecto está fundamentado en una base de datos que se encarga de recopilar todos los
                    datos que contienen información sobre la población de vehículos eléctricos en el estado de
                    Washington, Estados Unidos. Estos datos fueron recopilados el 9 de octubre de 2023 y vienen
                    del departamento de ventas de Washington Dc, por lo que setiene la certeza de que son datos
                    recientes y confiables.''',
                    
                    html.Br(),
                    html.Br(),
                    
                    html.Strong('LINK BASE DE DATOS: https://www.kaggle.com/datasets/amirhosseinzinati/electric-vehicle-population-data'),
                    
                    html.Br(),
                    html.Br(),
                    html.Strong('Análisis Integral del Mercado de Vehículos Eléctricos en Washington:  '),
                    '''Descubrir patrones y tendencias en la adopción de vehículos eléctricos, como los modelos más demandados, 
                    las marcas preferidas, y las variaciones estacionales en la demanda, es esencial para comprender 
                    el mercado de carros eléctricos en Washington. Estos conocimientos pueden proporcionar valiosa información
                    a fabricantes, concesionarios y autoridades locales, permitiéndoles tomar decisiones estratégicas 
                    basadas en datos sólidos. Desde ajustar la oferta de modelos hasta desarrollar estrategias de promoción, 
                    estas percepciones ayudarán a optimizar el desempeño de la industria de vehículos eléctricos en la región.''',
                    html.Br(),
                    html.Br(),
                    html.Strong('Análisis de Patrones de Adquisición y Proyección de la Demanda Futura de Vehículos Eléctricos en la Ciudad: '),
                    '''Analizar Patrones de Adquisición y Proyectar la Demanda Futura de Vehículos Eléctricos en la Ciudad. 
                    Esta Evaluación es Esencial para Garantizar un Suministro Adecuado y Prevenir Problemas Relacionados con 
                    la Escasez o el Excedente de Inventarios en el Sector de Vehículos Eléctricos.''',
                    html.Br(),
                    html.Br(),
                    html.Strong('Exploración de Segmentos en el Mercado de Vehículos Eléctricos: '),
                    '''Identificación de Segmentos Específicos en el Mercado de Vehículos Eléctricos: Explorando Diferencias 
                    Demográficas y Geográficas en los Patrones de Adquisición. La Identificación de Estos Segmentos Facilita 
                    la Adaptación de Estrategias Comerciales y de Oferta, Alineándolas con las Preferencias y Necesidades de 
                    Cada Grupo.''',
                    html.Br(),
                    html.Br(),
                    html.Strong('Realizar estudios de precios y rentabilidad: '),
                    '''"Análisis de Precios, Márgenes de Beneficio y Rentabilidad en el Mercado de Vehículos Eléctricos: 
                    Información Crucial para Estrategias de Precios y Evaluación de la Viabilidad Económica."''',
                    html.Br(),
                    html.Br(),
                    html.Strong('Optimización de Investigaciones de Mercado en el Proyecto de Vehículos Eléctricos:'),
                    '''Exploración Exhaustiva al Integrar Datos Detallados de Consumo, Analizar Perfiles Demográficos y
                      Comprender Comportamientos del Consumidor. Este Enfoque Profundo Proporciona un Conocimiento Integral y 
                      Detallado de los Factores que Influyen en las Preferencias y Decisiones de Compra, Permitiendo una Toma de 
                      Decisiones Informada y una Adaptación Precisa de Estrategias para el Futuro Sostenible del Transporte Eléctrico.''',
                    html.Br(),
                    html.Br(),
                    '''A continuación realizaremos un analisis a profundidad de cada uno de los escenarios elegidos:'''
                    ],
                    style=styles['content']
                ),

            
                html.Div(
                    children=[
                        html.H2(
                            children='1. Eficiencia energética de los vehículos eléctricos',
                            style=styles['subtitle'],
                        ),

                        html.Div(
                            children=html.P(
                                children='''Para observar como es la eficiencia energética de todos los vehiculos 
                                en el estado de washington, 
                                se consulta la relacion entre la marca, el modelo y su rango de carga. A continuación 
                                se presentan las sentencias SQL y las gráficas realizadas que dejan ver de manera clara 
                                la consulta que 
                                queremos hacer.''',
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Br(),

                        html.Div(
                            children=html.P(
                                children=html.Strong('Sentencia: '),
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Pre(
                            children= ['\tSELECT\n',
                    '\t\tM.Model_name,\n',
                    '\t\tEC.Electric_type,\n',
                    '\t\tMAX(EC.Electric_range) AS Electric_range,\n',
                    '\t\tMAX(EC.Clean_Alternative_Fuel_Vehicle) AS Clean_Alternative_Fuel_Vehicle\n',
                    '\tFROM Electric_Cars_Models M\n',
                    '\tJOIN Electric_Cars_Type EC ON M.Model_name = EC.Car_Model_name\n',
                    '\tWHERE EC.Electric_type IS NOT NULL\n',
                    '\t\tAND EC.Electric_range IS NOT NULL\n',
                    '\t\tAND EC.Clean_Alternative_Fuel_Vehicle IS NOT NULL\n',
                    '\tGROUP BY\n',
                    '\t\tM.Model_name,\n',
                    '\t\tEC.Electric_type;']

                           
                        ),



                        html.Br(),

                        html.Div(
                            children=html.P(
                                children=html.Strong('Gráficas: '),
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Div(
                            children=dcc.Graph(
                                id='Barras-Cat',
                                figure=fig11,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        html.Br(),
                        
                        html.Div(
                            dcc.Graph(
                                id='Embudo-Cat',
                                figure=fig12,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        

                        html.Br(),

                        html.Div(
                            children=html.P(
                                children=[
                                html.Strong('Analisis: '),
                                html.Br(),
                                html.Strong('Juan David: '),
                                '''Tras un análisis detenido de las gráficas presentadas, se revela un panorama revelador 
                                respecto a la eficiencia energética de los vehículos en venta en el estado de Washington. 
                                En primer lugar, se destaca la notoria falta de pruebas exhaustivas en la gran mayoría de los vehículos 
                                disponibles, evidenciando una carencia en la evaluación de su rendimiento energético.

                                Es especialmente destacable que muchos de estos vehículos aún no han 
                                sido clasificados en términos de su alcance o autonomía adecuada para entornos urbanos. 
                                Este aspecto es de particular importancia, ya que los compradores actuales están mostrando 
                                un interés significativo en la autonomía de sus vehículos, buscando opciones que satisfagan 
                                sus necesidades de movilidad en el ámbito citadino.

                                A pesar de la presencia de vehículos cuya autonomía ha sido probada, 
                                se observa una discrepancia notable entre la realidad actual y las expectativas de los consumidores. 
                                La distancia recorrida por los vehículos con autonomía confirmada es considerablemente menor de lo que
                                  se anticipa para este tipo de vehículos, lo que plantea interrogantes significativos sobre la 
                                  capacidad de satisfacer las demandas y expectativas de los consumidores. ''',
                                ],
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        )
                    ]
                ),

                #2. Sección de ingresos anuales por venta de licor
                html.Div(
                    children=[
                        html.H2(
                            children='2. Cambios en la participación de mercado de las marcas de vehículos',
                            style=styles['subtitle']
                        ),
                        
                        html.Div(
                            children=html.P(
                                children='''Para analizar los cambios de participacion en las ventas de las marcas de automoviles
                                se consultan las ventas por marca de los vehiculos. A continuación 
                                se presentan las gráficas realizadas y la sentencia SQL que deja ver de manera clara la consulta que 
                                queremos hacer.''',
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Div(
                            children=html.P(
                                children=html.Strong('Sentencia: '),
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                         html.Pre(
                            children= ['\tWITH VentasPorMarca AS (\n',
                            '\t\tSELECT\n',
                            '\t\t\tMaker.Maker_Name,\n',
                            '\t\t\tVehicle.Id_county,\n',
                            '\t\t\tVehicle.City_Name,\n',
                            '\t\t\tVehicle.Model_year,\n',
                            '\t\t\tCOUNT(Vehicle.DOL_Vehicle) AS VentasTotales\n',
                            '\t\tFROM\n',
                            '\t\t\tVehicle\n',
                            '\t\tJOIN\n',
                            '\t\t\tElectric_Cars_Models ON Vehicle.Car_Model_name = Electric_Cars_Models.Model_name\n',
                            '\t\tJOIN\n',
                            '\t\t\tMaker ON Electric_Cars_Models.Id_maker = Maker.Id_Maker\n',
                            '\t\tGROUP BY\n',
                            '\t\t\tMaker.Maker_Name,\n',
                            '\t\t\tVehicle.Id_county,\n',
                            '\t\t\tVehicle.City_Name,\n',
                            '\t\t\tVehicle.Model_year\n',
                            '\t)\n',
                            '\n',
                            '\tSELECT\n',
                            '\t\tVentasPorMarca.Maker_Name,\n',
                            '\t\tCounty.County_Name,\n',
                            '\t\tVentasPorMarca.City_Name,\n',
                            '\t\tVentasPorMarca.Model_year,\n',
                            '\t\tVentasPorMarca.VentasTotales\n',
                            '\tFROM\n',
                            '\t\tVentasPorMarca\n',
                            '\t\tJOIN\n',
                            '\t\tCounty ON VentasPorMarca.Id_county = County.Id_county\n',
                            '\tWHERE\n',
                            '\t\tVentasPorMarca.VentasTotales > 0;\n'
                        ]

                           
                        ),


                        html.Br(),
                        
                        html.Div(
                            children=html.P(
                                children=html.Strong('Gráficas: '),
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Div(
                            dcc.Graph(
                                id='Barras-An',
                                figure=fig14,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        html.Br(),
                        
                        html.Div(
                            dcc.Graph(
                                id='Pie-An',
                                figure=fig13,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        html.Br(),
                        
                        html.Div(
                            dcc.Graph(
                                id='Linea-An',
                                figure=fig15,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        html.Br(),
                        
                        

                        html.Div(
                            children=html.P(
                                children=[
                                html.Strong('Análisis: '),
                                html.Br(),
                                html.Strong('Juan David: '),
                                '''En consonancia con los análisis presentados en los diagramas, se observa que Tesla 
                                sobresale como la marca preeminente en términos de ventas de vehículos eléctricos en la 
                                mayoría de los condados examinados. Este patrón distintivo indica no solo una presencia 
                                consolidada en el mercado, sino también una preferencia considerable por parte de los consumidores 
                                hacia los productos de Tesla en comparación con otras marcas.

                                Además, se evidencia un fenómeno interesante en la industria de vehículos eléctricos a 
                                través de la expansión de otras marcas en este segmento de mercado. Diversas marcas han 
                                incursionado en la producción y comercialización de vehículos eléctricos, lo que refleja 
                                un crecimiento notorio en el interés y la adopción de esta línea de automóviles. 
                                Este fenómeno apunta a una tendencia ascendente en la aceptación de los vehículos eléctricos 
                                en general, no limitada exclusivamente a Tesla.''',
                                
                                ],
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        )
                    ]
                ),

                #3. Preferencias de Tipo Electrico por Condado y Marca
                html.Div(
                    children=[
                        html.H2(
                            children='3. Preferencias de Tipo Electrico por Condado y Marca',
                            style=styles['subtitle']
                        ),
                        
                        html.Div(
                            children=html.P(
                                children='''En aras de explorar las tendencias y preferencias relacionadas con los tipos de 
                                vehículos eléctricos en el marco de este proyecto, se emprende un análisis detallado de 
                                las elecciones de los consumidores en cada condado. Este estudio se enfoca en discernir 
                                las preferencias particulares de los usuarios en términos de tipos específicos de vehículos eléctricos, 
                                proporcionando así una visión detallada de la dinámica del mercado en cada ubicación geográfica.. A continuación
                                se presentan las gráficas y la sentencia SQL realizada que dejan ver de manera clara la consulta que 
                                queremos hacer.''',
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Div(
                            children=html.P(
                                children=html.Strong('Sentencia: '),
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Pre(
                            children=[
                                '\tSELECT\n',
                                '\t\tCounty.County_Name,\n',
                                '\t\tElectric_Cars_Type.Electric_type,\n',
                                '\t\tElectric_Cars_Models.Model_name,\n',
                                '\t\tCOUNT(*) AS Cantidad_Preferencias\n',
                                '\tFROM Vehicle\n',
                                '\tJOIN County ON Vehicle.Id_county = County.Id_county\n',
                                '\tJOIN Electric_Cars_Type ON Vehicle.Car_Model_name = Electric_Cars_Type.Car_Model_name\n',
                                '\tJOIN Electric_Cars_Models ON Electric_Cars_Type.Id_maker = Electric_Cars_Models.Id_maker\n',
                                '\tGROUP BY County.County_Name, Electric_Cars_Type.Electric_type, Electric_Cars_Models.Model_name\n',
                                '\tORDER BY County.County_Name, Cantidad_Preferencias DESC;\n'
                            ]
                           
                        ),

                        html.Br(),
                        
                        html.Div(
                            children=html.P(
                                children=html.Strong('Gráficas: '),
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Div(
                            dcc.Graph(
                                id='Barras-Con',
                                figure=fig17,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        html.Br(),
                        
                        html.Div(
                            dcc.Graph(
                                id='Dispersion-Con',
                                figure=fig18,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        html.Br(),
                        
                        html.Div(
                            dcc.Graph(
                                id='Calor-Con',
                                figure=fig19,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        

                        html.Br(),

                        html.Div(
                            children=html.P(
                                children=[
                                html.Strong('Análisis: '),
                                html.Br(),
                                html.Strong('Juan David: '),
                                '''A partir de los análisis gráficos presentados, emerge una dinámica competitiva claramente 
                                delineada entre dos categorías de vehículos eléctricos específicas: el automóvil eléctrico 
                                convencional y el automóvil eléctrico híbrido enchufable. Estos resultados indican un proceso 
                                de transición gradual en el cual los consumidores parecen optar por la adopción progresiva de 
                                tecnologías más sostenibles en el ámbito de la movilidad.

                                Se destaca una tendencia discernible en la cual los vehículos híbridos enchufables están emergiendo 
                                como la elección inicial predominante durante esta transición. Este fenómeno sugiere que, en el 
                                proceso de adopción de vehículos eléctricos, la población tiende a realizar una transición gradual, 
                                optando por vehículos híbridos antes de abrazar plenamente la movilidad eléctrica.\n

                                La preferencia por los automóviles híbridos enchufables puede interpretarse como un indicativo 
                                de la comodidad y la aceptación progresiva de las tecnologías eléctricas. Este patrón de cambio
                                  gradual de preferencias implica que la transición hacia los vehículos eléctricos puros podría 
                                materializarse en etapas subsiguientes.

                                En términos de condados, este comportamiento sugiere que las preferencias en 
                                la elección de vehículos eléctricos pueden variar según la ubicación geográfica. 
                                Un entendimiento más profundo de estos patrones específicos por condado podría ser esencial para 
                                la planificación estratégica de la infraestructura de carga y la promoción de vehículos eléctricos 
                                en diferentes regiones.''',
                                
                                ],
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        )
                    ]
                ),
                
                #4. VENTAS POR AÑO
                html.Div(
                    children=[
                        html.H2(
                            children='4. VENTAS POR AÑO',
                            style=styles['subtitle']
                        ),
                        
                        html.Div(
                            children=html.P(
                                children='''Con el objetivo de identificar el aumento de la demanda de los vehiculos electricos, se 
                                consulta el año con mayor volumen de ventas A continucación se presentan las gráficas 
                                realizadas y la sentencia SQL que deja ver de manera clara la consulta que queremos hacer.''',
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Div(
                            children=html.P(
                                children=html.Strong('Sentencia: '),
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Pre(
                            children=[
                                    '\tSELECT\n',
                                    '\t\tModel_year,\n',
                                    '\t\tCOUNT(*) AS Cantidad_Vehiculos_Electricos\n',
                                    '\tFROM\n',
                                    '\t\tvehicle\n',
                                    '\tGROUP BY\n',
                                    '\t\tModel_year\n',
                                    '\tORDER BY\n',
                                    '\t\tModel_year;\n'
                                ]
                                                        
                        ),

                        html.Br(),

                        html.Div(
                            children=html.P(
                                children=html.Strong('Gráficas: '),
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Div(
                            dcc.Graph(
                                id='Barras-Men',
                                figure=fig20,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        html.Br(),
                        
                        html.Div(
                            dcc.Graph(
                                id='Pie-Men',
                                figure=fig21,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        html.Br(),
                        
                        html.Div(
                            dcc.Graph(
                                id='Linea-Men',
                                figure=fig22,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        

                        html.Br(),

                        html.Div(
                            children=html.P(
                                children=[
                                html.Strong('Análisis: '),
                                html.Br(),
                                html.Strong('Juan David: '),
                                '''La exploración detallada de los gráficos revela un aumento constante y progresivo 
                                en las ventas de vehículos eléctricos a lo largo del tiempo. Este fenómeno se manifiesta 
                                de manera notoria a partir del año 2011, marcando el inicio de un ascenso continuo en las ventas de 
                                estos vehículos.

                                La tendencia de crecimiento exhibe una naturaleza exponencial, alcanzando su punto máximo en el año
                                  2023 con una cifra destacada de casi 30,000 unidades vendidas en un solo estado de los Estados 
                                  Unidos, específicamente en Washington (WA). Este incremento sostenido a lo largo de los años, y 
                                  la notable cifra alcanzada en 2023, reflejan no solo un interés creciente por los vehículos 
                                  eléctricos, sino también una adopción significativa de esta tecnología en la región.

                                El hecho de que las ventas de vehículos eléctricos hayan alcanzado niveles tan notables es 
                                una señal positiva tanto para el país como para el medio ambiente en general. Este aumento no solo
                                  evidencia un cambio en las preferencias de los consumidores hacia opciones más sostenibles, sino
                                    que también contribuye al esfuerzo global por reducir las emisiones de gases de efecto invernadero
                                      y promover prácticas de movilidad más respetuosas con el medio ambiente.''',
                                
                                ],
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        )
                    ]
                ),
 
                #5. MARCA MAS VENDIDA EN EL ESTADO
                html.Div(
                    children=[
                        html.H2(
                            children='5. Marca mas vendida en el estado',
                            style=styles['subtitle']
                        ),
                        
                        html.Div(
                            children=html.P(
                                children='''Con el propósito de realizar una comparativa exhaustiva entre las marcas 
                                más vendidas en los distintos estados, se lleva a cabo una consulta detallada que permite analizar
                                      y contrastar la presencia y preferencias del mercado en cada región. 
                                      Esta indagación se enfoca en identificar cuál es la marca que lidera las ventas en cada estado, 
                                      ofreciendo una visión integral de la dinámica competitiva en el ámbito de los vehículos eléctricos
                                        a nivel estatal. 
                                A continuación se presentan las gráficas y sentecias SQL realizadas que dejan ver de manera clara la 
                                consulta que queremos hacer.''',
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),
                        
                        html.Div(
                            children=html.P(
                                children=html.Strong('Sentencia: '),
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Pre(
                            children=[
                                '\tWITH RankedBrands AS (\n',
                                '\t\tSELECT\n',
                                '\t\t\tV.Id_county,\n',
                                '\t\t\tM.Maker_Name AS Marca,\n',
                                '\t\t\tCOUNT(*) AS Cantidad_Vehiculos,\n',
                                '\t\t\tROW_NUMBER() OVER (PARTITION BY V.Id_county ORDER BY COUNT(*) DESC) AS Rank\n',
                                '\t\tFROM\n',
                                '\t\t\tVehicle V\n',
                                '\t\t\tJOIN Electric_Cars_Models ECM ON V.Car_Model_name = ECM.Model_name\n',
                                '\t\t\tJOIN Maker M ON ECM.Id_maker = M.Id_Maker\n',
                                '\t\tGROUP BY\n',
                                '\t\t\tV.Id_county, M.Maker_Name\n',
                                '\t)\n',
                                '\tSELECT\n',
                                '\t\tId_county,\n',
                                '\t\tMarca AS Marca_Mas_Vendida\n',
                                '\tFROM\n',
                                '\t\tRankedBrands\n',
                                '\tWHERE\n',
                                '\t\tRank = 1;\n'
                            ]

                                                        
                        ),
                        
                        html.Br(),


                        html.Div(
                            children=html.P(
                                children=html.Strong('Gráficas: '),
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        ),

                        html.Div(
                            dcc.Graph(
                                id='Barras-Cos',
                                figure=fig23,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        html.Br(),
                        
                        html.Div(
                            dcc.Graph(
                                id='Dispersión-Cos',
                                figure=fig24,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),
                        
                        html.Br(),
                        
                        html.Div(
                            dcc.Graph(
                                id='Embudo-Cos',
                                figure=fig25,
                                style=styles['graph']
                            ),
                            style=styles['graph container']
                        ),

                        html.Br(),

                        html.Div(
                            children=html.P(
                                children=[
                                html.Strong('Analisis: '),
                                html.Br(),
                                html.Strong('Juan David : '),
                                '''Al analizar detalladamente los diagramas, se destaca una marcada diversidad en las ventas
                                  de vehículos eléctricos, especialmente por parte de Tesla. En 39 condados, Tesla emerge como 
                                  el fabricante líder en ventas, evidenciando una ventaja significativa. Este liderazgo de Tesla 
                                  puede atribuirse a su papel pionero en la adopción masiva de vehículos eléctricos, marcando la 
                                  pauta en este emergente mercado.

                                La posición destacada de Tesla refleja su influencia y éxito continuo en la promoción de vehículos 
                                eléctricos. Su presencia dominante en un extenso número de condados sugiere una aceptación generalizada
                                  de la marca y una preferencia por sus modelos entre los consumidores. Este fenómeno también señala 
                                  la importancia de ser el primero en introducirse en un mercado en evolución.

                                Es interesante notar que en algunos estados, como Nissan, Ford o Chevrolet, asumen la delantera en 
                                lugar de Tesla. Esta variación podría indicar patrones específicos relacionados con preferencias 
                                regionales o condiciones económicas particulares. La observación de que estos fabricantes alternativos
                                  lideran en ciertos estados podría sugerir que estas áreas, posiblemente de características más 
                                  rurales, encuentran más atractivas las ofertas de estos fabricantes en lugar de los modelos de Tesla.
                                      ''',
                                
                                ],
                                style=styles['content']
                            ),
                            style=styles['indentation']
                        )      
                    ]
                ),

                

                html.H2(
                    children='Conclusiones',
                    style=styles['subtitle'],
                ),
                
                html.Div(
                    children=html.P(
                        children=[
                            '''
                            Luego de analizar exhaustivamente los datos y realizar diversas consultas en el 
                            proyecto de vehículos eléctricos en Washington, se pueden extraer varias conclusiones clave:

                            Tesla lidera en ventas:

                            Tesla se destaca como el fabricante líder en ventas en la mayoría de los condados y estados analizados. 
                            Su posición dominante puede atribuirse a su papel pionero en la adopción de vehículos eléctricos y a la calidad 
                            de sus modelos.

                            Variedad de preferencias regionales:

                            Se observa una variabilidad en las preferencias de marca en diferentes estados y condados. Nissan, Ford
                            y Chevrolet, en ocasiones, superan a Tesla, indicando patrones específicos relacionados con preferencias 
                            regionales y condiciones económicas.

                            Crecimiento sostenido en ventas:

                            A lo largo de los años, se evidencia un crecimiento sostenido en las ventas de vehículos eléctricos 
                            en el estado de Washington. Este aumento progresivo señala una creciente aceptación y adopción de la 
                            tecnología eléctrica en la región.

                            Desafíos en la clasificación de eficiencia:

                            Se identifican desafíos en la clasificación de eficiencia de los vehículos, ya que muchos de ellos aún 
                            no han sido plenamente evaluados en términos de autonomía y eficiencia. Esto destaca la necesidad de una 
                            evaluación más exhaustiva para proporcionar información precisa a los consumidores.

                            Influencia de factores geográficos:

                            Las preferencias de marca pueden estar influenciadas por factores geográficos y de estilo de vida. 
                            Mientras Tesla domina en áreas urbanas, otros fabricantes pueden encontrar éxito en regiones más rurales, 
                            donde las necesidades de movilidad son diferentes.

                            Potencial para la expansión del mercado:

                            El crecimiento constante en las ventas sugiere un potencial significativo para la expansión del mercado 
                            de vehículos eléctricos en Washington. Los fabricantes y las autoridades podrían considerar estrategias 
                            para aprovechar este crecimiento.

                            Importancia de comprender dinámicas regionales:

                            La variabilidad en las preferencias destaca la importancia de comprender las dinámicas regionales 
                            para los fabricantes de automóviles. Adaptar estrategias de marketing y productos según las 
                            preferencias locales puede ser crucial para el éxito en mercados específicos.

                            En conjunto, el proyecto proporciona una visión integral del panorama de vehículos eléctricos en Washington, 
                            subrayando tanto los éxitos como los desafíos en este sector en evolución. Las conclusiones extraídas pueden ser 
                            fundamentales para fabricantes, reguladores y consumidores que buscan entender y contribuir al crecimiento 
                            sostenible de la movilidad eléctrica.
                            ''',
                        html.Br(),
                        html.Br(),
                        html.Sub(
                            children='''Trabajo realizado por Juan David Salazar.'''
                        ),
                        html.Br(),
                        html.Br()
                        ],
                        style=styles['content']
                    ),
                    style=styles['indentation']
                )
            ],
            style=styles['main column'],
        ),
        className='dbc'
    )
    
    if __name__ == '__main__':
        app.run_server(debug=False)


   










except Exception as ex:
    print(ex)
    
finally:
    connection.close()