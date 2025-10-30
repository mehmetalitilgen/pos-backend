FastAPI
-Web Apı geliştirmeyi kolaylaştıran modern bir Python framework'üdür
-Asenkron (async) yapıyı destekleyerek hızlı yanıt süreleri sağlar.
-Veri doğrulama ve dokümantasyonu otomatikleştirir.

SQLAlchemy:
-Python'da veritabanı işlemlerini kolaylaştıran bir ORM kütüphanesidir.
-SQL sorgularını Python nesneleri üzerinden yazmanı sağlar.

Alembic
-SQLAlchemy ile birlikte kullanılan veritabanı şema versiyonlama aracıdır.
-Veritabanı tablolarında yapılan değişiklikleri (ekleme, silme, güncelleme) migration dosyalarıyla takip eder.
-Yani veritabanı evrimi değişimi bundan sorulur

Pydantic
-Veri doğrulama ve veri modelleme için kullanılan güçlü bir kütüphanedir.
-FastAPI, gelen istek verilerini Pydantic modelleriyle kontrol eder.

Redis
-Bellek tabanlı bir anahtar-değer veritabanıdır.
-Veriye çok hızlı erişim sağladığı için önbellekleme (cache), oturum yönetimi ve kuyruklama sistemlerinde kullanılır.

### 🐳 Docker Ekosistemi Özeti

Docker, uygulamaları ve bu uygulamaların ihtiyaç duyduğu bağımlılıkları kapsülleyerek container (konteyner) adı verilen izole ortamlarda çalıştırmayı sağlar.
Bu sayede yazılım, geliştirici bilgisayarında nasıl çalışıyorsa sunucuda da aynı şekilde çalışır — “bende çalışıyor ama sende çalışmıyor” sorunu ortadan kalkar.

Docker Compose ise birden fazla container’ı (örneğin API, veritabanı, önbellek) tek bir dosyada tanımlayıp birlikte çalıştırmaya yarar.
Yani Compose, bir uygulamanın tüm servislerini tek komutla yönetme imkânı sunar.
“Docker Compose kullanarak çok bileşenli uygulamaları (örneğin FastAPI + PostgreSQL + Redis) tek yapılandırma dosyasında tanımlayıp kolayca başlatma avantajı sağlar çünkü tüm servisler aynı ağda, senkronize şekilde çalışır.”

## Neden Backend Projelerinde Kullanılır?

Her bileşeni (API, veritabanı, cache) izole eder, versiyon ve ortam farklarını ortadan kaldırır.

Geliştirme, test ve üretim ortamları arasında tutarlılık (consistency) sağlar.

CI/CD süreçlerinde otomasyon ve taşınabilirlik sunar.

## Neden PostgreSQL ve Redis ile Kullanılır?

PostgreSQL: Docker imajı sayesinde veritabanı kurulumu saniyeler içinde yapılır, manuel kurulum gerekmez.

Redis: Hafif ve hızlıdır; Docker ortamında kolayca başlatılarak cache veya queue sistemi olarak kullanılabilir.

Her ikisi de Compose üzerinden otomatik başlatılıp durdurulabilir, böylece geliştirici hiçbir manuel ayar yapmadan backend + veritabanı + cache sistemini aynı anda çalıştırabilir.