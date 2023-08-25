import anvil.files
from anvil.files import data_files
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta, date
import pandas as pd
import anvil.server
import json


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
  if 'new_values' in data:
    if 'is_confirmed_by_customer' in data['new_values'] and merctable is not None:
      
      if 'job.status_changed' in topic and 'updated' in data.get('event_type') and True == data['new_values']['is_confirmed_by_customer'] and merctable['rating_threshold'] >= data['order_info']['rating'] :
        #print(json)
        codes=data['order_info']['completion_codes']
        id_values = [str(code["code"]) for code in codes]
        id_string = ";".join(id_values)
          
        nv = data['new_values']['is_confirmed_by_customer']
        rating = data['order_info']['rating']
        counter = get_next_value_in_sequence()
        #try:
        app_tables.webhook.add_row(
        job_id = str(data['order_info']['order_id']),
        id= str(counter),
        customer_name = data['order_info']['customer']['name'],
        completion_code_id = id_string,
        date_created = datetime.now(),
        last_action_date =datetime.now(),
        job_reference = data['order_info']['title'],
        webhook_merchant_link=app_tables.merchant.get(token=data['token']),
        job_status = app_tables.job_status.get(sysName=data['order_info']['status']),
        job_report = data['order_info']['public_report_link'],
        customer_rating= str(rating),
        escalation_type = app_tables.escalation_type.get(name= "Low Rating"),
        latest_assignee = None,
        latest_status = app_tables.escalation_status.get(name= "New"),
        sub_brand=data['order_info']['sub_branding'],
        mobile_number=data['order_info']['customer']['phone'],
        date_delivered=datetime.strptime(data['order_info']['completed_at'], "%Y-%m-%dT%H:%M:%S.%f%z"), 
        job_reference2=data['order_info']['title_2'],
        job_reference3=data['order_info']['title_3'],
        address=data['order_info']['deliver_address']['address'],
        watch_list=False,
        watchlistUsers=[])
        #except:
           # print("falied")
   ## elif 'job.completion_codes_accepted' in topic and 'updated' in data.get('event_type'):
   ##     codes=data['order_info']['completion_codes']
   ##     id_values = [str(code["code"]) for code in codes]
   ##     id_string = ";".join(id_values)
          
        #nv = data['new_values']['is_confirmed_by_customer']
   ##     rating = data['order_info']['rating']
   ##     counter = get_next_value_in_sequence()
   ##     app_tables.test_table.add_row(
   ##      job_id = data['order_info']['order_id'],
   ##       id= str(counter),
   ##       customer_name = data['order_info']['customer']['name'],
   ##       completion_code_id_str = id_string,
   ##       date_created = datetime.now(),
   ##       last_action_date =datetime.now(),
   ##       job_reference = data['order_info']['title'],
   ##       webhook_merchant_link=app_tables.merchant.get(merchant_id= "124"),
   ##       job_status = data['order_info']['status'],
   ##       job_report = data['order_info']['public_report_link'],
   ##       customer_rating= rating,
   ##      escalation_type = app_tables.escalation_type.get(name= "Low Rating"),
   ##       latest_assignee = None,
   ##       latest_status = app_tables.escalation_status.get(name= "New"),
   ##       sub_brand=data['order_info']['sub_branding'],
   ##       mobile_number=data['order_info']['customer']['phone'],
   ##       date_delivered=data['order_info']['completed_at'],
   ##       job_reference2=data['order_info']['title_2'],
   ##       job_reference3=data['order_info']['title_3'],
   ##       address=data['order_info']['deliver_address']['address'],
   ##       watch_list=False)
    else:
        pass
  
  

@anvil.server.callable
def get_merchant_list():
  currentUser=anvil.users.get_user()
  Xvalues = []
  x_rows = currentUser['user_merchant_link']
  x_list =[r['name'] for r in x_rows]
 # print(x_list)
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
  return app_tables.users.search(user_merchant_link=q.any_of(*values))

#@anvil.server.callable
#def get_active_user():
#  active_user = anvil.users.get_user('name')
#  return active_user

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
    filter_dict['completion_code_id'] = compCode

  if escType != None:
    filter_dict['escalation_type'] = escType

  if watch is True :
    filter_dict['watch_list'] = True

  if escStatus != None:
  #  filter_dict['latest_status'] = escStatus
    
    if resolvedStatus is False:
      print(escStatus['name'])
      escStatus = app_tables.escalation_status.search(name=q.all_of(q.none_of("Resolved"),q.any_of(escStatus['name']))) 
      #print("----")
      #print(*escStatus)
      

    if resolvedStatus is True:
      escStatus = app_tables.escalation_status.search(name=q.any_of(q.any_of("Resolved"),q.any_of(escStatus['name']),))

  
  if escStatus == None:
    if resolvedStatus is False:
      escStatus = app_tables.escalation_status.search(name=q.none_of("Resolved")) 
      #print("1")
    if resolvedStatus is True:
      #print("2")
      escStatus = app_tables.escalation_status.search() 

  #print("-----")
  #print(*jjv)
  #selected_status_rows = [status_row for status_row in app_tables.webhook.search(job_status=q.any_of(*selected_statuses))]
  #print(selected_status_rows)
  
  #print(values)
  #print(jobValue)
  related_rows = currentUser['user_merchant_link']
    #print(RelatedJobStatus)
    #print(related_rows)
  values = [row for row in related_rows]
  if merchant_name is None and assigned_to is None :
    custTable = app_tables.webhook.search(tables.order_by("last_action_date", ascending=False),**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*values),latest_status=q.any_of(*escStatus))

  elif merchant_name is None and assigned_to is not None :
    custTable = app_tables.webhook.search(tables.order_by("last_action_date", ascending=False),**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*values),latest_status=q.any_of(*escStatus))

  elif merchant_name is not None and assigned_to is None :
    merchant_row = app_tables.merchant.search(name=merchant_name)
    #print(merchant_row)
    custTable = app_tables.webhook.search(tables.order_by("last_action_date", ascending=False),**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*merchant_row),latest_status=q.any_of(*escStatus))

  else:
    #filter_dict['webhook_merchant_link'] = merchant_name
    merchant_row = app_tables.merchant.search(name=merchant_name)
    #print(merchant_row)
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
    
  #custTable = custTable
  #status_row = app_tables.escalation_status.search(name=q.none_of("Resolved")) 
  #print(*status_row)
  #if resolvedStatus:
  #  custTable = [
  #    x for x in custTable
  #    if statusRow in x['esc_status']]

 #   if resolvedStatus:
 #    custTable = [
#       x for x in custTable
#       if  in x['job_status']

 
  

#  app_tables.merchant.search(name=q.all_of(*currentUser['user_merchant_link']))
  #print(*currentUser['user_merchant_link'])
  #if filters.get('job_status') and filters['job_status'] == Data.NO_STATUS_SELECTED:
  #  filters['job_status'] = None
  # Get a list of escalation from the Data Table, sorted by 'date_created' column, in descending order
  
 #custTable = app_tables.webhook.search(job_status=jobValue,completion_code_id=compCode,escalation_type=escType,latest_status=escStatus,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*values))
  return custTable
  
  #.search(**kwargs)
    #tables.order_by("date_created", ascending=False),
    #tables.order_by("last_action_date", ascending=False)
    #,job_status=jstatus
      

#return app_tables.articles.search(ArticleLink=q.any_of(*x['userMerchLink']))


@anvil.server.callable
def get_action(rowValue):
  # Get a list of articles from the Data Table, sorted by 'created' column, in descending order
 # print(rowValue)
  
  if rowValue is None: 
    print("No Escalation Selected")
  else:
    #print("-----aa")
    #print(rowValue)
    #print("-----bb")
    #print(rowValue['job_status'])
    return app_tables.action_log.search(tables.order_by("created_date",ascending=False),escalation_id=q.any_of(rowValue)
    
  )

@anvil.server.callable
def get_selectedMerchant(selectedMerchant):
  #valuesMerch = [row for row in selectedMerchant]
  related_rows = selectedMerchant
    #print(RelatedJobStatus)
    #print(related_rows)
  values = [row for row in related_rows]
  #print(related_rows)
 # print(values)
  
  if selectedMerchant is None:
    print("No Escalation Selected")
  else:
    xMerch = app_tables.users.search(user_merchant_link=[related_rows])
    values = [[row] for row in xMerch]
    x_list =[r['name'] for r in xMerch]
   # print("xxxxxx")
  #  print(x_list)
    return x_list
    

@anvil.server.callable
def add_comment(article, article_dict, description, status, created_date, assign_to):
  if app_tables.webhook.has_row(article):
   article_dict['last_action_date'] = datetime.now()
   article_dict['latest_status'] = status
   assignrow = app_tables.users.get(name=assign_to)
   article_dict['latest_assignee'] = assignrow
   tx = article['job_id']
   #print(assignrow)
   row = app_tables.action_log.add_row(
    job_id=article,
    user=anvil.users.get_user(),
    description=description,
    status=status,
    created_date = created_date,
    assign_to=assignrow,
    escalation_id=article)
   #print(*row)
   article.update(**article_dict)
  else:
   raise Exception("Article does not exist")
 # x_assign = app_tables.users.get(name=assign_x)
#  print(*x_assign)
 # currentUser = anvil.users.get_user()
 # app_tables.action_log.add_row(
    #job_id=job_id,
 #   user=currentUser,
 #   description=description,
  #  status=status,
  #  created_date = created_date,
  #  assign_to=x_assign
 # )

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
#@anvil.server.callable
#def search_webhook(query):
#  result = app_tables.webhook.search()
#  if query:
#    result = [
#      x for x in result
#      if query in x['job_id'].lower()
#      or query in x['job_reference'].lower()
#     or query in x['customer_name'].lower() 
 #   ]
#  return result

@anvil.server.callable
def update_item(row_id,watch_list):
  watch_list = watch_list
  row_id=row_id
  row=app_tables.webhook.get(id=row_id)  
  #job_id=article
    #if app_tables.webhook.has_row(article):
  row['watch_list']=watch_list
  #app_tables.webhook.update(row_id,watch_list)

@tables.in_transaction
def get_next_value_in_sequence():
  row = int(app_tables.webhook.search(tables.order_by("id", ascending=False))[0]['id'])
  
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
    #print(df['customer_rating'])
    compdf =df
    counter = get_next_value_in_sequence()
    df= df.loc[df['customer_rating'].isin([1,2,3])]
    df['completed_at'] = pd.to_datetime(df['completed_at'])
    for d in df.to_dict(orient="records"):
      # d is now a dict of {columnname -> value} for this row
      # We use Python's **kwargs syntax to pass the whole dict as
      # keyword arguments
     # print(d['order_status'])
     # print(*d)
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
        user=app_tables.users.get(name= "System"),
        description="CSV Import",
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
      # d is now a dict of {columnname -> value} for this row
      # We use Python's **kwargs syntax to pass the whole dict as
      # keyword arguments
     # print(d['order_status'])
     # print(*d)
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
      escalation_type = app_tables.escalation_type.get(name= "Customer Not home"),
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
        user=app_tables.users.get(name= "System"),
        description="CSV Import",
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
      # d is now a dict of {columnname -> value} for this row
      # We use Python's **kwargs syntax to pass the whole dict as
      # keyword arguments
     # print(d['order_status'])
     # print(*d)
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
        user=app_tables.users.get(name= "System"),
        description="CSV Import",
        escalation_id=app_tables.webhook.get(id= str(counter)),
        job_id=app_tables.webhook.get(id= str(counter)),
        status = app_tables.escalation_status.get(name= "New"),
        created_date=datetime.now())
      counter += 1
      
    counter = get_next_value_in_sequence()
    compdf3= compdf3.loc[compdf3['completion_codes'].str.contains("202",na=False)]
    compdf3['completed_at'] = pd.to_datetime(compdf3['completed_at'])
    for d in compdf3.to_dict(orient="records"):
      # d is now a dict of {columnname -> value} for this row
      # We use Python's **kwargs syntax to pass the whole dict as
      # keyword arguments
     # print(d['order_status'])
     # print(*d)
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
        user=app_tables.users.get(name= "System"),
        description="CSV Import",
        escalation_id=app_tables.webhook.get(id= str(counter)),
        job_id=app_tables.webhook.get(id= str(counter)),
        status = app_tables.escalation_status.get(name= "New"),
        created_date=datetime.now())
      counter += 1


