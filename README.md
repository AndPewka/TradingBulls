

## Local deployment

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
   - TA-lib:
   ```
   curl -L -O http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && tar -xvzf ta-lib-0.4.0-src.tar.gz && \
   cd ta-lib/ && ./configure --prefix=/usr && \
   make && sudo make install
   ```
   - install docker and docker-compose, working manual for ubuntu [here](https://itisgood.ru/2019/01/21/ustanovite-docker-i-docker-compose-v-linux-mint-19/). Reboot system after adding user.

2. Clone project from github:
   ```
   git clone https://github.com/AndPewka/TradingBulls.git
   ```

3. Go to project directory and install python requirements:
   
   > Note: it is recommended to deploy the python environment for the project, for example with [venv](https://docs.python.org/3/library/venv.html).

   install dependences from requirements.txt:
   ```
   pip install -r requirements.txt
   ```

4. Copy and fill your .env file:
   ```
   cp ./.env-example ./.env
   ```
   - You need to set your django secret key (DJANGO_SECRET_KEY)
   
      To generate secret key use:
      ```
      python utils/secret_key_generator.py
      ```
   - You can also change your credentials and db options if you won't use default

5. Initialize and run containers:
    
    pull all required images:
    ```
    docker-compose pull
    ```
    run compose:
    ```
    docker-compose up
    ```

6. Create postgress database

    when containers is runnung, create postgresql database with command:
    ```
    docker exec -it <postgres-container-name> createdb <env-variable-PG_DATABASE_NAME> -U <env-variable-PG_DATABASE_USER>
    ```
    you can find container name by executing command: 
    ```
    docker ps -a | grep postgres_
    ```
    it should be something like `tradingbulls_postgres_1`

7. Migrate your database

   ```
   python manage.py migrate
   ```

8. Create user for django application:

   ```
   python manage.py createsuperuser
   ```

9. Run django server:

   python manage.py runserver localhost:8000
   > Note: server can be started when docker-compose is running or if you have configured remote database



## Docker:
   ```
   
   ```

   Drop container by name
   ```
    docker images -a | grep "binance_bot_django" | awk '{print $3}' | xargs docker rmi -f
   ```
