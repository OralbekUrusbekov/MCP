from typing import Dict, Any


class CalculatorTool:

    @staticmethod
    def calculate_discount(price: float, discount_percent: float) -> Dict[str, Any]:
        discount_amount = price * (discount_percent / 100)
        final_price = price - discount_amount

        return {
            'original_price': price,
            'discount_percent': discount_percent,
            'discount_amount': round(discount_amount, 2),
            'final_price': round(final_price, 2)
        }

    @staticmethod
    def add_tax(price: float, tax_percent: float) -> Dict[str, Any]:
        tax_amount = price * (tax_percent / 100)
        total_price = price + tax_amount

        return {
            'original_price': price,
            'tax_percent': tax_percent,
            'tax_amount': round(tax_amount, 2),
            'total_price': round(total_price, 2)
        }


class FormatterTool:

    @staticmethod
    def format_product_list(products: list) -> str:
        if not products:
            return "Өнімдер табылмады."

        formatted = []
        for product in products:
            stock_status = "✓ Қолда бар" if product.get('in_stock') else "✗ Қолда жоқ"
            formatted.append(
                f"ID: {product['id']}\n"
                f"  Атауы: {product['name']}\n"
                f"  Бағасы: {product['price']} ₸\n"
                f"  Категория: {product['category']}\n"
                f"  Статус: {stock_status}\n"
            )

        return "\n".join(formatted)

    @staticmethod
    def format_statistics(stats: Dict[str, Any]) -> str:
        result = [
            f"Жалпы өнімдер саны: {stats['total_products']}",
            f"Орташа баға: {stats['average_price']} ₸",
            f"Қолда бар өнімдер: {stats['in_stock_count']}",
            f"Қолда жоқ өнімдер: {stats['out_of_stock_count']}",
            "\nКатегориялар бойынша:"
        ]

        for category, count in stats['categories'].items():
            result.append(f"  {category}: {count} өнім")

        return "\n".join(result)

calculator = CalculatorTool()
formatter = FormatterTool()