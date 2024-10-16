import anvil.email
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
from fpdf import FPDF
from anvil.pdf import PDFRenderer


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
  try:
    lowrate_enable = merctable['low_rating_enabled'] 
    compcode_enable = merctable['completion_code_enabled'] // succession
    failcode_enable = merctable['fail_code_enabled'] // failed
    jobchecklist_enable = merctable['job_checklist_enabled'] // job checklist

    if 'new_values' in data :
      if data['new_values'] is not None and 'is_confirmed_by_customer' in data['new_values'] and lowrate_enable == True:
        if merctable is not None:
        
          if 'job.status_changed' in topic and 'updated' in data.get('event_type') and True == data['new_values']['is_confirmed_by_customer'] and merctable['rating_threshold'] >= data['order_info']['rating'] :
            #print("low rating")
            submit_low_rating(data)
  
      if 'job.completion_codes_accepted' in topic and 'updated' in data.get('event_type'):
        if 'delivered'==data['order_info']['status'] and compcode_enable == True:
            submit_completion_codes(data) 
        elif failcode_enable == True and 'failed'==data['order_info']['status']:
            #print("fail code")
            submit_completion_codes(data) 
      else:
          pass 
  
    if 'checklist.job_checklist_confirmation' in topic and jobchecklist_enable == True:
      checklist =  data.get('result_checklist_info', {}).get('checklist', {})
      questions = checklist.get('questions', [])
  
      for question in questions:
          correct_answer = question.get('correct_answer')
          given_answer = question.get('answer', {}).get('choice')
          # Check if the given answer does not match the correct answer
          if given_answer != correct_answer:
              # Code to insert the payload into an Anvil Data Table
              submit_failed_checklist(data)
              # Break after the first mismatch, or remove the break if you want to store all mismatches
              break
  except Exception as error: 
    #print(data['token'])
    print(merctable['name']) 
    print(error)          


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
def submit_failed_checklist(data):
  codes=data['order_info']['completion_codes']
  id_values = [str(code["code"]) for code in codes]
  id_string = ";".join(id_values)
  comp_names = [str(code["name"]) for code in codes]
  comp_string = ";".join(comp_names)
  updated_at = data.get('updated_at')
  merctable = app_tables.merchant.get(token=data['token'])

  if data['order_info']['sub_branding'] is not None:
        subbrandval = str(data['order_info']['sub_branding'])
  else:
        subbrandval = str(merctable['server']+str(data['order_info']['merchant'])+'00001')   
  existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=subbrandval, Server=merctable['server'], MerchantLink=merctable)
  if existing_record is None:
        sync_subbrand(merctable)
        existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=subbrandval, Server=merctable['server'], MerchantLink=merctable)
        if existing_record is None:
           existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=merctable['server']+str(data['order_info']['merchant'])+'00000', Server=merctable['server'], MerchantLink=merctable)

    #existing_record = app_tables.subbrands.get(Name="(Blank)")
    # comp_string = None
  sync_compCodes(merctable)  
  nv = data['order_info']['is_confirmed_by_customer']
  rating = data['order_info']['rating']
  counter = get_next_value_in_sequence()
  
  if data['order_info']['completed_at'] is None:
    completedAtVal = None
  else: 
    completedAtVal = datetime.strptime(data['order_info']['completed_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
  #try:
  app_tables.webhook.add_row(
  job_id = str(data['order_info']['order_id']),
  id= str(counter),
  customer_name = data['order_info']['customer']['name'],
  completion_code_id = id_string,
  completion_code_description = "Failed Job Checklist", 
  date_created = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%f%z"),
  last_action_date =datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%f%z"),
  job_reference = data['order_info']['title'],
  webhook_merchant_link=app_tables.merchant.get(token=data['token']),
  webhook_subbrand_link=existing_record,
  job_status = app_tables.job_status.get(sysName=data['order_info']['status']),
  job_report = data['order_info']['public_report_link'],
  customer_rating= str(rating),
  #escalation_type = "Low Rating",
  latest_assignee = None,
  latest_status = app_tables.escalation_status.get(name= "New"),
  sub_brand= existing_record['Name'],
  mobile_number=data['order_info']['customer']['phone'],
  date_delivered=completedAtVal, 
  job_reference2=data['order_info']['title_2'],
  job_reference3=data['order_info']['title_3'],
  comment=data['order_info']['comment'],
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
def submit_low_rating(data):
  codes=data['order_info']['completion_codes']
  id_values = [str(code["code"]) for code in codes]
  id_string = ";".join(id_values)
  comp_names = [str(code["name"]) for code in codes]
  comp_string = ";".join(comp_names)
  updated_at = data.get('updated_at')
  merctable = app_tables.merchant.get(token=data['token'])

  if data['order_info']['sub_branding'] is not None:
        subbrandval = str(data['order_info']['sub_branding'])
  else:
        subbrandval = str(merctable['server']+str(data['order_info']['merchant'])+'00001')   
  existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=subbrandval, Server=merctable['server'], MerchantLink=merctable)
  if existing_record is None:
        sync_subbrand(merctable)
        existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=subbrandval, Server=merctable['server'], MerchantLink=merctable)
        if existing_record is None:
           existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=merctable['server']+str(data['order_info']['merchant'])+'00000', Server=merctable['server'], MerchantLink=merctable)

    #existing_record = app_tables.subbrands.get(Name="(Blank)")
    # comp_string = None
  sync_compCodes(merctable)  
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
  webhook_subbrand_link=existing_record,
  job_status = app_tables.job_status.get(sysName=data['order_info']['status']),
  job_report = data['order_info']['public_report_link'],
  customer_rating= str(rating),
  #escalation_type = "Low Rating",
  latest_assignee = None,
  latest_status = app_tables.escalation_status.get(name= "New"),
  sub_brand= existing_record['Name'], 
  mobile_number=data['order_info']['customer']['phone'],
  date_delivered=datetime.strptime(data['order_info']['completed_at'], "%Y-%m-%dT%H:%M:%S.%f%z"), 
  job_reference2=data['order_info']['title_2'],
  job_reference3=data['order_info']['title_3'],
  comment=data['order_info']['customer_comment'],
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
  merctable = app_tables.merchant.get(token=data['token'])
  
  if data['order_info']['sub_branding'] is not None:
        subbrandval = str(data['order_info']['sub_branding'])
  else:
        subbrandval = str(merctable['server']+str(data['order_info']['merchant'])+'00001')   
  existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=subbrandval, Server=merctable['server'], MerchantLink=merctable)
  if existing_record is None:
        sync_subbrand(merctable)
        existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=subbrandval, Server=merctable['server'], MerchantLink=merctable)
        if existing_record is None:
           existing_record = app_tables.subbrands.get(MerchantID=str(data['order_info']['merchant']), ID=merctable['server']+str(data['order_info']['merchant'])+'00000', Server=merctable['server'], MerchantLink=merctable)

    #existing_record = app_tables.subbrands.get(Name="(Blank)")
  
  submission_made = False
  sync_compCodes(merctable)
  codeChecks = id_string.split(';')
  for codeCheck in codeChecks:
    print("Code:" + codeCheck)
    #print(data['order_info']['merchant'])
    print(merctable['server'])
    category = app_tables.compcodes.get(ID=codeCheck,MerchantID=str(data['order_info']['merchant']),Server=merctable['server'])
    print(category)
    print(category['is_enabled'])
    if submission_made:
            break
    if category and category['is_enabled']:
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
      webhook_subbrand_link=existing_record,
      job_status = app_tables.job_status.get(sysName=data['order_info']['status']),
      job_report = data['order_info']['public_report_link'],
      customer_rating= str(rating),
      #escalation_type = "Low Rating",
      latest_assignee = None,
      latest_status = app_tables.escalation_status.get(name= "New"),
      sub_brand=existing_record['Name'],
      mobile_number=data['order_info']['customer']['phone'],
      date_delivered=datetime.strptime(data['order_info']['completed_at'], "%Y-%m-%dT%H:%M:%S.%f%z"), 
      job_reference2=data['order_info']['title_2'],
      job_reference3=data['order_info']['title_3'],
      #comment=data['order_info']['comment'],
      comment = data['order_info'].get('error_comment', data['order_info'].get('completion_comment', 'Default comment')),
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
      submission_made = True
  

@anvil.server.callable
def get_merchant_list(currentUser):
  #currentUser=anvil.users.get_user()
  #Xvalues = []
  x_rows = currentUser['user_merchant_link']
  x_list =[r['name'] for r in x_rows]
  #sbValues =[[row] for row in x_rows]
  #SBrecords = app_tables.subbrands.search(MerchantLink=q.any_of(*x_rows))
  #print(*SBrecords)
 # print(x_list)
  x_list.sort()
  return x_list

#@anvil.server.callable
#def get_subbrand_list(currentUser):
  #currentUser=Data.currentUser
  #sbvalues = app_tables.subbrands.search(merchant_link=q.any_of(*values))
  #Xvalues = []
#  print('subbrand step1)'+str(datetime.now()))##################
#  x_rows = currentUser['user_merchant_link']
#  if currentUser.get('user_subbrand_link'):
#    x_rows = currentUser['user_subbrand_link']
#    x_list =[r['name'] for r in x_rows]
#  else:
#    print('subbrand step2)'+str(datetime.now()))##################
  #x_list =[r['name'] for r in x_rows]
  #sbValues =[[row] for row in x_rows]
#    SBrecords = app_tables.subbrands.search(q.any_of(MerchantLink=q.any_of(*x_rows),ID=q.any_of(*['00000000','00000001'])))
#    print('subbrand step3)'+str(datetime.now()))##################
#    x_list =[r['Name'] for r in SBrecords]
#    print('subbrand step4)'+str(datetime.now()))##################
  #print(SBrecords)
  #print(x_list)
#  x_list.sort()
#  return x_list

#@anvil.server.callable
#def get_compCodes_list(currentUser):
  
  #sbvalues = app_tables.subbrands.search(merchant_link=q.any_of(*values))
  #Xvalues = []
#  x_rows = currentUser['user_merchant_link']
  #x_list =[r['name'] for r in x_rows]
  #sbValues =[[row] for row in x_rows]
#  CCrecords = app_tables.compcodes.search(q.any_of(merchantLink=q.any_of(*x_rows),ID=q.any_of(*['00000000','00000001','00000002'])))
#  x_list =[r['Name'] for r in CCrecords]
  #print(SBrecords)
  #print(x_list)
#  x_list.sort()
#  return x_list

#@anvil.server.callable
#def get_user_list(currentUser):
  #currentUser=anvil.users.get_user()
#  related_rows = currentUser['user_merchant_link']
 # print(related_rows)
#  values = [[row] for row in related_rows]
  #print(values)
  
  #rows = list(dict(r) for r in related_rows)
  #print(rows)
  #return app_tables.users.search(user_merchant_link=q.any_of(*values))
#  return app_tables.users.search(tables.order_by("name", ascending=True),user_merchant_link=q.any_of(*values))

@anvil.server.callable
def get_filter_value():
  print('filter-getuser start)'+str(datetime.now()))##################
  currentUser=anvil.users.get_user()
  print('filter-getuser end)'+str(datetime.now()))##################
  #get_user_list
  print('filter-userlist start)'+str(datetime.now()))##################
  x_rows = currentUser['user_merchant_link']
  values = [[row] for row in x_rows]
  user_list = app_tables.users.search(tables.order_by("name", ascending=True),user_merchant_link=q.any_of(*values))
  print('filter-userlist end)'+str(datetime.now()))##################
  ##
  #get_comp_list
  print('filter-complist start)'+str(datetime.now()))##################
  CCrecords = app_tables.compcodes.search(q.any_of(merchantLink=q.any_of(*x_rows),ID=q.any_of(*['00000000','00000001','00000002'])))
  cc_list =[r['Name'] for r in CCrecords]
  cc_list = list(set(cc_list))
  cc_list.sort()
  print('filter-complist end)'+str(datetime.now()))##################
  ##
  ##get_subbrands_list
  print('filter-sblist start)'+str(datetime.now()))##################
  
  # Fetch merchant and subbrand values separately
  merchant_links = currentUser.get('user_merchant_link', [])
  subbrand_links = currentUser.get('user_subbrand_link', []) or []
  
  merchant_subbrands = {}
  
  for merchant in merchant_links:
      # Check if the current merchant has any specific subbrand links
      linked_subbrands = [sb for sb in subbrand_links if sb['MerchantLink'] == merchant]
  
      if not linked_subbrands:
          # If no specific subbrand links, show all subbrands for this merchant
          all_subbrands = list(app_tables.subbrands.search(MerchantLink=merchant))
          merchant_subbrands[merchant] = all_subbrands
      else:
          # Only show the linked subbrands for this merchant
          merchant_subbrands[merchant] = linked_subbrands
  
  # Generate dropdown items from the organized subbrands
  dropdown_items = []
  for merchant, subbrands in merchant_subbrands.items():
      for subbrand in subbrands:
          # Display subbrands with the merchant's name to clarify the association
          dropdown_item = (f"{subbrand['Name']} - {merchant['name']}", subbrand)
          dropdown_items.append(dropdown_item)
  
  # Sort the dropdown items by the subbrand name for better user experience
  dropdown_items.sort(key=lambda item: item[0])

  
  # Debugging to check the final list of dropdown items
  #print("Dropdown items:")
  #for item in dropdown_items:
  #    print(item[0])
    
  print('filter-sblist end)'+str(datetime.now()))##################
  ##
  ##get_merchant_list
  print('filter-merchlist start)'+str(datetime.now()))##################
  m_list =[r['name'] for r in x_rows]
  m_list.sort()
  print('filter-merchlist end)'+str(datetime.now()))##################

  return user_list,cc_list,dropdown_items,m_list

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
def get_list(jobValue, compCode, escType, escStatus, startDate, endDate, merchant_name, assigned_to, searchText, resolvedStatus, watch):
    currentUser = anvil.users.get_user()

    filter_dict = {}
    if assigned_to is not None:
        defaultassign = app_tables.users.get(name=assigned_to['name'])
        filter_dict['latest_assignee'] = defaultassign

    if jobValue is not None:
        filter_dict['job_status'] = jobValue

    #if compCode is not None:
    #    filter_dict['sub_brand'] = compCode

    if escType is not None:
        filter_dict['completion_code_description'] = q.ilike(f"%{escType}%")

    if watch:
        filter_dict['watchlistUsers'] = [currentUser]

    # Handling escalation status based on resolved status
    if escStatus is not None:
      if resolvedStatus is False:
        escStatus = app_tables.escalation_status.search(name=q.all_of(q.none_of("Resolved"),q.any_of(escStatus['name'])))    
      if resolvedStatus is True:
        escStatus = app_tables.escalation_status.search(name=q.any_of(q.any_of("Resolved"),q.any_of(escStatus['name']),))
    else:
        if resolvedStatus is False:
          escStatus = app_tables.escalation_status.search(name=q.none_of("Resolved")) 
        if resolvedStatus is True:
          escStatus = app_tables.escalation_status.search() 
  
  # Fetch merchant and subbrand values separately
    merchant_links = currentUser.get('user_merchant_link', [])
    subbrand_links = currentUser.get('user_subbrand_link', []) 
    
    merchant_subbrands = {}

    for merchant in merchant_links:
        # Check if the current merchant has any specific subbrand links
        linked_subbrands = [sb for sb in (subbrand_links or []) if sb['MerchantLink'] == merchant]
    
        if not linked_subbrands:
            # If no specific subbrand links, show all subbrands for this merchant plus universal subbrands
            all_subbrands = list(app_tables.subbrands.search(MerchantLink=merchant)) 
            merchant_subbrands[merchant] = all_subbrands
        else:
            # Only show the linked subbrands for this merchant
            merchant_subbrands[merchant] = linked_subbrands
    
    # Optional: Print to check what's being processed
    for merchant, subbrands in merchant_subbrands.items():
      #print(f"Merchant: {merchant['name']}, Subbrands: {[sb['Name'] for sb in subbrands]}")  
      print("filter change")
    selected_merchant = next((m for m in merchant_links if m['name'] == merchant_name), None)
    custTable = []
    # Handle merchant name if provided
    if merchant_name is None and compCode is None: #and assigned_to is None:
      for merchant, subbrands in merchant_subbrands.items():
        results = app_tables.webhook.search(
            tables.order_by("last_action_date", ascending=False),
            **filter_dict,
            date_created=q.between(min=startDate, max=endDate),
            webhook_merchant_link=merchant,  # Directly use the merchant object
            webhook_subbrand_link=q.any_of(*subbrands),  # Use the list of subbrand objects
            latest_status=q.any_of(*escStatus)
        )
        custTable.extend(results)
       
    elif merchant_name is not None and compCode is None:
      
      subbrands = merchant_subbrands.get(selected_merchant, [])
      results = app_tables.webhook.search(
          tables.order_by("last_action_date", ascending=False),
          **filter_dict,
          date_created=q.between(min=startDate, max=endDate),
          webhook_merchant_link=selected_merchant,  # Use the selected merchant object
          webhook_subbrand_link=q.any_of(*subbrands),  # Use all subbrands for this merchant
          latest_status=q.any_of(*escStatus)
      )
      custTable = results   
    
    elif merchant_name is None and compCode is not None:
      # Proceed with normal search for specific subbrands
        custTable = app_tables.webhook.search(
          tables.order_by("last_action_date", ascending=False),
          **filter_dict,
          date_created=q.between(min=startDate, max=endDate),
          webhook_merchant_link=compCode['MerchantLink'],  # Use the subbrand's specific merchant
          webhook_subbrand_link=compCode,  # Use the subbrand object directly
          latest_status=q.any_of(*escStatus)
      )        
    elif merchant_name is not None and compCode is not None:

        custTable = app_tables.webhook.search(
          tables.order_by("last_action_date", ascending=False),
          **filter_dict,
          date_created=q.between(min=startDate, max=endDate),
          webhook_merchant_link=selected_merchant,  # Use the subbrand's specific merchant
          webhook_subbrand_link=compCode,  # Use the subbrand object directly
          latest_status=q.any_of(*escStatus)
      )
    
    
    
    else:
      merchant_row = app_tables.merchant.search(name=merchant_name)
      #subbrand_row = app_tables.subbrands.search(Name=compCode)
      custTable = app_tables.webhook.search(tables.order_by("last_action_date", ascending=False),
                                            **filter_dict,date_created=q.between(min=startDate,max=endDate),
                                            webhook_merchant_link=q.any_of(*merchant_row),
                                            webhook_subbrand_link=compCode,
                                            latest_status=q.any_of(*escStatus))
  
    if searchText:
      custTable = [
          x for x in custTable
            if searchText.lower() in x['job_id'].lower() or
               searchText.lower() in x['job_reference'].lower() or
               searchText.lower() in x['customer_name'].lower() or
               (x['mobile_number'] and searchText.lower() in x['mobile_number'].lower()) or
               (x['sub_brand'] and searchText.lower() in x['sub_brand'].lower()) or
               (x['job_reference2'] and searchText.lower() in x['job_reference2'].lower()) or
               (x['job_reference3'] and searchText.lower() in x['job_reference3'].lower())
        ]
    custTable = sorted(custTable, key=lambda x: (x['last_action_date']), reverse=True)
    return custTable
    #custTable = sorted(custTable, key=lambda x: (x['last_action_date']), reverse=True)

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
  #print('sub:',subbrand)

  # Check if subbrand is None and fetch the specific "(Blank)" subbrand for the given merchant
  if subbrand is None:
      
      # Attempt to fetch the specific (Blank) subbrand
      subbrand_row = app_tables.subbrands.get(MerchantLink=merchant_row, ID=blank_subbrand_id)
      
      if not subbrand_row:
          # Construct the ID for the (Blank) subbrand specific to this merchant
          blank_subbrand_id = merchant_row['server'] + str(merchant_row['merchant_id']) + '00001'

          # Optional: Create the subbrand if it doesn't exist
          new_subbrand = app_tables.subbrands.add_row(
              MerchantID=str(merchant_row['merchant_id']),
              ID=blank_subbrand_id,
              Name='(Blank)',
              Server=merchant_row['server'],
              LastUpdated=datetime.now(),
              MerchantLink=merchant_row
          )
          subbrand_row = app_tables.subbrands.get(MerchantLink=merchant_row, ID=blank_subbrand_id)
          print("Created new (Blank) subbrand for Merchant ID:", merchant_row['merchant_id'])
  
  row = app_tables.webhook.add_row(
     job_id = job,
     job_reference = jobref,
     customer_name = customer,
     mobile_number = mobile,
     webhook_merchant_link = merchant_row,
     comment = description,
     sub_brand = subbrand['Name'],
     webhook_subbrand_link = subbrand_row,
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
        assign_to=assign_to,
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
    data = [
      {
        "User": r["user"]["name"], 
        "Status": r["status"], 
        "Created Date": r["created_date"]
      } 
      for r in app_tables.action_log.search(escalation_id=q.any_of(*escalations))
      if not (r["user"]["name"] == "System")
    ]
    df = pd.DataFrame(data)
    #df1 = df.loc[df["User"] !='System' ]
    #https://sparkbyexamples.com/pandas/pandas-groupby-multiple-columns/
    grouped_df = df1.groupby(['User']).agg(
    Count=pd.NamedAgg(column='User', aggfunc='count')
    ).reset_index()
    grouped_df.columns = ['User', 'count']
    sorted_df = grouped_df.sort_values(by='count', ascending=True)
    sorted_df.reset_index(inplace=True)
    ch_user = px.bar(sorted_df, x='count', y='User', orientation='h', text ='count')
    ch_user.update_layout(font=dict(family="Arial",color='rgb(128,128,128)'),
                        margin=dict(l=20, r=20, t=10, b=20),
                        plot_bgcolor="white",
                        xaxis_title=None, yaxis_title=None
                        )
    ch_user.update_traces(marker_color='rgb(18,35,158)', opacity=0.9, textangle=0,
                        hovertemplate=
                        "<b>%{y}</b><br>" +
                        "Responses : %{x}<br>" +
                        "<extra></extra>")
    ch_user.update_xaxes(showline=True, linewidth=1, linecolor='rgb(128,128,128)')
    ch_user.update_yaxes(showline=True, linewidth=1, linecolor='rgb(128,128,128)',
                      showticklabels=True,ticks="outside",tickson="boundaries",
                      ticklen=5,tickangle=0,tickfont=dict(family='Arial', color='rgb(128,128,128)', size=12))
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
             for r in app_tables.webhook.search(webhook_merchant_link=q.any_of(*values))
             if not (r["latest_status"]["name"] == "Resolved" and r["latest_assignee"]["name"] == "System")
           ]
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
    if not last_week_df_resolved.empty:
      last_week_per = round(last_week_resolved / last_week *100 ,1)
    else: 
      last_week_per = "N/A"
    prior_week_df_resolved = filtered_df_prior_week[filtered_df_prior_week['Status'] == 'Resolved']
    prior_week_resolved = len(prior_week_df_resolved)
    if not prior_week_df_resolved.empty:
      prior_week_per = round(prior_week_resolved / prior_week *100 ,1)
    else:
      prior_week_per = "N/A"
    if last_week_per == "N/A" or prior_week_per == "N/A":
      delta2 = "N/A"
    else:
      delta2 = round(last_week_per - prior_week_per,1) 

    df['resolve_time'] = (df['last_action_datetime'] - df['Datetime Created']) / pd.to_timedelta(1, unit='D')
    resolved_df_last_week = df[(df['last_action_date'] >= start_date_last_week) & (df['last_action_date'] <= end_date_last_week) & (df['Status'] == 'Resolved')]
    resolved = len(resolved_df_last_week)
    resolved_df_prior_week = df[(df['last_action_date'] >= start_date_prior_week) & (df['last_action_date'] <= end_date_prior_week) & (df['Status'] == 'Resolved')]
    prior_resolved = len(resolved_df_prior_week)
    delta3 = resolved - prior_resolved
    if not resolved_df_last_week.empty:
      ave_resolve_time_lw = round(resolved_df_last_week['resolve_time'].mean(),1)
    else: 
      ave_resolve_time_lw = "N/A"
    if not resolved_df_prior_week.empty:
      ave_resolve_time_pw = round(resolved_df_prior_week['resolve_time'].mean(),1)
    else: 
      ave_resolve_time_pw = "N/A"
    if ave_resolve_time_lw == "N/A" or ave_resolve_time_pw == "N/A":
      delta4 = "N/A"
    else:
      delta4 = round(ave_resolve_time_lw - ave_resolve_time_pw,1)
      

    return last_week, delta, last_week_per, delta2, resolved, delta3, start_date_last_week, end_date_last_week, ave_resolve_time_lw, delta4


@anvil.server.callable
def all_charts(today,currentUser):
    #create dataset
    related_rows = currentUser['user_merchant_link']
    values = [row for row in related_rows]
    data = [
      {
        "Escalation Type": r["completion_code_description"].capitalize(), 
        "last_action_date": r["last_action_date"],
        "Status": r["latest_status"]["name"], 
        "Date Created": r["date_created"].date(),
        "Datetime Created": r["date_created"],
      } 
      for r in app_tables.webhook.search(webhook_merchant_link=q.any_of(*values))
      if not (r["latest_status"]["name"] == "Resolved" and r["latest_assignee"]["name"] == "System")
      ]
    df = pd.DataFrame(data)
    #pie chart last week and bar chart last week vs this week
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
                   color_discrete_map={'New':'rgb(161,52,60)','Active':'rgb(252,166,54)','Pending Approval':'rgb(40,166,77)','Approved':'rgb(13,13,13)','Resolved':'rgb(153,153,153)'})
    pie.update_traces(textinfo='label+value', insidetextorientation='horizontal', pull=0.00,hoverinfo='label+value+percent',
                        hovertemplate=
                        "<b>%{label}</b><br>" +
                        "Tickets : %{value}<br>" +
                        "<extra></extra>")
    pie.update_layout(font=dict(family="Arial",color="rgb(128,128,128)"),
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
    name='This Week', marker_color='rgb(40,166,77)',texttemplate='%{y}'
    )
    trace_last_week = go.Bar(
    x=grouped_df[grouped_df['Week'] == 'Last Week']['Day'],
    y=grouped_df[grouped_df['Week'] == 'Last Week']['Count'],
    name='Last Week', marker_color='rgb(161,52,60)',texttemplate='%{y}'
    )
    chart = go.Figure(data=[trace_this_week, trace_last_week])
    chart.update_layout(font=dict(family="Arial",color="rgb(128,128,128)"),
                        showlegend=True, hovermode='closest',
                        margin=dict(l=10, r=10, t=10, b=10),
                        xaxis_title=None, yaxis_title=None,
                        plot_bgcolor="white")
    chart.update_yaxes(showticklabels=False)
    #chart.update_traces(hovertemplate=
    #                    "%{Week}<br>" +
    #                    "Tickets : %{x}<br>" +
    #                    "<extra></extra>")
    chart.update_xaxes(showline=True, linewidth=1, linecolor='rgb(128,128,128)',tickcolor='rgb(128,128,128)',
                       showticklabels=True,ticks="outside",tickson="boundaries",
                       ticklen=5,tickangle=0,tickfont=dict(family='Arial', color='rgb(128,128,128)', size=12))

    #tickets by current status
    grouped_df = df.groupby('Status').agg(
    Count=pd.NamedAgg(column='Date Created', aggfunc='count')
    ).reset_index()
    grouped_df.columns = ['Status', 'count']
    sorted_df = grouped_df.sort_values(by='count', ascending=True)
    sorted_df.reset_index(inplace=True)
    ch_status = px.bar(sorted_df, x="count", y="Status", orientation='h', color='Status', text ='count',
                   category_orders={"Status": ["New", "Active", "Pending Approval", "Approved",'Resolved']},
                   color_discrete_map={'New':'rgb(161,52,60)','Active':'rgb(252,166,54)','Pending Approval':'rgb(40,166,77)','Approved':'rgb(13,13,13)','Resolved':'rgb(153,153,153)'})
    ch_status.update_layout(font=dict(family="Arial",color="rgb(128,128,128)"),
                        margin=dict(l=20, r=20, t=10, b=20),
                        showlegend=False,
                        plot_bgcolor="white",
                        xaxis_title=None, yaxis_title=None
                        )
    ch_status.update_traces(hovertemplate=
                        "<b>%{y}</b><br>" +
                        "Tickets : %{x}<br>" +
                        "<extra></extra>")
    ch_status.update_xaxes(showline=True, linewidth=1, linecolor='rgb(128,128,128)')
    ch_status.update_yaxes(showline=True, linewidth=1, linecolor='rgb(128,128,128)',
                      showticklabels=True,ticks="outside",tickson="boundaries",
                      ticklen=5,tickangle=0,tickfont=dict(family='Arial', color='rgb(128,128,128)', size=12))

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
                   color_discrete_map={'New':'rgb(161,52,60)','Active':'rgb(252,166,54)','Pending Approval':'rgb(40,166,77)','Approved':'rgb(13,13,13)','Resolved':'rgb(153,153,153)'})
    ch_date.update_layout(font=dict(family="Arial",color="rgb(128,128,128)"),
                        margin=dict(l=20, r=20, t=10, b=20),
                        plot_bgcolor="white",hovermode='x',
                        xaxis_title=None, yaxis_title=None
                        )         
    ch_date.update_xaxes(showline=True, linewidth=1, linecolor='rgb(128,128,128)',
                      showticklabels=True,ticks="outside",tickson="boundaries",
                      minor=dict(ticklen=3, tickcolor="rgb(128,128,128)", showgrid=False),
                      ticklen=8,tickangle=0,tickfont=dict(family='Arial', color='rgb(128,128,128)', size=12))
    ch_date.update_yaxes(showline=True, linewidth=1, linecolor='rgb(128,128,128)')
  
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
                               mode='lines', name='Average Resolution time', 
                               line=dict(color='rgb(161,52,60)'),line_shape='spline'
                               ))
    # Update the layout
    ch_type.update_layout(font=dict(family="Arial",color='rgb(128,128,128)'),
                        margin=dict(l=20, r=20, t=10, b=20),
                        plot_bgcolor="white",hovermode='y unified',
                        xaxis_title=None, yaxis_title=None
                        )
    ch_type.update_traces(hoverinfo = 'y+x')
    ch_type.update_xaxes(showline=True, linewidth=1, linecolor='rgb(128,128,128)',
                      rangemode="tozero")
    ch_type.update_yaxes(showline=True, linewidth=1, linecolor='rgb(128,128,128)',
                      showticklabels=True,ticks="outside",tickson="boundaries",rangemode="tozero",
                      ticklen=5,tickangle=0,tickfont=dict(family='Arial', color='rgb(128,128,128)', size=12))

    return pie,chart,ch_status,ch_date,ch_type
    #print("-----aa")
    #print(rowValue)
    #print("-----bb")
    #print(rowValue['job_status'])
    return app_tables.webhook.get(id=q.any_of(id))

@anvil.server.callable
def sync_subbrand(record):
    # Construct API server URL based on the server number
    apiServer = "" if record['server'] == '1' else f"-{record['server']}"

    # Check if an API token is available
    if record['APIToken']:
        # Build the API request URL
        url = f"https://api{apiServer}.radaro.com.au/api/webhooks/sub-brands/?key={record['APIToken']}&page_size=100"
        try:
            # Send the API request
            response = requests.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                # Check the count of subbrands
                if data['count'] == 0:
                    print("No subbrands found for the given merchant.")
                else:
                    results = data.get('results', [])
                    print(f"Processing {len(results)} subbrands.")
                    # Process each subbrand in the results
                    for result in results:
                        # Fetch existing subbrand record or create a new one
                        existing_record = app_tables.subbrands.get(MerchantID=str(result['merchant']), ID=str(result['id']), Server=record['server'])
                        if existing_record:
                            existing_record.update(Logo=result['logo'], Name=result['name'], LastUpdated=datetime.now())
                            #print(f"Updated subbrand {result['name']} for merchant ID {result['merchant']}.")
                        else:
                            app_tables.subbrands.add_row(
                                MerchantID=str(result['merchant']),
                                ID=str(result['id']),
                                Logo=result['logo'],
                                Name=result['name'],
                                Server=record['server'],
                                LastUpdated=datetime.now(),
                                MerchantLink=record
                            )
                            print(f"Added new subbrand {result['name']} for merchant ID {result['merchant']}.")
            else:
                print(f"Failed to retrieve subbrands: {response.status_code} {response.text}")
        except requests.exceptions.RequestException as e:
            print("API request failed:", e)
        except Exception as e:
            print("An error occurred:", e)
    else:
        print("No API Token on record")

    # Call the function to ensure default subbrands, regardless of the above results
    ensure_default_subbrands(record)

@anvil.server.callable
def ensure_default_subbrands(record):
    # Check and add default "(Blank)" and "Unidentified" subbrands if not already present
    blank_subbrand = app_tables.subbrands.get(MerchantID=record['merchant_id'], ID=record['server'] + str(record['merchant_id']) + '00001')
    if not blank_subbrand:
        app_tables.subbrands.add_row(
            MerchantID=str(record['merchant_id']),
            ID=record['server'] + str(record['merchant_id']) + '00001',
            Name="(Blank)",
            Server=record['server'],
            LastUpdated=datetime.now(),
            MerchantLink=record
        )
        print("Default (Blank) subbrand added.")

    unidentified_subbrand = app_tables.subbrands.get(MerchantID=record['merchant_id'], ID=record['server'] + str(record['merchant_id']) + '00000')
    if not unidentified_subbrand:
        app_tables.subbrands.add_row(
            MerchantID=str(record['merchant_id']),
            ID=record['server'] + str(record['merchant_id']) + '00000',
            Name="Unidentified",
            Server=record['server'],
            LastUpdated=datetime.now(),
            MerchantLink=record
        )
        print("Default Unidentified subbrand added.")
       


@anvil.server.callable
def sync_compCodes(record):
  #print(record['APIToken'])
  if record['server'] == '1':
    apiServer = ""
  else:
    apiServer = "-" + record['server']

  print(apiServer)
  print(record['APIToken'])
  if record['APIToken'] is not None:
    response = requests.get('https://api'+apiServer+'.radaro.com.au/api/webhooks/completion-codes/?key='+record['APIToken']+'&page_size=100')
    data = response.json()
    #print(response.status_code)
    #print(response.reason)
    try:
      for result in data['results']:
          #print(result['id'])
            # Check if a record with the same MerchantID and ID exists
          existing_record = app_tables.compcodes.get(MerchantID=str(result['merchant']), ID=str(result['code']),Server=record['server'])
            
          if existing_record:
                # Update existing record
              existing_record.update(Name=result['name'],LastUpdated=datetime.now(),codeType=result['type'])
          else:
                # Insert new record
              if 'success' == result['type']: 
                app_tables.compcodes.add_row(MerchantID=str(result['merchant']), ID=str(result['code']), Name=result['name'],Server=record['server'],LastUpdated=datetime.now(),merchantLink=record,is_enabled=False,codeType=result['type'])
              else:
                app_tables.compcodes.add_row(MerchantID=str(result['merchant']), ID=str(result['code']), Name=result['name'],Server=record['server'],LastUpdated=datetime.now(),merchantLink=record,is_enabled=True,codeType=result['type'])
    except Exception as  e:
      print("API Request Failed")
      print(e)
  else:
    print("No API Token on record")
    
@anvil.server.callable
def DB_task(now):
  """Fire off the training task, returning the Task object to the client."""
  #anvil.server.launch_background_task('update_db_value',now)
  anvil.server.launch_background_task('update_sb_value',now)

@anvil.server.background_task
def update_sb_value(now):
    # Fetch all webhook entries
    webhooks = app_tables.webhook.search()

    # Clear existing subbrand links
    for webhook in webhooks:
        webhook['webhook_subbrand_link'] = None

    # Fetch all subbrands and organize them for quick access
    subbrands = {}
    for sub in app_tables.subbrands.search():
        if sub['MerchantLink']:
            key = (sub['MerchantLink'].get_id(), sub['Name'])
            subbrands[key] = sub

    # Refresh webhook entries after clearing the links
    webhooks = app_tables.webhook.search()

    for webhook in webhooks:
        sub_brand_name = webhook['sub_brand']
        merchant_link = webhook['webhook_merchant_link']

        if not merchant_link:
            print("Warning: No MerchantLink for webhook ID:", webhook.get_id())
            continue

        # Determine sub_brand_name specifics
        sub_brand_key = (merchant_link.get_id(), sub_brand_name)

        if sub_brand_key in subbrands:
            # Set the webhook_subbrand_link to the matching subbrand
            webhook['webhook_subbrand_link'] = subbrands[sub_brand_key]
            print(f"Linked subbrand {sub_brand_name} to webhook ID {webhook.get_id()}.")
        else:
            print(f"No matching subbrand found for {sub_brand_name} under merchant {merchant_link['name']}")
            # Handle (Blank) and Unidentified specially if no direct match is found
            if sub_brand_name in ["(Blank)", "Unidentified", "---", "None"] or sub_brand_name in subbrands:
                normalized_name = "(Blank)" if sub_brand_name in ["None", "---"] else sub_brand_name  
                suffix = '00001' if sub_brand_name in ["(Blank)", "---", "None"] else '00000'
                sub_brand_id = merchant_link['server'] + str(merchant_link['merchant_id']) + suffix
                # Attempt to fetch or create specific subbrand
                specific_subbrand_key = (merchant_link.get_id(), normalized_name)
                specific_subbrand = subbrands.get(specific_subbrand_key) or app_tables.subbrands.get(MerchantLink=merchant_link, ID=sub_brand_id)
                if not specific_subbrand:
                    specific_subbrand = app_tables.subbrands.add_row(
                        MerchantID=str(merchant_link['merchant_id']),
                        ID=sub_brand_id,
                        Name=normalized_name,
                        Server=merchant_link['server'],
                        LastUpdated=datetime.now(),
                        MerchantLink=merchant_link
                    )
                    subbrands[specific_subbrand_key] = specific_subbrand  # Update dictionary
                    print(f"Created new {sub_brand_name} subbrand for Merchant ID: {merchant_link['merchant_id']}")
                webhook['webhook_subbrand_link'] = specific_subbrand
            else:
              # Check against both Name and ID
              sub_brand_key = (merchant_link.get_id(), sub_brand_name)
              matching_subbrand = subbrands.get(sub_brand_key) or app_tables.subbrands.get(MerchantLink=merchant_link, ID=sub_brand_name)
              if matching_subbrand:
                  webhook['webhook_subbrand_link'] = matching_subbrand
              else:
                  print(f"No matching subbrand found for {sub_brand_name} under merchant {merchant_link['name']}")
                  # Optionally set a default subbrand or handle the error
                  # webhook['webhook_subbrand_link'] = default_subbrand

# Call the function with the current datetime
#update_sb_value(datetime.datetime.now())

@anvil.server.background_task
def update_db_value(now):
    # Fetch all rows from the table
    #rows = app_tables.webhook.search()
    
    portal_for_change = "--"
    status = app_tables.escalation_status.get(name="Resolved")
    user = app_tables.users.get(name="System")
    description="Prelaunch trial data"
    start_date = datetime(year=2023, month=11, day=5)
    end_date = datetime(year=2023, month=11, day=18)
    rows = app_tables.webhook.search(date_created=q.between(start_date, end_date))
    #print(*rows) 
    for row in rows:
      print(row['completion_code_description'])
      if row["webhook_merchant_link"]["token"] == portal_for_change and row['completion_code_description'] == "Completed" and row["latest_status"]["name"] != "Resolved":

          print(row)
          print(now)
             #Update the value in the database
          row["latest_status"] = status
          row["last_action_date"] = now
          row["latest_assignee"]= user
          row = app_tables.action_log.add_row(
          job_id=row,
          user= user,
          description=description,
          status=status,
          created_date = now,
          assign_to=user,
          escalation_id=row)

@anvil.server.callable
def send_email(record_copy,description,status,created_date,recipient,submitter):
  senderemail = submitter['email']
  recipientrow = app_tables.users.get(name=recipient)
  recipientemail = recipientrow['email']
  formatted_date = created_date.strftime("%d %b, %Y %H:%M")
  anvil.email.send(
      from_name="Radaro REACT Notification",
      to=recipientemail,
      subject="REACT Escalation: %s" % (record_copy["job_reference"]),
#      html='Hi %s, <br><br> You have been assigned a ticket from %s.<br><br> <b>Comments : </b>%s <br> Click <a href="https://au-react.radaro.com.au">here</a> to action. <br><br> <b><u> Details of the ticket : </b></u><br> <b>Date created : </b>%s. <br> <b>Ticket number : </b>%s. <br> <b>Status : </b>%s' % (recipientrow['name'], submitter['name'], description, formatted_date, record_copy["job_reference"], status['name']),
      html = (
    '<html>'
    '<body>'
    '    <table width="100%" style="background:none 50% 50%/cover no-repeat rgb(255,255,255);border-radius:5px">'
    #'        <tr>'
    '            <td style="padding-top:9px;padding-bottom:0px;">'
    '                <table width="100%" style="border-collapse:collapse;">'
    #'                    <tr>'
    '                        <td style="padding-top:9px;">'
    '                            <table width="100%" style="max-width:100%;border-collapse:collapse;">'
    '                                <tr>'
    '                                    <td style="padding:0px 60px;font-family:Lato,\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:24px;font-style:normal;font-weight:normal;text-align:center;">'
    '                                        <div style="text-align:center;">'
    '                                            <p style="text-align:left;font-weight:bold;font-size:18px;font-family:lato,helvetica neue,helvetica,arial,sans-serif;color:#202020;line-height:22px;">'
    '                                               Hello {},'
    '                                            </p>'
    '                                        </div>'
    '                                    </td>'
    '                                </tr>'
    '                            </table>'
    '                        </td>'
    '                    </tr>'
    '                </table>'
    '            </td>'
    '        </tr>'
    '    </table>'
    '<table width="100%" style="border-collapse:collapse;">'
    '    <tr>'
    '        <td>'
    '            <table width="100%" style="max-width:100%;border-collapse:collapse;">'
    '                <tr>'
    '                    <td style="padding:0 65px;">'
    '                        <div style="text-align:left;font-size:16px;font-family:lato,helvetica neue,helvetica,arial,sans-serif;color:#202020!important;">'
    '                            You have been assigned an Escalation from {}'
    '                            <table style="font-size:12px;line-height:16px;text-align:left;margin-top:18px;">'
    '                                <tr>'
    '                                    <td style="color:#959595;width:120px;">Job ID:</td>'
    '                                    <td>{}</td>'
    '                                </tr>'
    '                                <tr>'
    '                                    <td style="color:#959595">Job Reference:</td>'
    '                                    <td>{}</td>'
    '                                </tr>'
    '                                <tr>'
    '                                    <td style="color:#959595">Date Created:</td>'
    '                                    <td>{}</td>'
    '                                </tr>'
    '                                <tr>'
    '                                    <td style="color:#959595">Escalation Status</td>'
    '                                    <td>{}</td>'
    '                                </tr>'
    '                                <tr>'
    '                                    <td style="color:#959595">Comment:</td>'
    '                                    <td>{}</td>'
    '                                </tr>'
    '                            </table>'
    '                        </div>'
    '                    </td>'
    '                </tr>'
    '            </table>'
    '        </td>'
    '    </tr>'
    '</table>'
    '<table width="100%">'
    '    <tr>'
    '        <td style="padding:28px 65px;">'
    '            <table width="100%" style="border-top-width:1px;border-top-style:solid;border-top-color:#ececec;">'
    '                <tr>'
    '                    <td><span></span></td>'
    '                </tr>'
    '            </table>'
    '        </td>'
    '    </tr>'
    '</table>'
    '<table width="100%" style="border-collapse:collapse;">'
    '    <tr>'
    '        <td style="padding-top:0;padding-right:18px;padding-left:18px" valign="top" align="center">'
    '            <table style="border-collapse:separate!important;border:2px solid #252525;border-radius:50px;background-color:#252525;">'
    '                <tr>'
    '                    <td align="center" valign="middle" style="max-width:400px;font-family:Lato,"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:12px;padding:15px;">'
    '                        <a title="SEE DETAILS" href="https://au-react.radaro.com.au" style="padding:0 40px;font-weight:normal;letter-spacing:3px;line-height:100%;text-align:center;text-decoration:none;color:#ffffff" target="_blank" data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=http://url4248.radaro.com.au/ls/click?upn%3DoG3S6L9g-2BFrJdFWz3k0-2B8NWPxSAKvrCF19-2FaKCsRrKDc7ALY3YnVdy5F5M8LavXr2LpbVc8zxyU0Q8re2-2BZssma0gBeK-2FqsAXO47ah-2Bj3kdKWZfaLcoUsv0K1NYrEHJXJ3WF-2Fz9bEu0hMx0fl93yJQ-3D-3D2CoR_bHSYq-2FBQrXUeej-2B2FOFDQKcEX5zBpkqGdwoCET-2BPhIJ1GGali2iv8jAle0fMlYStgyGxQEDXrxyTye3ZL9td2MKcyzk4vGQnRqMCy3a-2Fv1bzVO1DeyEe-2BCrbK0awLiFKZ9hoxC8qB82muwsLe-2FegEpwIRNnEHQAxH3AAKf9pT0ke3CoNfAWglDni3-2FF3pMcisl7KW81258fJzIczCohpDM-2FyLjZqFVq4fChIwrBbonm9HewHxF-2BI7pf034IhJ9Un-2FsCLTs3UCEzvBOYcbs-2FqVkk1kQv1LDlUUTjN4k2WaBGyikExg-2B-2BmKpPz&amp;source=gmail&amp;ust=1694817764536000&amp;usg=AOvVaw3powU_fk5fpLgRGL2VIfr6">'
    '                            SEE DETAILS'
    '                        </a>'
    '                    </td>'
    '                </tr>'
    '            </table>'
    '        </td>'
    '    </tr>'
    '</table'
    '<table width="100%" style="border-collapse:collapse;">'
    '    <tr>'
    '        <td style="padding-top:13px">'
    '            <table width="100%" style="max-width:100%;border-collapse:collapse;">'
    '                <tr>'
    '                    <td style="padding:0px 60px 9px;color:#979797;font-family:Lato,"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:16px;text-align:center">'
    '                        <div style="background-color:#f1f1f1;text-align:center;font-size:16px;font-family:lato,helvetica neue,helvetica,arial,sans-serif;border-radius:5px;padding:18px 25px 20px;line-height:20px">'
    '                            You can get more information by using the button above.'
    '                        </div>'
    '                    </td>'
    '                </tr>'
    '            </table>'
    '        </td>'
    '    </tr>'
    '</table>'
    '</body>'
    '</html>'
).format(recipientrow['name'], submitter['name'], record_copy["job_id"], record_copy["job_reference"], formatted_date, status['name'],description)
  )

@anvil.server.callable
def create_pdf(ires):
    filename= "REACT_" + ires
    iresrow = app_tables.webhook.get(id=ires)
    ires=iresrow
    #pdf = anvil.pdf.render_form('Modal_pdf',ires)
    pdf = PDFRenderer(filename = f'{filename}.pdf', page_size='A4', scale = 0.8).render_form('Modal_pdf',ires)
    return pdf

