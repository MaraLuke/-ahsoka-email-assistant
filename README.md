# Ahsoka Tano - GPT Email Assistant

Tento projekt je osobní asistent pro správu e-mailů z účtu `martin.danek@advamat.cz`, propojený s ChatGPT přes Actions.

## 🔧 Spuštění lokálně

1. Nainstaluj si Python 3.10+
2. Nainstaluj závislosti:
   ```
   pip install -r requirements.txt
   ```
3. Spusť server:
   ```
   uvicorn app.main:app --reload
   ```

## ☁️ Nasazení na Render

1. Vytvoř nový web service
2. Nahraj kód nebo připoj Git
3. Nastav `uvicorn app.main:app --host 0.0.0.0 --port 10000`
4. Přidej proměnné prostředí pro heslo, e-mail atd.

## 🤖 Připojení k GPT

1. V ChatGPT (Plus) vytvoř nové vlastní GPT
2. Nahraj `actions.json`
3. Používej jako "Ahsoka Tano"