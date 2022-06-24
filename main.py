import cv2
import numpy as np
import pytesseract
import imutils


#Bu fonksiyon plaka eşleşmesi olursa garaj kapısı elektroniğine açılma sinyali yolluyor
def garajKapisiniAc():
    pass



try:
    # Burada işlem yapılacak görüntü img değişkenine atılıyor.
    """
    Burada kameradan görüntü alınıyor ve cam değişkenine atanıyor. Daha sonra görüntü kare kare img değişkenine atanıyor ve işleme alınıyor.
Ancak uygulama kolaylığı açısından görüntüleri doğrudan proje dosyası içindeki arabalar dosyasından aldım. Dosya yolunu kendinize göre ayarlamanız gerekli.
    cam = cv2.VideoCapture(1)
    while True:
        ret, img = cam.read()
    """
    img = cv2.imread("C:\\Users\Arslanlar\\PycharmProjects\\Plaka_Tanima\\arabalar\\golf.jpg")
    img = cv2.resize(img, (640, 400))


    #Burada aracın bulunduğu görüntü sırasıyla griye dönüştürülüyor, gereksiz detaylar atılıyor ve kenarlar belirleniyor
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 3, 250, 250)
    edged = cv2.Canny(filtered, 30, 200)

    #burada önce hat çizgileri daha sonra plakanın konumu bulunuyor
    contours = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contours)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screen = None

    for c in cnts:
        epsilon = 0.018 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c,epsilon, True)
        if len(approx) == 4:
            screen = approx
            break

    if screen is None:
        print("Plaka Algılanmadı")

    else:
        #burada plakanın konumu dışındaki alanlar maskeleniyor görüntüde sadece plaka kalıyor
        mask = np.zeros(gray.shape, np.uint8)
        new_img = cv2.drawContours(mask, [screen], 0, (255, 255, 255), -1)
        new_img = cv2.bitwise_and(img, img, mask =mask)

        (x,y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        cropped = gray[topx:bottomx+1, topy:bottomy+1]

        #Plakadaki yazıları okumak için Tesseract-OCR kullandım. Kodun düzgün çalışması için Tessractı kurmanız ve bilgisayarızdaki yolu aşağıya vemeniz gerekli
        img_to_str = pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        plaka = pytesseract.image_to_string(cropped, lang="eng", config='-c tessedit_char_whitelist=0123456789QWERTYUIOPASDFGHJKLZXCVBNM --psm 8 --oem 3')


        #Plakadaki okunan boşluk ya da farklı karakterleri tekrar aşağıda temizledim. Sadece plakannın kendisi kaldı
        alfabe = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C", "V", "B", "N", "M", "1","2","3","4","5","6","7","8","9","0"]
        plaka_kontrol = ""
        for c in plaka:
            if c in alfabe:
                plaka_kontrol = plaka_kontrol+c

        print("Girişteki aracın plakası:", plaka_kontrol)

        #Burada plakaların kayıtlı olduğu txt dosyasına ulaşıyoruz. Okunan plaka kayıtlı mı onun kontrolu yapılıyor. Dosya yolunu kendi bilgisayarınıza göre ayarlayın
        kayitli_plakalar = open("C:\\Users\\Arslanlar\\Desktop\\Plakalar.txt", "r")
        for p in kayitli_plakalar:
            pk = plaka_kontrol + "\n"
            if p == pk:
                print("Kayitli arac. Garaj kapisi aciliyor...")
                garajKapisiniAc()
                break

        else:
            print("Araç plakası kayıtlı değil")


except cv2.error:
    print("Görüntü aktarma sorunu")

except FileNotFoundError:
    print("Kayıt Dosyası bulunamadı")

except pytesseract.pytesseract.TesseractNotFoundError:
    print("Tesseract yazılımı bulunamadı")
