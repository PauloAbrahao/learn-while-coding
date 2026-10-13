function calculateDiscount(user, cart) {
  if (!user || !user.isActive) return 0;
  if (cart.items.length === 0) return 0;

  if (user.tier === "gold") return cart.total * 0.2;
  if (cart.total > 100) return cart.total * 0.1;

  return 0;
}

module.exports = { calculateDiscount };
