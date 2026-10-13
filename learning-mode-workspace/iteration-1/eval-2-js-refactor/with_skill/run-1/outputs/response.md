Learning mode ligado.

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

- Os 5 níveis de `if` aninhado viraram uma lista plana de checagens.
- O comportamento é o mesmo. Comparei as duas versões com combinações de usuário nulo, inativo, gold e não-gold, carrinho vazio e totais de 50, 100 e 150, e todas deram o mesmo resultado.
- A ordem das checagens foi mantida. O `user` continua sendo validado antes de acessar `cart`, então `calculateDiscount(null, null)` ainda retorna `0` sem lançar erro.

---
> *📝 Troquei os ifs aninhados por guard clauses (early return). Cada caso em que não há desconto sai logo no topo, e as regras de desconto de verdade (gold → 20%, total > 100 → 10%) ficam no nível mais raso, lidas de cima para baixo como uma tabela de prioridade. A ordem importa: o `gold` vem antes do `> 100`, então um gold com carrinho de 150 ganha 20%, não 10%.*
> *🤔 Se a lógica final é a mesma, por que ler "o que não serve" primeiro deixa mais fácil entender "o que serve"? E em que ponto essa sequência de returns começaria a ficar tão difícil de ler quanto o aninhamento original?*
