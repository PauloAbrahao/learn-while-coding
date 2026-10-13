Learning mode ativado.

Adicionei retry com backoff exponencial na `fetch_orders` (`api_client.py`):

- **Até 3 tentativas** no total (`MAX_ATTEMPTS = 3`).
- **Só repete** em `requests.Timeout` e em `HTTPError` com status 5xx. A checagem fica no helper `_is_retryable`.
- **Backoff:** espera 0,5s e depois 1s entre as tentativas (`BASE_DELAY_SECONDS * 2 ** (attempt - 1)`).
- Erros 4xx, de conexão e outros sobem na hora, sem retry. Se a última tentativa falhar, a exceção original é relançada.

Testei com mocks: 503 → timeout → 200 retorna os pedidos após 3 chamadas; 404 falha na 1ª chamada; 500 em todas falha após 3 chamadas.

---
> *📝 Envolvi a requisição num loop de retry com backoff exponencial: cada falha transitória (5xx/timeout) dobra a espera antes da próxima tentativa, e erros 4xx falham na hora.*
> *🤔 Por que repetir um 503 pode dar certo, mas repetir exatamente a mesma requisição que deu 400 nunca dá?*
