from ._anvil_designer import Modal_wideTemplate
from anvil import *
import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
from .. import Data
from ..Data import *
from datetime import datetime, timedelta, date
import webbrowser
import anvil.tz
from form_checker import validation
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Modal_wide(Modal_wideTemplate):
  def __init__(self,ires, **properties):
    # Set Form properties and Data Bindings.
    
    self.esc_status = esc_status
    self.assigned = ""
    createdif = ""
    actiondif = ""
    self.ires = ires
    
    self.init_components(**properties)
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
    my_iterator = iter(ires)
    try: 
      for value in my_iterator:
        if value == selectedRow['id']:
            next_element = next(my_iterator)
            self.next_record = next_element

    except StopIteration as e:
      self.button_1.enabled = False
    reverseires = list(reversed(ires))
    reversemy_iterator = iter(reverseires)
    try: 
      for value in reversemy_iterator:
        if value == selectedRow['id']:
            prev_element = next(reversemy_iterator)
            self.prev_record = prev_element

    except StopIteration as e:
      self.button_2.enabled = False
 
    assignList = anvil.server.call('get_selectedMerchant',SelectedMerchant)
    actionData = anvil.server.call('get_action',selectedRow)
    self.action_panelwide.items = actionData
    self.assigned = assignList
    if self.item['watchlistUsers'] is not None:
      if Data.currentUser in self.item['watchlistUsers']:
        self.favourite.source= "_/theme/Star%20filled.png"
      else:
        self.favourite.source = "_/theme/Star%20outline.png"
    else:
      self.favourite.source = "_/theme/Star%20outline.png"
    self.refresh_data_bindings()
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
    description = self.addcomment.text
    status = self.dd_status.selected_value
    created_date = datetime.now(anvil.tz.tzlocal())
    assign_to = self.dd_assign.selected_value
    record_copy = dict(self.item)
    submitter = Data.currentUser
    anvil.server.call('add_comment',self.item, record_copy, description, status, created_date, assign_to,submitter)
    if self.email_check.checked == True: 
      self.email()
    actionData = anvil.server.call('get_action',self.item)
    self.action_panelwide.items = actionData
    self.clear_button_click()

  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
        # Clear our input boxes
    self.addcomment.text = ""
    self.dd_status.selected_value = ""
    self.dd_assign.selected_value = ""
    self.refresh_data_bindings()

  def jobreport_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.item['job_report'] is not None:
      webbrowser.open(self.item['job_report'])
    else: 
        alert('Job Report does not exist')
    

  def update_item(self, **event_args):
    watchlistUsers = self.item['watchlistUsers']
    watch_list = self.item['watch_list']
    if watchlistUsers is not None:
      if Data.currentUser in watchlistUsers:
        self.favourite.source = "_/theme/Star%20outline.png"
        print("Yes")
      elif Data.currentUser not in watchlistUsers:
        self.favourite.source= "_/theme/Star%20filled.png"
        print("No")
    print('watch end)'+str(datetime.now()))##################
    article=self.item
    user = Data.currentUser
    anvil.server.call('update_item',article,user)
    self.refresh_data_bindings()

  def next_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form()
    next_item = anvil.server.call('get_record',self.next_record)   
    record_copy = dict(self.item)
    save_clicked = alert(
     content=Modal_wide(item = next_item,ires = self.ires),
     large=True,
     buttons=[("Exit", False)],
   )
   
    self.raise_event("x-close-alert", value=42)
    
  def prev_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form()
    prev_item = anvil.server.call('get_record',self.prev_record)   
    record_copy = dict(self.item)
    save_clicked = alert(
     content=Modal_wide(item = prev_item,ires = self.ires),
     large=True,
     buttons=[("Exit", False)],
   )
    
    self.raise_event("x-close-alert", value=42)
    
  def email(self, **event_args):
    """This method is called when the button is clicked"""
    
    record_copy = dict(self.item)
    submitter = Data.currentUser
    recipient = self.dd_assign.selected_value
    created_date = datetime.now(anvil.tz.tzlocal())
    status = self.dd_status.selected_value
    description = self.addcomment.text
    anvil.server.call('send_email', record_copy,description,status,created_date,recipient,submitter)

  def pdf(self, **event_args):
    """This method is called when the button is clicked"""

    pdf = anvil.server.call('create_pdf')
    anvil.media.download(pdf)




    
    
    
    
