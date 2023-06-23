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
def get_list(jobValue,compCode):
  currentUser=anvil.users.get_user()
  kwargs={'job_status':jobValue,'completion_code_id':compCode}
  #jobStatusValue = jobValue
  #print(jobStatusValue)
  #print(jobStatusValue['job_status'][0]['name']) 
  #for jobStatusValue in jobStatusValue:
   # print(jobStatusValue['name'])
  #if jobValue
  total = []
  for r in currentUser['user_merchant_link']:
    #print(*currentUser['user_merchant_link'])
    total += r
    print(r)
    
  links = [[r] for r in currentUser['user_merchant_link']]
  print(links)

#  app_tables.merchant.search(name=q.all_of(*currentUser['user_merchant_link']))
  #print(*currentUser['user_merchant_link'])
  #if filters.get('job_status') and filters['job_status'] == Data.NO_STATUS_SELECTED:
  #  filters['job_status'] = None
  # Get a list of escalation from the Data Table, sorted by 'date_created' column, in descending order
  custTable = app_tables.webhook.search(q.all_of(job_status=q.all_of(jobValue),completion_code_id=q.all_of(compCode),))
  return custTable
  #.search(**kwargs)
    #tables.order_by("date_created", ascending=False),
    #tables.order_by("last_action_date", ascending=False)
    #,job_status=jstatus
      

#return app_tables.articles.search(ArticleLink=q.any_of(*x['userMerchLink']))


@anvil.server.callable
def get_action():
  # Get a list of articles from the Data Table, sorted by 'created' column, in descending order
  return app_tables.action_log.search(
    tables.order_by("created_date")
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
