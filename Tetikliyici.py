from os import system, _exit

system("mode 80,18 & title Renk Tetikliyicisi & powershell $H=get-host;$W=$H.ui.rawui;$B=$W.buffersize;$B.width=80;$B.height=9999;$W.buffersize=$B;")

from time import sleep, perf_counter
from ctypes import WinDLL

print('''\033[31mRenk Tetikliyicisi\033[37m \033[32mSeuzfaar \033[37mtarafından yapıldı.
''')
print('''\033[39m[███████|||] 75% Yükleniyor...\n\n''')


def exit_():
    system("echo Herhangi bir tuşa basarak kapatabilirsiniz. . . . & pause >nul")
    _exit(0)


ERROR = "\x1b[38;5;255m[\x1b[31mx\x1b[38;5;255m]"
SUCCESS = "\x1b[38;5;255m[\x1b[32m✓\x1b[38;5;255m]"
INFO = "\x1b[38;5;255m[\x1b[31m!\x1b[38;5;255m]"


try:
    from PIL.Image import frombytes
    from mss import mss
    from keyboard import is_pressed, add_hotkey, block_key, unblock_key
except ModuleNotFoundError:
    print(f"{INFO} Modül dosyaları bekleniyor lütfen bekleyiniz.\n[|||||||||] 0% Beklemede")
    o = system("pip3 install keyboard mss pillow --quiet --no-warn-script-location --disable-pip-version-check")


try:
    TRIGGER, HIGHLIGHT = [line.strip() for line in open("config.txt")]
    print(f"{SUCCESS} Tuş: {TRIGGER}\n{SUCCESS} Düşman Renk Tetikliyicisi: {HIGHLIGHT}\n")
except (FileNotFoundError, ValueError):
    print(f"{ERROR} Ayarlarını bulamadık. Yeniden oluşturuluyor.\n")
    HIGHLIGHT = input(f"{INFO} Düşman rengini seç:\n\n[\x1b[35m1\x1b[38;5;255m] Kırmızı \n[\x1b[35m2\x1b[38;5;255m] Mor\n[\x1b[35m3\x1b[38;5;255m] Sarı\n\n> ")
    if HIGHLIGHT not in ["1", "2", "3"]:
        print(f"{ERROR} 1,2 ve 3 arasından rakam gir.\n")
        exit_()
    if HIGHLIGHT == "1":
        HIGHLIGHT = "kırmızı"
    elif HIGHLIGHT == "2":
        HIGHLIGHT = "mor"
    elif HIGHLIGHT == "3":
        HIGHLIGHT = "sarı"
    print(f"\n{SUCCESS} Düşman rengi tanımlandı.\n{INFO} Config.txt dosyasından şimdi bir tuş atamalısın.\n")
    with open("config.txt", "w") as f:
        f.write(f"Bu ilk satırı kısayol tuşunuzla değiştirin. Örneğin: c veya ` veya hatta ctrl + alt + z\n{HIGHLIGHT}")
    exit_()


if HIGHLIGHT == "kırmızı":
    R, G, B = (152, 20, 37)
elif HIGHLIGHT == "mor":
    R, G, B = (250, 100, 250)
elif HIGHLIGHT == "sarı":
    R, G, B = (252, 252, 84)                         

MODE = input(f"{INFO} \x1b[35mOynamak istediğiniz türü seçiniz.\n\n\033[37m[\x1b[35m1\x1b[38;5;255m] Basılı Tut\n[\x1b[35m2\x1b[38;5;255m] Aç/Kapat\n\n> ")
if MODE not in ["1", "2"]:
    print(f"{ERROR} 1 ve 2 arasından rakam gir.\n")
    exit_()


user32, kernel32, shcore = WinDLL("user32", use_last_error=True), WinDLL("kernel32", use_last_error=True), WinDLL("shcore", use_last_error=True)

shcore.SetProcessDpiAwareness(2)
WIDTH, HEIGHT = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

TOLERANCE, ZONE = 35, 6
GRAB_ZONE = (int(WIDTH / 2 - ZONE), int(HEIGHT / 2 - ZONE), int(WIDTH / 2 + ZONE), int(HEIGHT / 2 + ZONE))


class PopOff:
    def __init__(self):
        self.active = False
        kernel32.Beep(440, 75), kernel32.Beep(200, 100)
        print(f"{SUCCESS} Girdiler kaydedildi.")

    def switch(self):
        self.active = not self.active
        kernel32.Beep(440, 75), kernel32.Beep(700, 100) if self.active else kernel32.Beep(440, 75), kernel32.Beep(200, 100)

    def search(self):
        start_time = perf_counter()
        with mss() as sct:
            img = sct.grab(GRAB_ZONE)
        pmap = frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        for x in range(0,ZONE):
            for y in range(0,ZONE):
                r, g, b = pmap.getpixel((x, y))
                if R - TOLERANCE < r < R + TOLERANCE and G - TOLERANCE < g < G + TOLERANCE and B - TOLERANCE < b < B + TOLERANCE:
                    print(f"\x1b[2A{INFO} Reaksiyon Süresi: {int((perf_counter() - start_time) * 1000)}ms")
                    blocked, held = [], []  
                    user32.mouse_event(2, 0, 0, 0, 0)
                    sleep(0.005)
                    user32.mouse_event(4, 0, 0, 0, 0)
                    for b in blocked:
                        unblock_key(b)
                    for h in held:
                        user32.keybd_event(h, 0, 2, 0)
                    break

    def hold(self):
        while 1:
            if is_pressed(TRIGGER):
                while is_pressed(TRIGGER):
                    self.search()
            else:
                sleep(0.007)

    def toggle(self):
        add_hotkey(TRIGGER, self.switch)
        while 1:
            self.search() if self.active else sleep(0.007)


o = system("cls")
if MODE == "1":
    PopOff().hold()
elif MODE == "2":
    PopOff().toggle()

##=======================Unique Kod Çeviricisi=======================##
#6cc68915cfa8e9e5138632eaa9cc98ef
#7b4e0cb28fb9101a73f0230d74f7efb2
#85560b0e0c344c6caf24c11a28383f9d
#626310e9a653c52272b0e1c2f9c75864
#c1d61f9ac7ae7b8e3c9fc7ffc8492e41
#c932de9ef87c5a8cd5f61ed7688bfaf3
#70b1e24698f783365066542d82f597e3
#7f89d85be9c0aa45bb138e03981371dd
#c59e5c27013ea71075da1f5b9af7b17f
#baaa55671ed0353f4d1d9f96ca1bebc7
#e977b0b88345b92fc62faf55529bab9c
#e42bc8298203989e44174a2a34ce5742
#dc4fb0e910fd8f477be9594d36be8fb7
#eaba718e7f09ad4bd4337800922e4b02
#394239abaf4c61a198db52893a9856eb
#69bcc6c26d278828b688879411e2463e
#0ef07f3e88a17390ca8e7116168cf177
#a677fd48c2b4377e38d59def74897e51
#92e433dcec285367ce855dd326c4d5f5
#e3820a5908ae483ef8a3587a1e36b2f3
#568d0d024e03d5ca532a16da2182cd8c
#0c41825ce37e7f5930471f30df1686d8
#8968b954b1b0d69474c1ebfd49bb3bae
#ec3de3b6bf07559c0b9ebda3936a872b
#e07648466fc963da9e81193d114fdcc4
#d584d5f02ca17e51d3eef523fc25588a
#789534e7eb30555f854e25022a21c6fb
#45100a4129931838d2106246d176b046
#cbb75c0375b6de4d27c42b59e8da59b6
#36d0462f12bd7d46789f1a93835dc554
#dbdfd59bfafc068e46a50bc3d5a72154
#734be1d1ff1b3bec8f60ad2e36b5255a
#fc36e6893c5d4d6e8102da748c2faa70
#cf86917dbf93dbb9407080811aed4dac
#23d9c583d79e92abcd462f8e3ec73b27
#2dceec20eadbee6a5c1e41157ef59b43
#ed002eff92adc24024cdb167f0ca5604
#d85bdd9da8620b30511d04c88a330c8b
#9d113f5b18811968b616f7867f41f2c5
#5cd68bc0ec4c59ca76ef27a493b45686
#b3e8e28689fef6901133700b693c63f3
#efcab892ff86b4c4c6b6567bd6d056ea
#3f0a7981832e0d95dac3e7df0abebfcf
#c4646499064997fe80b34d3a229e596e
#67dc3ff9e3920992529034e3a34fc36a
#111b4bb4a45eafd7fe389f77c14386b5
#6bc8b1cfb54c895469b69ad9605e7343
#991d1195944c64dd553b6d88860c1a7a
#8a81cc0685e04b02719bb55a4f149312
#71f9a8b06e01e497637289989c1181fc
#33c655d54d26f86f4344c2aace4d2766
#3b0bc1281d77b1701d7784db1b6363b0
#3051d6a6b71eb608f20eb14b0b6402ff
#589718e988ca7db84ab0224e01dede1d
#5c2ff62f211aef2e204752f27e65eb94
#3cbada1aa06f1fac4a8577b03c2d964b
#675852b393cec624ab58f2a5338b3533
#3f27b17215101c4fb95b918ab8ce77ea
#d26da0130b5378050cd6fa091eb47528
#f5436ea9f909247985a59ce8d7d075ae
#3aa4ff594aa2fd8da4b561019c99b1fe
#23780a7d12d6cf6d7355bb121a8fd12b
#6027d9640091fabbc0bf4622018f36b4
#b13c8fefa929e1553b3370d6d422f179
#a4c0ec4327d447a01a0faff2c5330486
#09d63891335d470a4dc36dfcc273a44a
#104e7205c8056f497ca93ad21247c3c6
#0267a73db0d7d51e8fc20b15a69a7961
#06799b09f5e88ada5167a291f9df23d8
#ed3fbb1a94f23ae4faa76445bddc5122
#f8d9832ddff959120aabbf9139a92279
#2e401acbdb5e34b13bd63e6e157dd90f
#0dbf6583cb038af3dd6fa90c95afeccf
#683414ccea57f656a071e0a131d2339e
#2968316061c05580512ea6cf4ee1b87a
#d37dc1e332c27112c1729e9d31635a0b
#237e1754ec9d456d4372178d6f093a6e
#d555e9a364f24e19a041a712168ff837
#d20477d90c5c5abde726431d2d3eec63
#b28787e4ecc2c4b52cdab5d04f12b503
#27d72813c44351a2b2781d41eefe756c
#b84ec4eb22d5399e6731339fcda7114b
#e29d1301cc63534c3ef49b08d742d72c
#598d0ac6a33c6bdd5a11d46ecfb6213a
#4463e80fdb3789e71ac7c61a1928b65f
#6c58d2a1cd3694220cc3037f30fc25fe
#fafcea5a9b3976fb438f7fbd548e9d2a
#5a821f98affde7cf1b896300b35bc65e
#6a717312a2d08f2473769fa4d72fe350
#55a904d81591c1b00c15f2fadb0265b5
#99ae84b795becb6756b82f3d8984ba21
#d866d9a996c6d6e4fa8752115427bab4
#91653f64cc55499b9a69e445badc1a84
#791f4bf1553b2e7a6fdcb146a7ed0bb1
#819365a60d4576b45d80955903446442
#5306c4b180fb56290889aa0a04cbbd24
#0a70b885622ffc33c372ec7fdb5c4c52
#9d1eda68ff3fc178fedd2da497a2214d
#b76130152a8db149f7ab8a4ed89c206c
#d16fbba10647d4935e0689047dd5d2f4
#5c26ba60abc75a6aa6f91627bcf65a20
#21c458518d3bf68401b86763df868599
#9840166d1450be415b2f5e6a54403e8b
#d14b79cbbe830eb61f16dff2657d46a9
#c0d17739856849c635b5010827276cca
#56b70797e7c296afed8bb580752d4ee4
#db0cef93478bc21e1824e923a7489239
#cc8d1681823ee1fee5c12859d71ff975
#db7d4d495b99628836d013939ba49b91
#281627ef22d3c916c1887814153780df
#21f8aa796034e4954c3086d23e85ddde
#22e83ebff03d085a43523394ebefeebb
#759d6b46e44c0d69e84bbcc83ea483df
#11e90d80e6018af85ca91333f80e025b
#3a50e15415b82c5971031144bd967c32
#72ee4afe0d4cb3ce99605a8d2e38a581
#c2c41987bf99f91d7ac474eb5fee4d4d
#f1dfcc7b3f9f9456b34ad76d131191c1
#177741c44ae014bcb963b654cefbf157
#c7537ca497e98739040880de5994eead
#822a11a99c564f14997a3734c0a38aa4
#e7cbf15cb34a20d0e1579703ca69d4f9
#81919067b9357ea2eec5a5a6e804e497
#9b56a873267e8c43b82290786efa2e98
#c2e52281b7251a01d265dc3e42d2b643
#bf8317df00baf969a4c4b256b75d23e2
#251012733efd7b968b6f71f86d19e22a
#f5bbbd36b6e9efeefba52f7b69606ea8
#f539ba49987f25a0bfdd5db8b32cf2a3
#39f2233bc6362073df85ebc7c9d9286b
#72b5f2bc1227416f0a215ac337aad071
#b6c6251a21ddf69a1cc32dd69a972406
#b45b1065ffe608ccca39176b94913a8a
#4784c3f325c775c80682126cc3e88e8e
#ece68a60e49e49eceefabd1336cc3852
#fa35bf42cf037b85d098580b9c9702f7
#003fdc623c51d45229c057e10ea6c630
#5a7bbbd036ae84a66461070d193c6549
#237c4b1b46fd75fdac544a1edf0b6d5f
#99487d536ed5d48b5c73643e99b81f05
#0d9da3776afb2e7892c47647df786038
#43e405c75e2612b6560b871e398cacda
#752647a969fdbdde8be900b5bd661409
#33b71837cc31894fc92195015176b7b5
#0272ab3f456b2c5638586bfc574875dc
#554b67aa317728350169696f80d7127d
#ca788920f92b64206b27b6f90e796979
#7b6ec56a43b88d9437eb4cf5906ef5bd
#7a316d688ee8e53819448ab71796c7f3
#f818749eec6851ff90ff78c2cf4bce15
#b5a62e3f290fcc3b4c976f7eceb290a8
#bffa6678a582618dd4f3006edb9b07dd
#357578f7136a9718c018e4ff12356451
#5b4d5e938dbf1b1fbf47dd18f2ca5e61
#e95c1a655b418432e0b5d27c071fa2ce
#acd645589813c29c0d761ffed674f687
#35e5521d30be00e4006818217ca60b8b
#2746040e0cacd1f547dc33e9a6a175de
#63aecb449d7120fc0aeb817f16595fe2
#f4ff128885f9f378dac280176b094cae
#82858d2e6b545cc8de219054b2b1fed3
#f952d0a1e4a59c2a898ed3977feaab9c
#76497676003dec06b1b3c7011ce65a73
#b1f75395fec26439054ec51fa61e80e3
#871ced1b90984e631d0996e400b6a035
#552fba30a4687e590e0344fb24c30d43
#d3ea38fc131b2d42761ec0488df7b867
#f07a1c14f4a7881e40880a340d070f44
#5b346a8364149922cd01c07ff4abf35b
#7315820f27cf9b0d5e30ebe3131bd62b
#b865b7403756a499b6bf013f5922315c
#9d87d078f28f3e12ca7ea19d41330602
#df3d0f51c257850d384b749f17529b80
#7e49e065e84fe9573b23b4a72c854221
#064f975a5c17d0bad9ca1698448195dd
#a1fdd7772cc93607bdfdedea4fb12511
#c27fb2e831b6557b27aa8889feae6062
#fcd21794478f1dfa2340705bd44af2a2
#b1d24d144cbd782d1c8ddf2eaff0c3a5
#ae853098badd6ac3b8ef16664e2601e0
#9418d8ced559a35aee8ecac16c8e76e6
#3c7178ef62de19594d505c8d14c0d47e
#861b6db7dbeaebae00dc10dff1db3dd3
#52d49ea51263f29ba34b1e9cf4782441
#dff92b6778407137e53a6f548f06286e
#446413190aadc132ea477a1d67ac1347
#5a2ed98d67f21016bd3fc65c8a81de27
#7d8e2e434ea23065a403e045b629e75d
#b51c3cd4cd28f86629b7b801c3ec47d3
#e68806b9f85eebe6dfed866d4faa7b40
#0f5cf3fb077aecae34d287b5e0a22796
#b1ae68728c31fc59000f5a0584f7faef