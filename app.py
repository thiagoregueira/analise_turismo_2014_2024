import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
import folium
from streamlit_folium import folium_static

# Configuração da página
st.set_page_config(
    page_title="Dashboard Turismo Brasil - 2014 a 2024",
     layout="wide",
     page_icon=":earth_americas:",
     initial_sidebar_state="expanded"
     )

# Definindo paletas de cores mais diversificadas
COLOR_PALETTE = {
    'primary': '#1f77b4',
    'secondary': '#2ecc71',
    'accent': '#e74c3c',
    'sequential': px.colors.qualitative.Set3,  # Paleta com várias cores diferentes
    'region_colors': px.colors.qualitative.Set1  # Paleta específica para regiões
}

# Estilo base para todos os gráficos
CHART_STYLE = {
    'template': 'plotly_white',
    'title': {'font_size': 24, 'font_family': 'Arial'},
    'axis': {
        'title_font_size': 14,
        'gridcolor': '#f0f0f0',
        'showgrid': True
    }
}

# Carregando os dados
@st.cache_data
def load_data():
    df = pd.read_csv('df_turismo_all.csv')
    # Converter mes_ano para datetime
    df['mes_ano'] = pd.to_datetime(df['mes_ano'])
    
    # Padronizar os nomes dos meses
    meses_map = {
        'janeiro': 'Janeiro', 'Janeiro': 'Janeiro',
        'fevereiro': 'Fevereiro', 'Fevereiro': 'Fevereiro',
        'março': 'Março', 'Marco': 'Março', 'marco': 'Março', 'Março': 'Março',
        'abril': 'Abril', 'Abril': 'Abril',
        'maio': 'Maio', 'Maio': 'Maio',
        'junho': 'Junho', 'Junho': 'Junho',
        'julho': 'Julho', 'Julho': 'Julho',
        'agosto': 'Agosto', 'Agosto': 'Agosto',
        'setembro': 'Setembro', 'Setembro': 'Setembro',
        'outubro': 'Outubro', 'Outubro': 'Outubro',
        'novembro': 'Novembro', 'Novembro': 'Novembro',
        'dezembro': 'Dezembro', 'Dezembro': 'Dezembro'
    }
    df['mes'] = df['mes'].map(meses_map)
    return df

df = load_data()

# Sidebar para navegação
st.sidebar.title('Análises')
pagina = st.sidebar.radio('Selecione a página:', 
    ['Geral', 'Por Regiões', 'Por Estado', 'Temporal', 'Previsões'])

if pagina == 'Geral':
    st.title('Análise Geral do Turismo no Brasil - 2014 a 2024')
    
    # Total de turistas por ano
    turistas_por_ano = df.groupby('ano').size().reset_index(name='total_turistas')
    fig_total = px.line(turistas_por_ano, 
                        x='ano', y='total_turistas',
                        title='Total de Turistas por Ano',
                        template=CHART_STYLE['template'])
    fig_total.update_traces(line_color=COLOR_PALETTE['primary'], line_width=3)
    fig_total.update_layout(
        title=dict(
            text='Total de Turistas por Ano',
            font=dict(size=CHART_STYLE['title']['font_size'], family=CHART_STYLE['title']['font_family'])
        ),
        xaxis=dict(
            title="Ano",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        ),
        yaxis=dict(
            title="Total de Turistas",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        )
    )
    st.plotly_chart(fig_total)
    
    # Top 10 países de origem (excluindo "Outros países")
    top_paises = df[df['pais'] != 'Outros países'].groupby('pais').size().sort_values(ascending=False).head(10)
    fig_paises = px.bar(x=top_paises.index, y=top_paises.values,
                       title='Top 10 Países de Origem dos Turistas',
                       template=CHART_STYLE['template'],
                       color=top_paises.index,  # Usar o nome do país como base para as cores
                       color_discrete_sequence=COLOR_PALETTE['sequential'])
    fig_paises.update_layout(
        title=dict(
            text='Top 10 Países de Origem dos Turistas',
            font=dict(size=CHART_STYLE['title']['font_size'], family=CHART_STYLE['title']['font_family'])
        ),
        xaxis=dict(
            title="País",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        ),
        yaxis=dict(
            title="Total de Turistas",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        )
    )
    st.plotly_chart(fig_paises)
    
    # Distribuição por via de chegada
    via_chegada = df.groupby('via').size().reset_index(name='total')
    fig_via = px.pie(via_chegada, 
                     values='total', names='via',
                     title='Distribuição por Via de Chegada',
                     template=CHART_STYLE['template'],
                     color_discrete_sequence=COLOR_PALETTE['sequential'])
    fig_via.update_layout(
        title=dict(
            text='Distribuição por Via de Chegada',
            font=dict(size=CHART_STYLE['title']['font_size'], family=CHART_STYLE['title']['font_family'])
        )
    )
    st.plotly_chart(fig_via)

elif pagina == 'Por Regiões':
    st.title('Análise por Regiões do Brasil')
    
    # Total por região (ordenado do maior para o menor)
    turistas_por_regiao = df.groupby('regiao').size().reset_index(name='total_turistas')
    turistas_por_regiao = turistas_por_regiao.sort_values('total_turistas', ascending=False)
    
    fig_regiao = px.bar(x=turistas_por_regiao['regiao'], y=turistas_por_regiao['total_turistas'],
                       title='Distribuição de Turistas por Região',
                       template=CHART_STYLE['template'],
                       color=turistas_por_regiao['regiao'],  # Usar o nome da região como base para as cores
                       color_discrete_sequence=COLOR_PALETTE['region_colors'])
    fig_regiao.update_layout(
        title=dict(
            text='Distribuição de Turistas por Região',
            font=dict(size=CHART_STYLE['title']['font_size'], family=CHART_STYLE['title']['font_family'])
        ),
        xaxis=dict(
            title="Região",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        ),
        yaxis=dict(
            title="Total de Turistas",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        )
    )
    st.plotly_chart(fig_regiao)

elif pagina == 'Por Estado':
    st.title('Análise por Estado')
    
    estado = st.selectbox('Selecione o Estado:', df['uf'].unique())
    estado_df = df[df['uf'] == estado]
    
    # Agrupar por ano para o estado selecionado
    estado_ano = estado_df.groupby('ano').size().reset_index(name='total_turistas')
    fig_estado = px.line(estado_ano,
                        x='ano', y='total_turistas',
                        title=f'Evolução do Turismo em {estado}',
                        template=CHART_STYLE['template'])
    fig_estado.update_traces(line_color=COLOR_PALETTE['accent'], line_width=3)
    fig_estado.update_layout(
        title=dict(
            text=f'Evolução do Turismo em {estado}',
            font=dict(size=CHART_STYLE['title']['font_size'], family=CHART_STYLE['title']['font_family'])
        ),
        xaxis=dict(
            title="Ano",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        ),
        yaxis=dict(
            title="Total de Turistas",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        )
    )
    st.plotly_chart(fig_estado)

elif pagina == 'Temporal':
    st.title('Análise Temporal')
    
    # Criar duas colunas
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Análise Anual')
        # Total de turistas por ano
        turistas_por_ano = df.groupby('ano').size().reset_index(name='total_turistas')
        fig_anual = px.line(turistas_por_ano,
                           x='ano', y='total_turistas',
                           title='Total de Turistas por Ano',
                           template=CHART_STYLE['template'],
                           markers=True)
        fig_anual.update_traces(line_color=COLOR_PALETTE['primary'], line_width=3)
        fig_anual.update_layout(
            title=dict(
                text='Total de Turistas por Ano',
                font=dict(size=CHART_STYLE['title']['font_size'], family=CHART_STYLE['title']['font_family'])
            ),
            xaxis=dict(
                title="Ano",
                gridcolor=CHART_STYLE['axis']['gridcolor'],
                showgrid=CHART_STYLE['axis']['showgrid']
            ),
            yaxis=dict(
                title="Total de Turistas",
                gridcolor=CHART_STYLE['axis']['gridcolor'],
                showgrid=CHART_STYLE['axis']['showgrid']
            )
        )
        st.plotly_chart(fig_anual, use_container_width=True)

    with col2:
        st.subheader('Análise Mensal')
        # Criar um mapeamento para ordenar os meses corretamente
        ordem_meses = {
            'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
            'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
            'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
        }
        
        # Total de turistas por mês (independente do ano)
        df['ordem_mes'] = df['mes'].map(ordem_meses)
        turistas_por_mes = df.groupby(['mes', 'ordem_mes']).size().reset_index(name='total_turistas')
        turistas_por_mes = turistas_por_mes.sort_values('ordem_mes')
        
        fig_mensal = px.bar(turistas_por_mes,
                           x='mes', y='total_turistas',
                           title='Total de Turistas por Mês (Todos os Anos)',
                           template=CHART_STYLE['template'],
                           color='mes',  # Usar o nome do mês como base para as cores
                           color_discrete_sequence=COLOR_PALETTE['sequential'],
                           category_orders={'mes': sorted(df['mes'].unique(), key=lambda x: ordem_meses.get(x, 13))})
        fig_mensal.update_layout(
            title=dict(
                text='Total de Turistas por Mês (Todos os Anos)',
                font=dict(size=CHART_STYLE['title']['font_size'], family=CHART_STYLE['title']['font_family'])
            ),
            xaxis=dict(
                title="Mês",
                tickangle=-45,
                gridcolor=CHART_STYLE['axis']['gridcolor'],
                showgrid=CHART_STYLE['axis']['showgrid']
            ),
            yaxis=dict(
                title="Total de Turistas",
                gridcolor=CHART_STYLE['axis']['gridcolor'],
                showgrid=CHART_STYLE['axis']['showgrid']
            )
        )
        st.plotly_chart(fig_mensal, use_container_width=True)

    # Análise de tendência mensal ao longo dos anos
    st.subheader('Tendência Mensal ao Longo dos Anos')
    turistas_mes_ano = df.groupby(['ano', 'mes', 'ordem_mes']).size().reset_index(name='total_turistas')
    turistas_mes_ano = turistas_mes_ano.sort_values(['ano', 'ordem_mes'])
    
    fig_tendencia = px.line(turistas_mes_ano,
                           x='ano', y='total_turistas',
                           color='mes',
                           title='Tendência Mensal ao Longo dos Anos',
                           template=CHART_STYLE['template'],
                           color_discrete_sequence=COLOR_PALETTE['sequential'],
                           category_orders={'mes': sorted(df['mes'].unique(), key=lambda x: ordem_meses.get(x, 13))})
    fig_tendencia.update_layout(
        title=dict(
            text='Tendência Mensal ao Longo dos Anos',
            font=dict(size=CHART_STYLE['title']['font_size'], family=CHART_STYLE['title']['font_family'])
        ),
        xaxis=dict(
            title="Ano",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        ),
        yaxis=dict(
            title="Total de Turistas",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        ),
        showlegend=True,
        legend_title="Mês"
    )
    st.plotly_chart(fig_tendencia, use_container_width=True)

else:  # Previsões
    st.title('Previsões de Turismo')
    
    # Preparando dados para previsão
    anos_df = df.groupby('ano').size().reset_index(name='total_turistas')
    X = anos_df['ano'].values.reshape(-1, 1)
    y = anos_df['total_turistas'].values
    
    # Treinando modelo
    model = LinearRegression()
    model.fit(X, y)
    
    # Interface para previsão
    ano_futuro = st.slider('Selecione o ano para previsão:', 
                          min_value=int(df['ano'].max()) + 1,
                          max_value=2030,
                          value=int(df['ano'].max()) + 5)
    
    # Gerando previsões
    anos_futuros = np.array(range(int(df['ano'].min()), ano_futuro + 1)).reshape(-1, 1)
    previsoes = model.predict(anos_futuros)
    
    # Plotando resultados
    fig_previsao = go.Figure()
    fig_previsao.add_trace(go.Scatter(
        x=anos_df['ano'], 
        y=anos_df['total_turistas'],
        mode='lines+markers', 
        name='Dados Históricos',
        line=dict(color=COLOR_PALETTE['primary'], width=3)
    ))
    fig_previsao.add_trace(go.Scatter(
        x=anos_futuros.flatten(), 
        y=previsoes,
        mode='lines', 
        name='Previsão',
        line=dict(color=COLOR_PALETTE['accent'], width=3, dash='dash')
    ))
    fig_previsao.update_layout(
        title=dict(
            text='Previsão de Turistas',
            font=dict(size=CHART_STYLE['title']['font_size'], family=CHART_STYLE['title']['font_family'])
        ),
        xaxis=dict(
            title="Ano",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        ),
        yaxis=dict(
            title="Número de Turistas",
            gridcolor=CHART_STYLE['axis']['gridcolor'],
            showgrid=CHART_STYLE['axis']['showgrid']
        ),
        template=CHART_STYLE['template']
    )
    st.plotly_chart(fig_previsao)
