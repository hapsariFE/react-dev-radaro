from ._anvil_designer import CMSTemplate
from anvil import *
import anvil.microsoft.auth
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta, date

class CMS(CMSTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.name = ""
    self.merchant_id = ""
    self.completion_code_enabled = ""
    self.fail_code_enabled = ""    
    self.low_rating_enabled = ""
    self.rating_threshold = ""
    
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    name = self.name
    fail_code_enabled = self.fail_code_enabled
    completion_code_enabled = self.completion_code_enabled
    low_rating_enabled = self.low_rating_enabled
    rating_threshold = self.rating_threshold
    
    cmsData = anvil.server.call('get_cms')
    self.repeating_panel_1.items = cmsData
  

  def Dashboard_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homepage')

  def dbUpdateButton_click(self, **event_args):
    """This method is called when the button is clicked"""
    now = datetime.now().astimezone()
    anvil.server.call('DB_task',now)
