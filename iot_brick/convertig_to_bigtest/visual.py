
from asyncio.windows_events import NULL
import datetime
import psycopg2
import psycopg2.extras
import matplotlib.pyplot as plt
import pandas as pd

hostname = 'localhost'
database = 'thingsboard'
username = 'postgres'
pwd = 'postgres'
port_id = 5432
conn = None



ides = {
    57 : "freon after compressor  "     ,
    59 : "freon after air cooler "      ,
    61 : "freon afther water cooler"    ,
    60 : "outside temp"                 ,
    58 : "compresor on_off"             ,
    62 : "vrata"                        ,
    16 : "chaimber"                     ,
}


try:
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            cur.execute('''SELECT * FROM bigtest
                        ORDER BY id desc limit 100''')
            
            for record in cur.fetchall():
                
                print('{} -|{}|-  {}  {}  {}  {}  {}  {}  {}'.format(record['id'], record['time'], record['chaimber'], record['freon_after_water_coler'], record['vrata'], record['compresor_on_off'], record['outside_temp'], record['freon_after_air_cooler'], record['freon_after_compressor']))
             # freon_after_water_coler, vrata, compresor_on_off, outside_temp, freon_after_air_cooler, freon_after_compressor, time
                                                            
             
                
                
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

        





#   Name:                    KEY:     

#freon after compressor         - 57
#freon after air cooler         - 59
#freon afther water cooler      - 61
#outside temp                   - 60
#compresor on\off               - 58 свършвва
#vrata                          - 62 свършвва
#chaimber                       - 16 Започва 
        
