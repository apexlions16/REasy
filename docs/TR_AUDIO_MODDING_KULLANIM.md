# REasy Ses Modlama Kullanım Notları

Bu doküman, fork üzerinde eklenen ses modlama altyapısının nasıl kullanılacağını açıklar.

## 1. Ses bankası raporu üretme

Yeni eklenen CLI aracı:

```bash
python tools/audio_mod_report_cli.py "path/to/soundbank.bnk" --out-dir reports
```

veya PCK için:

```bash
python tools/audio_mod_report_cli.py "path/to/soundbank.pck" --out-dir reports
```

Çıktılar:

```text
reports/soundbank_bnk_audio_report.json
reports/soundbank_bnk_audio_report.csv
```

Rapor alanları:

```text
index
source_id
name
dialogue_text
offset
length
absolute_offset
embedded
duration_seconds
codec
channels
sample_rate
suggested_wem_filename
suggested_wav_filename
notes
```

## 2. Name map ile source ID -> isim/replik eşleştirme

Bir CSV/JSON/TXT dosyası vererek source ID'leri anlamlı isimlere ve replik metinlerine bağlayabilirsiniz.

Örnek CSV:

```csv
source_id,name,dialogue_text,character,replacement_filename,notes
42190312,vo_leon_combat_003,"Example original subtitle line",Leon,42190312_TR.wav,"Source ID based replacement"
88123012,ui_menu_confirm,"",UI,ui_menu_confirm.wav,"Name based replacement candidate"
```

Kullanım:

```bash
python tools/audio_mod_report_cli.py "path/to/soundbank.bnk" --name-map resources/examples/audio_name_map_example.csv --out-dir reports
```

## 3. Replik eşleştirme mantığı

Replik eşleştirme için tek bir kesin yöntem yoktur. REasy fork'unda şu sırayla ilerlenmelidir:

1. Önce source ID'ler çıkarılır.
2. Varsa Wwise companion dosyalarından isimler bulunur.
3. Varsa MSG/subtitle/metin dosyalarından replikler çıkarılır.
4. İsim, ID, karakter, sahne ve süre bilgisiyle aday eşleşmeler üretilir.
5. Gerekirse WEM -> WAV -> speech-to-text yapılarak metin benzerliğiyle ikinci kontrol yapılır.
6. Kullanıcıya aday eşleşmeler raporlanır.

İlk aşamada CSV/JSON/TXT name map desteği eklendi. Sonraki aşamada `SoundbanksInfo.xml`, `Wwise_IDs.h`, `wwnames.txt`, `wwnames.db3` ve MSG/subtitle parser'ları eklenecektir.

## 4. Publish package / EXE üretme

Fork'a özel GitHub Actions workflow'u eklendi:

```text
.github/workflows/build-fork-package.yml
```

GitHub üzerinden çalıştırma:

1. GitHub'da repo sayfasına girin.
2. `Actions` sekmesini açın.
3. `Build Fork Package` workflow'unu seçin.
4. `Run workflow` butonuna basın.
5. İş tamamlanınca artifact kısmından ZIP paketini indirin.

ZIP içinde `dist/REasy.exe` ve gerekli kaynak dosyaları bulunur.

Bu workflow imzasız paket üretir. Orijinal workflow'daki SignPath/Firebase secret'larına ihtiyaç duymaz.

## 5. Geliştirmede sıradaki adım

Bir sonraki kod adımı, `SoundViewer` içine şu butonların bağlanmasıdır:

```text
Load Name Map
Export Report
```

Böylece CLI kullanmadan doğrudan uygulama arayüzünden JSON/CSV raporu alınabilecektir.
