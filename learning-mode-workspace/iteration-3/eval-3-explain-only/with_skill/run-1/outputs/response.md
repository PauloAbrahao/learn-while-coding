Modo aprendizado ativado.

A função `slugify` transforma qualquer texto num "slug": uma versão só com letras minúsculas, números e hífens, boa para URLs (ex.: `"  Olá, Mundo!  "` → `"ola-mundo"`). Ela é uma única cadeia de métodos de string, em que cada etapa recebe o resultado da anterior:

```ts
export function slugify(input: string): string {
```
Declara e exporta a função. Recebe uma `string` e devolve uma `string`.

```ts
  return input
```
Começa a cadeia a partir do texto original. Strings em JS são imutáveis, então cada método abaixo devolve uma **nova** string. `input` nunca é alterado.

```ts
    .normalize("NFD")
```
Aplica a normalização Unicode **NFD** (decomposição canônica), que separa letras acentuadas em letra base + acento combinante. Ex.: `"é"` (um caractere) vira `"e"` + `"́"` (dois code points).

```ts
    .replace(/[̀-ͯ]/g, "")
```
Remove todos os caracteres no intervalo `U+0300` a `U+036F`, o bloco "Combining Diacritical Marks". Como o passo anterior soltou os acentos das letras, aqui eles são apagados: `"Olá"` → `"Ola"`, `"ação"` → `"acao"`. A flag `g` faz substituir todas as ocorrências, não só a primeira.

```ts
    .toLowerCase()
```
Converte tudo para minúsculas: `"Ola Mundo"` → `"ola mundo"`.

```ts
    .trim()
```
Tira espaços (e outros espaços em branco, como `\n` e `\t`) do início e do fim.

```ts
    .replace(/[^a-z0-9]+/g, "-")
```
O passo principal. `[^a-z0-9]` casa com qualquer caractere que **não** seja letra minúscula ASCII ou dígito, e o `+` agrupa uma sequência contínua deles. Cada sequência vira um único `-`. Ex.: `"ola, mundo!"` → `"ola-mundo-"` (o `", "` vira um hífen só, e o `"!"` final vira outro).

```ts
    .replace(/^-+|-+$/g, "");
```
Limpa os hífens das pontas: `^-+` casa com hífens no início e `-+$` com hífens no fim (o `|` significa "ou"). Os dois são trocados por nada: `"ola-mundo-"` → `"ola-mundo"`.

```ts
}
```
Fecha a função.

**Exemplo completo**, `"  Ação & Reação!  "`:

| Etapa | Resultado |
|---|---|
| `normalize("NFD")` + remover acentos | `"  Acao & Reacao!  "` |
| `toLowerCase()` | `"  acao & reacao!  "` |
| `trim()` | `"acao & reacao!"` |
| `replace(/[^a-z0-9]+/g, "-")` | `"acao-reacao-"` |
| `replace(/^-+\|-+$/g, "")` | `"acao-reacao"` |

Dois detalhes que vale saber:
- O `trim()` é quase redundante: mesmo sem ele, os espaços das pontas virariam hífens e a última linha os removeria.
- Caracteres que não se decompõem em letra + acento, como `ß`, `ø` e `æ`, ou letras não latinas como `日本`, são **descartados** em vez de transliterados. Um texto só com esses caracteres vira `""`.
