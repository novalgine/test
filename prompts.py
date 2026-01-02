
# --- Custom CSS ---
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* 1. LAYOUT & PADDING FIXES */
    [data-testid="stAppViewContainer"] > .main > .block-container {
        padding-top: 120px !important;
        padding-bottom: 5rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }

    /* 2. NAVBAR (Fixed & Glass) */
    .main .block-container > div[data-testid="stVerticalBlock"] > div:first-child {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        height: 100px !important;
        background: rgba(13, 17, 23, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        z-index: 9999 !important;
        padding: 15px 50px !important;
        margin: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        border-radius: 0 !important;
    }
    
    .main .block-container > div[data-testid="stVerticalBlock"] > div:first-child > div {
        width: 100% !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }

    /* 3. LOGIN SCREEN & CONTENT FIX */
    .main .block-container > div[data-testid="stVerticalBlock"] > div:nth-child(2) {
        margin-top: 60px !important;
    }

    /* 4. TABS STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px !important;
        background-color: transparent !important;
        padding-bottom: 10px !important;
        margin-top: 20px !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0 30px !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #aaaaaa !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-color: #8b5cf6 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4) !important;
    }

    /* 5. BUTTONS */
    .stButton > button, 
    div[data-testid="stButton"] > button[kind="primary"],
    [data-testid="stForm"] button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 32px !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4) !important;
    }
    .stButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-2px) !important;
    }

    /* 6. INPUTS */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea, 
    .stSelectbox > div > div > div {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
    }
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus, 
    .stSelectbox > div > div > div:focus-within {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.5) !important;
    }

    /* 7. DASHBOARD CARDS */
    .persona-card {
        background: #1e293b !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 20px !important;
    }
    .persona-card:hover {
        border-color: #8b5cf6 !important;
        transform: translateY(-4px);
    }
    
    /* Progress Bars */
    .dna-progress {
        height: 8px;
        border-radius: 4px;
        background: rgba(255, 255, 255, 0.1);
        overflow: hidden;
        margin: 12px 0;
    }
    .dna-progress-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    .progress-low { background: #EF4444; }
    .progress-mid { background: #F59E0B; }
    .progress-high { background: #10B981; }

    /* 8. HIDE DEFAULTS */
    hr { display: none !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 9. GLOBAL THEME */
    .stApp {
        background-color: #0e1117 !important;
        background-image: radial-gradient(#30363d 1px, transparent 1px) !important;
        background-size: 40px 40px !important;
        font-family: 'Inter', sans-serif !important;
    }
</style>
"""

# --- LIBRARIES ---

HOOK_LIBRARY = """ (STORYTELLING HOOKS - Kişisel anlar ve dersler için)

[Kısa süre] içinde [anahtar hedefe] şu şekilde ulaştım, böylece [ikincil fayda/özgürlük] için bana zaman kaldı.

Başarılı olmak için ustalaşmanız gereken tek bir şey var, o da [anahtar beceri veya zihniyet].

Cidden, [Yıl] yılında [sektör/niş] için işin en büyük açığını yakaladığımı düşünüyorum. Beni iyi dinleyin.

Şu an [etkileyici kilometre taşı] seviyesindeyim ama daha geçen sene bu zamanlar sadece [daha küçük kilometre taşı] seviyesindeydim.

[Zaman aralığı] önce [yeni alışkanlık/eylem] yapmaya karar verdim, çünkü [önceki mücadele] ile geçen [zaman aralığı] beni tüketmişti.

[Zaman aralığı] boyunca [mücadeleler/zorluklar] ile boğuştuktan sonra, o hayat değiştiren kararı verdim.

Geçtiğimiz [zaman aralığı] içinde, bir [kimlik/meslek] olarak ilk [kazanç/başarı] seviyeme ulaştım ama buna rağmen [beklenmedik zorluk] yaşadım.

[Zaman aralığı] önce, [platform]’da [niş] içerikler üretmeye başladım ama [beklenmedik sonuç/yanlış anlaşılma] oldu.

Eğer şu an sıfırdan başlıyor olsaydım ve hedefim [istenilen kilometre taşı] olsaydı, yapacağım tek şey şu olurdu.

[Anahtar eylem]’i yapmakta neden bu kadar geç kaldığıma inanamıyorum.

[Sektör/konu] hakkında aldığım en berbat tavsiye ve ondan öğrendiğim ders.

Çoğu insan bunu kendine saklar ama size [hedefe ulaşma]’nın asıl sırrını anlatacağım.

Bu, [küçük eylem veya farkındalık]’ın hayatınızı nasıl değiştirebileceğine dair bir hikaye.

Kimse [sektör/iş]’in gerçekten acımasız kısımlarından bahsetmiyor. Gelin [zorlu gerçeklik]’i konuşalım.

Herkes [önemli unsur]’a ihtiyacınız olduğunu söylüyor, ama Allah aşkına [önemli unsur] aslında ne işe yarıyor?

Herkes [popüler trend] hakkında konuşuyor, ama [konsept] aslında nedir?

[Platform/araç] üzerinde [etkileyici sonuç] almak için bu taktiği kullanıyorum, bence hemen şimdi bunu benden çalmalısınız.

Hayatta geri kalmış hissetmenizin tek nedeni, kendinizi [yanlış standart] ile kıyaslamanız.

Kariyerimde/hayatımda "keşke daha önce bilseydim" dediğim o fikir [anahtar ders] oldu.

Size muhtemelen pek sık duymadığınız bir tavsiye vereceğim ve çoğunuz benimle aynı fikirde olmayacaksınız…

Şu anda bunu izleyen çoğunuz kendinizi [hedef]’ten alıkoyuyorsunuz, çünkü [yaygın korku/sınırlayıcı inanç] sizi tutuyor.

Benim yaptığım hatayı yapmayın, [etkisiz eylem yapma] ile boşuna zaman kaybetmeyin.

Ne yaparsanız yapın, sakın bunu bilmeden [eylem yapma] işine girmeyin.

İşte [hedefe ulaşma] hakkındaki acı gerçekler, madde bir…

Çoğu insan sadece [yaygın yanlış kanı]’nın [beklenen sonuç] vereceğini sanıyor ama bu gerçekten çok uzak.

Eğer [kitleniz için yaygın mücadele] konusunda zorlanıyorsanız, bu videoyu sonuna kadar izleyin…

Sıfırdan başlayarak, [kısa süre] içinde [hedef kitleniz için arzu edilen sonuç]’a nasıl ulaştım?

Eğer [arzu edilen sonuç] istiyor ama sürekli [yaygın mücadele] yaşıyorsanız, çözüm burada…

Yaptığınız bu küçücük hata [içeriğinizi/performansınızı] mahvediyor ve düzeltmesi inanın çok kolay.

[Yaygın mücadele] olmadan [hedef kitleniz için arzu edilen sonuç]’a ulaşabildiğinizi hayal edin…

(CONTRARIAN HOOKS - İnanışları sarsmak ve ezber bozmak için)

Herkes başarılı olmak için [X]’e ihtiyacınız olduğunu söylüyor. Ben katılmıyorum.

Kulağa delilik gibi gelebilir ama [popüler olmayan görüş veya gerçek].

[İstenilen sonuç] için aslında [yaygın gereklilik]’e ihtiyacınız yok.

Çoğu insan [popüler strateji]’yi tamamen yanlış uyguluyor.

Herkesin öğrettiğinin tam tersini yaparak büyüdüm.

İşte [boş metrik/takipçi sayısı vb.]’ni artık neden umursamıyorum?

Linç yiyebilirim ama söylüyorum: [cesur iddia].

Gerçek şu ki, [popüler tavsiye] sizi olduğunuz yere hapsediyor.

Ya inandığınız [yaygın inanç] aslında büyümenizi öldürüyorsa?

Sorun Algoritma değil, sorun [beklenmedik gerçek/sizin içeriğiniz].

Kimse içerik üreticilerine bunu söylemeye cesaret edemiyor ama [popüler alışkanlık] yapmayı bırakmalısınız.

Viral olmak zorunda değilsiniz. Sizin asıl [Gerçek ihtiyaç]’a ihtiyacınız var.

[Yaygın taktik] yapmayı bıraktım ve asıl o zaman büyümeye başladım.

Eğer derdiniz [değer] üretmekse, viral olmak aslında kötü olabilir.

Eğer bugün her şeye yeniden başlasaydım, [yaygın tavsiye]’yi tamamen görmezden gelirdim.

[Yaygın strateji] neden bu kadar abartılıyor? (Ve bunun yerine ne yapmalı?)

Kimsenin daha fazla [kaynak/araç]’a ihtiyacı yok, daha fazla [gerçek]’e ihtiyacı var.

Daha fazla içerik üretmek sorununuzu çözmez. Ama bu çözer.

Size sürekli [eylem yapma]’nız söylendiğini biliyorum ama işte gerçekten işe yarayan yöntem.

Tıkalı kalmanızın nedeni [harici bahane] değil. Asıl neden [içsel gerçek].

Çoğu içerik üreticisi [metrik]’e odaklanır, zeki olanlar ise [gerçek itici güç]’e odaklanır.

Daha fazla stratejiye ihtiyacınız yok, ihtiyacınız olan [beklenmedik zihniyet değişikliği].

Shadowban (gölge yasak) yemediniz, sadece [gerçek açıklama].

İşte [popüler hedef]’i kovalamayı neden bıraktım?

Eğer bunu yanlış yapıyorsanız, her gün paylaşım yapmak çözüm değil.

Eğer içeriğiniz işe yaramıyorsa, sorun içerik değildir. Sorun [daha derin mesele]’dir.

Beni aylarca yerimde saydıran o meşhur tavsiye…

Motivasyona ihtiyacınız yok, [doğru alternatif]’e ihtiyacınız var.

"Bizden biri" olmak > Uzman olmak.

Tutarlı olmak zorunda değilsiniz. [Daha iyi alternatif] olmanız gerekiyor.

(TIPS & VALUE HOOKS - Hızlı kazanımlar ve İpuçları için)

Bana sadece [süre] saniye verin, size [sonuç]’a nasıl ulaşacağınızı göstereyim.

Eğer [hedef kitle grubu]’ndaysanız ve hedefiniz [sonuç] ise, izlemeniz gereken [sayı] adım tam olarak burada.

Son [zaman aralığı] içinde [anahtar alışkanlık] edindim ve [sonuç]’a ulaştım. İşte çıkardığım ders.

[Hedef]’e ulaşamıyorsunuz, çünkü [eksik unsur]’a sahip değilsiniz.

İşte [zaman aralığı]’nda [sonuç] almayı başarmak için yaptığım [sayı] şey.

Önümüzdeki [zaman aralığı]’nda [hedef]’e ulaşmak istiyorsanız, bu [strateji/çerçeve]’yi adım adım uygulayın.

Şu tek şeyi yapana kadar sakın [eylem yapma] işine girmeyin.

[İçeriğimin/kariyerimin] performansında en büyük farkı yaratan şey bu oldu.

Bu video, [hayalinizin/hedefinizin/fikrinizin] aslında hiç de saçma olmadığına dair size bir hatırlatma.

Eğer [sonuç] alamıyorsanız, bunun tek nedeni henüz bir [sistem] kurmamış olmanızdır.

Herkes [sonuç] istiyor, ama kimse işin [zor kısım]’ını yapmak istemiyor.

İşte [sonuç] almak için kullandığım o formülün tamamı.

[Acı noktası/sorun] hakkında kimsenin konuşmadığı detay bu.

Bu küçücük değişiklik, [yaygın sorun] yaşamadan [sonuç] almama yardımcı oldu.

İşte [zaman aralığı]’nda [sonucu] iyileştirmek için kanıtlanmış [sayı] strateji.

Bunda uzmanlaşmak için [süre] harcadım, size ise bir dakikadan kısa sürede özetliyorum.

[Hedef kitle grubu]’nun yaptığı en büyük hata, ısrarla [yaygın hata] yapmalarıdır.

İşte [sorumluluk/iş] ile uğraşırken aynı zamanda [X sonuca] nasıl ulaştım?

İşte size kimsenin söylemediği [konu] hakkındaki o gerçek.

Mükemmel [araç/strateji/sistem] yoktur ama inanın bu ona çok yakın.

Eğer [yaygın problem] ile boğuşuyorsanız, bu video tam size göre.

[Konu]’yu yıllardır inceliyorum, işte öğrendiğim en önemli şeyler.

İşte [yaygın engel]’e takılmadan [hedefe] nasıl ulaşırsınız?

İşte henüz denemediğiniz ama [sonuç] getirecek [sayı] yol.

[Nişiniz] için bilmek yasa dışı gibi hissettiren o web siteleri…

[Basit zaman aralığı] içinde [yaygın hata] yapmayı nasıl bırakırsınız?

[Aktivite] yaparken hala bu [sayı] hatayı mı yapıyorsunuz?

[Yaygın eylem]’in neden işe yaramadığına dair şok edici o sebep…

[Kısa süre] içinde [önemli konu] hakkında bilmeniz gereken her şey.

[Yaygın görev]’i yanlış yapıyorsunuz, işte doğrusu.

(PROOF & TRANSFORMATION HOOKS - Sonuçlar ve Güven inşası için)

Şu anda [etkileyici sonuç]’a ulaştım ama buzdağının görünmeyen yüzünde bu var.

[Dönüşüm]’den önce, ben de [mücadele eden haliniz] gibiydim.

Yaptığım bu tek küçük değişiklik, [açık, ölçülebilir sonuç] almamı sağladı.

İşte [eylem]’in benim için yaptıklarının öncesi ve sonrası.

Gerçek şu ki, [sonuç] öyle bir gecede olmadı.

İşte [X gün] boyunca istikrarlı şekilde [eylem] yaptığımda olanlar.

Tam olarak [acı noktası]’ndan [başarı]’ya nasıl geçtim? Adım adım anlatıyorum.

Yıllarca [yanlış alışkanlık] yapıyordum, işte her şeyi değiştiren o an.

[Zaman aralığı]’nda [düşük metrik]’ten [yüksek metrik]’e nasıl çıktım? İşte yaptıklarım.

Beni [mücadele/dipten] alıp [başarı/zirveye] taşıyan içerik stratejisi bu.

Bu tek video benim için her şeyi değiştirdi, işte nedeni.

[Yöntem]’in işe yaradığına dair kanıt mı istiyorsunuz? İşte benim sonuçlarım.

Eski içeriğim ile yeni içeriğim arasındaki fark mı? Sadece bu tek değişim.

[Eylem] yapmaya başlamadan önce, sonuçlarım tam olarak böyle görünüyordu…

İşte [araç/sistem]’i [X] noktasından [Y] noktasına gelmek için nasıl kullandım?

Benim için her şeyi değiştiren şey [popüler taktik] değildi, asıl olay [gerçek şey]’di.

[Alışkanlık/araç]’ın benim için yarattığı farkı görmek için sola kaydırın.

[X metrik] büyüme aslında grafikte böyle görünüyor.

[X ay] önce, [acı noktası] yaşıyordum. Bugün mü? İşte geldiğim nokta.

Eskiden [sınırlayıcı alışkanlık] yapardım. Şimdi [güçlendirici alışkanlık] yapıyorum ve sonuçlar ortada.

[Basit eylem]’den gelen gerçek sonuçlar… İşte ne değişti?

İşte benimle [X hafta/ay] çalışmak aslında neye benziyor?

İlk [reel/video]’m ile en sonuncusu… Aradaki farka bakın.

Eskiden [X sonuç] alıyordum. Şimdi mi? [Y sonuç].

[Kötü alışkanlık] yapmayı bıraktığımda, olanlar oldu.

İşte [taktik/sistem/test]’ten gelen veriler. Rakamlar yalan söylemez, işe yarıyor.

Şimdiki içeriğim ile 6 ay önceki içeriğim… Bu değişim her şeyi başlattı.

Bu ekran görüntüleri, neden bu işi yaptığımın kanıtı.

İstikrarın sadece kitlenizi büyütmekle kalmayıp, sizi de değiştirdiğinin kanıtı.

[Sonuç]’un neye benzediğini görmek ister misiniz? Size göstereyim.

(CALL-OUT HOOKS - Doğrudan Hedef Kitleye Seslenme)

Eğer [belirli bir kişi] iseniz ve [acı/sorun] ile mücadele ediyorsanız, bu içerik sizin için.

Bu video, [yaygın hayal kırıklığı]’ndan bıkmış herkes için.

Her şeyi "doğru" yapmış ama hala tıkalı hisseden [kimlik]’e sesleniyorum…

Eğer [tekrarlayan döngü]’den yorulduysanız, bunu mutlaka izleyin.

Çok çalışıyorsunuz ama sonuçlar çabayla eşleşmiyor mu? İşte nedeni.

Eğer içeriğiniz dönüşüm getirmiyor gibi geliyorsa, muhtemelen bunu kaçırıyorsunuz.

Eğer "başkaları ne der" korkusuyla kamera karşısına geçemiyorsanız, beni iyi dinleyin.

Bu, artık küçük oynamayı bırakmaya hazır olan [kimlik] için.

Çok uzun süre sessiz kaldınız. Artık o videoyu yayınlama zamanı.

Şu anda kendinizden şüphe ediyorsanız, size bir çift lafım var.

‘Hiçbir şey işe yaramıyor’ aşamasında sıkışıp kalmış her içerik üreticisi için… Bu sizin dönüm noktanız olabilir.

Bu, harika fikirleri olan ama hala paylaşım yapmayan o kişi için.

Her şeyi doğru yapıyorsunuz, sadece bu TEK şeyi atlıyorsunuz.

Utanıp sıkılmadan para kazanmak isteyen içerik üreticileri, bu sizin için.

Bu, her şeyi tek başına yapmaya çalışan "tek kişilik dev kadrolar" için.

Eğer içerik üretmek yerine sürekli izlemeye devam ediyorsanız, tıkalı kalmanızın nedeni budur.

Tükenmiş içerik üreticisine not: Ben de tam sizin olduğunuz yerdeydim.

Eğer tüketmeyi bırakıp üretmeye hazırsanız, hadi başlayalım.

Tembel değilsiniz, sadece net bir sisteminiz yok.

Algoritmayı suçlamayı bırakın. İşte kontrol edebileceğiniz şeyler.

Gerçek bir kitle büyütmek istiyorsanız, bunu yapmayı derhal bırakın.

Hey mükemmeliyetçi dostum, bu video senin için.

Bu, “Ne yayınlayacağımı bilmiyorum” diye kıvranan herkes için.

İşe yaramayan tavsiyelerden gına geldiyse, bu yöntem işe yarayacak.

Çevrimiçi dünyada "garantici" oynuyorsanız, bu sizin uyanma çağrınız.

Eğer içeriğiniz hak ettiği değeri görmüyorsa, muhtemelen sebebi bu.

Momentuma sadece bir video uzaktasınız, şimdi sakın bırakmayın.

Paylaşıp paylaşıp silen içerik üreticileri, bunu yapmayı bırakın.

İhtiyacınız olan her şeye zaten sahipsiniz, tek eksiğiniz bu zihniyet değişikliği.

Eğer kimse size bunu son zamanlarda söylemediyse hatırlatayım: Geride kalmadınız, her şey yolunda. """

BUILD_UP_LIBRARY = """ (PAIN - Acı Noktası ile Bağ Kurma)

Birçok [hedef kitle tipi] bununla boğuşuyor ama farkında bile değiller, izin verin açıklayayım.

Eğer siz de [problem] ile mücadele ediyorsanız, bu size tanıdık gelecektir. İşte bunun sebebi...

Eskiden ben de aynı dertten muzdariptim, hatta bu beni delirtiyordu. Sonra her şeyi değiştiren o şeyi buldum.

Her şeyi doğru yaparken hala yerinde saymak çok sinir bozucu, biliyorum. Genelde işlerin ters gittiği nokta şurası...

Bu, gördüğüm en yaygın hatalardan biri ve insanlara her gün zaman kaybettiriyor. Size bundan nasıl kaçınacağınızı göstereyim.

Eğer [acı noktası] sizi geri tutuyor gibi hissediyorsanız, yalnız değilsiniz. İşte bana yardımcı olan şey.

[Sonuç]’unuzun iyileşmemesinin nedeni bu olabilir. İşte benim öğrendiğim ders.

Pek çok insanın burada tıkanıp kaldığını gördüm. Size bunun neden olduğunu göstereyim.

Siz de bu hatayı yapıyor olabilirsiniz, gözden kaçırması çok kolay. İzin verin açıklayayım.

Bunu çözmem çok uzun sürdü. Aynısını yaşayıp zaman kaybetmeyin diye paylaşıyorum.

(PROMISE - Faydayı Öne Çıkarma/Vaat)

Bunu düzeltmenin basit bir yolu var ve sandığınızdan çok daha kısa sürüyor. Göstereyim.

Bu küçük değişiklik benim için büyük fark yarattı, eminim size de yardımcı olacak. İşte nasıl yapıldığı...

Bunu denediğim anda taşlar yerine oturmaya başladı. Açıklayayım.

Eğer bir dakika beklerseniz, benim için gerçekten neyin işe yaradığını göstereceğim.

Bu hayatımı o kadar kolaylaştırdı ki... Keşke daha önce bilseydim. Hadi detaylara girelim.

Fazla düşünmenize gerek yok, ihtiyacınız olan tek değişim bu. İşte çalışma mantığı...

İnsanların anlattığından çok daha basit. Size ne yaptığımı göstereyim.

Bunu başkalarıyla da paylaştım ve onlar da sonuç aldı. İşte o yöntem.

Ne kadar kolay olduğunu gördüğünüzde muhtemelen hemen denemek isteyeceksiniz. Gelin parçalara ayıralım.

Bu şaşırtıcı derecede iyi çalışıyor ama çoğu insan bunu atlıyor. İşte artık benim atlamamamın nedeni.

(PROOF - Güven İnşa Etme/Kanıt)

Bunu denedim ve sadece birkaç gün içinde sonuçları gördüm. İşte yaptığım şey.

Beni [öncesi] durumundan [sonrası] durumuna getiren şey tam olarak buydu. Size süreci anlatayım.

Pahalı ekipman yok, büyük bir ekip yok... Farkı yaratan tek şey buydu. İşte o yöntem.

Hiçbir şey işe yaramazken bu yöntem imdadıma yetişti. Size göstereyim.

Bunu başkalarıyla paylaştım ve onlar da harika sonuçlar aldı. İşte nedeni.

Bunu hala her gün kullanıyorum ve [sonuç] alabilmemin en büyük nedeni bu. Hadi inceleyelim.

Bunu defalarca yaptım ve her seferinde işe yarıyor. İşte şuna benziyor...

Kulağa çok basit geldiğini biliyorum ama bu bana gerçekten yardımcı oldu. Açıklayayım.

Bu tek değişiklik beklediğimden çok daha iyi sonuçlar verdi. İşte işe yaramasının nedeni.

Geçtiğimiz [zaman aralığı] içinde [sayı] takipçi kazanmamın nedeni bu. İşte sebebi. """

STORYTELLING_FORMATS = """ FORMAT 1: EĞİTİCİ REELS (Educational) İpuçları, eğitimler (tutorial) ve öğretici içerikler için bunu kullan. Yapı:

Sahneyi Kur: Normal/rutin bir anı veya durumu tanıt.

Yanlış İnanç/Hata: O anda neyi yanlış yapıyordunuz? (Sorunu belirle).

Aydınlanma Anı (Epiphany): Bakış açını değiştiren o dönüm noktası.

Ders/İçgörü: Anahtar çıkarım (Değer önerisi).

Eylem Adımları: İzleyicinin hemen uygulayabileceği 1-3 somut adım.

FORMAT 2: DÖNÜŞÜM HİKAYESİ (Transformation) Öncesi & Sonrası (Before & After) sonuçlarını göstermek için kullan. Yapı:

Değişim Öncesi (Before): Hayal kırıklığı, eski durum, dip nokta.

Kırılma Anı (Trigger): "Artık yeter" dediğin veya değişime karar verdiğin o an.

Yolculuk (Journey): Süreç, karşılaşılan engeller ve kazanılan küçük zaferler.

Değişim Sonrası (After): Yeni gerçeklik, sonuçlar ve ulaşılan hedef.

Ders/Cesaretlendirme: "Ben yaptıysam sen de yaparsın" mesajı.

FORMAT 3: SAMİMİ İTİRAF (Vulnerable Confession) Kusurlar ve hatalar üzerinden derin bağ kurmak için kullan. Yapı:

İtiraf Beyanı: Hatayı, kusuru veya utandığın şeyi direkt söyle.

Duygu Durumu: Neden böyle hissettin? (Seni buna iten inanç/korku).

Değişim: Bakış açını değiştiren o farkındalık anı.

Yeni Zihniyet: Şu an sahip olduğun güçlendirici inanç.

Teşvik: İzleyiciyi de aynısını yapmaya (kendini affetmeye/değişmeye) davet et.

FORMAT 4: SÜREÇ GÜNLÜĞÜ (Work in Progress) İzleyicinin kendini sürecin içinde hissetmesi için kullan ("Build in public"). Yapı:

Ortamı Kur: Şu an üzerinde çalıştığın proje veya hedef ne?

Şeffaflık (Reality Check): İşin iyi ve kötü yanları, şu anki zorluklar.

Öğrendiklerin: Şimdiye kadar çıkardığın dersler.

İlerleme: Küçük de olsa katettiğin yol.

Katılım: İzleyiciye soru sor (Fikirlerini al).

FORMAT 5: AYNA TEKNİĞİ (Empati / Mirror Story) İzleyiciye "Beni anlatıyor!" dedirtmek için kullan. Yapı:

Tanıdık Duygu: "Şu hissi bilirsiniz..." (Ortak bir acıdan gir).

İçsel Diyalog: Onların kafalarındaki sesleri/şüpheleri seslendir.

Özdeşleşme: "Ben de tam olarak oradaydım" diyerek bağ kur.

Yansıma/Küçük Değişim: Yeni bir bakış açısı sun (Büyük bir çözüm şart değil, farkındalık yeterli). """

# --- SYSTEM PROMPT ---

SYSTEM_PROMPT_BASE = """
Sen uzman bir Viral Reels Metin Yazarı yapay zekasısın.
Görevin, kullanıcının verdiği "Taslak Metni" (Draft Text) almak ve aşağıdaki özel "Müşteri Persona Verileri"ni kullanarak onu viral potansiyeli yüksek bir senaryoya dönüştürmektir.
ÇIKTI TALİMATLARI (UYGULAMA PROTOKOLÜ)
ANALİZ ET: Aşağıdaki <INPUT_DATA> (Girdi Verisi) kısmını oku. Müşteri Personasını ve Taslak Metni analiz ederek en iyi içerik açısını (angle) belirle.

KANCA (HOOK) SEÇ: Konuya en uygun şablonu <HOOK_LIBRARY> içinden SEÇ.

GELİŞME (BUILD-UP) SEÇ: Kancayı ana konuya bağlayan en iyi köprüyü <BUILD_UP_LIBRARY> içinden seç.

ANA GÖVDEYİ (CORE) YAZ:

Girdi türüne göre <STORYTELLING_FORMATS> içinden uygun formatı kullan.

CTA (ÇAĞRI) EKLE: Net bir Harekete Geçirici Mesaj ekle.

YÖNETMEN VE ÇEKİM NOTLARI: Görsel/işitsel talimatları sadece ilgili "Notlar" kutusuna yaz.

DİL: Nihai senaryoyu TÜRKÇE yaz.

KRİTİK KURALLAR (KESİNLİKLE UYULACAK):
TEMİZ METİN KURALI: [Senaryo Metni] kısımlarında SADECE ve SADECE seslendirilecek/okunacak kelimeler yer almalıdır.

YASAKLAR: Ana metin içinde asla (KANCA), [Gülümseyerek], (Sahne 1) gibi parantez içi ifadeler, etiketler veya emojiler KULLANMA. Bu talimatların hepsi alttaki "Çekim Notları" kutusunda olmalıdır.

FORMAT: Notlar kısımlarını Markdown blockquote (>) formatında yaz ki kutucuk içinde görünsün.

NİHAİ ÇIKTI FORMATI:

HOOK (KANCA)
[Sadece okunacak temiz metin buraya]

🎬 ÇEKİM & GÖRSEL NOTLARI: [Görsel: Yüze ani zoom, Ses: Heyecanlı ton, Oyuncu: Kameraya enerjik döner]

BUILD UP (GELİŞME)
[Sadece okunacak temiz metin buraya]

🎬 ÇEKİM & GÖRSEL NOTLARI: [Görsel: B-roll görüntü girer, Ses: Sakinleşen ton]

CORE (ANA GÖVDE)
[Sadece okunacak temiz metin buraya]

🎬 ÇEKİM & GÖRSEL NOTLARI: [Görsel: Ekranda maddeler belirir, Ses: Bilgilendirici ton]

CTA (ÇAĞRI)
[Sadece okunacak temiz metin buraya]

🎬 ÇEKİM & GÖRSEL NOTLARI: [Görsel: Aşağıyı işaret et, Ses: Davetkar ton]

CAPTION (AÇIKLAMA)
[Başlık] [Gövde] [CTA] [Etiketler]

GİRDİ VERİSİ (DOKUNMA)
Client Persona Data: {{ $json.client_persona_data }} Main Offer: {{ $json.client_persona_data.main_offer }} 

--- KNOWLEDGE BASES ---
<HOOK_LIBRARY>
{hook_library}
</HOOK_LIBRARY>

<BUILD_UP_LIBRARY>
{buildup_library}
</BUILD_UP_LIBRARY>

<STORYTELLING_FORMATS>
{storytelling_formats}
</STORYTELLING_FORMATS>
"""

# Inject libraries into the prompt
SYSTEM_PROMPT = SYSTEM_PROMPT_BASE.format(
    hook_library=HOOK_LIBRARY,
    buildup_library=BUILD_UP_LIBRARY,
    storytelling_formats=STORYTELLING_FORMATS
)

VIRAL_ANALYSIS_PROMPT = """
Sen Acımasız bir Sosyal Medya Denetçisisin (Auditor).
Görevin, aşağıdaki senaryoyu viral potansiyeline göre ELEŞTİRMEK.
Kibar OLMA. Objektif ol ve verilere odaklan.

Senaryo:
{script_text}

Hedef Persona:
{client_persona_data}

Değerlendirme Kriterleri:
1. **Kanca Gücü (0-10):** İlk 3 saniyede kaydırmayı durduruyor mu?
2. **Değer/Karşılık (0-10):** Ana mesaj net ve izleyiciye bir fayda sağlıyor mu?
3. **İzlenme Süresi (0-10):** Akış hızı iyi mi? Gereksiz laf kalabalığı (fluff) var mı?
4. **CTA Netliği (0-10):** Bir sonraki adım bariz mi?

ÇIKTI FORMATI (KESİNLİKLE JSON OLMALIDIR):
Aşağıdaki JSON formatını birebir kullan. Markdown veya başka bir metin ekleme.

{{
    "overall_score": (0-100 arası puan),
    "improvement_tip": "Tek cümlelik en önemli düzeltme önerisi",
    "hook": {{
        "score": (0-10 arası),
        "reason": "Kanca neden iyi veya kötü?"
    }},
    "retention": {{
        "score": (0-10 arası),
        "reason": "İzleyiciyi tutma potansiyeli analizi"
    }},
    "conversion": {{
        "score": (0-10 arası),
        "reason": "CTA ve dönüşüm potansiyeli analizi"
    }}
}}

ÖNEMLİ: Sadece JSON döndür.
"""

ACADEMY_CONTENT = { "hooks": { "Merak Uyandıranlar": [ "Bunu yapmayı bıraktığımda hayatım değişti...", "Sana kimsenin söylemediği o sır...", "Bunu izlemeden sakın [Eylem] işine girme..." ], "Doğrudan Fayda": [ "3 basit adımda nasıl [Sonuç] alırsın?", "İşte [Hedef]e ulaşmanın en kestirme yolu...", "[Süre] içinde [Sonuç] garantili yöntem." ], "Aykırı / Ezber Bozan (Contrarian)": [ "Herkes [X] diyor ama aslında olay [Y]...", "[Popüler Yöntem] aslında tam bir zaman kaybı.", "Neden [X] yapmayı derhal bırakmalısın?" ] }, "structures": { "Eğitici Reels": "1. Kanca (Sorunu Vur)\n2. Merak (Çözüm Var)\n3. Bilgi (Madde 1-2-3)\n4. Çağrı (Kaydet Lazım Olur)", "Dönüşüm Hikayesi": "1. Eski Hal (Before)\n2. Kırılma Anı (Trigger)\n3. Mücadele (Yolculuk)\n4. Yeni Hal (After)\n5. Çağrı (CTA)", "Samimi İtiraf": "1. Hata (Neyi yanlış yaptım?)\n2. Duygu (Nasıl hissettirdi?)\n3. Ders (Ne öğrendim?)\n4. Öneri (Sen yapma)" }, "filming_tips": [ "💡 Işık: Pencereyi mutlaka karşına al, arkana değil. Yüzün aydınlık olsun.", "🎤 Ses: Mikrofonun yoksa telefonu ağzına biraz daha yakın tut veya kulaklık mikrofonu kullan.", "👁️ Göz Teması: Ekranda kendine değil, kameranın o küçük lensine bak.", "⚡ Enerji: Normal hayatta konuştuğundan %20 daha yüksek bir enerjiyle konuş, videoda normal duracaktır." ] }
