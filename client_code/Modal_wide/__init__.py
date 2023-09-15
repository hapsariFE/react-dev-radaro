from ._anvil_designer import Modal_wideTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Data
from ..Data import *
from datetime import datetime, timedelta, date
import webbrowser
import anvil.tz
from form_checker import validation

class Modal_wide(Modal_wideTemplate):
  def __init__(self,ires, **properties):
    # Set Form properties and Data Bindings.
    
   # print('initiateModal start)'+str(datetime.now()))##################
    
    self.esc_status = esc_status
    self.assigned = ""
    createdif = ""
    actiondif = ""
    self.ires = ires
   # print('initiateModal end)'+str(datetime.now()))##################

    self.init_components(**properties)
    #print('Modal start)'+str(datetime.now()))##################
    #print("------")
    # Any code you write here will run before the form opens.
    createdif = datetime.now(anvil.tz.tzlocal()) - self.item['date_created']
    if createdif.seconds < 3600:
      createdif = str((createdif.seconds//60)%60) + " minutes"
    elif createdif.days < 1:
      createdif = str(createdif.seconds//3600) + " hours, " + str((createdif.seconds//60)%60) + " minutes"
    else:
      createdif = str(createdif.days) + " days, " + str(createdif.seconds//3600) + " hours"
    self.label_26.text = createdif
    actiondif = datetime.now(anvil.tz.tzlocal()) - self.item['last_action_date']
    if actiondif.seconds < 3600:
      actiondif = str((actiondif.seconds//60)%60) + " minutes"
    elif actiondif.days < 1:
      actiondif = str(actiondif.seconds//3600) + " hours, " + str((actiondif.seconds//60)%60) + " minutes"
    else:
      actiondif = str(actiondif.days) + " days, " + str(actiondif.seconds//3600) + " hours"
    self.label_27.text = actiondif
    selectedRow = self.item
    SelectedMerchant = self.item['webhook_merchant_link']
    self.next_record = None
    #print(selectedrow)
    #print("--")
    my_iterator = iter(ires)
    try: 
      for value in my_iterator:
        if value == selectedRow['id']:
            next_element = next(my_iterator)
            #print("Next Ele:" +next_element)
            self.next_record = next_element

    except StopIteration as e:
      self.button_1.visible = False

    #print(ires)

    reverseires = list(reversed(ires))
    #print(reverseires)

    reversemy_iterator = iter(reverseires)
    try: 
      for value in reversemy_iterator:
        #print(value)
        #print(selectedRow['id'])
        if value == selectedRow['id']:
            #print(value)
            #print(selectedRow['id'])
            #print(next(reversemy_iterator))
            prev_element = next(reversemy_iterator)
           #print("test:" + prev_element)
            self.prev_record = prev_element

    except StopIteration as e:
      self.button_2.visible = False
      #elif value != selectedRow['id']:
      #    self.button_1.visible = False
    #print(self.next_record)
   # if self.next_record is None:
   #   self.button_1.visible = False
      
    #jobrow = app_tables.webhook.get(id=str(counter)) 
    #print(selectedRow)
    #print(self.item)
    #print(SelectedMerchant)
    #print(counter)
    #print(jobrow)
    #Next = Row(selectedRow) + 1
    #print(Next)
    #print(self.item['watchlistUsers'])

   # print('assignlist start)'+str(datetime.now()))##################
    assignList = anvil.server.call('get_selectedMerchant',SelectedMerchant)
   # print('assignlist end)'+str(datetime.now()))##################
   # print('actiondata start)'+str(datetime.now()))##################
    actionData = anvil.server.call('get_action',selectedRow)
   # print('actiondata end)'+str(datetime.now()))##################
    self.action_panelwide.items = actionData
    self.assigned = assignList
   # print('watch start)'+str(datetime.now()))##################
    if self.item['watchlistUsers'] is not None:
      if Data.currentUser in self.item['watchlistUsers']:
        self.favourite.source= "_/theme/Star%20filled.png"
      else:
        self.favourite.source = "_/theme/Star%20outline.png"
    else:
      self.favourite.source = "_/theme/Star%20outline.png"
  #  print('watch end)'+str(datetime.now()))##################
   # print('refresh start)'+str(datetime.now()))##################
    #print(selectedRow['id'])
   # print(ires)
   # ires = ires

    self.refresh_data_bindings()
  #  print('refresh end)'+str(datetime.now()))##################
   # print('Modal end)'+str(datetime.now()))##################
    self.validator = validation.Validator()
    self.validator.require_text_field(self.addcomment, self.e_comment)
    self.validator.require(self.dd_status, ['change'],
                          lambda DropDown: DropDown.selected_value is not None,
                          self.e_status)
    self.validator.require(self.dd_assign, ['change'],
                          lambda DropDown: DropDown.selected_value is not None,
                          self.e_assign)    
          
    # Uncomment the line below to disable the button until the form is complete:
    self.validator.enable_when_valid(self.submit_button)

  def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    #print('submit start)'+str(datetime.now()))##################
    description = self.addcomment.text
    status = self.dd_status.selected_value
    created_date = datetime.now(anvil.tz.tzlocal())
    assign_to = self.dd_assign.selected_value
    record_copy = dict(self.item)
    submitter = Data.currentUser

    #print(assign_to)
    #print(created_date)
    #print(status)
       



    anvil.server.call('add_comment',self.item, record_copy, description, status, created_date, assign_to,submitter)
    actionData = anvil.server.call('get_action',self.item)
    self.action_panelwide.items = actionData
    self.clear_button_click()
    #print('submit end)'+str(datetime.now()))##################
      

  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
        # Clear our input boxes
   # print('clear start)'+str(datetime.now()))##################
    self.addcomment.text = ""
    self.dd_status.selected_value = ""
    self.dd_assign.selected_value = ""
  #  print('clear start)'+str(datetime.now()))##################
  #  print('refresh start)'+str(datetime.now()))##################
    self.refresh_data_bindings()
   # print('refresh end)'+str(datetime.now()))##################

  def jobreport_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.item['job_report'] is not None:
      webbrowser.open(self.item['job_report'])
    else: 
        alert('Job Report does not exist')
    

  def update_item(self, **event_args):
   # print('update start)'+str(datetime.now()))##################
   # print('watch start)'+str(datetime.now()))##################
    watchlistUsers = self.item['watchlistUsers']
    watch_list = self.item['watch_list']
    #print(watchlistUsers)
    if watchlistUsers is not None:
      if Data.currentUser in watchlistUsers:
        self.favourite.source = "_/theme/Star%20outline.png"
        print("Yes")
      elif Data.currentUser not in watchlistUsers:
        self.favourite.source= "_/theme/Star%20filled.png"
        print("No")
    print('watch end)'+str(datetime.now()))##################
    #if watch_list == False:
    #  watch_list = True
    #  self.favourite.source= "_/theme/Star%20filled.png"
    #  self.refresh_data_bindings()
   # else:
    #  watch_list = False
    #  self.favourite.source = "_/theme/Star%20outline.png"
    article=self.item
    #print('getuser start)'+str(datetime.now()))##################
    user = Data.currentUser
    #print('getuser end)'+str(datetime.now()))##################
    anvil.server.call('update_item',article,user)
   # print('update end)'+str(datetime.now()))##################
    #print('refresh start)'+str(datetime.now()))##################
    self.refresh_data_bindings()
   # print('refresh end)'+str(datetime.now()))##################
    #watch_list = self.item['watch_list']
    #if watch_list == False:
     # watch_list = True
     # self.favourite.source= "_/theme/Star%20filled.png"
     # self.refresh_data_bindings()
    #else:
     # watch_list = False
     # self.favourite.source = "_/theme/Star%20outline.png"
    #row_id=self.item['id']
   # anvil.server.call('update_item',row_id,watch_list)
    #self.refresh_data_bindings()

  def next_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form()
    
    #selectedRow = self.item
    #SelectedMerchant = self.item['webhook_merchant_link']
    #print(*SelectedMerchant)
    #assignList = anvil.server.call('get_selectedMerchant',SelectedMerchant)
    #actionData = anvil.server.call('get_action',selectedRow)
    #print("------")
    #print(list(assignList))
    #atest = assignList['name']
    #print(atest)
    #print(*assignList)
    #job_status = [(x['name'], x) for x in app_tables.job_status.search()]
    #[(x['name'], x) for x in users]
    #my_iterator = iter(ires)
    #for value in my_iterator:
     # if value == self.item['id']:
     #     next_element = next(my_iterator)
      #    print(next_element)
    next_item = anvil.server.call('get_record',self.next_record)   
    record_copy = dict(self.item)
    #print("aaaaaaaa")
    #print(*next_item)
    #print(*self.item)
    #print(record_copy)
    #n_i = next_item
    #print("llllll")
    #print(n_i)
    
    #self.parent.raise_event("x-custom_event", record=actionData, assign=assignList)

    self.raise_event("x-close-alert", value=42)
    save_clicked = alert(
     content=Modal_wide(item = next_item,ires = self.ires),
     title="Job ID : " + next_item["job_reference"],
     large=True,
     buttons=[("Exit", False)],
   )
    
  def prev_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form()
    
    #selectedRow = self.item
    #SelectedMerchant = self.item['webhook_merchant_link']
    #print(*SelectedMerchant)
    #assignList = anvil.server.call('get_selectedMerchant',SelectedMerchant)
    #actionData = anvil.server.call('get_action',selectedRow)
    #print("------")
    #print(list(assignList))
    #atest = assignList['name']
    #print(atest)
    #print(*assignList)
    #job_status = [(x['name'], x) for x in app_tables.job_status.search()]
    #[(x['name'], x) for x in users]
    #my_iterator = iter(ires)
    #for value in my_iterator:
     # if value == self.item['id']:
     #     next_element = next(my_iterator)
      #    print(next_element)
    prev_item = anvil.server.call('get_record',self.prev_record)   
    record_copy = dict(self.item)
    #print("aaaaaaaa")
    #print(*next_item)
    #print(*self.item)
    #print(record_copy)
    #n_i = next_item
    #print("llllll")
    #print(n_i)
    
    #self.parent.raise_event("x-custom_event", record=actionData, assign=assignList)

    self.raise_event("x-close-alert", value=42)
    save_clicked = alert(
     content=Modal_wide(item = prev_item,ires = self.ires),
     title="Job ID : " + prev_item["job_reference"],
     large=True,
     buttons=[("Exit", False)],
   )
    
