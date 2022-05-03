from typing import Dict, List, Union
import pandas as pd
import json
import pickle
from Movie import Movie, MovieHandler
from os.path import exists

metadataFile = "dataset/movies_metadata.csv"
creditsFile = "dataset/credits.csv"

def printJson(jsonDict:Union[Dict,List[Dict]]):
  print(json.dumps(jsonDict, indent=4))

def toJson(jsonStr:str):
  if not isinstance(jsonStr,str):
    return jsonStr
  jsonStr = jsonStr.replace("'",'"').replace('O"',"O'").replace('None','null')
  return json.loads(jsonStr)

if exists("dataframe.pkl"):
  with open("dataframe.pkl",'rb') as file:
    df = pickle.load(file)
else:
  metadata = pd.read_csv(metadataFile)[['belongs_to_collection','title', 'id']]
  metadata['belongs_to_collection'].fillna('{}', inplace=True)
  metadata = metadata.drop([19730, 29503, 35587])
  metadata['belongs_to_collection'] = metadata['belongs_to_collection'].apply(eval)
  metadata['id']=pd.to_numeric(metadata['id'])

  creditsDF = pd.read_csv(creditsFile)
  creditsDF['crew'] = creditsDF['crew'].fillna('[]').apply(eval)
  creditsDF['cast'] = creditsDF['cast'].fillna('[]').apply(eval)
  df = pd.merge(metadata,creditsDF,on='id')
  with open("dataframe.pkl","wb") as file:
    pickle.dump(df,file)

df = df.sample(frac=1, random_state=1)
handler = MovieHandler()
for i in df.index:
  try:
    cast = [j['id'] for j in df['cast'][i]]
    crew = [j['id'] for j in df['crew'][i]]
    movie = Movie(df['id'][i], df['title'][i], df['belongs_to_collection'][i].get('id',None),cast,crew)
  except:
    print(df.iloc[i])
    raise
  handler.addMovie(movie)

handler.computeAdjacency()
print(handler.movies)