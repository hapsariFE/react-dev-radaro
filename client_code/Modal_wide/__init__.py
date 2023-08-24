from ._anvil_designer import Modal_wideTemplate
from anvil import *
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

class Modal_wide(Modal_wideTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    print('initiateModal start)'+str(datetime.now()))##################
    self.esc_status = esc_status
    self.assigned = ""
    print('initiateModal end)'+str(datetime.now()))##################

    self.init_components(**properties)
    print('Modal start)'+str(datetime.now()))##################
    #print("------")
    # Any code you write here will run before the form opens.

    selectedRow = self.item
    SelectedMerchant = self.item['webhook_merchant_link']
    #print(selectedRow)
    #print(self.item['watchlistUsers'])
    print('assignlist start)'+str(datetime.now()))##################
    assignList = anvil.server.call('get_selectedMerchant',SelectedMerchant)
    print('assignlist end)'+str(datetime.now()))##################
    print('actiondata start)'+str(datetime.now()))##################
    actionData = anvil.server.call('get_action',selectedRow)
    print('actiondata end)'+str(datetime.now()))##################
    self.action_panelwide.items = actionData
    self.assigned = assignList
    print('watch start)'+str(datetime.now()))##################
    if self.item['watchlistUsers'] is not None:
      if Data.currentUser in self.item['watchlistUsers']:
        self.favourite.source= "_/theme/Star%20filled.png"
      else:
        self.favourite.source = "_/theme/Star%20outline.png"
    else:
      self.favourite.source = "_/theme/Star%20outline.png"
    print('watch end)'+str(datetime.now()))##################
    print('refresh start)'+str(datetime.now()))##################
    self.refresh_data_bindings()
    print('refresh end)'+str(datetime.now()))##################
    print('Modal end)'+str(datetime.now()))##################


  def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    print('submit start)'+str(datetime.now()))##################
    description = self.addcomment.text
    status = self.dd_status.selected_value
    created_date = datetime.now(anvil.tz.tzlocal())
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
      #self.refresh_data_bindings()
      self.clear_button_click()
      print('submit end)'+str(datetime.now()))##################
      Notification("Your comment was submitted").show()

  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
        # Clear our input boxes
    print('clear start)'+str(datetime.now()))##################
    self.addcomment.text = ""
    self.dd_status.selected_value = ""
    self.dd_assign.selected_value = ""
    print('clear start)'+str(datetime.now()))##################
    print('refresh start)'+str(datetime.now()))##################
    self.refresh_data_bindings()
    print('refresh end)'+str(datetime.now()))##################

  def jobreport_click(self, **event_args):
    """This method is called when the button is clicked"""

    webbrowser.open(self.item['job_report'])

  def update_item(self, **event_args):
    print('update start)'+str(datetime.now()))##################
    print('watch start)'+str(datetime.now()))##################
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
    print('getuser start)'+str(datetime.now()))##################
    user = Data.currentUser
    print('getuser end)'+str(datetime.now()))##################
    anvil.server.call('update_item',article,user)
    print('update end)'+str(datetime.now()))##################
    print('refresh start)'+str(datetime.now()))##################
    self.refresh_data_bindings()
    print('refresh end)'+str(datetime.now()))##################
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
    record_copy = dict(self.item)
    
    print(*self.item)
    print(record_copy)
    
    
    #self.parent.raise_event("x-custom_event", record=actionData, assign=assignList)

    save_clicked = alert(
     content=Modal_wide(item = self.item),
     title="Job ID : " + self.item["job_reference"],
     large=True,
     buttons=[("Exit", False)],
   )



