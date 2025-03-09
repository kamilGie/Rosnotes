# Mechanizm projektu

Projekt składa się z 4 kroków:

1. **Segregowanie rozwiązań** z szablonów zeszytu do folderów rozwiązań w [Solutions](../../Solutions) jako surowe rozwiązania w postaci oddzielnych plików PDF.
2. Rozdzielenie skryptu na wiele procesów w celu przyspieszenia działania programu. Każdy proces to jeden motyw, który powstaje na podstawie **Startera**, czyli pliku PDF zawierającego tła zadań, okładki oraz ustawienia, takie jak kolory, itp.
3. **Generowanie motywów**. Każdy proces wczytuje surowe rozwiązanie, zmienia je na swoje rozwiązanie, dodając własne tło oraz zmieniając kolorystykę, a następnie zapisuje to jako nazwę motywu w folderach rozwiązań w   [Solutions](../../Solutions) obok surowego rozwiązania.
4. **Budowanie zeszytu**. Proces zaczyna się od okładki i opisu, następnie zbiera z każdego folderu rozwiązanie motywu, dodając przed nim szablon. W każdym folderze dodawana jest okładka zestawu, a na koniec okładka tylna.

<p align="center">
  <a href="https://www.youtube.com/watch?v=b0Zu_EqJeUA&feature=youtu.be" target="_blank">
    <picture>
      <source srcset="https://github.com/user-attachments/assets/6452bbe9-1124-4c42-b192-f7f07c1c5845" media="(prefers-color-scheme: light)">
      <source srcset="https://github.com/user-attachments/assets/5db5d609-cdaa-4e3f-a596-57d9e92a2eda" media="(prefers-color-scheme: dark)">
      <img src="https://github.com/user-attachments/assets/6452bbe9-1124-4c42-b192-f7f07c1c5845" alt="Task solution" width=100%>
    </picture>
  </a>
</p>

Każdy krok posiada swój folder, jest niezależny od innych i można go uruchamiać samodzielnie.

--- 


### Szczegóły projektu znajdują się w odpowiednich folderach. Wystarczy przejść do interesującej części projektu i zapoznać się z jej README.

- [**starters**](./starters) – Pliki pdf na podstawie ktorych sa generowane motywy.


<p align="center">
  <a href="https://www.youtube.com/watch?v=b0Zu_EqJeUA&feature=youtu.be" target="_blank">
    <picture>
      <source srcset="https://github.com/user-attachments/assets/f527aa3b-e050-4b58-9750-ed519a4a7af6" media="(prefers-color-scheme: light)">
      <source srcset="https://github.com/user-attachments/assets/d1aceab9-e226-4ad7-bf7e-92d89653f063" media="(prefers-color-scheme: dark)">
      <img src="https://github.com/user-attachments/assets/f527aa3b-e050-4b58-9750-ed519a4a7af6" alt="Task solution" width="400">
    </picture>
</p>

