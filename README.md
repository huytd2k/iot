## Requirements
- Python = ^3.8
- Poetry
## Installation
```bash
$ git clone https://github.com/huytd2k/iot.git
$ cd iot
$ poetry install
$ poetry shell
```
## Run the server
### If you have `make`
```bash
$ make run-dev
```
### Otherwise
```bash
$ python -m uvicorn server.main:app --reload
```