import logging
import os
import json
from typing import Dict, Union, Optional
import uuid
import datetime
from decimal import Decimal

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
TRANSACTION_FEE_PERCENTAGE = Decimal('0.02')  # 2% transaction fee
DEFAULT_CURRENCY = "USD"

class InvalidAmountError(ValueError):
    pass

class InvalidCurrencyError(ValueError):
    pass

class PaymentGatewayError(Exception):
    pass


# Data validation functions
def validate_amount(amount: Union[int, float, Decimal]) -> Decimal:
    """Validates and converts the amount to a Decimal."""
    try:
        amount = Decimal(amount)
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive.")
        return amount.quantize(Decimal('0.00'))  # Ensure at most two decimal places
    except (ValueError, TypeError):
        raise InvalidAmountError("Invalid amount format.")

def validate_currency(currency: str) -> str:
    """Validates the currency code."""
    if not isinstance(currency, str) or len(currency) != 3:
        raise InvalidCurrencyError("Currency code must be a 3-letter string.")
    return currency.upper() # Standardize to uppercase

# Payment processing functions
def calculate_transaction_fee(amount: Decimal) -> Decimal:
    """Calculates the transaction fee."""
    return (amount * TRANSACTION_FEE_PERCENTAGE).quantize(Decimal('0.00'))

def process_payment(amount: Union[int, float, Decimal], currency: str = DEFAULT_CURRENCY) -> Dict[str, Union[str, Decimal]]:
    """Processes a payment and returns a transaction record."""
    try:
        amount = validate_amount(amount)
        currency = validate_currency(currency)
        transaction_fee = calculate_transaction_fee(amount)
        net_amount = amount - transaction_fee

        transaction_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        transaction_record = {
            "transaction_id": transaction_id,
            "timestamp": timestamp,
            "amount": amount,
            "currency": currency,
            "transaction_fee": transaction_fee,
            "net_amount": net_amount,
            "status": "success"
        }

        logging.info(f"Payment processed successfully. Transaction ID: {transaction_id}")
        return transaction_record

    except (InvalidAmountError, InvalidCurrencyError) as e:
        logging.error(f"Payment processing failed: {e}")
        raise PaymentGatewayError(str(e))
    except Exception as e:
        logging.exception("Unexpected error during payment processing.")  # Log full stack trace
        raise PaymentGatewayError(f"Unexpected error: {e}")

# Example Usage (can be removed for production)
if __name__ == "__main__":
    try:
        payment_result = process_payment(100.50, "USD")
        print(json.dumps(payment_result, indent=2))

        payment_result = process_payment(100, "EUR")
        print(json.dumps(payment_result, indent=2))

        # Example with invalid amount
        # payment_result = process_payment(-10, "USD") # This will raise an exception

        # Example with invalid currency
        # payment_result = process_payment(100, "US") # This will raise an exception

    except PaymentGatewayError as e:
        print(f"Payment failed: {e}")