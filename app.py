import json
from datetime import datetime
from pathlib import Path
import streamlit as st

st.set_page_config(page_title='Detetives da Notícia | 6º ano', page_icon='📰', layout='wide')
st.markdown('''<style>
.stApp {background:#f5f7fb;color:#182c46} .block-container{max-width:1150px;padding-top:1.4rem}
.hero{background:linear-gradient(115deg,#163b65,#237ca0);padding:25px 30px;border-radius:20px;color:white;margin-bottom:20px}
.hero h1{color:white;margin:0;font-size:2.1rem}.hero p{margin-bottom:0;color:#eaf5ff}
.panel{background:white;border-left:5px solid #1e88a8;border-radius:12px;padding:16px 20px;margin:12px 0;box-shadow:0 2px 10px #19385c12}
.kicker{font-weight:800;color:#136485;font-size:.9rem;text-transform:uppercase;letter-spacing:.06em}
.small{font-size:.95rem;color:#496179}.stButton>button[kind=primary]{background:#126687}
</style>''', unsafe_allow_html=True)

DEFAULT_A = {'titulo':'Chuva forte provoca alagamentos em alguns bairros', 'fonte':'Portal Cidade em Foco (exemplo fictício)', 'data':'15/03/2026', 'autor':'Equipe de reportagem', 'texto':'Após a chuva forte da tarde, ruas de alguns bairros ficaram alagadas. A Defesa Civil informou que recebeu chamados de moradores e orientou a população a evitar áreas inundadas. A reportagem não informa o total de casas atingidas.', 'url':''}
DEFAULT_B = {'titulo':'Cidade inteira ficou debaixo d’água! Veja o caos!', 'fonte':'Perfil Notícias Agora (exemplo fictício)', 'data':'Data não informada', 'autor':'Autor não identificado', 'texto':'Uma publicação afirma que toda a cidade ficou alagada e que milhares de famílias perderam suas casas. O texto não apresenta dados oficiais nem identifica entrevistas ou documentos para sustentar essa afirmação.', 'url':''}
QUESTIONS = [
('Qual das publicações identifica de maneira mais clara a origem das informações?', ['A primeira, pois cita a Defesa Civil.','A segunda, pois usa palavras chamativas.','As duas apresentam as mesmas fontes.','Nenhuma, porque toda notícia é opinião.'],0,'Citar a Defesa Civil permite identificar uma fonte da informação; ainda é importante verificar a notícia.'),
('A expressão “Cidade inteira ficou debaixo d’água!” deve ser analisada com cuidado porque...', ['sempre prova que a notícia é verdadeira.','pode exagerar o alcance do acontecimento sem apresentar evidências.','toda manchete com exclamação é falsa.','substitui a necessidade de entrevistar testemunhas.'],1,'Uma manchete alarmante pede conferência. O exagero não prova, sozinho, que todo o conteúdo seja falso.'),
('Qual informação é comum às duas publicações?', ['Houve chuva e alagamentos.','Milhares de casas foram destruídas.','Toda a cidade ficou inundada.','A prefeitura decretou calamidade.'],0,'As duas mencionam alagamentos; as proporções e os detalhes apresentados são diferentes.'),
('O que ajudaria a verificar quantos bairros foram atingidos?', ['Compartilhar a notícia mais impactante.','Conferir boletins da Defesa Civil e outras fontes confiáveis.','Escolher a notícia com mais curtidas.','Acreditar na notícia publicada primeiro.'],1,'Comparar dados verificáveis com outros registros ajuda a julgar a fidedignidade.'),
('Se a reportagem não mostra a data da publicação, o leitor deve...', ['desconsiderar todas as notícias da internet.','assumir que foi publicada hoje.','procurar a data e conferir se o conteúdo é atual.','repassar a publicação imediatamente.'],2,'Uma notícia antiga pode circular fora do contexto original.'),
('Qual atitude demonstra leitura crítica?', ['Acreditar na imagem sem conferir o contexto.','Repassar a notícia para avisar os colegas imediatamente.','Escolher a manchete com mais emoção.','Comparar autor, data, fontes, evidências e linguagem.'],3,'A análise conjunta de autoria, data, fontes, evidências e linguagem permite uma avaliação melhor.'),
]

if 'questions' not in st.session_state: st.session_state.questions = [(q, opts.copy(), c, why) for q,opts,c,why in QUESTIONS]
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'written' not in st.session_state: st.session_state.written = {}
if 'checked' not in st.session_state: st.session_state.checked = False

st.markdown('<div class="hero"><h1>📰 Detetives da Notícia</h1><p>Missão investigativa • 6º ano do Ensino Fundamental • Leitura crítica de reportagens em diferentes mídias</p></div>', unsafe_allow_html=True)
st.info('🎯 **Objetivo:** avaliar a fidedignidade de informações sobre o mesmo fato em diferentes mídias, verificando fonte, autoria, data, evidências e linguagem.')

with st.sidebar:
    st.header('⚙️ Preparação da atividade')
    modo = st.radio('Modo de uso', ['Aluno(a)', 'Professor(a)'])
    nome = st.text_input('Nome do estudante ou da dupla', placeholder='Ex.: Ana e João')
    turma = st.text_input('Turma', value='6º ano')
    st.caption('A atividade funciona sem internet depois que o Streamlit e suas dependências estiverem instalados. Nenhuma imagem é enviada a serviço externo pelo aplicativo.')
    if st.button('Limpar respostas'):
        st.session_state.answers = {}; st.session_state.written = {}; st.session_state.checked = False; st.rerun()

if 'reports' not in st.session_state: st.session_state.reports = [DEFAULT_A.copy(), DEFAULT_B.copy()]
if 'uploads' not in st.session_state: st.session_state.uploads = [None, None]

if modo == 'Professor(a)':
    st.subheader('Painel do professor | Monte as duas reportagens')
    st.warning('Use duas publicações sobre o MESMO fato. Se houver print, indique também a fonte, a data e o endereço original quando possível. Não trate o texto de um print, isoladamente, como informação verificada.')
    tabs = st.tabs(['Fonte A', 'Fonte B', 'Questões', 'Orientações'])
    for idx in range(2):
        with tabs[idx]:
            report = st.session_state.reports[idx]
            for field, title in [('titulo','Título / manchete'),('fonte','Veículo ou perfil'),('data','Data'),('autor','Autor ou responsável'),('url','Link original (opcional)')]:
                report[field] = st.text_input(title, value=report[field], key=f'{idx}_{field}')
            report['texto'] = st.text_area('Transcrição ou síntese fiel da publicação', value=report['texto'], height=130, key=f'{idx}_texto')
            st.session_state.uploads[idx] = st.file_uploader('Print da reportagem (PNG, JPG ou WEBP)', type=['png','jpg','jpeg','webp'], key=f'img_{idx}')
    with tabs[2]:
        st.caption('Edite as perguntas e o gabarito para combinar com as reportagens escolhidas. As perguntas não são geradas automaticamente por inteligência artificial a partir do print.')
        updated=[]
        for i,(q,opts,c,why) in enumerate(st.session_state.questions):
            with st.expander(f'Questão {i+1}',expanded=i==0):
                q=st.text_input('Enunciado',value=q,key=f'eq{i}')
                opts=[st.text_input(f'Alternativa {"ABCD"[j]}',value=opts[j],key=f'eo{i}_{j}') for j in range(4)]
                c=st.selectbox('Alternativa correta',options=list(range(4)),index=c,format_func=lambda v:'ABCD'[v],key=f'ec{i}')
                why=st.text_area('Explicação do gabarito',value=why,key=f'ew{i}')
                updated.append((q,opts,c,why))
        st.session_state.questions=updated
    with tabs[3]:
        st.markdown('''**Sugestão de mediação (50 min):** 5 min de situação-problema; 10 min de leitura individual; 10 min de comparação em duplas; 15 min de questões; 10 min de socialização.

**Importante:** as questões objetivas são construídas com base nos dois exemplos fictícios iniciais. Caso você substitua as reportagens, revise também as perguntas e o gabarito antes de aplicar. As perguntas discursivas são adequadas à comparação de qualquer par de publicações.

**Cuidados:** ocultar nomes, fotos e dados pessoais de menores nos prints; respeitar direitos de uso de imagens e citar os veículos de origem.''')
    if st.button('Restaurar exemplos fictícios'):
        st.session_state.reports = [DEFAULT_A.copy(), DEFAULT_B.copy()]; st.session_state.questions=[(q,opts.copy(),c,why) for q,opts,c,why in QUESTIONS]; st.rerun()

st.markdown('### Painel 1 | Observe duas versões do mesmo acontecimento')
a, b = st.columns(2, gap='large')
for idx, col in enumerate((a,b)):
    with col:
        r=st.session_state.reports[idx]
        st.markdown(f'<div class="panel"><div class="kicker">📌 Publicação {"A" if idx==0 else "B"}</div><h3>{r["titulo"]}</h3><p><b>Veículo:</b> {r["fonte"]}<br><b>Data:</b> {r["data"]}<br><b>Autoria:</b> {r["autor"]}</p></div>',unsafe_allow_html=True)
        if st.session_state.uploads[idx] is not None:
            st.image(st.session_state.uploads[idx], caption=f'Print da publicação {"A" if idx==0 else "B"}', use_container_width=True)
        st.write(r['texto'])
        if r.get('url'): st.markdown(f'[Consultar publicação original]({r["url"]})')

st.markdown('### Painel 2 | Lupa do investigador')
st.markdown('<div class="panel"><b>🔎 Para cada publicação, observe:</b> Quem escreveu? Quando foi publicada? De onde vêm os dados? Há documentos, entrevistas ou fontes identificáveis? O título exagera? As imagens mostram o fato e a data corretos?</div>',unsafe_allow_html=True)
criteria = ['Autoria identificada', 'Data verificável', 'Fontes e evidências identificáveis', 'Linguagem sem exageros', 'Informações confirmáveis em outra fonte']
comparison = {}
for k in criteria:
    cols=st.columns([2,1,1])
    cols[0].write(k)
    comparison[k] = [cols[1].selectbox('Publicação A', ['Não sei','Sim','Não'],key='a'+k,label_visibility='collapsed'),cols[2].selectbox('Publicação B',['Não sei','Sim','Não'],key='b'+k,label_visibility='collapsed')]
st.caption('Nas colunas: primeira seleção = publicação A; segunda seleção = publicação B. O “não sei” é uma resposta válida quando faltam dados.')

st.markdown('### Painel 3 | Desafio de múltipla escolha')
st.caption('Leia atentamente cada pergunta e escolha a alternativa que pode ser sustentada pelas evidências disponíveis.')
for i, (question,opts,correct,why) in enumerate(st.session_state.questions):
    st.markdown(f'**{i+1}. {question}**')
    choice=st.radio('Escolha uma alternativa',options=list(range(4)),format_func=lambda v:f'{"ABCD"[v]}) {opts[v]}',index=st.session_state.answers.get(i),key=f'q_{i}',label_visibility='collapsed')
    st.session_state.answers[i]=choice
    if st.session_state.checked:
        st.write(('✅ Correto. ' if choice==correct else f'📘 Resposta esperada: {"ABCD"[correct]}. ')+why)

st.markdown('### Painel 4 | Sua conclusão')
writing_prompts = [
'1. Quais informações aparecem nas duas publicações? Quais são diferentes?',
'2. Qual publicação apresenta informações mais verificáveis? Justifique com DUAS pistas do texto ou do print.',
'3. Que informação ainda precisa ser conferida antes de compartilhar a notícia?',
]
for i,q in enumerate(writing_prompts):
    st.session_state.written[i]=st.text_area(q,value=st.session_state.written.get(i,''),height=95,key=f'd_{i}')

if st.button('Conferir minhas respostas',type='primary'):
    st.session_state.checked=True
    st.rerun()
if st.session_state.checked:
    score=sum(st.session_state.answers.get(i)==c for i, (_,_,c,_) in enumerate(st.session_state.questions))
    st.success(f'Você acertou {score} de {len(st.session_state.questions)} questões objetivas. As questões discursivas devem ser analisadas pelo professor.')

result = {'atividade':'Detetives da Notícia — 6º ano','estudante':nome,'turma':turma,'data_registro':datetime.now().isoformat(timespec='seconds'),
          'publicacoes':[{'titulo':r['titulo'],'fonte':r['fonte'],'data':r['data'],'autor':r['autor'],'url':r.get('url','')} for r in st.session_state.reports],
          'comparacao':comparison,'respostas_objetivas':[{'questao':i+1,'alternativa':('ABCD'[st.session_state.answers[i]] if isinstance(st.session_state.answers.get(i),int) else None)} for i in range(len(st.session_state.questions))],
          'respostas_discursivas':[{'pergunta':p,'resposta':st.session_state.written.get(i,'')} for i,p in enumerate(writing_prompts)]}
st.download_button('📥 Baixar minhas respostas (JSON)',data=json.dumps(result,ensure_ascii=False,indent=2),file_name='respostas_detetives_noticia.json',mime='application/json')
st.caption('Material educativo demonstrativo. As duas notícias de exemplo são fictícias e não devem ser apresentadas como fatos reais.')
