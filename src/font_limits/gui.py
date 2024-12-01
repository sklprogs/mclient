#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtGui import QFont, QFontMetrics


class FontLimits:
    
    def get_font(self, family, size, weight, italic):
        return QFont(family, pointSize = size, weight = weight, italic = italic)
    
    def get_space(self, text, qfont):
        qrect = QFontMetrics(qfont).boundingRect(text)
        return qrect.width() * qrect.height()
