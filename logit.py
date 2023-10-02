from tradier import *


sp500 = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv');


sp500 = sp500.sample(15);

sp500_symbols = list(sp500['Symbol']);

df = pd.DataFrame({'profitable':[], 'volume_change':[]});

for s in sp500_symbols:
    bar_data = quotes.get_historical_quotes(s, interval='monthly', start_date='2022-10-01');
    print(bar_data)
    bar_data['price_change'] = bar_data['close'] - bar_data['open'];
    bar_data['profitable'] = (bar_data['close']-bar_data['open'] > 0).astype(int);
    bar_data['volume_change'] = bar_data['volume'].diff();
    
    df = df.append(bar_data[['profitable', 'volume_change']]);


