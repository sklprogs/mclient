(in development)

## 7.1.7
* Fix loading .dsl and Stardict dictionaries
* Synchronize changes with shared module

## 7.1.6
* Adopt [multitran.com](https://www.multitran.com) changes (remove useless text)

## 7.1.5
* Fix word forms

## 7.1.4
* Fix Alt-~ on Windows
* Fix "Separate words" mode (should be improved)
* Remove a warning about wrong input data in the "Nothing has been found" mode
* Comments having a URL are no longer detected as a word form
* Now transcriptions always start a new cell

## 7.1.3
* Fix searching in an article

## 7.1.2
* Attempt to fix a locale issue

## 7.1.1
* Remove languages from a phrase-type article
  \([multitran.com](https://www.multitran.com)\).

## 7.1
* Resize rows by contents (if the corresponding option is enabled)
* Adopt [multitran.com](https://www.multitran.com) updates (remove excessive
  text)
* Refactor the code to conform with skl_shared_qt

## 7.0.2
* Adopt [multitran.com](https://www.multitran.com) updates (thesauruses,
  multi-word word forms, a comment prior to a word form)
* Custom search field border

## 7.0.1
* Adopt multitran.com updates (word forms)

## 7.0
* Migrate to Qt
* Migrate to a config file formatted as JSON
* Small fixes and improvements

## 6.14.4
* Remove "Get short URL" block
* Remove extra blocks at the end of the article

## 6.14.3
* Fix mode of showing separate words only
* Fix selecting blocks in "Phrases" section

## 6.14.1
* A different number of columns is used for common and special articles.
  Special articles are those that have only an even number of columns
  (e.g., a source-target pair).

## 6.14
* Calculate column widths faster on the basis of predefined values
* Add a button to suggest optimal column widths
* Change a "timeout" key type to a floating number
* Delete keys AdjustLayout, table_width
* Add keys term_col_width, fixed_col_width, hotkey_delay, Ping
* Increase an update interval up to 0.6 seconds

## 6.13.2
* Fix calling the window in Windows for some cases

## 6.13.1
* Fix calling the window with Alt-~, Ctrl-C-C and Ctrl-Ins-Ins in Windows
* Remove a Windows workaround which could lead to thread freezing

## 6.13
* Improve selecting a column width on the basis of a text width
* Colorize subjects from a Phrases section
* Add hotkeys Alt + digit to change a number of columns (for example, Alt-4 -
  4 columns, Alt-6 - 6 columns, Alt-0 - 10 columns)

## 6.12.2
* Update according to recent changes at multitran.com
* Fix composing an email to the author

## 6.12.1
* Fix calculating a column width for articles with no fixed columns
* Fix bindings for widgets

## 6.12
* Get a column width based on a factual (not preset) number of columns
* Fix too wide columns for a single-line article
* Set "Adjust columns by width" and "Use a custom table width:"
  (configurable in settings). These options are automatically
  saved/loaded from the configuration file.

## 6.11
* Align columns by width (except for one-row articles)
* Adjust table layout such as to fit most columns
* Break too long words (e.g., URLs) in order to keep column edges visible
* Update documentation
* Fix parsing user names
* Remove an extra space before user names
* Fix processing user names as subjects
* Allow subjects with commas while blocking/prioritizing in an article view

## 6.10
* Set up subject priorities in a separate window
* Configure subject blocking in a separate window
* Set the vertical view button after the alphabetization button
* Drop left/right mouse subject management support
* Support subjects in multiple languages based on multitran.com
* Save lists of prioritized and blocked subjects on exit
* Manage subject groups on the basis of main subjects

## 6.9.1
* Fix a webpage generated in a current view
* Delete the "Get short URL" block
* Make the program smaller (enchant module is optional now)

## 6.9
* Rewrite multitran.com parser, make it faster and more accurate
* Support multitran.com suggestions for spelling mistakes
* Support "⇒" section
* Support URL inside user comments
* Skip "Russian thesaurus" and "English thesaurus" blocks
* Show a phrase count (configurable in settings). This option is automatically
  saved/loaded from the configuration file.
* Move records from the Great encyclopedic dictionary to a separate subject
* Fix saving the article

## 6.8
* Show tooltips within the screen (a change in the shared module)
* Select all or terms-only blocks (configurable in settings). This option
  is automatically saved/loaded from the configuration file.
* Iconify the program window after copying (configurable in settings).
  This option is automatically saved/loaded from the configuration file.
* Show suggestions on input (configurable in settings). This option
  is automatically saved/loaded from the configuration file.
* Autoswap Russian and the other language in GUI if appropriate (configurable
  in settings). This option is automatically saved/loaded from
  the configuration file.
* Support various language pairs for DSL dictionaries
* Delete blocks "Download", "Contacts"

## 6.7
* Improve separating cells at multitran.com (separate cells on the basis
  of semicolons, fix user names, etc.)
* Support the tag [ref dict="Dic title"] for DSL

## 6.6
* Delete "Terms of Use" block
* Add "Shorten parts of speech" setting
* Fix restoring settings

## 6.5
* Fix standalone comments
* Add "Show user names" option
* Use a brighter color for user names
* Add a basic support for DSL files
* Load widgets only when necessary
* Save and restore settings
* Delete "Terms of Use" block
* Add detailed hints to some buttons

## 6.4.1
* Fix loading Stardict format

## 6.4
* Center fixed columns only
* Set dictionary titles for a phrase-only article
* Update the building system which corrected errors

## 6.3
* Expand dictionary titles on the basis of multitran.com
* Add support for local Multitran files (short demo only)
* Ignore "Forvo, Google" blocks

## 6.2.4
* Refactor the code

## 6.2.3
* Delete "in specified order only" block

## 6.2.2
* Fix an article saving bug
* Make consistent with the latest changes at multitran.com

## 6.2.1
* Fix URLs for "only individual words found" section
* Delete "phantom" parts of a word form

## 6.2
* Refactor the code
* Add bind_copy_nominative key (copy the source word/phrase in the nominative
  case; Ctrl-W by default)
* Slightly improve multitran.com parser
* Delete "+", "Сообщить об ошибке"

## 6.1.1
* Delete unicode control codes
* Fix titles of Stardict dictionaries
* Fix an error upon an incorrect config
* Restore a source and languages when navigating History
* Fix switching sources

## 6.1
* Add language pairs supported by multitran.com
* Recognize dictionary titles for phrase-type articles
* Delete language names from articles
* Delete keys bind_prev_pair, bind_prev_pair_alt, bind_next_pair,
  bind_next_pair_alt
* Add keys bind_next_lang1 (F8 by default), bind_next_lang1_alt (Ctrl-K
  by default), bind_prev_lang1 (Shift-F8 by default), bind_prev_lang1_alt
  (Ctrl-Shift-K by default), bind_next_lang2 (F9 by default),
  bind_next_lang2_alt (Ctrl-L by default), bind_prev_lang2 (Shift-F9
  by default), bind_prev_lang2_alt (Ctrl-Shift-L by default), bind_swap_langs
  (Ctrl-Space by default)

## 6.0
* Reimplement reading Stardict files, make import faster and add support for
  GZIP files
* Import dictionary sources as plugins
* Add multitran.com support
* Delete bind_quit_now key, rename bind_quit_now_alt key to bind_quit
* Update documentation
* Add main hotkeys to the Welcome screen
* Enable autocompletion for all sources
* Improve comment parsing

## 5.12
* Wrap up too broad columns
* Move user files to
  C:\Documents and Settings\<user>\Application Data\mclient (Windows)
  and $HOME/.config/mclient (Linux)
* Add a Linux build (32-bit and 64-bit AppImage)

## 5.11.1
* Rework prioritization: only one click is required now in order to
  increase/decrease a priority of a dictionary or a group of dictionaries.
  Please note, however, that dictionary group having shared dictionary titles
  are considered to have the same priority.
* Fix a search field focusing bug
* By default, Control-F7 now copies the URL of the current article and Shift-F7
  copies the URL of the selected term (set this behavior in mclient.cfg)

## 5.11
* Autocomplete input
* Add a key Autocompletion

## 5.10
* Support several dictionary titles
* Support both full and shortened dictionary titles in the prioritized
  dictionary list and the blacklist
* Toggle full and shortened dictionary titles
* Click on a dictionary to (un-)prioritize or (un-)block it, in particular:
  LMB on:
    - a common dictionary: prioritize it
    - prioritized dictionary: increase priority
    - blocked dictionary: unblock it
  RMB on:
    - a common dictionary: block it
    - prioritized dictionary: decrease priority/unprioritize it
    - blocked dictionary: unblock it
  If several dictionary titles are selected, then this rule will be applied
  to each of these titles. For example, increasing a priority for a title
  'Британский английский, Пивное производство' will also increase a priority
  for titles 'Британский английский', 'Пивное производство' separately.
* Use Alt-f (by default) to go to a list of phrases
* Separate logic and GUI
* Close child windows with the same hotkeys they are shown
* Fix the size of option menus
* Add a key bind_go_phrases
* Delete a key bind_copy_history

## 5.9
* Fix a bug causing word forms to be shown as "0" in rare cases
* Set Multitran timeout for 6s at loading
* Fix SelectTermsOnly mode and toggle it on-the-fly (Control-t by default)
* Expand abbreviations for parts of speech comprising an additional information
  (e.g., "нареч. n -(e)s" => "Наречие n -(e)s")
* Click on a dictionary to (un-)prioritize or (un-)block it, in particular:
  LMB on:
    - a common dictionary: prioritize it
    - prioritized dictionary: do nothing (in future: increase priority)
    - blocked dictionary: unblock it
  RMB on:
    - a common dictionary: block it
    - prioritized dictionary: unprioritize it
    - blocked dictionary: unblock it
* Do not load the config file twice
* Do not warn about an empty URL or text when there are no articles yet
* Select transcription and dictionary "... фраз" by mouse
* Parse the article following "... фраз"
* Add a key: bind_toggle_sel

## 5.8
* Add a heuristic analysis for local Stardict dictionaries (Stardict2 type)
* Add a special sorting of parts of speech

## 5.7.2
* Fix tagging for the 'invoice' article

## 5.7.1
* Set a timeout (6 seconds by default)

## 5.7
* Add a heuristic analysis for local Stardict dictionaries (Stardict1 type)
* Insert "bookmarks" (restore a selection for articles from the History,
  but only when settings of the current view remain unchanged)
* Navigate by sections of column 3 (Shift-Down, Shift-Up by default)
* Add keys: bind_col1_down, bind_col1_up, bind_col2_down, bind_col2_up,
            bind_col3_down, bind_col3_up
* Keep (if possible) the column when moving to a preceding/following section
* Ignore the Transcription column when navigating through sections

## 5.6.2
* Move phrases (at any view mode) to the end

## 5.6.1
* Fix a bug (preserve fixed column contents upon changing views)

## 5.6
* Quickly go to elements of the 1st and 2nd column:
  - Control-Down: go to the next element of the 1st column
  - Control-Up  : go to the previous element of the 1st column
  - Alt-Down    : go to the next element of the 2nd column
  - Alt-Up      : go to the previous element of the 2nd column
* Fix a bug (Down arrow navigation)
* Improve color assignment in the Vertical mode
* Expand abbreviations for column 1

## 5.5.2
* Fix a bug (do not warn after clearing the History)
* Delete a key: bind_copy_sel_alt2

## 5.5.1
* Automatically set a color of blocked elements on the basis of the column font
  color

## 5.5
* Automatically set a color of priority elements on the basis of the column
  font color
* Set a font color, family and size on the basis of the column number instead
  of the block type
* Rename keys:
  - color_dics         -> color_col1
  - font_dics_family   -> font_col1_family
  - font_dics_size     -> font_col1_size
  - color_speech       -> color_col2
  - font_speech_family -> font_col2_family
  - font_speech_size   -> font_col2_size
* Create new keys: font_col3_family, font_col4_family, font_col3_size,
                   font_col4_size

## 5.4.3
* Fix a bug (use an item with the same name in the History)
* Migrate to ARTICLEID

## 5.4.2
* Fix some bugs
* Set hotkeys for the History widget: Home - go to the start of the list, End -
  go to the end of the list.

## 5.4.1
* Align cells by top

## 5.4
* Scroll a button panel if it exceeds widget sizes. In order to scroll
  the panel, move the mouse pointer to a left or right corner.

## 5.3
* Select fixed columns
* Settings menu
* Make scrolling by keys more accurate

## 5.2
* Set a default column width
* Add a key: col_width (set to 0 to select the column width
  automatically)

## 5.1.5
* Fix word forms

## 5.1.4
* Inform about missing articles

## 5.1.3
* Set a special behavior for a mouse wheel (Windows)

## 5.1.2
* Fix button hints

## 5.1.1
* Fix Ctrl-c-c (Ctrl-Ins-Ins)

## 5.1
* New tag parser: parse tags, including nested ones, more accurately
* Determine word forms
* Color corrections with green (the 1st level)
* Refactor the code, use a database
* Print an article (using a browser in a landscape orientation)
* Enhance visibility of blocks for horizontal/vertical scrolling
* Add a welcome screen
* Loop moves using arrows (go to the start from the end and vice versa)
  (to be elaborated)
* Rename CopyTermsOnly to SelectTermsOnly
* Add keys: bind_print
* Delete keys: bind_add_cell, bind_delete_cell, bind_go, bind_go_alt,
               bind_go_search, bind_go_search_alt, bind_go_url, bind_iconify,
               bind_move_*

## 5.0
* Add a basic Stardict support
* Fix the bug causing skipping cells

## 4.10
* Add phonetic signs

## 4.9
* Add a drop-down list to select the number of columns
* Automatically alphabetize dictionaries and then group them by word
  forms
* Add new modes: blacklisting, prioritizing, terms alphabetizing
* Refactor the code
* Delete keys: bind_clear_history_alt, ExploreMismatch, SelectTermsOnly,
               ShortHistory, default_*, icon_*
* Change bind_toggle_view_alt to '<Alt-v>' by default

## 4.8.2
* Fix tags when only separate words are found

## 4.8.1
* Enhance tag extraction

## 4.8
* Change the ENG-RUS pair link to the alternative one which does not require
  registration when open in a browser
* Define parts of speech in the DEU-RUS pair

## 4.7.8
* Fix links because of changes on multitran.ru
* Move links to the config file

## 4.7.7
* Fix links because of changes on multitran.ru

## 4.7.6
* Fix links because of changes on multitran.ru
* Create a separate repository for shared files ("shared")

## 4.7.5
* Fix scrollbars
* Some improvements in minimize/maximize/activate actions
* Select the entire text when calling the search entry (Linux)
* Clear the search entry upon history deletion
* Add Alt-` combination for calling the program window without translating
  the clipboard contents

## 4.7.1
* Fix searching words with "ъ" character
* Update documentation

## 4.7
* Significantly refactor the code 
* Drop EasyGUI
* Elaborate widgets (center, show/close with a corresponding hotkey or with
  Esc)
* Accelerate loading of previously loaded articles
* Add a new experimental mode of view (arrange dictionaries vertically)
* Check a request length (do not occasionally send a large fragment with
  Ctrl-c-c/Ctrl-Ins-Ins)
* Use Control-Insert-Insert to capture the clipboard
* Fit the search panel on screen at 1024x768
* Delete keys: AutoHideHistory, online_dic_url, bind_get_history,
               icon_change_ui_lang
* Add keys: bind_next_pair, bind_next_pair_alt (select the next language pair,
  F8 and Control-l correspondingly by default), bind_prev_pair,
  bind_prev_pair_alt (select the previous language pair, Shift-F8 and Control-L
  correspondingly by default), bind_toggle_view, bind_toggle_view_alt (select
  the current view, F6 and Control-V correspondingly by default),
  icon_toggle_view_hor, icon_toggle_view_ver
* Move icons to the 'resources' directory
* Cycle navigation through History using Alt-Left and Alt-Right (default
  hotkeys)
* Add symbols Ғ, ғ, Ø, ø
* Due to the new program architecture this is no longer possible to change
  the language in GUI (set the language in the configuration file)

## 4.6
* Make the foreground of the selected cell black by default
* Add the key color_terms_sel_fg
* Rename the key color_terms_sel to color_terms_sel_bg
* Shift the screen so as to show the selected cell when using keyboard
* Fix a bug: cannot quit when the Internet connection is missing
* Set UTF-8 encoding when saving the current view

## 4.5.2
* Add an empty cell
* Add keys: bind_delete_cell, bind_add_cell
* Change key combinations for adding and deleting a cell to
  Control-Insert and Control-Delete correspondingly in order to avoid conflict
  with Delete in the search field
* Update documentation

## 4.5.1
* Lift the window in Openbox
* Fix Control-c-c capture in Windows versions newer than XP

## 4.5
* Delete keys: bind_move_page_start, bind_move_page_end
* Save an article in a current view
* Scroll the screen while searching and when using PageUp/PageDn, Control-Home,
  Control-End
* Enhance navigation using up and down arrows
* Scroll the screen with MMB like in previous versions
* Informing about start/end while searching
* Fix a bug: Highlight a first selectable element when loading an article
* Fix a bug: Do not select parts of speech
* Remove useless code

## 4.4.1
* Delete the key: mclientSaveTitle
* Set focus on the window in case of Control-c-c in Windows versions newer than
  XP
* Show the license information on the third-parties in GUI
* Update a window title correctly

## 4.4
* Delete keys: bind_toggle_iconify, bind_watch_clipboard,
               bind_watch_clipboard_alt, window_size, ShowWallet, TextButtons,
               UseOptionalButtons, AlwaysMaximize
* Translate clipboard by Control-c-c (instead of "the Clipboard Mode")
* Navigate using up and down arrows, Home, End, Control-Home and Control-End
* Fix the icon in past Windows XP systems

## 4.3.1.
* Fix an empty history bug

## 4.3
* Add keys: color_speech, font_speech_family, font_speech_size
* Delete keys: ReadOnlyProtection, InternalDebug, Spelling, UnixSelection,
  icon_main, tab_length, bind_search_field
* Delete symbols '<' and '>', if cyrillic symbols are nearby (define tags more
  accurately)
* Recognize when an element marked as a term is actually a comment
* Delete the tag <eq>
* Detect parts of speech

## 4.2
* Define cell borders more accurately
* Select cells more accirately (still needs to be elaborated)

## 4.1
* Fix a bug when moving to a previous article
* Fix a bug when copying a cell with a hotkey
* Delete a cell (the Delete key)

## 4.0
* Column view
* Delete keys: TermsColoredSep, bind_hide_top, color_borders, font_comments,
  font_dics, font_terms
* Add keys: CopyTermsOnly, SelectTermsOnly, font_comments_size, font_dics_size,
  font_terms_size, bind_hide_top, font_comments_family, font_dics_family,
  font_terms_family

## 3.12.1
* Fix a bug that prevents from restoring default settings in case the config
  file is missing or corrupted
* Refactor the code

## 3.12
* Temporarily enable/disable minimizing the window with copying actions
  (bind_toggle_iconify)
* Copy the URL of the current term to clipboard (bind_copy_url)
* Copy the URL of the article to clipboard (bind_copy_article_url)
* Turn off the Clipboard Mode only when the user does so

## 3.11
* Separate dictionary titles and terms with tabs
* Add keys tab_length (Tabulation size in symbols), ExploreMismatch (Show
  a translation of the last word of a phrase that was not found)
* Provide links for separate matches if the searched phrase was not found
* Section "Phrases"

## 3.10
* Add symbols ā, Ā
* Add pair RUS <=> XAL, since otherwise a wrong URL is formed for words
  in Russian
* Open a webpage with a definition of the current term (keys: web_search_url,
  bind_define, icon_define)
* "About" window is now on foreground in Windows
* Provide support for '<Control-a>' ("Select All") combination in the search
  field

## 3.9.1
* The special symbols window is now on foreground in Windows
* Buttons for pasting special symbols are increased in size

## 3.9
* Fix a conflict of Alt-F4 and F4 (Alt-F4 works again)
* Paste special symbols (keys icon_spec_symbol, bind_spec_symbol, spec_syms,
  AutoCloseSpecSymbol)

## 3.8.1
* Fix the bug in the search
* Add the bind_watch_clipboard_alt config key

## 3.8
* Fix hang-up after canceling saving article.
* Minimize the window using MMB (bind_close_top) when not in the Clipboard Mode
* (Optionally) Hide the History field after copying items in it or following
  them (AutoHideHistory)
* Rely on URL instead of string requests in the History
* Add a ShortHistory key: add requests that already have been added to
  the History (0, False) or not (1, True). Set ShortHistory=0 to make
  navigation with buttons '→' and '←' more consistent.
* Add new hotkeys (config keys bind_reload_article_alt, bind_save_article_alt,
  bind_toggle_history, bind_toggle_history_alt, bind_clear_history_alt,
  bind_open_in_browser, bind_open_in_browser_alt, bind_watch_clipboard), Esc
  and Ctrl-w to close the window (in the Clipboard Mode), Esc to minimize
  the window (in the regular mode)
* Fix the button for switching a UI language
* Change the clear history button image

## 3.7
* Use the same key combination both for the terms field and the search field.
  If the search field is not empty, then its contents will be translated,
  otherwise the terms area will be translated.
* Rename the config file to mclient.cfg
* Delete keys bind_go_url_alt, bind_go_url_alt2. Add keys font_style,
  online_dic_url, ui_lang, win_encoding, InternalDebug, ReadOnlyProtection.
* Eliminate revealed hangups at certain requests
* Load default settings if the configuration file is missing or has errors
* Select the default GUI language (ui_lang)
* Fix a bug in the Clipboard Mode when copying by the program itself

## 3.6.1
* Add the missing module with EasyGUI

## 3.6
* Add button images (to use text buttons, set TextButtons=1 in the config file)

## 3.5
* Add a case-insensitive search in an article (Control-F3 - new search, F3 -
  new search/search down, Shift-F3 - search up)
* F5 to reload the article
* F2 to save to disk or copy the article text or code to clipboard
* Buttons 'Save' and 'Search in article'
* Paste the previous request to the search field and copy it to clipboard
  (input '!' (repeat_sign) or '!!' (repeat_sign2) to the clipboard and press
  Enter)
* Add new hotkeys (F1 - 'About', etc.)

## 3.4
* Fix a bug: embedded user comments are now visible (but only inside the tag
  <span STYLE="color:rgb(60,179,113)">)
* Fix a bug: a request "refer as" does not hang the app now
* Fix a bug: updating the History field after changing the UI language caused
  an error
* Close the current window in the Clipboard mode using MMB (bind_close_top)
* Add a hotkey Control-q (bind_quit_now) to quit the app
* Delete MBSysEnabled key because double-click paste should be controlled
  differently
* Rewrite clipboard algorithms
* Fix regression bugs that were revealed
* Fix pasting with MMB

## 3.3
* Set hotkeys (keyboard + mouse) in the config file
* Press RMB to copy a History entry
* Change loading a History entry by LMB to double LMB, because copying
  a History entry requires selecting first this entry by LMB
* Set the config key MBSysEnabled to indicate whether clipboard paste works
  on the system level (1, True) or this should be done on the program level
  (0, False)

## 3.2
* Disallow empty search requests
* Fix bugs: the article is reloaded before quitting the program and after
  showing/hiding the History
* Remember current selection when showing/hiding the History (only if
  the selection is located on the first page)
* Enable the mouse wheel on Windows
* Enable the scrollbar (some corrections may be necessary, especially,
  on Windows)
* Change hotkeys to go to the preceding/following page to Alt-Left and
  Alt-Right correspondingly in order not to conflict with the search field

## 3.1
* Drop switching the search field and terms field (F6 is no longer supported)
* Enter on a basic and expanded keyboard in the terms field has been reassigned
  to Shift-Enter

## 3.0
﻿* Use mouse for control: a term is selected according to the mouse pointer, use
  the left mouse button (LMB) to translate the selection, use the right mouse
  button (RMB) to copy the selection; wheel up - page up, wheel down - page
  down
* Do not duplicate entries in the History
* Use RMB to clear the History
* Ignore URL links when translating in the Clipboard mode
* Use RMB to clear the search field
* Use the middle mouse button to clear the search field and paste clipboard
  contents
* Fix the bug: the History is not added while in the Clipboard mode
* Go to the previous article from the History (Ctrl-←), go to the next article
  from the History (Ctrl-→) (there are still some inaccuracies, for example,
  selecting '8 phrases' will go to 'phrase', not to a corresponding URL)
* Use key bindings in the search field as well (except for Return)

## 2.3
* Enhance keyboard navigation:
    ←: go to the nearest term to the left
    →: the nearest term to the right
    ↑: the first term of the preceding dictionary
    ↓: the first term of the following dictionary
    Home: the first term of the current dictionary
    End: the last term of the current dictionary
    Ctrl-Home: the first term of the article
    Ctrl-End: the last term of the article
    Shift-Home: the first term of the current page
    Shift-End: the first term of the current page
    PageUp: the first term of the preceding page
    PageDown: the first term of the following page
    
## 2.2
* Archive program builds, so you do not need to download again the whole ZIP
  when the program updates
* Fix keyboard navigation

## 2.1
* Add an icon
* Focus on the search field by default (see FocusSearch in the config file;
  still focus on the terms field in the Clipboard mode)
* Separate adjacent terms with semicolumn by default. Use TermsColoredSep=1
  to separate terms with a coloured space
* Change line breaks to Windows-style in the config file
* Update manuals
* Update README.md

## 2.0
* Configure the window size
* Confirm the further operation if the server connection has been lost instead
  of entering an infinite loop
* Add a config file
* Change colors and fonts

## 1.1
* Remove the root window while waiting for clipboard
* Keep the default window title (optional)
* Show the window above all
* Close the window instead of minimizing in the clipboard mode

## 1.0
Initial release
