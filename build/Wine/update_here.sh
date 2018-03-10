#!/bin/sh

# Do not use "verbose" in order to spot errors easily

mkdir -p ./resources/{buttons,dics}
mkdir -p ./resources/locale/ru/LC_MESSAGES

# Copy mclient image resources
cp -u /usr/local/bin/mclient/resources/buttons/icon_36x36_{alphabet_off,alphabet_on,block_off,block_on,clear_search_field,define,go_back,go_back_off,go_forward,go_forward_off,go_search,open_in_browser,paste,print,priority_off,priority_on,quit_now,reload,repeat_sign2,repeat_sign2_off,repeat_sign,repeat_sign_off,save_article,search_article,settings,show_about,spec_symbol,toggle_history,toggle_view_hor,toggle_view_ver,watch_clipboard_off,watch_clipboard_on}.gif ./resources/buttons
# This is actually used by all platforms
cp -u /usr/local/bin/mclient/resources/icon_64x64_mclient.gif ./resources/

# Copy shared resources
cp -u /usr/local/bin/shared/resources/{error.gif,info.gif,question.gif,warning.gif} ./resources/

# Copy other mclient resources
cp -u /usr/local/bin/mclient/resources/dics/{block.txt,prioritize.txt} ./resources/dics/
cp -u /usr/local/bin/mclient/resources/{mclient.cfg,third\ parties.txt} ./resources/
cp -u /usr/local/bin/mclient/resources/locale/ru/LC_MESSAGES/mclient.mo ./resources/locale/ru/LC_MESSAGES/

# Copy mclient Python files
cp -u /usr/local/bin/mclient/src/{cells,db,elems,gui,logic,mclient,mkhtml,offline,page,tags}\.py .

# Copy shared Python files
cp -u /usr/local/bin/shared/{gettext_windows.py,regexp.py,shared.py,sharedGUI.py} .

# (Wine-only) Copy platform-specific mclient Python files
cp -u /usr/local/bin/mclient/src/kl_mod_win.py .

# (Wine-only) Copy mclient icon
cp -u /usr/local/bin/mclient/resources/icon_64x64_mclient.ico ./resources/

# (Wine-only) Copy build scripts
cp -u /usr/local/bin/mclient/build/Wine/{build.sh,clean_up.sh,setup.py,update_mclient.sh} .

# (Wine-only) Copy tkinterhtml binaries
mkdir ./tkhtml
cp -r /usr/lib/python3.4/site-packages/tkinterhtml/tkhtml/Windows/ ./tkhtml/

ls .
