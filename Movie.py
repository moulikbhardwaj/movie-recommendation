from sys import stdout
from typing import Dict, List, Set, Union


class Movie:
  def __init__(self, id, name, collectionId, cast, crew) -> None:
      self.id:int = id
      self.name:str = name
      self.cid:int = collectionId
      self.cast:List[int] = cast
      self.crew:List[int] = crew
      
      self.adjList:Dict[id,int] = {}

  def __repr__(self) -> str:
      return f"<{self.name}:{len(self.adjList)}>"

class InvalidParameterException(Exception):
  ...

class MovieHandler:
  def __init__(self) -> None:
      self.movies:Dict[int,Movie] = {}
      self.nameReverse:Dict[str,Movie]  = {}
      self.collections:Dict[int,List[Movie]] = {}
      self.castMovies:Dict[int,List[Movie]] = {}
      self.crewMovies:Dict[int,List[Movie]] = {}

      self.collections[None] = []
      self.castMovies[None] = []
      self.crewMovies[None] = []
  
  def addMovie(self, movie:Movie):
    self.movies[movie.id] = movie
    self.nameReverse[movie.name] = movie
    for castId in movie.cast:
      if castId not in self.castMovies:
        self.castMovies[castId] = []
      self.castMovies[castId].append(movie)

    for crewId in movie.crew:
      if crewId not in self.crewMovies:
        self.crewMovies[crewId] = []
      self.crewMovies[crewId].append(movie)

    if movie.cid is None:
      pass
    elif movie.cid not in self.collections:
      self.collections[movie.cid] = [movie]
    else:
      self.collections[movie.cid].append(movie)
  
  def get(self, query: Union[int, str]):
    if isinstance(query,int):
      return self.movies[query]
    elif isinstance(query,str):
      return self.nameReverse[query]
    raise InvalidParameterException(f"Invalid type {type(query)}")

  def computeAdjacency(self):
    cnt = 0
    for id in self.movies:
      cnt+=1
      print(f"{cnt}/{len(self.movies)}", end='\r')
      stdout.flush()
      cid = self.movies[id].cid
      movies = [i.id for i in self.collections[cid] if i != self.movies[id]]
      for castId in self.movies[id].cast:
        movies.extend([i.id for i in self.castMovies[castId]])
      for crewId in self.movies[id].crew:
        movies.extend([i.id for i in self.crewMovies[crewId]])
      for i in movies:  
        if i not in self.movies[id].adjList:
          self.movies[id].adjList[i] = 0
        self.movies[id].adjList[i]+=1