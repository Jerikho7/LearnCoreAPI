import stripe

from config.settings import SECRET_KEY_API

stripe.api_key = SECRET_KEY_API


def create_stripe_product(course):
    """
    Создаёт продукт в Stripe на основе курса.
    Args:
        course: Объект модели Course.
    Returns:
        dict: JSON с id продукта.
    """
    try:
        product = stripe.Product.create(
            name=course.title,
            description=course.description,
        )
        return {"product_id": product.id}
    except stripe.error.StripeError as e:
        return {"error": str(e)}


def create_stripe_price(course, product_id):
    """
    Создаёт цену в Stripe для продукта.
    Args:
        course: Объект модели Course.
        product_id: ID продукта в Stripe.
    Returns:
        dict: JSON с id цены.
    """
    try:
        price = stripe.Price.create(
            product=product_id, unit_amount=int(course.price * 100), currency="rub"  # Цена в копейках
        )
        return {"price_id": price.id}
    except stripe.error.StripeError as e:
        return {"error": str(e)}


def create_stripe_checkout_session(user, course, price_id):
    """
    Создаёт сессию оплаты в Stripe.
    Args:
        user: Объект модели User.
        course: Объект модели Course.
        price_id: ID цены в Stripe.
    Returns:
        dict: JSON с URL сессии и её ID.
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="subscription" if getattr(course, "is_subscription", False) else "payment",
            success_url="http://127.0.0.1:8000/courses/courses/",
            customer_email=user.email,
        )
        return {"payment_url": session.url, "session_id": session.id}
    except stripe.error.StripeError as e:
        return {"error": str(e)}
