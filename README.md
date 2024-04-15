# Sistema de Gestão para o Projeto ELLP

## Contexto
A Universidade Tecnológica Federal do Paraná (UTFPR) abriga o projeto "ELLP - Ensino Lúdico de Lógica e Programação", destacando-se entre os 1.552 projetos de extensão ativos. A gestão eficiente deste projeto requer organização meticulosa, desde o arquivamento dos registros dos membros até o gerenciamento do banco de horas.

## Justificativa
O armazenamento tradicional em papel dos documentos e do banco de horas relacionados a projetos de extensão na UTFPR tem levado a problemas de perda, desorganização e redundância de informações. A dificuldade em gerenciar efetivamente esses projetos afeta tanto alunos quanto docentes, com impacto direto no registro de horas de atividades extracurriculares.

## Proposta
Propomos a implementação de um sistema de gestão de presença em tempo real, por meio de uma aplicação desktop e um Sistema Gerenciador de Banco de Dados (SGBD). Esse sistema permitirá que discentes e docentes monitorem as atividades do projeto ELLP digitalmente, facilitando o acompanhamento e a organização.

## Integrantes do grupo

- Vinicius Sussumu Vieira Ogawa
- Pedro Henrique Ferreira Vinchi
- Willian Gomes Zentil

## Requisitos funcionais

| Código | Descrição                                       |
|--------|-------------------------------------------------|
| RF01   | Cadastro de professores                         |
| RF02   | Cadastro de oficinas                            |
| RF03   | Autenticação de professores                     |
| RF04   | Consultar e Alterar dados de professores        |
| RF05   | Consultar e Alterar dados de oficinas           |
| RF06   | Registro de Presença                            |
| RF07   | Visualizar Histórico de Presença                |
| RF08   | Geração de certificados para os alunos presentes|
| RF09   | Editar registros de presença                    |

## Arquiteura do projeto

![Arquitetura do Projeto](/arquitetura.png)

## Configuração Inicial

Recomendamos a utilização de um ambiente virtual para instalar e executar este projeto:

```bash
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
```

Instale todas as dependências do projeto com o seguinte comando:

```bash
pip install -r requirements.txt
```

Configure seu banco de dados no arquivo .env e ajuste as variáveis de ambiente conforme necessário.

Execute as migrações necessárias com:

```bash
python manage.py migrate
```

Inicie o servidor de desenvolvimento com:
```bash
python manage.py runserver
```

## Executando Testes

Para executar os testes, use o comando pytest no terminal:

```bash
pytest
```

pytest irá automaticamente encontrar e executar todos os testes no projeto que correspondam aos padrões de nomeação especificados.
