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
    
    #self.repeating_panel_1.set_event_handler('x-jstatus', self.refresh_list)
    
    #self.refresh_list(jstatus,**event_args)
    
  #def refresh_list(self, jstatus,**event_args):
    # Load existing data from the Data Table, 
    # and display them in the RepeatingPanel
    
   # self.repeating_panel_1.items = anvil.server.call('get_list',jstatus)
    #self.repeating_panel_1.items=app_tables.webhook.search(
    
    #tables.order_by("last_action_date", ascending=False)
    #,job_status=jstatus
     #)
    
    #self.repeating_panel_1.items = app_tables.webhook.search()