from ._anvil_designer import NewTemplate
from anvil import *
import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
from datetime import datetime, timedelta, date
from ..Data import *
import anvil.tz
from form_checker import validation
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class New(NewTemplate):
  def __init__(self, eres, **properties):
    # Set Form properties and Data Bindings.
    self.esc_status = esc_status
    self.esc_type = esc_type
    self.assigned = ""
    self.etype = ""
    fUsers, ccVals,sVals,fmerch = anvil.server.call('get_filter_value')
    self.etype = ccVals
    self.merchant_name = fmerch
    self.subbrand = sVals
        
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    users = fUsers
    self.assigned = [(x['name'], x) for x in users]
    self.refresh_data_bindings()
    self.validator = validation.Validator()
    self.validator.require_text_field(self.job_input, self.e_job)
    self.validator.require_text_field(self.customer_input, self.e_customer)
    self.validator.require_text_field(self.addcomment_input, self.e_comment)
    self.validator.require(self.dd_merchant, ['change'],
                          lambda DropDown: DropDown.selected_value is not None,
                          self.e_merchant)
    self.validator.require(self.dd_subbrand, ['change'],                      
                          lambda Dropdown:  (
                          Dropdown.selected_value is None or
                          Dropdown.selected_value.get('ID') in ['00000000', '00000001'] or
                          ('MerchantLink' in Dropdown.selected_value and
                          Dropdown.selected_value['MerchantLink'].get('name') == self.dd_merchant.selected_value)
                          ),
                          self.e_subbrand)
    self.validator.require(self.dd_assign, ['change'],
                          lambda DropDown: DropDown.selected_value is not None,
                          self.e_assign)
    self.validator.require(self.dd_esc_type, ['change'],
                          lambda DropDown: DropDown.selected_value is not None,
                          self.e_type)    
    self.validator.require(self.dd_esc_status, ['change'],
                          lambda DropDown: DropDown.selected_value is not None,
                          self.e_status)             
    # Uncomment the line below to disable the button until the form is complete:
    self.validator.enable_when_valid(self.button_1)
    
    
  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
        # Clear our input boxes
    self.job_input.text = ""
    self.job_ref.text = ""
    self.customer_input.text = ""
    self.mobile_input.text = ""
    self.dd_merchant.selected_value = ""
    self.dd_subbrand.selected_value = ""
    self.addcomment_input.text = ""    
    self.dd_esc_status.selected_value = ""
    self.dd_esc_type.selected_value = ""
    self.dd_assign.selected_value = ""
    self.refresh_data_bindings()

  def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    job = self.job_input.text
    jobref = self.job_ref.text
    customer = self.customer_input.text
    mobile = self.mobile_input.text
    merchant_name = self.dd_merchant.selected_value
    subbrand = self.dd_subbrand.selected_value
    description = self.addcomment_input.text
    esc_status = self.dd_esc_status.selected_value
    esc_type = self.dd_esc_type.selected_value    
    assign_to = self.dd_assign.selected_value
    date_created = datetime.now(anvil.tz.tzlocal())
    last_action_date = date_created

    if job is "":
      alert("Please enter a Job ID")
    elif customer is "":
      alert("Please enter a Customer Name")
    elif merchant_name is None:
      alert("Please select a Merchant")
    elif assign_to is None:
      alert("Please assing to a user")      
    elif esc_type is None:
      alert("Please select an Escalation Type")    
    elif esc_status is None:
      alert("Please select an Escalation Status")    
    elif description == "":
      alert("Please submit a Comment")
    elif self.e_subbrand.visible: 
    
            anvil.alert("The selected Sub Brand does not belong to the selected Merchant Details")

    
    else:
      anvil.server.call('new',job, jobref, customer, mobile, merchant_name, subbrand, description, esc_status, esc_type, date_created, last_action_date, assign_to)
      self.clear_button_click()
      self.raise_event('x-close-alert', article=self.item)
      





