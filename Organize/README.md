# W tym folderze należy umieścić zeszyt, aby dodać lub zmienić rozwiązania projektu

<p align="center" style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="https://github.com/user-attachments/assets/b0f7c3ad-6482-47ee-8ebc-ee76b2877078" alt="IMG_1014 2" style="height: 350px; width: auto;">
    <img src="https://github.com/user-attachments/assets/df0036d1-0d8e-4709-8bf9-74b133f06afd" alt="IMG_1017" style="height: 350px; width: auto;">
    <img src="https://github.com/user-attachments/assets/c42c668c-35f2-45ce-b629-c5f84feb351b" alt="IMG_1017" style="height: 350px; width: auto;">
</p>






Wypełnij szablon, używając koloru wyniku (podanego na początku zeszytu w opisie) i udostępnij cały zeszyt jako plik PDF. Następnie umieść zeszyt w tym folderze i uruchom skrypt z tego folderu  [`Organize.py`](./Organize.py) . Skrypt będzie szukał kolorów wyniku w szablonach i, gdzie je znajdzie, zaktualizuje rozwiązanie oraz zbuduje zeszyty ulepszone o Twoje rozwiązania z szablonów do folderu [`Notebooks`](../Notebooks/).


<details>
  <summary> Inicjalizacja zesztów encrypted i modyfikacja działania Skrytpu </summary>

### ℹ️ Pierwsze uruchomienie skryptu  

Przy pierwszym uruchomieniu skryptu proces może potrwać nieco dłużej, ponieważ inicjalizowane są **zeszyty publiczne**.  
Po zakończeniu tego etapu system zostanie skonfigurowany z **czterema domyślnymi motywami publicznymi**, które będą automatycznie aktualizowane przy każdym dodaniu nowych zadań do zeszytu.

### 🔐 Inicjalizacja alternatywnych motywów

Jeśli chcesz zainicjalizować inny motyw, na przykład **Encrypted** (który wymaga podania hasła), przekaż jego nazwę jako argument przy uruchomieniu skryptu.  
Wówczas skrypt poprosi Cię o hasło, a następnie zainicjalizuje wskazane motywy.  
Od tego momentu Twoje lokalne repozytorium będzie generować również te zaszyfrowane motywy.

#### 📌 Przykład użycia:
```bash
python Organize/Organize.py Encrypted_III Encrypted_II
```

> **Uwaga:** Pierwsze uruchomienie skryptu jest równoważne z wywołaniem:
> 
> `python Organize/Organize.py Noxus Tangled White Black`
> 
> Możesz podczas pierwszego uruchomienia wybrać pojedynczy motyw (np. tylko *Noxus*).  
> W takim przypadku Twoje lokalne repozytorium będzie skonfigurowane wyłącznie dla tego motywu,  
> co może być korzystne, jeśli zależy Ci na optymalizacji czasu aktualizacji.

</details>

### Biblioteki do pobrania
Projekt używa trzech bibliotek: NumPy, Pillow i PyMuPDF.
Przy pierwszym użyciu należy je zainstalować za pomocą polecenia:
``` bash
pip install -r requirements.txt
```


#  Jakie elementy przepiszemy, a jakich elementów należy unikać

<p align="center">
    Długopis Kulkowy, Tekst, Podkreślenia markerem, Zdjęcia, Kształty
</p>


<p align="center">
    <img src="https://github.com/user-attachments/assets/9070dfff-b744-4360-aa3c-9af059546ff7" width="35%">
    <img src="https://github.com/user-attachments/assets/3d8fc26a-47cf-4676-b004-20003fbad9fd" width="25%">
    <img src="https://github.com/user-attachments/assets/0d920863-5567-4c0e-ba29-b9c9b0217deb" width="35%">
</p>

<p align="center">
    Długopisy zależne od nacisku, Gumka precyzyjna, Kredki, Czcionki, które nie zawierają polskich znaków
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/98da3e97-62b3-4f66-8efa-fa8821cda0ee" width="35%">
  <img src="https://github.com/user-attachments/assets/e9a44079-1d2d-4752-beb6-d37d8d3310a7" width="25%">
  <img src="https://github.com/user-attachments/assets/ba77c89c-28a6-4010-9a4f-b938ada0fba9" width="35%">
</p>


Trzeba też pamiętać, że czcionki są między sobą różne, więc lepiej nie pisać na skraju strony, ponieważ jest duża szansa, że tekst wyjdzie poza stronę po zmianie.

<details>
  <summary> Szczegóły dodawania zadań </summary>

- Zadania, których nie chcesz dodawać, wystarczy, że nie będą zawierać koloru wynikowego.
- Można dodawać strony niezwiązane z Rosnotes np. wykłady, notatki itp. (nie zepsuje to skryptu).
- Można dodawać wiele stron. Każda z nich ma ukryte oznaczenie, które znajduje się w treści na górze. Jeśli stworzysz nową stronę, kopiując obecną, skrypt będzie odczytywał zadania (dopóki ich treść się nie zmieni) i doda każdą stronę.
- Można używać wszystkich kolorów, lecz trzeba pamiętać, że skrypt będzie porównywał każdy kolor do kolorów danego motywu i w zależności od tego, do którego będzie najbliżej, tak zmieni zeszyt i inne motywy.
- Aby dodać teorię, trzeba usunąć z folderu Solutions folder `Teorie' i wygenerować zeszyt. Zeszyt wygenerowany w ten sposób będzie zawierał szablon na teorię, który po wypełnieniu doda teorię.

</details>

--- 

### Szczegóły projektu znajdują się w odpowiednich folderach. Wystarczy przejść do interesującej części projektu i zapoznać się z jej README.

- [**src**](./src) – Mechanizm projektu oraz wyjaśnienie kodu


<p align="center">
  <a href="https://www.youtube.com/watch?v=b0Zu_EqJeUA&feature=youtu.be" target="_blank">
    <picture>
      <source srcset="./src/assets/logo_light.png" media="(prefers-color-scheme: light)">
      <source srcset="./src/assets/logo_dark.png" media="(prefers-color-scheme: dark)">
      <img src="./src/assets/logo_light.png" alt="Logo" width="400">
    </picture>
</p>

