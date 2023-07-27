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
    endDate = (date.today() + timedelta(days=1))
    escType= None
    self.assigned = ""
    assigned_to = None
    
    #self.dd_assign=""
    
    #jobValue = self.dd_job_status.selected_value
    compCode = None
    escStatus = None
    merchName = None
    #print(jobValue)
    #print(startDate)
    self.start_date_picker.date = startDate
    self.end_date_picker.date = endDate
    self.status = Data.esc_status
    actionData= None
    merchant_name = None
    searchText = None
    resolvedStatus = False
    watch = False
    
    #self.assign = 'Danny'
    
    self.init_components(**properties) 
    # Any code you write here will run before the form opens.
    anvil.users.login_with_form()
    currentUser=anvil.users.get_user()
    my_media = anvil.URLMedia(currentUser['Logo'])
    #self.image_2.source = my_media
    self.refresh_data_bindings()
    #print("test1")
    self.repeating_panel_1.set_event_handler("x-custom_event", self.handle_custom_event)
    self.repeating_panel_1.set_event_handler("x-edit-article", self.filter_change)
    merchName = anvil.server.call('get_merchant_list')
    #print(merchant_name)
    self.merchant_name = merchName
    users = anvil.server.call('get_user_list')
    #print(merchName)
    #x_rows = users['user_merchant_link']
    #x_list =[r['name'] for r in x_rows]
    #print(x_list)
    #print(users)
    
    self.users = [(x['name'], x) for x in users]
    self.refresh_data_bindings()
    self.start_date_picker.date = startDate
    jobValue = self.dd_job_status.selected_value
    self.end_date_picker.date = endDate
    #print(self.start_date_picker.date)
    #print("test2")
    self.refresh_list(jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch)
    
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

  def refresh_list(self,jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch):
     #Load existing data from the Data Table, 
     #and display them in the RepeatingPanel+
    
    #print(**event_args)
    self.repeating_panel_1.items = anvil.server.call('get_list',jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch)

  #def refresh_action(self):
      # Load existing actions from the Data Table, 
      # and display them in the RepeatingPanel
      #self.action_panel.items = anvil.server.call('get_action',None)
    
  def log_out_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    self.repeating_panel_1.items = None
    self.refresh_data_bindings()
    open_form('Mainpage.Mainpage')

  def filter_change(self, **event_args):
    """This method is called when an item is selected"""
    jobValue = self.dd_job_status.selected_value
    compCode = self.dd_completion_code.selected_value
    escType = self.dd_esc_type.selected_value
    escStatus = self.dd_esc_status.selected_value
    merchant_name = self.dd_merchant.selected_value
    startDate = self.start_date_picker.date
    endDate = self.end_date_picker.date
    assigned_to = self.dd_assigned.selected_value
    searchText = self.text_box_search.text
    resolvedStatus = self.resolved_checkbox.checked
    #watch = False

    if searchText is not "":
      #print(searchText == "")
      self.clear_icon.visible = True
      
    #print(jobValue)
    #print(startDate)
    #print(endDate)
    self.refresh_list(jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch)
    #alert("You changed the filter")
  
  def handle_custom_event(self,record,assign, **event_args):
   
   self.action_panel.items = record
   self.assigned = assign
   self.refresh_data_bindings()

  def sorting_function(self, column_name, sorting_way):
    """function used for sorting in combination with headers""" 
    """https://anvil.works/forum/t/how-to-add-sorting-functionality-to-datagrid-with-repeating-panels/17750/6"""

  #def search(self, **event_args):
  #  self.repeating_panel_1.items = anvil.server.call(
  #    'search_webhook',
  #    self.text_box_search.text
  #  )
   # self.clear_icon.visible = True

  def clear_search(self, **event_args):
    self.text_box_search.text = None
    self.filter_change()
    #jobValue = self.dd_job_status.selected_value
    #compCode = self.dd_completion_code.selected_value
    #escType = self.dd_esc_type.selected_value
    #escStatus = self.dd_esc_status.selected_value
    #merchant_name = self.dd_merchant.selected_value
    #startDate = self.start_date_picker.date
    #endDate = self.end_date_picker.date
    #assigned_to = self.dd_assigned.selected_value
    #self.repeating_panel_1.items = anvil.server.call('get_list',jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to)
    self.clear_icon.visible = False

  def resolved_checkbox_click(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    jobValue = self.dd_job_status.selected_value
    compCode = self.dd_completion_code.selected_value
    escType = self.dd_esc_type.selected_value
    merchant_name = self.dd_merchant.selected_value
    startDate = self.start_date_picker.date
    endDate = self.end_date_picker.date
    assigned_to = self.dd_assigned.selected_value
    ##escStatus = self.dd_esc_status.selected_value
    ##self.item['Resolved'] = self.resolved_checkbox.checked
    if self.resolved_checkbox.checked == True:
      escStatus = app_tables.escalation_status.get(name="Resolved")
    else:
      escStatus = self.dd_esc_status.selected_value
    self.repeating_panel_1.items = anvil.server.call('get_list',jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,resolvedStatus,watch)


  def filter_display(self, **event_args):
    if self.grid_panel_1.visible:
      self.grid_panel_1.visible = False
      self.button_2.icon = 'fa:angle-down'
    else:
      self.grid_panel_1.visible = True
      self.button_2.icon = 'fa:angle-up'

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    anvil.server.call('manual_import',file)
    self.filter_change()
    self.refresh_data_bindings()
    
    


    




    
    

  
    
