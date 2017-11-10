### How to run

To set your secret key for `socket.io` provide enviroment variable with docker run (by flag `--env 'SECRET_KEY='your_key'`).

### Socket.io API

___
**name:** `find_canditates`\
**args:** `department`, `position`\
**returns:**
```json
[
    {
      id: 123,
      department: 'department',
      positii
    },
    ...
]
```
___
