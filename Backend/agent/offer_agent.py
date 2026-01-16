from db.mongo import customers_collection, orders_collection

class OfferAgent:

    def check_customer_exists(self, mobile: str):
        return customers_collection.find_one({"mobile": mobile})

    def get_order_count(self, mobile: str) -> int:
        return orders_collection.count_documents({"mobile": mobile})

    def check_offer_eligibility(self, mobile: str) -> dict:
        customer = self.check_customer_exists(mobile)

        if not customer:
            return {
                "response": (
                    "❌ You are not registered with us.\n"
                    "Please sign up and place orders to avail exciting offers.\n"
                    "Happy shopping 🛍️"
                )
            }

        total_orders = self.get_order_count(mobile)

        if total_orders > 2:
            return {
                "response": (
                    f"🎉 Congratulations!\n"
                    f"You are eligible for the special offer.\n"
                    f"Total orders placed: {total_orders}"
                )
            }

        return {
            "response": (
                f"🙂 You have placed {total_orders} orders.\n"
                "Place more than 2 orders to unlock exciting offers!"
            )
        }
