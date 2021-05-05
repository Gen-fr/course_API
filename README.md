# The API provids basic functionality using Python, Flask and SQLite.

Routes
$ flask routes --sort rule

```
Endpoint       Methods    Rule
-------------  ---------  -----------------------
get_courses    GET        /courses
get_course     GET        /courses/<int:id>
create_course  POST       /courses
edit_course    PUT        /courses/<id>
delete_course  DELETE     /courses/<id>
search         GET, POST  /search

index          GET, POST  /
edit_course_h  GET, POST  /edit/<int:id>
static         GET        /static/<path:filename>
```


Courses

# GET /courses: List of all courses

$ curl --location --request GET 'http://127.0.0.1:5000/courses' \
--data-raw ''

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 1250
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Wed, 05 May 2021 17:52:58 GMT

```
{
  "courses": [
    {
      "end_date": "2021-05-02", 
      "hourse": 42, 
      "id": 1, 
      "name": "Pascal", 
      "start_date": "2021-05-02"
    }, 
    {
      "end_date": "2024-05-02", 
      "hourse": 34, 
      "id": 2, 
      "name": "C#", 
      "start_date": "2024-05-02"
    }
  ]
}
```

# GET /courses/<int:id>: Query single cousre

$ curl --location --request GET 'http://127.0.0.1:5000/courses/02' \
--header 'Content-Type: application/json' \
--data-raw ''

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 142
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Wed, 05 May 2021 17:52:02 GMT

```
{
  "course": {
    "end_date": "2021-05-02", 
    "hours": 42, 
    "id": 1, 
    "name": "Pascal 98", 
    "start_date": "2021-05-02"
  }
}
```

# POST /course: Create new course

$ curl --location --request POST 'http://127.0.0.1:5000/courses' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "C++",
    "end_date": "2021-05-02",
    "hours": 22,
    "id": 12,
    "start_date": "2021-05-02"
}'

POST /courses HTTP/1.1" 200 -

```
{
    "message": "New course added"
}
```

# PUT /courses/<id>: Update course data

Can change data but not primary id.

$ curl --location --request PUT 'http://127.0.0.1:5000/courses/09' \
--header 'Content-Type: application/json' \
--data-raw '{
        "hours": 34,
        "name":".Net",
        "start_date": "2021-05-02",
        "end_date": "2021-05-02",
}'

PUT /courses/05 HTTP/1.1" 200 -

```
Edited
```

# DELETE /courses/<id>: Delete course

$ curl --location --request DELETE 'http://127.0.0.1:5000/courses/04' \
--data-raw ''

DELETE /courses/09 HTTP/1.1" 200

```
{
  "message": "The course has been deleted!"
}
```

# GET, POST  /search?q=pascal

Search by name and sort by the start date of the course. 


$ curl --location --request GET 'http://127.0.0.1:5000/search?q=Pascal'

GET /search?q=Pascal HTTP/1.1" 200


```
{
    "courses": [
        {
            "end_date": "2021-03-10 00:00:00",
            "hourse": 75,
            "id": 7,
            "name": "Pascal ",
            "start_date": "2021-02-01 00:00:00"
        },
        {
            "end_date": "2021-05-19 00:00:00",
            "hourse": 25,
            "id": 5,
            "name": "Pascal 66",
            "start_date": "2021-04-12 00:00:00"
        }
    ]
}
```