#!/bin/sh

# Do not use "verbose" in order to spot errors easily

# Remove mclient image resources
rm ./resources/buttons/icon_36x36_{alphabet_off,alphabet_on,block_off,block_on,clear_search_field,define,go_back,go_back_off,go_forward,go_forward_off,go_search,open_in_browser,paste,print,priority_off,priority_on,quit_now,reload,repeat_sign2,repeat_sign2_off,repeat_sign,repeat_sign_off,save_article,search_article,settings,show_about,spec_symbol,toggle_history,toggle_view_hor,toggle_view_ver,watch_clipboard_off,watch_clipboard_on}.gif

# Remove shared resources
rm ./resources/{error,info,question,warning}.gif

# Remove other mclient resources
rm ./user/{dic_abbr.txt,mclient.cfg}
rm ./resources/third\ parties.txt
rm ./resources/locale/ru/LC_MESSAGES/mclient.mo
rm ./user/dics/{block.txt,prioritize.txt}

# Remove mclient Python files
rm ./{cells,db,elems,gui,logic,mclient,mkhtml,offline,page,tags}.py

# Remove shared Python files
rm ./{gettext_windows,shared,sharedGUI}.py

# (Linux-only) Remove platform-specific mclient files
rm ./kl_mod_lin.py
rm ./user/dics/rm_dics.sh

# (All platforms) Remove mclient icon
rm ./resources/icon_64x64_mclient.gif

# (Linux-only) Remove build scripts
rm ./{build.sh,clean_up.sh,find_shared_libs.sh,pack.sh,setup.py,update_here.sh,update_mclient.sh}

rmdir resources/buttons
rmdir -p resources/locale/ru/LC_MESSAGES user/dics

ls .
