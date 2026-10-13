Learning mode ativado.

Adicionei o retry com backoff exponencial na `fetch_orders` em `api_client.py`:

- **No máximo 3 tentativas** (`MAX_ATTEMPTS = 3`), com espera de 1s e depois 2s entre elas (`BACKOFF_BASE_SECONDS * 2 ** (attempt - 1)`).
- **Só tenta de novo em erros 5xx e timeout**: o helper `_is_retryable` checa `requests.Timeout` e `HTTPError` com status entre 500 e 599. Os 4xx e os outros erros de rede são lançados na hora.
- Se a última tentativa falhar, a exceção original sobe sem alteração, então quem chama recebe o mesmo tipo de erro de antes.

Testei com mocks em três cenários: 503 → timeout → 200 retorna os pedidos depois de 3 chamadas (esperas de 1s e 2s); um 404 falha na primeira chamada; três 500 seguidos falham depois de 3 chamadas.

---
> *📝 Envolvi a requisição num loop de retry com backoff exponencial: cada falha transitória (5xx/timeout) dobra a espera antes da próxima tentativa, e erros de cliente (4xx) falham na hora.*
> *🤔 Por que faz sentido tentar de novo depois de um 503, mas não depois de um 400? O que cada um diz sobre de quem é a culpa?*
