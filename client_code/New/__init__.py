from ._anvil_designer import NewTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Data import *

class New(NewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.esc_status = esc_status
    self.esc_type = esc_type
    
    self.init_components(**properties)
    # Any code you write here will run before the form opens.






  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
        # Clear our input boxes
    self.job_input.text = ""
    self.customer_input.text = ""
    self.mobile_input.text = ""
    self.subbrand_input.text = ""
    self.dd_esc_status.selected_value = ""
    self.dd_esc_type.selected_value = ""
    self.refresh_data_bindings()

