import sys,traceback
from datetime import datetime

fError = open("except_error.log",  'a')
def UserExceptHook(tp, val, tb):
    traceList = traceback.format_tb(tb)
    html = repr(tp) + "\n"
    html += (repr(val) + "\n")
    for line in traceList:
        html += (line + "\n")
    print(html, file=sys.stderr)
    print(datetime.now(), file=fError)
    print(html, file=fError)
    fError.close()

def main():
    sFirst = input("First number:")
    sSecond = input("Second number:")
    try:
        fResult = int(sFirst) / int(sSecond)
    except Exception:
        print("发现异常，但我不处理，抛出去.")
        raise
    else:
        print( sFirst, "/", sSecond, "=", fResult)

sys.excepthook = UserExceptHook
main()
fError.close()