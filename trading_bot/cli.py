import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from bot.client import get_client
from bot.orders import place_market_order, place_limit_order, place_stop_limit_order, parse_order_response,set_leverage
from bot.validators import validate_all
from bot.logging_config import setup_logger

console = Console()
logger = setup_logger("cli")


def print_order_summary(symbol, side, order_type, quantity, price=None, stop_price=None, leverage=None):
    table = Table(title="📋 Order Request Summary", box=box.ROUNDED, style="cyan")
    table.add_column("Field", style="bold white")
    table.add_column("Value", style="yellow")
    table.add_row("Symbol", symbol)
    table.add_row("Side", side)
    table.add_row("Order Type", order_type)
    table.add_row("Quantity", str(quantity))
    table.add_row("Leverage", f"{leverage}x" if leverage else "10x")
    if price:
        table.add_row("Price", str(price))
    if stop_price:
        table.add_row("Stop Price", str(stop_price))
    console.print(table)


def print_order_response(response: dict):
    table = Table(title="✅ Order Response", box=box.ROUNDED, style="green")
    table.add_column("Field", style="bold white")
    table.add_column("Value", style="bright_green")
    for key, value in response.items():
        if value is not None:
            table.add_row(key, str(value))
    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol",     required=True,  help="Trading pair e.g. BTCUSDT")
    parser.add_argument("--side",       required=True,  help="BUY or SELL")
    parser.add_argument("--type",       required=True,  dest="order_type", help="MARKET, LIMIT, or STOP-LIMIT")
    parser.add_argument("--quantity",   required=True,  help="Order quantity")
    parser.add_argument("--price",      required=False, default=None, help="Limit price (required for LIMIT/STOP-LIMIT)")
    parser.add_argument("--stop-price", required=False, default=None, dest="stop_price", help="Stop price (required for STOP-LIMIT)")
    parser.add_argument("--leverage", required=False, default="10", help="Leverage 1-125 (default: 10)")

    args = parser.parse_args()

    console.print(Panel.fit("🤖 [bold cyan]Binance Futures Testnet Trading Bot[/bold cyan]"))

    # Validate inputs
    try:
        params = validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
            leverage=args.leverage 
        )
        logger.info(f"Validated inputs: {params}")
    except ValueError as e:
        console.print(f"\n[bold red]❌ Validation Error:[/bold red] {e}\n")
        logger.error(f"Validation failed: {e}")
        return

    # Print summary
    print_order_summary(
        symbol=params["symbol"],
        side=params["side"],
        order_type=params["order_type"],
        quantity=params["quantity"],
        price=params.get("price"),
        stop_price=params.get("stop_price"),
        leverage=params.get("leverage")
    )

    # Confirm
    confirm = input("\n⚠️  Confirm placing this order? (y/n): ").strip().lower()
    if confirm != "y":
        console.print("[yellow]Order cancelled by user.[/yellow]")
        logger.info("Order cancelled by user.")
        return

    # Init client
    try:
        client = get_client()
        set_leverage(client, params["symbol"], params["leverage"])
    except Exception as e:
        console.print(f"\n[bold red]❌ Client Error:[/bold red] {e}\n")
        return

    # Place order
    try:
        if params["order_type"] == "MARKET":
            response = place_market_order(client, params["symbol"], params["side"], params["quantity"])
        elif params["order_type"] == "LIMIT":
            response = place_limit_order(client, params["symbol"], params["side"], params["quantity"], params["price"])
        elif params["order_type"] == "STOP-LIMIT":
            response = place_stop_limit_order(client, params["symbol"], params["side"], params["quantity"], params["price"], params["stop_price"])

        parsed = parse_order_response(response)
        print_order_response(parsed)
        console.print("\n[bold green]✅ Order placed successfully![/bold green]\n")
        logger.info(f"Order placed successfully: {parsed}")
        logger.info("-"*200)

    except Exception as e:
        console.print(f"\n[bold red]❌ Order Failed:[/bold red] {e}\n")
        logger.error(f"Order placement failed: {e}")


if __name__ == "__main__":
    main()