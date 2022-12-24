import psycopg2
import psycopg2.extras

hostname = 'localhost'
database = 'iotBrick'
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

            cur.execute('DROP TABLE IF EXISTS ftest')

            create_script = ''' CREATE TABLE IF NOT EXISTS ftest (
                                                id                        int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                                device           TEXT,
                                                temp1            NUMERIC(5,2),
                                                temp2            NUMERIC(5,2),
                                                temp3            NUMERIC(5,2),
                                                temp4            NUMERIC(5,2),
                                                state1           BOOLEAN,
                                                time             TIMESTAMP) '''
            cur.execute(create_script)    

        
            
            cur.execute('''SELECT * FROM ftest
                        ORDER BY id ASC''')
          
                  
                                         
                          
              
                
                
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

   