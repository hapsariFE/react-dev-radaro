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
    #users = anvil.server.call('get_user_list')
    self.users = ""
    #self.users = 'Danny'
    self.esc_status = Data.esc_status
    self.esc_type = Data.esc_type
    self.job_status = Data.job_status
    self.merchant_name = ""
    startDate= (date.today() - timedelta(days=60))
    endDate = date.today()
    escType= None
    self.assigned = ""
    #self.dd_assign=""
    
    #jobValue = self.dd_job_status.selected_value
    compCode = None
    escStatus = None
    merchName = None
    #print(jobValue)
    print(startDate)
    self.start_date_picker.date = startDate
    self.end_date_picker.date = endDate
    self.status = Data.esc_status
    actionData= None
    merchant_name = None
    #self.assign = 'Danny'
    
    self.init_components(**properties) 
    # Any code you write here will run before the form opens.
    anvil.users.login_with_form()
    self.repeating_panel_1.set_event_handler("x-custom_event", self.handle_custom_event)
    merchName = anvil.server.call('get_merchant_list')
    #print(merchant_name)
    self.merchant_name = merchName
    users = anvil.server.call('get_user_list')
    #x_rows = users['user_merchant_link']
    #x_list =[r['name'] for r in x_rows]
    #print(x_list)
    #print(users)
    
    self.users = [(x['name'], x) for x in users]
    self.refresh_data_bindings()
    self.start_date_picker.date = startDate
    jobValue = self.dd_job_status.selected_value
    self.end_date_picker.date = endDate
    #print(*jobValue)
    self.refresh_list(jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name)
    
    #self.refresh_action()
  
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

  def refresh_list(self,jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name):
     #Load existing data from the Data Table, 
     #and display them in the RepeatingPanel+
    
    #print(**event_args)
    self.repeating_panel_1.items = anvil.server.call('get_list',jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name)

  #def refresh_action(self):
      # Load existing actions from the Data Table, 
      # and display them in the RepeatingPanel
      #self.action_panel.items = anvil.server.call('get_action',None)
    
  def log_out_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()

  def filter_change(self, **event_args):
    """This method is called when an item is selected"""
    jobValue = self.dd_job_status.selected_value
    compCode = self.dd_completion_code.selected_value
    escType = self.dd_esc_type.selected_value
    escStatus = self.dd_esc_status.selected_value
    merchant_name = self.dd_merchant.selected_value
    startDate = self.start_date_picker.date
    endDate = self.end_date_picker.date
    #print(jobValue)
    #print(startDate)
    #print(endDate)
    self.refresh_list(jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name)
    #alert("You changed the filter")

  def submit_button_click(self, **event_args):
     
     description = self.addcomment.text
     status = self.dd_status.selected_value
     created_date = datetime.now()
     assign_to = self.dd_assign.selected_value
     
     print(assign_to)
     print(created_date)
     print(status)
     if assign_to is None:
       alert("Please select a Assignee")
     elif status is None:
       alert("Please select a Status")
     elif description is "":
       alert("Please submit a comment")
     else:
       anvil.server.call('add_comment', description, status, created_date, assign_to)
       alert("Comment Submitted")
       self.refresh_data_bindings()
       self.clear_inputs() 
     #Notification("Comment submitted!").show()
     

  def clear_inputs(self):
    # Clear our input boxes
    self.addcomment.text = ""
    self.dd_status.selected_value = ""
    self.dd_assign.selected_value = ""
    self.refresh_data_bindings()

  def handle_custom_event(self,record,assign, **event_args):
   
   self.action_panel.items = record
   self.assigned = assign
   self.refresh_data_bindings()
    