import streamlit as st

from bot.orders import submit_order
from bot.client import get_current_price

st.set_page_config(
    page_title="Binance Futures Testnet Bot",
    page_icon="📈",
    layout="centered"
)

st.title("Binance Futures Testnet Trading Bot")

st.markdown(
    "Simple trading interface for Binance Futures Testnet"
)

st.divider()

symbol = st.text_input(
    "Trading Symbol",
    value="BTCUSDT"
)

try:
    current_price = get_current_price(symbol.upper())

    st.info(
        f"Current {symbol.upper()} Price: "
        f"{current_price:,.2f}"
    )

except Exception:
    current_price = None

col1, col2 = st.columns(2)

with col1:
    side = st.selectbox(
        "Side",
        ["BUY", "SELL"]
    )

with col2:
    order_type = st.selectbox(
        "Order Type",
        ["MARKET", "LIMIT"]
    )

quantity = st.number_input(
    "Quantity",
    min_value=0.001,
    value=0.01,
    step=0.001,
    format="%.3f"
)
st.caption(
    "Example: 0.01 means 0.01 BTC (~$627)"
)
price = None

estimated_value = quantity * current_price

st.info(
    f"Estimated Position Value: "
    f"{estimated_value:,.2f}"
)

if order_type == "LIMIT":

    default_price = (
        current_price if current_price
        else 60000.0
    )

    price = st.number_input(
        "Limit Price",
        min_value=1.0,
        value=float(default_price),
        step=100.0
    )

    if current_price:

        if side == "SELL" and price < current_price:

            st.warning(
                "SELL limit price is below "
                "current market price."
            )

        elif side == "BUY" and price > current_price:

            st.warning(
                "BUY limit price is above "
                "current market price."
            )

st.divider()

if st.button(
    "🚀 Place Order",
    use_container_width=True
):

    try:

        with st.spinner(
            "Submitting order..."
        ):

            response = submit_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=str(quantity),
                price=str(price) if price else None
            )

        st.success(
            "Order placed successfully!"
        )

        st.subheader("Order Details")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Order ID",
                response.get("orderId", "N/A")
            )

            st.metric(
                "Status",
                response.get("status", "N/A")
            )

        with c2:
            st.metric(
                "Executed Qty",
                response.get(
                    "executedQty",
                    "N/A"
                )
            )

            st.metric(
                "Symbol",
                response.get(
                    "symbol",
                    "N/A"
                )
            )

        with st.expander(
            "View Full API Response"
        ):
            st.json(response)

    except Exception as e:
        st.error(str(e))