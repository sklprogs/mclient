#!/bin/bash

# Do not use "verbose" in order to spot errors easily

mkdir -p ./resources/{buttons,locale/ru/LC_MESSAGES} ./src

# Copy mclient image resources
cp -u $HOME/bin/mclient/resources/buttons/icon_36x36_{alphabet_off,alphabet_on,block_off,block_on,clear_search_field,define,go_back,go_back_off,go_forward,go_forward_off,go_search,open_in_browser,paste,print,priority_off,priority_on,quit_now,reload,repeat_sign2,repeat_sign2_off,repeat_sign,repeat_sign_off,save_article,search_article,settings,show_about,spec_symbol,toggle_history,toggle_view_hor,toggle_view_ver,watch_clipboard_off,watch_clipboard_on}.gif ./resources/buttons/

# Copy shared resources
cp -u $HOME/bin/shared/resources/{error,info,question,warning}.gif ./resources/

# Copy other mclient resources
cp -u $HOME/bin/mclient/resources/locale/ru/LC_MESSAGES/mclient.mo ./resources/locale/ru/LC_MESSAGES/
cp -u $HOME/bin/mclient/resources/{abbr.txt,default.cfg,third\ parties.txt} ./resources/

# Copy mclient Python files
cp -u $HOME/bin/mclient/src/{cells,db,elems,gui,logic,mclient,mkhtml,offline,page,tags}.py ./src/

# Copy shared Python files
cp -u $HOME/bin/shared/src/{gettext_windows,shared,sharedGUI}.py ./src

# (Wine-only) Copy platform-specific mclient files
cp -u $HOME/bin/mclient/src/kl_mod_win.py ./src

# (All platforms) Copy mclient icon
cp -u $HOME/bin/mclient/resources/icon_64x64_mclient.gif ./resources/
# (Wine-only) Copy mclient icon
cp -u $HOME/bin/mclient/resources/icon_64x64_mclient.ico ./resources/

# (Wine-only) Copy a script for fast launch
cp -u $HOME/bin/mclient/build/Wine/launch.sh ./src/

# (Wine-only) copy tkinterhtml
mkdir -p ./src/tkhtml/Windows
cp -rn $HOME/.wine/drive_c/Python34/Lib/site-packages/tkinterhtml/tkhtml/Windows/* ./src/tkhtml/Windows/

rm ./update_structure.sh

ls --color=always .
