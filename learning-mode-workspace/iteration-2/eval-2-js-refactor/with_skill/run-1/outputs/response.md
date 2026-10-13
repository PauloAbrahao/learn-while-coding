Learning mode ativado.

Refatorei o `calculateDiscount` em `discount.js`:

```js
function calculateDiscount(user, cart) {
  if (!user || !user.isActive) return 0;
  if (cart.items.length === 0) return 0;

  if (user.tier === "gold") return cart.total * 0.2;
  if (cart.total > 100) return cart.total * 0.1;

  return 0;
}
```

- Os 4 níveis de `if` aninhado viraram checagens planas, e os quatro `else { return 0; }` repetidos sumiram.
- O comportamento é o mesmo. Rodei os casos principais (sem usuário, inativo, carrinho vazio, gold, não-gold acima e abaixo de 100) e todos devolvem o mesmo resultado da versão original.

---
> *📝 Troquei o aninhamento por guard clauses (early return): os casos inválidos saem logo no topo, então as regras de desconto ficam numa leitura linear.*
> *🤔 Se cada `if` aninhado era uma condição que precisava continuar valendo, o que deixa de ser preciso guardar na cabeça quando o caso inválido já saiu?*
