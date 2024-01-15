### Kurulum
``` sh
pip install -r requirements.txt
cd client && yarn 
```
### Çalıştırma
``` sh
uvicorn main:app --reload

cd client & yarn dev
```

### Bard Token Hatası 

  File ".\train_gpt_models\.venv\Lib\site-packages\bardapi\core.py", line 142, in _get_snim0e
    raise Exception(
Exception: __Secure-1PSID value must end with a single dot. Enter correct __Secure-1PSID value.

- Comment block this lines 141 -144

     if not self.token or self.token[-1] != ".":
         raise Exception(
             "__Secure-1PSID value must end with a single dot. Enter correct __Secure-1PSID value."
         )



## Popüler LLM' lerin Eğitilerek Karşılaştırılması

> Llama tamamen ücretsiz olması ile birlikte daha fazla ayrıntı ve içerik sağlayarak en başarılı llm olarak belirlendi

> gemini-pro ise diğer llm lere göre çok alakasız ve saçma yanıtlar vererek en kötü llm seçildi

#### Paketler
-   React
-   FastApi
-   Langchain
-   bard-api
-   llama-api
-   google.generativeai
-   openai

#### Modeller
-   Gpt-3.5-Turbo
-   Gpt-4
-   llama-default
-   gemini-pro
-   bard (ChatBot)
#### Limitler
-   bard-api > dakikada 10 request
-   llama > -
-   gemini > dakikada 60 request
-   gpt-3.5-turbo > 0.0003$
-   gpt-3.5-turbo > 0.0006$

#### Karşılaşılan İstisnai Durumlar
-   bard-api paketinin google dan bağımsız bir ekip tarafından geliştirilmesi nedeni ile api-key alma işleminde yaşanan sıkıntılar

> Google' ın yeni api key politikası ile oluşan api-key formatı hatası, paket kodları elle müdahele edilerek değiştirllerek düzeltildi, buna rağmen her paket yükleme işlemi sonrası pakete herhangi bir güncelleme gelene kadar tekrarlanması gerekmekte  

-   bard-api' nin langchain paketi ile kullanılabilmesi için herhangi bir adaptör paketininin mevcut olmaması

> Langchain paketinin bard-api ile çalışabilmesi için harici bir adaptör sınıfı yazıldı, bu durum bard' ın aslında llm değil de chatbot olamsından kaynaklı yeterince verimli olamamasına neden oldu buna rağmen performans açısından llama ya yakın sonuçlar verdi 


#### Uygulamanın içeriği

Ortak bir eğitim havuzu oluşturularak bütün botlara erişim imkanı tanındı, her bottan kendisine gelen isteklere cevap vermesi istenerek süre ve içerik metninin uzunluğu ve anlat bütünlüğü test edildi, Bütün botlara aynı anda istek atılarak ilk cevap veren en altta kalacak şekilde anlık olarak listeleme yapıldı  

#### Sistemin İşleyişi
Öncelikle bir eğitim dosyası hazırlanarak langchain paketi içerisindeki loader yöntemi ile okuma işlemi sağlandı bu yöntem ile bütün dosya formatları desteklenmektedir, daha sonra alınan eğitim içeriği embedding işlemi için GooglePalmEmbbeding, OpenAiEmbedding gibi embedding api hizmetlerine gönderilerek bir vector index store oluşturma işlemi yapıldı, hazırlanan bu vector store index içerisinde query işlemi yapılarak sorulan sorgu ile alakalı unsurlar belirlenerek bir içerk oluşturuldu, oluştrurlan bu içerik llm e gönderilerek llm in bir sonuç veya çıkarım yapması istenildi   


#### Test Materyalleri
-   Emirdağ baskını maakalesi
-   Göz hastalıkları
