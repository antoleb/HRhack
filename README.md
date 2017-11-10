### How to run

Run example:
```
# Save data in "./data/krok.xlsx"

docker build -t server .
docker run -it -p 8000:8000 server
```

To set your secret key for `socket.io` provide enviroment variable with docker run (by flag `--env 'SECRET_KEY='your_key'`).

### Socket.io API

___
**name:** `find_canditates`\
**args:** `department`, `position`\
**returns:**
```json
[
    {
      "id": 123,
      "department": "department_name",
      "position": "position_name",
      "finished_courses": ["name_1", ...],
      "suggested_courses": ["name_1", ...],
      "careers": [
        {
            "id": "45338"
            "department": "name",
            "position": "name",
            "start_timestamp": 1214870400.0,
            "end_timestamp": 1204588800.0
        },
        ...
      ]
    },
    ...
]
```
___
