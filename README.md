#  Proxy Checker

## Запуск софту
### 1. Створіть віртуальне середовище у кореневій папці проєкту:
   ```bash
   python -m venv venv
   ```

### 2. Активуйте віртуальне середовище:
   - Для Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Для macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

### 3. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Створіть файл **proxies.txt** та внесіть проксі для перевірки. Підтримуються формати:
   - `ip:port:login:pass`
   - `login:pass@ip:port`
   - `http://login:pass@ip:port`
   - `socks5://login:pass@ip:port`


### 5. За потреби змініть налаштування в файлі **settings.py**:
   - `proxy_type` - впишіть тип проксі: `http` або `socks5`
   - `multi` - впишіть `True` або `False`. Якщо `True` - проксі будуть перевірені одночасно (швидко), якщо `False` - проксі будуть перевірятись по одному (може знадобитись якщо треба щоб в репорті проксі були в тому ж порядку як і в файлі **proxies.txt**)
   - `do_report` - впишіть `True` або `False`. Якщо `True` - після перевірки створяться файли **good_proxies.txt** зі списком працюючих проксі та **bad_proxies.txt** зі списком не працюючих. Якщо робити цього не потрібно залиште `False`.
   - `country` - можна вписати дволітерний код країни (наприклад `UA` або `GB`) і створиться файл **country_report.txt** в котрий випишуться проксі цієї країни. Якщо робити цього не потрібно залиште ''.


### 6. Запустіть софт:
   ```bash
   python main.py
   ```

---

### Telegram: [Все дозволено •](https://t.me/+oCfK6i7az5czNDU6)
