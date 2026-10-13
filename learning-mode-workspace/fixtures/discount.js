function calculateDiscount(user, cart) {
  if (user) {
    if (user.isActive) {
      if (cart.items.length > 0) {
        if (user.tier === "gold") {
          return cart.total * 0.2;
        } else {
          if (cart.total > 100) {
            return cart.total * 0.1;
          } else {
            return 0;
          }
        }
      } else {
        return 0;
      }
    } else {
      return 0;
    }
  } else {
    return 0;
  }
}

module.exports = { calculateDiscount };
