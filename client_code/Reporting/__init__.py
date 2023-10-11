from ._anvil_designer import ReportingTemplate
from anvil import *
import plotly.graph_objects as go
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
from datetime import datetime, timedelta, date


class Reporting(ReportingTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    

    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    
    fig = anvil.server.call('create_fig') 
    self.plot_1.figure = fig
    

