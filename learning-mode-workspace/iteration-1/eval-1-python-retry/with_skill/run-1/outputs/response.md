Learning mode ativado.

Adicionei retry com backoff exponencial na `fetch_orders` em `api_client.py`:

- **Até 3 tentativas** no total (`MAX_ATTEMPTS = 3`).
- **Só tenta de novo** em `requests.Timeout` ou em `HTTPError` com status 5xx; isso fica no helper `_is_retryable`. Erros 4xx, falhas de conexão e problemas no JSON sobem na hora.
- **Backoff:** espera 0.5s antes da 2ª tentativa e 1s antes da 3ª (`BASE_DELAY_SECONDS * 2 ** (attempt - 1)`).
- Quando a última tentativa falha, a exceção original é relançada, então quem chama a função continua recebendo o mesmo tipo de erro de antes.

Testei com `requests.get` mockado: 503 → timeout → 200 retorna os pedidos depois de 3 chamadas, com esperas de 0.5s e 1s. Um 404 falha logo na 1ª chamada, e três 500 seguidos desistem depois de 3 chamadas.

---
> *📝 O retry só vale para falhas **transitórias**: 5xx e timeout podem dar certo numa nova tentativa, já um 4xx vai falhar sempre do mesmo jeito. O backoff exponencial (0.5s, 1s) dobra a espera a cada falha, o que dá tempo para um servidor sobrecarregado se recuperar em vez de ser bombardeado.*
> *🤔 Se mil clientes recebem o mesmo 503 no mesmo instante e todos seguem exatamente esse backoff, o que acontece com o servidor quando chega a hora de tentar de novo, e o que faltaria para evitar isso?*
