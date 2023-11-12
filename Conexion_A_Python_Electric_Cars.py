
#TABLE MAKER#
import psycopg2
try:
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'Proyecto_Final'
    )
    
    print("\n-------------------------------------------TABLA MAKER-------------------------------------------")
    cursor = connection.cursor()
    cursor.execute("select * from Maker")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)
    
finally:
    connection.close()



#TABLE COUNTY#
import psycopg2
try:
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'Proyecto_Final'
    )
    
    print("\n-------------------------------------------TABLA COUNTY-------------------------------------------")
    cursor = connection.cursor()
    cursor.execute("select * from County")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)
    
finally:
    connection.close()




#TABLE CITY#
import psycopg2
try:
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'Proyecto_Final'
    )
    
    print("\n-------------------------------------------TABLA CITY-------------------------------------------")
    cursor = connection.cursor()
    cursor.execute("select * from City")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)
    
finally:
    connection.close()



#TABLE CENSUS_TRACK#
import psycopg2
try:
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'Proyecto_Final'
    )
    
    print("\n-------------------------------------------TABLA CENSUS_TRACK-------------------------------------------")
    cursor = connection.cursor()
    cursor.execute("select * from Census_Track")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)
    
finally:
    connection.close()



#TABLE ELECTRIC-CARS-MODELS#
import psycopg2
try:
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'Proyecto_Final'
    )
    
    print("\n-------------------------------------------TABLA ELECTRIC-CARS-MODELS-------------------------------------------")
    cursor = connection.cursor()
    cursor.execute("select * from Electric-Cars-Models")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)
    
finally:
    connection.close()



#TABLE ELECTRIC-CARS-TYPE#
import psycopg2
try:
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'Proyecto_Final'
    )
    
    print("\n-------------------------------------------TABLA ELECTRIC-CARS-TYPE-------------------------------------------")
    cursor = connection.cursor()
    cursor.execute("select * from Electric_Cars_Type")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)
    
finally:
    connection.close()



#TABLE DOL_ID#
import psycopg2
try:
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'Proyecto_Final'
    )
    
    print("\n-------------------------------------------TABLA DOL_ID-------------------------------------------")
    cursor = connection.cursor()
    cursor.execute("select * from Dol_Id")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)
    
finally:
    connection.close()



#TABLE VEHICLES#
import psycopg2
try:
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'Proyecto_Final'
    )
    
    print("\n-------------------------------------------TABLA VEHICLES-------------------------------------------")
    cursor = connection.cursor()
    cursor.execute("select * from Vehicle")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)
    
finally:
    connection.close()



