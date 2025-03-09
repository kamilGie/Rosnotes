# W tym folderze należy umieścić zeszyt, aby dodać lub zmienić rozwiązania projektu

<p align="center" style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="https://github.com/user-attachments/assets/ba06659a-1d28-4250-af34-1857c34c193a" alt="IMG_1014 2" style="height: 350px; width: auto;">
    <img src="https://github.com/user-attachments/assets/159fbd03-27e8-4a07-970b-ef6d21aa0d30" alt="IMG_1017" style="height: 350px; width: auto;">
    <img src="https://github.com/user-attachments/assets/b5606666-0b63-4952-9310-8964729038c4" alt="IMG_1017" style="height: 350px; width: auto;">
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
    <img src="https://github.com/user-attachments/assets/c8cd9c1e-3644-42a0-b969-72d58680dafd" width="35%">
    <img src="https://github.com/user-attachments/assets/7e167fdc-af2e-4e0b-91c9-d9a1a2cd0e33" width="25%">
    <img src="https://github.com/user-attachments/assets/ec46607b-8cf9-4989-86e4-a424a03834ce" width="35%">
</p>

<p align="center">
    Długopisy zależne od nacisku, Gumka precyzyjna, Kredki, Czcionki, które nie zawierają polskich znaków
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/d069df29-5dd4-4673-bb6e-0686c1959a99" width="35%">
  <img src="https://github.com/user-attachments/assets/7e167fdc-af2e-4e0b-91c9-d9a1a2cd0e33" width="25%">
  <img src="https://github.com/user-attachments/assets/58dee1c5-27c7-4922-84df-20371663321e" width="35%">
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

