import psycopg2
import psycopg2.extras

hostname = 'localhost'
database = 'iotBrick'
username = 'postgres'
pwd = 'postgres'
#pwd = '123'
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

            cur.execute('DROP TABLE IF EXISTS alarmsValue')

            create_script = ''' CREATE TABLE IF NOT EXISTS alarmsValue (
                                    id      int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                    device  TEXT,
                                    temp1   NUMERIC(5,2),
                                    temp2   NUMERIC(5,2),
                                    temp3   NUMERIC(5,2),
                                    temp4   NUMERIC(5,2)) '''
            cur.execute(create_script)    
                   
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

'''
CREATE TABLE IF NOT EXISTS alarmsValue
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    device text COLLATE pg_catalog."default",
    temp1 numeric(5,2),
    temp2 numeric(5,2),
    temp3 numeric(5,2),
    temp4 numeric(5,2),
    state1 boolean,
    "time" timestamp without time zone,
    CONSTRAINT alarmsValue_pkey PRIMARY KEY (id)
)
'''