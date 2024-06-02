import pygame

pygame.init()

LEBAR, TINGGI = 800, 500
WINDOW = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Ping-Pong")

FPS = 60

PUTIH = (255, 255, 255)
HITAM = (0, 0, 0)

LEBAR_PADDLE, TINGGI_PADDLE = 20, 100
JARI_BOLA = 1

FONT_SKOR = pygame.font.SysFont("Game Over", 40)
SKOR_MENANG = 1


class Paddle:
    WARNA_KIRI = (255, 0, 0)  # Merah
    WARNA_KANAN = (0, 0, 255)  # Biru
    VEL = 4

    def __init__(self, x, y, lebar, tinggi, sisi):
        self.x = self.x_asli = x
        self.y = self.y_asli = y
        self.lebar = lebar
        self.tinggi = tinggi
        self.sisi = sisi  # 'kiri' atau 'kanan'

    def gambar(self, win):
        if self.sisi == 'kiri':
            pygame.draw.rect(win, self.WARNA_KIRI, (self.x, self.y, self.lebar, self.tinggi))
        elif self.sisi == 'kanan':
            pygame.draw.rect(win, self.WARNA_KANAN, (self.x, self.y, self.lebar, self.tinggi))

    def gerak(self, atas=True):
        if atas:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.x_asli
        self.y = self.y_asli



class Bola:
    MAX_VEL = 5
    GAMBAR_BOLA = pygame.transform.scale(pygame.image.load("img/ball.png"), (25 * JARI_BOLA, 25 * JARI_BOLA))

    def __init__(self, x, y, jari):
        self.x = self.x_asli = x
        self.y = self.y_asli = y
        self.jari = jari
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def gambar(self, win):
        win.blit(self.GAMBAR_BOLA, (self.x - self.jari, self.y - self.jari))

    def gerak(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.x_asli
        self.y = self.y_asli
        self.y_vel = 0
        self.x_vel *= -1


def gambar(win, paddles, bola, skor_kiri, skor_kanan):
    # Load gambar meja tenis sebagai background
    background = pygame.image.load("img/back.jpeg")
    background = pygame.transform.scale(background, (LEBAR, TINGGI))
    win.blit(background, (0, 0))

    skor_kiri_teks = FONT_SKOR.render(f"{skor_kiri}", 1, HITAM)
    skor_kanan_teks = FONT_SKOR.render(f"{skor_kanan}", 1, HITAM)

    # Atur posisi tulisan "Home" di pojok kiri atas
    home_posisi = (10, 10)
    # Atur posisi skor "Home" di tengah
    skor_kiri_posisi = (LEBAR // 4 - skor_kiri_teks.get_width() // 2, 10)
    # Atur posisi tulisan "Away" di pojok kanan atas
    away_posisi = (LEBAR - skor_kanan_teks.get_width() - 70, 10)
    # Atur posisi skor "Away" di samping skor "Home"
    skor_kanan_posisi = (LEBAR * 3 / 4 - skor_kanan_teks.get_width() // 2, 10)

    win.blit(skor_kiri_teks, skor_kiri_posisi)
    win.blit(skor_kanan_teks, skor_kanan_posisi)

    font_home_away = pygame.font.SysFont("Game Over", 40)
    home_teks = font_home_away.render("Home", 1, HITAM)
    away_teks = font_home_away.render("Away", 1, HITAM)

    win.blit(home_teks, home_posisi)
    win.blit(away_teks, away_posisi)

    for paddle in paddles:
        paddle.gambar(win)

    bola.gambar(win)
    
    pygame.display.update()


def deteksi_tumbukan(bola, paddle_kiri, paddle_kanan):
    if bola.y + bola.jari >= TINGGI or bola.y - bola.jari <= 0:
        bola.y_vel *= -1

    if bola.x_vel < 0 and paddle_kiri.x <= bola.x <= paddle_kiri.x + paddle_kiri.lebar and \
            paddle_kiri.y <= bola.y <= paddle_kiri.y + paddle_kiri.tinggi:
        bola.x_vel *= -1

        tengah_y = paddle_kiri.y + paddle_kiri.tinggi / 2
        selisih_y = tengah_y - bola.y
        faktor_pengurangan = (paddle_kiri.tinggi / 2) / bola.MAX_VEL
        y_vel = selisih_y / faktor_pengurangan
        bola.y_vel = -1 * y_vel

    elif bola.x_vel > 0 and paddle_kanan.x <= bola.x <= paddle_kanan.x + paddle_kanan.lebar and \
            paddle_kanan.y <= bola.y <= paddle_kanan.y + paddle_kanan.tinggi:
        bola.x_vel *= -1

        tengah_y = paddle_kanan.y + paddle_kanan.tinggi / 2
        selisih_y = tengah_y - bola.y
        faktor_pengurangan = (paddle_kanan.tinggi / 2) / bola.MAX_VEL
        y_vel = selisih_y / faktor_pengurangan
        bola.y_vel = -1 * y_vel


def deteksi_gerakan_paddle(tombol, paddle_kiri, paddle_kanan):
    if tombol[pygame.K_w] and paddle_kiri.y - paddle_kiri.VEL >= 0:
        paddle_kiri.gerak(atas=True)
    if tombol[pygame.K_s] and paddle_kiri.y + paddle_kiri.VEL + paddle_kiri.tinggi <= TINGGI:
        paddle_kiri.gerak(atas=False)

    if tombol[pygame.K_UP] and paddle_kanan.y - paddle_kanan.VEL >= 0:
        paddle_kanan.gerak(atas=True)
    if tombol[pygame.K_DOWN] and paddle_kanan.y + paddle_kanan.VEL + paddle_kanan.tinggi <= TINGGI:
        paddle_kanan.gerak(atas=False)


def main():
    jalankan = True
    jam = pygame.time.Clock()

    paddle_kiri = Paddle(10, TINGGI // 2 - TINGGI_PADDLE // 2, LEBAR_PADDLE, TINGGI_PADDLE, 'kiri')
    paddle_kanan = Paddle(LEBAR - 10 - LEBAR_PADDLE, TINGGI // 2 - TINGGI_PADDLE // 2, LEBAR_PADDLE, TINGGI_PADDLE, 'kanan')
    bola = Bola(LEBAR // 2, TINGGI // 2, JARI_BOLA)

    skor_kiri = 0
    skor_kanan = 0

    while jalankan:
        jam.tick(FPS)
        gambar(WINDOW, [paddle_kiri, paddle_kanan], bola, skor_kiri, skor_kanan)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jalankan = False
                break

        tombol = pygame.key.get_pressed()
        deteksi_gerakan_paddle(tombol, paddle_kiri, paddle_kanan)

        bola.gerak()
        deteksi_tumbukan(bola, paddle_kiri, paddle_kanan)

        if bola.x < 0:
            skor_kanan += 1
            bola.reset()
        elif bola.x > LEBAR:
            skor_kiri += 1
            bola.reset()

        menang = False
        if skor_kiri >= SKOR_MENANG:
            menang = True
            teks_menang = "HOME WIN!"
            warna_menang = Paddle.WARNA_KIRI
        elif skor_kanan >= SKOR_MENANG:
            menang = True
            teks_menang = "AWAY WIN!"
            warna_menang = Paddle.WARNA_KANAN

        if menang:
            teks = FONT_SKOR.render(teks_menang, 1, warna_menang)
            teks_posisi = (LEBAR // 2 - teks.get_width() // 2, TINGGI // 4 - teks.get_height() // 2)
            WINDOW.blit(teks, teks_posisi)
            pygame.display.update()
            pygame.time.delay(3000)
            bola.reset()
            paddle_kiri.reset()
            paddle_kanan.reset()
            skor_kiri = 0
            skor_kanan = 0

    pygame.quit()


if __name__ == '__main__':
    main()
