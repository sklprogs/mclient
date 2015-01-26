# mclient
Multitran Online Client
Description and objectives
Multitran Online Client is a program that connects to the web-site multitran.ru and returns translation of words entered by a user. The objective of this program is to ensure more comfortable work with keyboard and also to provide some additional functionality.

System requirements
OS: Windows XP and later, Linux
Mac OS X was not tested, however, it is possible to launch the program in this OS.
An Internet connection is required.
Free space: 20 Mb (Windows build)
Free RAM: 20 Mb (Windows build)
Screen resolution: greater than 1024x758, at 1024x758 or less buttons may overlap.
The program can work on slow computers, however, on fast computers its speed will be limited only by the Internet connection.

Installation
You can start the build or the script (source code) itself. The build does not require installation, just copy it in some directory of your choice. To start the script itself, install Python 3 and all corresponding modules.
Additional software that may be required:
Windows (the build): Microsoft Visual C++ 2010 Redistributable Package (x86) (vcredist_x86.exe) (otherwise, you can receive a warning about missing msvcr100.dll)
Linux (the script): Python 3, an additional installation of html.parser and pyperclip, as well as other modules indicated in the import section, may be required.

Usage and functionality
You need the Internet to work with this program. If the program is unable to get an article from the web-site, the corresponding warning will be shown. You will need to check the Internet connection and multitran.ru accessibility. If the Internet is up and stable - do not worry, the Multitran will be accessible soon. It is often enough to press "OK" button just after receiving this warning message.
Both one or several words may be requsted. If the requested phrase is not found with the current declension or grammatical number, the Multitran will automatically select the necessary declension and number. Thus, if you enter "colorants", then the Multitran will show the article "colorant".
The program properly processes such symbols as á, ß, è, etc.
Titles of dictionaries from which terms are selected are highlighted in green. The current selected term is highlighted in blue. Comments, user names are highlighted in gray. The space between adjacents terms is highlighted in yellow. End dictionary links are processed as they were terms.
After the article is downloaded, the program title changes to the text of your request. If the program has just started, the title shows the program title and build date.
You can switch between adjacents terms using arrows. Press the left arrow to go to the nearest term from the left. Press the right arrow to go to the nearest term from the right. Press the up arrow to go to the first term of the preceding dictionary. Press the down arrow to go to the first term of the following dictionary.
To return the translation of the current selected term, press Enter (on the basic or expanded keyboard). To copy the current term, press Ctrl-Enter. The program window will minimize and show a window of a program where the copied term can be inserted.
In order to manually enter a term to translate, use the search field on the bottom of the window. After you have entered the necessary term, press Enter or the "Search" button.
In order to switch between the search field and selected terms, press F6 or click the left mouse button in the required area.
The language pair can be selected on the drop-down list. All language pairs currently present on the Multitran are supported. Please note that, if, for example, the English-Russian language pair is selected, you do not have to switch to the Russian-English pair (not counting the keyboard layout), because the Multitran can automatically determine the language of the term entered by you.
In order to switch between buttons using keyboard, press Tab and Shift-Tab. A button can be activated by the left mouse button click, Enter (on the basic or expanded keyboard) or Space.
You can enable/disable the history of requests by pressing the button "History". Requests are sorted from the newest to the oldest. You can repeat a request by clicking the required term once in the history field. You can scroll the history field using the mouse wheel.
Use the function "Clipboard" to translate terms from the clipboard. The language pair, as always, is determined by the value provided by the drop-down list. After you have pressed the button "Clipboard", the current window will be closed and a small window with the title 'Change clipboard...' will show up. Since that the program with 1 second delay will check whether the clipboard has changed. After the clipboard has changed, the program will load the new article correspondingly to the value stored in the clipboard. Please note: in a normal mode closing the article window will cause the program to exit. However, in the "Clipboard" mode after the article window has shown up, you will have to close it manually (pressing Alt-F4 or clicking "X"). The clipboard will be checked only when the current article window is closed. Please note that it is necessary to close the current article window in the "Clipboard" mode by pressing Alt-F4 or clicking "X", and not the "Exit" button, because pressing this button will cause the program to exit even in the "Clipboard" mode.
If the "Clipboard" mode is activated, then the text of the corresponding button becomes red. You can disable the clipboard scanning by pressing the corresponding button again. Please note that if the "Clipboard" mode is enabled, translating terms not by means of the clipboard but using the search, article or history fields will automatically disable this mode. This is the normal behavior and is reasoned by the logic of priotiries used in the program.
In order to open the current article in a default browser, press the button "In a browser".
The program currently supports 2 interface languages - Russian and English. In order to switch between them, press buttons 'In English' and 'На русском' correspondingly.
In order to look up the copyright information, press "About".
To exit the program, close the current window or press "Exit". Please note that in the "Clipboard" mode closing the current window will not cause the program to close. To exit the program in this mode press "Exit".

Known issues
In long articles the selection can get out of the screen view. Scroll the screen with the scrollbar or the mouse wheel.
Sometimes an HTML code fragment, particularly, a URL fragment, can be witnessed. If you notice that the program window lacks some text fragments or, vice versa, excessive fragments have been added, open the page in the browser and send me an address (URL) of this page. You can send me an e-mail in the window "About".
If you have discovered that the program has "crashed", firstly check the list of running applications by pressing Alt-Tab. Sometimes the window shows behind windows of other applications and not above them. If you have discovered that the program permanently crashes when loading a certain page, please e-mail me the URL of this page.
When switching to the English interface and enabling History, the program can firstly fail to get a correct list of requests. This bug is not obvious to the user, because the article is instantly reloaded.

Potential enhancements
Eliminate the revealed bugs.
Assign F1-F12 keys to the program buttons.
Save web-page on a hard drive.
Stop duplicating requests in the history field.

To developers
The program is distributed on the terms of GPL v.3. The program interface is translated into Russian (mes_ru.py) and English (mes_en.py), but you can add your own translations. Please note that these files store all messages used by me in various projects, not only in this one. Comments in the source code are mainly in Russian - sorry. If you decide to fork this program, you may want to contact me first in order not to duplicate efforts.
