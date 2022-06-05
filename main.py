import os
import subprocess
import imp
import sys
import time
import threading

import og
import helpers

# usb or sd card
user_dir = os.getenv("USER_DIR", "/usbdrive")

# State
state = {
  "current_directory": user_dir,
  "copied_path": "",
  "selected_path": "",
  "selected_file": ""
}

# UI elements
menu = og.Menu()
menu.items = []

# lock for updating menu
menu_lock = threading.Lock()

def update_menu():
  menu_lock.acquire()
  try :
    pass
  finally :
    menu_lock.release()

# bg connection checker
def check_status():
  while True:
    time.sleep(1)
    update_menu()
    og.redraw_flag = True

# Menu actions
def clear_menu():
  global menu
  og.clear_screen()
  menu.subheader = ''
  menu.separator = False
  menu.items = []
  menu.selection = 0
  menu.cursor_offset = 0
  menu.menu_offset = 0

def folder_up():
  global state
  new_path = os.path.dirname(state["current_directory"])
  state["current_directory"] = new_path
  draw_manager_menu()

def select_directory():
  global state
  global menu
  selected_folder = menu.items[menu.selection][2]
  new_path = "/".join((state["current_directory"], selected_folder))
  state["current_directory"] = new_path
  draw_manager_menu()

# Action status views
def confirm_view(title, from_path, to_path):
  og.clear_screen()
  og.println(0, title)
  og.println(1, "---------------------")
  og.println(2, from_path[-20:])
  if to_path:
    og.println(3, from_path[-17:])
  time.sleep(2.5)
  draw_manager_menu()

def delete_file():
  global state
  os.system('rm -f ' + state["selected_path"].replace(' ', '\ '))
  confirm_view("Deleted", state["selected_path"], None)

def copy_file():
  global state
  state["copied_path"] = state["selected_path"]
  confirm_view("Copied", state["selected_path"], None)

def paste_file():
  global state
  os.system('cp  ' + state["copied_path"].replace(' ', '\ ') + ' ' +  state["selected_path"].replace(' ', '\ '))
  state["copied_path"] = ''
  confirm_view("Pasted", state["copied_path"], state["selected_path"])

# Menu views
def confirm_menu(header, subheader, yes_callback):
  global state
  global menu
  clear_menu()
  menu.separator = True
  menu.header = header
  menu.subheader = subheader
  menu.items.append(["No", draw_manager_menu])
  menu.items.append(["Yes", yes_callback])
  menu.perform()

def confirm_delete_menu():
  header= "DELETE " + state["selected_file"]
  confirm_menu(header, None, delete_file)

def confirm_paste_menu():
  header= "COPY " + state["copied_path"][-15:]
  subheader= "TO " + state["selected_path"][-17:]
  confirm_menu(header, subheader, paste_file)

def draw_action_menu():
  global menu
  global state
  state["selected_file"] = menu.items[menu.selection][0]
  if (state["selected_file"] != '/'):
    file_path = "/".join((state["current_directory"], state["selected_file"]))
  else:
    file_path = state["current_directory"] + '/'
  state["selected_path"] = file_path
  clear_menu()
  menu.header = 'ACTIONS'
  menu.separator = True
  if (state["selected_file"] != '/'):
    menu.items.append(['Copy', copy_file])
  if (state["copied_path"] != ''):
    menu.items.append(['Paste', confirm_paste_menu])
  if (state["selected_file"] != '/'):
    menu.items.append(['Delete', confirm_delete_menu])
  menu.items.append(['Abort', draw_manager_menu])
  menu.items.append([''])
  menu.perform()

def draw_manager_menu():
  global menu
  global state
  clear_menu()
  menu.header= 'DIR:.' + state["current_directory"][-14:]
  files_list = sorted(filter(helpers.isfile, os.listdir(state["current_directory"])))
  dirs_list = sorted(filter(helpers.isdir, os.listdir(state["current_directory"])))
  if (state["current_directory"] != user_dir):
    menu.items.append(['../', folder_up])
  if (state["copied_path"] != ''):
    menu.items.append(['/', draw_action_menu])
  for dir_name in dirs_list:
    menu.items.append(["/" + dir_name, select_directory, dir_name])
  for file_name in files_list:
    menu.items.append([file_name, draw_action_menu])
  menu.items.append(['<-- Quit', quit])
  menu.perform()

# App
def quit():
  og.end_app()

def start():
  og.start_app()
  draw_manager_menu()

menu_updater = threading.Thread(target=check_status)
menu_updater.daemon = True # stop the thread when we exit

og.redraw_flag = True

# start thread to update connection status
menu_updater.start()

# Init
start()

