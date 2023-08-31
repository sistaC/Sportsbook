"""
This python file is used to define all the database related operations
"""

from databases import Database
import aiosqlite
from contextlib import asynccontextmanager
import os
from .queries import UPDATE_TABLE

@asynccontextmanager
async def get_db():
    """Return a database connection for use as a dependency.
    This connection has the Row row factory automatically attached."""
    db = os.environ.get('DB_PATH', 'sportsbook.db')
    database = Database(f'sqlite+aiosqlite:///{db}')
    await database.connect()
    database.row_factory = aiosqlite.Row

    try:
        yield database
    finally:
        await database.disconnect()


async def fetch_values(query : str, values : list =None ) -> list(dict):
    """
    Executes the given query and returns all the rows that match the condition
 
    Parameters
    ----------
    query : str
        query to be executes
    values : list
        if there are any values to be replaced
 
    Returns
    -------
    list(dict)
        The dictionary of the selected rows
    """
    async with get_db() as database:
        rows = await database.fetch_all(query=query, values=values)
        return [row._asdict() for row in rows]

async def insert_values(query : str, values : list =None) -> int:
    """
    Inserts the values into the database
 
    Parameters
    ----------
    query : str
        query to be executes
    values : list
        if there are any values to be replaced
 
    Returns
    -------
    int
        updated row id
    """
    async with get_db() as database:
        return await database.execute(query=query, values=values)

async def update_values(model, condition : str, table_name : str) -> int:
    """
    Updates the values in the database and returns the updated id
 
    Parameters
    ----------
    model : pydanticmodel
        query to be executes
    condition : str
        where condition to update
    table_name : str
        table name to update the data
 
    Returns
    -------
    int
        updated row id
    """
    
    values = ""
    values_dict = {}
    for key, value in model.update:
        if value is not None:
            values = f'{values}, {key}=:{key}' if values else f'{key}=:{key}'
            values_dict[key] = value
    query = UPDATE_TABLE.format(table_name = table_name, values = values, condition = condition)    
    return await insert_values(query=query, values=values_dict)