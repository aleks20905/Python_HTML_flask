import psycopg2
import psycopg2.extras

hostname = 'localhost'
database = 'thingsboard'
username = 'postgres'
pwd = 'postgres'
port_id = 5432
conn = None
 
try:
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            cur.execute('DROP TABLE IF EXISTS bigtest')

            create_script = ''' CREATE TABLE IF NOT EXISTS bigtest (
                                                id                        int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                                chaimber                  NUMERIC(5,2),
                                                freon_after_water_coler   NUMERIC(5,2),
                                                vrata                     NUMERIC(5,2),
                                                compresor_on_off          NUMERIC(5,2),
                                                outside_temp              NUMERIC(5,2),
                                                freon_after_air_cooler    NUMERIC(5,2),
                                                freon_after_compressor    NUMERIC(5,2),
                                                time TIMESTAMP) '''
            cur.execute(create_script)    

           

            delete_script = 'DELETE FROM bigtest WHERE chaimber = %s'
            delete_record = ('1',)
            cur.execute(delete_script, delete_record)
            
            cur.execute('''SELECT * FROM bigtest
                        ORDER BY id ASC''')
            # count = 0
            # for record in cur.fetchall():
            #     print(' {:25} -| {} |- {}{}'.format(record['key'],record['ts'], record['long_v'],  record['dbl_v'])) 
                  
                                         
               
               
              
                
                
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

   