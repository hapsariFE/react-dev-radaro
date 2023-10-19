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
    #pie chart last week
    create_stat1 = anvil.server.call('create_stat1') 
    self.plot_6.figure = create_stat1

    #bar chart last week vs this week
    create_stat2 = anvil.server.call('create_stat2') 
    self.plot_7.figure = create_stat2

    #response by user
    create_chart1 = anvil.server.call('create_chart1') 
    self.plot_1.figure = create_chart1

    #tickets by escalation type
    create_chart2 = anvil.server.call('create_chart2') 
    self.plot_2.figure = create_chart2

    #tickets by creation date
    create_chart3 = anvil.server.call('create_chart3') 
    self.plot_3.figure = create_chart3
    
    #        
    #create_chart4 = anvil.server.call('create_chart4') 
    #self.plot_4.figure = create_chart4

    #tickets by creation date
    create_chart5 = anvil.server.call('create_chart5') 
    self.plot_5.figure = create_chart5

    

  def Dashboard_click(self, **event_args):

    open_form('Homepage')

  #def call_js(self, **event_args):
    """This method is called when the Plot is shown on the screen"""
   # self.call_js('buildChart')
   # pass
