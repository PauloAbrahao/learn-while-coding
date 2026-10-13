Learning mode ativado: daqui pra frente vou explicando o porquê de cada decisão, não só o que mudou.

Adicionei o retry na `fetch_orders` em `api_client.py`.

## O que mudou

```python
import time

import requests

MAX_ATTEMPTS = 3
BASE_DELAY_SECONDS = 0.5


def _is_retryable(exc: Exception) -> bool:
    """Retry only on timeouts and 5xx server errors."""
    if isinstance(exc, requests.Timeout):
        return True
    if isinstance(exc, requests.HTTPError) and exc.response is not None:
        return 500 <= exc.response.status_code < 600
    return False


def fetch_orders(customer_id: str) -> list[dict]:
    url = f"https://api.example.com/customers/{customer_id}/orders"

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()["orders"]
        except (requests.Timeout, requests.HTTPError) as exc:
            if not _is_retryable(exc) or attempt == MAX_ATTEMPTS:
                raise
            # Exponential backoff: 0.5s, 1s, 2s, ...
            time.sleep(BASE_DELAY_SECONDS * 2 ** (attempt - 1))
```

## Por que ficou assim

**1. Por que só 5xx e timeout?**
Um 5xx significa "o servidor falhou", e muitas vezes é passageiro (deploy, sobrecarga), então vale tentar de novo. Um 4xx (404, 401, 400) significa "o seu pedido está errado", e repetir o mesmo pedido vai dar o mesmo erro. Fazer retry em 4xx só atrasa a falha e gera carga à toa. Timeout costuma ser lentidão momentânea, então entra na lista.

**2. Por que `raise_for_status()` + checar o status na exceção?**
`raise_for_status()` lança `HTTPError` tanto para 4xx quanto para 5xx. O `HTTPError` carrega o `response`, então dá pra olhar o `status_code` e decidir. Separei essa decisão em `_is_retryable` pra regra ficar num lugar só, fácil de ler e de testar.

**3. Por que backoff exponencial e não um intervalo fixo?**
Se o servidor está sobrecarregado, bater de novo logo em seguida piora a situação. Dobrar a espera a cada tentativa (0,5s, depois 1s) dá tempo pro serviço se recuperar. Com 3 tentativas há só 2 esperas, então no pior caso são ~1,5s de sleep (mais os timeouts de 5s de cada chamada).

**4. Por que `attempt == MAX_ATTEMPTS` re-lança a exceção original?**
Usar `raise` sem argumento preserva a exceção e o traceback originais. Quem chama `fetch_orders` continua recebendo o mesmo `HTTPError`/`Timeout` de antes, então o contrato da função não mudou, ela só ficou mais insistente.

**5. O que fica de fora de propósito**
- `ConnectionError` (DNS, conexão recusada) **não** tem retry, porque você pediu só 5xx e timeout. Na prática costuma valer incluir. Se quiser, é só adicionar no `_is_retryable` e no `except`.
- Não coloquei *jitter* (um valor aleatório somado ao delay). Ele evita que vários clientes façam retry exatamente no mesmo instante ("thundering herd"). Pra um cliente só, não faz diferença. Com muitos workers, vale a pena.
- Não usei a lib `tenacity` nem o `Retry` do `urllib3`. Fazem isso em uma linha, mas o loop explícito deixa claro o que acontece, que é o objetivo aqui.

## Como testei

Simulei respostas com `mock` (sem rede, com `time.sleep` substituído):
- 503 → timeout → 200: retorna os pedidos, com esperas de `[0.5, 1.0]`
- 404: lança na hora, sem retry
- 500 nas três tentativas: lança `HTTPError` depois de esperar `[0.5, 1.0]`

**Pra fixar:** se a API devolvesse **429 Too Many Requests**, você acha que deveria entrar no retry? E o que o header `Retry-After` mudaria na conta do backoff?
