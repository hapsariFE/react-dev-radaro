from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.text_box_2.align = 'left'

  def update_cms(self, **event_args):
    
    anvil.server.call('update_cms',
    rowid = self.item,
    name = self.text_box_2.text,
    token = self.text_box_1.text,
    server = self.text_box_3.text,
    merchant_id = self.text_box_4.text,
    completion_code_enabled = self.check_box_1.checked,
    low_rating_enabled = self.check_box_2.checked,
    rating_threshold = self.text_box_7.text
    )

                      
