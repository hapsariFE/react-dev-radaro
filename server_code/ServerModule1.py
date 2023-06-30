import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
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

@anvil.server.callable
def get_user_list():
  return app_tables.users.search()

#@anvil.server.callable
#def get_active_user():
#  active_user = anvil.users.get_user('name')
#  return active_user

@anvil.server.callable
def get_list(jobValue,compCode,escType,escStatus,startDate,endDate):
  currentUser=anvil.users.get_user()
  kwargs={'job_status':jobValue,'completion_code_id':compCode}
  total = []
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

  if jobValue != None:
    filter_dict['job_status'] = jobValue

  if compCode != None:
    filter_dict['completion_code_id'] = compCode

  if escType != None:
    filter_dict['escalation_type'] = escType

  if escStatus != None:
    filter_dict['escStatus'] = escStatus

  #print("-----")
  #print(*jjv)
  #selected_status_rows = [status_row for status_row in app_tables.webhook.search(job_status=q.any_of(*selected_statuses))]
  #print(selected_status_rows)
  related_rows = currentUser['user_merchant_link']
  #print(RelatedJobStatus)
  #print(related_rows)
  values = [row for row in related_rows]
  #print(values)
  

#  app_tables.merchant.search(name=q.all_of(*currentUser['user_merchant_link']))
  #print(*currentUser['user_merchant_link'])
  #if filters.get('job_status') and filters['job_status'] == Data.NO_STATUS_SELECTED:
  #  filters['job_status'] = None
  # Get a list of escalation from the Data Table, sorted by 'date_created' column, in descending order
  custTable = app_tables.webhook.search(**filter_dict,date_created=q.between(min=startDate,max=endDate),webhook_merchant_link=q.any_of(*values))
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
  print("-----aa")
  print(rowValue)
  print("-----bb")
  print(rowValue)
  if rowValue is None: 
    print("No Escalation Selected")
  else:
    return app_tables.action_log.search(tables.order_by("created_date"),escalation_id=q.any_of(rowValue)
    
  )

@anvil.server.callable
def add_comment(description, status, created_date, assign_to):
  app_tables.action_log.add_row(
    #job_id=job_id,
    user=anvil.users.get_user,
    description=description,
    status=status,
    created_date = created_date,
    assign_to=assign_to
  )
