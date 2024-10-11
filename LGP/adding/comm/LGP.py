import os
import datetime

def ls():
    print("_" * ((62)))
    print("|" +  "\u001b[38;5;11mName\u001b[38;5;15m" + " " * 9 +
          "|" + "\u001b[38;5;11mDate edit\u001b[38;5;15m" + " " * 10 +
          "|" + "\u001b[38;5;11mType\u001b[38;5;15m" + " " * 6+
          "|" + "\u001b[38;5;11mSize (bytes)\u001b[38;5;15m" + " " * 3 + "|")
    print("_" * ((62)))
    for item in os.listdir():
        path = os.path.join(os.getcwd(), item)
        name = item
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
        type_ = "Folder" if os.path.isdir(path) else "File"
        size = os.path.getsize(path) if not os.path.isdir(path) else "-"
        print(f"|\u001b[38;5;11m{name:<13}\u001b[38;5;15m|\u001b[38;5;11m{mod_time:<15}\u001b[38;5;15m|\u001b[38;5;11m{type_:<10}\u001b[38;5;15m|\u001b[38;5;11m{size:<15}\u001b[38;5;15m|")
    print("_" * ((62)))
