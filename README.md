# 📄 Desafio técnico


## ⚙️ Requisitos do Sistema

* Python 3.9+
* pip atualizado
* Sistema operacional: Windows / Linux / macOS

---

## 📦 Instalação das Dependências

Antes de executar o projeto, instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como Executar o Projeto

Após instalar as dependências, execute o pipeline principal:

```bash
python main.py
```

---

## 📁 Estrutura do Projeto

```
mudas_detector/
│
├── input/
│   └── imagens .tif que serão processadas
│
├── output/
│   ├── imagem-deteccao/
│   │   └── imagens geradas com detecção das mudas
│   │
│   ├── mudasgeojson/
│   │   └── arquivos .geojson com georreferenciamento das mudas 
│   │
│   ├── metricas_homogeneidade.json
│   │   └── métricas homogeneidade do plantio 
│   │
│   ├── estatisticas.json
│   │   └── estatísticas gerais do processamento
│
├── src/
│   ├── carregar_imagem.py - responsável por carregar e preparar imagens TIFF georreferenciadas
│   ├── deteccao.py - implementação do algoritmo de detecção das mudas de eucalipto
│   ├── geo_localizacao.py - conversão das detecções para coordenadas geográficas
│   ├── metricas_homogeneidade..py - cálculo dos indicadores de homogeneidade do plantio
│   └── estatistica_plantio.py - cálculo da estatísticas do resultado
│   └── processamento.py - pipeline de pré-processamento e limpeza das imagens
│   └── visualizacao.py - Algoritimo que gera imagem das mudas detectada 
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

## 📊 Saídas Geradas

Para cada imagem processada, o sistema gera:

### 1. 🗺️ GeoJSON (mudas detectadas)

* Local: `output/mudasgeojson/`
* Conteúdo: pontos georreferenciados das mudas detectadas

---

### 2. 📈 Estatísticas Gerais

Arquivo: `output/estatisticas.json`

* Número total de plantas detectadas
* Área analisada (hectares)
* Densidade de plantas por hectare

---

### 3. 📐 Métrica de Homogeneidade

Arquivo: `output/metricas_homogeneidade.json`

- area_media_influencia_px  
- variacao_area_influencia_px  
- variacao_espacamento_percentual  
- indice_uniformidade_plantio  
- indice_desigualdade_espacial  
- espacamento_medio_mudas  
- variacao_espacamento_mudas  
---

