from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Category, Comment, Like, Post, Tag

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with rich demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))

        Like.objects.all().delete()
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(username__in=['demo_author', 'ola_dev', 'marek_travel', 'ania_culture']).delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing demo content'))

        categories_data = [
            ('Technologia', 'technologia'),
            ('Programowanie', 'programowanie'),
            ('Życie', 'zycie'),
            ('Podróże', 'podroze'),
            ('Książki', 'ksiazki'),
            ('Filmy', 'filmy'),
            ('Gaming', 'gaming'),
            ('Praca', 'praca'),
        ]
        categories = {
            slug: Category.objects.create(name=name, slug=slug)
            for name, slug in categories_data
        }

        tags_data = [
            'python', 'django', 'frontend', 'react', 'api', 'ai', 'produktywnosc',
            'remote-work', 'podroze', 'city-break', 'czytanie', 'recenzje',
            'kino', 'seriale', 'gaming', 'pc', 'indie', 'lifestyle', 'startup',
            'architektura', 'testy', 'sqlite', 'javascript', 'roadtrip', 'technologia',
        ]
        tags = {
            name: Tag.objects.create(name=name, slug=name)
            for name in tags_data
        }

        authors_data = [
            {
                'username': 'demo_author',
                'email': 'demo@example.com',
                'password': 'DemoAuthor123',
                'avatar': '',
                'bio': 'Backend developer, który lubi budować małe produkty w Django i dopinać je pod demo.',
                'website': 'https://demo-author.dev',
                'location': 'Warszawa',
            },
            {
                'username': 'ola_dev',
                'email': 'ola@example.com',
                'password': 'OlaDev123',
                'avatar': '',
                'bio': 'Pisze o frontendzie, produktywności i tym, jak projekt wygląda od strony użytkownika.',
                'website': 'https://oladev.example.com',
                'location': 'Krakow',
            },
            {
                'username': 'marek_travel',
                'email': 'marek@example.com',
                'password': 'MarekTravel123',
                'avatar': '',
                'bio': 'Laczy blogowanie o podrozach z technologia i lubi testowac rzeczy w praktyce.',
                'website': 'https://marektravel.example.com',
                'location': 'Gdansk',
            },
            {
                'username': 'ania_culture',
                'email': 'ania@example.com',
                'password': 'AniaCulture123',
                'avatar': '',
                'bio': 'Czyta, oglada i wybiera z kultury to, co faktycznie warto polecic dalej.',
                'website': 'https://aniaculture.example.com',
                'location': 'Wroclaw',
            },
        ]
        authors = []
        for author_data in authors_data:
            user = User.objects.create_user(
                username=author_data['username'],
                email=author_data['email'],
                password=author_data['password'],
            )
            user.profile.avatar = author_data['avatar']
            user.profile.bio = author_data['bio']
            user.profile.website = author_data['website']
            user.profile.location = author_data['location']
            user.profile.save()
            authors.append(user)

        image_urls = [
            'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=1200&q=80',
            'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80',
            'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80',
            'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80',
            'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=1200&q=80',
            'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1200&q=80',
            'https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1200&q=80',
            'https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1200&q=80',
        ]

        posts_blueprint = {
            'technologia': [
                ('AI w małych firmach: gdzie naprawdę oszczędza czas', ['ai', 'startup', 'produktywnosc']),
                ('5 trendów technologicznych, które warto śledzić w 2026', ['ai', 'frontend', 'api']),
                ('Czy lokalne modele AI mają sens na domowym sprzęcie?', ['ai', 'pc', 'technologia']),
            ],
            'programowanie': [
                ('Django po godzinach: jak szybko postawić projekt na demo', ['python', 'django', 'sqlite']),
                ('Testy integracyjne w Django bez chaosu w kodzie', ['python', 'django', 'testy']),
                ('React i Django: prosty podział odpowiedzialności w projekcie', ['react', 'django', 'javascript']),
            ],
            'zycie': [
                ('Małe rytuały, które porządkują dzień developera', ['lifestyle', 'produktywnosc', 'remote-work']),
                ('Jak nie spalić się zawodowo przy pracy nad własnym projektem', ['lifestyle', 'startup', 'produktywnosc']),
                ('Weekend offline: co daje odcięcie od ekranu na 48 godzin', ['lifestyle', 'czytanie', 'podroze']),
            ],
            'podroze': [
                ('City break w Porto: plan na 3 dni bez pośpiechu', ['podroze', 'city-break', 'roadtrip']),
                ('Jak pakuję się na 7 dni tylko z bagażem podręcznym', ['podroze', 'lifestyle', 'city-break']),
                ('Mazury poza sezonem: spokojny roadtrip po Polsce', ['podroze', 'roadtrip', 'lifestyle']),
            ],
            'ksiazki': [
                ('3 książki o produktywności, do których naprawdę wracam', ['czytanie', 'recenzje', 'produktywnosc']),
                ('Najciekawsze reportaże, które przeczytałem tej zimy', ['czytanie', 'recenzje', 'lifestyle']),
                ('Książki techniczne, które pomagają pisać prostszy kod', ['czytanie', 'python', 'django']),
            ],
            'filmy': [
                ('Najciekawsze premiery filmowe na spokojny wieczór', ['kino', 'recenzje', 'seriale']),
                ('Filmy science fiction, które dobrze się zestarzały', ['kino', 'ai', 'recenzje']),
                ('Seriale, które warto nadrobić w jeden weekend', ['seriale', 'kino', 'lifestyle']),
            ],
            'gaming': [
                ('Indie gry, które zrobiły na mnie większe wrażenie niż AAA', ['gaming', 'indie', 'pc']),
                ('Setup do grania i pracy przy jednym biurku', ['gaming', 'pc', 'produktywnosc']),
                ('Gry na 20 minut dziennie, kiedy nie masz czasu', ['gaming', 'indie', 'lifestyle']),
            ],
            'praca': [
                ('Remote work bez chaosu: mój tygodniowy system pracy', ['remote-work', 'produktywnosc', 'startup']),
                ('Jak prowadzić krótkie spotkania, które mają sens', ['remote-work', 'produktywnosc', 'lifestyle']),
                ('Czego szukam w ofertach pracy jako backend developer', ['startup', 'python', 'remote-work']),
            ],
        }

        article_bodies = {
            'AI w małych firmach: gdzie naprawdę oszczędza czas': "Największy błąd, jaki małe firmy popełniają przy wdrażaniu AI, polega na szukaniu spektakularnych use case'ów zanim uporządkują codzienną pracę. W praktyce największy zwrot pojawia się tam, gdzie zespół i tak wykonuje powtarzalne czynności: odpowiada na podobne pytania klientów, przygotowuje opisy ofert, porządkuje notatki po spotkaniach albo streszcza długie dokumenty.\n\nDobrze działa podejście etapowe. Najpierw warto policzyć, ile czasu kosztują ręczne zadania wykonywane co tydzień. Potem wybrać jedno z nich i sprawdzić, czy model potrafi skrócić pracę o 30-40 procent bez pogorszenia jakości. Taki eksperyment można przeprowadzić w marketingu, sprzedaży albo supportcie bez dużych inwestycji infrastrukturalnych.\n\nDrugim obszarem, który często daje szybki efekt, jest praca z wiedzą wewnętrzną. Jeśli firma ma rozproszone procedury w mailach, Slacku i dokumentach, nawet prosty chatbot oparty o własną bazę materiałów potrafi odciążyć bardziej doświadczonych pracowników. Kluczowe jest jednak to, by nie traktować odpowiedzi modelu jako ostatecznej prawdy, tylko jako pierwszy szkic lub podpowiedź.\n\nAI nie zastępuje procesu, tylko go uwypukla. Jeżeli dane wejściowe są chaotyczne, a odpowiedzialność za decyzje nie jest jasno przypisana, automatyzacja tylko przyspieszy bałagan. W małej firmie lepiej wygrać trzema nudnymi usprawnieniami niż jednym efektownym demo, które po tygodniu nikt nie otwiera.",
            '5 trendów technologicznych, które warto śledzić w 2026': "Rok 2026 nie zapowiada się jako czas jednej rewolucji, tylko raczej dojrzewania kilku kierunków naraz. Pierwszy z nich to dalsza specjalizacja narzędzi AI. Zamiast uniwersalnych modeli do wszystkiego, coraz częściej pojawiają się produkty wyspecjalizowane pod konkretne procesy: analizę umów, planowanie kampanii, review kodu czy wsparcie helpdesku.\n\nDrugi trend to przesunięcie części obliczeń bliżej użytkownika. Lokalne modele, edge computing i lżejsze pipeline'y stają się atrakcyjne nie tylko ze względu na prywatność, ale też na koszty. Firmy zaczynają zadawać bardziej praktyczne pytania: czy naprawdę potrzebujemy wywoływać ciężkie API przy każdym zadaniu i czy możemy utrzymać część funkcji offline.\n\nTrzeci kierunek dotyczy frontendów. Interfejsy są coraz bardziej reaktywne, ale jednocześnie rośnie oczekiwanie, że będą prostsze w utrzymaniu. Dlatego zyskują podejścia, które ograniczają nadmiar stanu po stronie klienta i przesuwają odpowiedzialność z powrotem na serwer tam, gdzie ma to sens.\n\nCzwarty trend to observability dla mniejszych zespołów. Jeszcze niedawno rozbudowany monitoring kojarzył się głównie z dużą skalą, dziś staje się elementem higieny nawet w niewielkich SaaS-ach. Piąty trend to bezpieczeństwo wbudowane w codzienny workflow: krótszy czas życia sekretów, lepsza segmentacja dostępu i automatyczne skany zależności już na etapie developmentu.",
            'Czy lokalne modele AI mają sens na domowym sprzęcie?': "Lokalne modele AI mają sens wtedy, gdy wiesz, po co je uruchamiasz. Jeśli celem jest nauka, prywatność danych albo szybkie eksperymenty bez kosztu za każde zapytanie, domowy sprzęt bywa wystarczający. Do prostego streszczania tekstu, klasyfikacji notatek czy generowania krótkich szkiców nie zawsze potrzebujesz infrastruktury chmurowej.\n\nNajwiększe ograniczenie to pamięć i przepustowość. W praktyce doświadczenie zależy bardziej od ilości RAM-u i VRAM-u niż od samego procesora. Na słabszym sprzęcie da się pracować, ale wtedy trzeba wybierać mniejsze modele, korzystać z kwantyzacji i akceptować wolniejsze odpowiedzi. To wciąż bywa użyteczne, jeśli zadanie nie wymaga interakcji w czasie rzeczywistym.\n\nDużą zaletą pracy lokalnej jest przewidywalność. Nikt nie zmieni ci nagle limitów API, nie podniesie cen i nie wyśle danych poza komputer. Dla części osób to argument ważniejszy niż czysta wydajność. Z drugiej strony trzeba pamiętać o kosztach energii, miejscu na dysku oraz czasie potrzebnym na konfigurację narzędzi.\n\nDla większości użytkowników najlepszy model pracy będzie hybrydowy. Lokalny model sprawdzi się do eksperymentów, prywatnych notatek i prostych automatyzacji, a chmura do większych zadań wymagających wyższej jakości albo długiego kontekstu. Kluczowe jest nie to, czy da się uruchomić model lokalnie, tylko czy jego ograniczenia pasują do realnego scenariusza.",
            'Django po godzinach: jak szybko postawić projekt na demo': "Jeśli budujesz projekt na zaliczenie, rozmowę rekrutacyjną albo szybkie demo dla klienta, Django nadal jest jednym z najkrótszych sposobów dojścia od pomysłu do działającej aplikacji. Najwięcej czasu oszczędza to, że framework daje gotowe fundamenty: routing, ORM, formularze, system użytkowników i panel admina.\n\nNajpraktyczniejszy start to bardzo mały zakres. Na początku warto zamknąć się w jednym modelu głównym, kilku relacjach i dwóch lub trzech widokach, które pokazują pełny przepływ: lista, szczegół, tworzenie wpisu. Dopiero kiedy to działa, ma sens dokładanie wyszukiwarki, dashboardu, filtrów czy dodatkowej moderacji.\n\nW projektach demo ogromną przewagą jest seed danych. Pusta aplikacja wygląda jak niedokończony szkic, nawet jeśli kod jest poprawny. Gdy baza startuje z użytkownikami, wpisami, komentarzami i sensownymi treściami, całość od razu sprawia wrażenie bardziej dopracowanej. To samo dotyczy prostego stylowania. Nawet podstawowy Tailwind daje szybko efekt, który pomaga skupić rozmowę na produkcie, a nie na brakach wizualnych.\n\nWarto też pilnować granicy między szybkością a chaosem. Demo nie wymaga od razu pełnej architektury produkcyjnej, ale powinno mieć czytelny układ plików, podstawowe testy i jednoznacznie nazwane widoki. Dzięki temu projekt można potem rozwinąć, zamiast przepisywać od zera po pierwszej prezentacji.",
            'Testy integracyjne w Django bez chaosu w kodzie': "Testy integracyjne w Django są najbardziej przydatne wtedy, gdy obejmują realne przepływy użytkownika, a nie próbują odtwarzać każdej linijki implementacji. Zwykle lepiej sprawdzić, czy zalogowany autor może utworzyć wpis i zobaczyć go pod poprawnym URL-em, niż rozbijać ten scenariusz na kilkanaście drobnych asercji o wewnętrznych detalach formularza.\n\nPierwsza zasada porządku to świadome przygotowanie danych. `setUp` albo proste fabryki powinny tworzyć minimalny zestaw obiektów potrzebnych do danego scenariusza. Im mniej przypadkowych zależności w danych testowych, tym łatwiej zrozumieć, co faktycznie zostało złamane po zmianie kodu.\n\nDruga zasada to rozsądny poziom szczegółowości. Test integracyjny nie powinien wiedzieć wszystkiego o środku widoku. Ma sprawdzić efekt: status odpowiedzi, redirect, zapis do bazy, widoczny komunikat błędu lub ograniczenie uprawnień. Gdy test zaczyna powielać logikę produkcyjną, staje się kruchy i przestaje pełnić rolę ochronną.\n\nTrzecia zasada to grupowanie testów według zachowania, nie plików. Osobny zestaw dla komentarzy, osobny dla autoryzacji, osobny dla zarządzania wpisami daje czytelniejszy obraz niż przypadkowy zbiór metod wrzuconych do jednej klasy. Dobrze utrzymane testy integracyjne nie spowalniają pracy, tylko pozwalają refaktorować bez ciągłego zgadywania, co się właśnie zepsuło.",
            'React i Django: prosty podział odpowiedzialności w projekcie': "Łączenie Reacta z Django ma sens wtedy, gdy każda warstwa ma jasno określoną rolę. Django dobrze sprawdza się jako backend odpowiedzialny za dane, autoryzację, walidację i reguły biznesowe. React jest mocny tam, gdzie interfejs wymaga bardziej dynamicznych interakcji, szybkiego filtrowania, złożonych formularzy albo wielu stanów widoku.\n\nNajwięcej problemów pojawia się wtedy, gdy oba światy próbują robić to samo. Jeśli logika walidacji rozjeżdża się między backendem i frontendem, a routing jest częściowo po stronie serwera i częściowo po stronie SPA bez jasnych zasad, projekt szybko traci spójność. Dlatego warto już na starcie ustalić, czy budujemy klasyczne API plus osobny frontend, czy raczej serwer renderuje większość stron, a React obsługuje tylko wybrane wyspy interakcji.\n\nW mniejszych projektach bardzo dobrze działa wariant pośredni. Django zwraca podstawowe widoki i utrzymuje większość logiki, a React dostaje konkretne moduły, na przykład zaawansowane wyszukiwanie, edytor albo panel z filtrami. Taki układ daje lepszy balans kosztu do korzyści niż pełne SPA wszędzie.\n\nNajprostszy podział odpowiedzialności brzmi tak: dane i zasady po stronie Django, doświadczenie interakcji po stronie Reacta. Gdy ta granica jest jasna, łatwiej utrzymać kod, rozdzielić pracę w zespole i unikać sporów o to, gdzie powinno żyć konkretne zachowanie aplikacji.",
            'Małe rytuały, które porządkują dzień developera': "Produktywność w pracy programisty rzadko zależy od jednego wielkiego systemu. Częściej wygrywają małe rytuały, które porządkują początek dnia i zmniejszają koszt przełączania kontekstu. Najprostszy przykład to pięć minut na zapisanie trzech najważniejszych zadań przed otwarciem komunikatorów. Taki drobiazg ustawia priorytety lepiej niż kolejny rozbudowany planner.\n\nDrugi rytuał to zamykanie pętli po zakończonym bloku pracy. Krótka notatka: co zostało zrobione, co zostało otwarte i od czego zacząć jutro, bardzo obniża próg wejścia przy kolejnym podejściu. Dzięki temu nie tracisz rano energii na odtwarzanie toku myślenia z poprzedniego dnia.\n\nWiele osób lekceważy też wartość prostego resetu między zadaniami. Dwie minuty bez ekranu, krótki spacer po mieszkaniu albo nalanie wody działają lepiej niż próba utrzymania wysokiego skupienia przez cztery godziny bez przerwy. Programowanie jest poznawczo drogie i udawanie, że zmęczenie nie istnieje, zwykle kończy się gorszym kodem.\n\nNajważniejsze jest to, żeby rytuały były lekkie. Jeśli system organizacji sam staje się projektem do utrzymania, przestaje pomagać. Dobra rutyna to taka, której trzymasz się nawet w gorszym tygodniu, bo jest prosta i naprawdę wspiera pracę.",
            'Jak nie spalić się zawodowo przy pracy nad własnym projektem': "Własny projekt potrafi dać dużo satysfakcji, ale równie łatwo zamienia się w źródło chronicznego napięcia. Problem zwykle zaczyna się wtedy, gdy każda wolna godzina ma być produktywna, a odpoczynek zaczyna wyglądać jak zaniedbanie. W takiej konfiguracji nawet ciekawy pomysł po kilku tygodniach zaczyna ciążyć.\n\nPierwsza rzecz, która pomaga, to ograniczenie tempa. Nie każda iteracja musi kończyć się nową funkcją. Czasem wartościowym sprintem jest uporządkowanie backlogu, poprawa testów albo spisanie decyzji architektonicznych. Taki rytm jest mniej widowiskowy, ale dużo bardziej zrównoważony.\n\nDruga rzecz to świadome oddzielenie pracy etatowej od projektu prywatnego. Jeśli po ośmiu godzinach debugowania próbujesz jeszcze codziennie dowieźć kolejne trzy godziny feature'ów, organizm prędzej czy później wystawi rachunek. Lepiej pracować krócej, ale regularnie, niż nakręcać się na zryw, po którym przychodzi całkowity zjazd.\n\nWarto też pilnować sensu projektu. Jeśli cały wysiłek idzie w odtwarzanie cudzych roadmap albo porównywanie się do startupów z większym zespołem, motywacja szybko siada. Własny produkt jest zdrowszy wtedy, gdy odpowiada na realny cel: naukę, portfolio, rozwiązanie konkretnego problemu albo sprawdzenie hipotezy biznesowej.",
            'Weekend offline: co daje odcięcie od ekranu na 48 godzin': "Pomysł dwóch dni bez ekranu może brzmieć jak przesada, zwłaszcza jeśli zawodowo spędzasz większość czasu przy komputerze. W praktyce taki reset działa zaskakująco dobrze, bo przerywa ciągłe bodźce, które na co dzień wydają się neutralne: powiadomienia, szybkie sprawdzanie maila, mimowolne sięganie po telefon między zadaniami.\n\nNajbardziej odczuwalna zmiana pojawia się zwykle drugiego dnia. Głowa przestaje oczekiwać natychmiastowej stymulacji, łatwiej utrzymać uwagę na jednej czynności i wraca bardziej naturalne tempo. Nagle okazuje się, że spacer, książka albo zwykła rozmowa nie potrzebują tła w postaci kolejnego okna przeglądarki.\n\nOffline nie musi oznaczać ascetycznego planu. Chodzi raczej o odzyskanie przestrzeni, w której nic nie walczy o uwagę. Taki weekend daje też dobrą perspektywę na własne nawyki. Po powrocie do komputera szybciej widać, które aplikacje są naprawdę potrzebne, a które tylko wypełniają przerwy.\n\nNie jest to rozwiązanie na każde zmęczenie, ale jako regularny reset działa lepiej, niż się wydaje. Nawet jeśli nie odetniesz się na pełne 48 godzin, już jeden dzień bez ciągłego scrollowania potrafi zauważalnie obniżyć mentalny szum.",
            'City break w Porto: plan na 3 dni bez pośpiechu': "Porto dobrze nadaje się na krótki wyjazd, bo nie wymaga obsesyjnego odhaczania atrakcji. To miasto najlepiej działa wtedy, gdy zostawisz sobie margines na włóczenie się ulicami, kawę w przypadkowym miejscu i dłuższy spacer nad rzeką. Trzy dni wystarczą, żeby zobaczyć sporo, ale bez wrażenia biegu od punktu do punktu.\n\nPierwszy dzień warto przeznaczyć na historyczne centrum i oswojenie rytmu miasta. Spacer przez Ribeirę, wejście na punkt widokowy, późny lunch i zejście nad Douro dają dobry start bez nadmiaru planowania. Porto jest fotogeniczne, ale największy urok robią tam detale: elewacje, małe księgarnie, schody i światło odbijające się od azulejos.\n\nDrugiego dnia dobrze poświęcić więcej czasu na dzielnice poza najbardziej oczywistym szlakiem. Zamiast ścigać listę top 10, lepiej wybrać dwie lub trzy rzeczy i zostawić miejsce na spontaniczność. Miasto sprzyja właśnie takiemu zwiedzaniu, bo nawet zwykła droga między punktami jest częścią doświadczenia.\n\nTrzeci dzień najlepiej zamknąć czymś spokojniejszym: śniadaniem bez pośpiechu, krótkim wejściem do jednego muzeum albo przejazdem w stronę oceanu. Porto wygrywa atmosferą, nie skalą. Jeśli dasz mu trochę czasu, odwdzięcza się bardziej niż wiele większych, głośniejszych kierunków na weekend.",
            'Jak pakuję się na 7 dni tylko z bagażem podręcznym': "Pakowanie na tydzień do małej walizki przestaje być trudne w momencie, gdy przestajesz pakować scenariusze awaryjne na każdą możliwą okazję. Zamiast myśleć kategoriami pojedynczych stylizacji, lepiej zbudować mały zestaw rzeczy, które łączą się między sobą i działają w różnych warunkach.\n\nU mnie punkt wyjścia jest zawsze ten sam: ograniczona paleta kolorów, dwie pary spodni maksymalnie, kilka lekkich warstw i buty, które realnie pasują do planu podróży. Jeśli wiem, że dużo chodzę, nie biorę obuwia „na wszelki wypadek”, które tylko zajmuje miejsce. Największy błąd to pakowanie rzeczy, których normalnie i tak nie nosisz.\n\nDruga zasada to małe pojemniki i dyscyplina w kosmetykach. Naprawdę nie trzeba zabierać połowy łazienki na siedem dni. W większości wyjazdów działa też szybkie pranie jednej lub dwóch rzeczy w trakcie, co od razu zmniejsza objętość bagażu.\n\nBagaż podręczny daje wygodę, bo skraca lotniskową logistykę i zmusza do prostszych decyzji. Po kilku wyjazdach wchodzi z tego rutyna. Zamiast zastanawiać się, czy czegoś zabraknie, zaczynasz bardziej doceniać to, jak mało rzeczy jest faktycznie potrzebnych do komfortowego podróżowania.",
            'Mazury poza sezonem: spokojny roadtrip po Polsce': "Mazury kojarzą się zwykle z latem, tłokiem przy marinach i ruchem na wodzie, ale poza sezonem mają zupełnie inny charakter. Jesienią albo wczesną wiosną region jest cichszy, drogi są luźniejsze, a tempo podróży naturalnie zwalnia. To dobry kierunek dla osób, które chcą odpocząć od miasta bez konieczności organizowania dużej wyprawy.\n\nRoadtrip po Mazurach najlepiej planować luźno. Zamiast codziennie zmieniać nocleg, rozsądniej wybrać jedną lub dwie bazy i robić krótsze trasy po okolicy. Dzięki temu więcej czasu zostaje na miejsca, które trudno zapisać w planie: małe punkty widokowe, puste pomosty, boczne drogi prowadzące przez las i jeziora.\n\nPoza sezonem szczególnie widać, jak mocno ten region działa krajobrazem, a nie tylko atrakcjami. Spacer przy wodzie, kawa wypita z widokiem na mgłę nad jeziorem albo wieczór przy książce w drewnianym domu dają inny rodzaj odpoczynku niż intensywny city break.\n\nMazury nie potrzebują wielkiej narracji. To kierunek, który broni się prostotą. Jeśli szukasz podróży blisko, spokojnie i bez presji „zaliczania”, wyjazd poza sezonem potrafi zaskoczyć bardziej niż niejeden popularny weekendowy kierunek.",
            '3 książki o produktywności, do których naprawdę wracam': "Większość książek o produktywności obiecuje więcej, niż dowozi. Dlatego najbardziej cenię te, do których faktycznie wracam po kilku miesiącach, bo zawierają nie tylko motywujące hasła, ale użyteczne ramy myślenia o pracy. Dobre książki z tego obszaru pomagają uprościć system, a nie rozbudować go do granic absurdu.\n\nPierwszy typ wartościowej lektury to książka, która porządkuje priorytety. Nie chodzi o to, by robić więcej, tylko by rozsądniej decydować, co w ogóle zasługuje na uwagę. Drugi typ to pozycje pokazujące, jak tworzyć środowisko sprzyjające skupieniu: mniej tarcia, mniej przełączania kontekstu, więcej przewidywalnych nawyków. Trzeci typ to książki uczące odpoczynku jako części systemu, a nie nagrody po wszystkim.\n\nZ perspektywy czasu widzę, że najlepsze efekty dają te idee, które da się wdrożyć od razu i bez specjalnej ceremonii. Jedna zmiana w planowaniu tygodnia albo prostszy sposób zamykania zadań daje więcej niż najbardziej efektowna metoda z dwudziestoma etapami.\n\nWarto wracać do takich książek nie po to, by szukać kolejnej rewolucji, ale żeby przypomnieć sobie podstawy. Produktywność działa najlepiej wtedy, gdy jest nudna, stabilna i wspiera realną pracę zamiast stawać się osobnym hobby.",
            'Najciekawsze reportaże, które przeczytałem tej zimy': "Zimą najchętniej czytam reportaże, które nie próbują być tylko zbiorem faktów, ale potrafią zbudować świat i napięcie bez uciekania w fikcję. Dobre reportaże zostają ze mną dłużej niż szybkie nowości, bo uczą patrzeć szerzej: na ludzi, instytucje i codzienne mechanizmy, które zwykle giną w skrótowych komentarzach.\n\nNajbardziej zapamiętałem te książki, które łączyły solidny research z wyczuciem języka. Kiedy autor potrafi pokazać miejsce albo bohatera bez przesadnego ozdobnika, tekst staje się mocniejszy. Ważne jest też tempo. Reportaż nie musi być głośny, żeby był angażujący; czasem wystarczy spokojne prowadzenie czytelnika przez dobrze zebrany materiał.\n\nZimowa lektura sprzyja też wybieraniu książek gęstszych i bardziej wymagających. W dłuższe wieczory łatwiej wejść w tekst, który potrzebuje uwagi, a nie tylko szybkiego przelatywania wzrokiem. Właśnie wtedy najlepiej widać różnicę między reportażem opartym na tezie a reportażem, który zostawia przestrzeń na niejednoznaczność.\n\nJeśli miałbym wskazać wspólny mianownik najlepszych tytułów z ostatnich miesięcy, byłaby to uczciwość wobec czytelnika. Bez taniej sensacji, bez wymuszonego moralizowania, za to z wyraźnym poczuciem, że ktoś wykonał rzetelną pracę i ma coś ważnego do opowiedzenia.",
            'Książki techniczne, które pomagają pisać prostszy kod': "Nie wszystkie książki techniczne starzeją się dobrze. Najbardziej użyteczne okazują się zwykle te, które nie są przywiązane do jednej biblioteki czy mody, tylko uczą prostszego myślenia o projektowaniu kodu. To właśnie do nich warto wracać, gdy projekt zaczyna się rozrastać szybciej niż zrozumienie jego struktury.\n\nDla mnie najcenniejsze są książki, które pokazują koszt nadmiaru abstrakcji. Łatwo zachłysnąć się wzorcami i elastycznością, ale w codziennej pracy prostota wygrywa częściej niż spryt. Dobra lektura techniczna uczy zadawać niewygodne pytania: czy ten podział naprawdę coś upraszcza, czy tylko rozkłada odpowiedzialność na więcej plików.\n\nDruga grupa przydatnych książek dotyczy testów i utrzymania. Pomagają zrozumieć, że czytelność kodu nie kończy się na nazwie funkcji. Liczy się też to, jak łatwo zmienić zachowanie bez lawiny regresji, jak szybko nowa osoba odnajdzie się w projekcie i czy reguły domenowe są widoczne tam, gdzie powinny.\n\nNajlepsze książki techniczne nie sprawiają, że kod staje się bardziej imponujący. Sprawiają, że staje się bardziej oczywisty. A to w dłuższym terminie daje większą przewagę niż większość efektownych trików architektonicznych.",
            'Najciekawsze premiery filmowe na spokojny wieczór': "Nie każdy wieczór potrzebuje filmu, który próbuje być wydarzeniem sezonu. Czasem najbardziej satysfakcjonujące są premiery mniejsze, lepiej napisane i spokojniej prowadzone, które nie opierają całej atrakcyjności na tempie albo zwrotach akcji. Właśnie takie tytuły najczęściej zostają w pamięci dłużej niż najbardziej hałaśliwe blockbustery.\n\nPrzy wyborze filmu na spokojny wieczór szukam przede wszystkim konsekwencji tonu. Jeśli obraz od początku wie, czy chce być kameralnym dramatem, lekką komedią czy subtelnym thrillerem, łatwiej wejść w jego rytm. Dużo mniej interesują mnie produkcje, które za wszelką cenę próbują zmieścić wszystko naraz.\n\nW ostatnich premierach najbardziej doceniam też powrót do solidnego aktorstwa i scenariuszy opartych na relacjach, a nie wyłącznie na koncepcji. To właśnie rozmowy, napięcie między postaciami i dobrze rozpisane drobne konflikty budują film, do którego chce się wrócić.\n\nDobry film na wieczór nie musi zmieniać życia. Wystarczy, że przez dwie godziny utrzyma uwagę, nie traktuje widza protekcjonalnie i zostawia po sobie coś więcej niż poczucie, że właśnie zaliczyłeś kolejny tytuł z listy nowości.",
            'Filmy science fiction, które dobrze się zestarzały': "Science fiction starzeje się dobrze wtedy, gdy nie opiera całej swojej siły na technologicznej powierzchni. Jeśli film ma ciekawy pomysł na człowieka, władzę, pamięć albo relację z maszyną, przetrwa nawet wtedy, gdy część wizualnych przewidywań okaże się nietrafiona. Właśnie dlatego do niektórych klasyków tego gatunku wraca się bez poczucia muzealnej wizyty.\n\nNajbardziej lubię te tytuły, które traktują futurystyczny świat jako narzędzie do zadawania współczesnych pytań. Kiedy technologia jest tłem dla rozmowy o kontroli, samotności, tożsamości albo granicy między wygodą a zależnością, film nie zamyka się w epoce swojego powstania.\n\nDobrze starzeją się też produkcje z mocnym językiem wizualnym. Nawet jeśli efekty specjalne nie robią już takiego wrażenia jak kiedyś, spójna estetyka i odważna scenografia nadal budują świat, który ma własny charakter. To ważniejsze niż perfekcyjna realistyczność każdego detalu.\n\nNajlepsze science fiction po latach nie jest tylko testem trafności przewidywań. To raczej sprawdzian, czy twórcy potrafili powiedzieć coś istotnego o ludzkich wyborach. Jeśli tak, film pozostaje aktualny dużo dłużej niż sama technologia, którą pokazywał.",
            'Seriale, które warto nadrobić w jeden weekend': "Weekendowe nadrabianie serialu ma sens tylko wtedy, gdy historia rzeczywiście wspiera ten sposób oglądania. Najlepiej działają miniseriale albo krótkie sezony, które mają wyraźny rytm i nie rozwlekają fabuły tylko po to, by przedłużyć obecność w katalogu platformy. W takim formacie łatwiej utrzymać emocjonalne zaangażowanie i nie zgubić szczegółów.\n\nSzukam zwykle produkcji, które szybko ustawiają stawkę, ale nie spalają wszystkiego w pierwszym odcinku. Dobry serial na weekend powinien mieć wystarczająco mocny haczyk, by zachęcić do kolejnego epizodu, a jednocześnie zostawiać miejsce na rozwój bohaterów. Sama intryga nie wystarcza, jeśli postaci są tylko nośnikami twistów.\n\nCoraz bardziej cenię też seriale, które wiedzą, kiedy skończyć. Krótsza forma często działa na korzyść całości, bo wymusza precyzję. Mniej wypełniaczy oznacza więcej scen, które faktycznie niosą historię i budują klimat.\n\nJeśli masz dwa wolne wieczory i chcesz obejrzeć coś naprawdę satysfakcjonującego, warto wybierać tytuły domknięte, dobrze napisane i formalnie konsekwentne. Taki serial zostawia poczucie pełnej historii, a nie kolejnej pozycji dodanej do nieskończonej listy do obejrzenia.",
            'Indie gry, które zrobiły na mnie większe wrażenie niż AAA': "Gry indie wygrywają ze sceną AAA nie budżetem, tylko wyrazistością. Kiedy mniejszy zespół ma mocny pomysł na mechanikę, styl wizualny albo nastrój, potrafi zostawić silniejsze wrażenie niż produkcja z ogromną kampanią marketingową i checklistą bezpiecznych rozwiązań. Właśnie dlatego tak wiele niezależnych tytułów pamięta się dłużej.\n\nNajbardziej cenię indie za odwagę w projektowaniu. Te gry częściej pozwalają sobie na dziwność, ciszę, nieoczywisty rytm albo mechanikę, która nie musi podobać się wszystkim. Dzięki temu powstają doświadczenia bardziej osobne, czasem nierówne, ale przynajmniej niezamienne z dziesiątkami innych premier.\n\nDruga przewaga to szacunek do czasu gracza. Wiele świetnych gier niezależnych nie próbuje zatrzymać cię na sto godzin. Zamiast tego daje kilka lub kilkanaście godzin skupionego doświadczenia, które ma początek, rozwinięcie i mocne domknięcie. Taki format bywa dziś wręcz odświeżający.\n\nNie chodzi o to, że AAA nie potrafi dostarczyć dobrych produkcji. Po prostu w segmencie indie łatwiej znaleźć rzeczy bardziej autorskie. Kiedy gra naprawdę ma coś do powiedzenia, skala przestaje być najważniejszym kryterium.",
            'Setup do grania i pracy przy jednym biurku': "Połączenie stanowiska do pracy i grania przy jednym biurku brzmi dobrze, dopóki nie okaże się, że oba scenariusze mają inne potrzeby. Do pracy liczy się ergonomia, porządek i wygoda wielogodzinnego siedzenia. Do grania dochodzą peryferia, dźwięk i często większa tolerancja na wizualny charakter setupu. Da się to pogodzić, ale wymaga kilku świadomych decyzji.\n\nNajważniejszy jest monitor albo zestaw monitorów. To one definiują, czy stanowisko będzie męczyć wzrok, jak dużo miejsca zostanie na biurku i czy przełączanie między zadaniami będzie wygodne. Drugim kluczowym elementem jest krzesło i wysokość blatu. Efektowna klawiatura niewiele pomoże, jeśli po trzech godzinach bolą plecy.\n\nW praktyce najlepiej sprawdza się minimalizm okablowania i kilka stałych stref. Dobrze mieć prosty sposób przełączania audio, miejsce na odstawienie pada albo słuchawek i porządną lampkę, która nie męczy wieczorem. Im mniej drobnych przeszkód w codziennym użyciu, tym bardziej setup działa jako narzędzie, a nie ekspozycja sprzętu.\n\nWspólne biurko do pracy i grania nie musi być kompromisem złej jakości. Przy rozsądnym doborze sprzętu może wręcz ułatwić życie, bo zamiast dublować przestrzeń, budujesz jedno stanowisko, które wspiera oba tryby bez nadmiaru chaosu.",
            'Gry na 20 minut dziennie, kiedy nie masz czasu': "Nie każda gra wymaga długich sesji i pełnego zanurzenia na pół wieczoru. W momentach, gdy dnia praktycznie już nie ma, najbardziej doceniam tytuły, które respektują krótkie okna czasowe. Dobrze zaprojektowana gra na 20 minut potrafi dać satysfakcję bez wrażenia, że uruchamiasz coś, czego i tak nie zdążysz sensownie kontynuować.\n\nNajlepiej sprawdzają się produkcje z krótką, czytelną pętlą rozgrywki. Jedna plansza, jeden run, jedno wyzwanie albo jeden dzień w grze to format, który naturalnie mieści się w napiętym harmonogramie. Ważne jest też szybkie wejście. Jeśli tytuł potrzebuje dziesięciu minut na przypomnienie sterowania i kontekstu, przestaje być dobrą opcją na krótką sesję.\n\nCoraz bardziej cenię również gry, które nie karzą za przerwy. Możliwość bezbolesnego powrotu po dwóch dniach jest w dorosłym życiu dużo ważniejsza niż niekończąca się progresja. W praktyce wiele osób szuka dziś nie „większej” gry, tylko takiej, która dobrze mieści się w realnym tempie dnia.\n\nKrótka sesja nie oznacza mniejszej wartości. Czasem właśnie te mniejsze, sprytnie zaprojektowane tytuły zostawiają najwięcej frajdy, bo zamiast walczyć o każdą minutę uwagi, po prostu dobrze wykorzystują czas, który naprawdę masz.",
            'Remote work bez chaosu: mój tygodniowy system pracy': "Praca zdalna daje dużą swobodę, ale bez własnego systemu bardzo łatwo zamienia się w ciąg reagowania na to, co akurat wpadnie na ekran. U mnie największą zmianę zrobiło planowanie tygodnia z góry w blokach tematycznych. Zamiast codziennie od nowa zastanawiać się, kiedy robić deep work, spotkania i drobne rzeczy operacyjne, część decyzji zapada już wcześniej.\n\nPoczątek tygodnia poświęcam na rozpisanie najważniejszych rezultatów, nie pojedynczych zadań. To pozwala odróżnić pracę, która realnie przesuwa projekt, od aktywności dającej tylko poczucie zajętości. Potem układam dni tak, by podobne typy pracy nie konkurowały ze sobą przez cały czas. Jeśli rano mam blok skupienia, staram się nie rozbijać go komunikatorami i spotkaniami.\n\nRównie ważne są zasady kończenia dnia. Krótki przegląd otwartych tematów, dopisanie jednego pierwszego kroku na jutro i zamknięcie zbędnych kart robią dużą różnicę. Dzięki temu nie zaczynam kolejnego poranka od odtwarzania kontekstu z chaosu.\n\nRemote work staje się lżejszy nie wtedy, gdy wszystko jest idealnie zoptymalizowane, ale gdy liczba codziennych decyzji spada. Dobry system tygodniowy powinien dawać strukturę, ale zostawiać też trochę miejsca na rzeczy, których i tak nie da się przewidzieć.",
            'Jak prowadzić krótkie spotkania, które mają sens': "Krótki meeting sam w sobie nie jest wartością. Spotkanie ma sens dopiero wtedy, gdy wiadomo, po co się odbywa i jaka decyzja ma po nim zapaść. Bez tego nawet piętnaście minut potrafi być stratą czasu, bo uczestnicy wychodzą z różnymi interpretacjami i bez jasnego następnego kroku.\n\nNajprostsza poprawka to agenda zamknięta w dwóch lub trzech punktach, wysłana przed spotkaniem. Nie chodzi o rozbudowany dokument, tylko o sygnał: ten call służy temu i temu, a na końcu potrzebujemy konkretnego ustalenia. Dzięki temu łatwiej zaprosić tylko potrzebne osoby i utrzymać rozmowę w ryzach.\n\nDrugą rzeczą jest dyscyplina czasowa połączona z asynchronicznością. Jeśli status można wysłać w wiadomości, nie trzeba rezerwować na niego wspólnego czasu. Spotkanie powinno być miejscem do rozwiązywania niejasności, podejmowania decyzji i odblokowywania pracy, a nie czytania sobie nawzajem ticketów.\n\nDobre krótkie spotkanie kończy się jednym zdaniem: kto robi co dalej i do kiedy. Bez tego nawet przyjemna rozmowa zostaje tylko rozmową. Im prostsza struktura, tym większa szansa, że spotkania przestaną być domyślnym odruchem i zaczną pełnić realną funkcję w pracy zespołu.",
            'Czego szukam w ofertach pracy jako backend developer': "Z wiekiem coraz mniej interesują mnie ogólne hasła o dynamicznym środowisku i coraz bardziej konkret: jak wygląda zespół, czego ode mnie oczekuje i w jaki sposób podejmuje decyzje techniczne. Dobra oferta pracy dla backend developera nie musi być przesadnie marketingowa, ale powinna jasno pokazywać kontekst roli.\n\nNajpierw patrzę na odpowiedzialność. Czy to stanowisko dotyczy utrzymania istniejących usług, budowy nowych funkcji, pracy blisko produktu, a może przede wszystkim integracji i niezawodności. Bez tej informacji trudno ocenić, czy opis jest uczciwy i czy rola rzeczywiście pasuje do mojego sposobu pracy.\n\nDrugim filtrem jest jakość techniczna sygnałów. Nie chodzi o listę modnych technologii, tylko o to, czy firma w ogóle komunikuje coś o testach, review, monitoringu, wdrożeniach i podejściu do długu technicznego. Nawet jedno czy dwa konkretne zdania mówią więcej niż długi akapit benefitów.\n\nPatrzę też na dojrzałość procesu. Transparentne widełki, sensownie opisane etapy rekrutacji i jasne oczekiwania wobec seniority budują zaufanie szybciej niż najbardziej kreatywna nazwa stanowiska. W ogłoszeniu szukam więc przede wszystkim sygnału, że po drugiej stronie jest zespół, który wie, jak chce pracować, a nie tylko kogo chce zatrudnić.",
        }

        posts = []
        days_offset = 1
        image_index = 0
        for category_slug, items in posts_blueprint.items():
            for idx, (title, tag_names) in enumerate(items):
                author = authors[(days_offset + idx) % len(authors)]
                post = Post.objects.create(
                    author=author,
                    title=title,
                    content=article_bodies[title],
                    category=categories[category_slug],
                    image_url=image_urls[image_index % len(image_urls)],
                    is_published=True,
                    is_featured=(idx == 0),
                )
                post.tags.set([tags[name] for name in tag_names if name in tags])
                post.created_at = timezone.now() - timedelta(days=days_offset)
                post.updated_at = post.created_at + timedelta(hours=6)
                post.save(update_fields=['created_at', 'updated_at'])
                posts.append(post)
                image_index += 1
                days_offset += 2

        commenter_pool = [
            ('Anna Kowalska', 'anna@example.com'),
            ('Piotr Nowak', 'piotr@example.com'),
            ('Kasia Lis', 'kasia@example.com'),
            ('Marek Zielinski', 'marekz@example.com'),
            ('Julia Mazur', 'julia@example.com'),
            ('Pawel Kaczmarek', 'pawel@example.com'),
            ('Monika Wrobel', 'monika@example.com'),
            ('Tomasz Baran', 'tomasz@example.com'),
        ]
        comment_texts = [
            'Bardzo konkretny wpis. Dobrze się to czyta i zostawia praktyczne wnioski.',
            'Podoba mi się tempo tego artykułu. Jest krótko, ale treściwie.',
            'To jest dokładnie taki materiał, jakiego szukałem do porannej lektury.',
            'Świetna miniatura i sensowna treść. Daj znać, jeśli będzie kontynuacja.',
            'Mam podobne doświadczenia i dobrze widzieć to opisane prostym językiem.',
        ]

        for idx, post in enumerate(posts):
            comments_count = 1 + (idx % 3)
            for offset in range(comments_count):
                name, email = commenter_pool[(idx + offset) % len(commenter_pool)]
                Comment.objects.create(
                    post=post,
                    name=name,
                    email=f'{idx}-{offset}-{email}',
                    content=comment_texts[(idx + offset) % len(comment_texts)],
                    is_approved=True,
                    created_at=post.created_at + timedelta(hours=offset + 1),
                )

        like_ips = [
            '10.0.0.10', '10.0.0.11', '10.0.0.12', '10.0.0.13', '10.0.0.14',
            '10.0.0.15', '10.0.0.16', '10.0.0.17', '10.0.0.18', '10.0.0.19',
        ]
        for idx, post in enumerate(posts):
            likes_count = (idx % 5) + 1
            for ip in like_ips[:likes_count]:
                Like.objects.create(post=post, ip_address=ip)

        self.stdout.write(self.style.SUCCESS('Created demo authors:'))
        for author_data in authors_data:
            self.stdout.write(self.style.SUCCESS(f"  - {author_data['username']} / {author_data['password']}"))

        self.stdout.write(self.style.SUCCESS(
            f'Seed completed: {Category.objects.count()} categories, '
            f'{Tag.objects.count()} tags, {Post.objects.count()} posts, '
            f'{Comment.objects.count()} comments, {Like.objects.count()} likes.'
        ))
