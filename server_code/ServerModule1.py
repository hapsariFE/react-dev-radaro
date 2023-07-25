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
@anvil.server.http_endpoint("/users/list")
def get_user_list():
  return [u['email'] for u in app_tables.users.search()]

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
    custTable = app_tables.webhook.search(tables.order_by("last_action_date"),**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*values),latest_assignee=q.any_of(*defaultassign),latest_status=q.any_of(*escStatus))

  elif merchant_name is None and assigned_to is not None :
    custTable = app_tables.webhook.search(tables.order_by("last_action_date"),**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*values),latest_status=q.any_of(*escStatus))

  elif merchant_name is not None and assigned_to is None :
    merchant_row = app_tables.merchant.search(name=merchant_name)
    #print(merchant_row)
    custTable = app_tables.webhook.search(tables.order_by("last_action_date"),**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*merchant_row),latest_assignee=q.any_of(*defaultassign),latest_status=q.any_of(*escStatus))

  else:
    #filter_dict['webhook_merchant_link'] = merchant_name
    merchant_row = app_tables.merchant.search(name=merchant_name)
    #print(merchant_row)
    custTable = app_tables.webhook.search(tables.order_by("last_action_date"),**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*merchant_row),latest_status=q.any_of(*escStatus))

  if searchText:
    custTable = [
      x for x in custTable
      if searchText.lower() in x['job_id'].lower()
      or searchText.lower() in x['job_reference'].lower()
      or searchText.lower() in x['customer_name'].lower() 
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
@anvil.server.callable
def search_webhook(query):
  result = app_tables.webhook.search()
  if query:
    result = [
      x for x in result
      if query in x['job_id'].lower()
      or query in x['job_reference'].lower()
      or query in x['customer_name'].lower() 
    ]
  return result

@anvil.server.callable
def update_item(row_id,watch_list):
  watch_list = watch_list
  row_id=row_id
  row=app_tables.webhook.get(id=row_id)  
  #job_id=article
    #if app_tables.webhook.has_row(article):
  row['watch_list']=watch_list
  #app_tables.webhook.update(row_id,watch_list)