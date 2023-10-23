from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
from .. import Data
from ..Data import *



class LoginForm(LoginFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.

    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def form_show (self, **event_args):
    # Do the code here to show this blank form.
    while anvil.users.get_user() is None:
      anvil.users.login_with_form()
      
    Data.currentUser=anvil.users.login_with_form()
    open_form('Homepage')