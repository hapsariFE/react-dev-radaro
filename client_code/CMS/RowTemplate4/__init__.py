from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.microsoft.auth
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users

class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    

  def update_cms(self, **event_args):
    
    anvil.server.call('update_cms',
    rowid = self.item,
    name = self.text_box_2.text,
    fail_code_enabled = self.check_box_3.checked,
    completion_code_enabled = self.check_box_1.checked,
    low_rating_enabled = self.check_box_2.checked,
    rating_threshold = self.text_box_7.text
    )

                      
