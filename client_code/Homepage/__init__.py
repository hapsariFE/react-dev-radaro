from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from ..Data import *
from anvil.tables import app_tables
from datetime import datetime, timedelta, date


class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.filters = {}
    self.date_filters = {} 
    #users = anvil.server.call('get_user_list')
    self.users = ""
    #self.users = 'Danny'
    self.esc_status = esc_status
    self.esc_type = esc_type
    self.job_status = job_status
    self.merchant_name = ""
    startDate= (date.today() - timedelta(days=60))
    endDate = date.today()
    escType= None
    self.assigned = ""
    assigned_to = None

    
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
