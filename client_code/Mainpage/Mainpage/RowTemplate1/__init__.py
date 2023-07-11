from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...jobreport import jobreport

from ...Modal import Modal
import webbrowser

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    #self.data = data
    #self.orderSelectionRadio.set_event_handler("change", orderSelection_radio_clicked) 
    # Set Form properties and Data Bindings.
    #assign = None
    #status = None
    #description = ""
    
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    #self.repeating_panel_1.set_event_handler('x-jstatus', self.refresh_list)
  
  def jobreport_click(self, **event_args):
    """This method is called when the button is clicked"""
   
    webbrowser.open(self.item['job_report']) 
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
     large=True,

     buttons=[("Exit", False)], 
   )

    #if save_clicked:
      #anvil.server.call('add_comment', self.item, record_copy)
      #self.refresh_data_bindings()
      #self.parent.raise_event('x-edit-article', article=self.item)
      # Now refresh the page
      #self.refresh_data_bindings()

   

    



