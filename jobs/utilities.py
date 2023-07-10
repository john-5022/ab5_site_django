"""jobs/utilities.py
This contains generic functions that we regularly use.

***This has been copied from jobS_ab5_psg and can be modified as needed for Django***

They are grouped by functions:
String & numeric, Date, (CSV,SQL and SQLite)
Convention: import utilities as util - then call as util.function()"""

import csv
import sqlite3
from datetime import date, datetime, timedelta
import string

#================String & numeric functions===========================
def build_placeholders(how_many):
    """Builds comma separated string e.g. '(?,?,?,?)' as placeholders for SQL INSERT

    Note that this is not a tuple (no commas) so it works with a single field
    This is called from other function(s)"""
    
    count = 1
    while count <= how_many:
        if count == 1:
            holder = '?'
        else:
            holder = f'{holder},?'
        count += 1
    return f'({holder})'

def list_to_string(*args):
    """This receives a list of strings and returns a comma-separated string.

    The first parameter is the a list
    The second is optional and is the type ('str' or 'int') - default is 'str'

    If the type is 'str' or none, each item is surrounded by quotes.
    There is no need for quotes for integers.
    It was created for a listbox in PySimpleGUI"""

    str_val =''
    lst_name = args[0]
    if len(args) < 2:
        s_type = 'str'
    else:
        s_type = args[1]
    item_num = 0
    for item in lst_name: # Process contents of list
        item_num += 1
        if item_num == 1:
            if s_type == 'str':
                str_val = f'{str_val} "{item}"' # Need quotes around each item
            else: # Assume integer
                str_val = f'{str_val} {item}' # Integer - no quotes
        else:
            if s_type == 'str':
                str_val = f'{str_val}, "{item}"' # Add comma
            else:
                str_val = f'{str_val}, {item}'
    return str_val # Developer to add brackets, etc as needed

#================Date and time functions===========================
def str2date_obj(s_date):
    """Return a date object from a date string (e.g. '2022-04-02') 
        ****Called below so needs to be on top****

    The date object can be used for date calculations.
    """

    date_obj = date(int(s_date[0:4]), int(s_date[5:7]), int(s_date[8:10]))
    return date_obj

def date_today():
    '''Returns today's date as YYYY-MM-DD
    Note: to get datetime - date_time_now = datetime.now() - add function as needed'''

    today = date.today()
    return today

def d2str(dateobj_or_str, f_map):
    """Returns a formatted string from a date object or string.
    
        Parameters:-
            Date object, a date as string ('YYYY-MM-DD) or an empty string
            Format map:
            - 'd_Mmm_YYYY'  to return e.g. 2 Apr 2022
            - 'd_Mmmm_YYYY'  to return e.g. 2 April 2022
            - 'YYYY-MM-DD'  to return e.g. 2022-04-02
            - 'YYYY-MM'  to return e.g. 2022-04"""
    
    f_date = '' # Default return if empty
    if dateobj_or_str:      
        if isinstance(dateobj_or_str, date): # Is it is already a date object?
            date_obj = dateobj_or_str
        else: # Convert string to obj
            date_obj = str2date_obj(dateobj_or_str)

        if f_map == 'd_Mmm_YYYY': #  returns e.g. 2 Apr 2022
            f_date = date_obj.strftime("%d %b %Y")
            f_date = f_date.lstrip('0') # Strip any leading zero

        elif f_map == 'd_Mmmm_YYYY': #  returns e.g. 2 April 2022
            f_date = date_obj.strftime("%d %B %Y")
            f_date = f_date.lstrip('0') # Strip any leading zero

        elif f_map == 'YYYY_MM_DD': #  returns e.g. 2022-04-02 for Sqlite etc.
            f_date = date_obj.strftime("%Y-%m-%d")

        elif f_map == 'YYYY_MM': #  returns e.g. 2022-04-02 for Sqlite etc.
            f_date = date_obj.strftime("%Y-%m")

    return f_date

def hour_min_to_min(hours, minutes):
    """Receives hours and minutes and returns minutes.
    Must be integers - if not, zeros are returned"""
    mins = (hours * 60) + minutes
    return mins

def increment_date(date_obj, num_days):
    """This adds or subtracts days to a date.
    
    Number of days can be + or -
    This saves working out days in a month and handling leap years."""

    date_obj = date_obj + timedelta(days=num_days) # Date object
    return date_obj

def min_to_hour_min(minutes):
    """Receives minutes and returns hours and minutes.
    Must be integer - if not, zeros are returned"""
    if minutes >= 0:
        hours = minutes // 60
        mins = minutes % 60
        return hours, mins
    else:
        return 0, 0

def reformat_psg_popup_date(t_date):
    """Reformat PSG date for SqLite and user.
    
    The PSG popup returns the selected date as a tuple (m,d,y) so we need to
        convert the parameters to strings, add leading zeros as needed
        and reformat it as 'YYYY-MM-DD' for Sqlite and 'd Mmm yyyy' for user."""
    # Extract year, month, day from tuple
    s_year = str(t_date[2]) 
    s_month = str(t_date[0]).rjust(2,"0")
    s_day = str(t_date[1]).rjust(2,"0")
    s_date = f'{s_year}-{s_month}-{s_day}' # Format date as string
    d_date = str2date_obj(s_date) # Date object
    f_date = d2str(d_date, 'd_Mmm_YYYY') # Date formatted as 2 Mar 2022
    s_date = f"'{s_date}'" # Date as string '2022-03-02' with quotes for sql

    return s_date, f_date

def test_from_to_dates(s_date_from, s_date_to):
    """Call to make sure that from and to dates are in the correct order. 
    
    Returns an error message or an empty string when the order is OK.)"""

    if s_date_from and s_date_to and s_date_from > s_date_to:
        return "The 'from' date must not be after the 'to' date - please change!"
    else:
        return ''

#==========================CSV, SQL and SqLite functions===========================
def build_filters_from_list(lst_filters):
    """Builds a WHERE clause from a list of strings containing filter conditions.

    Returns a string that can be used to add the WHERE clause to sql.
    Only use this where elements are connected with AND"""

    n_count = 0
    s_where = ' '
    for item in lst_filters:
        n_count += 1
        if n_count> 1: # Add to the existing ststement
            s_where = f' {s_where} AND {item}'
        else: # n_count is zero so we need the WHERE clause
            s_where = f'WHERE {item}'
    return s_where

def csv_to_list(csv_file_name, list_type):
    """Converts contents of a CSV file to a list, tuple or dictionary
    
    2nd parameter MUST be one of: 'list', 'tuple' or 'dict'
    If we want to print, use: for row in list then print(row)
    This is called from a function below"""
    
    data = message_ = ''
    try:
        file_name = open(csv_file_name, "r")
        if list_type in ('list', 'tuple'):
            reader = csv.reader(file_name, delimiter=',')
            data = [] # Emply list - we need to fill it...
            line_no = 0
            for line in reader: # Build list of lists
                line_no += 1
                if line_no == 1:
                    header_tuple = line
                else:
                    if list_type == 'list':
                        data.append(line)
                    else: #List of tuples
                        data.append(tuple(line))                    
        elif list_type == 'dict':
            reader = csv.DictReader(file_name, delimiter=',')
            data = list(reader) # List of dicts 
        else:
            message_ = 'Error - a valid list_type was not passed'
    except Exception as e:
        message_ = f"Failed to execute csv_to_list\n with error:\n{e}"
    return header_tuple, data, message_

def add_recs(con, table_name, header_tuple, data):
    """Add record(s) to a table.

    The parameter 'data' must contain a list of tuples.

    Calling function(s) must handle con open and close.
    Returns no. of records added and message.
    
    Note: for tables with a single field, ensure that each record has a value to avoid error
    ...because it is not inturpreted as a tuple"""

    message_ = ''
    recs_added = 0
    field_count = len(header_tuple)

    item_no = 0
    for item in header_tuple:
        item_no += 1
        if item_no == 1:
            field_names = f'{item}'
        else:
            field_names = f'{field_names}, {item}'

    placeholders = build_placeholders(field_count) # e.g. (?,?,?)
    
    sql = f'INSERT INTO {table_name} ({field_names}) VALUES{placeholders}'
    try:
        cur = con.executemany(sql, data) # Insert all
        con.commit()
        recs_added = cur.rowcount
    except Exception as e:
        message_ = f"Failed to execute - error: {e}"

    return recs_added, message_

def add_recs_from_csv(con, table_name, csv_filename):
    """Generic function to add records to a single table when no processing is needed.

    Inserts data into a single table from CSV file
    Calling function must handle con open and close"""

    # from_csv = csv_to_list(csv_filename, 'tuple') # List of tuples from csv file
    header_tuple, data, message_ = csv_to_list(csv_filename, 'tuple')

    recs_added, message_ = add_recs(con, table_name, header_tuple, data) # Includes try:

    # Calling function should test message_ - indicates error
    return recs_added, message_

def delete_record(con, table, filters):
    """Delete record(s)
    
    Filters contains either:-
    - 'All' to delete all records or
    - a dictionary with filter string(s) and value(s)
    The filter string must contain everything needed for the WHERE clause INCLUDING spaces and ?
    ...e.g. first: 'WHERE field_name >= ?'
    ...second: ' AND field_name2 <= ?'"""

    message_ = ''
    recs_deleted = 0
    sql = f'DELETE FROM {table}'
    if type(filters) is dict: # Dictionary - add WHERE clause
        filter_strings = tuple(filters.keys())
        filter_vals  = tuple(filters.values())
        for f_string in filter_strings: # Update the SQL
            sql = f'{sql} {f_string}'
    elif filters == 'All':
        sql = sql # No action - leave sql unchanged so all records will be deleted
    else:
        message_ = 'The function did not receive a valid filter - no action taken'
    if not message_:
        try:
            if filters != 'All':
                cur = con.execute(sql, filter_vals) # filter_vals replace the ? 
            else:
                cur = con.execute(sql) # Delete all
            con.commit()
            recs_deleted = cur.rowcount
        except Exception as e:
            message_ = f"Failed to execute delete. Query: {sql}, Filter Vals: {filter_vals}\n with error:\n{e}"
    return recs_deleted, message_

def sql_to_dicts(con, sql):
    """Runs an SQL query then returns data as a list of dicts.

    Column names become keys. Thanks to Nick George post.
    Params:- 
    * sql is the SELECT statement as a string.
    """

    try:
        con.row_factory = sqlite3.Row   # Gets the row names
        things = con.execute(sql).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked # List of dictionaries
    except Exception as e:
        print(f"Failed to execute. Query: {sql}\n with error:\n{e}")
        return e

def sql_to_list(con, sql):
    """Runs an SQL query then returns data as a list

    * sql is the SELECT statement as a string.
    """

    try:
        cur = con.execute(sql)
        list_ = []
        for row in cur:
            list_.append(row[0]) # Each row is a tuple
        return list_ # List

    except Exception as e:
        print(f"Failed to execute. Query: {sql}\n with error:\n{e}")
        return e  

def sql_to_lists(con, sql):
    """Runs an SQL query then returns data as a list of lists

    * sql is the SELECT statement as a string.
    """

    try:
        cur = con.execute(sql)
        list_rows = []
        for row in cur:
            list_col = []
            col_no = -1
            for col in row:
                col_no += 1
                list_col.append(col)
            list_rows.append(list_col)
        return list_rows # List of lists

    except Exception as e:
        print(f"Failed to execute. Query: {sql}\n with error:\n{e}")
        return e       

def update_record(con, table, fields_and_vals, filters):
    """Updates record(s)
    
    Params:
    - fields_and_vals - dictionary that contains field name and new value pairs
    - filters contains either:-
       - 'All' to delete all records or
       - a dictionary with filter string(s) and value(s)
        The filter string must contain everything needed for the WHERE clause INCLUDING spaces and ?
        ...e.g. first: 'WHERE field_name >= ?'
        ...second: ' AND field_name2 <= ?'
    Returns:
    - recs_updated, (error) message_
    The record(s) is updated using placeholders."""

    # Sample SQL
    # : UPDATE {table} SET field1 = ?, field2 = ? WHERE id = ?
    message_ = ''
    recs_updated = 0
    # Extract field names and values from dictionaries
    field_names = tuple(fields_and_vals.keys()) # Fields to be updated
    ff_vals  = list(fields_and_vals.values()) # New field (and filter) values - list so we can append to it
    # Build the SQL
    sql = f'UPDATE {table} SET '

    i = 0 # Add field names and placeholders
    for f_name in field_names:
        i += 1
        if i == 1:
            sql = f'{sql} {f_name} = ?' # No comma
        else:
            sql = f'{sql}, {f_name} = ?' # Trailing comma

    if type(filters) is dict: # Dictionary - add WHERE clause
        filter_strings = tuple(filters.keys())
        filter_vals  = tuple(filters.values())
        for f_string in filter_strings: # Update the SQL
            sql = f'{sql} {f_string}'
        for f_val in filter_vals: # Append filter values to field values
            ff_vals.append(f_val)
        ff_vals = tuple(ff_vals) # Convert to tuple for execute
    else:
        message_ = 'The function did not receive a valid filter - no action taken'
    if not message_:
        try:
            cur = con.execute(sql, ff_vals) # Replace the ? for fields and filters
            con.commit()
            recs_updated = cur.rowcount
        except Exception as e:
            message_ = f"Failed to execute delete. Query: {sql}, Filter Vals: {filter_vals}\n with error:\n{e}"
    return recs_updated, message_

#======= End of ============CSV, SQL and SqLite functions===========================