"""
Shop logic system

"""

class ShopItem:
    def __init__(self, name, description, price, effect_type, effect_value, icon="🎁"):
        self.name = name
        self.description = description
        self.price = price
        self.effect_type = effect_type  # 'hunger', 'energy', 'mood', 'cleanliness'
        self.effect_value = effect_value
        self.icon = icon

class Shop:
    def __init__(self):
        self.items = [
            ShopItem("Premium Steak", "Huge hunger fill", 50, "hunger", 60, "🥩"),
            ShopItem("Energy Drink", "Instant boost", 40, "energy", 80, "🥤"),
            ShopItem("Golden Ball", "Massive mood boost", 30, "mood", 50, "🥎"),
            ShopItem("Royal Spa", "Ultimate clean", 35, "cleanliness", 70, "🛁"),
            ShopItem("Magic Snack", "Small treat", 10, "hunger", 15, "🍪")
        ]
    
    def buy_item(self, item, pet):
        """Process item purchase"""
        if pet.coins < item.price:
            return False, "Not enough coins!", pet.coins
        
        # Apply effect
        if hasattr(pet, item.effect_type):
            current = getattr(pet, item.effect_type)
            setattr(pet, item.effect_type, min(100, current + item.effect_value))
            
            # Deduct cost
            pet.coins -= item.price
            
            # Bonus XP for buying things
            pet.add_exp(5)
            
            return True, f"Bought {item.name}!", pet.coins
        else:
            return False, "Invalid item effect", pet.coins