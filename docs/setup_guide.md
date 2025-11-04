FastAPI
- Web Apı geliştirmeyi kolaylaştıran modern bir Python framework'üdür
- Asenkron (async) yapıyı destekleyerek hızlı yanıt süreleri sağlar.
- Veri doğrulama ve dokümantasyonu otomatikleştirir.

SQLAlchemy:
- Python'da veritabanı işlemlerini kolaylaştıran bir ORM kütüphanesidir.
- SQL sorgularını Python nesneleri üzerinden yazmanı sağlar.

Alembic
- SQLAlchemy ile birlikte kullanılan veritabanı şema versiyonlama aracıdır.
- Veritabanı tablolarında yapılan değişiklikleri (ekleme, silme, güncelleme) migration dosyalarıyla takip eder.
- Yani veritabanı evrimi değişimi bundan sorulur

Pydantic
- Veri doğrulama ve veri modelleme için kullanılan güçlü bir kütüphanedir.
- FastAPI, gelen istek verilerini Pydantic modelleriyle kontrol eder.

Redis
- Bellek tabanlı bir anahtar-değer veritabanıdır.
- Veriye çok hızlı erişim sağladığı için önbellekleme (cache), oturum yönetimi ve kuyruklama sistemlerinde kullanılır.

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

## FastAPI Uygulama Başlatma 
FastAPI uygulamaları genellikle bir main.py dosyası üzerinden başlatılır.

# main.py
- Uygulamanın ana giriş noktasıdır.
- FastAPI uygulama nesnesi (app) burda tanımlanır.
- Projenin kalbidir.

# app = FastAPI() Ne Yapar ?
- Bir FastAPI uygulama örneği(instance) oluşturur.
- Bu nesne, tüm API yollarını (routes), middleware’leri, event’leri ve yapılandırmaları yönetir.
- Yani uygulamanın çekirdeği budur — tüm HTTP istekleri bu app nesnesi üzerinden karşılanır.
- Kısaca app bir ASGI(Asynchronous Server Gateway Interface) uygulamasıdır.

# @app.get() ve Diğer Decoratorlar Nasıl Çalışır?
- FastAPI'de @app.get(), @app.post(), @app.put() gibi decorator'lar, belirli URL'lere gelen istekleri belirli fonksiyonlara bağlar.
    - @app.get("/users") -> /users adresine gelen GET isteğini bu fonksiyona yönlendir demektir.
    - Yani decorator, HTTP isteği ile Python fonksiyonunu ilişkilendirir.

## Uygulama Yaşam Döngüsü
FastAPI uygulaması, çalıştığı süre boyunca 3 temel aşamadan geçer.

1. Startup (Başlatma)
- Uygulama başlarken yapılması gereken işlemler burda tanımlanır. Örnek: veritabanı bağlantısı açmak, Redis'e bağlanmak
- @app.on_event("startup") decorator'ı ile yapılır.

2. Running (Çalışma)
- API endpoint’leri gelen istekleri işler.
- Kullanıcıdan gelen her HTTP isteği, tanımlı route’lardan birine yönlendirilir.

3. Shutdown (Kapatma)
- Uygulama kapanırken yapılması gereken temizlik işlemleri burada olur. Örnek: veritabanı bağlantısını kapatmak, logları flush etmek, cache temizlemek.
- @app.on_event("shutdown") decorator’ı ile tanımlanır. 


# events.py 
- startup ve shutdown işlemleri genellikle events.py dosyasında yönetilir.
- Amacı uygulama başlatıldığında veya kapandığında yapılacak işlemleri merkezi şekilde tanımlamak.
    - PostgreSQL ve Redis bağlantılarını başlatmak.
    - Background servislerini tetiklemek.
    - Log servislerini devreye almak.


## APIRouter Nedir ?
- APIRouter, FastAPI'de route(endpoint) tanımlarını modüler hale getirmek için kullanılan bir sınıftır. Normalde @app.get() gibi decorator'lar doğrudan main.py içinde tanımlanabilir, ama büyük projelerde bu yöntem kod karmaşasına neden olur.
- Bu yüzden FastAPI, her modül (auth, payments, users, vs.) için ayrı bir router tanımlamayı destekler.
- main.py dosyası içinde değilde router.py dosyası içinde olma nedeni main.py dosyası sadece uygulama başlatma ve yapılandırma görevini üstlenir.
- Bu yüzden her alan (örneğin auth.py, payments.py, transactions.py) kendi router’ını tanımlar

Örnek :
app/
 ├── main.py
 ├── api/
 │    └── v1/
 │         ├── auth.py
 │         ├── payments.py
 │         ├── transactions.py
 │         └── router.py

auth.py, payments.py ve transactions.py her biri kendi router’ını tanımlar. router.py tüm router’ları tek bir noktada toplar. Son olarak, ana uygulama bu “ana router”’ı dahil eder.


# "v1" versiyonlama kullanımı
- API’ler zamanla değişir: yeni alanlar eklenir, bazı endpoint’ler kaldırılır veya veri formatı değişir.
- Bu durumda, eski kullanıcıların (örneğin mobil uygulama, entegrasyonlar) bozulmaması için versiyonlama yapılır.
- Eski kullanıcılar /v1 ile çalışmaya devam ederken, yeni özellikler /v2 üzerinden sunulur. Bu sayede geriye dönük uyumluluk (backward compatibility) korunur.

# core/config.py içinde genellikle ne olur
- core/config.py, projenin tüm yapılandırma ayarlarını (configuration settings) merkezi bir yerde toplar.
- Yani veritabanı bağlantı bilgileri, API anahtarları, gizli anahtarlar, port numaraları gibi değerler burada tanımlanır.
- Geliştirme, test ve prod ortamlarında farklı ayarları kolayca değiştirebilmek.
- Bu dosya .env içindeki değişkenleri otomatik okur be settings nesnesine yükler.

# .env dosyasnın görevi
- .env dosyası, sistem ortam değişkenlerini (environment varibales) içerir. Bu dosya gizli bilgileri koddan ayırmak için kullanılır

# .env → config.py → main.py Akışı
- .env dosyası ortam değişkenlerini barındırır (genelde .gitignore eklenir)
- core/config.py, pydantic.BaseSettings aracılığıyla bu değişkenleri okur ve Settings sınıfına aktarır.
    - .env dosyasındaki her satır otomatik olarak bir sınıf özelliğine (attribute) dönüşür.
- main.py, config.py içindeki settings nesnesini kullanır.
    - Uygulama başlarken bu ayarları kullanarak veritabanı, Redis veya diğer servis bağlantılarını kurar.

# Dependency Injection
- Bağımlılık enjeksiyonu (DI), bir fonksiyonun ihtiyaç duyduğu nesneleri kendisi oluşturmak yerine dışarıdan alması prensibidir.
- FastAPI’de bu mekanizma Depends() fonksiyonu ile yönetilir.

# dependencies.py Dosyasında Ne Olur?

- Büyük projelerde bağımlılıklar genellikle dependencies.py dosyasında toplanır.
- Bu sayede kod modüler olur, test etmek kolaylaşır.
- Bu dosyada tipik olarak bulunan fonksiyonlar:
    - get_db() : Veritabanı oturumunu (session) oluşturur ve yönetir.
    - get_current_user() : JWT token doğrulaması yapar, aktif kullanıcıyı döndürür.
    - get_settings() : Ortam ayarlarını (config) döndürür.
    - common_parameters() : Sayfalama, filtre gibi tekrarlanan parametreleri sağlar.

# Lifetime (Yaşam Süresi) Kavramı
- Bağımlılıkların lifetime (ömür) kavramı, o bağımlılığın ne kadar süreyle aktif kalacağını belirler.
- Bir bağımlılık yield içeriyorsa → “yaşam döngüsü” vardır.
- FastAPI bu bağımlılığı çağırır, yield’e kadar çalıştırır, endpoint bittiğinde yield’den sonrasını (cleanup kısmını) otomatik olarak çalıştırır.

# Uygulama Mimarisi Akış Diyagramı

┌──────────────┐
│   Request    │   
│ (HTTP İsteği)│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Router     │
│ (API Katmanı)│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Service    │
│ (İş Mantığı) │
└──────┬───────┘
       │
       ▼
┌────────────────┐
│   DB / Session  │
│ (Veritabanı Katmanı) │
└──────┬─────────┘
       │
       ▼
┌──────────────┐
│   Response   │
│ (HTTP Yanıtı)│
└──────────────┘


Request → Router : Kullanıcı veya istemci (örneğin frontend, Postman, mobil uygulama) HTTP isteği gönderir (GET, POST, PUT, DELETE). Bu istek, Router (API katmanı) tarafından karşılanır. Router, hangi endpoint’in çağrıldığını belirler ve isteği ilgili fonksiyona yönlendirir.

Router → Service : Router sadece yönlendirme yapar; karmaşık mantıkları içermez. Gerçek iş mantığı (örneğin sipariş oluşturma, kullanıcı doğrulama, ödeme hesaplama) Service katmanında yer alır. Router, gerekli bağımlılıkları (örneğin db, current_user) Depends() ile service fonksiyonuna iletir.

Service → DB/Session : Service katmanı, iş mantığını yürütürken veritabanı işlemlerine ihtiyaç duyabilir. Bu aşamada db oturumu (Session) kullanarak CRUD işlemleri yapılır (SELECT, INSERT, UPDATE, DELETE). Bağlantı dependencies.py içindeki get_db() fonksiyonu aracılığıyla yönetilir (yield dependency).

DB/Session → Response : Veritabanı işlemi tamamlandıktan sonra sonuç service katmanına, oradan router’a döner. Router bu sonucu JSON formatında HTTP Response olarak kullanıcıya iletir.