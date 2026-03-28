🪓 Data Shovel – Interaktywna aplikacja do eksploracji i analizy danych
Data Shovel to uniwersalne narzędzie desktopowe stworzone w PyQt6, które pozwala użytkownikom wczytywać, przeglądać, porządkować i analizować dane z plików .csv. Aplikacja umożliwia również tworzenie wykresów, wykonywanie regresji oraz zapisywanie wyników. Idealna dla studentów, analityków i hobbystów zajmujących się danymi.

## Funkcjonalność
- Import danych z plików CSV i Excel
- Przeglądanie danych w formie tabeli
- Filtrowanie danych (dla kolumn numerycznych i kategorycznych)
- Generowanie różnych typów wykresów:
  - Słupkowe (bar)
  - Liniowe (line)
  - Punktowe (scatter)
  - Pudełkowe (box)
  - Skrzypcowe (violin)
  - Histogramy (hist)
  - Heatmapy (heatmap)
- Analiza regresji liniowej z wizualizacją

## Wymagania systemowe

- Python 3.8 lub nowszy
- Zainstalowane pakiety wymienione w plikach requirements.(yml, txt)

## Instalacja

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/Jacus000/DataShovel.git
   cd Projekt-Programowanie-2025
   ```
2. Stwórz środowisko i zainstaluj wymagane pakiety:
    - Conda(zalecane) 
        1. Stwórz środowisko
        ```
        conda env create -f requirements.yml
        ```
        2. Aktywuj środowisko
        ```
        conda activate DSenv
        ```
    - Lub użyj venv:
      1. Stwórz środowisko
      ```
      python -m venv DSvenv
      ``` 
      2. Aktywuj środowiska
         - Linux
           ```
           source DSvenv/bin/activate
           ```
           - Windows
           ```
           .\DSvenv\Scripts\activate
           ```
      3. Instalacja bibliotek
      ```
      pip install -r requirements.txt
      ```
3. Uruchom aplikację: 
    ```bash
    python main.py
    ```

## Przykładowe użycie
- Otwórz plik z danymi (CSV lub Excel) poprzez menu File → Open

- Przeglądaj dane w zakładce "Data"

- Użyj panelu filtrów po prawej stronie, aby zawęzić zestaw danych

- Generuj wykresy w zakładce "Plots"

- Wykonaj analizę regresji w zakładce "Regression"
