#------------------------------------------------------------------------------
#
#   Yusuf DURSUN
#   Python üzerinde Parçacık Sürü Optimizasyonunun Kullanılarak Knapsack(Sırt Çantası) Probleminin Dinamik Bir Şekilde Çözülmesi
#
#------------------------------------------------------------------------------

# Proje bağımlılıklarının dahil edilmesi...
import matplotlib.pyplot as plt
import random
import math


# Global değişkenlerin tanımlanması [Önemli: Diğerler değişkenler ve algoritmanın çalıştırılması kısmı sayfanın en aşağısındadır]...
isimler = ['Televizyon', 'Kamera', 'Projektör', 'Walkman', 'Radyo', 'Cep Telefonu', 'Dizüstü Bilgisayar']
kar = [35, 85, 135, 10, 25, 2, 94]
kg = [2, 3, 9, 0.5, 2, 0.1, 4]
maxKg = 25


# Maksimize etmeye çalıştığımız fonksiyon...
def fncMax(x):
    t = fncTaneKar(x)
    return t + fncTaneKilogram(x, t)


def fncTaneKar(x):
    toplam = 0
    for i in range(len(x)):
        toplam += x[i] * kar[i]  # Tane * Kâr
    return toplam


def fncTaneKilogram(x, sifirlayanEleman):
    toplam = 0
    for i in range(len(x)):
        toplam += x[i] * kg[i]  # Tane * kg

    if toplam <= maxKg:
        if toplam <= sifirlayanEleman:
            return sifirlayanEleman - toplam
        else:
            return 0
    else:
        return -sifirlayanEleman

    """
        Eğer kilogram maxKg 'ı geçerse;
        fonksiyondan ceza puanı olarak 1.fonksiyon değerinin negatifini döndürerek,
        sonuç değerini sıfırlıyor bu sayede varolan değeri almaması sağlanıyor...
    """



# Parcacik sınıfımız...
class Parcacik:
    def __init__(self, baslangicDegerleri):
        self.pozisyon = []      # Parcacik pozisyonu
        self.hiz = []           # Parcacik hızı
        self.pBest = []         # Bireysel en iyi pozisyon
        self.pBestYaklasim = -1 # Bireysel en iyi yaklaşım
        self.yaklasim = -1      # Bireysel yaklaşım

        for i in range(parSayisi):
            self.hiz.append(random.uniform(-1, 1))
            self.pozisyon.append(baslangicDegerleri[i])

    # Fonksiyona uygunluğunu hesapla...
    def hesapla(self, fonksiyon):
        self.yaklasim = fonksiyon(self.pozisyon)

        # Şu anki pozisyonun, bireysel en iyi olup olmadığını kontrol et...
        if self.yaklasim > self.pBestYaklasim or self.pBestYaklasim == -1:
            self.pBest = self.pozisyon
            self.pBestYaklasim = self.yaklasim

    # Yeni parçacık hızını güncelle...
    def hiz_guncelle(self, grupMaxPozisyon):
        w = 0.99    # Parçacığın önceki hızını koruma isteğinin katsayısı.
        c1 = 1.99   # Kendi en iyisini koruma isteğinin katsayısı.
        c2 = 1.99   # Sürünün en iyi değerini alma isteğinin katsayısı.

        for i in range(parSayisi):
            r1 = random.random()
            r2 = random.random()

            bilissel_hiz = c1 * r1 * (self.pBest[i] - self.pozisyon[i])
            sosyal_hiz = c2 * r2 * (grupMaxPozisyon[i] - self.pozisyon[i])
            self.hiz[i] = w * self.hiz[i] + bilissel_hiz + sosyal_hiz

    # Yeni güncellenen parçacık hızına göre, yeni pozisyonları hesaplama...
    def pozisyon_guncelle(self, sinirDegerler):
        for i in range(parSayisi):
            maxZiplama = (sinirDegerler[i][1] - sinirDegerler[i][0])

            if self.hiz[i] < -maxZiplama:
                self.hiz[i] = -maxZiplama
            elif self.hiz[i] > maxZiplama:
                self.hiz[i] = maxZiplama

            self.pozisyon[i] = self.pozisyon[i] + self.hiz[i]

            if self.pozisyon[i] > sinirDegerler[i][1]:      # Eğer pozisyon üst sınır değerin üzerindeyse, üst sınır değerine çek
                self.pozisyon[i] = sinirDegerler[i][1]
            elif self.pozisyon[i] < sinirDegerler[i][0]:    # Eğer pozisyon alt sınır değerin altındaysa, alt sınır değerine çek
                self.pozisyon[i] = sinirDegerler[i][0]
            else:
                self.pozisyon[i] = round(self.pozisyon[i])

class PSO:
    adimKar, adimKg, grupMaxPozisyon, grupMaxYaklasim = [], [], [], -1

    def __init__(self, fonksiyon, baslangicDegerleri, sinirDegerler, parcacikSayisi, suruSayisi, maxIter, adimlarYazdirilsinMi = True): # fncMax, baslangicDegerleri, sinirDegerler, parcacikSayisi=7, maxIter=0.1
        global parSayisi

        parSayisi = len(baslangicDegerleri)
        self.grupMaxYaklasim = -1  # Grup için en iyi yaklaşım
        self.grupMaxPozisyon = []  # Grup için en iyi pozisyon

        # Sürümüze başlangıç değerlerini atayalım...
        suru = []
        for i in range(suruSayisi):
            suru.append(Parcacik(baslangicDegerleri))

        # Optimizasyon döngüsü başlangıcı...
        sayac = 0
        while sayac < maxIter:
            sayac += 1

            # Sürüdeki parçacıklarının fonksiyona uygunluğunun hesaplanması...
            for j in range(suruSayisi):
                suru[j].hesapla(fonksiyon)

                # Şimdiki parçacığın global en iyi olup olmadığının kontrolü ve gerekli güncellemelerin yapılması...
                if suru[j].yaklasim > self.grupMaxYaklasim or self.grupMaxYaklasim == -1:
                    self.grupMaxPozisyon = list(suru[j].pozisyon)
                    self.grupMaxYaklasim = float(suru[j].yaklasim)

            # Sürüdeki hız ve pozisyonların güncellenmesi...
            for j in range(suruSayisi):
                suru[j].hiz_guncelle(self.grupMaxPozisyon)
                suru[j].pozisyon_guncelle(sinirDegerler)

            toplamKar = 0
            toplamKg = 0
            for i in range(parcacikSayisi):
                toplamKar += self.grupMaxPozisyon[i] * kar[i]
                toplamKg += self.grupMaxPozisyon[i] * kg[i]
            self.adimKar.append(toplamKar)
            self.adimKg.append(toplamKg)

            if adimlarYazdirilsinMi:
                print(self.grupMaxPozisyon)

    # Sonuçların yazdırılması...
    def SonucuYazdir(self):
        print('\n\nSONUÇLAR:\n\n')
        toplamKar = 0
        toplamKg = 0
        for i in range(len(self.grupMaxPozisyon)):
            print(isimler[i], ': ', self.grupMaxPozisyon[i], ' tane', sep='')
            toplamKar += self.grupMaxPozisyon[i] * kar[i]
            toplamKg += self.grupMaxPozisyon[i] * kg[i]
        print('#' * 50, '\nElde Edilen Kâr: ', toplamKar, ',\nKilogram: ', toplamKg, sep='')

    # Sonuçların plot ile ekrana çizdirilmesi [Sonuç görüntüsünü bilgisayara kaydetmek istemiyorsak 'dosyaAdi' adlı parametre boş kalmalı!]...
    def SonucuCizdir(self, dosyaAdi = ''):
        plt.plot(self.adimKg, self.adimKar)
        plt.xlabel('Kilogram (kg)')
        plt.ylabel('Elde edilen kâr')
        plt.title('Elde Edilen Sonuçlara Göre Kâr - Kilogram Grafiği')
        plt.grid(True)

        if not(dosyaAdi == ''):         # 'dosyaAdi' adlı değişken boş değilse, o isimle dosyayı png formatında kaydet...
            dosyaAdi = dosyaAdi+".png"
            plt.savefig(dosyaAdi)

        plt.show()
        plt.close()


# Başlangıç ve sınır değerlerinin atanıp algoritmanın çalıştırılması...

# baslangicDegerleri = [0, 0, 0, 0, 0, 0, 0]  # Baslangiç degerleri [x1, x2...]
# sinirDegerler = [(0, 12), (0, 8), (0, 2), (0, 50), (0, 12), (0, 250), (0, 6)]  # Sınır değerler [(x1_min,x1_max),(x2_min,x2_max)...]

print('[esya_ismi: alt_sinir - ust_sinir]\n', sep='')
baslangicDegerleri = []
sinirDegerler = []
for i in range(len(isimler)):
    baslangicDegerleri.append(0)                                                    # Baslangiç degerleri [x1, x2...]
    sinirDegerler.append((baslangicDegerleri[i], math.floor(maxKg/kg[i])))          # Sınır değerler [(x1_min,x1_max),(x2_min,x2_max)...]
    print(isimler[i], ': ', sinirDegerler[i][0], ' - ', sinirDegerler[i][1], sep='')
print('\nolmak üzere toplam ', len(isimler), ' değişken var...\n\n', sep='')

pso = PSO(fncMax, baslangicDegerleri, sinirDegerler, parcacikSayisi=len(isimler), suruSayisi=100, maxIter=50, adimlarYazdirilsinMi=True)
pso.SonucuYazdir()
pso.SonucuCizdir(dosyaAdi='test')

# Algoritma sonu :)
