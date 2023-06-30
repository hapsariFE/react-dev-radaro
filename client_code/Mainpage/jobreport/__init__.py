from ._anvil_designer import jobreportTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import jQuery
from anvil.js import get_dom_node

class jobreport(jobreportTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.xy_panel_1 = None
    self.init_components(**properties)

  iframe = jQuery("<iframe width='100%' height='800px'>").attr("src","https://www.wired.co.uk/")
  iframe.appendTo(get_dom_node(self.xy_panel_1))




    # Any code you write here will run before the form opens.
