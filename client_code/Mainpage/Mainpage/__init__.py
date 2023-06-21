from ._anvil_designer import MainpageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from ... import Data
from anvil.tables import app_tables
from datetime import datetime, timedelta, date

class Mainpage(MainpageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.filters = {}
    self.date_filters = {} 
    #users = anvil.server.call('get_users')
    #self.users = [(x['name'], x) for x in users]
    self.users = 'Danny'
    self.esc_status = Data.esc_status
    self.esc_type = Data.esc_type
    self.job_status = Data.job_status
    self.merchant_name = Data.merchant_name

    
    self.init_components(**properties) 
    # Any code you write here will run before the form opens.
    anvil.users.login_with_form()
    self.refresh_list()
  
  #def initialise_start_dates(self):
    """Initialise the DatePickers so that the filter auto-displays data for the previous week"""
   # self.date_filters['start'] = (date.today() - timedelta(days=6))
   # self.date_filters['end'] = date.today()
    
    
    
  def filter_change(self, **event_args):
    """This method is called when an item is selected"""
    jstatus = self.dd_job_status.selected_value
    #self.dd_job_status.raise_event('x-jstatus',jstatus=self.filters['job_status'])
    self.dd_job_status.raise_event('x-jstatus')
    #self.parent.raise_event('x-jstatus')
    #self.refresh_data_bindings()
    #self.refresh_list(jstatus)
    print(jstatus['name'])
    alert("You changed the filter")


  def date_change(self, **event_args):
    """This method is called when an item is selected"""

    self.refresh_data_bindings()
   # self.refresh_list()
    alert("You changed the date")

  def refresh_list(self):
     #Load existing data from the Data Table, 
     #and display them in the RepeatingPanel+
     self.repeating_panel_1.items = anvil.server.call('get_list')

  def log_out_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
