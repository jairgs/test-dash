import requests
import json
import pandas as pd


#consulta para hacer requests a la base de indicadores económicos
IdIndicador='493911' #493911
Idioma='es'
AreaGeo='0700'
Recientes='false' #true= ultimo valor; false= serie completa
FuenteDatos='BIE' #BISE or BIE 
Version='2.0'
Token='5a9fe7dc-cc4a-77eb-e5cf-f2153a7c41bc'
Formato='json'

def getdata(IdIndicador, Idioma='es', AreaGeo='0700', Recientes='false', FuenteDatos='BIE', Version='2.0', Token='5a9fe7dc-cc4a-77eb-e5cf-f2153a7c41bc', Formato='json'):
    url='https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/'+IdIndicador+'/'+Idioma+'/'+AreaGeo+'/'+Recientes+'/'+FuenteDatos+'/'+Version+'/'+Token+'?type='+Formato
    response= requests.get(url)
    if response.status_code==200:
        content= json.loads(response.content)
        #print(json.dumps(content, indent=2))
        series=content['Series']   
        obs=[]
        for i in series:
            obs.append(i['OBSERVATIONS'])
        #print(obs)
        values=[]
        for i in obs:
            foo=[]
            for j in i:
                foo.append(j['OBS_VALUE'])
            values.append(foo)
        
        #for i in values:
            #print(len(i))
            #print(i[-1])
        
        return pd.DataFrame(obs[0]) #only one element per request
        

    else: print('bad request:'+response)

'''
#consulta para denue
token='229b1e5e-0636-4a1d-b78c-58f51731820c'
url='https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarAreaActEstr/01/0/0/0/0/0/0/0/0/oxxo/1/15/0/1/'+token
response= requests.get(url)
if response.status_code==200:
    content= json.loads(response.content)
    for i in content:
        print(i['Nombre'])
'''
    
#print(getdata(IdIndicador))   

    
