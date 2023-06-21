import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

authenticated_callable = anvil.server.callable(require_user=True)

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
@authenticated_callable
def get_users():
  return app_tables.users.search()


@anvil.server.callable
def get_list():
  currentUser=anvil.users.get_user()
  #if filters.get('job_status') and filters['job_status'] == Data.NO_STATUS_SELECTED:
  #  filters['job_status'] = None
  # Get a list of escalation from the Data Table, sorted by 'date_created' column, in descending order
  return app_tables.webhook.search(webhook_merchant_link=q.any_of(*currentUser["user_merchant_link"])
    #tables.order_by("date_created", ascending=False),
    #tables.order_by("last_action_date", ascending=False)
    #,job_status=jstatus
      )

#return app_tables.articles.search(ArticleLink=q.any_of(*x['userMerchLink']))