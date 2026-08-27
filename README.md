# Consulta de Juízo - Sistema CNJ

Aplicação web para consultar e identificar juízos brasileiros através de números de processos no padrão CNJ (Conselho Nacional de Justiça).

## 🚀 Recursos

- ✅ Validação de formato CNJ (NNNNNNN-DD.AAAA.J.TR.OOOO)
- ✅ Interface web interativa e responsiva
- ✅ API REST para consultas programáticas
- ✅ Mensagens de erro detalhadas em português
- ✅ Suporte para múltiplos segmentos de justiça

## 📋 Formato do Número CNJ

```
NNNNNNN-DD.AAAA.J.TR.OOOO
```

- **NNNNNNN**: Número sequencial do processo
- **DD**: Dígito verificador
- **AAAA**: Ano de ajuizamento
- **J**: Código do segmento de Justiça (1 dígito)
- **TR**: Código do Tribunal (2 dígitos)
- **OOOO**: Código da unidade de origem (4 dígitos)

### Exemplo
```
0010507-38.2021.5.18.0008
```

## 🛠️ Instalação Local

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/triagemprocessualcivel-ops/identificaprocesso.git
cd identificaprocesso
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python app.py
```

4. Acesse no navegador:
```
http://localhost:5000
```

## 🌐 Deploy no Render

### Opção 1: Usar render.yaml

1. Conecte seu repositório GitHub ao [Render](https://render.com/)
2. Crie um novo serviço web
3. Selecione "Python" como runtime
4. O Render lerá automaticamente o arquivo `render.yaml`
5. Clique em "Deploy"

### Opção 2: Deploy manual

1. Vá para [render.com](https://render.com/)
2. Clique em "New +" → "Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: `consulta-juizo-cnj`
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free (opcional)
5. Clique em "Deploy"

Após o deploy, sua aplicação estará disponível em:
```
https://consulta-juizo-cnj.onrender.com
```

## 📡 API Endpoints

### GET `/`
Retorna a página web interativa.

### POST `/api/consultar`
Consulta um número de processo e retorna o juízo correspondente.

**Request:**
```json
{
  "numero_processo": "0010507-38.2021.5.18.0008"
}
```

**Response (Sucesso):**
```json
{
  "sucesso": true,
  "juizo": "8ª Vara do Trabalho de Goiânia — TRT 18ª Região (Goiás)"
}
```

**Response (Erro):**
```json
{
  "sucesso": false,
  "erro": "Número de processo em formato inválido. Esperado: NNNNNNN-DD.AAAA.J.TR.OOOO (ex: 0010507-38.2021.5.18.0008)"
}
```

### GET `/health`
Verifica o status da aplicação.

**Response:**
```json
{
  "status": "ok"
}
```

## 🧪 Teste

```bash
# Via web
curl http://localhost:5000

# Via API
curl -X POST http://localhost:5000/api/consultar \
  -H "Content-Type: application/json" \
  -d '{"numero_processo": "0010507-38.2021.5.18.0008"}'
```

## 📝 Estrutura do Projeto

```
.
├── app.py                      # Aplicação Flask principal
├── consulta_juizo_cnj.py       # Script CLI original
├── matriz_codigos_cnj.json     # Base de dados de tribunais e unidades
├── requirements.txt            # Dependências Python
├── render.yaml                 # Configuração para Render
└── templates/
    └── index.html              # Interface web
```

## 🔄 Segmentos de Justiça Suportados

| Código | Segmento | Exemplos |
|--------|----------|----------|
| 1, 7, 9 | Federal | TRF, JF |
| 2 | Estadual Militar | STM |
| 3 | Militar da União | STM |
| 4, 5 | Trabalho | TRT |
| 6 | Eleitoral | TRE |
| 8 | Estadual | TJSP, TJMG, etc |

## 📚 Referências

- [Resolução 65/2008 - CNJ](https://www.cnj.jus.br/programas-e-acoes/numeracao-unica/)
- [Tabela de Códigos - CNJ](https://www.cnj.jus.br/programas-e-acoes/numeracao-unica/tabelas-de-codigos/)

## 📄 Licença

Este projeto é de código aberto e disponível sob a licença MIT.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para problemas, dúvidas ou sugestões, abra uma [issue](https://github.com/triagemprocessualcivel-ops/identificaprocesso/issues).
