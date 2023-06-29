from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import webbrowser

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    #self.data = data
    #self.orderSelectionRadio.set_event_handler("change", orderSelection_radio_clicked) 
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    #self.repeating_panel_1.set_event_handler('x-jstatus', self.refresh_list)
  
  def jobreport_click(self, **event_args):
    """This method is called when the button is clicked"""
    webbrowser.open(self.item['job_report'])

  def orderSelection_radio_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    selectedRow = self.item
    actionData = anvil.server.call('get_action',selectedRow)

    #self.raise_event("custom_event", actionData)
    
    print(*actionData)
    values = [row for row in actionData]
    print(*values)
   

    



