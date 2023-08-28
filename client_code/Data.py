import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
"""This module collects global variables to be used throughout the app"""
import anvil.server
#import anvil.google.auth, anvil.google.drive
#from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js

esc_status = [(x['name'], x) for x in app_tables.escalation_status.search()]
esc_type = [(x['name'], x) for x in app_tables.escalation_type.search()]
job_status = [(x['name'], x) for x in app_tables.job_status.search()]
merchant_name = [(x['name'], x) for x in app_tables.merchant.search()]
NO_STATUS_SELECTED = 'None'
currentUser= None

def set_theme():
  css = themed_css
     
  anvil.js.call_js("setThemeCss", css)

themed_css = """

.filterpanel {
  padding: 0 18px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
}

.collapsible: {
	border-style: solid;
	border-width: 0.15em 0.15em 0 0;
	content: '';
	display: inline-block;
	height: 1.0em;
	left: 0.15em;
	position: relative;
	top: 0.15em;
	vertical-align: top;
	width: 1.0em;
}

.active, .collapsible:hover {
  color: #555;
}

.collapsible:after {
	border-style: solid;
	border-width: 0.15em 0.15em 0 0;
	content: '';
	display: inline-block;
	height: 1.0em;
	left: 0.15em;
	position: relative;
	top: 0.15em;
	transform: rotate(135deg);
	vertical-align: top;
	width: 1.0em;
}

.active:after {
	transform: rotate(-45deg);
  vertical-align: bottom;
}
"""