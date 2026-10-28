All endpoints except `/register` and `/login/` require header: 'Authorization: Bearer TOKEN'

# Users
## GET
- `/users/{id}` returns data of user with specified id  
    #### Response:
    ```JSON
        {
          "id": "int",
          "username": "string"
        }
    ```
    User not found - 404
  

- `/users/me/` returns data of current user  
    #### Response:
    ```JSON
        {
          "id": "int",
          "username": "string"
        }
    ```
  
## POST
- `/register`
    User registration
    #### Request:
    ```JSON
    {
      "username": "string",
      "password": "string"
    }
    ```
    
    #### Response:
    Success - 201  
    Fail - 400


- `/login/`
    Login endpoint. Returns JWT token for later authentication and authorization\
    #### Request:
    **header:** 'Content-Type: application/json'
    ```JSON
    {
      "username": "string",
      "password": "string"
    }
    ```
    #### Response:
    ```JSON
    {
      "access": "token",
      "refresh": "token"
    }
    ```
    Wrong username or password - 401
## DELETE
- `/users/{id}` deletes user with specified id  
  #### Response:
    Success - 200  
    Fail - 400  
    User not found - 404 

# GAMES
## GET
- `/games/{id}`

#### Response
```JSON
{
  "id": "int",
  "name": "string",
  "description": "string",
  "max_team_size": "int",
  "admin": {
    "id": "int",
    "username": "string"
  },
  "checkpoints": [{
    "id": "int",
    "name": "string",
    "description": "string",
    "previous": "int | null"
  },],
  "achievements": [{
    "id": "int",
    "description": "string",
    "bonus": "int",
    "treshold": "int | null",
    "checkpoint_id": "int | null"
  },]
}
```
Game not found - 404

- `/games/users/{user_id}/admin`
#### Response
```JSON
[
  {
    "id": "int",
    "name": "string",
    "description": "string",
    "max_team_size": "int"
  },
]
```

- `/games/users/{user_id}/player`
#### Response
```JSON
[
  {
    "id": "int",
    "name": "string",
    "description": "string",
    "max_team_size": "int"
  },
]
```
- `/games/{game_id}/teams/user/{user_id}`
#### Response
```JSON
{
  "id": "int",
  "name": "string",
  "description": "string",
  "max_team_size": "int",
  "admin": {
    "id": "int",
    "username": "string"
  },
  "checkpoints_unlocked": [{
    "id": "int",
    "name": "string",
    "description": "string",
    "previous": "int | null"
  },],
  "checkpoints_locked": [{
    "id": "int",
    "name": "string",
    "description": "string",
    "previous": "int | null"
  },],
  "achievements": [{
    "id": "int",
    "description": "string",
    "bonus": "int",
    "treshold": "int | null",
    "checkpoint_id": "int | null"
  },]
}
```
Game not found - 404

## POST
- `/games` creates new game with specified parameters

  `previous` is index of checkpoint in `checkpoints` list that has to be unlocked first, -1 if none\
  achievement has `treshold` (points needed) or `checkpoint_id` (index of checkpoint in `checkpoints` list)
  #### Request
  ```JSON
  {
    "game": {
      "name": "string",
      "description": "string",
      "game_admin_id": "int",
      "max_team_size": "int"
    },
    "checkpoints": [{
      "name": "string",
      "description": "string",
      "previous": "int"
    },],
    "achievements": [{
      "description": "string",
      "bonus": "int",
      "treshold": "int",
      "checkpoint_id": "int"
    },]
  }
  ```
  #### Response
  Success - 201
```JSON
  {"id": "int"}
```

## PUT
- `/games` updates game with specified name

  #### Request
  ```JSON
  {
    "name": "string",
    "description": "string",
    "game_admin_id": "int",
    "max_team_size": "int"
  }
  ```
  #### Response
  Success - 201

# COMMENTS
## GET
- `/checkpoint/{checkpoint_id}/comments`

```json
[
  {
    "comment": "str",
    "time": "timestamp",
    "author": "str"
  }
]
```

## POST
- `/checkpoint/{checkpoint_id}/comments`
```json
{
  "comment": "str",
  "user_id": "int"
}
```
#### Response
Success - 201

# CHECKPOINTS
## GET
- `/checkpoints/{checkpoint_id}/player`
#### Response
```json
{
  "id": "int",
  "name": "string",
  "description": "string",
  "previous": "int | null"
}
```
- `/checkpoints/{checkpoint_id}/admin`
#### Response
```json
{
  "id": "int",
  "name": "string",
  "description": "string",
  "previous": "int | null",
  "qr_code_path": "str"
}
```
## PUT
- `/checkpoint/{checkpoint_id}/team/{team_id}/unlock` unlocks checkpoint for team, adds 1 point and bonuses of reached achievements
#### Response
Success - 201  
Checkpoint already unlocked or previous checkpoint not unlocked - 400

# TEAM
## GET
- `/teams/{game_id}`
#### Response
```json
[{
  "id": "int",
  "game_id": "int",
  "name": "str",
  "points": "int",
  "game_times": ["timestamp",]
}]
```
- `/teams/team/{team_id}`
#### Response
```json
{
  "id": "int",
  "game_id": "int",
  "name": "str",
  "points": "int",
  "game_times": ["timestamp",],
  "members": ["str",]
}
```
Team not found - 404
- `/teams/{game_id}/{user_id}` returns team of user in game
#### Response
```json
{
  "id": "int",
  "game_id": "int",
  "name": "str",
  "points": "int",
  "game_times": ["timestamp",]
}
```
Team not found - 404

## POST
- `/teams/{game_id}`
#### Request
```json
{
  "name": "str",
  "players": ["str",]
}
```
#### Response
Success - 201
