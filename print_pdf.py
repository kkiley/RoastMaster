__author__ = 'Kor'

import win32api

fname = "D:/Development/RoastMaster/print_pdf.py"
win32api.ShellExecute(0, "print", fname, None, ".", 0)

# import tempfile
# import win32api
# import win32print
#
# # filename = tempfile.mktemp (".txt")
# filename = "D:/Development/RoastMaster/report.pdf"
#
# # open (filename, "w").write ("This is a test")
# win32api.ShellExecute (
#   0,
#   "printto",
#   filename,
#   '"%s"' % win32print.GetDefaultPrinter (),
#   ".",
#   0
# )
