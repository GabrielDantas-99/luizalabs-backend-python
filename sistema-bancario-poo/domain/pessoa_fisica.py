class PessoaFisica:
    """Representa os dados básicos de uma pessoa física."""

    def __init__(self, nome: str, data_nascimento: str, cpf: str) -> None:
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def data_nascimento(self) -> str:
        return self._data_nascimento

    @property
    def cpf(self) -> str:
        return self._cpf

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nome={self._nome!r}, cpf={self._cpf!r})"
