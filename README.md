<p align="center">
  <a href="https://www.youtube.com/watch?v=b0Zu_EqJeUA&feature=youtu.be" target="_blank">
    <picture>
      <source srcset="https://github.com/user-attachments/assets/405097e1-9a0d-44e3-8c98-7bf0992bc175" media="(prefers-color-scheme: light)">
      <source srcset="https://github.com/user-attachments/assets/f058cb10-5988-4587-be08-68301d9ba5b1" media="(prefers-color-scheme: dark)">
      <img src="https://github.com/user-attachments/assets/405097e1-9a0d-44e3-8c98-7bf0992bc175" alt="Logo czwartku studenckiego" width="800">
    </picture>
</p>

<!-- Usuń ten fragment po użyciu szablonu  -->

---

## 🚀 Przeznaczenie

Repozytorium to szablon umożliwiający tworzenie rozwiązań do zestawów zadań w różnych motywach.  
Przykładowe repozytorium wykorzystujące ten szablon: [***Rosnotes Dyskretna***](https://github.com/kamilGie/Rosnotes-Dyskretna).

### 🛠️ Użycie szablonu Rosnotes do zestawu zadań

Użycie szablonu polega na wycięciu treści zadań, nazwaniu ich `desc_{numer zadania}.png` i umieszczeniu w folderach `Zestaw {numer zestawu} {nazwa zestawu}` w folderze [Solutions](./Solutions).

<div align=center>
  <img width="256" alt="Zrzut ekranu 2025-03-8 o 12 46 26" src="https://github.com/user-attachments/assets/6e9bba96-e9d8-4c67-84a0-b1629fe0a5ad" />
</div>



Wypełniony w ten sposób folder [Solutions](./Solutions) jest gotowy do tworzenia zeszytów oraz dalszego rozwijania projektu. Wystarczy jeszcze tylko podać nazwę przedmiotu w skrypcie [Organize/Organize.py](./Organize/Organize.py) w klasie configu i uruchomić ten skrypt.

<details>
  <summary>Ustawianie repozytorium GitHub</summary>

## Automatyzacja projektu 

Projekt w dużej mierze korzysta z GitHub Actions ([link do tego, co to jest](https://www.youtube.com/watch?v=eB0nUzAI7M8)). Informacje o użytych akcjach znajdują się w pliku README w katalogu [**.github/workflows**](./.github/workflows).

### Ustawienie GitHub Actions dla projektu Rosnotes

1. **Wygenerowanie tokena GitHub**  
   Na początku wygeneruj token GitHub ([link jak to zrobić (30s)](https://www.youtube.com/shorts/rlO6C6dDKNs)). Token trzeba wygenerować z odpowiednimi ustawieniami.


![image](https://github.com/user-attachments/assets/3f97956d-5dc6-4743-a4ec-718befdbacbb)


2. **Ustawienie sekretów**  
   Następnie, w sekretach GitHub, w ustawieniach repozytorium, w zakładce **Secrets and variables > Actions**, ustaw token oraz hasła do zeszytów, które znasz (nie trzeba podawać wszystkich, README będzie zawierać tylko te zeszyty, do których hasło zostało podane lub te, które nie zawierają hasła).

![image](https://github.com/user-attachments/assets/cae16dba-e0ac-4a02-9a9c-046f5ad3d388)


   > Wszystkie sekrety muszą być nazwane dokładnie tak samo.

3. **Udzielenie zgody workflow**  
   Na sam koniec udziel workflowowi zgody na zmiany w repozytorium. Robi się to w ustawieniach repozytorium w zakładce **Actions > General**.

![image](https://github.com/user-attachments/assets/21f949f6-bb04-48bc-8c84-d6dc57fda1d8)

Tak ustawiony projekt jest gotowy do testowania i dodawania zadań. Każde nowe zadanie będzie automatycznie dodawane do linków w wydaniach (releases) oraz do README, a także do mechanizmu testowania.

> **Uwaga:** Projekt posiada workflow, który aktualizuje każdy projekt Rosnotes utworzony na podstawie szablonu. Dzięki temu mogę pracować tylko na repozytorium głównym, a zmiany są codziennie o 24:00 synchronizowane z każdym repozytorium potomnym Rosnotes. Prowadzi to jednak do sytuacji, w której **edycja** plików w repozytoriach potomnych skutkuje przywracaniem ich pierwotnej zawartości, chyba że wykluczymy dany plik z mechanizmu aktualizacji, dodając go do listy plików wykluczonych w [**.github/workflows/exclude-list.txt**](./.github/workflows/exclude-list.txt). Należy jednak pamiętać, że wykluczenie pliku spowoduje, że nie będzie on wspierany przez zmiany w głównym repozytorium Rosnotes.


</details>

---

<!--  Usuń ten fragment po użyciu szablonu   -->


### 🔧 Używanie Projektu

Projekt składa się z **4 głównych folderów**:


1.  [**`Solutions`**](./Solutions) – folder z rozwiązaniami zadań.
2.  [**`Notebooks`**](./Notebooks) – zeszyty do pobrania w różnych motywach zawierające szablony oraz rozwiązania.
3.  [**`Organize`**](./Organize) – skrypt do przenoszenia rozwiązań z zeszytów do folderu `Solutions` i synchronizacji między motywami.
4. [**`github/workflow`**](./.github/workflows) - aktualizacja [Release](./releases/tag/Notebooks) po każdej zmianie, zapewniając, że zeszyty w `Notebooks` są aktualne.


---

### 📓 Zawartość zeszytów

W zeszycie każde zadanie ma szablon, a rozwiązane zadanie będzie mieć dodatkowo rozwiązanie na następnej stronie.

<p align="center">
    <picture>
      <source srcset="https://github.com/user-attachments/assets/0be2dca0-421d-4542-81e1-b5e774bb2931" media="(prefers-color-scheme: light)">
      <source srcset="./Organize/src/assets/example.png" media="(prefers-color-scheme: dark)">
      <img src="https://github.com/user-attachments/assets/0be2dca0-421d-4542-81e1-b5e774bb2931" alt="Task solution" width="1000">
    </picture>
</p>

Aby pobrać zeszyt, przejdź do [**`Notebooks`**](./Notebooks) i kliknij nazwę motywu.

---



### 🔍 Ukryte motywy
4 motywy publiczne oraz 7 motywów encrypted. W motywach publicznych ukryte są podpowiedzi do haseł motywów encrypted. Hasło zawsze będzie także nazwą danego motywu, który odblokowujesz.

### 🎨 3 Kolory  
Każdy zeszyt ogranicza się do trzech kolorów:  **Głównego** do pisania, **Dodatkowego** do zaznaczania, podkreślania itp., oraz **Trzeciego** do wyników. 
Na początku zeszytu znajduje się informacja, który kolor pełni jaką funkcję, aby łatwo można było znaleźć odpowiedzi na zadania.

### 📝 Dodawanie Zadań  
Wystarczy wypełnić szablon, dodać plik PDF Twojego zeszytu do folderu `Organize` i uruchomić skrypt znajdujący się w tym folderze. Wszystkie motywy zostaną automatycznie zaktualizowane o Twoje rozwiązania.

### 🛠️ Modyfikacja Zeszytów  
W folderze [startery](./Organize/src/starters/) znajdują się startery zeszytów. Możesz edytować i zastąpić istniejącą stronę własną, tworząc wersję zeszytu z innymi stronami, kolorami lub czcionką.


### 🎲 Losowanie Motywów Rozwiązań
Motyw rozwiązania w pliku README jest losowy, przy czym istnieje 92% szans na motyw publiczny oraz **8%** na motyw Encrypted!


### 🐛 Zgłaszanie Błędów
Błędy w rozwiązaniach lub w skrypcie zgłaszaj na ****Issues**** lub <a href="https://gieras.pl/">****prywatnie****</a>.


### 🗿 Najwięksi współtwórcy:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://github.com/kamilGie/Rosnotes-Dyskretna/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=kamilGie/Rosnotes-Dyskretna" alt="Najwięksi współtwórcy" />
</a>

---

### Szczegóły projektu znajdują się w odpowiednich folderach. Wystarczy przejść do interesującej części projektu i zapoznać się z jej README.

- [**Organize**](./Organize) – korzystanie z projektu i dodawanie zadań,
- [**Notebooks**](./Notebooks) – linki do pobrania zeszytów,
- [**.github/workflows**](./.github/workflows) – automatyzacja i testy,
- [**Solutions**](./Solutions) – statystyki dotyczące częstości występowania motywów w rozwiązaniach,
- [**Organize/src**](./Organize/src) – mechanizm projektu oraz wyjaśnienie kodu,
- [**Organize/src/starters**](./Organize/src/starters) – pliki pdf, na podstawie których są generowane motywy.


<p align="center">
  <a href="https://www.youtube.com/watch?v=b0Zu_EqJeUA&feature=youtu.be" target="_blank">
    <picture>
      <source srcset="./Organize/src/assets/logo_light.png" media="(prefers-color-scheme: light)">
      <source srcset="./Organize/src/assets/logo_dark.png" media="(prefers-color-scheme: dark)">
      <img src="./Organize/src/assets/logo_light.png" alt="Logo" width="400">
    </picture>
</p>

