from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from ... import Data
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...jobreport import jobreport
from ...Modal_wide import Modal_wide
#from ...Modal import Modal
import webbrowser
import anvil.tz
from datetime import datetime, timedelta, date

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    print('initiaterow start)'+str(datetime.now()))##################
    #self.data = data
    #self.orderSelectionRadio.set_event_handler("change", orderSelection_radio_clicked)
    # Set Form properties and Data Bindings.
    #assign = None
    #status = None
    #description = ""
    #self.label_2.text = str(self.item['last_action_date'].astimezone(anvil.tz.tzlocal()))
    print('initiaterow end)'+str(datetime.now()))##################

    self.init_components(**properties)
    print('rowtemplate start)'+str(datetime.now()))##################
    #print(self.item['latest_status']['name'])
    #if self.item['job_status']['name'] == "Failed":
      #self.label_4.bold = True
     # my_media = anvil.URLMedia("https://radaro-api.s3.ap-southeast-2.amazonaws.com/media-2/Merchant/b0cc7b64-7f6a-4392-8043-54437660de96.png")
      #self.label_1.icon = my_media
      #print(my_media)
     # self.label_1.background = "Black"
      #self.refresh_data_bindings()
    #  self.label_1.background = "Black"
    #self.label_2.text = self.item['last_action_date'].astimezone(anvil.tz.tzlocal())
    print('watchlist start)'+str(datetime.now()))##################
    if self.item['watchlistUsers'] is not None:
      if Data.currentUser in self.item['watchlistUsers']:
        self.favourite.source= "_/theme/Star%20filled.png"
      else:
        self.favourite.source = "_/theme/Star%20outline.png"
    else:
      self.favourite.source = "_/theme/Star%20outline.png"
    print('watchlist end)'+str(datetime.now()))##################
    #print('refresh start)'+str(datetime.now()))##################
    #self.refresh_data_bindings()
    #print('refresh end)'+str(datetime.now()))##################
    #elif
    print('rowtemplate end)'+str(datetime.now()))##################


    #self.refresh_data_bindings()
    # Any code you write here will run before the form opens.
    #self.repeating_panel_1.set_event_handler('x-jstatus', self.refresh_list)

  def jobreport_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.item['job_report'] is not None:
      webbrowser.open(self.item['job_report'])
    else: 
        alert('Job Report does not exist')



  """
  def orderSelection_radio_clicked(self, **event_args):
    #This method is called when this radio button is selected
    selectedRow = self.item
    SelectedMerchant = self.item['webhook_merchant_link']
    #print(*SelectedMerchant)
    assignList = anvil.server.call('get_selectedMerchant',SelectedMerchant)
    actionData = anvil.server.call('get_action',selectedRow)
    #print("------")
    #print(list(assignList))
    #atest = assignList['name']
    #print(atest)
    #print(*assignList)
    self.parent.raise_event("x-custom_event", record=actionData, assign=assignList)

    #print(*actionData)
    #values = [row for row in actionData]
    #print(*values)

  def comment_button_click(self, **event_args):
   #This method is called when the button is clicked
   # print(*self.item)
   # selectedRow = self.item
    record_copy = dict(self.item)
   # SelectedMerchant = self.item['webhook_merchant_link']
   # print(record_copy)
    #assignList = anvil.server.call('get_selectedMerchant',SelectedMerchant)
    #actionData = anvil.server.call('get_action',selectedRow)
    alert(
      content=ActionPage(item=record_copy),
      title="Action Log",
      large=True,
   )
"""
  def comment_click(self, **event_args):
    """This method is called when the button is clicked"""
    print('comment start)'+str(datetime.now()))##################
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
    record_copy = dict(self.item)
    #print(*self.item)
    #self.parent.raise_event("x-custom_event", record=actionData, assign=assignList)

    save_clicked = alert(
     content=Modal(item = self.item),
     title="Job ID : " + self.item["job_reference"],
     #large=True,


     buttons=[("Exit", False)],
   )
    print('comment end)'+str(datetime.now()))##################
    #if save_clicked:
      #anvil.server.call('add_comment', self.item, record_copy)
      #self.refresh_data_bindings()
    print('editarticle start)'+str(datetime.now()))##################
    self.parent.raise_event('x-edit-article', article=self.item)
    print('editarticle end)'+str(datetime.now()))##################
      # Now refresh the page
    print('refresh start)'+str(datetime.now()))##################
    self.refresh_data_bindings()
    print('refresh end)'+str(datetime.now()))##################
    
  def widecomment_click(self, **event_args):
    """This method is called when the button is clicked"""
    print('comment start)'+str(datetime.now()))##################
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
    record_copy = dict(self.item)
    #print(*self.item)
    #self.parent.raise_event("x-custom_event", record=actionData, assign=assignList)

    save_clicked = alert(
     content=Modal_wide(item = self.item),
     title="Job ID : " + self.item["job_reference"],
     large=True,


     buttons=[("Exit", False)],
   )
    print('comment end)'+str(datetime.now()))##################

    #if save_clicked:
      #anvil.server.call('add_comment', self.item, record_copy)
      #self.refresh_data_bindings()
    print('editarticle start)'+str(datetime.now()))##################
    self.parent.raise_event('x-edit-article', article=self.item)
    print('editarticle end)'+str(datetime.now()))##################
      # Now refresh the page
    print('refresh start)'+str(datetime.now()))##################
    self.refresh_data_bindings()
    print('refresh end)'+str(datetime.now()))##################

  def update_item(self, **event_args):
    print('watchupdate start)'+str(datetime.now()))##################
    watch_list = self.watch.checked
    row_id=self.item['id']
    anvil.server.call('update_item',row_id,watch_list)
    print('watchupdate end)'+str(datetime.now()))##################

  def update_item2(self, **event_args):
    """This method is called when the link is clicked"""
    print('watchupdate start)'+str(datetime.now()))##################
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
        
    #if watch_list == False:
    #  watch_list = True
    #  self.favourite.source= "_/theme/Star%20filled.png"
    #  self.refresh_data_bindings()
   # else:
    #  watch_list = False
    #  self.favourite.source = "_/theme/Star%20outline.png"
    article=self.item
    user = Data.currentUser
    anvil.server.call('update_item',article,user)
    print('watchupdate end)'+str(datetime.now()))##################
    print('refresh start)'+str(datetime.now()))##################
    self.refresh_data_bindings()
    print('refresh end)'+str(datetime.now()))##################
