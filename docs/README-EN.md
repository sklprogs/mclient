# MClient 7.0
[Description and objectives](#description-and-objectives)
[System requirements](#system-requirements)
[Installing and running](#installing-and-running)
  - [Running Windows build](#running-windows-build)
  - [Running Linux build](#running-linux-build)
  - [Running script on Windows](#running-script-on-windows)
  - [Running script on Linux](#running-script-on-linux)
[Use and functionality](#use-and-functionality)
[Hotkeys and mouse keys](#hotkeys-and-mouse-keys)

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

You can run either the build (in the `.exe` format for Windows and `.AppImage`
for Linux (if available)) or the script (source code) itself. The build
does not require installation, just copy it in some directory of your
choice. To run the script, install Python 3 and all dependencies.

### Running Windows Build

Windows 10 or later is required. You may also need to Windows updates and
[vcredist](https://www.microsoft.com/en-us/download/details.aspx?id=48145).

1. Download [mclient_win64.7z](https://github.com/sklprogs/mclient/releases/download/latest/mclient_win64.7z).
1. Unpack the archive to a writeable directory (you may need [7-zip](https://www.7-zip.org/)).
1. Run `mclient.cmd`.

### Running Linux Build

1. Install FUSE (if not installed).
1. Allow file execution (for example, by running `chmod +x mclient-linux-x86_64-glibc2.36.AppImage`).
1. Run the `.AppImage` file.

### Running Script on Windows

1. Install [Git for Windows](https://git-scm.com/download/win).
   - Select the option **Git from the command line and also from 3rd-party
     software**.
1. Start the terminal (for example, press `Win+R` and enter `cmd`).
1. Enter the following:
```
cd %USERPROFILE%
mkdir sklprogs
cd sklprogs
git clone https://github.com/sklprogs/shared_qt.git
git clone https://github.com/sklprogs/mclient.git
```
1. Install [Python 3](https://www.python.org/) to `C:\Python`.
   - Add Python to `PATH`.
1. Update `pip` by entering the following in the terminal:
   `python -m pip install --upgrade pip`
1. Install dependencies:
   `pip install -r "%USERPROFILE%\sklprogs\mclient\docs\requirements.txt"`.
1. Install pyWinhook: `pip install pywinhook`.
1. Configure and run the program:
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
1. Configure and run the program (paths may differ depending on your Python
   version):

```
ln -s "$HOME/sklprogs/shared_qt/src" "$HOME/sklprogs/mclient_venv/lib/python3.11/site-packages/skl_shared_qt"
ln -s "$HOME/sklprogs/shared_qt/resources" "$HOME/sklprogs/mclient_venv/lib/python3.11/site-packages/resources"
python3 "$HOME/sklprogs/mclient/src/mclient.py"&
deactivate
```

Antiviruses may alert about a keylogger, since MClient captures `Ctrl`, `Ins`
and `c` keypresses in other applications to monitor clipboard. Data on
keypresses is not stored or sent anywhere. If `Ctrl+c+c` and `Ctrl+Ins+Ins`
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

## Hotkeys and Mouse Keys

Abbreviations: LMB &mdash; left mouse button, RMB &mdash; right mouse button,
MMB &mdash; middle mouse button

+----------------+----------------+----------------+----------------+
| Hotkeys        | Mouse          | Action         | Config Key     |
+----------------+----------------+----------------+----------------+
|                |                |                |                |
+----------------+----------------+----------------+----------------+
| Ctrl-q,        | click X        | quit the       | bind_quit      |
| Alt-F4, F10    |                | program        |                |
+----------------+----------------+----------------+----------------+
| Esc            | click MMB      | minimize the   |                |
|                |                | window         |                |
+----------------+----------------+----------------+----------------+
| F1             | Button "About" | program info   | b              |
|                |                |                | ind_show_about |
+----------------+----------------+----------------+----------------+
|                |                |                |                |
+----------------+----------------+----------------+----------------+
| ←              | point at a     | go to the      |                |
|                | cell           | nearest cell   |                |
|                |                | to the left    |                |
+----------------+----------------+----------------+----------------+
| →              | point at a     | the nearest    |                |
|                | cell           | cell to the    |                |
|                |                | right          |                |
+----------------+----------------+----------------+----------------+
| ↑              | point at a     | the previous   |                |
|                | cell           | cell of the    |                |
|                |                | current column |                |
+----------------+----------------+----------------+----------------+
| ↓              | point at a     | the following  |                |
|                | cell           | cell of the    |                |
|                |                | current column |                |
+----------------+----------------+----------------+----------------+
| Home           | point at a     | the first cell |                |
|                | cell           | of the current |                |
|                |                | line           |                |
+----------------+----------------+----------------+----------------+
| End            | point at a     | the last cell  |                |
|                | cell           | of the current |                |
|                |                | line           |                |
+----------------+----------------+----------------+----------------+
| Ctrl-Home      | use the mouse  | the first cell |                |
|                | wheel to go to | of the article |                |
|                | the 1^st^      |                |                |
|                | page, point at |                |                |
|                | a term, use    |                |                |
|                | LMB            |                |                |
+----------------+----------------+----------------+----------------+
| Ctrl-End       | use the mouse  | the last cell  |                |
|                | wheel to go to | of the article |                |
|                | the last page, |                |                |
|                | point at a     |                |                |
|                | term, use LMB  |                |                |
+----------------+----------------+----------------+----------------+
| PageUp         | wheel up       | the preceding  |                |
|                |                | page           |                |
+----------------+----------------+----------------+----------------+
| PageDown       | wheel down     | the following  |                |
|                |                | page           |                |
+----------------+----------------+----------------+----------------+
|                |                |                |                |
+----------------+----------------+----------------+----------------+
| F2, Ctrl-s     | ![](           | save or copy   | bind           |
|                | Pictures/10000 |                | _save_article, |
|                | 00100000024000 |                | bind_sa        |
|                | 00024B727DC6C2 |                | ve_article_alt |
|                | 6280AA2.gif){w |                |                |
|                | idth="0.953cm" |                |                |
|                | height="0      |                |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
| F3             | \-             | search down    | bind_search_a  |
|                |                |                | rticle_forward |
+----------------+----------------+----------------+----------------+
| Shift-F3       | \-             | reverse search | bind_search_ar |
|                |                |                | ticle_backward |
+----------------+----------------+----------------+----------------+
| Ctrl-F3        | ![](           | new search     | bind_re_       |
|                | Pictures/10000 |                | search_article |
|                | 00100000024000 |                |                |
|                | 000247241776DD |                |                |
|                | F923AC7.gif){w |                |                |
|                | idth="0.953cm" |                |                |
|                | height="0      |                |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
| F5, Ctrl-r     | ![](           | reload         | bind_r         |
|                | Pictures/10000 |                | eload_article, |
|                | 00100000024000 |                | bind_relo      |
|                | 000245D3002727 |                | ad_article_alt |
|                | 43C464A.gif){w |                |                |
|                | idth="0.953cm" |                |                |
|                | height="0      |                |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
| F6, Alt-v      | ![](           | toggle the     | bin            |
|                | Pictures/10000 | article view   | d_toggle_view, |
|                | 00100000024000 | mode           | bind_t         |
|                | 00024304DC9694 |                | oggle_view_alt |
|                | 3D19DB9.gif){w |                |                |
|                | idth="0.953cm" |                |                |
|                | height="0      |                |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
| F7, Ctrl-b     | ![](           | open the       | bind_op        |
|                | Pictures/10000 | current        | en_in_browser, |
|                | 00100000024000 | article in a   | bind_open_     |
|                | 000249CD8194D7 | browser        | in_browser_alt |
|                | 9602CFF.gif){w |                |                |
|                | idth="0.953cm" |                |                |
|                | height="0      |                |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
| F8, Ctrl-L     | LMB on a       | select the     | b              |
|                | pull-down menu | next language  | ind_next_pair, |
|                |                | pair           | bind           |
|                |                |                | _next_pair_alt |
+----------------+----------------+----------------+----------------+
| Shift-F8,      | LMB on a       | select the     | b              |
| Ctrl-Shift-L   | pull-down menu | previous       | ind_prev_pair, |
|                |                | language pair  | bind           |
|                |                |                | _prev_pair_alt |
+----------------+----------------+----------------+----------------+
| Ctrl-d         | ![](           | define the     | bind_define    |
|                | Pictures/10000 | current term   |                |
|                | 00100000024000 |                |                |
|                | 00024D17E1A1AE |                |                |
|                | 0443354.gif){w |                |                |
|                | idth="0.953cm" |                |                |
|                | height="0      |                |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
| Shift-F7       | \-             | copy the URL   | bind_copy_url  |
|                |                | of the current |                |
|                |                | term to        |                |
|                |                | clipboard      |                |
+----------------+----------------+----------------+----------------+
| Control-F7     | \-             | copy the URL   | bind_co        |
|                |                | of the article | py_article_url |
|                |                | to clipboard   |                |
+----------------+----------------+----------------+----------------+
|                |                |                |                |
+----------------+----------------+----------------+----------------+
| Enter (basic   | Use LMB        | Translate the  |                |
| or expanded    |                | current        |                |
| keyboard)      |                | selected cell  |                |
+----------------+----------------+----------------+----------------+
| Ctrl-Enter     | Use RMB        | Copy the       | bind_copy_sel, |
|                |                | current        | bin            |
|                |                | selected term. | d_copy_sel_alt |
|                |                | The program    |                |
|                |                | window will    |                |
|                |                | minimize and   |                |
|                |                | show a window  |                |
|                |                | of a program   |                |
|                |                | where the      |                |
|                |                | copied term    |                |
|                |                | can be         |                |
|                |                | inserted.      |                |
+----------------+----------------+----------------+----------------+
|                | Button         | Translate a    |                |
|                | ![](           | word or a      |                |
|                | Pictures/10000 | phrase from    |                |
|                | 00100000024000 | the clipboard  |                |
|                | 000244AD9A50D6 | by capturing   |                |
|                | 81C1B88.gif){w | Ctrl-c-c or    |                |
|                | idth="0.953cm" | Ctrl-Ins-Ins   |                |
|                | hei            | from a         |                |
|                | ght="0.953cm"} | third-party    |                |
|                |                | application.   |                |
+----------------+----------------+----------------+----------------+
|                |                |                |                |
+----------------+----------------+----------------+----------------+
| Enter          | point at the   | translate      |                |
|                | "Search"       | manually input |                |
|                | button, use    | terms          |                |
|                | LMB            |                |                |
+----------------+----------------+----------------+----------------+
| Ctrl-V         | press the      | clear the      | bind_past      |
|                | mouse wheel    | search field,  | e_search_field |
|                |                | paste the      |                |
|                |                | clipboard      |                |
|                |                | contents       |                |
+----------------+----------------+----------------+----------------+
| Backspace      | use RMB        | clear the      | bind_clea      |
|                |                | search field   | r_search_field |
+----------------+----------------+----------------+----------------+
| !              | ![](           | copy the last  | repeat_sign    |
|                | Pictures/10000 | request to     |                |
|                | 00100000024000 | clipboard and  |                |
|                | 00024B6BA0A0D2 | paste it in    |                |
|                | 92EB659.gif){w | the search     |                |
|                | idth="0.953cm" | field          |                |
|                | height="0      |                |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
| !!             | ![](           | copy the       | repeat_sign2   |
|                | Pictures/10000 | next-to-last   |                |
|                | 00100000024000 | request to     |                |
|                | 00024D531E9421 | clipboard and  |                |
|                | B2AC529.gif){w | paste it in    |                |
|                | idth="0.953cm" | the search     |                |
|                | height="0      | field          |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
| Ctrl-a         | \-             | select all     | \-             |
|                |                | text           |                |
+----------------+----------------+----------------+----------------+
| Ctrl-e         | ![](           | Paste a        | bi             |
|                | Pictures/10000 | special symbol | nd_spec_symbol |
|                | 00100000024000 |                |                |
|                | 000249C0C1CB2E |                |                |
|                | 080CFCC.gif){w |                |                |
|                | idth="0.953cm" |                |                |
|                | height="0      |                |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
|                |                |                |                |
+----------------+----------------+----------------+----------------+
| F4, Ctrl-h     | ![](           | show/hide the  | bind_t         |
|                | Pictures/10000 | history        | oggle_history, |
|                | 00100000024000 |                | bind_togg      |
|                | 00024616C5F5A7 |                | le_history_alt |
|                | DA4A42C.gif){w |                |                |
|                | idth="0.953cm" |                |                |
|                | height="0      |                |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
| Ctrl-Shift-Del | Use RMB on the | clear the      | bind           |
|                | button         | history        | _clear_history |
|                | ![](           |                |                |
|                | Pictures/10000 |                |                |
|                | 00100000024000 |                |                |
|                | 00024616C5F5A7 |                |                |
|                | DA4A42C.gif){w |                |                |
|                | idth="0.953cm" |                |                |
|                | hei            |                |                |
|                | ght="0.953cm"} |                |                |
+----------------+----------------+----------------+----------------+
| Alt-←          | ![](           | go to the      | bind_go_back   |
|                | Pictures/10000 | preceding      |                |
|                | 00100000024000 | article in the |                |
|                | 00024019319928 | History        |                |
|                | 052EAE6.gif){w |                |                |
|                | idth="0.953cm" |                |                |
|                | height="0      |                |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
| Alt-→          | ![](           | go to the      | b              |
|                | Pictures/10000 | following      | ind_go_forward |
|                | 00100000024000 | article in the |                |
|                | 00024DCB30ADDA | History        |                |
|                | A2BF303.gif){w |                |                |
|                | idth="0.953cm" |                |                |
|                | height="0      |                |                |
|                | .953cm"}Button |                |                |
+----------------+----------------+----------------+----------------+
| ↑, ↓           | LMB            | go to the      | \-             |
|                |                | History entry  |                |
+----------------+----------------+----------------+----------------+
|                | RMB            | copy the       |                |
|                |                | History entry  |                |
+----------------+----------------+----------------+----------------+

You can change key/mouse bindings in the configuration file. Key
bindings are given
[**here**](http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html).
LMB is indicated as \<ButtonRelease-1\>, MMB -- \<ButtonRelease-2\>, RMB
-- \<ButtonRelease-3\>. Bindings should be embraced with "\>", "\<", for
example: \<Control-F10\>; \<ButtonRelease-1\>. Capital letters in a
hotkey mean pressed Shift, for example, \<Control-V\> means
Ctrl-Shift-v. L is capital in the table above just to avoid confusion.

The language pair can be selected on the drop-down list. Please note
that, if, for example, the English-Russian language pair is selected,
you do not have to switch to the Russian-English pair (not counting the
keyboard layout), because the Multitran can automatically determine the
language of the term entered by you. Owing to the specifics of
multitran.com, Russian-Kazakh and Kazakh-Russian pairs are implemented
as separate.

In order to switch between buttons using keyboard, press Tab and
Shift-Tab. A button can be activated by the left mouse button click,
Enter (on the basic or expanded keyboard) or Space.

In order to paste a symbol missing on your keyboard, press the button
![](Pictures/1000000100000024000000249C0C1CB2E080CFCC.gif){width="0.953cm"
height="0.953cm"}. You can delete or add symbols (see the *spec_syms*
key in the configuration file).

You can enable/disable the history of requests by pressing the button
![](Pictures/100000010000002400000024616C5F5A7DA4A42C.gif){width="0.953cm"
height="0.953cm"}. Requests are sorted from the newest to the oldest.
You can repeat a request by clicking the required term once in the
history field. You can scroll the history field using the mouse wheel.

Press the button to translate terms from the clipboard. The language
pair, as always, is determined by the value provided by the drop-down
list. After Ctrl-c-c or Ctrl-Ins-Ins combination is captured in any
application that supports copying by Ctrl-c/Ctrl-Ins, *mclient *will
load the new article correspondingly to the value stored in the
clipboard.

If the "Capture Ctrl-c-c and Ctrl-Ins-Ins" mode is activated, then the
color of the corresponding button becomes blue. You can disable
Ctrl-c-c/Ctrl-Ins-Ins scanning by pressing the corresponding button
again.

In order to open the current article in a default browser, press the
button
![](Pictures/1000000100000024000000249CD8194D79602CFF.gif){width="0.953cm"
height="0.953cm"}.

In order to get a definition of the current term, press the button
![](Pictures/100000010000002400000024D17E1A1AE0443354.gif){width="0.953cm"
height="0.953cm"}. Please note that this button provides the definition
only for the article title, whereas the Ctrl-d combination (the
*bind_define* key) provides the definition for the current selected
term.

The program currently supports 2 interface languages -- Russian and
English. The interface language is determined automatically on the basis
of the system language.

In order to look up the copyright information, press
![](Pictures/100000010000002400000024C881EE946EB4A0C9.gif){width="0.953cm"
height="0.953cm"}.

To exit the program, close all its windows or press
![](Pictures/100000010000002400000024D4394F4E9756A45D.gif){width="0.953cm"
height="0.953cm"}.

-   -   -   ### 

        -   ### []{#anchor-5}Configuration file

You can adjust yourt settings in the configuration file **mclient.cfg**,
which must be located in C:\\users\\\<USER\>\\Application Data\\mclient
(Windows) or \$HOME/.config/mclient (Linux). If the configuration file
is missing then it will be created. Please note that key values can be
changed manually, however, everything else will be rewritten.

Adjustable parameters are set after the equal sign. They should not be
used inside quotation marks. Spaces inside parameters are allowed.

In order to ignore certain lines of the configuration file (comments,
examples, etc.), put \# at the beginning of a line. Such lines will not
be loaded.

The \[Boolean\] section allows only the following parameters: True or 1
(an option is enabled), False or 0 (an option is disabled).

When editing **mclient.cfg** manually, you should ensure that the text
editor does not set the BOM mark. The standard Windows editor
notepad.exe is not suitable for editing the configuration file. We
suggest using Akelpad or the like.

-   -   -   -   #### []{#anchor-6}Colors

You can select a desirable color by consulting an image "[color
chart.png](https://github.com/sklprogs/mclient/raw/master/docs/color%20chart.png)".
Set the necessary color name after the equal sign in the configuration
file. Spaces just before or after the equal sign are allowed. Colors of
prioritized and blocked dictionaries depend on a color of the column
where these dictionaries are indicated. The color of the prioritized
dictionary is more saturated and the color of the blocked dictionary is
less saturated than the color of the column where these dictionaries are
indicated.

-   -   -   -   #### []{#anchor-7}Fonts

In Windows: Open the directory C:\\WINDOWS\\Fonts and get the short name
of a desirable font. For example, Times New Roman is designated as
TIMES, Segoe UI -- as SEGOEUI. Set this short title (case-insensitive)
after the equal sign.

In Linux: Open a directory with fonts, for example, /usr/share/fonts,
then find the necessary font (for example,
truetype/ttf-dejavu/DejaVuSansMono.ttf) and extract the title (for
example, DejaVuSansMono). Set this title (also case-insensitive) after
the equal sign.

As a result, you must get, for example, the following:

font_comments_family=Mono

font_comments_size=3

-   -   -   -   #### []{#anchor-8}Buttons

Button images can be set individually. These images must be in a GIF
format, be present in the *resources *directory and their height and
width must be the same and equal to *default_button_size* (36 by
default). The majority of default images have been taken from the Oxygen
collection.

-   -   -   -   #### 

        -   ### []{#anchor-9}Issues 

If a dictionary entry is displayed incorrectly, send me an address (URL)
of this entry or indicate dictionaries being used. You can send me an
e-mail in the window "About".

-   -   -   ### []{#anchor-10}To developers 

The program is distributed on the terms of GPL v.3. The program
interface is translated (resources/locale) into Russian and English, but
you can add your own translations.
