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
            
                cur.execute('''SELECT * FROM ftest
                        ORDER BY id desc limit 100''')
            
                for record in cur.fetchall():
                    
                    print('{} -|{}|-  {}  {}  {}  {} '.format(record['device'],record['time'], record['temp2'], record['temp3'], record['temp4'], record['state1'] ))
                                                          
             
                
                
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

        
