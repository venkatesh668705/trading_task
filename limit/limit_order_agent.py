from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self._execution_client = execution_client
        self._pending_orders: Dict[str, Tuple[bool, float, int]] = {}  # (buy/sell, limit_price, amount)

    def add_order(self,buy: bool,product_id: str,amount: int,limit_price: float,) -> None:
        """
        Add a new limit order to the agent.

        Args:
            buy: True for buy, False for sell.
            product_id: The product identifier.
            amount: The quantity to buy/sell.
            limit_price: The maximum price for buy or minimum price for sell.
        """
        self._pending_orders[product_id] = (buy, limit_price, amount)
    def on_price_tick(self, product_id: str, price: float):
        
        """
        Check for and execute matching orders whenever a price tick arrives.

        Args:
            product_id: The product identifier for the price update.
            price: The current market price of the product.
        """
        if product_id in self._pending_orders:
            buy, limit_price, amount = self._pending_orders.pop(product_id)

            if (buy and price <= limit_price) or (not buy and price >= limit_price):
                try:
                    if buy:
                        self._execution_client.buy(product_id, amount)
                    else:
                        self._execution_client.sell(product_id, amount)
                    print(f"Executed order: {product_id}, {'buy' if buy else 'sell'}, {amount}, {limit_price}")
                except ExecutionException as e:
                    print(f"Execution failed for {product_id}: {e}")


