
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
   
3. Copy and fill your .env file:
   ```
   cp ./.env-example ./.env
   ```

4. Create dbs and fill developer data:
   ```
   docker-compose up
   python utils/seeds.py
   docker-compose down
   ```

5. Run server:
   ```
   honcho start
   ```
   > Note: server can be started when docker-compose is running or if you have configured remote database

## Docker:
   Drop container by name
   ```
   docker images -a | grep "container_name" | awk '{print $3}' | xargs docker rmi -f
   ```
