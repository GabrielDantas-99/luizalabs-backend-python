class SaldoInsuficienteError(Exception):
    """Levantada quando o saldo é insuficiente para um saque."""


class LimiteSaqueExcedidoError(Exception):
    """Levantada quando o valor do saque ultrapassa o limite permitido."""


class NumeroSaquesExcedidoError(Exception):
    """Levantada quando a quantidade diária de saques é atingida."""


class ValorInvalidoError(Exception):
    """Levantada quando o valor informado é menor ou igual a zero."""
