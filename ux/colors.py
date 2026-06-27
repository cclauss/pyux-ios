from .uikit import UIColor
from ctypes import c_double, byref

def uicolor(color):
    if isinstance(color, str):
        if color[:1] == '#':
            if len(color) == 7:
                R = float(int(color[1:3], 16)/255.0)
                G = float(int(color[3:5], 16)/255.0)
                B = float(int(color[5:7], 16)/255.0)
                return UIColor.colorWithRed(R, green=G, blue=B, alpha=1.0)
            else:
                return None
        else:
            color = color.lower()
            if color == 'clear':
                return UIColor.clearColor
            if color == 'black':
                return UIColor.blackColor
            elif color == 'blue':
                return UIColor.blueColor
            elif color == 'brown':
                return UIColor.brownColor
            elif color == 'cyan':
                return UIColor.cyanColor
            elif color == 'darkgray':
                return UIColor.darkGrayColor
            elif color == 'gray':
                return UIColor.grayColor
            elif color == 'green':
                return UIColor.greenColor
            elif color == 'lightgray':
                return UIColor.lightGrayColor
            elif color == 'magenta':
                return UIColor.magentaColor
            elif color == 'orange':
                return UIColor.orangeColor
            elif color == 'purple':
                return UIColor.purpleColor
            elif color == 'red':
                return UIColor.redColor
            elif color == 'white':
                return UIColor.whiteColor
            elif color == 'yellow':
                return UIColor.yellowColor
            elif color == 'systemblue':
                try:
                    return UIColor.systemBlueColor()
                except Exception:
                    return UIColor.systemBlueColor
            elif color == 'systembrown':
                try:
                    return UIColor.systemBrownColor()
                except Exception:
                    return UIColor.systemBrownColor
            elif color == 'systemcyan':
                try:
                    return UIColor.systemCyanColor()
                except Exception:
                    return UIColor.systemCyanColor
            elif color == 'systemgray':
                try:
                    return UIColor.systemGrayColor()
                except Exception:
                    return UIColor.systemGrayColor
            elif color == 'systemgray2':
                try:
                    return UIColor.systemGray2Color()
                except Exception:
                    return UIColor.systemGray2Color
            elif color == 'systemgray3':
                try:
                    return UIColor.systemGray3Color()
                except Exception:
                    return UIColor.systemGray3Color
            elif color == 'systemgray4':
                try:
                    return UIColor.systemGray4Color()
                except Exception:
                    return UIColor.systemGray4Color
            elif color == 'systemgray5':
                try:
                    return UIColor.systemGray5Color()
                except Exception:
                    return UIColor.systemGray5Color
            elif color == 'systemgray6':
                try:
                    return UIColor.systemGray6Color()
                except Exception:
                    return UIColor.systemGray6Color
            elif color == 'systemgreen':
                try:
                    return UIColor.systemGreenColor()
                except Exception:
                    return UIColor.systemGreenColor
            elif color == 'systemindigo':
                try:
                    return UIColor.systemIndigoColor()
                except Exception:
                    return UIColor.systemIndigoColor
            elif color == 'systemmint':
                try:
                    return UIColor.systemMintColor()
                except Exception:
                    return UIColor.systemMintColor
            elif color == 'systemorange':
                try:
                    return UIColor.systemOrangeColor()
                except Exception:
                    return UIColor.systemOrangeColor
            elif color == 'systempink':
                try:
                    return UIColor.systemPinkColor()
                except Exception:
                    return UIColor.systemPinkColor
            elif color == 'systempurple':
                try:
                    return UIColor.systemPurpleColor()
                except Exception:
                    return UIColor.systemPurpleColor
            elif color == 'systemred':
                try:
                    return UIColor.systemRedColor()
                except Exception:
                    return UIColor.systemRedColor
            elif color == 'systemteal':
                try:
                    return UIColor.systemTealColor()
                except Exception:
                    return UIColor.systemTealColor
            elif color == 'systemyellow':
                try:
                    return UIColor.systemYellowColor()
                except Exception:
                    return UIColor.systemYellowColor

    elif isinstance(color, tuple):
        return UIColor.colorWithRed(color[0], green=color[1], blue=color[2], alpha=color[3])
        if color == (0.0392156862745098, 0.5176470588235295, 1.0, 1.0):
            return UIColor.colorWithRed(color[0], green=color[1], blue=color[2], alpha=color[3])

        return None
    return None

def uicolor_rgba(color):
    r, g, b, a = c_double(), c_double(), c_double(), c_double()
    if UIColor(color).getRed(byref(r), green=byref(g),
        blue=byref(b), alpha=byref(a)):
        return (r.value, g.value, b.value, a.value)
    else:
        return None
