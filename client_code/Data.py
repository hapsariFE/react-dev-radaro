import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
"""This module collects global variables to be used throughout the app"""
import anvil.server
#import anvil.google.auth, anvil.google.drive
#from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


esc_status = [(x['name'], x) for x in app_tables.escalation_status.search()]
esc_type = [(x['name'], x) for x in app_tables.escalation_type.search()]
job_status = [(x['name'], x) for x in app_tables.job_status.search()]
#merchant_name = [(x['name'], x) for x in app_tables.merchant.search()]
NO_STATUS_SELECTED = 'None'
currentUser= None

