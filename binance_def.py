from binance_api import Binance

bot = Binance(
    API_KEY='****',
    API_SECRET='****'
)

get_json = bot.futuresExchangeInfo( )
key_sym = get_json['symbols']
symb_list = []
for i in key_sym:
    symb_list.append(i['symbol'])
# c = b[0]['symbol']\
symb_list.sort( )


# список по буквам
def alphab_lists(letter):
    alph_list = []
    for i in symb_list:
        if i.startswith(letter):
            alph_list.append(i)
    return alph_list


# ticker list
def tickers_list(symb_list):
    get_json = bot.futuresExchangeInfo( )
    key_sym = get_json['symbols']
    # symb_list = []
    for i in key_sym:
        symb_list.append(i['symbol'])
    symb_list.sort( )
    return symb_list


c = tickers_list([])


# ticker price
def get_price(Ticker):
    tick = bot.futuresSymbolPriceTicker(symbol=Ticker)
    price = tick['price']
    print(price)
    return price
    # print(tick)



print(c)
