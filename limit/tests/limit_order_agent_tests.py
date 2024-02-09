
import unittest
from unittest.mock import MagicMock
from limit.limit_order_agent import LimitOrderAgent

class TestLimitOrderAgent(unittest.TestCase):

    def setUp(self):
        # Create a mock execution client for testing
        self.execution_client = MagicMock()

        # Create an instance of LimitOrderAgent with the mock execution client
        self.agent = LimitOrderAgent(self.execution_client)

    def test_add_order(self):
        # Test adding a buy order
        self.agent.add_order(True, "AAPL", 100, 150)
        self.assertIn("AAPL", self.agent._pending_orders)
        self.assertEqual(self.agent._pending_orders["AAPL"], (True, 150, 100))

        # Test adding a sell order
        self.agent.add_order(False, "GOOG", 200, 100)
        self.assertIn("GOOG", self.agent._pending_orders)
        self.assertEqual(self.agent._pending_orders["GOOG"], (False, 100, 200))

    def test_on_price_tick(self):
        # Add some orders
        self.agent.add_order(True, "AAPL", 100, 150)
        self.agent.add_order(False, "GOOG", 200, 100)

        # Test execution of buy order when price drops below limit
        self.agent.on_price_tick("AAPL", 140)
        self.execution_client.buy.assert_called_with("AAPL", 100)

        # Test execution of sell order when price goes above limit
        self.agent.on_price_tick("GOOG", 110)
        self.execution_client.sell.assert_called_with("GOOG", 200)

    def test_on_price_tick_no_matching_order(self):
        # Test on_price_tick when there are no matching orders
        self.agent.on_price_tick("AAPL", 140)
        self.assertFalse(self.execution_client.buy.called)
        self.assertFalse(self.execution_client.sell.called)


if __name__ == "__main__":
    unittest.main()

