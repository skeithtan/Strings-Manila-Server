from entity_management.models import ProductDescription
from django.db.models import Model, ForeignKey, DateTimeField, FloatField


class ProductOccurrence(Model):
    product = ForeignKey(ProductDescription)
    date = DateTimeField(auto_now_add=True)

    @staticmethod
    def increment_for_product(product):
        ProductOccurrence.objects.create(product=product)

    @staticmethod
    def count_for_product(product):
        return ProductOccurrence.objects.filter(product=product).count()


class ProductPairOccurrence(Model):
    product_1 = ForeignKey(ProductDescription, related_name="product_1")
    product_2 = ForeignKey(ProductDescription, related_name="product_2")
    date = DateTimeField(auto_now_add=True)

    @staticmethod
    def count_for_pair(product_1, product_2):
        pair_1_head = ProductPairOccurrence.objects.filter(product_1=product_1, product_2=product_2)
        pair_2_head = ProductPairOccurrence.objects.filter(product_1=product_2, product_2=product_1)

        return pair_1_head.count() + pair_2_head.count()

    @staticmethod
    def increment_for_pair(product_1, product_2):
        ProductPairOccurrence.objects.create(product_1=product_1, product_2=product_2)


class Recommendation(Model):
    root_product = ForeignKey(ProductDescription, related_name="root_product")
    associated_product = ForeignKey(ProductDescription, related_name="associated_product")
    confidence = FloatField(default=0)
    lift = FloatField(default=0)

    def __str__(self):
        return f"{self.root_product.name} - {self.associated_product.name} - C{self.confidence} - L{self.lift}"

    @staticmethod
    def recommendation_for_product(product):
        recommendations = Recommendation.objects.filter(root_product=product, lift__gt=1, confidence__gt=0).order_by(
            "-confidence")
        recommendations = recommendations[:3]

        return [recommendation.associated_product for recommendation in recommendations]

    @staticmethod
    def set_recommendation(root_product, associated_product, lift, confidence):
        Recommendation.objects.update_or_create(root_product=root_product,
                                                associated_product=associated_product,
                                                defaults={
                                                    "lift": lift,
                                                    "confidence": confidence
                                                })
