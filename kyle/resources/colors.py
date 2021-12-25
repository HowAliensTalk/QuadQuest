

class Colors:

    Black = "\u001b[30m"
    Red = "\u001b[31m"
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    Cyan = "\u001b[36m"
    White = "\u001b[37m"
    Reset = "\u001b[0m"


    Bold = "\u001b[1m"
    Underline = "\u001b[4m"
    Reversed = "\u001b[7m"


    def reverse_color_msg(msg, color, end="\n"):
        return Colors.Reversed + msg + Colors.Reset + color + end

    def color_msg(msg, color, end="\n"):
        return color + msg + Colors.Reset + color + end
