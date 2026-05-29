# REasy Editor v0.7.0 ![GitHub all releases](https://img.shields.io/github/downloads/seifhassine/REasy/total)

<p align="center">
  <img src="resources/images/reasy_editor_logo.png" alt="REasy Editor Logo" style="max-width:300px;">
</p>


<br>

**REasy Editor**, RE oyunları için geliştirilmiş bir kullanım kolaylığı araç setidir. Şu anda bazı RE Engine dosyalarını görüntülemeyi ve düzenlemeyi destekler. Ayrıca çalışma sürecinizi hızlandırmak için çeşitli yardımcı araçlar da içerir.
Tüm oyunlardaki RSZ dosyalarını (SCN, PFB, User) destekler; bunun yanında UVAR, MSG, MOTBANK, MESH ve CFIL dosyaları için de destek sunar.

REasy arayüzü şu anda İngilizce ve Çince (sınırlı) olarak kullanılabilir.


<br>
<br>

<p align="center">
   <img src="https://github.com/user-attachments/assets/64a84918-ad58-47ee-8186-e0e7a5a1ace0" alt="REasy Editor Logo" width=70%">
</p>

<p align="center">
<img alt="image" src="https://github.com/user-attachments/assets/19ca472b-8578-495a-852e-a8ddc924b06c"  width=70%/>
</p>

<br>


## Özellikler

<br>
<div align="center">

<sub><sup>Not: Aşağıdaki formatlar kaynak koda göre listelenmiştir. Yayın arşivi güncel olmayabilir ve bu formatların tamamını henüz desteklemiyor olabilir.</sup></sub>  
<sub><sup>Not 2: Birçok format RE7 non-rt sürümünde desteklenmez.</sup></sub>  
| Dosya Türü | Destek | Test Edildiği Oyunlar |
|-----------|---------|-----------|
| UVAR      | ✅       | Çoğu oyun  |
| RCOL      | ✅    <sub><sup>[RE7, Wilds DESTEKLENMEZ]</sup></sub>   | Çoğu oyun       |
| SCN       | ✅       | Çoğu oyun       |
| User       | ✅       |Çoğu oyun       |
| PFB       | ✅       | Çoğu oyun      |
| MSG       | ✅       | Çoğu oyun      |
| MESH (3D Görüntüleme)       | ✅ <sub><sup>[RE7, KGPG DESTEKLENMEZ]</sup></sub>       | Çoğu oyun      |
| PAK       | ✅       | Çoğu oyun      |
| CFIL       | ✅       | Çoğu oyun      |
| MOTBANK       | ✅       | Çoğu oyun      |
| MCAMBANK       | ✅       | Çoğu oyun      |
| TEX/DDS       | ✅ <sub><sup>[Görüntüleme/Dönüştürme]</sup></sub>      | Çoğu oyun      |
| MDF       | ✅       |    Çoğu oyun   |
| BNK/PCK       | ✅       |    Çoğu oyun   |
| WEL       | ✅       |    Çoğu oyun|
| WCC       | ✅       |    Çoğu oyun |
| UVS       | ✅       |    Çoğu oyun   |
| CDEF       | Yakında       |       |
| EFX       | Yakında       |       |
  
</div>
<br>
<br>

- **PAK Dosyası Çıkarma ve Oluşturma**  
  - REasy şu anda en hızlı PAK çıkarma sistemine sahiptir.
  - Tekil giriş çıkarma desteği sunar.
  - Dosya listesinde Regex araması desteklenir.
 
- **3D Mesh İnceleme**
   
- **RSZ Genişletilmiş Dosya Görüntüleme ve Düzenleme:**  
  - User, PFB ve SCN dosyaları gelişmiş düzenleme özellikleriyle desteklenir.
  - Template Manager ile favori GameObject öğelerinizi dışa aktarabilir ve bunları farklı dosyalara içe aktarabilirsiniz. Dışa aktarılan GameObject öğeleri `templates` dizininde düz metin (JSON) olarak bulunur.
  - Farklı dosyalar arasında array öğeleri, component'ler ve GameObject'ler için kopyala-yapıştır yapmayı sağlayan pano sistemi bulunur (JSON olarak serileştirilir).
  - Community Templates tarayıcısı sayesinde farklı oyunlar için diğer kullanıcıların şablonlarını indirebilir, puanlayabilir ve kendi şablonlarınızı yükleyebilirsiniz (Template Manager içinden erişilebilir).
  - Tüm oyunlar için güncel ve iyileştirilmiş RSZ dump dosyaları bulunur.
  - Eski/uyumsuz RSZ dosyası algılayıcısı mevcuttur (`Tools` bölümünde bulunur).
  - RE7'den itibaren kullanılan tüm RSZ dosya sürümleri desteklenir.
  - Ve çok daha fazlası...
    
- **RSZ Diff Viewer:**  
  - RSZ dosyalarını karşılaştırmayı sağlar. Şu anda yalnızca SCN dosyaları desteklenmektedir.

- **Arama İşlevi:**  
  Dizinler genelinde tüm dosyalarda şunları arayabilirsiniz:
  - Belirli metinler (UTF-16LE kodlamalı)
  - 32-bit sayılar (hexadecimal gösterimle)
  - GUID değerleri (standart formattan dönüştürme ile)
  - Belirli RSZ alan değerleri

- **Project Manager:**
  
  Mod oluşturma ve bunları `.PAK` ya da Fluffy Manager `.ZIP` arşivi olarak dışa aktarma olanağı sunar (`File > Create Project`).
   
-  **Dosyalar için Yedekleme Sistemi**

-  **Karanlık Mod**  



## Rehberler:

- **Wiki:**  
  [Buradan](https://github.com/seifhassine/REasy-Wiki/blob/main/README.md) erişilebilir. Çalışma devam ediyor.
   
- **RE4R'ye Yeni Flag Ekleme:**  
  22000 yeni flag eklemeyi test ettim (dosya boyutu 2 MB'tan yaklaşık 16 MB'a çıktı) ve bazılarını rastgele denedim. Oyun stabil çalıştı. 50 bin eklenen flag seviyesinde, oyun kaydı tetiklendiğinde çöküyor. Kesin sınırı belirlemek için testlerinize ve geri bildiriminize ihtiyaç var. Ancak 20 bin fazlasıyla yeterli olmalı. ([Burada](https://www.nexusmods.com/residentevil42023/articles/346) bir rehber yazdım.)

- **RE8:**
  [Modding Weapons and Items with REasy Editor](https://www.nexusmods.com/residentevilvillage/articles/45) - [matalayudasleazy](https://next.nexusmods.com/profile/matalayudasleazy?gameId=3669) tarafından hazırlanmıştır.

## Doğruluk

- Çıkıştan önce çoğu oyundaki tüm RSZ (`.user`, `.pfb`, `.scn`) dosyaları test edilir:
  
    [![Build and Package REasy](https://github.com/seifhassine/REasy/actions/workflows/build.yml/badge.svg)](https://github.com/seifhassine/REasy/actions/workflows/build.yml)


## RSZ Dump Dosyaları:

- [/resources/data/dumps](https://github.com/seifhassine/REasy/tree/master/resources/data/dumps) altında tüm oyunlar için güncellenmiş RSZ şablonlarının listesini bulabilirsiniz.

## Kurulum

- `build.bat` dosyasını çalıştırın.

- Python bağımlılıkları `requirements.txt` dosyasında listelenmiştir.

- Microsoft Visual C++ 14.0 veya daha yeni bir sürüm gereklidir. Bunu "Microsoft C++ Build Tools" ile edinebilirsiniz: https://visualstudio.microsoft.com/visual-cpp-build-tools/

- Python 3.12+ gereklidir.

- `build.bat`, 3.12+ sürümünün bulunmadığını söylüyorsa varsayılan olarak hangi Python sürümünün kullanıldığını kontrol etmek için `python --version` komutunu çalıştırın.

- `REasy.py` dosyasını çalıştırmak istiyorsanız, öncesinde build batch script'ini kullanmalı veya `python setup.py build_ext --inplace` komutunu çalıştırmalısınız.

REasy'yi Linux üzerinde çalıştırmak istiyorsanız ve açılışta "Aborted" hatasıyla karşılaşırsanız, `apt-get` kullanarak `libxcb-cursor0` paketini yüklemeyi deneyin.

## Katkıda Bulunanlar:

010 RE şablonları için @alphazolam.

RE'nin MurMurHash3 implementasyonu için @TrikzMe.

RSZ JSON dump dosyalarını ve REF'i hazırladığı için @praydog.

`.exe` hata ayıklama ile ilgili konularda yardımcı olduğu için Discord'dan @don.

Çeşitli konularda danışmanlık sağladığı ve birçok güncel dosya formatı yapısını paylaştığı için @shadowcookie.

PAK dosyası şifre çözme algoritmaları için @Ekey.

MHWILDS+ üzerindeki MPLY flag'leri için @NSACloud.

## REasy'yi Destekleyin:

Çalışmamı beğeniyor ve aracın geliştirilmesini desteklemek istiyorsanız, bu [bağlantı](https://linktr.ee/seifhassine) üzerinden destek olabilirsiniz.

## Lisans ve Katkılar:

REasy, MIT lisansı altındadır.
Projeye katkıda bulunabilirsiniz. Şu anda aktifim ve PR'ları inceleyeceğim.

## Üçüncü Taraf Bileşenler

Bu proje, **[PySide6](https://pypi.org/project/PySide6/)** (Qt for Python) kullanır ve **LGPL version 3** lisansı altındadır.
Daha fazla bilgi için:  
- [Qt Licensing Information](https://www.qt.io/licensing/)  
- [LGPL v3 License Text](https://www.gnu.org/licenses/lgpl-3.0.html)
   
## Sponsorlar
<table>
 <tbody>
  <tr>
   <td align="center"><img alt="[SignPath]" src="https://avatars.githubusercontent.com/u/34448643" height="30"/></td>
   <td>Windows üzerinde ücretsiz kod imzalama hizmeti <a href="https://signpath.io/">SignPath.io</a> tarafından, sertifika ise <a href="https://signpath.org/">SignPath Foundation</a> tarafından sağlanmaktadır.</td>
  </tr>
 </tbody>
</table>