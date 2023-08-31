"""
This python file is used to define all the pydantic models used in this project
"""

from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, List, Any, Union
from datetime import datetime, timezone
import re
import pytz

from .constants import VALID_EVENT_TYPE, VALID_EVENT_STATUS, VALID_SELECTION_OUTCOME, VALID_CONDITIONS

class Sports(BaseModel):
    """
    Pydantic model for inserting values in sports table
    """
    sport_name: str 
    slug: str
    active: bool
     
    @field_validator("sport_name")
    def validate_name(cls, value):
        if re.search("[^a-zA-Z0-9s]", value):
            raise ValueError("Sports name cannot contain special characters")
        return value

class UpdateSportValues(BaseModel):
    """
    Pydantic model to update sports table values
    TODO: Use the Sports base table
    """
    slug: Optional[str] = None
    active: Optional[bool] = None
    sport_name: Optional[str] = None

class UpdateSportConditions(BaseModel):
    """
    Pydantic model to update sports table on given condition
    """
    sport_name: Optional[str] = None
    id: Optional[int] = None

    @model_validator(mode='before')
    def validate_conditions(cls, values):
        if not values.get("id") and (not values.get("sport_name")):
            raise ValueError("Either id or name should be provided")
        return values

class UpdateSport(BaseModel):
     """
     Pydantic model to update sports table
     """
     update: UpdateSportValues
     condition: UpdateSportConditions

     @model_validator(mode='before')
     def validate_update(cls, values):
        if values.get("condition").get("sport_name") and values.get("update").get("sport_name"):
            raise ValueError("Name cannot be updated when condition is name")
        return values

class Event(BaseModel):
    """
    Pydantic model for inserting values in event table
    """
    event_name: str 
    slug: str
    active: bool
    type: str
    sport_name: str
    status: str
    scheduled_start: datetime
    actual_start: Optional[datetime] = None

    @field_validator("event_name")
    def validate_name(cls, value):
        if re.search("[^a-zA-Z0-9s]", value):
            raise ValueError("Events name cannot contain special characters")
        return value
    
    @field_validator("type")
    def validate_type(cls, value):
        if value not in VALID_EVENT_TYPE:
            raise ValueError(f"Event type should be one among {VALID_EVENT_TYPE}")
        return value
    
    @field_validator("status")
    def validate_status(cls, value):
        if value not in VALID_EVENT_STATUS:
            raise ValueError(f"Event status should be one among {VALID_EVENT_STATUS}")
        return value
    
    @field_validator("scheduled_start")
    def validate_scheduled_start(cls, value):
        return value.astimezone(pytz.utc)
    
    @field_validator("actual_start")
    def validate_actual_start(cls, value):
        return value.astimezone(pytz.utc)
    
    @model_validator(mode='before')
    def validate_event(cls, values):
        if values.get("status") != "started" and values.get("actual_start"):
            raise ValueError("Actual start should be updated only if event is changed to started")
        return values

class EventUpdateValues(BaseModel):
    """
    Pydantic model to update events table values
    TODO: Use the Events base model
    """
    event_name: Optional[str] = None 
    slug: Optional[str] = None
    active: Optional[bool] = None
    type: Optional[str] = None
    sport_name: Optional[str] = None
    status: Optional[str] = None
    scheduled_start: Optional[str] = None
    actual_start: Optional[str] = None

    @model_validator(mode='before')
    def validate_event(cls, values):
        if values.get("status") != "started" and values.get("actual_start"):
            raise ValueError("Actual start should be updated only if event is changed to started")
        return values

class EventUpdateCondition(BaseModel):
    """
    Pydantic model to update event table on given condition
    """
    event_name: Optional[str] = None
    sport_name: Optional[str] = None
    id: Optional[int] = None

    @model_validator(mode='before')
    def validate_condition(cls, values):
        if not values.get("id") and not values.get("event_name") and not values.get("sport_name"):
            raise ValueError("Either id or event_name and sport_name should be provided")
        return values

class EventUpdate(BaseModel):
    update: EventUpdateValues
    condition: EventUpdateCondition

    @model_validator(mode='before')
    def validate_update(cls, values):
        if values.get("condition").get("event_name") and values.get("update").get("event_name"):
            raise ValueError("Name cannot be updated when condition is name")
        return values

class Selection(BaseModel):
    """
    Pydantic model for inserting values in selections table
    """
    selection_name: str 
    event_name: str
    price: float
    active: bool
    outcome: str

    @field_validator("selection_name")
    def validate_name(cls, value):
        if re.search("[^a-zA-Z0-9s]", value):
            raise ValueError("Selection  name cannot contain special characters")
        return value
    
    @field_validator("outcome")
    def validate_outcome(cls, value):
        if value not in VALID_SELECTION_OUTCOME:
            raise ValueError(f"Selection outcome should be one among {VALID_SELECTION_OUTCOME}")
        return value


class SelectionUpdateValues(BaseModel):
    """
    Pydantic model to update selections table values
    TODO: Use the Selection base model
    """
    selection_name: Optional[str] = None 
    event_name: Optional[str] = None
    price: Optional[float] = None
    active: Optional[bool] = None
    outcome: Optional[str] = None

class SelectionUpdateConditions(BaseModel):
    """
    Pydantic model to update selection table on given condition
    """
    selection_name: Optional[str] = None 
    event_name: Optional[str] = None 
    id: Optional[int] = None

    @model_validator(mode='before')
    def validate(cls, values):
        if not values.get("id") and not values.get("selection_name") and not values.get("event_name"):
            raise ValueError("Either id or name and sport_name should be provided")
        return values

class SelectionUpdate(BaseModel):
    """
     Pydantic model to update events table
     """
    update: SelectionUpdateValues
    condition: SelectionUpdateConditions

    @model_validator(mode='before')
    def validate(cls, values):
        if values.get("condition").get("selection_name") and values.get("update").get("selection_name"):
            raise ValueError("Name cannot be updated when condition is name")
        return values
    
class Select(BaseModel):
    """
    Pydantic model for select statement
    """
    table_name: Optional[str] = ''
    join_key: Optional[str] = ''
    keys: Union[List[str], str, None]

class Conditions(BaseModel):
    """
    Pydantic model for where condition
    """
    key: str
    value: Any
    operator: str

    @field_validator('operator')
    def validate_operator(cls, value, values):
        if value not in VALID_CONDITIONS:
            raise ValueError(f'Valid operator are {VALID_CONDITIONS}')
        if value == 'between' and (type(values.get('value')) != list or len(values.get('value'))!= 2):
            raise ValueError('between should have only two values')

class ConditionsDate(BaseModel):
    """
    Pydantic model for where conditions with date type
    """
    key: str
    value: Union[datetime, list[datetime]]
    operator: str

    @field_validator('operator')
    def validate_operator(cls, value, values):
        if value not in VALID_CONDITIONS:
            raise ValueError(f'Valid operator are {VALID_CONDITIONS}')
        if value == 'between' and (type(values.get('value')) != list or len(values.get('value'))!= 2):
            raise ValueError('between should have only two values')
        
    @field_validator('value')
    def validate_operator(cls, value):
        if type(value) == list:
            return [date.astimezone(pytz.utc) for date in value]
        return value.astimezone(pytz.utc)

class Search(BaseModel):
    """
    Pydantic model to search in the database
    """
    table_name: str
    conditions: Optional[List[Conditions]] = []
    conditions_date: Optional[List[ConditionsDate]] = []
    select: Optional[Select] = None