#!/bin/sh

# Do not use "verbose" in order to spot errors easily

# Remove mclient image resources
rm -f ./resources/buttons/icon_36x36_{alphabet_off,alphabet_on,block_off,block_on,clear_search_field,define,go_back,go_back_off,go_forward,go_forward_off,go_search,open_in_browser,paste,print,priority_off,priority_on,quit_now,reload,repeat_sign2,repeat_sign2_off,repeat_sign,repeat_sign_off,save_article,search_article,settings,show_about,spec_symbol,toggle_history,toggle_view_hor,toggle_view_ver,watch_clipboard_off,watch_clipboard_on}.gif
rm -f ./resources/icon_64x64_mclient.gif

# Remove shared resources
rm -f ./resources/{error.gif,info.gif,question.gif,warning.gif}

# Remove mclient Python files
rm -f ./{cells,db,elems,gui,logic,mclient,mkhtml,offline,page,tags}\.py

# Remove shared Python files
rm -f ./{gettext_windows.py,regexp.py,shared.py,sharedGUI.py}

# Remove other mclient resources
rm ./resources/locale/ru/LC_MESSAGES/mclient.mo
rm -f ./resources/{mclient.cfg,third\ parties.txt}
rm -f ./resources/dics/{block.txt,prioritize.txt}

# (Wine-only) Remove platform-specific mclient Python files
rm -f ./kl_mod_win.py

# (Wine-only) Remove mclient icon
rm -f ./resources/icon_64x64_mclient.ico

# (Wine-only) Remove build scripts
rm -f ./{build.sh,clean_up.sh,setup.py,update_mclient.sh}

# (Wine-only) Remove tkinterhtml binaries
rm -rf ./tkhtml/Windows/*
rmdir -p tkhtml/Windows

rmdir resources/{buttons,dics}
rmdir -p resources/locale/ru/LC_MESSAGES

ls .
