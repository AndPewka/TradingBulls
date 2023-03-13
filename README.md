1. Install system dependencies
   - Utils:
   ```
   sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
   libbz2-dev libreadline-dev libsqlite3-dev curl \
   libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git
   ```
   - Python via pyenv:
   ```
   curl https://pyenv.run | bash && \
   pyenv install 3.10.4 && \
   pyenv global 3.10.4
   ```
   - Mysql:
   ```
   sudo apt install mysql-server
   ```
   - TA-lib:
   ```
   curl -L -O http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && tar -xvzf ta-lib-0.4.0-src.tar.gz && \
   cd ta-lib/ && ./configure --prefix=/usr && \
   make && sudo make install
   ```

2. Go to project directory, copy and fill your .env file:
   ```
   cp ./.env-example ./.env
   ```

3. Install python requirements:
   ```
   pip install -r requirements.txt
   ```

4. Add user to mysql with same credentials as you placed in .env file:
    ```
    sudo mysql -e "CREATE DATABASE trading_bot"
    sudo mysql -e "CREATE USER 'YOUR_USERNAME_HERE'@'localhost' IDENTIFIED BY 'YOUR_PASSWORD_HERE'"
    sudo mysql -e "GRANT ALL ON trading_bot.* TO 'YOUR_USERNAME_HERE'@'localhost'"
    ```

5. Migrate your database
   ```
   python manage.py migrate
   ```
6. Create user for django application:
   ```
   python manage.py createsuperuser
   ```
7. Run django server
   ```
   python manage.py runserver localhost:3000
   ```

