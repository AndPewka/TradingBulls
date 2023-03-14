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

2. Go to project directory, copy and fill your .env file:
   ```
   cp ./.env-example ./.env
   ```

3. Install python requirements:
   ```
   pip install -r requirements.txt
   ```

4. Initialising and running containers, creating postgresql database:
    
    if you already have postgresql and redis with other versions, run following commands:
    ```
    docker pull postgres:15.2-alpine
    docker pull redis:7.0.9-alpine
    ```
    after this:
    ```
    docker-compose build
    docker-compose up
    docker exec -it <postgres-container-name> createdb <env-variable-PG_DATABASE_NAME> -U <env-variable-PG_DATABASE_USER>
    ```
    you can find container name by executing command (when docker-compose is running): 
    ```
    docker ps
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

