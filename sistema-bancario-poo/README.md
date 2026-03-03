Sistema Bancário - Refatorado com boas práticas de OOP em Python.

Melhorias aplicadas:

- Encapsulamento real com properties (sem atributos públicos mutáveis)
- abstractmethod correto (abstractclassmethod/abstractproperty foram depreciados)
- Tipagem completa com `from __future__ import annotations` para forward references
- Consistência nos tipos de retorno e nas assinaturas
- Separação de responsabilidades: UI (Banco) isolada do domínio
- Classe Banco como ponto de entrada e controlador do estado da aplicação
- Tratamento de erros com exceções customizadas em vez de prints misturados à lógica
- Formatação de strftime corrigida (%s → %S)
- Property `numero` corrigida (retornava `saldo` por engano)
- `filtrar_cliente` retorna None de forma explícita (sem efeito colateral de print)
- Docstrings em todas as classes e métodos públicos
