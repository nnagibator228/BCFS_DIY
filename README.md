<h1 align="center"><b><u>⛓ BCFS</u></b></h1>

<h3 align="center">Simple BlockChain From Scratch implementation</h3>

<div align="center">
    
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Ethereum](https://img.shields.io/badge/Ethereum-3C3C3D?style=for-the-badge&logo=Ethereum&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

</div>

<div align="center">
    
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1EPN0kpwHq9O7rogYHsGUea2weRKFC9nS?usp=sharing)

</div>

---

## 💼 Базовая реализация блокчейна с нуля

Данный проект реализован в рамках *"челленджа"* по предмету "Вычислительная математика" при обучении на направлении "Информатика и Вычислительная техника" на Космическом факультете в МФ МГТУ им. Н. Э. Баумана 
*(куратор проекта - Малашин А. А.)*

### ⚡️ Реализованные компоненты
В проекте реализованные следующие компоненты блокчейна:

1. Базовый хэш-класс
2. Аккаунт-кошелек
3. Блок и его компоненты (merkle, head)
4. Механизм майнинга
5. Блокчейн
6. RPC-сервер для взаимодействия с БЧ

## 🖥️ Как запустить

1. В корне директории с клонированным репозиторием создайте `.env` файл со следующим контентом:

```
TELEGRAM_BOT_TOKEN=<ваш токен тг-бота>
RPC_SERVER_PORT=<порт для запуска rpc-сервера, например 8001>
```

2. Запустить compose-стэк:


```
docker compose up -d
```

## ℹ️ Дополнительные ссылки

- [Ссылка на Google Collab с конспектами по проекту](https://colab.research.google.com/drive/1EPN0kpwHq9O7rogYHsGUea2weRKFC9nS?usp=sharing)
- [Ссылка на презентацию проекта на Gamma.app](https://gamma.app/public/-iisj401tgwldi21)

> Если вам понравились материалы проекта, оставьте, пожалуйста, звездочку этому репозиторию ⭐️
