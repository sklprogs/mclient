#!/bin/sh

#mkdir resources
cp -vn /usr/local/bin/shared/resources/* /usr/local/bin/mclient/src/resources/* resources
cp -rvu /usr/local/bin/mclient/src/{locale,dics} .

cp -vu /usr/local/bin/shared/{gettext_windows.py,regexp.py,shared.py,sharedGUI.py} .
cp -vu /usr/local/bin/mclient/src/{cells.py,db.py,elems.py,kl_mod_lin.py,mclient.py,mclient.cfg,mkhtml.py,page.py,tags.py} .

# Linux-only
cp -vu /usr/local/bin/mclient/build/Linux/setup.py .
