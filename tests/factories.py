"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal
from service.models import Product


class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        """Maps factory to data model"""
        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(
        choices=[
            "Hat",
            "Shoes",
            "Big Mac",
            "Sheets",
            "Laptop",
            "Tablet",
            "Phone",
            "Book"
        ]
    )
    description = factory.Faker("text")
    price = FuzzyDecimal(0.5, 2000.0, 2)
    available = FuzzyChoice(choices=[True, False])
    category = FuzzyChoice(
        choices=[
            "CLOTHS",
            "FOOD",
            "HOUSEWARES",
            "AUTOMOTIVE",
            "TOOLS",
            "ELECTRONICS",
            "BOOKS"
        ]
    )