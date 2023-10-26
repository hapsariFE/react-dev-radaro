import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from anvil.google.drive import app_files
import anvil.secrets
import anvil.mpl_util
import anvil.users
import anvil.server
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import anvil.server
import anvil.tz
import json
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import requests


#authenticated_callable = anvil.server.callable(require_user=True)

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
#@authenticated_callable
#def get_users():
#  return app_tables.users.search()
#@anvil.server.http_endpoint("/users/list")
#def get_user_list():
#  return [u['email'] for u in app_tables.users.search()]


@anvil.server.http_endpoint('/incoming_msg')
def incoming_msg(**kwargs): 
  data = anvil.server.request.body_json
  #json['topic']
  topic = data.get('topic')
  merctable = app_tables.merchant.get(token=data['token'])
  
  lowrate_enable = merctable['low_rating_enabled']
  compcode_enable = merctable['completion_code_enabled']
  failcode_enable = merctable['fail_code_enabled']
  
  if 'new_values' in data :
    if data['new_values'] is not None and 'is_confirmed_by_customer' in data['new_values'] and lowrate_enable == True:
      if merctable is not None:
      
        if 'job.status_changed' in topic and 'updated' in data.get('event_type') and True == data['new_values']['is_confirmed_by_customer'] and merctable['rating_threshold'] >= data['order_info']['rating'] :
        #print(json)
          submit_low_rating(data)

    if 'job.completion_codes_accepted' in topic and 'updated' in data.get('event_type'):
       if 'delivered'==data['order_info']['status'] and compcode_enable == True:
          submit_completion_codes(data) 
       elif failcode_enable == True and 'failed'==data['order_info']['status']:
          print("fail code testing")
          submit_completion_codes(data) 
    else:
        pass 
       ##     codes=data['order_info']['completion_codes']
    ##     id_values = [str(code["code"]) for code in codes]
    ##     id_string = ";".join(id_values)
        #codes=data['order_info']['completion_codes']
        #id_values = [str(code["code"]) for code in codes]
        #id_string = ";".join(id_values)
       # comp_names = [str(code["name"]) for code in codes]
        #comp_string = ";".join(comp_names)
        #if not comp_string:
        #  print(comp_string)
         # comp_string = None
          
       # nv = data['new_values']['is_confirmed_by_customer']
       # rating = data['order_info']['rating']
       # counter = get_next_value_in_sequence()
        #try:
       # app_tables.webhook.add_row(
        #job_id = str(data['order_info']['order_id']),
       # id= str(counter),
       # customer_name = data['order_info']['customer']['name'],
      #  completion_code_id = id_string,
       # completion_code_description = "Low Rating", 
       # date_created = datetime.now(),
       # last_action_date =datetime.now(),
       # job_reference = data['order_info']['title'],
      #  webhook_merchant_link=app_tables.merchant.get(token=data['token']),
      #  job_status = app_tables.job_status.get(sysName=data['order_info']['status']),
      #  job_report = data['order_info']['public_report_link'],
      #  customer_rating= str(rating),
        #escalation_type = "Low Rating",
      #  latest_assignee = None,
      #  latest_status = app_tables.escalation_status.get(name= "New"),
       # sub_brand=str(data['order_info']['sub_branding']),
       # mobile_number=data['order_info']['customer']['phone'],
       # date_delivered=datetime.strptime(data['order_info']['completed_at'], "%Y-%m-%dT%H:%M:%S.%f%z"), 
       # job_reference2=data['order_info']['title_2'],
       # job_reference3=data['order_info']['title_3'],
      #  address=data['order_info']['deliver_address']['address'],
      #  watch_list=False,
      # watchlistUsers=[])
        #except:
           # print("falied")
      
    #if 'job.completion_codes_accepted' in topic and 'updated' in data.get('event_type'):
    #  if 'delivered'==data['order_info']['status']:
    #    if compcode_enable == True:
    ##     codes=data['order_info']['completion_codes']
    ##     id_values = [str(code["code"]) for code in codes]
    ##     id_string = ";".join(id_values)
     #     submit_completion_codes(data) 
     #   elif failcode_enable == True and 'failed'==data['order_info']['status']:
     #     submit_completion_codes(data) 
        #nv = data['new_values']['is_confirmed_by_customer']
       # rating = data['order_info']['rating']
       # codes=data['order_info']['completion_codes']
      #  id_values = [str(code["code"]) for code in codes]
      #  id_string = ";".join(id_values)
      #  comp_names = [str(code["name"]) for code in codes]
       # comp_string = ";".join(comp_names)
       # counter = get_next_value_in_sequence()
        #try:
       # app_tables.webhook.add_row(
       # job_id = str(data['order_info']['order_id']),
      #  id= str(counter),
      #  customer_name = data['order_info']['customer']['name'],
      #  completion_code_id = id_string,
      #  completion_code_description = comp_string, 
      #  date_created = datetime.now(),
      #  last_action_date =datetime.now(),
      #  job_reference = data['order_info']['title'],
     #   webhook_merchant_link=app_tables.merchant.get(token=data['token']),
      #  job_status = app_tables.job_status.get(sysName=data['order_info']['status']),
      #  job_report = data['order_info']['public_report_link'],
      #  customer_rating= str(rating),
        #escalation_type = "Low Rating",
      #  latest_assignee = None,
      #  latest_status = app_tables.escalation_status.get(name= "New"),
      #  sub_brand=str(data['order_info']['sub_branding']),
      #  mobile_number=data['order_info']['customer']['phone'],
      #  date_delivered=datetime.strptime(data['order_info']['completed_at'], "%Y-%m-%dT%H:%M:%S.%f%z"), 
      #  job_reference2=data['order_info']['title_2'],
      #  job_reference3=data['order_info']['title_3'],
      #  address=data['order_info']['deliver_address']['address'],
      #  watch_list=False,
      #  watchlistUsers=[])
    

@anvil.server.callable
def submit_low_rating(data):
  codes=data['order_info']['completion_codes']
  id_values = [str(code["code"]) for code in codes]
  id_string = ";".join(id_values)
  comp_names = [str(code["name"]) for code in codes]
  comp_string = ";".join(comp_names)
  updated_at = data.get('updated_at')

  if data['order_info']['sub_branding'] is not None:
    subbrandval = str(data['order_info']['sub_branding'])
    merctable = app_tables.merchant.get(token=data['token'])
    existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=str(subbrandval),Server=merctable['server'],MerchantLink=merctable)
    if existing_record is not None:
      subbrandval = existing_record['Name']
    else:
      sync_subbrand(merctable)
      existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=str(subbrandval),Server=merctable['server'],MerchantLink=merctable)
      if existing_record is not None:
        subbrandval = existing_record['Name']
      else:
        subbrandval = "Unidentified"
            
  else:    
    subbrandval = "(Blank)"

  
  #if not comp_string:
  #  print(comp_string)
    # comp_string = None
    
  nv = data['new_values']['is_confirmed_by_customer']
  rating = data['order_info']['rating']
  counter = get_next_value_in_sequence()
  #try:
  app_tables.webhook.add_row(
  job_id = str(data['order_info']['order_id']),
  id= str(counter),
  customer_name = data['order_info']['customer']['name'],
  completion_code_id = id_string,
  completion_code_description = "Low Rating", 
  date_created = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%f%z"),
  last_action_date =datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%f%z"),
  job_reference = data['order_info']['title'],
  webhook_merchant_link=app_tables.merchant.get(token=data['token']),
  job_status = app_tables.job_status.get(sysName=data['order_info']['status']),
  job_report = data['order_info']['public_report_link'],
  customer_rating= str(rating),
  #escalation_type = "Low Rating",
  latest_assignee = None,
  latest_status = app_tables.escalation_status.get(name= "New"),
  sub_brand=subbrandval,
  mobile_number=data['order_info']['customer']['phone'],
  date_delivered=datetime.strptime(data['order_info']['completed_at'], "%Y-%m-%dT%H:%M:%S.%f%z"), 
  job_reference2=data['order_info']['title_2'],
  job_reference3=data['order_info']['title_3'],
  address=data['order_info']['deliver_address']['address'],
  watch_list=False,
  watchlistUsers=[])

  jobrow = app_tables.webhook.get(id=str(counter)) 
  jr_dict = dict(jobrow)
  assignname = None
  esc_status = app_tables.escalation_status.get(name= "New")
  description = "Created from Radaro"
  date_created = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%f%z")
  submitter = app_tables.users.get(email='system')
  add_comment(jobrow,jr_dict,description,esc_status,date_created,assignname,submitter)


@anvil.server.callable
def submit_completion_codes(data):
  rating = data['order_info']['rating']
  codes=data['order_info']['completion_codes']
  id_values = [str(code["code"]) for code in codes]
  id_string = ";".join(id_values)
  comp_names = [str(code["name"]) for code in codes]
  comp_string = ";".join(comp_names)
  updated_at = data.get('updated_at')
  counter = get_next_value_in_sequence()
  if data['order_info']['sub_branding'] is not None:
    subbrandval = str(data['order_info']['sub_branding'])
    merctable = app_tables.merchant.get(token=data['token'])
    existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=str(subbrandval),Server=merctable['server'],MerchantLink=merctable)
    if existing_record is not None:
      subbrandval = existing_record['Name']
    else:
      sync_subbrand(merctable)
      existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=str(subbrandval),Server=merctable['server'],MerchantLink=merctable)
      if existing_record is not None:
        subbrandval = existing_record['Name']
      else:
        subbrandval = "Unidentified"
            
  else:    
    subbrandval = "(Blank)"
  #try:
  app_tables.webhook.add_row(
  job_id = str(data['order_info']['order_id']),
  id= str(counter),
  customer_name = data['order_info']['customer']['name'],
  completion_code_id = id_string,
  completion_code_description = comp_string, 
  date_created = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%f%z"),
  last_action_date = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%f%z"),
  job_reference = data['order_info']['title'],
  webhook_merchant_link=app_tables.merchant.get(token=data['token']),
  job_status = app_tables.job_status.get(sysName=data['order_info']['status']),
  job_report = data['order_info']['public_report_link'],
  customer_rating= str(rating),
  #escalation_type = "Low Rating",
  latest_assignee = None,
  latest_status = app_tables.escalation_status.get(name= "New"),
  sub_brand=subbrandval,
  mobile_number=data['order_info']['customer']['phone'],
  date_delivered=datetime.strptime(data['order_info']['completed_at'], "%Y-%m-%dT%H:%M:%S.%f%z"), 
  job_reference2=data['order_info']['title_2'],
  job_reference3=data['order_info']['title_3'],
  address=data['order_info']['deliver_address']['address'],
  watch_list=False,
  watchlistUsers=[])
  
  jobrow = app_tables.webhook.get(id=str(counter)) 
  jr_dict = dict(jobrow)
  assignname = None
  esc_status = app_tables.escalation_status.get(name= "New")
  description = "Created from Radaro"
  date_created = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%f%z")
  submitter = app_tables.users.get(email='system')
  add_comment(jobrow,jr_dict,description,esc_status,date_created,assignname,submitter)
  

@anvil.server.callable
def get_merchant_list():
  currentUser=anvil.users.get_user()
  Xvalues = []
  x_rows = currentUser['user_merchant_link']
  x_list =[r['name'] for r in x_rows]
  #sbValues =[[row] for row in x_rows]
  #SBrecords = app_tables.subbrands.search(MerchantLink=q.any_of(*x_rows))
  #print(*SBrecords)
 # print(x_list)
  x_list.sort()
  return x_list

@anvil.server.callable
def get_subbrand_list():
  currentUser=anvil.users.get_user()
  #sbvalues = app_tables.subbrands.search(merchant_link=q.any_of(*values))
  Xvalues = []
  x_rows = currentUser['user_merchant_link']
  #x_list =[r['name'] for r in x_rows]
  #sbValues =[[row] for row in x_rows]
  SBrecords = app_tables.subbrands.search(q.any_of(MerchantLink=q.any_of(*x_rows),ID=q.any_of(*['00000000','00000001'])))
  x_list =[r['Name'] for r in SBrecords]
  #print(SBrecords)
  print(x_list)
  #x_list.sort()
  return x_list

@anvil.server.callable
def get_user_list():
  currentUser=anvil.users.get_user()
  related_rows = currentUser['user_merchant_link']
 # print(related_rows)
  values = [[row] for row in related_rows]
  #print(values)
  
  #rows = list(dict(r) for r in related_rows)
  #print(rows)
  #return app_tables.users.search(user_merchant_link=q.any_of(*values))
  return app_tables.users.search(tables.order_by("name", ascending=True),user_merchant_link=q.any_of(*values))
  
#@anvil.server.callable
#def get_active_user():
#  active_user = anvil.users.get_user('name')
#  return active_user

@anvil.server.callable
def get_cms():
 
  return app_tables.merchant.search(tables.order_by("name", ascending=True))

@anvil.server.callable
def update_cms(rowid,name,fail_code_enabled,completion_code_enabled,low_rating_enabled,rating_threshold):
  
    #rowid = app_tables.merchant.get(name=name)
    rowid.update(
    name=name,
    fail_code_enabled=fail_code_enabled,
    completion_code_enabled=completion_code_enabled,
    low_rating_enabled=low_rating_enabled,
    rating_threshold=rating_threshold
    )


  

@anvil.server.callable
def get_list(jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch):
  currentUser=anvil.users.get_user()
  kwargs={'job_status':jobValue,'completion_code_id':compCode}
  total = []
  
  #print(assignrow)
  defaultassign = get_user_list()
  #print(*defaultassign)
  #print(*[r for r in defaultassign])
  #if assignrow == None:
  #  assignrow = [[r] for r in defaultassign]
  #print(escStatus)

  #print("ooooooo")
  #print(escStatus)
  #print(jobValue)
  #selectedGroups = [r for r in currentUser['user_merchant_link']]
  #print(selectedGroups)
  #RelatedJobStatus = jobValue['name']
#  Jobvalues = [row for row in jobValue]
  #if jobValue is None:  
  #  jobValue = [jobValue for jobValue in app_tables.job_status.search()]
  #else:
   # jobValue = [row for row in jobValue]
  filter_dict = {}
  if assigned_to != None:
    defaultassign = app_tables.users.get(name=assigned_to['name'])
    filter_dict['latest_assignee'] = defaultassign

  if jobValue != None:
    filter_dict['job_status'] = jobValue

  if compCode != None:
    filter_dict['sub_brand'] = compCode
    print(filter_dict['sub_brand'])

  if escType != None:
    filter_dict['completion_code_description'] = escType

  if watch is True :
    filter_dict['watchlistUsers'] = [anvil.users.get_user()]

  if escStatus != None:
    if resolvedStatus is False:
      print(escStatus['name'])
      escStatus = app_tables.escalation_status.search(name=q.all_of(q.none_of("Resolved"),q.any_of(escStatus['name'])))    
    if resolvedStatus is True:
      escStatus = app_tables.escalation_status.search(name=q.any_of(q.any_of("Resolved"),q.any_of(escStatus['name']),))

  if escStatus == None:
    if resolvedStatus is False:
      escStatus = app_tables.escalation_status.search(name=q.none_of("Resolved")) 
    if resolvedStatus is True:
      escStatus = app_tables.escalation_status.search() 

  related_rows = currentUser['user_merchant_link']
  values = [row for row in related_rows]
  if merchant_name is None and assigned_to is None :
    custTable = app_tables.webhook.search(tables.order_by("last_action_date", ascending=False),**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*values),latest_status=q.any_of(*escStatus))

  elif merchant_name is None and assigned_to is not None :
    custTable = app_tables.webhook.search(tables.order_by("last_action_date", ascending=False),**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*values),latest_status=q.any_of(*escStatus))

  elif merchant_name is not None and assigned_to is None :
    merchant_row = app_tables.merchant.search(name=merchant_name)
    custTable = app_tables.webhook.search(tables.order_by("last_action_date", ascending=False),**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*merchant_row),latest_status=q.any_of(*escStatus))

  else:
    merchant_row = app_tables.merchant.search(name=merchant_name)
    custTable = app_tables.webhook.search(tables.order_by("last_action_date", ascending=False),**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*merchant_row),latest_status=q.any_of(*escStatus))

  if searchText:
    custTable = [
      x for x in custTable
        if searchText.lower() in x['job_id'].lower()
        or searchText.lower() in x['job_reference'].lower()
        or searchText.lower() in x['customer_name'].lower()
        or x['mobile_number'] is not None and searchText.lower() in x['mobile_number'].lower() 
        or x['sub_brand'] is not None and searchText.lower() in x['sub_brand'].lower() 
        or x['job_reference2'] is not None and searchText.lower() in x['job_reference2'].lower() 
        or x['job_reference3'] is not None and searchText.lower() in x['job_reference3'].lower()
    ]
    
#  app_tables.merchant.search(name=q.all_of(*currentUser['user_merchant_link']))
  #print(*currentUser['user_merchant_link'])
  #if filters.get('job_status') and filters['job_status'] == Data.NO_STATUS_SELECTED:
  #  filters['job_status'] = None
  # Get a list of escalation from the Data Table, sorted by 'date_created' column, in descending order
  
 #custTable = app_tables.webhook.search(job_status=jobValue,completion_code_id=compCode,escalation_type=escType,latest_status=escStatus,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*values))
  return custTable

@anvil.server.callable
def get_action(rowValue):
  # Get a list of articles from the Data Table, sorted by 'created' column, in descending order
  if rowValue is None: 
    print("No Escalation Selected")
  else:
    return app_tables.action_log.search(tables.order_by("created_date",ascending=False),escalation_id=q.any_of(rowValue)
  )

@anvil.server.callable
def get_selectedMerchant(selectedMerchant):
  related_rows = selectedMerchant
  values = [row for row in related_rows] 
  if selectedMerchant is None:
    print("No Escalation Selected")
  else:
    xMerch = app_tables.users.search(user_merchant_link=[related_rows])
    values = [[row] for row in xMerch]
    x_list =[r['name'] for r in xMerch]
    x_list.sort()
    return x_list

@anvil.server.callable
def add_comment(article, article_dict, description, status, created_date, assign_to,submitter):
  if app_tables.webhook.has_row(article):
   article_dict['last_action_date'] = created_date
   article_dict['latest_status'] = status
   assignrow = app_tables.users.get(name=assign_to)
   article_dict['latest_assignee'] = assignrow
   tx = article['job_id']
   row = app_tables.action_log.add_row(
    job_id=article,
    user= submitter ,
    description=description,
    status=status,
    created_date = created_date,
    assign_to=assignrow,
    escalation_id=article)
   article.update(**article_dict)
  else:
   raise Exception("Article does not exist")

@anvil.server.callable
def new(job, jobref, customer, mobile, merchant_name, subbrand, description, esc_status, esc_type, date_created, last_action_date, assign_to):
  merchant_row = app_tables.merchant.get(name=merchant_name) 
  status_row = app_tables.job_status.get(name='Failed') 
  counter = get_next_value_in_sequence()
  row = app_tables.webhook.add_row(
     job_id = job,
     job_reference = jobref,
     customer_name = customer,
     mobile_number = mobile,
     webhook_merchant_link = merchant_row,
     sub_brand = subbrand,
     id = str(counter),
     latest_status = esc_status,
     job_status = status_row,
     completion_code_description = esc_type,
     date_created = date_created,
     last_action_date = last_action_date,
     latest_assignee=assign_to,
   )
  jobrow = app_tables.webhook.get(id=str(counter)) 
  jr_dict = dict(jobrow)
  assignname = assign_to['name']
  app_tables.action_log.add_row(
        assign_to=None,
        user=anvil.users.get_user(),
        description="created manually",
        escalation_id=app_tables.webhook.get(id= str(counter)),
        job_id=app_tables.webhook.get(id= str(counter)),
        status = app_tables.escalation_status.get(name= "New"),
        created_date=datetime.now())  

"""
@anvil.server.callable
def import_excel_data(file):
  with open(file, "rb") as f:
    df = pd.read_excel(f)
    for d in df.to_dict(orient="records"):
      # d is now a dict of {columnname -> value} for this row 
      # We use Python's **kwargs syntax to pass the whole dict as 
      # keyword arguments 
      app_tables.test_table.add_row(**d)

import_excel_data("anvil_upload.xlsx")
"""

@anvil.server.callable
def update_item(article,user):
  if article['watchlistUsers'] is None:
    article['watchlistUsers'] = [user]
  elif anvil.users.get_user() in article['watchlistUsers']:
    article['watchlistUsers'] = [r for r in article['watchlistUsers'] if r != user]
  else: 
    article['watchlistUsers'] += [user] 

@tables.in_transaction
def get_next_value_in_sequence():
  row = int(app_tables.webhook.search(tables.order_by("date_created", ascending=False))[0]['id'])
  row += 1
  return row

@anvil.server.callable
def manual_import(file):
  with anvil.media.TempFile(file) as file_name:
    if file.content_type == 'text/csv':
      df = pd.read_csv(file_name)
    else:
      df = pd.read_excel(file_name)

    app_tables.import_test.delete_all_rows()
    df = df.replace({pd.np.nan: None})
    df = df.drop(['external_job_id', 'manager_name', 'manager_email', 'manager_phone','driver_phone','total_job_time', 'time_at_job', 'time_inside_geofence', 'geofence_entered_at','pickup_address', 'pickup_address_2', 'pickup_name', 'pickup_email', 'pickup_phone', 'pickup_before_date', 'pickup_geofence_entered_at', 'time_at_pickup', 'pickup_after_date'], axis=1)
    compdf =df
    counter = get_next_value_in_sequence()
    df= df.loc[df['customer_rating'].isin([1,2,3])]
    df['completed_at'] = pd.to_datetime(df['completed_at'])
    for d in df.to_dict(orient="records"):
      app_tables.webhook.add_row(
        job_id = str(d['order_id']),
      id= str(counter),
      customer_name = d['customer_name'],
      completion_code_id =str(d['completion_codes']),
      date_created = datetime.now(),
      last_action_date =datetime.now(),
      job_reference = d['order_title'],
      webhook_merchant_link=app_tables.merchant.get(merchant_id= "124"),
      job_status = app_tables.job_status.get(sysName= d['order_status']),
      job_report = d['full_report_url'],
      customer_rating= str(d['customer_rating']),
      escalation_type = app_tables.escalation_type.get(name= "Low Rating"),
      latest_assignee = None,
      latest_status = app_tables.escalation_status.get(name= "New"),
      sub_brand=d['subbrand_name'],
      mobile_number=str(d['customer_phone']),
      date_delivered=d['completed_at'],
      job_reference2=d['order_title_2'],
      job_reference3=d['order_title_3'],
      address=d['deliver_address'],
      watch_list=False)
      app_tables.action_log.add_row(
        assign_to=None,
        user=anvil.users.get_user(),
        description="created manually",
        escalation_id=app_tables.webhook.get(id= str(counter)),
        job_id=app_tables.webhook.get(id= str(counter)),
        status = app_tables.escalation_status.get(name= "New"),
        created_date=datetime.now())
      counter += 1

    counter = get_next_value_in_sequence()
    #compdf = compdf.
    compdf2 = compdf
    compdf= compdf.loc[compdf['completion_codes'].str.contains("501",na=False)]
    compdf['completed_at'] = pd.to_datetime(compdf['completed_at'])
    for d in compdf.to_dict(orient="records"):
      app_tables.webhook.add_row(
        job_id = str(d['order_id']),
      id= str(counter),
      customer_name = d['customer_name'],
      completion_code_id =str(d['completion_codes']),
      date_created = datetime.now(),
      last_action_date =datetime.now(),
      job_reference = d['order_title'],
      webhook_merchant_link=app_tables.merchant.get(merchant_id= "124"),
      job_status = app_tables.job_status.get(sysName= d['order_status']),
      job_report = d['full_report_url'],
      customer_rating= str(d['customer_rating']),
      escalation_type = app_tables.escalation_type.get(name= "Customer Not Home"),
      latest_assignee = None,
      latest_status = app_tables.escalation_status.get(name= "New"),
      sub_brand=d['subbrand_name'],
      mobile_number=str(d['customer_phone']),
      date_delivered=d['completed_at'],
      job_reference2=d['order_title_2'],
      job_reference3=d['order_title_3'],
      address=d['deliver_address'],
      watch_list=False)
      app_tables.action_log.add_row(
        assign_to=None,
        user=anvil.users.get_user(),
        description="created manually",
        escalation_id=app_tables.webhook.get(id= str(counter)),
        job_id=app_tables.webhook.get(id= str(counter)),
        status = app_tables.escalation_status.get(name= "New"),
        created_date=datetime.now())
      counter += 1

    counter = get_next_value_in_sequence()
    compdf3 = compdf2
    compdf2= compdf2.loc[compdf2['completion_codes'].str.contains("502",na=False)]
    compdf2['completed_at'] = pd.to_datetime(compdf2['completed_at'])
    for d in compdf2.to_dict(orient="records"):
      app_tables.webhook.add_row(
        job_id = str(d['order_id']),
      id= str(counter),
      customer_name = d['customer_name'],
      completion_code_id =str(d['completion_codes']),
      date_created = datetime.now(),
      last_action_date =datetime.now(),
      job_reference = d['order_title'],
      webhook_merchant_link=app_tables.merchant.get(merchant_id= "124"),
      job_status = app_tables.job_status.get(sysName= d['order_status']),
      job_report = d['full_report_url'],
      customer_rating= str(d['customer_rating']),
      escalation_type = app_tables.escalation_type.get(name= "Customer Rejected Goods"),
      latest_assignee = None,
      latest_status = app_tables.escalation_status.get(name= "New"),
      sub_brand=d['subbrand_name'],
      mobile_number=str(d['customer_phone']),
      date_delivered=d['completed_at'],
      job_reference2=d['order_title_2'],
      job_reference3=d['order_title_3'],
      address=d['deliver_address'],
      watch_list=False)
      app_tables.action_log.add_row(
        assign_to=None,
        user=anvil.users.get_user(),
        description="created manually",
        escalation_id=app_tables.webhook.get(id= str(counter)),
        job_id=app_tables.webhook.get(id= str(counter)),
        status = app_tables.escalation_status.get(name= "New"),
        created_date=datetime.now())
      counter += 1
      
    counter = get_next_value_in_sequence()
    compdf3= compdf3.loc[compdf3['completion_codes'].str.contains("202",na=False)]
    compdf3['completed_at'] = pd.to_datetime(compdf3['completed_at'])
    for d in compdf3.to_dict(orient="records"):
      app_tables.webhook.add_row(
        job_id = str(d['order_id']),
      id= str(counter),
      customer_name = d['customer_name'],
      completion_code_id =str(d['completion_codes']),
      date_created = datetime.now(),
      last_action_date =datetime.now(),
      job_reference = d['order_title'],
      webhook_merchant_link=app_tables.merchant.get(merchant_id= "124"),
      job_status = app_tables.job_status.get(sysName= d['order_status']),
      job_report = d['full_report_url'],
      customer_rating= str(d['customer_rating']),
      escalation_type = app_tables.escalation_type.get(name= "Up-Sell Service Opportunity"),
      latest_assignee = None,
      latest_status = app_tables.escalation_status.get(name= "New"),
      sub_brand=d['subbrand_name'],
      mobile_number=str(d['customer_phone']),
      date_delivered=d['completed_at'],
      job_reference2=d['order_title_2'],
      job_reference3=d['order_title_3'],
      address=d['deliver_address'],
      watch_list=False)
      app_tables.action_log.add_row(
        assign_to=None,
        user=anvil.users.get_user(),
        description="created manually",
        escalation_id=app_tables.webhook.get(id= str(counter)),
        job_id=app_tables.webhook.get(id= str(counter)),
        status = app_tables.escalation_status.get(name= "New"),
        created_date=datetime.now())
      counter += 1

@anvil.server.callable
def get_record(id):
  if id is None: 
    print("No Record")
  else:
    return app_tables.webhook.get(id=q.any_of(id))

@anvil.server.callable
def chart_user(currentUser):
    #response by user
    #https://plotly.com/python/reference/layout/#layout-paper_bgcolor
    related_rows = currentUser['user_merchant_link']
    values = [row for row in related_rows]
    escalations = app_tables.webhook.search(webhook_merchant_link=q.any_of(*values))
    data = [{"User": r["user"]["name"], "Status": r["status"], "Created Date": r["created_date"]} for r in app_tables.action_log.search(escalation_id=q.any_of(*escalations))]
    df = pd.DataFrame(data)
    df1 = df.loc[df["User"] !='System' ]
    #https://sparkbyexamples.com/pandas/pandas-groupby-multiple-columns/
    grouped_df = df1.groupby(['User']).agg(
    Count=pd.NamedAgg(column='User', aggfunc='count')
    ).reset_index()
    grouped_df.columns = ['User', 'count']
    sorted_df = grouped_df.sort_values(by='count', ascending=True)
    sorted_df.reset_index(inplace=True)
    ch_user = px.bar(sorted_df, x='count', y='User', orientation='h', text ='count')
    ch_user.update_layout(font=dict(family="Arial",color="black"),
                        margin=dict(l=20, r=20, t=10, b=20),
                        plot_bgcolor="white",
                        xaxis_title=None, yaxis_title=None
                        )
    ch_user.update_traces(marker_color='rgb(18,35,158)', opacity=0.9, textangle=0,
                        hovertemplate=
                        "<b>%{y}</b><br>" +
                        "Responses : %{x}<br>" +
                        "<extra></extra>")
    ch_user.update_xaxes(showline=True, linewidth=1, linecolor='black')
    ch_user.update_yaxes(showline=True, linewidth=1, linecolor='black',
                      showticklabels=True,ticks="outside",tickson="boundaries",
                      ticklen=5,tickangle=0,tickfont=dict(family='Arial', color='black', size=12))
    return ch_user

@anvil.server.callable
def create_chart4(currentUser):
    #testing animation
    related_rows = currentUser['user_merchant_link']
    values = [row for row in related_rows]
    data = [{"User": r["user"]["name"], "status": r["status"], "Created Date": r["created_date"]} for r in app_tables.action_log.search(webhook_merchant_link=q.any_of(*values))]
    df = pd.DataFrame(data)
    count_df = df['User'].value_counts().reset_index()
    count_df.columns = ['User', 'count']
    count_df = count_df.sort_values(by="count")
    # Create the initial bar chart
    fig, ax = plt.subplots()
    x = count_df['count']
    y = count_df['User']
    bars = plt.barh(x, y, color='blue')
#bars = animate()
    ani = animation.FuncAnimation(fig, animate, fargs=(bars, x, ax), interval=100)

    return anvil.mpl_util.plot_image()

def animate(i, b, x, ax):
    for bar, height in zip(b, x[:i]):
        bar.set_width(height)
    ax.relim()
    ax.autoscale_view()
    return b

# Display the animated chart (you may need to save it or display it in a Jupyter Notebook)


@anvil.server.callable
def highlights(today,currentUser):
    #New tickets last 7 days with delta and % Resolved
    related_rows = currentUser['user_merchant_link']
    values = [row for row in related_rows]
    data = [{"Status": r["latest_status"]["name"], "Datetime Created": r["date_created"], "Date Created": r["date_created"].date(),
             "last_action_date": r["last_action_date"].date(),"last_action_datetime": r["last_action_date"]}
             for r in app_tables.webhook.search(webhook_merchant_link=q.any_of(*values))]
    df = pd.DataFrame(data)
    today = today
    Resolved = 'Resolved'
    days_until_sunday = (today.weekday() - 6) % 7  # Calculate the number of days until the next Sunday
    end_date_last_week = today - timedelta(days=days_until_sunday)
    start_date_last_week = end_date_last_week - timedelta(days=6)
    end_date_prior_week = end_date_last_week - timedelta(days=7)
    start_date_prior_week = start_date_last_week - timedelta(days=7)
    filtered_df_last_week = df[(df['Date Created'] >= start_date_last_week) & (df['Date Created'] <= end_date_last_week)]
    last_week = len(filtered_df_last_week)
    filtered_df_prior_week = df[(df['Date Created'] >= start_date_prior_week) & (df['Date Created'] <= end_date_prior_week)]
    prior_week = len(filtered_df_prior_week)  
    delta = last_week - prior_week
  
    last_week_df_resolved = filtered_df_last_week[filtered_df_last_week['Status'] == 'Resolved']
    last_week_resolved = len(last_week_df_resolved)
    last_week_per = round(last_week_resolved / last_week *100 ,1)
    prior_week_df_resolved = filtered_df_prior_week[filtered_df_prior_week['Status'] == 'Resolved']
    prior_week_resolved = len(prior_week_df_resolved)
    prior_week_per = round(prior_week_resolved / prior_week *100 ,1)
    delta2 = round(last_week_per - prior_week_per,1)

    df['resolve_time'] = (df['last_action_datetime'] - df['Datetime Created']) / pd.to_timedelta(1, unit='D')
    resolved_df_last_week = df[(df['last_action_date'] >= start_date_last_week) & (df['last_action_date'] <= end_date_last_week) & (df['Status'] == 'Resolved')]
    resolved = len(resolved_df_last_week)
    resolved_df_prior_week = df[(df['last_action_date'] >= start_date_prior_week) & (df['last_action_date'] <= end_date_prior_week) & (df['Status'] == 'Resolved')]
    prior_resolved = len(resolved_df_prior_week)
    delta3 = resolved - prior_resolved
    ave_resolve_time_lw = round(resolved_df_last_week['resolve_time'].mean(),1)
    ave_resolve_time_pw = round(resolved_df_prior_week['resolve_time'].mean(),1)
    delta4 = round(ave_resolve_time_lw - ave_resolve_time_pw,1)

    return last_week, delta, last_week_per, delta2, resolved, delta3, start_date_last_week, end_date_last_week, ave_resolve_time_lw, delta4


@anvil.server.callable
def all_charts(today,currentUser):
    #pie chart last week and bar chart last week vs this week
    related_rows = currentUser['user_merchant_link']
    values = [row for row in related_rows]
    data = [{"Escalation Type": r["completion_code_description"].capitalize(), "last_action_date": r["last_action_date"],
             "Status": r["latest_status"]["name"], "Date Created": r["date_created"].date(),"Datetime Created": r["date_created"],
            } for r in app_tables.webhook.search(webhook_merchant_link=q.any_of(*values))]
    df = pd.DataFrame(data)
    today = today
    days_until_sunday = (today.weekday() - 6) % 7  # Calculate the number of days until the next Sunday
    end_date = today - timedelta(days=days_until_sunday)
    start_date = end_date - timedelta(days=6)
    filtered_df = df[(df['Date Created'] >= start_date) & (df['Date Created'] <= end_date)]
    grouped_df = filtered_df.groupby('Status').agg(
    Count=pd.NamedAgg(column='Date Created', aggfunc='count')
    ).reset_index()
    grouped_df.columns = ['Status', 'count']
    sorted_df = grouped_df.sort_values(by='Status', ascending=True)
    sorted_df.reset_index(inplace=True)
    pie = px.pie(sorted_df,values ='count', names ='Status', hole = 0.55,color='Status',
                   category_orders={"Status": ["New", "Active", "Pending Approval", "Approved",'Resolved']},
                   color_discrete_map={'New':'rgb(161,52,60)','Active':'rgb(11,180,87)','Pending Approval':'rgb(153,153,0)','Approved':'rgb(153,153,153)','Resolved':'rgb(18,35,158)'})
    pie.update_traces(textinfo='label+value', insidetextorientation='horizontal', pull=0.00,hoverinfo='label+value+percent',
                        hovertemplate=
                        "<b>%{label}</b><br>" +
                        "Tickets : %{value}<br>" +
                        "<extra></extra>")
    pie.update_layout(font=dict(family="Arial",color="black"),
                        showlegend=False,
                        margin=dict(l=10, r=10, t=10, b=10),
                        plot_bgcolor="white")
    #bar chart last week vs this week
    df['Date Created2'] = pd.to_datetime(df['Date Created'], utc=True)
    df['Day'] = df['Date Created2'].dt.day_name().str[:3]
    custom_sort_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df['Day'] = pd.Categorical(df['Day'], categories=custom_sort_order, ordered=True)
    days_until_sunday = (today.weekday() - 6) % 7  # Calculate the number of days until the next Sunday
    end_date_last_week = today - timedelta(days=days_until_sunday)
    start_date_last_week = end_date_last_week - timedelta(days=6)
    end_date_this_week = end_date_last_week + timedelta(days=7)
    start_date_this_week = start_date_last_week + timedelta(days=7)
    filtered_df_last_week = df[(df['Date Created'] >= start_date_last_week) & (df['Date Created'] <= end_date_last_week)]
    filtered_df_last_week['Week'] = 'Last Week'
    filtered_df_this_week = df[(df['Date Created'] >= start_date_this_week) & (df['Date Created'] <= end_date_this_week)]
    filtered_df_this_week['Week'] = 'This Week'  
    filtered_df_last_week.reset_index(drop=True, inplace=True)
    filtered_df_this_week.reset_index(drop=True, inplace=True)  
    concatenated_df = pd.concat([filtered_df_last_week, filtered_df_this_week])
    grouped_df = concatenated_df.groupby(['Week', 'Day']).agg(
    Count=pd.NamedAgg(column='Date Created', aggfunc='count')
    ).reset_index()
    trace_this_week = go.Bar(
    x=grouped_df[grouped_df['Week'] == 'This Week']['Day'],
    y=grouped_df[grouped_df['Week'] == 'This Week']['Count'],
    name='This Week', marker_color='rgb(11,180,87)',texttemplate='%{y}'
    )
    trace_last_week = go.Bar(
    x=grouped_df[grouped_df['Week'] == 'Last Week']['Day'],
    y=grouped_df[grouped_df['Week'] == 'Last Week']['Count'],
    name='Last Week', marker_color='rgb(161,52,60)',texttemplate='%{y}'
    )
    chart = go.Figure(data=[trace_this_week, trace_last_week])
    chart.update_layout(font=dict(family="Arial",color="black"),
                        showlegend=True, hovermode='closest',
                        margin=dict(l=10, r=10, t=10, b=10),
                        xaxis_title=None, yaxis_title=None,
                        plot_bgcolor="white")
    chart.update_yaxes(showticklabels=False)
    #chart.update_traces(hovertemplate=
    #                    "%{Week}<br>" +
    #                    "Tickets : %{x}<br>" +
    #                    "<extra></extra>")
    chart.update_xaxes(showline=True, linewidth=1, linecolor='black',tickcolor='black',
                       showticklabels=True,ticks="outside",tickson="boundaries",
                       ticklen=5,tickangle=0,tickfont=dict(family='Arial', color='black', size=12))

    #tickets by current status
    grouped_df = df.groupby('Status').agg(
    Count=pd.NamedAgg(column='Date Created', aggfunc='count')
    ).reset_index()
    grouped_df.columns = ['Status', 'count']
    sorted_df = grouped_df.sort_values(by='count', ascending=True)
    sorted_df.reset_index(inplace=True)
    ch_status = px.bar(sorted_df, x="count", y="Status", orientation='h', color='Status', text ='count',
                   category_orders={"Status": ["New", "Active", "Pending Approval", "Approved",'Resolved']},
                   color_discrete_map={'New':'rgb(161,52,60)','Active':'rgb(11,180,87)','Pending Approval':'rgb(153,153,0)','Approved':'rgb(153,153,153)','Resolved':'rgb(18,35,158)'})
    ch_status.update_layout(font=dict(family="Arial",color="black"),
                        margin=dict(l=20, r=20, t=10, b=20),
                        showlegend=False,
                        plot_bgcolor="white",
                        xaxis_title=None, yaxis_title=None
                        )
    ch_status.update_traces(hovertemplate=
                        "<b>%{y}</b><br>" +
                        "Tickets : %{x}<br>" +
                        "<extra></extra>")
    ch_status.update_xaxes(showline=True, linewidth=1, linecolor='black')
    ch_status.update_yaxes(showline=True, linewidth=1, linecolor='black',
                      showticklabels=True,ticks="outside",tickson="boundaries",
                      ticklen=5,tickangle=0,tickfont=dict(family='Arial', color='black', size=12))

  #tickets by creation date
    grouped_df = df.groupby(['Date Created','Status']).agg(
    Count=pd.NamedAgg(column='Date Created', aggfunc='count')
    ).reset_index()
    #df['delta'] = ('Max_Created_Date' - 'Min_Created_Date') / pd.to_timedelta(1, unit='D') 
    grouped_df.columns = ['Date Created', 'Status', 'count']
    sorted_df = grouped_df.sort_values(by='Status', ascending=True)
    sorted_df.reset_index(inplace=True)
    ch_date = px.bar(sorted_df, x="Date Created", y="count", color = 'Status', text ='count',
                   category_orders={"Status": ["New", "Active", "Pending Approval", "Approved",'Resolved']},
                   color_discrete_map={'New':'rgb(161,52,60)','Active':'rgb(11,180,87)','Pending Approval':'rgb(153,153,0)','Approved':'rgb(153,153,153)','Resolved':'rgb(18,35,158)'})
    ch_date.update_layout(font=dict(family="Arial",color="black"),
                        margin=dict(l=20, r=20, t=10, b=20),
                        plot_bgcolor="white",hovermode='x',
                        xaxis_title=None, yaxis_title=None
                        )         
    ch_date.update_xaxes(showline=True, linewidth=1, linecolor='black',
                      showticklabels=True,ticks="outside",tickson="boundaries",
                      minor=dict(ticklen=3, tickcolor="black", showgrid=False),
                      ticklen=8,tickangle=0,tickfont=dict(family='Arial', color='black', size=12))
    ch_date.update_yaxes(showline=True, linewidth=1, linecolor='black')
  
    #tickets by escalation type
    df.loc[df['Escalation Type'].str.contains(';', na=False), 'Escalation Type'] = 'Multiple Escalations'
    df['delta'] = (df['last_action_date'] - df['Datetime Created']) / pd.to_timedelta(1, unit='D')
    grouped_df = df.groupby('Escalation Type').agg({'Escalation Type': 'count', 'delta': 'mean'})
    grouped_df.columns = ['count', 'average delta']
    grouped_df['average delta'] = grouped_df['average delta'].round(1)
    sorted_df = grouped_df.sort_values(by='count', ascending=True)
    sorted_df.reset_index(inplace=True)    
    ch_type = go.Figure()
    # Add a bar chart for the count
    ch_type.add_trace(go.Bar(x=sorted_df['count'], y=sorted_df['Escalation Type'], orientation='h', 
                           name='Count',marker_color='rgb(18,35,158)'))
    # Add a line chart for the average delta
    ch_type.add_trace(go.Scatter(x=sorted_df['average delta'], y=sorted_df['Escalation Type'], 
                               mode='lines+markers', name='Average Resolution time', 
                               line=dict(color='rgb(161,52,60)')
                               ))
    # Update the layout
    ch_type.update_layout(font=dict(family="Arial",color="black"),
                        margin=dict(l=20, r=20, t=10, b=20),
                        plot_bgcolor="white",hovermode='y unified',
                        xaxis_title=None, yaxis_title=None
                        )
    ch_type.update_traces(hoverinfo = 'y+x')
    ch_type.update_xaxes(showline=True, linewidth=1, linecolor='black',
                      rangemode="tozero")
    ch_type.update_yaxes(showline=True, linewidth=1, linecolor='black',
                      showticklabels=True,ticks="outside",tickson="boundaries",rangemode="tozero",
                      ticklen=5,tickangle=0,tickfont=dict(family='Arial', color='black', size=12))

    return pie,chart,ch_status,ch_date,ch_type
    #print("-----aa")
    #print(rowValue)
    #print("-----bb")
    #print(rowValue['job_status'])
    return app_tables.webhook.get(id=q.any_of(id))

@anvil.server.callable
def sync_subbrand(record):
  #print(record['APIToken'])
  if record['server'] == '1':
    apiServer = ""
  else:
    apiServer = "-" + record['server']

  print(apiServer)
  if record['APIToken'] is not None:
    response = requests.get('https://api'+apiServer+'.radaro.com.au/api/webhooks/sub-brands/?key='+record['APIToken'])
    data = response.json()
    try:
      for result in data['results']:
            # Check if a record with the same MerchantID and ID exists
          existing_record = app_tables.subbrands.get(MerchantID=str(result['merchant']), ID=str(result['id']),Server=record['server'])
            
          if existing_record:
                # Update existing record
              existing_record.update(Logo=result['logo'], Name=result['name'],LastUpdated=datetime.now())
          else:
                # Insert new record
              app_tables.subbrands.add_row(MerchantID=str(result['merchant']), ID=str(result['id']), Logo=result['logo'], Name=result['name'],Server=record['server'],LastUpdated=datetime.now(),MerchantLink=record)
    except:
      print("API Request Failed")
  else:
    print("No API Token on record")

@anvil.server.callable
def sync_compCodes(record):
  #print(record['APIToken'])
  if record['server'] == '1':
    apiServer = ""
  else:
    apiServer = "-" + record['server']

  print(apiServer)
  if record['APIToken'] is not None:
    response = requests.get('https://api'+apiServer+'.radaro.com.au/api/webhooks/completion-codes/?key='+record['APIToken'])
    data = response.json()
    try:
      for result in data['results']:
            # Check if a record with the same MerchantID and ID exists
          existing_record = app_tables.compCodes.get(MerchantID=str(result['merchant']), ID=str(result['id']),Server=record['server'])
            
          if existing_record:
                # Update existing record
              existing_record.update(Name=result['name'],LastUpdated=datetime.now())
          else:
                # Insert new record
              app_tables.compCodes.add_row(MerchantID=str(result['merchant']), ID=str(result['id']), Name=result['name'],Server=record['server'],LastUpdated=datetime.now(),MerchantLink=record)
    except:
      print("API Request Failed")
  else:
    print("No API Token on record")