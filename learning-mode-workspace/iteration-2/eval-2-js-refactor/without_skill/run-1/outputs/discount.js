const GOLD_RATE = 0.2;
const BIG_CART_RATE = 0.1;
const BIG_CART_THRESHOLD = 100;

function calculateDiscount(user, cart) {
  // Guard clauses: casos sem desconto saem logo no início
  if (!user || !user.isActive) return 0;
  if (cart.items.length === 0) return 0;

  if (user.tier === "gold") return cart.total * GOLD_RATE;
  if (cart.total > BIG_CART_THRESHOLD) return cart.total * BIG_CART_RATE;

  return 0;
}

module.exports = { calculateDiscount };
