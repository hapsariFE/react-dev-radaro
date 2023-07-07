from ._anvil_designer import ModalTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Data

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
  