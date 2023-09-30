# Seed Chat GPT with Contextual Sales Data

This repo explores the idea that we can seed Chat GPT with contextual CSV sales order data. So that 
a user can ask natural language questions and get back details about certain order data (related to a single customer).  
These could be things like order status, when an order was shipped, expected delivery date, what items are on the order, and more.
The sales order data could be provided from any data source, so any ecommerce company could 
leverage this kind of technology. It could be used by internal stakeholders or by external customers engaging in an AI chat bot.

Sample CSV sales data is provided in the data folder, and loaded into a Pandas dataframe by the app.

## Installation

Requires Python 3.8 or newer.

Create an [openai account](https://platform.openai.com/) if you do not already have one.

Obtain an API key from the [api keys](https://platform.openai.com/account/api-keys) account page, and seed your account with money to make requests. 
As of 9/29/2023 you could seed your account with as little as $10 to get started.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages from requirements.txt.

```bash
pip install -r requirements.txt
```

Set your api key in your .zshrc file.

```bash
export CHATGPT_API_KEY=your-api-key-from-your-openai-account
```

## Usage

Start the development server:

```bash
python app.py
```

Make a curl POST request:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"customer_id":"778","user_request":"List the distinct product lines on order 10292"}' \
  http://localhost:5000/api/chat
```

Example response:

```json
{
  "response": "The distinct product lines on order 10292 are:\n\n1. Classic Cars\n2. Trucks and Buses\n3. Trains"
}
```

Example response screenshots:

![distinct product lines response](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/distinct-product-lines-response.png?raw=true)
![distinct product lines csv](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/distinct-product-lines-csv.png?raw=true)

![total quantity ordered response](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/total-quantity-ordered-response.png?raw=true)
![total quantity ordered csv](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/total-quantity-ordered-csv.png?raw=true)

![order status by date response](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/order-status-by-date-response.png?raw=true)
![order status by date csv](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/order-status-by-date-csv.png?raw=true)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)