# Projeto RASI — Docker e Docker Compose

**Aluno:** Valmir Pereira da Rosa Filho  
**Instituição:** IFSP — Campus Campos do Jordão  
**Curso:** Técnico em Informática Integrado ao Ensino Médio  
**Disciplina:** Redes e Administração de Sistemas (RASI)

## Objetivo
Demonstrar a execução de uma aplicação Flask em containers e a integração de Flask, MySQL e Apache com Docker Compose.

## Arquitetura
Navegador → Apache (porta 80) → Flask (porta interna 5000) → MySQL (porta interna 3306).

O Compose administra os serviços `server`, `flask` e `db`. O volume nomeado `mysql_data` mantém os dados do banco.

## Estrutura
- `app/app.py`: aplicação Flask com rotas Início, Sobre, Contato e Alunos.
- `app/requirements.txt`: dependências Python.
- `Dockerfile`: imagem da aplicação.
- `compose.yaml`: orquestração dos três serviços.
- `httpd.conf`: configuração do Apache como proxy reverso.
- `mysql/init.sql`: criação e carga inicial da tabela alunos.
- `.env.example`: modelo das variáveis de ambiente.

## Executar
Requer Docker Engine e Docker Compose.

```bash
cp .env.example .env
nano .env
docker compose config
docker compose up -d --build
docker compose ps
```

Defina senhas próprias no arquivo `.env`. **Nunca publique o arquivo `.env`**; ele está excluído pelo `.gitignore`.

Acesse `http://localhost/` e teste:
- `/`
- `/sobre`
- `/contato`
- `/alunos`

Para consultar logs e encerrar:

```bash
docker compose logs
docker compose down
```

Para verificar persistência, execute `docker compose down` e depois `docker compose up -d`. Não use `docker compose down -v` nesse teste, pois isso remove o volume do banco.

## Etapa básica Flask
O Dockerfile também pode ser utilizado para testar a aplicação diretamente na porta 5000:

```bash
docker build -t flask-app .
docker run -d -p 5000:5000 --name meu-flask flask-app
docker ps
docker logs meu-flask
```

## Evidências e situação
O código e as configurações foram organizados para execução. **A execução real dos containers, a VM Ubuntu e o acesso SSH ainda precisam ser realizados e comprovados com capturas reais.** Imagens meramente ilustrativas não devem ser apresentadas como evidência de execução.

## Referência da atividade
https://github.com/CesarAugusto88/RAS-Docker
