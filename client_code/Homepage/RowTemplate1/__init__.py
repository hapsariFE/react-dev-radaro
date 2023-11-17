from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from ... import Data
import anvil.server
import anvil.users
from ...jobreport import jobreport
from ...Modal_wide import Modal_wide
from ...Homepage import Homepage
import webbrowser
import anvil.tz
from datetime import datetime, timedelta, date
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.

    self.init_components(**properties)
    self.label_8.text = self.get_time_difference_string(self.item['date_created'])
    self.label_2.text = self.get_time_difference_string(self.item['last_action_date'])
    #createdif = datetime.now(anvil.tz.tzlocal()) - self.item['date_created']
    #if createdif.seconds < 3600:
    #  createdif = str((createdif.seconds//60)%60) + " minutes"
    #elif createdif.days < 1:
    #  createdif = str(createdif.seconds//3600) + " hours, " + str((createdif.seconds//60)%60) + " minutes"
    #else:
    #  createdif = str(createdif.days) + " days, " + str(createdif.seconds//3600) + " hours"
    #self.label_8.text = createdif

    #actiondif = datetime.now(anvil.tz.tzlocal()) - self.item['last_action_date']
    #if actiondif.seconds < 3600:
    #  actiondif = str((actiondif.seconds//60)%60) + " minutes"
   # elif actiondif.days < 1:
   #   actiondif = str(actiondif.seconds//3600) + " hours, " + str((actiondif.seconds//60)%60) + " minutes"
    #else:
    #  actiondif = str(actiondif.days) + " days, " + str(actiondif.seconds//3600) + " hours"
   # self.label_2.text = actiondif
    if self.item['watchlistUsers'] is not None:
      if Data.currentUser in self.item['watchlistUsers']:
        self.favourite.source= "_/theme/Star%20filled.png"
      else:
        self.favourite.source = "_/theme/Star%20outline.png"
    else:
      self.favourite.source = "_/theme/Star%20outline.png"

  def jobreport_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.item['job_report'] is not None:
      webbrowser.open(self.item['job_report'])
    else: 
        alert('Job Report does not exist')

  def comment_click(self, **event_args):
    """This method is called when the button is clicked"""
    record_copy = dict(self.item)
    save_clicked = alert(
     content=Modal(item = self.item),
     buttons=[("Exit", False)],
   )
    self.parent.raise_event('x-edit-article', article=self.item)
    self.refresh_data_bindings()
    
  def widecomment_click(self, **event_args):
    """This method is called when the button is clicked"""
    iresvalue = get_open_form().itemlist
    record_copy = dict(self.item)
    save_clicked = alert(
     content=Modal_wide(item=self.item,ires=iresvalue),
     large=True,
     buttons=[("Exit", False)],
   )
    self.parent.raise_event('x-edit-article', article=self.item)
    self.refresh_data_bindings()

  def update_item(self, **event_args):
    watch_list = self.watch.checked
    row_id=self.item['id']
    anvil.server.call('update_item',row_id,watch_list)

  def update_item2(self, **event_args):
    """This method is called when the link is clicked"""
    watchlistUsers = self.item['watchlistUsers']
    watch_list = self.item['watch_list']
    if watchlistUsers is not None:
      if Data.currentUser in watchlistUsers:
        self.favourite.source = "_/theme/Star%20outline.png"
        print("Yes")
      elif Data.currentUser not in watchlistUsers:
        self.favourite.source= "_/theme/Star%20filled.png"
        print("No") 
    article=self.item
    user = Data.currentUser
    anvil.server.call('update_item',article,user)
    self.refresh_data_bindings()

  def get_time_difference_string(self, from_time):
    time_difference = datetime.now(anvil.tz.tzlocal()) - from_time
    days = time_difference.days
    seconds = time_difference.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days} days, {hours} hours"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes"
    else:
        return f"{minutes} minutes"