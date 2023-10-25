# uvatradier

`uvatradier` is a comprehensive Python package designed to interact with the Tradier API. This package simplifies the process of making API requests, handling responses, and performing various trading and account management operations.

## Features

- **Account Management**: Retrieve profile, balance, gain/loss, orders, and positions related to a trading account.
- **Trading**: Place, modify, and cancel equity and option orders.
- **Market Data**: Access real-time and historical market data for equities and options.
- **Options Data**: Retrieve options chains, strikes, and expiration dates.

## Installation

To install `uvatradier`, you can use `pip`:

\```sh
pip install uvatradier
\```

## Quick Start

To get started, you need to import the necessary classes from `uvatradier` and provide your Tradier account number and authorization token.

\```python
from uvatradier import Account, Tradier, EquityOrder, OptionsOrder, OptionsData, Quotes

ACCOUNT_NUMBER = 'YOUR_ACCOUNT_NUMBER'
AUTH_TOKEN = 'YOUR_AUTH_TOKEN'

account = Account(ACCOUNT_NUMBER, AUTH_TOKEN)
tradier = Tradier(ACCOUNT_NUMBER, AUTH_TOKEN)
equity_order = EquityOrder(ACCOUNT_NUMBER, AUTH_TOKEN)
options_order = OptionsOrder(ACCOUNT_NUMBER, AUTH_TOKEN)
options_data = OptionsData(ACCOUNT_NUMBER, AUTH_TOKEN)
quotes = Quotes(ACCOUNT_NUMBER, AUTH_TOKEN)
\```

## Usage

### Account Management

- Get User Profile:

  \```python
  user_profile = account.get_user_profile()
  \```

- Get Account Balance:

  \```python
  account_balance = account.get_account_balance()
  \```

- Get Gain/Loss:

  \```python
  gain_loss = account.get_gainloss()
  \```

- Get Orders:

  \```python
  orders = account.get_orders()
  \```

- Get Positions:

  \```python
  positions = account.get_positions()
  \```

### Trading

- Place Equity Order:

  \```python
  order_response = equity_order.place_order('AAPL', 'buy', 1, 'limit', 150)
  \```

- Place Options Order:

  \```python
  order_response = options_order.place_order('AAPL210917C00125000', 'buy_to_open', 1, 'limit', 3.5)
  \```

### Market Data

- Get Quotes:

  \```python
  quotes_data = quotes.get_quote_day('AAPL')
  \```

- Get Historical Quotes:

  \```python
  historical_data = quotes.get_historical_quotes('AAPL')
  \```

- Get Time Sales:

  \```python
  timesales = quotes.get_timesales('AAPL')
  \```

### Options Data

- Get Options Chains:

  \```python
  options_chains = options_data.get_options_chain('AAPL')
  \```

- Get Options Strikes:

  \```python
  options_strikes = options_data.get_options_strikes('AAPL')
  \```

- Get Options Expirations:

  \```python
  options_expirations = options_data.get_options_expirations('AAPL')
  \```

## Development

To contribute or make changes to the `uvatradier` package, clone the repository, create a virtual environment, and install the dependencies:

\```sh
git clone https://github.com/YOUR_USERNAME/uvatradier.git
cd uvatradier
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
\```

## Testing

Run the tests using `pytest`:

\```sh
pytest
\```

## License

`uvatradier` is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to Tradier for providing a comprehensive trading API.
- Thanks to all the contributors who helped in building and maintaining this package.

## Contact

For any questions or suggestions, feel free to contact the maintainers of this repository.
