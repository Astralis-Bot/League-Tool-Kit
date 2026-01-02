# 🎮 League Toolkit (LTK)

**Premium League of Legends Automation Toolkit** - Um aplicativo Electron completo para automação de funcionalidades do League of Legends.

![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20MacOS%20%7C%20Linux-lightgrey.svg)

---

## ✨ Funcionalidades Principais

### 🎯 Automações de Champ Select
- **Auto Accept** - Aceita partidas automaticamente
- **Auto Pick** - Seleciona campeões automaticamente (com suporte a pick aleatório)
- **Auto Ban** - Bane campeões automaticamente (com proteção para picks dos aliados)

### 👤 Personalização de Perfil
- **Trocar Ícone** - IDs de 1 a 5000
- **Trocar Background** - Qualquer skin do jogo
- **Trocar Riot ID** - Nome e tag
- **Status Personalizado** - Mensagem customizada
- **Remover Badges** - Limpar badges do perfil

### 🎲 Ações de Jogo
- **Reveal Lobby** - Abre Porofessor.gg com informações dos jogadores
- **Remover Amigos** - Remove todos os amigos de uma vez
- **Restart Client** - Reinicia o cliente do LoL


### 🔧 Sistema Avançado
- **Logs em Tempo Real** - Sistema completo de logging
- **Cache Inteligente** - Otimização de performance
- **Reconexão Automática** - Detecta quando o cliente reinicia
- **Interface Moderna** - UI responsiva e intuitiva

---

## 📋 Pré-requisitos

### Para Executar o Aplicativo
- **Node.js** 18+ ([Download aqui](https://nodejs.org/))
- **League of Legends** instalado
- **Windows 10/11**, MacOS 10.15+, ou Linux

### Para Scripts Python (Opcional)
- **Python 3.8+** ([Download aqui](https://www.python.org/downloads/))
- Bibliotecas listadas em `python-scripts/requirements.txt`

---

## 🚀 Instalação Rápida

### 1. Clone ou Baixe o Projeto
```bash
git clone https://github.com/Astralis-Bot/League-Tool-Kit
cd league-toolkit
```

### 2. Instale as Dependências
```bash
npm install
```

### 3. Execute o Aplicativo
```bash
npm start
```

---

## 📦 Build para Produção

### Windows
```bash
npm run build:win
```
Gera arquivos em `dist/`:
- **LTK Setup.exe** - Instalador
- **LTK Portable.exe** - Versão portátil

### MacOS
```bash
npm run build:mac
```
Gera: **LTK.dmg** e **LTK.zip**

### Linux
```bash
npm run build:linux
```
Gera: **LTK.AppImage** e **LTK.deb**

---

## 🎮 Como Usar

### Passo 1: Abrir o League of Legends
1. Inicie o **League of Legends**
2. Faça login normalmente
3. O LTK detectará automaticamente o cliente

### Passo 2: Ativar Funcionalidades

#### Auto Accept
1. Clique em **"Auto Accept"** no painel
2. Entre na fila
3. O aplicativo aceitará automaticamente quando encontrar partida

#### Auto Pick
1. Digite o nome do campeão (ex: "Yasuo")
2. Clique em **"Set Auto Pick"**
3. Ou digite "random" para pick aleatório

#### Auto Ban
1. Digite o nome do campeão (ex: "Yasuo")
2. Marque **"Protect Ally Picks"** se quiser evitar banir campeões que aliados marcaram
3. Clique em **"Set Auto Ban"**

#### Trocar Background
1. Pesquise pelo campeão ou skin desejada
2. Copie o **Skin ID** de sites como [CommunityDragon](https://www.communitydragon.org/)
3. Cole no campo e clique em **"Change"**

---

## 🏗️ Estrutura do Projeto

```
league-toolkit/
├── main.js                 # Processo principal do Electron
├── preload.js              # Script de ponte (IPC)
├── app.js                  # Lógica do renderer
├── index.html              # Interface HTML
├── styles.css              # Estilos CSS
├── package.json            # Dependências e scripts
│
├── services/              # Serviços principais
│   ├── LCUService.js      # Conexão com LCU API
│   ├── FeatureService.js  # Automações e funcionalidades
│   ├── SummonerService.js # Dados do invocador
│   ├── MatchService.js    # Histórico de partidas
│   ├── StatsService.js    # Cálculos e estatísticas
│   └── LogService.js      # Sistema de logs
│
├── utils/                 # Utilitários
│   └── LogThrottle.js     # Throttling de logs
│
├── python-scripts/        # Scripts Python (opcionais)
│   ├── Rengar.py          # Conexão com LCU
│   ├── AutoAccept.py      # Auto accept
│   ├── Backgrounds.py     # Trocar background
│   ├── Badges.py          # Manipular badges
│   ├── Icons.py           # Trocar ícone
│   ├── Dodge.py           # Dodge de partida
│   ├── Reveal.py          # Revelar lobby
│   ├── StatusChanger.py   # Trocar status
│   ├── Riotidchanger.py   # Trocar Riot ID
│   ├── RemoveFriends.py   # Remover amigos
│   ├── RestartUX.py       # Reiniciar cliente
│   ├── api_bridge.py      # Ponte Python-Electron
│   └── requirements.txt   # Dependências Python
│
└── assets/                # Recursos (ícones, imagens)
    └── icon.ico           # Ícone do aplicativo
```

---

## 🛠️ Tecnologias Utilizadas

### Frontend
- **Electron 28** - Framework para aplicativos desktop
- **HTML5/CSS3** - Interface moderna
- **JavaScript ES6+** - Lógica do aplicativo

### Backend/Services
- **Node.js** - Runtime JavaScript
- **HTTPS** - Conexão segura com LCU
- **WebSockets** - Comunicação em tempo real (futuro)

### Integrações
- **LCU API** - API oficial do cliente League of Legends
- **Community Dragon** - Dados de skins e campeões
- **Porofessor.gg** - Estatísticas de jogadores

---

## 🔍 Como Funciona

### 1. Conexão com o LCU
O aplicativo se conecta à **LCU (League Client Update) API** local:
```javascript
// Encontra credenciais do processo LeagueClientUx.exe
const credentials = await findCredentials();

// Conecta em https://127.0.0.1:<porta>
const response = await https.request({
    hostname: '127.0.0.1',
    port: credentials.port,
    headers: {
        'Authorization': `Basic ${base64('riot:' + credentials.password)}`
    }
});
```

### 2. Polling e Eventos
- Verifica status do cliente a cada 3-5 segundos
- Detecta automaticamente quando entra/sai de champ select
- Mantém cache para otimizar performance

### 3. Automações
```javascript
// Exemplo: Auto Accept
setInterval(async () => {
    const readyCheck = await lcu.get('/lol-matchmaking/v1/ready-check');
    if (readyCheck.state === 'InProgress') {
        await lcu.post('/lol-matchmaking/v1/ready-check/accept');
    }
}, 400); // Verifica a cada 400ms
```

---

## 🐛 Resolução de Problemas

### ❌ "LCU not connected"
**Soluções:**
1. Certifique-se de que o League of Legends está **aberto e logado**
2. Clique em **"Refresh"** no aplicativo
3. Reinicie o League of Legends
4. Reinicie o LTK

### ❌ "Champion not found"
**Soluções:**
1. Verifique a ortografia do nome
2. Tente variações: "Wukong" ou "MonkeyKing"
3. Use nomes em inglês
4. Recarregue a lista de campeões

### ❌ "You don't own this champion"
**Causa:** Você não possui o campeão selecionado
**Solução:** Escolha outro campeão ou use "random"

### ❌ Background não muda
**Soluções:**
1. Use Skin IDs válidos do [Community Dragon](https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/skins.json)
2. Formato esperado: números como `27001`, `27002`, etc
3. Alguns skins podem não funcionar como background

### ❌ Build falha no Windows
**Solução:**
```bash
# Instale ferramentas de build
npm install --global windows-build-tools

# Ou use Visual Studio Build Tools
# https://visualstudio.microsoft.com/downloads/
```

---

## 🔐 Segurança

### É Seguro?
✅ **SIM** - O aplicativo:
- Apenas se conecta à API **local** do League of Legends
- **Não modifica arquivos** do jogo
- **Não coleta dados pessoais**
- **Código aberto** - você pode auditar o código

### Posso Ser Banido?
⚠️ **ATENÇÃO:**
- Riot Games **não endossa** ferramentas de terceiros
- Use por **sua conta e risco**
- **Não abuse** das funcionalidades (ex: troca de background excessivo)


---

## 📝 Scripts Disponíveis

```bash
# Desenvolvimento
npm start              # Inicia o aplicativo
npm run dev            # Inicia com DevTools aberto

# Build
npm run build          # Build para todas as plataformas
npm run build:win      # Build apenas para Windows
npm run build:mac      # Build apenas para MacOS
npm run build:linux    # Build apenas para Linux
npm run pack           # Empacota sem criar instalador
npm run dist           # Cria distribuição completa
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add: Minha nova feature'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

### Diretrizes
- Siga o estilo de código existente
- Adicione comentários para código complexo
- Teste suas mudanças antes de submeter
- Atualize o README se necessário

---

## 📜 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License

Copyright (c) 2025 LTK Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🌟 Roadmap Futuro

- [ ] Sistema de notificações
- [ ] Temas customizáveis
- [ ] Dashboard web (opcional)

---

## 📞 Suporte

### 🐛 Bugs e Issues
Abra uma issue no GitHub: [Issues](https://github.com/seu-usuario/league-toolkit/issues)

### 💬 Discussões
Participe das discussões: [Discussions](https://github.com/seu-usuario/league-toolkit/discussions)

### 📧 Contato
- Twitter/X: x.com/novatheprince
- Discord: starykk

---

## ⚠️ Disclaimer

Este projeto **NÃO** é afiliado, associado, autorizado, endossado por, ou de qualquer forma oficialmente conectado com a **Riot Games, Inc.**, ou qualquer de suas subsidiárias ou afiliadas.

**League of Legends** e todos os conteúdos relacionados são marcas registradas ou marcas comerciais da Riot Games, Inc.

**USE POR SUA CONTA E RISCO.**

---

<div align="center">

**⭐ Se este projeto te ajudou, considere dar uma estrela! ⭐**

younk  ★

[⬆ Voltar ao topo](#-league-toolkit-ltk)

</div>
