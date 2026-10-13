Learning mode ativado.

Refatorei o `calculateDiscount` em `discount.js`: os 4 níveis de `if` aninhado viraram uma sequência plana de verificações, cada uma com `return` direto.

```js
function calculateDiscount(user, cart) {
  if (!user || !user.isActive) return 0;
  if (cart.items.length === 0) return 0;

  if (user.tier === "gold") return cart.total * 0.2;
  if (cart.total > 100) return cart.total * 0.1;

  return 0;
}
```

O comportamento não mudou. Testei 7 casos contra a versão original (sem usuário, usuário inativo, carrinho vazio, gold com total baixo, não-gold acima de 100, exatamente 100 e abaixo de 100) e todos deram o mesmo resultado.

---
> *📝 Troquei os ifs aninhados por guard clauses (early return): os casos sem desconto saem logo no começo, e a regra de desconto fica lida de cima para baixo.*
> *🤔 Se o resultado é idêntico, por que a ordem em que lemos as condições muda tanto a facilidade de entender o código?*
