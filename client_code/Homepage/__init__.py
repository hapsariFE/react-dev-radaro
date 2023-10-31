from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from .. import Data
from ..Data import *
from anvil.tables import app_tables
from datetime import datetime, timedelta, date
from ..New import *



class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    start_time = datetime.now()
    print('initiate start) '+str(datetime.now()))##################
    self.filters = {}
    self.date_filters = {} 
    self.users = ""
    self.esc_status = esc_status
    self.esc_type = esc_type
    self.job_status = job_status
    self.merchant_name = ""
    startDate= (date.today() - timedelta(days=60))
    endDate = (date.today() + timedelta(days=1))
    escType= None
    self.assigned = ""
    assigned_to = None
    compCode = None
    escStatus = None
    merchName = None

    self.start_date_picker.date = startDate
    self.end_date_picker.date = endDate
    self.status = esc_status
    actionData= None
    merchant_name = None
    searchText = None
    resolvedStatus = False
    watch = False
    self.subbrand = ""
    self.etype = ""
    print('initiate end) '+str(datetime.now()))##################
    
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    print('homepage start) '+str(datetime.now()))##################
    print('login start) '+str(datetime.now()))##################
    Data.currentUser=anvil.users.login_with_form()
    print('login end) '+str(datetime.now()))##################
    self.loggedin.text = 'logged in as '+Data.currentUser['name']
    print('filterget start)'+str(datetime.now()))##################  
    fUsers, ccVals,sVals,fmerch = anvil.server.call('get_filter_value')
    print('filterget end)'+str(datetime.now()))##################
    self.subbrand = sVals
    self.etype = ccVals
    self.merchant_name = fmerch
    users = fUsers
    self.users = [(x['name'], x) for x in users]
    
    if Data.currentUser['is_super_user'] == True:
      #print('true')
      self.cms.visible = True
    else:
      #print('false')
      self.cms.visible = False
    

    my_media = anvil.URLMedia(Data.currentUser['Logo'])
    self.image_2.source = my_media
    print('refresh_db start) '+str(datetime.now()))##################
    self.refresh_data_bindings()
    print('refresh_db end) '+str(datetime.now()))##################
    print('repeatingcustomevent start) '+str(datetime.now()))##################
    self.repeating_panel_1.set_event_handler("x-custom_event", self.handle_custom_event)
    print('repeatingcustomevent end) '+str(datetime.now()))##################
    print('repeatingfilterchange start) '+str(datetime.now()))##################
    self.repeating_panel_1.set_event_handler("x-edit-article", self.filter_change)
    print('repeatingfilterchange end) '+str(datetime.now()))##################
    print('refresh_db start) '+str(datetime.now()))##################
    self.refresh_data_bindings()
    print('refresh_db end) '+str(datetime.now()))##################
    self.start_date_picker.date = startDate
    jobValue = self.dd_job_status.selected_value
    self.end_date_picker.date = endDate
    
    print('refreshlist start) '+str(datetime.now()))##################
    self.refresh_list(jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch)
    print('refreshlist end) '+str(datetime.now()))##################
   # print('refreshlist end)'+str(datetime.now()))##################
   
    #itemlist = list()
    #for x in self.repeating_panel_1.items:
    #  itemlist.append(x['id'])
    #ires = []
    #for val in itemlist:
    #  if val != None:
     #   if val not in ires:
     #     ires.append(val)
    #self.itemlist = ires
    self.start_date_picker.date = startDate
    self.end_date_picker.date = endDate
    print('dates start) '+str(datetime.now()))##################
    self.initialise_start_dates()
    print('dates end) '+str(datetime.now()))##################
    print('refresh_db start) '+str(datetime.now()))##################
    self.refresh_data_bindings()
    print('refresh_db end) '+str(datetime.now()))##################
    #print(merchName)
    end_time = datetime.now()
    time_difference = (end_time - start_time).total_seconds()
    print("Time difference in seconds:", time_difference)
    #print(merchName)
    #self.set_pages()
    
  def initialise_start_dates(self):
    
    """Initialise the DatePickers so that the filter auto-displays data for the previous week"""
    self.date_filters['start'] = (date.today() - timedelta(days=60))
    self.date_filters['end'] = (date.today() + timedelta(days=1))    

  def refresh_list(self,jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch):
    #Load existing data from the Data Table, 
     #and display them in the RepeatingPanel+
    self.repeating_panel_1.items = anvil.server.call('get_list',jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch)
    #itemlist = list()
    #for x in self.repeating_panel_1.items:
    # itemlist.append(x['id'])
    #ires = []
    #for val in itemlist:
    #  if val != None:
     #   if val not in ires:
    #      ires.append(val)
    #self.itemlist = ires
    #self.set_pages()
  
  #def set_pages(self):
   # page = self.data_grid_1.get_page()  
   # no_rows = self.data_grid_1.rows_per_page
   # start_page = ((page + 1) * no_rows)
   # end_page = min(start_page, len(self.itemlist))
   # text = f"{(page * no_rows) + 1}-{end_page} of {len(self.itemlist)}"
   # self.label_1.text = text
   # print(page)
  
  def log_out_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    self.repeating_panel_1.items = None
    self.refresh_data_bindings()
    open_form('Homepage')

    
  def filter_change(self, **event_args):
    """This method is called when an item is selected"""
    jobValue = self.dd_job_status.selected_value
    compCode = self.dd_completion_code.selected_value
    escType = self.dd_esc_type.selected_value
    escStatus = self.dd_esc_status.selected_value
    merchant_name = self.dd_merchant.selected_value
    if self.start_date_picker.date is None:
      self.start_date_picker.date= (date.today() - timedelta(days=60))
    startDate = self.start_date_picker.date
    if self.end_date_picker.date is None:
      self.end_date_picker.date =(date.today() - timedelta(days=60))
    endDate = self.end_date_picker.date
    assigned_to = self.dd_assigned.selected_value
    searchText = self.text_box_search.text
    resolvedStatus = self.resolved_checkbox.checked
    watch = self.watch_list.checked
    if searchText is not "":
      self.clearbutton.visible = True
      self.text_box_search.visible = False
      self.clearbutton.text = searchText

    self.refresh_list(jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch)
    
    #self.set_pages()

  def handle_custom_event(self,record,assign, **event_args):
   self.action_panel.items = record
   self.assigned = assign
   self.refresh_data_bindings()
   
    
  def sorting_function(self, column_name, sorting_way):
    """function used for sorting in combination with headers""" 
    """https://anvil.works/forum/t/how-to-add-sorting-functionality-to-datagrid-with-repeating-panels/17750/6"""

  def clear_search(self, **event_args):
    self.text_box_search.text = None
    self.filter_change()
    self.clearbutton.visible = False
    self.text_box_search.visible = True
    
  def resolved_checkbox_click(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    jobValue = self.dd_job_status.selected_value
    compCode = self.dd_completion_code.selected_value
    escType = self.dd_esc_type.selected_value
    merchant_name = self.dd_merchant.selected_value
    startDate = self.start_date_picker.date
    endDate = self.end_date_picker.date
    assigned_to = self.dd_assigned.selected_value
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
    
  def new_escalation(self, **event_args):
    """This method is called when the button is clicked"""
    eres = self.etype
    save_clicked = alert(
     content=New(eres),
     title="Create a new escalation",
     large=False,
     buttons=[("Exit", False)],
   )
    self.filter_change()
    self.refresh_data_bindings()

  def show_filter(self, **event_args):
    """This method is called when the button is clicked"""
    self.call_js('filtercollapse')
  
  def cms_click(self, **event_args):
    """This method is called when the button is clicked"""
    if Data.currentUser['is_super_user'] == True:
      open_form('CMS')
    else:
      alert("you do not have authorisation")

  def reporting_click(self, **event_args):
    """This method is called when the button is clicked"""
    if Data.currentUser['is_reporting'] == True:
      open_form('Reporting')
    else:
      alert("you do not have authorisation")    
    
    
