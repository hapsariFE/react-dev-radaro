from ._anvil_designer import Modal_pdfTemplate
from anvil import *
import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
from .. import Data
from ..Data import *
from datetime import datetime, timedelta, date
import webbrowser
import anvil.tz
from form_checker import validation
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Modal_pdf(Modal_pdfTemplate):
  def __init__(self,ires, **properties):
    # Set Form properties and Data Bindings.

    self.esc_status = esc_status
    self.assigned = ""
    createdif = ""
    actiondif = ""
    self.ires = ires
    print(ires)
    self.item=ires

    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    createdif = datetime.now(anvil.tz.tzlocal()) - self.item['date_created']
    if createdif.seconds < 3600:
      createdif = str((createdif.seconds//60)%60) + " minutes"
    elif createdif.days < 1:
      createdif = str(createdif.seconds//3600) + " hours, " + str((createdif.seconds//60)%60) + " minutes"
    else:
      createdif = str(createdif.days) + " days, " + str(createdif.seconds//3600) + " hours"
    self.label_26.text = createdif
    actiondif = datetime.now(anvil.tz.tzlocal()) - self.item['last_action_date']
    if actiondif.seconds < 3600:
      actiondif = str((actiondif.seconds//60)%60) + " minutes"
    elif actiondif.days < 1:
      actiondif = str(actiondif.seconds//3600) + " hours, " + str((actiondif.seconds//60)%60) + " minutes"
    else:
      actiondif = str(actiondif.days) + " days, " + str(actiondif.seconds//3600) + " hours"
    self.label_27.text = actiondif
    selectedRow = self.item
    SelectedMerchant = self.item['webhook_merchant_link']
    
    assignList = anvil.server.call('get_selectedMerchant',SelectedMerchant)
    actionData = anvil.server.call('get_action',selectedRow)
    self.action_panelwide.items = actionData
 







