
from asyncio.windows_events import NULL
from operator import index
import re
import string
from numpy import empty, rec
import datetime
import psycopg2
import psycopg2.extras
from psycopg2 import extras
from sqlalchemy import null
import time


hostname = 'localhost'
database = 'thingsboard'
username = 'postgres'
pwd = 'postgres'
port_id = 5432
conn = None

new_dict=dict()
start = time.time()

ides = {
    57 : "freon after compressor  "     ,
    59 : "freon after air cooler "      ,
    61 : "freon afther water cooler"    ,
    60 : "outside temp"                 ,
    58 : "compresor on_off"             ,
    62 : "vrata"                        ,
    16 : "chaimber"                     ,
}
def repp(a):
    
    return ides[a]
 
def epochToTime(idk):
        
    return datetime.datetime.fromtimestamp(int(str(idk)[:-3])).strftime('%Y-%m-%d %H:%M:%S')

def ifEmpty(st): 
    if str(st) == "None":
        return ''
    
    return st
    
def exist(key):
    if key in new_dict:
        return new_dict[key]
    #print("fakkkkkkkkkk#################")
    return None

try:
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            
            cur.execute('''SELECT * FROM public.ts_kv
                        WHERE key IN (16, 57, 58, 59, 60, 61, 62)
                        ORDER BY ts DESC LIMIT 2000000''') 
            count = 0
            mylist = list()
            insert_script = ''
            for record in cur.fetchall():
                
                if(record['key'] == 16 or count > 0 and count < 7):    
                                                                     
                    if count > 6 :                        
                        new_dict['time'] = epochToTime(record['ts'])
                        #print(new_dict)
                        mylist.append([ new_dict['chaimber'], exist('freon afther water cooler'), exist('vrata'), exist('compresor on_off'), exist('outside temp'), exist('freon after air cooler '), exist('freon after compressor  '),new_dict['time'] ])          
                        insert_script  = 'INSERT INTO bigtest ( chaimber, freon_after_water_coler, vrata, compresor_on_off, outside_temp, freon_after_air_cooler, freon_after_compressor, time ) VALUES  %s'
                        # insert_values = [( new_dict['chaimber'], exist('freon afther water cooler'), exist('vrata'), exist('compresor on_off'), exist('outside temp'), exist('freon after air cooler '), exist('freon after compressor  '),new_dict['time']),
                        #                  ( new_dict['chaimber'], exist('freon afther water cooler'), exist('vrata'), exist('compresor on_off'), exist('outside temp'), exist('freon after air cooler '), exist('freon after compressor  '),new_dict['time']),
                        #                  ( new_dict['chaimber'], exist('freon afther water cooler'), exist('vrata'), exist('compresor on_off'), exist('outside temp'), exist('freon after air cooler '), exist('freon after compressor  '),new_dict['time'])
                        # ]
                        #extras.execute_values(cur,insert_script,insert_values) 
                                            
                        #cur.execute(insert_script, insert_values)    #0.5mil 12
                        #cur.executemany(insert_script, insert_values) #0.5mil 12.5 
                        new_dict.clear()
                        
                        
                        
                        count = 0                     
                             
                    count+=1   
                   
                    if len(str(ifEmpty(record['long_v']))):
                        new_dict[repp(record['key'])] = record['long_v']
                    else:
                        new_dict[repp(record['key'])] =  record['dbl_v']
                if len(mylist)>35000:
                    extras.execute_values(cur,insert_script,mylist)  
                    mylist.clear()
                           
                       
            #print(mylist)
            extras.execute_values(cur,insert_script,mylist)  
                    
            print(time.time()-start)        
                    
                                                         
             
            
             
          
              
                
                
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
     
     
# cur.execute('DROP TABLE IF EXISTS bigtest')

#                         create_script = ''' CREATE TABLE IF NOT EXISTS bigtest (
#                                                 id                        int PRIMARY KEY,
#                                                 chaimber                  NUMERIC(3,2),
#                                                 freon_after_water_coler   NUMERIC(3,2),
#                                                 vrata                     NUMERIC(3,2),
#                                                 compresor_on_off          NUMERIC(3,2),
#                                                 outside_temp              NUMERIC(3,2),
#                                                 freon_after_air_cooler    NUMERIC(3,2),
#                                                 freon_after_compressor    NUMERIC(3,2),
#                                                 time TIMESTAMP) '''
#                         cur.execute(create_script)        