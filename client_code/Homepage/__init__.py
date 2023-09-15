from ._anvil_designer import HomepageTemplate
from anvil import *
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
    #print('initiate start)'+str(datetime.now()))##################
    self.filters = {}
    self.date_filters = {} 
    #users = anvil.server.call('get_user_list')
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
    #self.loggedin.text = anvil.users.get_user()['name']
    
    compCode = None
    escStatus = None
    merchName = None
    #print(jobValue)
    #print(startDate)
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
    #print('initiate end)'+str(datetime.now()))##################
 
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    #print('homepage start)'+str(datetime.now()))##################
    #print('login start)'+str(datetime.now()))##################
    Data.currentUser=anvil.users.login_with_form()
    self.loggedin.text = 'logged in as '+Data.currentUser['name']
    if Data.currentUser['is_super_user'] == True:
      print('true')
      self.cms.visible = True
    else:
      print('false')
      self.cms.visible = False
   # print('login end)'+str(datetime.now()))##################
    #print('getuser start)'+str(datetime.now()))##################
    #currentUser=anvil.users.get_user()
    #print('getuser end)'+str(datetime.now()))##################
    my_media = anvil.URLMedia(Data.currentUser['Logo'])
    self.image_2.source = my_media
    #print('refresh start)'+str(datetime.now()))##################
    self.refresh_data_bindings()
    #print('refresh end)'+str(datetime.now()))##################
    #print("test1")
    #print('repeatingcustomevent start)'+str(datetime.now()))##################
    self.repeating_panel_1.set_event_handler("x-custom_event", self.handle_custom_event)
    #print('repeatingcustomevent end)'+str(datetime.now()))##################
    #print('repeatingfilterchange start)'+str(datetime.now()))##################
    self.repeating_panel_1.set_event_handler("x-edit-article", self.filter_change)
   # print('repeatingfilterchange end)'+str(datetime.now()))##################
    #print('getmerchant start)'+str(datetime.now()))##################
    merchName = anvil.server.call('get_merchant_list')
   # print('getmerchant end)'+str(datetime.now()))##################
    #print(merchant_name)
    self.merchant_name = merchName
   # print('userlist start)'+str(datetime.now()))##################
    users = anvil.server.call('get_user_list')
   # print('userlist end)'+str(datetime.now()))##################
    #print(merchName)
    #x_rows = users['user_merchant_link']
    #x_list =[r['name'] for r in x_rows]
    #print(x_list)
    #print(users)
    
    self.users = [(x['name'], x) for x in users]
   # print('refresh start)'+str(datetime.now()))##################
    self.refresh_data_bindings()
   # print('refresh end)'+str(datetime.now()))##################
    self.start_date_picker.date = startDate
    jobValue = self.dd_job_status.selected_value
    self.end_date_picker.date = endDate
    #print(self.start_date_picker.date)
    #print("test2")
   # print('refreshlist start)'+str(datetime.now()))##################
    self.refresh_list(jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch)
   # print('refreshlist end)'+str(datetime.now()))##################
   # print('subbrand start)'+str(datetime.now()))##################
    subbrands = list()
    for x in self.repeating_panel_1.items:
      subbrands.append(x['sub_brand'])
    res = []
    for val in subbrands:
      if val != None:
        if val not in res:
          res.append(val)
    res.sort()
    self.subbrand = res
   # print('subbrand end)'+str(datetime.now()))##################
   # print('etype start)'+str(datetime.now()))##################
    etypes = list()
    for x in self.repeating_panel_1.items:
      etypes.append(x['completion_code_description'])
    eres = []
    for val in etypes:
      if val != None:
        if val not in eres:
          eres.append(val)
    eres.sort()
    self.etype = eres
   # print('etype end)'+str(datetime.now()))##################  
   # print('itemlist start)'+str(datetime.now()))##################
    itemlist = list()
    for x in self.repeating_panel_1.items:
      itemlist.append(x['id'])
    ires = []
    for val in itemlist:
      if val != None:
        if val not in ires:
          ires.append(val)
    self.itemlist = ires
    #print(ires)
   # print('itemlist end)'+str(datetime.now()))##################  
    self.start_date_picker.date = startDate
    self.end_date_picker.date = endDate
    #print(endDate)
   # print('dates start)'+str(datetime.now()))##################
    self.initialise_start_dates()
   # print('dates end)'+str(datetime.now()))##################
   # print('refresh start)'+str(datetime.now()))##################
    self.refresh_data_bindings()
   # print('refresh end)'+str(datetime.now()))##################
    #if self.filterpanel.visible == True:
      #self.filterbutton.role = '.anvil-role-outlined-button > .btn:focus'
      #self.filterbutton.icon = 'fa:angle-up'
      #self.filterbutton.role = '.anvil-role-outlined-button > .btn'
    #else: 
      #self.filterbutton.role = '.anvil-role-outlined-button > .btn:focus'
      
    #self.refresh_action()
  #  print('homepage end)'+str(datetime.now()))##################
  def initialise_start_dates(self):
    
    """Initialise the DatePickers so that the filter auto-displays data for the previous week"""
    self.date_filters['start'] = (date.today() - timedelta(days=60))
    self.date_filters['end'] = (date.today() + timedelta(days=1))

    
    
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
    #print('refresh list start)'+str(datetime.now()))##################
    #Load existing data from the Data Table, 
     #and display them in the RepeatingPanel+
    
    #print(**event_args)
    #print('repeatingpanel start)'+str(datetime.now()))##################
    self.repeating_panel_1.items = anvil.server.call('get_list',jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch)
   # print('itemlist start)'+str(datetime.now()))##################
    itemlist = list()
    for x in self.repeating_panel_1.items:
      itemlist.append(x['id'])
    ires = []
    for val in itemlist:
      if val != None:
        if val not in ires:
          ires.append(val)
    self.itemlist = ires
   # print(ires)
    #print('itemlist end)'+str(datetime.now()))##################  
    #print(self.repeating_panel_1.items['sub_brand'])
   # print('repeatingpanel end)'+str(datetime.now()))##################
      
    #self.subbrand = self.repeating_panel_1.items[merchant_name]
  #def refresh_action(self):
      # Load existing actions from the Data Table, 
      # and display them in the RepeatingPanel
      #self.action_panel.items = anvil.server.call('get_action',None)
    #print('refresh list end)'+str(datetime.now()))##################
    
  def log_out_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    self.repeating_panel_1.items = None
    self.refresh_data_bindings()
    open_form('Homepage')

    
  def filter_change(self, **event_args):
    """This method is called when an item is selected"""
    #print('filterchange start)'+str(datetime.now()))##################
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
      #print(searchText == "")
      self.clearbutton.visible = True
      self.text_box_search.visible = False
      self.clearbutton.text = searchText
      
    #print(jobValue)
    #print(startDate)
    #print(endDate)
    self.refresh_list(jobValue,compCode,escType,escStatus,startDate,endDate,merchant_name,assigned_to,searchText,resolvedStatus,watch)
    #alert("You changed the filter")
    #print('filterchange end)'+str(datetime.now()))##################

  def handle_custom_event(self,record,assign, **event_args):
   #print('customevent start)'+str(datetime.now()))##################
   self.action_panel.items = record
   self.assigned = assign
   self.refresh_data_bindings()
   #print('customevent end)'+str(datetime.now()))##################
    
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
    #print('clearsearch start)'+str(datetime.now()))##################
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
    self.clearbutton.visible = False
    self.text_box_search.visible = True
    #print('clearsearch end)'+str(datetime.now()))##################
    
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
    #print('filterdisplay start)'+str(datetime.now()))##################
    if self.grid_panel_1.visible:
      self.grid_panel_1.visible = False
      self.button_2.icon = 'fa:angle-down'
    else:
      self.grid_panel_1.visible = True
      self.button_2.icon = 'fa:angle-up'

    #print('filterdisplay end)'+str(datetime.now()))##################
      
  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    anvil.server.call('manual_import',file)
    self.filter_change()
    self.refresh_data_bindings()    
    
  def new_escalation(self, **event_args):
    """This method is called when the button is clicked"""
    eres = self.etype
    #print('newescalation start)'+str(datetime.now()))##################
    save_clicked = alert(
     content=New(eres),
     title="Create a new escalation",
     large=False,
     buttons=[("Exit", False)],
   )
   # print('newescalation end)'+str(datetime.now()))##################
    #self.raise_event("x-close-alert", article=self.item)
    #self.raise_event("x-edit-article", article=self.item)
    self.filter_change()
    self.refresh_data_bindings()

  def show_filter(self, **event_args):
    """This method is called when the button is clicked"""
    self.call_js('filtercollapse')
  
  def cms_click(self, **event_args):
    """This method is called when the button is clicked"""
    if Data.currentUser['is_super_user'] == True:
      #print('true')
      open_form('CMS')
    else:
      alert("you do not have authorisation")

    
    
    