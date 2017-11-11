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
**request_name:** `find_candidates`\
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
**request_name:** `get_all_positions`\
**args:** -\
**returns:**
```json
{
    "department_name": [
        "position_1",
        "position_2",
        ...
    ],
    ...
}
```
___
**request_name:** `get_position_and_time`\
**args:** `id`
**returns:**
```json
{
    "department": "name",
    "position": "name",
    "work_time": 12,
}
```
___
**request_name:** `get_suggested_positions`\
**args:** `id`
**returns:**
```json
[
    {
        "position": "name",
        "department": "name",
        "promotion_number": 2,
        "mean_time": 123,
        "promoted_ids": [1, 2, 3]
    }
    ...
]
```
___
