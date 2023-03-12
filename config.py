debug = True
futures = True

#sql
db = "mysql"
userDB = "andpewka"
passwordDB= "2301404"
nameDB="binance_bot"
tg_token = "5668352750:AAEoxSriWtVHw0jDMVcQx38iq-DTObP4ayc"

if not futures:
	if debug:
		api_key = "zq9mR4usBdf1agHodbvxKqrJ0qa8IM7EbcIFbW7Vw0xmRqbjDcSaefcxwBGw84BK"
		secret_key = "fXEdIt65wFReRLISEx02o0vkevLjuuQa9e1oThJrxu2h5P3eVBepve8JtPIsGwEd"
		base_url = "https://testnet.binance.vision"
	else:
		api_key = "WUed2uyVgRmnKMgWrlV5pFQ5GBPhHYIlBV7OjoRx8mYcndDFW27odiBoPb6jPs22"
		secret_key = "MfQzKlZVgK8N3D7vCBfl70ovCa2SoJnxLXbjg1rzlHR6uSnfgxXAHmo4ZQrYH7hd"
		base_url = "https://api.binance.com"


if futures:
	if debug:
		api_key = "acab0fc978ad7919d9d103203213ee7f10245493edf769248849e12e20c6dfbf"
		secret_key = "de9dcee1a19ed4cadf5ab33406fd93d988d140e909516c961c3eb65e5785c8a6"
		base_url = "https://testnet.binancefuture.com"
	else:
		api_key = "7I5cmkWqfuH37JqvCd94gEeM3q3egikP1qe5NL8v7orv7VDUU2WCzOsrVrV994V3"
		secret_key = "NQxnN6LXqZ4Iab5HYJcVPghiIHKy0biig7c8cfAiIp3MOyfB4mGonzOGyT4DZazB"
		base_url = "https://dapi.binance.com"


