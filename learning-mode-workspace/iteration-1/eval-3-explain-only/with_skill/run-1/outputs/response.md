Modo aprendizado ativado.

A `slugify` transforma qualquer texto em um "slug": uma string só com letras minúsculas sem acento, números e hífens, pronta para usar em URLs (ex.: `"  Olá, Mundo! "` → `"ola-mundo"`). Ela é uma cadeia de métodos de string, em que cada etapa recebe o resultado da anterior:

```ts
export function slugify(input: string): string {
```
Declara e exporta a função. Ela recebe uma `string` e devolve outra `string`.

```ts
  return input
```
Começa a cadeia a partir do texto original. Strings são imutáveis em JS, então cada método abaixo devolve uma **nova** string, e `input` nunca é alterado.

```ts
    .normalize("NFD")
```
Aplica a normalização Unicode **NFD** (decomposição canônica). Ela separa cada caractere acentuado em duas partes: a letra base e o acento como um caractere "combinante" à parte. Por exemplo, `"é"` vira `"e"` + `"́"` (acento agudo).

```ts
    .replace(/[̀-ͯ]/g, "")
```
Remove todos os caracteres da faixa Unicode `U+0300`–`U+036F`, o bloco de *Combining Diacritical Marks* (acentos, til, cedilha etc.). Como a linha anterior isolou os acentos, aqui eles somem e sobra só a letra base: `"ação"` → `"acao"`. A flag `g` faz substituir todas as ocorrências, não só a primeira.

```ts
    .toLowerCase()
```
Converte tudo para minúsculas: `"Acao"` → `"acao"`.

```ts
    .trim()
```
Remove espaços (e outros whitespaces) do começo e do fim.

```ts
    .replace(/[^a-z0-9]+/g, "-")
```
Troca toda **sequência** de um ou mais caracteres que *não* são `a-z` ou `0-9` por um único hífen. O `^` dentro dos colchetes nega a classe, e o `+` agrupa caracteres consecutivos, então `"ola,   mundo!"` vira `"ola-mundo-"` em vez de `"ola----mundo-"`. Espaços, pontuação, emojis e letras não latinas que restaram caem todos aqui.

```ts
    .replace(/^-+|-+$/g, "");
```
Tira hífens que ficaram nas pontas: `^-+` pega hífens no início e `-+$` pega hífens no fim (o `|` é "ou"). `"-ola-mundo-"` → `"ola-mundo"`.

```ts
}
```
Fecha a função.

**Exemplo completo**, `"  Café com Pão! "`:

| Etapa | Resultado |
|---|---|
| entrada | `"  Café com Pão! "` |
| `normalize` + remover acentos | `"  Cafe com Pao! "` |
| `toLowerCase` | `"  cafe com pao! "` |
| `trim` | `"cafe com pao!"` |
| não-alfanuméricos → `-` | `"cafe-com-pao-"` |
| tirar hífens das pontas | `"cafe-com-pao"` |

Dois detalhes que vale notar:
- O `trim()` é quase redundante: mesmo sem ele, os espaços das pontas virariam hífens e a última linha os removeria.
- Texto sem nenhum caractere latino ou dígito (ex.: `"日本語"` ou `"!!!"`) vira string vazia `""`. Quem chama a função talvez precise tratar esse caso.
