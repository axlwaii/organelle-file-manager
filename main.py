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
file_manager_directory = user_dir
file_manager_selected_path = ''
file_manager_selected_file = ''
file_manager_copied_path = ''


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
  global file_manager_directory
  new_path = os.path.dirname(file_manager_directory)
  file_manager_directory = new_path
  draw_manager_menu()

def select_directory():
  global file_manager_directory
  global menu
  selected_folder = menu.items[menu.selection][2]
  new_path = "/".join((file_manager_directory, selected_folder))
  file_manager_directory = new_path
  draw_manager_menu()

# Action status views
def delete_file():
  global file_manager_selected_path
  og.clear_screen()
  og.println(0, "Deleted")
  og.println(1, "---------------------")
  og.println(2, file_manager_selected_path[-20:])
  os.system('rm -f ' + file_manager_selected_path.replace(' ', '\ '))
  time.sleep(2.5)
  draw_manager_menu()

def copy_file():
  global file_manager_selected_path
  global file_manager_copied_path
  og.clear_screen()
  og.println(0,"COPIED")
  og.println(1, "---------------------")
  og.println(2, file_manager_selected_path[-20:])
  file_manager_copied_path = file_manager_selected_path
  time.sleep(4)
  draw_manager_menu()

def paste_file():
  global file_manager_copied_path
  og.clear_screen()
  og.println(0,"PASTED")
  og.println(1, "---------------------")
  og.println(2, file_manager_copied_path[-20:])
  og.println(3, "TO " + file_manager_selected_path[-17:])
  os.system('cp  ' + file_manager_copied_path.replace(' ', '\ ') + ' ' +  file_manager_selected_path.replace(' ', '\ '))
  time.sleep(4)
  file_manager_copied_path = ''
  draw_manager_menu()

# Menu views
def confirm_delete_menu():
  global file_manager_directory
  global file_manager_selected_file
  global menu
  clear_menu()
  menu.separator = True
  menu.header= "DELETE " + file_manager_selected_file
  menu.items.append(["No", draw_manager_menu])
  menu.items.append(["Yes", delete_file])
  menu.perform()

def confirm_paste_menu():
  global file_manager_directory
  global file_manager_copied_path
  global menu
  clear_menu()
  menu.separator = True
  menu.header= "COPY " + file_manager_copied_path[-15:]
  menu.subheader= "TO " + file_manager_selected_path[-17:]
  menu.items.append(['No', draw_manager_menu])
  menu.items.append(['Yes', paste_file])
  menu.perform()

def draw_action_menu():
  global menu
  global file_manager_selected_path
  global file_manager_selected_file
  file_manager_selected_file = menu.items[menu.selection][0]
  if (file_manager_selected_file != '/'):
    file_path = "/".join((file_manager_directory, file_manager_selected_file))
  else:
    file_path = file_manager_directory + '/'
  file_manager_selected_path = file_path
  clear_menu()
  menu.header = 'ACTIONS'
  menu.separator = True
  if (file_manager_selected_file != '/'):
    menu.items.append(['Copy', copy_file])
  if (file_manager_copied_path != ''):
    menu.items.append(['Paste', confirm_paste_menu])
  if (file_manager_selected_file != '/'):
    menu.items.append(['Delete', confirm_delete_menu])
  menu.items.append(['Abort', draw_manager_menu])
  menu.items.append([''])
  menu.perform()

def draw_manager_menu():
  global menu
  global file_manager_directory
  clear_menu()
  menu.header= 'DIR:.' + file_manager_directory[-14:]
  files_list = sorted(filter(isfile, os.listdir(file_manager_directory)))
  dirs_list = sorted(filter(isdir, os.listdir(file_manager_directory)))
  if (file_manager_directory != user_dir):
  files_list = sorted(filter(helpers.isfile, os.listdir(state["current_directory"])))
  dirs_list = sorted(filter(helpers.isdir, os.listdir(state["current_directory"])))
    menu.items.append(['../', folder_up])
  if (file_manager_copied_path != ''):
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

