from ._anvil_designer import jobreportTemplate
from anvil import *
import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
from anvil.js.window import jQuery
from anvil.js import get_dom_node

class jobreport(jobreportTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    #self.xy_panel_1 = None
    self.init_components(**properties)

    iframe = jQuery("<iframe width='100%' height='100%'>").attr("src","https://account.radaro.com.au/public-report/MTk5/1a5dbc5e-1360-4bb8-ace2-5e2895037849?domain=api-2.radaro.com.au&cluster_number=s2")
    iframe.appendTo(get_dom_node(self.xy_panel_1))




    # Any code you write here will run before the form opens.
