from os import system, _exit, path, urandom

system("mode 80,18 & title Unique Kod Çevirici & powershell $H=get-host;$W=$H.ui.rawui;$B=$W.buffersize;$B.width=80;$B.height=9999;$W.buffersize=$B;")


def exit_():
    system("echo Herhangi bir tuşa basarak kapatabilirsiniz. . . . & pause >nul")
    _exit(0)


ERROR = "\x1b[38;5;255m[\x1b[31mx\x1b[38;5;255m]"
SUCCESS = "\x1b[38;5;255m[\x1b[32m✓\x1b[38;5;255m]"


def randint(a, b, seed=[0]):
    seed[0] = (1664525 * seed[0] + 1013904223) % 2 ** 32
    return int(a + (1 + b - a) * seed[0] / 2 ** 32)


if not path.exists("Tetikliyici.py"):
    print(f"{ERROR} Tetikliyici dosyası bulunamadı.\n")
    exit_()
with open("Tetikliyici.py", "a") as f:
    for _ in range(1, randint(4, 10)):
        f.write(f"\n#{urandom(16).hex()}")
print(f"{SUCCESS} Dosya Uniqe Koda Çevrildi.\n")
exit_()
