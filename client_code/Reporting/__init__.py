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
    my_media = anvil.URLMedia(Data.currentUser['Logo'])
    self.image_2.source = my_media
    #today = datetime.now().astimezone().date()
    today = datetime.date(2023-10-15)
    currentUser= anvil.users.login_with_form()
    
    #New tickets last 7 days with delta and % Resolved
    last_week,delta,last_week_per,delta2,resolved,delta3,start_date_last_week,end_date_last_week,ave_resolve_time_lw, delta4 = anvil.server.call('highlights',today,currentUser)
    
    #New tickets
    self.label_9.text = last_week   
    self.label_16.text = "%s vs prior week" % (delta)
    if delta > 0: 
      self.label_16.icon = "fa:arrow-up"
      self.label_16.role = "red-arrow"
    elif delta < 0 : 
      self.label_16.icon = "fa:arrow-down"
      self.label_16.role = "green-arrow"
    else: self.label_16.icon = False
    # % Resolved
    self.label_11.text = "%s%" % (last_week_per)
    self.label_17.text = "%s vs prior week" % (delta2)
    if delta2 > 0: 
      self.label_17.icon = "fa:arrow-up"
      self.label_17.role = "green-arrow"
    elif delta2 < 0 : 
      self.label_17.icon = "fa:arrow-down"
      self.label_17.role = "red-arrow"
    else: self.label_17.icon = False
    #Resolved
    self.label_10.text = resolved
    self.label_19.text = "%s vs prior week" % (delta3)
    if delta3 > 0: 
      self.label_19.icon = "fa:arrow-up"
      self.label_19.role = "green-arrow"
    elif delta3 < 0: 
      self.label_19.icon = "fa:arrow-down"
      self.label_19.role = "red-arrow"
    else: self.label_19.icon = False
    #ave resolution
    self.label_13.text = "%sd" % (ave_resolve_time_lw)
    self.label_18.text = "%s vs prior week" % (delta4)
    if delta4 > 0: 
      self.label_18.icon = "fa:arrow-up"
      self.label_18.role = "red-arrow"
    elif delta4 < 0: 
      self.label_18.icon = "fa:arrow-down"
      self.label_18.role = "green-arrow"
    else: self.label_18.icon = False
    
    start_date = start_date_last_week.strftime("%b %d %Y")
    end_date = end_date_last_week.strftime("%b %d %Y")    
    self.label_20.text = "(%s to %s)" % (start_date,end_date)
    
    #Resolved tickets last 7 days with delta
    
    

    pie,chart,ch_status,ch_date,ch_type = anvil.server.call('all_charts',today,currentUser) 
    self.plot_6.figure = pie
    self.plot_7.figure = chart
    self.plot_5.figure = ch_status
    self.plot_3.figure = ch_date
    self.plot_2.figure = ch_type
    
    #response by user
    ch_user = anvil.server.call('chart_user',currentUser)
    self.plot_1.figure = ch_user 
   
    #create_chart4 = anvil.server.call('create_chart4',currentUser)
    #self.plot_4.figure = create_chart4


    

  def Dashboard_click(self, **event_args):

    open_form('Homepage')

  #def call_js(self, **event_args):
    """This method is called when the Plot is shown on the screen"""
   # self.call_js('buildChart')
   # pass
