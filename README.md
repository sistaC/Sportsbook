# SportsBook
> Sportsbook product which is responsible for managing sports, events and selections.
> This is a restapi which will help you to insert, update, search in sportsbook database

## Database description  
A sport contains the following elements:
* sport_name
* slug (url friendly version of name)
* active (either true or false)

An event contains the following elements:
* event_name
* slug (url friendly version of name)
* active (Either true or false)
* type (Either preplay or inplay)
* sport_name
* status (pending, started, ended or cancelled)
* scheduled_start (UTC datetime)
* actual_start (created at the time the event has the status changed to "Started")

A selection contains the following elements:
* selection_name
* event_name
* price (Decimal value, to 2 decimal places)
* active (Either true or false)
* outcome (Unsettled, Void, Lose or Win)

## Requirements  (Prerequisites)
* Docker [Install](https://docs.docker.com/desktop/install/windows-install/)

## Installation
A step by step list of commands / guide that informs how to install an instance of this project. 
`$ clone the project`

`$ cd to the directory`

`$ docker build -it sportsbook:1.0 .`

`$ docker run -e DB_PATH='/app/data/sportbook.db' -v data:/app/data -it -d --publish 8000:8000 sportsbook:1.0 `


## Features
You can perform insert, update, search on sports, events, selections.

#### POST /sport

You can insert data into sport table using this request and body as below

```json
{
  "sport_name": "string",  
  "slug": "string", 
  "active": "bool"
}
```

#### POST /event

You can insert data into events table using this request and body as below

```json
{
  "event_name": "string",
  "slug": "string",
  "active": "bool",
  "type": "string",
  "sport_name": "string",
  "status": "string",
  "scheduled_start": "2023-08-31T07:44:13.260Z #datetime format" , 
  "actual_start": "2023-08-31T07:44:13.260Z #datetime format" 
}
```

#### POST /selection

You can insert data into selections table using this request and body as below

```json
{
  "selection_name": "string",
  "event_name": "string",
  "price": "float",
  "active": "bool",
  "outcome": "string"
}
```

#### PUT /sport

You can update the data inserted into sports table using the below JSON.
you need to provide either id or name as base condition to avoid unecessary updates 
to the whole table.

You can update the name only by providing id in the condition.

```json
{
  "update": {
    "slug": "string",
    "active": "bool",
    "sport_name": "string"
  },
  "condition": {
    "sport_name": "string",
    "id": 0
  }
}
```

#### PUT /event

You can update the data inserted into events table using the below JSON.
you need to provide either id or sport_name or event_name as base condition to avoid unecessary updates 
to the whole table.

You can update the event_name only by providing id in the condition.

```json
{
  "update": {
    "event_name": "string",
    "slug": "string",
    "active": true,
    "type": "string",
    "sport_name": "string",
    "status": "string",
    "scheduled_start": "string",
    "actual_start": "string"
  },
  "condition": {
    "event_name": "string",
    "sport_name": "string",
    "id": 0
  }
}
```

#### PUT /selection

You can update the data inserted into selections table using the below JSON.
you need to provide either id or selection_name or event_name as base condition to avoid unecessary updates 
to the whole table.

You can update the event_name only by providing id in the condition.

```json
{
  "update": {
    "selection_name": "string",
    "event_name": "string",
    "price": 0,
    "active": true,
    "outcome": "string"
  },
  "conditions": {
    "selection_name": "string",
    "event_name": "string",
    "id": 0
  }
}
```
#### POST /search


```json
{
  "table_name" : "name of the table you want to filter",
  "conditions": [{
    "key": "name of the column",
    "operator": "=, >=, <=, >, <, like, between",
    "value": "value in accordance with the operator",  
  }],
  "conditions_date": [{
    "key": "name of the column",
    "operator": "=, >=, <=, >, <, like, between",
    "value": "value in accordance with the operator",  
  }],
  "select": {
    "table_name": "name of the table to select from either parent table or same table",
    "keys": "column names to select from",
    "join_key": "column name that joins two tables"
  }
}
```

###### Example to get all sports
```json
{
  "table_name" : "sports",
}
```

###### Example to get all sports with name filter
```json
{
  "table_name" : "sports",
  "conditions": [{
    "key": "sport_name",
    "operator": "like",
    "value": "valid regex",  
  }]
}
```

###### Example to get all sports with inactive events
```json
{
  "table_name" : "events",
  "conditions": [{
    "key": "active",
    "operator": "=",
    "value": false,  
  }],
  "select": {
    "table_name": "sports",
    "join_key": "sport_name"
  }
}
```

## Running the tests
You need to install pytest to execute the tests and execute the tests using below command.

`$ pytest`

## Authors
Chidrupi Sista  – chidrupi.sista@gmail.com
 
 You can find me here at:
[LinkedIn](https://www.linkedin.com/in/chidrupi-sista-34a121168/)

