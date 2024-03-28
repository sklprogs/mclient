# MClient 7.0

[Description and objectives](#description-and-objectives)

[System requirements](#system-requirements)

[Installing and running](#installing-and-running)
  - [Running build](#running-build)
    - [Running build on Windows](#running-build-on-windows)
    - [Running build on Linux](#running-build-on-linux)
  - [Running script](#running-script)
    - [Running script on Windows](#running-script-on-windows)
    - [Running script on Linux](#running-script-on-linux)

[Use and functionality](#use-and-functionality)

[Keyboard and mouse bindings](#keyboard-and-mouse-bindings)

[Configuration file](#configuration-file)

[Colors][#colors]

[Fonts][#fonts]
  - [Fonts on Windows](#fonts-on-windows)
  - [Fonts on Linux](#fonts-on-linux)

[Buttons](#buttons)

[Issues](#issues)

[To-developers](#to-developers)

***

## Description and Objectives

Multitran Online Client (MClient) is a program which connects to the
[multitran.com](https://www.multitran.com/) web-site and returns translation of
words and phrases entered by the user. Local dictionaries in the formats of
Stardict, Lingvo (DSL) and Multitran (Demo) have initial support. The program
enables instant access to article items and their sorting,
blocking\/prioritizing of sibjects, and so on. Articles are adjustable and
formatted in columns.

## System Requirements

Operating system: Windows 10 (or later) or Linux.

Mac OS X was not tested; however, there are no significant issues that would
hinder starting the program on this system.

An internet connection is required (for online dictionaries).

Free space: 244 Mb (Linux build)

Free RAM: 115 Mb (Linux build)

## Installing and Running

You can run either a build (as `.exe` for Windows and `.AppImage` for Linux or
a script (source code) itself. The build does not require installation, just
copy it in some directory of your choice. To run the script, install Python 3
and all dependencies.

### Running Build on Windows

Windows 10 or later is required. You may also need to Windows updates and
[vcredist](https://www.microsoft.com/en-us/download/details.aspx?id=48145).

1. Download [mclient_win64.7z](https://github.com/sklprogs/mclient/releases/download/latest/mclient_win64.7z).
1. Unpack the archive to a writeable directory (you may need [7-zip](https://www.7-zip.org/)).
1. Run `mclient.cmd`.

### Running Build on Linux

1. Download [mclient-linux-x86_64-glibc2.36.AppImage](https://github.com/sklprogs/mclient/releases/download/latest/mclient-linux-x86_64-glibc2.36.AppImage).
1. The glibc version must be 2.36 or later. To determine the current version,
run `ldd --version`. If the version is too old, update your system.
1. Install FUSE (if not installed).
1. Allow file execution (for example, by running `chmod +x mclient-linux-x86_64-glibc2.36.AppImage`).
1. Run the file as a common application.

### Running Script on Windows

1. Install [Git for Windows](https://git-scm.com/download/win).
   - Select the option **Git from the command line and also from 3rd-party
     software**.
2. Start the terminal (for example, press `Win+R` and enter `cmd`).
3. Enter the following:
```
cd %USERPROFILE%
mkdir sklprogs
cd sklprogs
git clone https://github.com/sklprogs/shared_qt.git
git clone https://github.com/sklprogs/mclient.git
```
4. Install [Python 3](https://www.python.org/) to `C:\Python`.
   - Add Python to `PATH`.
5. Update `pip` by entering the following in the terminal:
   `python -m pip install --upgrade pip`
6. Install dependencies:
   `pip install -r "%USERPROFILE%\sklprogs\mclient\docs\requirements.txt"`.
7. Install pyWinhook: `pip install pywinhook`.
8. Configure and run the program:
```
move sklprogs\shared_qt\src C:\Python\Lib\site-packages\skl_shared_qt
move sklprogs\shared_qt\resources C:\Python\Lib\site-packages\resources
python sklprogs\mclient\src\mclient.py
```

### Running Script on Linux

1. Start a terminal and enter the following (commands and package names may
   differ depending on your distribution):
```
sudo apt-get install git python3 python3-xlib python3-venv
mkdir ~/sklprogs
cd ~/sklprogs
git clone https://github.com/sklprogs/shared_qt.git
git clone https://github.com/sklprogs/mclient.git
python3 -m venv mclient_venv
source "./mclient_venv/bin/activate"
python3 -m pip install --upgrade pip
pip install -r "./mclient/docs/requirements.txt"
```
2. Configure and run the program (paths may differ depending on your Python
   version):
```
ln -s "$HOME/sklprogs/shared_qt/src" "$HOME/sklprogs/mclient_venv/lib/python3.11/site-packages/skl_shared_qt"
ln -s "$HOME/sklprogs/shared_qt/resources" "$HOME/sklprogs/mclient_venv/lib/python3.11/site-packages/resources"
python3 "$HOME/sklprogs/mclient/src/mclient.py"&
deactivate
```

Antiviruses may alert about a keylogger, since MClient captures `Ctrl`, `Ins`
and `c` keypresses in other applications to monitor clipboard. Data on
keypresses is not stored or sent anywhere. If `Ctrl+C+C` and `Ctrl+Ins+Ins`
hotkeys do not work, add MClient to white lists in antiviruses and turn off
clipboard managers (if any).

## Use and Functionality

You need a permanent internet connection to use online sources. If the program
is unable to get an article from the website, the corresponding warning
will be shown. You will need to check the internet connection and
accessibility of websites (multitran.com and others). It is often enough to
click the **OK** button just after receiving this warning message.

A request can comprise one or several words. If the requested phrase is
not found with the current declension or grammatical number, Multitran will
automatically select the relevant declension and number. Thus, if you enter
*colorants*, Multitran will show a *colorant* article.

The program properly processes such symbols as *á*, *ß*, *è*, and so on.

## Keyboard and Mouse Bindings

| Action | Mouse bindings | Keyboard bindings | Config key |
| --- | --- | --- | --- |
| Quit | Click <img src="../resources/buttons/quit_now.png" width="36" height="36" /> or a close button | `Ctrl+Q`, `Alt+F4`, `F10` | `actions → quit` |
| Minimize | Middle click | `Esc` | |
| Translate the selected cell | Left click or <img src="../resources/buttons/go_search.png" width="36" height="36" /> | `Enter` | |
| Show program info | <img src="../resources/buttons/show_about.png" width="36" height="36" /> | `F1` | `actions → toggle_about` |
| Go to the nearest cell to the left | Mouse over | `←` | |
| Go to the nearest cell to the right | Mouse over | `→` | |
| Go to the previous cell of the current column | Mouse over | `↑` | |
| Go to the next cell of the current column | Mouse over | `↓` | |
| Go to the first cell of the current row | Mouse over | `Home` | |
| Go to the last cell of the current row | Mouse over | `End` | |
| Go to the first cell of the first row | Mouse wheel or slider | `Ctrl+Home` | |
| Go to the last cell of the last row | Mouse wheel or slider | `Ctrl+End` | |
| Go to the previous page | Mouse wheel or slider | `PageUp` | |
| Go to the next page | Mouse wheel or slider | `PageDown` | |
| Go to the previous section of column #1 | Mouse wheel or slider | `Ctrl+Up` | `actions → col1_up` |
| Go to the next section of column #1 | Mouse wheel or slider | `Ctrl+Down` | `actions → col1_down` |
| Go to the previous section of column #2 | Mouse wheel or slider | `Alt+Up` | `actions → col2_up` |
| Go to the next section of column #2 | Mouse wheel or slider | `Alt+Down` | `actions → col2_down` |
| Go to the previous section of column #3 | Mouse wheel or slider | `Shift+Up` | `actions → col3_up` |
| Go to the next section of column #3 | Mouse wheel or slider | `Shift+Down` | `actions → col3_down` |
| Go to the previous section of column #4 | Mouse wheel or slider | `Ctrl+Shift+Up` | `actions → col4_up` |
| Go to the next section of column #4 | Mouse wheel or slider | `Ctrl+Shift+Down` | `actions → col4_down` |
| Search forward | | `F3` | `actions → search_article_forward` |
| Search backward | | `Shift+F3` | `actions → search_article_backward` |
| Start new search | <img src="../resources/buttons/search_article.png" width="36" height="36" /> | `Ctrl+F3` | `actions → re_search_article` |
| Reload the article | <img src="../resources/buttons/reload.png" width="36" height="36" /> | `F5`, `Ctrl+R` | `actions → reload_article` |
| Open in a browser | <img src="../resources/buttons/open_in_browser.png" width="36" height="36" /> | `F7`, `Ctrl+B` | `actions → open_in_browser` |
| Set the next source language | Left click on the drop-down list of languages | `F8`, `Ctrl+K` | `actions → next_lang1` |
| Set the previous source language | Left click on the drop-down list of languages | `Shift+F8`, `Shift+Ctrl+K` | `actions → prev_lang1` |
| Set the next target language | Left click on the drop-down list of languages | `F9`, `Ctrl+L` | `actions → next_lang2` |
| Set the previous target language | Left click on the drop-down list of languages | `Shift+F9`, `Shift+Ctrl+L` | `actions → prev_lang2` |
| Open a web page with a definition of the current article title | <img src="../resources/buttons/define.png" width="36" height="36" /> | | |
| Open a web page with a definition of the selected block | | `Ctrl+D` | `actions → define` |
| Save or copy the current article | <img src="../resources/buttons/save_article.png" width="36" height="36" /> | `Ctrl+S` | `actions → save_article` |
| Copy the URL of the current article | | `Ctrl+F7` | `actions → copy_article_url` |
| Copy the URL of the current term | | `Shift+F7` | `actions → copy_url` |
| Copy the text of the selected cell | Right click | `Ctrl+Enter` | `actions → copy_sel` |
| Copy a word form corresponding to the selected cell | Select the word form and right click on it | `Ctrl+W` | `actions → copy_nominative` |
| Look up phrases | | `Alt+F` | `actions → go_phrases` |
| Translate clipboard from an external application | | `Ctrl+C+C`, `Ctrl+Ins+Ins` | |
| Paste clipboard | Right click on the search field and select **Paste** or click <img src="../resources/buttons/paste.png" width="36" height="36" /> | `Ctrl+V` | |
| Paste the current request | <img src="../resources/buttons/repeat_sign.png" width="36" height="36" /> | `!` | |
| Paste the previous request | <img src="../resources/buttons/repeat_sign2.png" width="36" height="36" /> | `!!` | |
| Paste a special symbol | <img src="../resources/buttons/spec_symbol.png" width="36" height="36" /> | `Ctrl+E` | `actions → toggle_spec_symbols` |
| Toggle history | <img src="../resources/buttons/toggle_history.png" width="36" height="36" /> | `F4, Ctrl+H` | `actions → toggle_history` |
| Clear history | | `Ctrl+Shift+Del` | `actions → clear_history` |
| Go to the previous article | <img src="../resources/buttons/go_back.png" width="36" height="36" /> | `Alt+Left` | `actions → go_back` |
| Go to the next article | <img src="../resources/buttons/go_next.png" width="36" height="36" /> | `Alt+Right` | `actions → go_next` |
| Go to a history item | Left click | ↑, ↓ | |
| Copy a history item title | Right click | | |
| Create a printer-friendly page | <img src="../resources/buttons/print.png" width="36" height="36" /> | `Ctrl+P` | `actions → print` |
| Toggle block-by-block mode | | `F2` | `actions → select_block` |
| Show a list of blocked subjects  | | `Ctrl+Shift+B` | `actions → show_block` |
| Show a list of prioritized subjects | | `Ctrl+Shift+P` | `actions → show_prior` |
| Show settings | <img src="../resources/buttons/settings.png" width="36" height="36" /> | `Alt+S`, `F12` | `actions → toggle_settings` |
| Swap source and target languages | <img src="../resources/buttons/swap_langs.png" width="36" height="36" /> | `Ctrl+Shift+Space` | `actions → swap_langs` |
| Toggle cell alphabetization | <img src="../resources/buttons/alphabet_on.png" width="36" height="36" /> | `Alt+A` | `actions → toggle_alphabet` |
| Toggle subject prioritization | <img src="../resources/buttons/priority_on.png" width="36" height="36" /> | `Alt+P` | `actions → toggle_priority` |

You can change key bindings in the configuration file.

The language pair can be selected from the drop-down list. Please note
that, if, for example, the English-Russian language pair is selected,
you do not have to switch to the Russian-English pair (not taking into
consideration the keyboard layout), because Multitran can automatically
determine a language of the term entered by you. Owing to the specifics of
multitran.com, Russian-Kazakh and Kazakh-Russian pairs are separated.

In order to switch between buttons using keyboard, press Tab and
Shift+Tab. A button can be activated with the left mouse button click,
Enter (on the basic or expanded keyboard) or Space.

In order to paste a symbol absent on your keyboard, click
<img src="../resources/buttons/spec_symbol.png" width="36" height="36" />. You
can remove or add symbols on demand (see the section
`actions → toggle_spec_symbols` of the configuration file).

You can show\/hide the history of requests by clicking
<img src="../resources/buttons/toggle_history.png" width="36" height="36" />.
You can repeat a request by clicking once on a required term in the history
field. You can scroll the history field using the mouse wheel.

Click <img src="../resources/buttons/watch_clipboard_off.png" width="36" height="36" />
to translate terms from clipboard. The language pair, as always, is determined
by the value set in the drop-down list. After a `Ctrl+C+C` or `Ctrl+Ins+Ins`
combination is captured in any application that supports copying using `Ctrl+C`\/`Ctrl+Ins`,
MClient will load a new article correspondingly to the clipboard content.

To open the current article in a default browser, click
<img src="../resources/buttons/open_in_browser.png" width="36" height="36" />.

To get a definition of the article title, click
<img src="../resources/buttons/define.png" width="36" height="36" />. To get
a definition of the selected block, use the Ctrl+D combination (the section
`actions → define` of the configuration file).

The program interface currently supports 2 languages &mdash; Russian and
English. The interface language is determined automatically on the basis
of the system language.

To look up the copyright information, click
<img src="../resources/buttons/show_about.png" width="36" height="36" />.

To exit the program, click the close button of the main window or
<img src="../resources/buttons/quit_now.png" width="36" height="36" />. All
remaining program windows (for example, a settings window) should be closed as
well.

## Configuration File

You can adjust your settings in the configuration file `mclient.json`,
which is stored in the directory `C:\users\<USER>\Application Data\mclient`
(Windows) or `$HOME/.config/mclient` (Linux). If the configuration file
is absent, it will be created. If the new program version uses new keys, they
should be automatically added to the existing configuration file without
affecting existing keys. However, if the key `config → min_version` is absent
or its value is lower than the one accepted by the program, the configuration
file will be forcibly updated, and all keys will be set to default values.

## Colors

Colors are defined by corresponding keys of the [configuration file](#configuration-file).
Change the `color` key value of a desired object by indicating a color name
from [this list](https://www.w3.org/TR/SVG11/types.html#ColorKeywords)
or a valid HEX code of any color (the first character is `#` followed by 6
Latin letters). If the configuration file indicates a color name, the color key
value can be overwritten with the corresponding HEX code. The HEX code of
a color can be determined using various websites, for example,
[here](https://www.colorhexa.com).

Colors of prioritized and blocked subjects are set automatically depending on
a text color of the column to which they belong. A prioritized subject has
a more saturated color, and a color of a blocked subject is less saturated than
the color of the corresponding column. To change a column text color and
therefore a subject color, set a value of the key `columns → 1 → font →
color` (replace `1` with the number of the required column within the range of
1 to 4).

| Object | Configuration file key | Default color | HEX code |
| --- | --- | --- | --- |
| Line at the bottom of too wide cells | `rows → border → color` | | `#CCCCCC` |
| Text of column #1 | `columns → 1 → font → color` | *coral* | `#FF7F50` |
| Text of column #2 | `columns → 2 → font → color` | *cadet blue* | `#5F9EA0` |
| Text of column #3 | `columns → 3 → font → color` | *slate gray* | `#708090` |
| Text of column #4 | `columns → 4 → font → color` | *slate gray* | `#708090` |
| Text of comments | `comments → font → color` | *gray* | `#808080` |
| Text of terms | `terms → font → color` | *black* | `#000000` |

## Fonts

### Fonts on Windows

Available fonts can be found in folders `C:\WINDOWS\Fonts` and
`C:\Users\<USER>\AppData\Local\Microsoft\Windows\Fonts` (Windows 10 Build 1809
and later).

### Fonts on Linux

The `fontconfig` utility is used by default to find fonts. To get the list of
families of available fonts, run `fc-list : family`.

## Buttons

You can use your own images for buttons. These images must be in a `.png`
format and be located in the `resources/buttons` directory. The majority of
them are taken from the Oxygen collection.

## Issues

If a dictionary entry is displayed incorrectly, send me an address (URL)
of this entry or indicate dictionaries being used. You can send me an email
message in the **About** window.

## To Developers 

The program is distributed on the terms of GPL v.3. The program interface is
translated into Russian and English (`resources/locale`), but you can add your
own translations.
