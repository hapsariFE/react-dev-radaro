from ._anvil_designer import Modal_wideTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Data
from datetime import datetime, timedelta, date
import webbrowser

class Modal_wide(Modal_wideTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.esc_status = Data.esc_status
    self.assigned = ""
    
    self.init_components(**properties)
    #print("------")
    # Any code you write here will run before the form opens.

    selectedRow = self.item
    SelectedMerchant = self.item['webhook_merchant_link']
    #print(selectedRow)
    assignList = anvil.server.call('get_selectedMerchant',SelectedMerchant)
    actionData = anvil.server.call('get_action',selectedRow)
    self.action_panelwide.items = actionData
    self.assigned = assignList
    if self.item['watch_list'] == False:
      self.favourite.source = "_/theme/Star%201.png"
    else:
      self.favourite.source= "_/theme/Star%20filled.png"
    self.refresh_data_bindings()


  def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    description = self.addcomment.text
    status = self.dd_status.selected_value
    created_date = datetime.now()
    assign_to = self.dd_assign.selected_value
    record_copy = dict(self.item)

    #print(assign_to)
    #print(created_date)
    #print(status)
    if assign_to is None:
      alert("Please select a Assignee")
    elif status is None:
      alert("Please select a Status")
    elif description is "":
      alert("Please submit a comment")
    else:
      anvil.server.call('add_comment',self.item, record_copy, description, status, created_date, assign_to)
      actionData = anvil.server.call('get_action',self.item)
      self.action_panelwide.items = actionData
      #alert("Comment Submitted")
      self.refresh_data_bindings()
      self.clear_button_click()
      Notification("Comment submitted!").show()

  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
        # Clear our input boxes
    self.addcomment.text = ""
    self.dd_status.selected_value = ""
    self.dd_assign.selected_value = ""
    self.refresh_data_bindings()

  def jobreport_click(self, **event_args):
    """This method is called when the button is clicked"""
   
    webbrowser.open(self.item['job_report']) 

  def update_item(self, **event_args):
    watch_list = self.item['watch_list']
    print(watch_list)
    if watch_list == False:
      watch_list = True
      self.favourite.source= "_/theme/Star%20filled.png"
      self.refresh_data_bindings()
    else:
      watch_list = False
      self.favourite.source = "_/theme/Star%201.png"
    row_id=self.item['id']
    anvil.server.call('update_item',row_id,watch_list)
    print(watch_list)
    self.refresh_data_bindings()