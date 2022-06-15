from typing import Optional
from fastapi import  FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{
    "title" : "This is the title 1",
    "content" : "This is content 1",
    "id" : 1
},
{
    "title" : "This is the title 2",
    "content" : "This is content 2",
    "id" : 2
}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i,p in enumerate(my_posts):
        return i


@app.get('/')
def root():
    return {'message':'hello world'}

@app.get('/posts')
def get_posts():
    return {'data':my_posts}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
#def create_post(payLoad: dict = Body(...)):
def create_post(post:Post):
    # print(post.rating)
    # print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {'data':my_posts}

@app.get('/posts/{id}')
def get_post(id : int,response: Response):
    # print(type(id))  
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post with id {} doesnt exist'.format(id))
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'mesage':'post with id {} not found'.format(id)}
    return {'post_details':post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post with id {} doesnt exist'.format(id))
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id:int, post:Post):
    print(post)
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post with id {} doesnt exist'.format(id))
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'message':'update post','data':post_dict}