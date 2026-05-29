# REasy Ses Modlama Yol Haritası

Bu doküman, REasy fork'unu özellikle RE Engine / Wwise ses modlama iş akışına göre geliştirmek için hazırlanmıştır.

Amaç yalnızca BNK/PCK içindeki WEM dosyalarını değiştirmek değildir. Asıl hedef, kullanıcının oyundaki sesleri, replikleri ve mümkünse subtitle/metin verilerini daha anlaşılır şekilde eşleştirip güvenli bir mod paketi üretebilmesidir.

## Mevcut durum

REasy içinde ses tarafında hâlihazırda şu temel yapı vardır:

- `BKHD`, `AKPK`, `SBNK`, `SPCK` magic değerlerini ses konteyneri olarak algılayan `SoundHandler`.
- BNK/PCK parse eden `bnk_parser.py`.
- Track/source ID çıkarma.
- Gömülü WEM verisini dışa aktarma.
- WEM'i vgmstream ile WAV'a decode ederek dinleme.
- Tekil track değiştirme.
- Klasörden toplu değiştirme.
- WAV/MP3/OGG/FLAC gibi girişleri FFmpeg ile PCM16 WAV'a dönüştürüp WEM benzeri RIFF/WAVE çıktısı oluşturma.
- Basit waveform ve sessizlik atlama önizlemesi.

Bu temel iyi, fakat gerçek ses modlama için eksik kalan şeyler şunlardır:

- Source ID'lerin anlamlı isimlere bağlanması.
- Event -> WEM / source ID ilişkisinin gösterilmesi.
- Replik/subtitle metni ile ses dosyasının eşleşmesi.
- Büyük projelerde export/replace raporu.
- Değişiklik öncesi risk/uyumluluk kontrolü.
- Mod paketi klasör yapısının otomatik üretilmesi.

## Repliklerle eşleştirme mümkün mü?

Evet, bazı oyunlarda mümkündür; ancak tek ve her oyunda %100 çalışan bir yöntem yoktur. Kullanılabilecek yöntemler aşağıdaki sırayla denenmelidir.

### 1. Wwise companion dosyaları ile ID -> isim eşleştirme

Bazı projelerde veya çıkarılmış verilerde şu tip dosyalar bulunabilir:

- `SoundbanksInfo.xml`
- `Wwise_IDs.h`
- bank dump `.txt` dosyaları
- `wwnames.txt`
- `wwnames.db3`
- kullanıcı tarafından hazırlanmış CSV/JSON listeleri

Bu dosyalar varsa en temiz yol source ID'leri event, object veya WEM isimleriyle eşleştirmektir.

Örnek:

```text
42190312 -> vo_leon_combat_003
88123012 -> ui_menu_confirm
```

Bu yöntem çoğu zaman replik metnini vermez, ancak sesin neye ait olduğunu anlamayı ciddi şekilde kolaylaştırır.

### 2. Oyun metin/subtitle dosyaları ile eşleştirme

RE Engine oyunlarında metinler genellikle MSG gibi ayrı dosya formatlarında tutulabilir. Eğer subtitle/replik metinleri çıkarılabiliyorsa şu alanlar üzerinden eşleştirme yapılabilir:

- Dosya adı benzerliği
- Event adı benzerliği
- Line ID / message ID benzerliği
- Karakter adı
- Sahne/quest/chapter adı
- Dil dosyası anahtarı

Örnek akış:

```text
MSG/metin dosyaları tara
  -> replik anahtarlarını çıkar
  -> Wwise/event isimleriyle fuzzy match yap
  -> aday eşleşmeleri kullanıcıya göster
```

Bu yöntem oyuna göre değişir. Bazı oyunlarda çok iyi çalışır, bazılarında yalnızca aday üretir.

### 3. Ses transkripsiyonu ile eşleştirme

Eğer metin dosyaları var ama ID bağlantısı yoksa veya seslerin isimleri anlamsızsa, çıkarılmış WAV dosyaları otomatik transkripsiyondan geçirilebilir.

Akış:

```text
WEM -> WAV
WAV -> speech-to-text
Transkript -> subtitle/metin listesiyle fuzzy match
```

Bu yöntem özellikle İngilizce seslerde güçlüdür. Türkçe dublaj üretiminde ise orijinal ses transkriptini, Türkçe çeviri tablosuna bağlamak için kullanılabilir.

### 4. Süre ve waveform tabanlı aday eşleştirme

Eğer elimizde sadece ses ve subtitle süreleri varsa:

- Ses süresi
- Subtitle görünme süresi
- Aynı sahnede sıralama
- Karakter sırası
- Dosya/klasör bağlamı

kullanılarak aday eşleştirme yapılabilir. Bu yöntem tek başına zayıftır ama diğer yöntemlerle birleşince işe yarar.

## Geliştirme sırası

### Faz 1 - Raporlama ve proje zemini

Hedef: Ses bankasını açınca değiştirilebilir tüm track'leri dışarıya düzenli rapor olarak verebilmek.

Yapılacaklar:

- `audio_mod_report.py` modülü.
- JSON/CSV rapor üretimi.
- Track/source ID, süre, codec, kanal, sample rate, offset, length alanları.
- İsteğe bağlı name map dosyası okuma.
- CSV/JSON/TXT name map desteği.

Durum: Başlandı.

### Faz 2 - REasy arayüzüne rapor/export butonları

Hedef: SoundViewer içinde tek tıkla rapor alma.

Yapılacaklar:

- `Export Report` butonu.
- `Load Name Map` butonu.
- Seçilen map dosyasını geçici olarak viewer'a bağlama.
- Raporu `.json` ve `.csv` olarak kaydetme.
- İsim ve replik metni varsa tabloda gösterme.

### Faz 3 - Akıllı bulk replace

Hedef: Dosya adı yalnızca source ID olmak zorunda kalmasın.

Eşleştirme sırası:

1. `source_id.wav`
2. `source_id_TR.wav`
3. name map'teki `name.wav`
4. CSV'deki özel `replacement_filename`
5. kullanıcı onaylı fuzzy eşleşme

Çıktı:

- kaç track değişti
- kaç dosya eşleşmedi
- hangi dosya hangi source ID'ye gitti
- risk uyarıları

### Faz 4 - Uyumluluk kontrolü

Replace öncesi ve sonrası şu alanlar karşılaştırılmalı:

- Süre farkı
- Kanal sayısı
- Sample rate
- Codec
- Dosya boyutu
- Embedded/external durum

Risk seviyesi:

```text
LOW    -> büyük ihtimalle güvenli
MEDIUM -> oyunda test edilmeli
HIGH   -> sessizlik, loop hatası veya crash riski olabilir
```

### Faz 5 - Wwise companion parser'ları

Hedef: ID'leri anlamlı isimlere bağlamak.

Eklenecek parser'lar:

- `SoundbanksInfo.xml`
- `Wwise_IDs.h`
- `wwnames.txt`
- `wwnames.db3`
- wwiser dump çıktıları

### Faz 6 - Replik/subtitle eşleştirme

Hedef: Sesleri mümkün olduğunca oyundaki repliklerle bağlamak.

Kaynaklar:

- REasy'nin MSG handler'ı
- export edilmiş subtitle/text CSV'leri
- kullanıcı çeviri tabloları
- speech-to-text çıktıları

Eşleştirme yöntemi:

```text
source_id/name/event bilgisi
+ MSG/subtitle anahtarları
+ karakter/sahne bilgisi
+ süre/sıra bilgisi
+ fuzzy text matching
```

Çıktı:

```text
source_id,name,character,original_text,translated_text,duration,replacement_status
```

### Faz 7 - Mod paketi çıktısı

Hedef: Kullanıcı yalnızca bank değiştirmesin, test edilebilir mod paketi alsın.

Çıktı yapısı:

```text
AudioModProject/
  original_wem/
  decoded_wav/
  replacements/
  rebuilt_banks/
  reports/
  mod_output/
```

## İlk uygulanacak teknik parça

İlk gerçek teknik parça `file_handlers/sound/audio_mod_report.py` modülüdür. Bu modül ses bankasından track raporu çıkarır ve ileride arayüz, replik eşleştirme ve bulk replace sisteminin temel veri modelini sağlar.
