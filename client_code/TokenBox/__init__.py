from ._anvil_designer import TokenBoxTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TokenBox(TokenBoxTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def add(self, text):
    """Add a token to the Flow Panel (and call the add_callback)."""
    token = Button(
      text=text,
      icon="fa:times",
      icon_align="left",
      role="primary-color",
    )
    token.set_event_handler("click", self.remove)
    self.flow_panel_1.add_component(token)

  def remove(self, **event_args):
    """Remove a token from the Flow Panel (and call the remove_callback)."""
    token = event_args['sender']
    token.remove_from_parent()

