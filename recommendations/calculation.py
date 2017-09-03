from datetime import datetime, timedelta

from orders.models import Order
from entity_management.models import ProductDescription
from .models import Recommendation, ProductOccurrence, ProductPairOccurrence


def calculate_recommendations():
    # Wipe data older than five weeks
    print("Calculating recommendations...")
    five_weeks_ago = datetime.now() - timedelta(weeks=5)
    print(f"Wiping occurrence data older than {five_weeks_ago.strftime('%b %d, %Y')}")

    ProductOccurrence.objects.filter(date__lte=five_weeks_ago).delete()
    ProductPairOccurrence.objects.filter(date__lte=five_weeks_ago).delete()

    all_transactions_count = Order.objects.filter(date_ordered__gte=five_weeks_ago).count()

    if all_transactions_count == 0:
        # Cannot divide by 0
        return

    Recommendation.objects.all().delete()  # Remove previous recommendations
    all_products = ProductDescription.objects.filter(is_active=True)

    for root_product in all_products:
        print(f"Calculating recommendations for {root_product}")
        for associated_product in all_products:

            if root_product == associated_product:
                # Cannot recommend product to itself
                continue

            associated_occurrence = ProductOccurrence.count_for_product(associated_product)
            associated_support = associated_occurrence / all_transactions_count

            if associated_support == 0:
                # Cannot divide by 0
                continue

            pair_occurrence = ProductPairOccurrence.count_for_pair(root_product, associated_product)
            pair_support = pair_occurrence / all_transactions_count

            confidence = pair_support / associated_support

            root_occurrence = ProductOccurrence.count_for_product(root_product)
            root_support = root_occurrence / all_transactions_count

            if root_support == 0:
                # Cannot divide by 0
                continue

            lift = confidence / root_support
            Recommendation.set_recommendation(root_product, associated_product, lift, confidence)

    print("Recommendation calculation done.")
