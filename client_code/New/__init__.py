from ._anvil_designer import NewTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
#from ..Data import *

class New(NewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    #self.esc_status = esc_status
    #self.esc_type = esc_type
    
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
