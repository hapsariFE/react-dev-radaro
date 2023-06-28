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
    users = anvil.server.call('get_user_list')
    self.users = [(x['name'], x) for x in users]
    #self.users = 'Danny'
    self.esc_status = Data.esc_status
    self.esc_type = Data.esc_type
    self.job_status = Data.job_status
    self.merchant_name = Data.merchant_name
    startDate= datetime.now()
    endDate = datetime.now()
    escType= None
    #jobValue = self.dd_job_status.selected_value
    compCode = None
    escStatus = None
    merchName = None
    #print(jobValue)

    self.status = Data.esc_status
    #self.assign = 'Danny'
    
    self.init_components(**properties) 
    # Any code you write here will run before the form opens.
    anvil.users.login_with_form()
    jobValue = if self.dd_job_status.selected_value == None
                row['job_status']
                else: row['job_status'] == self.dd_job_status.selected_value
    #print(*jobValue)
    self.refresh_list(jobValue,compCode,escType,escStatus,startDate,endDate)
    
    self.refresh_action()
  
  #def initialise_start_dates(self):
    """Initialise the DatePickers so that the filter auto-displays data for the previous week"""
   # self.date_filters['start'] = (date.today() - timedelta(days=6))
   # self.date_filters['end'] = date.today()
    
    
    
  #def filter_change(self, **event_args):
    """This method is called when an item is selected"""
    #jstatus = self.dd_job_status.selected_value
    #self.dd_job_status.raise_event('x-jstatus',jstatus=self.filters['job_status'])
    #self.dd_job_status.raise_event('x-jstatus')
    #self.parent.raise_event('x-jstatus')
    #self.refresh_data_bindings()
    #self.refresh_list(jstatus)
    #print(jstatus['name'])
    #alert("You changed the filter")


  #def date_change(self, **event_args):
    """This method is called when an item is selected"""

    #self.refresh_data_bindings()
   # self.refresh_list()
    #alert("You changed the date")

  def refresh_list(self,jobValue,compCode,escType,escStatus,startDate,endDate):
     #Load existing data from the Data Table, 
     #and display them in the RepeatingPanel+
    
    #print(**event_args)
    self.repeating_panel_1.items = anvil.server.call('get_list',jobValue,compCode,escType,escStatus,startDate,endDate)

  def refresh_action(self):
      # Load existing actions from the Data Table, 
      # and display them in the RepeatingPanel
      self.action_panel.items = anvil.server.call('get_action')
  
  def log_out_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()

  def filter_change(self, **event_args):
    """This method is called when an item is selected"""
    jobValue = self.dd_job_status.selected_value
    compCode = self.dd_completion_code.selected_value
    escType = self.dd_esc_type.selected_value
    escStatus = self.dd_esc_status.selected_value
    merchName = self.dd_merchant.selected_value
    startDate = self.start_date_picker.date
    endDate = self.end_date_picker.date
    #print(jobValue)
    #print(startDate)
    #print(endDate)
    self.refresh_list(jobValue,compCode,escType,escStatus,startDate,endDate)
    alert("You changed the filter")

  def submit_button_click(self, **event_args):
     
     description = self.addcomment.text
     status = self.dd_status.selected_value
     created_date = datetime.now()
     assign_to = self.dd_assign.selected_value
     #job_id = "15228"
     anvil.server.call('add_comment', description, status, created_date, assign_to)
     #Notification("Comment submitted!").show()
     alert("Comment Submitted")
     self.refresh_data_bindings()
     self.clear_inputs() 

  def clear_inputs(self):
    # Clear our input boxes
    self.addcomment.text = ""
    self.dd_status.selected_value = ""
    self.dd_assign.selected_value = ""
    self.refresh_data_bindings()
