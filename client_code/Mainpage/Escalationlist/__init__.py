from ._anvil_designer import EscalationlistTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Escalationlist(EscalationlistTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def refresh_list(self):
    # Load existing data from the Data Table, 
    # and display them in the RepeatingPanel
    self.articles_panel.items = anvil.server.call('get_list')
    self.articles_panel.items = anvil.server.call('get_list')
    
    #self.repeating_panel_1.items = app_tables.webhook.search()