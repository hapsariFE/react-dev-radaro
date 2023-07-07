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
    
    self.init_components(**properties)
    
    
    

    # Any code you write here will run before the form opens.
