from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlite3 import IntegrityError


import uvicorn

from .database import insert_values, fetch_values, update_values
from .queries import *
from .models import *
from .constants import *
from .exception import *


app = FastAPI()

def error_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except (IntegrityError, NotFoundException, Exception):
            raise 
    return inner_function

@app.exception_handler(IntegrityError)
@app.exception_handler(NotFoundException)
async def my_exception_handler(request: Request, exc):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
        content={"message": str(exc)})

@app.exception_handler(Exception)
async def my_exception_handler(request: Request, exc):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        content={"message": str(exc)})
   
@error_handler
@app.post("/sport")
async def insert_sport(sport: Sports):
    """
    Inserts values to sports table
 
    Parameters
    ----------
    sport : Sports
        pydantic model Sports that contains all the information to be inserted
 
    Returns
    -------
    HTTPResponse
        Response saying the value is inserted
    """
    response = await insert_values(INSERT_SPORT, dict(sport))
    return f'Inserted successfully with id {response}'
   
@error_handler
@app.put("/sport")
async def update_sport(sport: UpdateSport):
    """
    Updates values to sports table
    Here we can provide the values that are updated and we can only
    give conditions on id and sport_name column
 
    Parameters
    ----------
    sport : UpdateSport
        pydantic model Update that contains all the information to be updated
 
    Returns
    -------
    HTTPResponse
        Response saying the value is updated
    """
    sport_old = None
    # If the sport name is updated we have the sport name reference in event table
    # So get the old name inorder to update that value
    if sport.condition.id and sport.update.sport_name:
        select_query = SELECT_CONDITION.format(table_name = Tables.SPORTS, condition = f"id= {sport.condition.id}")
        sport_old = await fetch_values(select_query)
        if not sport_old:
            raise NotFoundException("Sport Not Found")
    condition = f'sport_name like "{sport.condition.sport_name}"' if sport.condition.sport_name else f"id = {sport.condition.id}"
    response = await update_values(sport, condition, Tables.SPORTS)
    if not response:
        raise NotFoundException("Sport Not Found")
    if sport_old:
        await insert_values(UPDATE_SPORT_NAME.format(sport_name= sport.update.sport_name, sport_name_old= sport_old[0]['sport_name']))
    return f"Sport successfully updated"

@error_handler  
@app.post("/event")
async def insert_event(event: Event):
    """
    Inserts values to events table
 
    Parameters
    ----------
    sport : Events
        pydantic model Events that contains all the information to be inserted
 
    Returns
    -------
    HTTPResponse
        Response saying the value is inserted
    """
    response = await insert_values(INSERT_EVENT, dict(event))
    return f'Inserted successfully with id {response}'

@error_handler
@app.put("/event")
async def update_event(event: EventUpdate):
    """
    Updates values to event table
    Here we can provide the values that are updated and we can only
    give conditions on id, event_name and sport_name column
 
    Parameters
    ----------
    sport : EventUpdate
        pydantic model Update that contains all the information to be updated
 
    Returns
    -------
    HTTPResponse
        Response saying the value is updated
    """
    event_old = None
    if event.condition.id and event.update.event_name:
        select_query = SELECT_CONDITION.format(table_name = Tables.EVENTS, condition = f"id= {event.condition.id}")
        event_old = await fetch_values(select_query)
        if not event_old:
            raise NotFoundException('Event not found')

    if event.condition.event_name:
        condition = f'event_name like "{event.condition.event_name}" ' 
    elif event.condition.sport_name:
        condition = f'sport_name like "{event.condition.sport_name}" ' 
    else: 
        condition = f"id = {event.condition.id}"
    id = await update_values(event, condition, Tables.EVENTS)
    if not id:
        raise NotFoundException("Event not found")
    
    select_query = SELECT_CONDITION.format(table_name = Tables.EVENTS, condition = f"id= {id}")
    updated_value = await fetch_values(select_query)
    # when all the events of a sport are inactive we need to make that sport inactive
    await insert_values(UPDATE_SPORT_EVENT.format(sport_name=updated_value[0]['sport_name']))
    if event_old:
        await insert_values(UPDATE_EVENT_NAME.format(event_name = event.update.event_name, event_name_old = event_old[0]['event_name']))
    return f"Event successfully updated"

@error_handler 
@app.post("/selection")
async def insert_selection(selection: Selection):
    """
    Inserts values to selection table
 
    Parameters
    ----------
    sport : Selection
        pydantic model Selection that contains all the information to be inserted
 
    Returns
    -------
    HTTPResponse
        Response saying the value is inserted
    """
    response = await insert_values(INSERT_SELECTION, dict(selection))
    return f'Inserted successfully with id {response}'

@error_handler
@app.put("/selection")
async def update_selection(selection: SelectionUpdate):
    """
    Updates values to Selnectio table
    Here we can provide the values that are updated and we can only
    give conditions on id, selection_name and event_name column
 
    Parameters
    ----------
    sport : UpdateSport
        pydantic model Update that contains all the information to be updated
 
    Returns
    -------
    HTTPResponse
        Response saying the value is updated
    """
    if selection.condition.selection_name:
        condition = f'selection_name like "{selection.condition.selection_name}" ' 
    elif selection.condition.event_name:
        condition = f'event_name like "{selection.condition.event_name}" ' 
    else: 
        condition = f"id = {selection.condition.id}"
        
    id = await update_values(selection, condition, Tables.SELECTIONS)
    if not id:
        raise NotFoundException("Event not found")
    select_query = SELECT_CONDITION.format(table_name = Tables.SELECTIONS, condition = f"id= {id}")
    updated_value = await fetch_values(select_query)
    # whenever all the selections are inactive update that event to be inactive
    response = await insert_values(UPDATE_EVENT_SELECTION.format(event_name=updated_value[0]['event_name']))
    return f"Selection successfully updated"

@error_handler
@app.post("/search")
async def search(search: Search):
    """
    Provides a search feature for all the tables
    Here we can provide 
    table_name -> where we want to filter on
    conditions -> Filter conditions on that table
        conditions is a dict with key, operator and value
    conditions_date -> Separated the datetime to make the validations simpler
        conditions_date is a dict with key, operator and value
    select -> provides a feature to filter on the child table and select from parent table
        table_name -> name of the same table or parent table
        join_key -> applicable only if we are selecting from parent table
        keys -> if we want to select only particular columns
 
    Parameters
    ----------
    search : Search
        pydantic model Search that contains all the information on filters
 
    Returns
    -------
    HTTPResponse
        All the values that are filtered
    """
    query = build_search_query(search)
    return await fetch_values(query) 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)