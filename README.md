# mastermind
api and database for mastermind





## Getting Started
Clone the repository from github



### Starting docker container
Start Docker Desktop
On Windows open a Windows PowerShell as administrator (Run as administrator)
change directory to the root of the cloned github repository, e.g.,
```
cd C:\Users\<username>\Documents\Workspace\mastermind
```
Start the docker containers (the first time this will also build the images)
```
docker-compose up
```
The server is now accessible at: localhost:8000



### Running test cases
On Windows open a new Windows PowerShell as administrator (Run as administrator)
change directory to the root of the cloned github repository, e.g.,
```
cd C:\Users\<username>\Documents\Workspace\mastermind
```
Enter the server:
```
docker exec -it mastermind-server /bin/bash
```
Command to run test cases:
```
python3 manage.py test
```
To exit the server:
```
ctrl+z
```



### Stopping docker container
In the original Windows PowerShell where you ran docker-compose up, run the following commands:
```
ctrl+c
```
```
docker-compose down
```





## REST API Services



### <mark>Postman collection</mark>
A <mark>**_postman collection_**</mark> with the following requests is included at <mark>**_/server/mastermind_rest_api.postman_collection.json_**</mark>.



### user registration
```
POST
localhost:8000/users/register/
Headers:
	Content-type: application/json
Post body example:
{
	"username": "testuser1",
	"email": "testuser1@test.com",
	"password": "password1234"
}
Example json response:
{
    "id": 1,
    "username": "testuser1",
    "email": "testuser1@test.com",
    "token": "8a2bcdeeb04567f5ef608d8d72f0182dca457d82"
}
```



### user login
```
POST
localhost:8000/users/login/
Headers:
	Content-type: application/json
Post body example:
{
	"username": "testuser1",
	"password": "password1234"
}
Example json response:
{
    "username": "testuser1",
    "token": "8a2bcdeeb04567f5ef608d8d72f0182dca457d82"
}
```



### create new game
```
POST
localhost:8000/api/games/
Headers:
	Content-type: application/json
	Authorization: Token 8a2bcdeeb04567f5ef608d8d72f0182dca457d82
Example json response:
{
    "id": 1,
    "number_of_moves": 12,
    "codebreaker": 1,
    "color_choices": [
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "purple"
    ]
}
```



### create new move
```
POST
localhost:8000/api/moves/
Headers:
	Content-type: application/json
	Authorization: Token 8a2bcdeeb04567f5ef608d8d72f0182dca457d82
Post body example:
{
    "game": 1,
    "code": [
        "purple",
        "purple",
        "orange",
        "green"
    ]
}
Example json response:
{
    "id": 1,
    "game": 1,
    "code": [
        "purple",
        "purple",
        "orange",
        "green"
    ],
    "result": [
        "black",
        "black",
        "white"
    ]
}
```



### get game and move history
```
GET
localhost:8000/api/games/1/
Headers:
	Authorization: Token 8a2bcdeeb04567f5ef608d8d72f0182dca457d82
Example json response:
{
    "id": 1,
    "number_of_moves": 12,
    "codebreaker": 1,
    "moves": [
        {
            "id": 1,
            "game": 1,
            "code": [
                "purple",
                "purple",
                "orange",
                "green"
            ],
            "result": [
                "black",
                "black",
                "white"
            ]
        }
    ],
    "color_choices": [
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "purple"
    ]
}
```
