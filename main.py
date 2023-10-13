from fastapi import FastAPI, Body, Path, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from schemas.movie import Movie



app = FastAPI()
app.title = 'MY FASTAPI APLICATION'
app.version = "0.0.1"


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar 2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2023',
        'rating': 7.8,
        'category': 'Acción'    
    }
]

    
@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1> hello </h1>')

@app.get('/movies', tags=['movies'], response_model=list[Movie])
def get_movies() -> list[Movie]:

    return JSONResponse(content=movies, status_code=status.HTTP_200_OK)

@app.get('/movies{id}', tags=['movies'])
def get_movie(id: int = Path(ge = 1, le= 2000)):
        movie = [movie for movie in movies if movie['id'] == id]
        return JSONResponse(content=movie[0], status_code=200)  if movie else JSONResponse(content={'message': 'Movie not found'}, status_code=status.HTTP_204_NO_CONTENT) 
    

@app.get('/movies/', tags=['movies'], response_model=list[Movie])
def get_movies(category: str = Query(min_length=5 , max_length=20) ) -> list[Movie]:    
    movies_by_category  = [movie for movie in movies if movie['category'] == category]
    return JSONResponse(content=movies_by_category, status_code=status.HTTP_200_OK) if movies_by_category else JSONResponse(content={'message': 'Movie not found'}, status_code=status.HTTP_204_NO_CONTENT)

@app.post('/movies', tags=['movies'], response_model=Movie)
def create_movie(movie : Movie) -> Movie:
    movies.append(movie)
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=status.HTTP_201_CREATED)


@app.put('/movies/{id}', tags=['movies'])
def update_movie(id : int, movie :Movie):    
    find_movie = [find_movie for find_movie in movies if find_movie['id'] == id]
    update = {        
        'title': movie.title,
        'overview': movie.overview,        
        'year': movie.year,
        'rating': movie.rating,
        'category': movie.category
        }
    find_movie[0].update(update)    
    return find_movie[0]


@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id : int) -> dict:
    movie = [movie for movie in movies if movie['id'] == id]
    if movie == []:
        return {'message': 'Movie not found'}
    movies.remove(movie[0])
    return {'message': 'Movie deleted successfully'}