from ._anvil_designer import ActionPageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Data

class ActionPage(ActionPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.esc_status = Data.esc_status
    self.assigned = ""
    #self.dd_assign = ""
    #self.dd_status = ""
    #print(self.item)
    
    self.init_components(**properties)
    print(self.item)
    selectedRow = self.item
    SelectedMerchant = self.item['webhook_merchant_link']
    #print(record_copy)
    assignList = anvil.server.call('get_selectedMerchant',SelectedMerchant)
    actionData = anvil.server.call('get_action',selectedRow)
    self.action_panel.items = record
    self.assigned = assign
    self.refresh_data_bindings()

    # Any code you write here will run before the form opens.
