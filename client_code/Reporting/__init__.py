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
    today = datetime.now().astimezone().date()- timedelta(days=5)
    currentUser= anvil.users.login_with_form()
    
    #New tickets last 7 days with delta and % Resolved
    last_week,prior_week,delta,last_week_per,delta2 = anvil.server.call('new_tickets',today,currentUser) 
    delta = +delta if delta > 0 else -delta
    self.label_9.text = last_week   
    self.label_16.text = "%s vs prior week" % (delta)
    self.label_16.icon = "fa:arrow-up" if delta > 0 else "fa:arrow-down"
    self.label_11.text = last_week_per
    self.label_17.text = "%s vs prior week" % (delta2)
    self.label_17.icon = "fa:arrow-up" if delta2 > 0 else "fa:arrow-down"
    
    #Resolved tickets last 7 days with delta
    
    
    
    
    
    #pie chart last week
    create_stat1 = anvil.server.call('create_stat1',today,currentUser) 
    self.plot_6.figure = create_stat1

    #bar chart last week vs this week
    create_stat2 = anvil.server.call('create_stat2',today,currentUser) 
    self.plot_7.figure = create_stat2

    #response by user
    #create_chart1 = anvil.server.call('create_chart1',currentUser)
    #self.plot_1.figure = create_chart1

    #tickets by escalation type
    #create_chart2 = anvil.server.call('create_chart2',currentUser)
    #self.plot_2.figure = create_chart2

    #tickets by creation date
    create_chart3 = anvil.server.call('create_chart3',currentUser)
    self.plot_3.figure = create_chart3
    
    #        
    #create_chart4 = anvil.server.call('create_chart4',currentUser)
    #self.plot_4.figure = create_chart4

    #tickets by current status
    #create_chart5 = anvil.server.call('create_chart5',currentUser)
    #self.plot_5.figure = create_chart5

    

  def Dashboard_click(self, **event_args):

    open_form('Homepage')

  #def call_js(self, **event_args):
    """This method is called when the Plot is shown on the screen"""
   # self.call_js('buildChart')
   # pass
