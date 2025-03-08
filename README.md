<p align="center">
  <a href="https://www.youtube.com/watch?v=b0Zu_EqJeUA&feature=youtu.be" target="_blank">
    <picture>
      <source srcset="https://github.com/user-attachments/assets/78bb78e5-0841-44a4-938e-b3ec8f776c6e" media="(prefers-color-scheme: light)">
      <source srcset="https://github.com/user-attachments/assets/78c11295-8336-4467-be7e-2e31ded448a8" media="(prefers-color-scheme: dark)">
      <img src="https://github.com/user-attachments/assets/78bb78e5-0841-44a4-938e-b3ec8f776c6e" alt="Task solution" width="800">
    </picture>
</p>

<!-- Usuń ten fragment po użyciu szablonu  -->

---

### Użycie szablonu Rosnotes do zestawu zadań

Użycie szablonu polega na wycięciu treści zadań, nazwaniu ich `desc_{numer zadania}.png` i umieszczeniu ich w folderach `Zestaw {numer zestawu} {nazwa zestawu}` w foldererze [Solutions](./Solutions).

<div align=center>
  <img width="256" alt="Zrzut ekranu 2025-03-8 o 12 46 26" src="https://github.com/user-attachments/assets/516edec8-4a02-4c5e-8b95-55b86d291199" />

</div>

Wypełniony w ten sposób folder [Solutions](./Solutions) jest gotowy do tworzenia zeszytów oraz dalszego rozwijania projektu. Wystarczy jeszcze tylko podać nazwę przedmiotu w skrypcie [Organize/Organize.py](./Organize/Organize.py) w klasie configu i uruchomić ten skrypt.

<details>
  <summary>Ustawianie repozytorium GitHub</summary>

## Automatyzacja projektu 

Projekt w dużej mierze korzysta z GitHub Actions ([link do tego, co to jest](https://www.youtube.com/watch?v=eB0nUzAI7M8)). Informacje o użytych akcjach znajdują się w pliku README w katalogu [**.github/workflows**](./.github/workflows).

### Ustawienie GitHub Actions dla projektu Rosnotes

1. **Wygenerowanie tokena GitHub**  
   Na początku należy wygenerować token GitHub ([link jak to zrobić (30s)](https://www.youtube.com/shorts/rlO6C6dDKNs)). Token trzeba wygenerować z odpowiednimi ustawieniami.

   ![Zrzut ekranu 2025-03-8 o 21 47 00](https://github.com/user-attachments/assets/52ab6aee-e304-41cb-a2e4-384b2b0be255)

2. **Ustawienie sekretów**  
   Następnie ustaw token w sekretach GitHub w ustawieniach repozytorium, w zakładce **Secrets and variables > Actions** oraz hasła do zeszytów, które znamy (nie trzeba podawać wszystkich, a README będzie zawierać tylko te, do których hasło zostało podane lub hasła nie zawierają).

   ![Zrzut ekranu 2025-03-8 o 21 47 40](https://github.com/user-attachments/assets/557bc992-04c3-4dce-b265-9f24925422d6)

   > Wszystkie sekrety muszą być nazwane dokładnie tak samo.

3. **Udzielenie zgody workflow**  
   Na sam koniec należy udzielić workflowowi zgody na zmiany w repozytorium. Robi się to w ustawieniach repozytorium, w zakładce **Actions > General**.

   ![Zrzut ekranu 2025-03-8 o 21 48 40](https://github.com/user-attachments/assets/f052481d-55c7-4600-82c5-735f6da3b9ef)

Tak ustawiony projekt jest gotowy do testowania i dodawania zadań. Każde nowe zadanie będzie automatycznie dodawane do linków w wydaniach (releases) oraz do README, a także do mechanizmu testowania.

> **Uwaga:** Projekt posiada workflow, który aktualizuje każdy projekt Rosnotes utworzony na podstawie szablonu. Dzięki temu mogę pracować tylko na repozytorium głównym, a zmiany są codziennie o 24:00 synchronizowane z każdym repozytorium potomnym Rosnotes. Prowadzi to jednak do sytuacji, w której **edycja** plików w repozytoriach potomnych skutkuje przywracaniem ich pierwotnej zawartości, chyba że wykluczymy dany plik z mechanizmu aktualizacji, dodając go do listy plików wykluczonych w [**.github/workflows/exclude-list.txt**](./.github/workflows/exclude-list.txt). Należy jednak pamiętać, że wykluczenie pliku spowoduje, że nie będzie on wspierany przez zmiany w głównym repozytorium Rosnotes.


</details>

---

<!--  Usuń ten fragment po użyciu szablonu   -->


### 🔧 Używanie Projektu

Projekt składa się z **4 głównych folderów**:


1.  [**`Solutions`**](./Solutions) – Folder z rozwiązaniami zadań.
2.  [**`Notebooks`**](./Notebooks) – Zeszyty do pobrania w różnych motywach zawierające szablony oraz rozwiązania.
3.  [**`Organize`**](./Organize) – Skrypt do przenoszenia rozwiązań z zeszytów do folderu `Solutions` i synchronizacji między motywami.
4. [**`github/workflow`**](./.github/workflows) - Aktualizuje [Release](./releases/tag/Notebooks) po każdej zmianie, zapewniając, że zeszyty w `Notebooks` są aktualne.


---

### 📓 Zawartość zeszytów

W zeszycie każde zadanie ma szablon, a rozwiązane zadanie będzie miało dodatkowo rozwiązanie na następnej stronie.

![Motyw (1)](https://github.com/user-attachments/assets/81ede432-39d1-464e-a2f9-7e2eb897f6f2)

Aby pobrać zeszyt, przejdź do [**`Notebooks`**](./Notebooks) i kliknij nazwę motywu.

---


### 🔍 Ukryte motywy
4 motywy publiczne oraz 7 motywów encrypted. W motywach publicznych ukryte są podpowiedzi do haseł motywów, encrypted. Hasło to zawsze będzie także nazwą danego motywu, który odblokowujesz.

### 🎨 3 Kolory  
Każdy zeszyt ogranicza się do trzech kolorów:  **Głównego** do pisma, **Dodatkowego** do zaznaczania, podkreślania itp , **Trzeciego** do wyników. 
Na początku zeszytu znajduje się informacja, który kolor pełni jaką funkcję, aby łatwo było znaleźć odpowiedzi na zadania.

### 📝 Dodawanie Zadań  
Wystarczy wypełnić szablon, dodać plik PDF twojego zeszytu do folderu `Organize` i uruchomić skrypt znajdujący się w tym folderze. Wszystkie motywy zostaną automatycznie zaktualizowane o Twoje rozwiązania.

### 🛠️ Modyfikacja Zeszytów  
W folderze [startery](./Organize/src/starters/) znajdują się startery zeszytów. Możesz edytować i zastąpić istniejącą stronę własną, tworząc wersję zeszytu z innymi stronami, kolorami lub czcionką.


### 🎲 Losowanie Motywów Rozwiązań
Motyw rozwiązania w pliku README jest losowy, przy czym istnieje 92% na motyw publiczny oraz **8%** na motyw Encrypted!


### 🐛 Zgłaszanie Błędów
Błędy w rozwiązaniach lub w skrypcie, zgłaszaj na ****Issues**** lub <a href="https://gieras.pl/">****prywatnie****</a>.


### 🗿 Najwięksi współtwórcy:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://github.com/kamilGie/Rosnotes-Dyskretna/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=kamilGie/Rosnotes-Dyskretna" alt="Najwięksi współtwórcy" />
</a>

---

### Szczegóły projektu znajdują się w odpowiednich folderach. Wystarczy przejść do interesującej części projektu i zapoznać się z jej README.

- [**Organize**](./Organize) – Korzystanie z projektu i dodawanie zadań
- [**Notebooks**](./Notebooks) – Linki do pobrania zeszytów
- [**.github/workflows**](./.github/workflows) – Automatyzacja i testy
- [**Solutions**](./Solutions) – Statystyki dotyczące częstości występowania motywów w rozwiązaniach
- [**Organize/src**](./Organize/src) – Mechanizm projektu oraz wyjaśnienie kodu
- [**Organize/src/starters**](./Organize/src/starters) – Pliki pdf na podstawie ktorych sa generowane motywy.


<p align="center">
  <a href="https://www.youtube.com/watch?v=b0Zu_EqJeUA&feature=youtu.be" target="_blank">
    <picture>
      <source srcset="https://github.com/user-attachments/assets/f527aa3b-e050-4b58-9750-ed519a4a7af6" media="(prefers-color-scheme: light)">
      <source srcset="https://github.com/user-attachments/assets/d1aceab9-e226-4ad7-bf7e-92d89653f063" media="(prefers-color-scheme: dark)">
      <img src="https://github.com/user-attachments/assets/f527aa3b-e050-4b58-9750-ed519a4a7af6" alt="Task solution" width="400">
    </picture>
</p>

