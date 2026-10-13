Modo aprendizado ativado.

A `slugify` transforma um texto qualquer em um "slug", um identificador seguro para URLs (ex.: `"Olá, Mundo!"` → `"ola-mundo"`). Ela é uma cadeia de métodos de string em que cada passo recebe o resultado do anterior:

```ts
export function slugify(input: string): string {
```
**Linha 1:** declara e exporta a função. Ela recebe uma `string` e devolve uma `string`.

```ts
  return input
```
**Linha 2:** começa a cadeia a partir do texto de entrada. O valor final da cadeia é o que a função retorna.

```ts
    .normalize("NFD")
```
**Linha 3:** aplica a normalização Unicode **NFD** (decomposição canônica). Caracteres acentuados passam a ser letra-base + acento combinante. Por exemplo, `"é"` vira `"e"` + `"́"`. Sozinho, isso não remove nada, só separa o acento da letra.

```ts
    .replace(/[̀-ͯ]/g, "")
```
**Linha 4:** remove todos os caracteres da faixa `U+0300–U+036F` ("Combining Diacritical Marks"), que é onde ficaram os acentos separados no passo anterior. Assim `"é"` vira `"e"` e `"ç"` vira `"c"`. A flag `g` faz a substituição em todas as ocorrências, não só na primeira.

```ts
    .toLowerCase()
```
**Linha 5:** converte tudo para minúsculas. Isso é necessário porque o próximo regex só aceita `a-z`.

```ts
    .trim()
```
**Linha 6:** remove os espaços em branco do início e do fim.

```ts
    .replace(/[^a-z0-9]+/g, "-")
```
**Linha 7:** troca toda sequência de um ou mais caracteres que **não** são letra minúscula ou dígito por um único hífen. O `^` dentro dos colchetes nega o conjunto, e o `+` agrupa a sequência inteira. Por isso `"ola,   mundo!"` vira `"ola-mundo-"` em vez de `"ola----mundo-"`.

```ts
    .replace(/^-+|-+$/g, "");
```
**Linha 8:** remove os hífens que sobraram no começo (`^-+`) ou no fim (`-+$`) do texto. Eles aparecem quando a string começa ou termina com pontuação, como o `!` do exemplo. O resultado final é `"ola-mundo"`.

```ts
}
```
**Linha 9:** fecha a função.

**Observações:**
- A linha 6 (`trim`) é na prática redundante: a linha 7 já transformaria espaços das pontas em hífens, e a linha 8 os removeria. Ela não faz mal nenhum.
- Caracteres que não se decompõem em letra + acento são descartados, não transliterados. Exemplos: `"ß"`, `"ø"`, `"æ"`, além de emojis e textos em alfabetos não latinos. `"Straße"` vira `"stra-e"`, e uma string só com caracteres japoneses vira `""`.
