from ._anvil_designer import NewTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Data import *

class New(NewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.esc_status = esc_status
    self.esc_type = esc_type
    
    self.init_components(**properties)
    # Any code you write here will run before the form opens.






  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
        # Clear our input boxes
    self.job_input.text = ""
    self.customer_input.text = ""
    self.mobile_input.text = ""
    self.dd_merchant.selected_value = ""
    self.subbrand_input.text = ""
    self.addcomment_input.text = ""    
    self.dd_esc_status.selected_value = ""
    self.dd_esc_type.selected_value = ""
    self.refresh_data_bindings()

  def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    job = self.job_input.text
    customer = self.customer_input.text
    mobile = self.mobile_input.text
    merchant_name = self.dd_merchant.selected_value
    subbrand = self.subbrand_input.text
    description = self.addcomment.text
    esc_status = self.dd_esc_status.selected_value
    esc_type = self.dd_esc_type.selected_value     
    date_created = datetime.now()
    last_action_date = date_created

    if job is "":
      alert("Please enter a job ID")
    elif customer is "":
      alert("Please enter a customer name")
    elif merchant_name is None:
      alert("Please select a merchant")
    elif esc_type is None:
      alert("Please select an escalation type")    
    elif esc_status is None:
      alert("Please select an escalation status")    
    elif description is "":
      alert("Please submit a comment")
    else:
      anvil.server.call('new',job, customer, mobile, merchant_name, subbrand, description, esc_status, esc_type, date_created, last_action_date)





