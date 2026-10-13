Refatorei o `calculateDiscount`. Os 5 níveis de `if` aninhado viraram uma sequência plana:

```js
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
```

Rodei as duas versões lado a lado com várias combinações de entrada (usuário nulo ou inativo, carrinho vazio, gold e não-gold, total abaixo de 100, igual a 100 e acima) e todas deram o mesmo resultado. O comportamento não mudou.

## 📚 Learning mode: o que aconteceu aqui

**1. Guard clauses (retorno antecipado)**
O código original tinha a forma "se tudo estiver ok, entra mais um nível… senão `return 0`". Cada `else { return 0; }` ficava longe do `if` que o abria, e para entender um deles você precisava contar as chaves.

A técnica é **inverter a condição e sair logo**: em vez de `if (user) { ...todo o resto... } else { return 0 }`, você escreve `if (!user) return 0;` e segue em frente. Depois de cada guard, o leitor sabe que aquela condição vale para o resto da função. Isso é o que deixa o código plano.

> Regra prática: quando um `else` só tem `return`/`throw`, ele quase sempre pode virar uma guard clause.

**2. Por que juntar `!user || !user.isActive` é seguro**
O `||` faz *short-circuit*: se `!user` for `true`, o JS nem avalia `user.isActive`, então não dá `TypeError` com `user` nulo. Foi isso que permitiu juntar dois `if` numa linha só.

**3. A ordem das guards importa**
Mantive a checagem do `user` *antes* da do `cart`. No original, se `user` fosse `null`, o `cart` nunca era acessado. Então `calculateDiscount(null, null)` retornava `0` sem quebrar, e a nova versão preserva isso. Se eu invertesse a ordem, essa chamada passaria a lançar erro. Em refatoração, o objetivo é **mudar a forma sem mudar o comportamento**, inclusive nesses casos de borda.

**4. Constantes nomeadas em vez de "números mágicos"**
`0.2`, `0.1` e `100` agora têm nome. `cart.total > BIG_CART_THRESHOLD` explica a regra de negócio sozinho, e se o limite mudar você altera em um lugar só.

**5. O `else` depois de `return` some**
Depois que um `if` retorna, o `else` é redundante, porque o código abaixo só roda quando a condição for falsa. Foi por isso que o `if (gold) ... else if (total > 100) ... else 0` virou três linhas independentes.

### Para praticar
- Experimente escrever um teste para `calculateDiscount({ isActive: true, tier: "gold" }, { items: [], total: 500 })`. Qual o resultado esperado e por quê?
- Uma pergunta para pensar: hoje um usuário gold sempre recebe 20%, mesmo com total baixo. É essa a regra de negócio, ou o desconto gold também deveria exigir um mínimo? A refatoração deixou essa regra bem mais visível, e esse é outro benefício de código legível.
