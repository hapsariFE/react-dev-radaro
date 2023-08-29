from ._anvil_designer import testTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class test(testTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  
  def click_me_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.token_box_1.add("Gene 100")

  def search(self, **event_args):
    self.token_box_1.add(self.text_box_1.text)

