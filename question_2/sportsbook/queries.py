"""
This python file is used to declare or build the queries used to perform operations
"""
from .models import Search

UPDATE_TABLE = "UPDATE {table_name} set {values} WHERE {condition}"
SELECT_ALL = "SELECT * from {table_name}"
SELECT_CONDITION = "SELECT * from {table_name} WHERE {condition}" 

INSERT_SPORT = "INSERT INTO sports(sport_name, slug, active) VALUES (:sport_name, :slug, :active)"
UPDATE_SPORT_EVENT = 'UPDATE sports set active = false WHERE (select count(*) from events e where e.sport_name like "{sport_name}" and e.active = true) = 0'
UPDATE_SPORT_NAME = 'UPDATE events set sport_name = "{sport_name}" WHERE sport_name = "{sport_name_old}"'

INSERT_EVENT = "INSERT INTO events(event_name, slug, active, type, sport_name, status, scheduled_start, actual_start) VALUES (:event_name, :slug, :active, :type, :sport_name, :status, :scheduled_start, :actual_start)"
UPDATE_EVENT_SELECTION = 'UPDATE events set active = false WHERE (select count(*) from selections s where s.event_name = "{event_name}" and s.active = false) = 0'
UPDATE_EVENT_NAME = 'UPDATE selections set event_name = "{event_name}" WHERE event_name = "{event_name_old}"'

INSERT_SELECTION = "INSERT INTO selections(selection_name, event_name, price, active, outcome) VALUES (:selection_name, :event_name, :price, :active, :outcome)"

def build_search_query(search_model: Search) -> str:
    """
    Builds sql query from pydantic model Search
    We allow simple select from a given table and also select keys from the parent table by mentioning join key
    TODO: There is a scope to update the request to select keys from both parent and child table
 
    Parameters
    ----------
    search_model : Search
        pydantic model that needs to be converted to sql
 
    Returns
    -------
    str
        returns the sql query
    """
    search_query = ""
    table_name = search_model.table_name
    select_table_name = ""

    # check if the select table name matches the given table name
    # other wise create the join query
    if search_model.select:
        keys = search_model.select.keys
        if search_model.select.table_name and search_model.select.table_name != search_model.table_name:
            select_table_name = search_model.select.table_name
            if keys:
                if type(keys) == list:
                    search_query = f"SELECT DISTINCT {', '.join('select_table_name' + key for key in search_model.select.keys)} FROM {select_table_name}"
                elif type(keys) == str and keys.lower() == "count":
                    search_query = f"SELECT COUNT(DISTINCT {select_table_name}.id) as count from {select_table_name}"
            else:
                search_query = f"SELECT DISTINCT {select_table_name}.* from {select_table_name}"
            search_query = f"{search_query} JOIN {table_name} ON {table_name}.{search_model.select.join_key}={select_table_name}.{search_model.select.join_key}" 
        elif keys:
                if type(keys) == list:
                    search_query = f"SELECT {', '.join(key for key in search_model.select.keys)} FROM {table_name}"
                elif type(keys) == str and keys.lower() == "count":
                     search_query = f"SELECT COUNT(*) as count FROM {table_name}"
        else:
            search_query = f"SELECT * FROM {table_name}"
    else:
        search_query = f"SELECT * from {table_name}"
    
    # Generate the where condition by iterating through all the conditions
    where_condition = ""
    for condition in search_model.conditions:
        if not select_table_name:
            where_condition = f" {where_condition} {condition.key} "
        else:
            where_condition = f" {where_condition} {table_name}.{condition.key} "             
        if type(condition.value) == str:
                where_condition = f'{where_condition} {condition.operator} "{condition.value}"'
        elif condition.operator == "between" and type(condition.value[0]) == str:
             where_condition = f'{where_condition} {condition.operator} "{condition.value[0]}" AND "{condition.value[-1]}" '
        elif condition.operator == "between" and type(condition.value[0]) != str:
             where_condition = f'{where_condition} {condition.operator} {condition.value[0]} AND {condition.value[-1]} '
        else:
            where_condition = f'{where_condition} {condition.operator} {condition.value}'
    
    # We have separate field for date search - to make things simpler 
    for condition in search_model.conditions_date:
        if not select_table_name:
            where_condition = f" {where_condition} {condition.key} "
        else:
            where_condition = f" {where_condition} {table_name}.{condition.key} "             
        if condition.operator == "between":
             where_condition = f'{where_condition} {condition.operator} "{condition.value[0]}" AND "{condition.value[-1]}" '
        else:
            where_condition = f'{where_condition} {condition.operator} "{condition.value}"'

    return search_query if not where_condition else f"{search_query} WHERE {where_condition}"
    