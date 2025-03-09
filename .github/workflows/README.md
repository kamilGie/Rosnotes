# Automatyzacja i testy projektu

## Automatyzacja

### Wydania i Zeszyty

Po każdym dodaniu zadania (push do folderu [Solutions](../../Solutions)) workflow [deploy.yml](./deploy.yml) wykonuje następujące operacje:
- Instalacja repozytorium zawierającego wszystkie motywy, w tym także te `Encrypted`.
- Aktualizacja wydania Notebooks, aby linki do zeszytów były zawsze aktualne.
- Sprawdzenie, w których folderach zadania nie posiadają zdjęcia, w celu przeprowadzenia losowania motywu, który pojawi się w pliku README.

Dla wylosowanego motywu wykonywane są następujące kroki:
- Utworzenie zdjęcia motywu.
- Wygenerowanie pliku README.md z informacją o prawdopodobieństwie wyboru danego motywu.

> Takie rozwiązanie powoduje, że nie trzeba inicjować żadnego motywu – wystarczy dodać surowe rozwiązania. Dzięki temu skrypt może działać szybciej, a osoby dodające rozwiązania poprzez pull request (nawet bez znajomości haseł do motywów) mogą tworzyć motywy `Encrypted`, i wszystkie zeszyty są na bieżąco ze zmianami.

### Synchronizacja z głównym repozytorium  

Codziennie o północy workflow [template_sync.yml](./template_sync.yml) sprawdza zmiany w głównym repozytorium [Rosnotes](https://github.com/kamilGie/Rosnotes) i pobiera aktualizacje z wyjątkiem wybranych folderów z [exclude-list.txt](./exclude-list.txt), aby projekt był na bieżąco z najnowszymi mechanizmami i starterami.

---

## Testy

Po każdej zmianie mechanizmu (push do folderu [Organize](../../Organize)) uruchamiany jest jeden z dwóch skryptów testowych.

### Test src

Workflow [test_src.yml](./test_src.yml) sprawdza, czy mechanizm zeszytu został zachowany, instalując repozytorium na wirtualnej maszynie. Test obejmuje:
- Inicjację zeszytów.
- Inicjację zeszytu oraz sprawdzenie, czy dodawanie zadań działa poprawnie.
- Inicjację zeszytów z gotowym zeszytem, weryfikując możliwość poprawnego uruchomienia.

### Test Starterów

Workflow [test_starters.yml](./test_starters.yml) polega na:
- Zainstalowaniu repozytorium zawierającego wszystkie motywy.
- Dla każdego motywu, dodaniu na parzystych stronach koloru wynikowego.
- Usunięciu wszystkich surowych rozwiązań.
- Przetestowaniu, czy po instalacji repozytorium z zeszytem, surowe rozwiązania pojawiają się wyłącznie na parzystych zadaniach.

Jeżeli test zakończy się powodzeniem, oznacza to, że zeszyt przeszedł kontrolę, a kolejne zeszyty są testowane, przy czym przed każdym testem usuwane są wszystkie surowe rozwiązania.

> Test Starterów wykorzystuje dość restrykcyjną metodę usuwania rozwiązań, dlatego skrypt do usuwania pozostałych rozwiązań nie został wydzielony, aby uchronić użytkownika przed przypadkowym usunięciem rozwiązań z repozytorium.

--- 
Dodatkowo istnieje jeszcze workflow [change_logo.yml](./change_logo.yml), który uruchamia się w każdy czwartek o 16:00 oraz codziennie o północy, sprawdzając, czy wypada święto. Jeśli tak, zmienia główne logo na tematyczne – dzięki temu, w studencki czwartek jest logo miasteczkowe oraz w okresie świątecznym, logo Rosnotes będzie miało świąteczną czapeczkę.  



<p align="center">
  <img width="50" alt="Ja wymyślający ta super zmiane" src="https://github.com/user-attachments/assets/790888c2-a83b-47e0-8b60-0288f5912544" style="margin-left: 10px;">
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=b0Zu_EqJeUA&feature=youtu.be" target="_blank">
    <picture>
      <source srcset="../Organize/src/assets/logo_light.png" media="(prefers-color-scheme: light)">
      <source srcset="../Organize/src/assets/logo_dark.png" media="(prefers-color-scheme: dark)">
      <img src="../Organize/src/assets/logo_light.png" alt="Logo" width="400">
    </picture>
</p>
