#!/bin/sh

# Do not use "verbose" in order to spot errors easily

# Remove mclient image resources
rm -f ./resources/icon_36x36_{alphabet_off,alphabet_on,block_off,block_on,clear_search_field,define,go_back,go_back_off,go_forward,go_forward_off,go_search,open_in_browser,paste,print,priority_off,priority_on,quit_now,reload,repeat_sign2,repeat_sign2_off,repeat_sign,repeat_sign_off,save_article,search_article,settings,show_about,spec_symbol,toggle_history,toggle_view_hor,toggle_view_ver,watch_clipboard_off,watch_clipboard_on}.gif

# Remove shared resources
rm -f ./resources/{error.gif,info.gif,question.gif,warning.gif}

# Remove other mclient resources
rm -rf ./{locale,dics,mclient.cfg}

# Remove mclient Python files
rm -f ./{cells.py,db.py,elems.py,mclient.py,mkhtml.py,offline.py,page.py,tags.py}

# Remove shared Python files
rm -f ./{gettext_windows.py,regexp.py,shared.py,sharedGUI.py}

# (Linux-only) Remove platform-specific mclient Python files
rm -f ./kl_mod_lin.py

# (Linux-only) Remove mclient icon
rm -f ./resources/icon_64x64_mclient.gif

# (Linux-only) Remove build scripts
rm -f ./{build.sh,clean_up.sh,setup.py,update_mclient.sh}

ls .
