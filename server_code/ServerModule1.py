import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta, date

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
def get_list(jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to):
  currentUser=anvil.users.get_user()
  kwargs={'job_status':jobValue,'completion_code_id':compCode}
  total = []
  assignrow = app_tables.users.get(name=assigned_to)
  print(assignrow)
  defaultassign = get_user_list()
  print(*defaultassign)
  print(*[r for r in defaultassign])
  if assignrow == None:
    assignrow = [[r] for r in defaultassign]

  
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
  #if assignrow != None:
  #  filter_dict['latest_assignee'] = assignrow

  if jobValue != None:
    filter_dict['job_status'] = jobValue

  if compCode != None:
    filter_dict['completion_code_id'] = compCode

  if escType != None:
    filter_dict['escalation_type'] = escType

  if escStatus != None:
    filter_dict['latest_status'] = escStatus

  
    

  #print("-----")
  #print(*jjv)
  #selected_status_rows = [status_row for status_row in app_tables.webhook.search(job_status=q.any_of(*selected_statuses))]
  #print(selected_status_rows)
  
  #print(values)
  
  related_rows = currentUser['user_merchant_link']
    #print(RelatedJobStatus)
    #print(related_rows)
  values = [row for row in related_rows]
  if merchant_name is None:
    custTable = app_tables.webhook.search(**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*values))

  else:
    #filter_dict['webhook_merchant_link'] = merchant_name
    merchant_row = app_tables.merchant.search(name=merchant_name)
    #print(merchant_row)
    custTable = app_tables.webhook.search(**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*merchant_row))

  

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
