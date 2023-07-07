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
    self.refresh_data_bindings()
    # Any code you write here will run before the form opens.
  
  def refresh_action(self):
      # Load existing actions from the Data Table, 
      # and display them in the RepeatingPanel
      self.m_action_panel.items = anvil.server.call('get_action',None)


  
  def handle_custom_event(self,record,assign, **event_args):
   
   self.m_action_panel.items = record
   self.assigned = assign
   self.refresh_data_bindings()