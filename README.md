
# CALROV Yaz Kampı

Bu kamp, geçen sene eğitim verilemediğinden ve seneye görevlerinizin artacağından dolayı bir eğitim niteliğinde olacaktır. Lütfen ödevleri zamanında ve eksiksiz yetiştirelim. Çok önemli olmadığı sürece mazeret kabul edilmeyecektir. Hepinize kolay gelsin :)

# MAVLink Ödevi:

1. Udp ile mavlink bağlantısı kurulsun. (Local IP adresi)
2. mavproxy kurup localhosta bağlanın. (İnternette dokümantasyonu var takılırsanız oradan bakabilirsiniz)
3. İlk başta heartbeat mesajı bekleyip sonrasında mesaj alma yapılacak (wait heartbeat())
4. Mesaj alma işleminde "HEARTBEAT" türünde mesaj alınacak ve herhangi bir txt dosyasına sözlük şeklinde gelen mesaj yazdırılacak. (Bu sonsuz bir döngüde yapılacak)
5. Bir klavye modu yapılacak ve program başladığında otomatik olarak klavye modu da başlayacak. Aşağıda tuşlara atanacak fonksiyonlar verilmiştir:
	- W, A, S, D: ileri, sol, geri, sağ
	- Arrow key up, Arrow key down: yukarı, aşağı
	- Arrow key right, Arrow key left: sağ yaw ekseni, sol yaw ekseni
	- Q: Arm
	- E: Disarm
	- 1, 2, 3: (sırasıyla) Manual, Depth Hold, Stabilize Modları
	- Esc: Klavye modundan çıkış
	- Z: Servo motora komut gönderme (mesaj türü: MAV_CMD_DO_SET_SERVO)
	
6. Klavye modunda hareket komutları mavlink ile verilecek ve verildiğinde x, y, z ve yaw değerleri ekranda gösterilecek. Ekranda gösterirken print() fonksiyonu değil "logging" kütüphanesi kullanılacak. Arm, disarm ve mod komutları da yine mavlink ile verilecek ve yine logging kütüphanesi ile ekrana yazdırılacak. Klavye modu çalışırken arka planda aynı anda heartbeat mesajının txt dosyasına yazdırılması da çalışacak. Bu ikisini aynı anda çalıştırmak için threading ve multiprocessing kütüphaneleri kullanılabilir. Servo motora komut göndermede ise verilen mesaj türü kullanılarak mavlink ile komut gönderilecek. 
	
	
# OpenCv Ödevi:
1. GStreamer kullanarak önce udpsink ile terminalden kendi bilgisayarınızın kamerasını açın.

2. Sonrasında opencv kullanarak VideoCapture classına CAP_GSTREAMER ve udpsrc kullanarak yazdığınız pipelineı parametre olarak verin. (GStreamer kısımlarında takılırsanız bizim repolarda örnek var)
3. OpenCv DNN modülü ile repoda bulunan yolov4.weights modelini ve yolov4.cfg dosyasını kullanarak bir yapay zeka algılama sistemi oluşturun. 
4. Açtığınız kamera görüntülerini yapay zekaya verin ve canlı kamera görüntüsü üzerinde algılanan objeleri bounding box içinde gösterin. Aynı zamanda objenin sınıfı da box üzerinde yazsın. Sınıfı aynı zamanda logging kütüphanesi kullanarak terminalde yazdırın
5. Kamera görüntülerine aynı zamanda HSV renk filtresi de uygulansın.
	
# PID Algoritması Ödevi: 
1. Mavlink ödevindeki klavye kontrolüne ek olarak arka planda her zaman çalışan bir PID sistemi yazın. Roll, pitch, yaw ve z eksenleri için PID yapılacak.
	
	
# Önemli Not: 
Ödevleri atmak için öncelikle GitHub hesabınızda bu repounun bir fork'unu oluşturun ve değişikliklerinizi bu fork üzerinde yapın. Her ödevin son teslim tarihi geldiğinde bu repoya pull request atın. Her ödev için ayrı branch olacak o yüzden pull request atarken ve değişiklik yaparken hangi branch'te olduğunuza dikkat edin. 

# Ödev Teslimleri
- MAVLink Ödevi son teslim: 11 Ağustos 2024 Pazar
- OpenCv Ödevi son teslim: 18 Ağustos 2024 Pazar
- PID Algoritması Ödevi son teslim: 25 Ağustos 2024 Pazar
