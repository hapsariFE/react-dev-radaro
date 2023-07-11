from ._anvil_designer import ModalTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Data
from datetime import datetime, timedelta, date

class Modal(ModalTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.esc_status = Data.esc_status
    self.assigned = ""
    
    self.init_components(**properties)
    print("------")
    
    selectedRow = self.item
    SelectedMerchant = self.item['webhook_merchant_link']
    print(selectedRow)
    assignList = anvil.server.call('get_selectedMerchant',SelectedMerchant)
    actionData = anvil.server.call('get_action',selectedRow)
    self.action_panel.items = actionData
    self.assigned = assignList
    self.refresh_data_bindings()
    # Any code you write here will run before the form opens.

  def form_change(self, **event_args):
    """This method is called when an item is selected"""
    assign = self.dd_assign.selected_value
    status = self.dd_status.selected_value
    description = self.addcomment.text
    print(description)
    #self.parent.raise_event()

  def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
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
     anvil.server.call('add_comment',self.item, description, status, created_date, assign_to)
     alert("Comment Submitted")
     self.refresh_data_bindings()
     self.clear_inputs() 
     Notification("Comment submitted!").show()

  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
        # Clear our input boxes
    self.addcomment.text = ""
    self.dd_status.selected_value = ""
    self.dd_assign.selected_value = ""
    self.refresh_data_bindings()



  