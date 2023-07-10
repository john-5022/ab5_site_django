# """jobs/create_records.py
# This contains functions that can be run as needed
#     including creating records from a CSV file.

#     ***This has been copied from jobS_ab5_psg and can be modified as needed for Django
#     this may not be used - get recurring working***

#     Uncomment below to run as needed
#     """
# import csv
# from datetime import datetime
# import sqlite3
# from unittest import result
# import utilities as util

# def new_job_etc_record(con, table_name, field_data, id_foreign, rec_order):
#     """ ***Create new Job, task or action record in database***
#         Called from job_data_from_csv function below as needed
#         For this test, field_data is just one record
#         field_data is a dictionary that we access as needed
#     """
#     if table_name == 'Action':
#         data_tuple = (field_data, id_foreign, rec_order)
#         sql = """INSERT INTO action(action_name, task_id, action_order)
#         VALUES(?,?,?)"""
#         try:
#             cur = con.execute(sql, data_tuple)
#             action_id = cur.lastrowid
#             return action_id                
#         except:
#                 print(f"{table_name}Insert did not work at: {datetime.time(datetime.now())}")
#     if table_name == 'Task':      
#         data_tuple = (field_data, id_foreign, rec_order)
#         sql = """INSERT INTO task(task_name, job_id, task_order)
#         VALUES(?,?,?)"""
#         try:
#             cur = con.execute(sql, data_tuple)
#             task_id = cur.lastrowid
#             return task_id                
#         except:
#                 print(f"{table_name}Insert did not work at: {datetime.time(datetime.now())}")
#     if table_name == 'Job':
#         data_tuple = (field_data, id_foreign)
#         sql = """INSERT INTO job(job_name, client_id)
#         VALUES(?,?)"""
#         try:
#             cur = con.execute(sql, data_tuple)
#             job_id = cur.lastrowid
#             return job_id                
#         except:
#             print(f"{table_name}Insert did not work at: {datetime.time(datetime.now())}")

# def new_r_record(con, table_name, field_data, id_foreign, rec_order):
#     """ ***Create new recurring Job, task or action record(s) in database***
#         Called from import_recurring_records function below as needed
#         For this test, field_data is just one record #ToDo Provide for multiple
#     """
#     if table_name == 'Action':
#         data_tuple = (field_data, id_foreign, rec_order)
#         sql = """INSERT INTO action(action_name, task_id, action_order)
#         VALUES(:action_name, :task_id, :action_order)"""
#         try:
#             cur = con.execute(sql, data_tuple)
#             action_id = cur.lastrowid
#             return action_id                
#         except:
#             print(f"{table_name}Insert did not work at: {datetime.time(datetime.now())}")
#     if table_name == 'Task':      
#         data_tuple = (field_data, id_foreign, rec_order)
#         sql = """INSERT INTO task(task_name, job_id, task_order)
#         VALUES(:task_name, :job_id, :task_order)"""
#         try:
#             cur = con.execute(sql, data_tuple)
#             task_id = cur.lastrowid
#             return task_id                
#         except:
#             print(f"{table_name}Insert did not work at: {datetime.time(datetime.now())}")
#     if table_name == 'Job':
#         data_tuple = (field_data, id_foreign)
#         sql = """INSERT INTO job(job_name, client_id)
#         VALUES(:job_name, :client_id)"""
#         try:
#             cur = con.execute(sql, data_tuple)
#             job_id = cur.lastrowid
#             return job_id                
#         except:
#                 print(f"{table_name}Insert did not work at: {datetime.time(datetime.now())}")

# def job_data_from_csv(con, file_name):
#     """ ***Build Job, Task and Action records from a CSV file.***
#         We process each column in order to ensure that correct FK is passed.
#         Records are created by calling function above.
#     """
#     client_id = 0   # The id's are reset as needed
#     job_id = 0
#     task_id = 0
#     with open(file_name, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         ##########
#         # Each row is a dictionary with the keys as per the header row
#         ##########
#         for row in reader:
#             if row['Client_id']: # Tests the value in the dictionary with this key
#                 #   Just reset the client FK - new Job record created below
#                 client_id = row['Client_id']
#             if row['Job']:
#                 task_order = 0 # Reset for new job
#                 job_id = new_job_etc_record(con, 'Job', row['Job'], client_id, 0)
#             if row['Task']:
#                 task_order = task_order + 1
#                 action_order = 0
#                 task_id = new_job_etc_record(con, 'Task', row['Task'], job_id, task_order)
#             if row['Action']: 
#                 action_order = action_order + 1
#                 action_id = new_job_etc_record(con, 'Action', row['Action'], task_id, action_order)
#                 #   action_id not used - just so we can see it
#     con.commit()
#     return 'Creating jobs, etc. has finished - please check the data file'

# def build_default_maps(con):
#     """Build dummy test maps between the default task and action tables - 5 actions for each task
#     We need to work out how to do this with real data"""

#     cur_task = con.execute('SELECT id from default_task') # Get all records into object
#     cur_action = con.execute('SELECT id from default_action')

#     keep_going = True
#     while(keep_going is True):
#         result1 = cur_task.fetchone()   # Get next record - tuple
#         if result1 is None: # No more records so bail out
#             keep_going = False
#         else:
#             id_task = result1[0] # Extract the first value from the tuple
#             result2 = cur_action.fetchmany(size = 5) # Next records limited by size - List of tuples
#             action_order = 0
#             for item in result2:
#                 action_order = action_order + 1
#                 id_action = item[0]

#                 sql = """INSERT INTO defaults_map(d_action_id, d_action_order, d_task_id) VALUES(?,?,?)"""
#                 data = (id_action, action_order, id_task)
#                 con.execute(sql, data) # Insert the record
#                 con.commit() # Save it!
#     return 'build_default_maps has completed - please check data'


# def import_recurring_records(con,file_name):
#     """ ***Build recurring Job, Task and Action records from a CSV file.***
#         We process each column in order to ensure that correct FK is passed.
#         Records are created by calling function above.
#     """
#     test_client_id = 0
#     test_job_name_start = ''
#     with open(file_name, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         ##########
#         # Each row is a dictionary with the keys as per the header row
#         ##########
#         for row in reader:
#             client_id = row['client_id']
#             job_name_start = row['job_name_start'] # This is used to test whether a new job is needed
#             if (test_client_id != client_id) or (test_job_name_start!= job_name_start):
#                 # We need a new r_job
#                 test_client_id = client_id
#                 test_job_name_start= job_name_start
#                 r_task_order = 0

#                 every = row['every']
#                 period_freq = row['period_freq']
#                 fin_year = row['fin_year']
#                 period_end = row['period_end']
#                 field_values = (client_id, job_name_start, every, period_freq, fin_year, period_end) # Tuple for INSERT
#                 field_names = ('client_id', 'job_name_start', 'every', 'period_freq', 'fin_year', 'period_end')
#                 # Create recur_job
#                 #   Build the sql statement
#                 sql = f'INSERT INTO recur_job {field_names} VALUES(?,?,?,?,?,?)'
#                 # sql = f'{sql} VALUES({field_values})' # Concatenate to 1 string
#                 # data_tuple = tuple(field_values) # Must use tuple to INSERT
#                 cur = con.execute(sql, field_values)
#                 r_job_id = cur.lastrowid
            
#             # Create r_task record
#             r_task_filter = row['r_task_filter']
#             r_task_name = row['d_task_name']
#             r_task_order = r_task_order + 1
#             field_values = (r_job_id, r_task_filter, r_task_name, r_task_order)
#             field_names = 'r_job_id', 'r_task_filter', 'r_task_name', 'r_task_order'
#             #   Build the sql statement
#             sql = f'INSERT INTO recur_task {field_names} VALUES(?,?,?,?)'
#             cur = con.execute(sql, field_values)
#             r_task_id = cur.lastrowid

#             # Create r_actions from default_actions linked to default_task via defaults_map
#             sql = f'SELECT default_action.d_action_name, default_action.d_action_description, '
#             sql = f'{sql}defaults_map.d_action_order FROM defaults_map '
#             sql = f'{sql}JOIN default_action on defaults_map.d_action_id = default_action.id '
#             sql = f'{sql}JOIN default_task on defaults_map.d_task_id = default_task.id '
#             sql = f'{sql}WHERE default_task.d_task_name == "{r_task_name}"'
#             cur = con.execute(sql)
#             result2 = cur.fetchmany() 
#             ##################---ToDo Test for at least one action---######################
#             for item in result2:
#                 r_action_name = item[0]
#                 r_action_description = item[1]
#                 r_action_order = item[2]

#                 # Create r_action record
#                 field_values = (r_task_id, r_action_description, r_action_name, r_action_order)
#                 field_names = 'r_task_id', 'r_action_description', 'r_action_name', 'r_action_order'
#                 sql = f'INSERT INTO recur_action {field_names} VALUES(?,?,?,?)'
#                 cur = con.execute(sql, field_values)
#     con.commit()
#     return 'Creating recurring jobs, etc. has finished - please check the data file'

# #=========================================================================
# #   Run - uncomment below as needed
# #=========================================================================
# con = sqlite3.connect('test_jobs.db') ########## - Check db name - ###################

# # recs_added, message_ = util.add_recs_from_csv(con, 'client', 'clients.csv')
# # recs_added, message_ = util.add_recs_from_csv(con, 'state', 'states.csv')

# # recs_added, message_ = util.add_recs_from_csv(con, 'default_action', 'Default Actions.csv')
# # recs_added, message_ = util.add_recs_from_csv(con, 'default_task', 'Default Tasks.csv')

# # message_ = build_default_maps(con) # Do after importing defaults
# # message_ = job_data_from_csv(con, 'jobs_etc.csv')
# message_ = import_recurring_records(con, 'Recurring starter.csv')

# print(message_)
# con.close()