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
    self.x_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
    self.y_values = anvil.server.call('return_data', "2023")
    self.create_bar_graph()

  def create_bar_graph(self):
    self.plot_1.data = go.Bar(
        x=self.x_months,
        y=self.y_values[0]
        )
    data = anvil.server.call('get_graph1_data')
    print(resolved_tickets)
