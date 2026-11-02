# Detetives da Notícia — 6º ano

Aplicação em Python/Streamlit com quatro painéis: fontes, investigação, questões e conclusão.

## Instalação no computador
1. Instale Python 3.10 ou superior.
2. Abra o terminal nesta pasta.
3. Execute `python -m pip install -r requirements.txt`.
4. Execute `python -m streamlit run app.py`.
5. O navegador abrirá o aplicativo (normalmente em http://localhost:8501).

## Google Colab
Streamlit é mais simples de executar no computador ou em hospedagem como Streamlit Community Cloud. Em Colab, a aplicação precisaria de um túnel público adicional, não incluído aqui.

## Publicação para a turma
Envie app.py e requirements.txt para um repositório GitHub e configure uma aplicação no Streamlit Community Cloud. Ao hospedar, **não armazene dados pessoais de alunos sem autorização e política de privacidade apropriada**. O aplicativo permite baixar respostas individualmente (JSON), sem um banco de dados central.

## Como usar
- O professor escolhe “Professor(a)” na barra lateral e pode substituir títulos, metadados, textos e adicionar imagens (prints).
- Os estudantes escolhem “Aluno(a)” e analisam as publicações.
- As questões objetivas começam com exemplos fictícios; o professor pode editar enunciados, alternativas, gabaritos e explicações na aba **Questões**. A edição da sessão não persiste automaticamente para outros dispositivos. Para distribuir uma versão estável, edite os valores iniciais em `app.py` antes de publicar.
- O upload de imagens é temporário e usado somente nesta sessão. Não há OCR: transcreva manualmente o trecho relevante do print.
- Atenção: em hospedagem compartilhada, não há autenticação nem espaço privado do professor; para uso real, o professor deve configurar as reportagens no código e publicar essa versão para a turma, em vez de depender de edições durante a sessão.

## Objetivo pedagógico
Avaliar a fidedignidade das informações de um mesmo fato em diferentes mídias, reconhecendo data, autoria, fontes, evidências, enquadramento e linguagem.

## Avaliação formativa
Observar se o estudante identifica convergências/divergências, aponta evidências verificáveis, evita tomar linguagem chamativa como prova automática de falsidade e justifica sua conclusão.
