# ⭐️ Split.tg bot
[![Website](https://img.shields.io/badge/Website-split.tg-blue)](https://split.tg)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)](https://t.me/FishStarsBot)
[![Telegram](https://img.shields.io/badge/Telegram-Channel-blue)](https://t.me/SplitTg)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
![Pipeline](https://wpci.itanarchy.app/api/badges/14/status.svg)

# About
Buy Telegram Stars and Telegram Premium easily with [@FishStarsBot](https://t.me/FishStarsBot)!

## System dependencies
- Python 3.11+
- Docker
- docker-compose
- make
- uv

## 🐳 Quick Start with Docker compose
- Rename `.env.dist` to `.env` and configure it
- Rename `docker-compose.example.yml` to `docker-compose.yml`
- Run `make app-build` command then `make app-run` to start the bot

Use `make` to see all available commands

## 🔧 Development

### Setup environment
```bash
uv sync
```
### Update database tables structure
**Make migration script:**
```bash
make migration message=MESSAGE_WHAT_THE_MIGRATION_DOES
```
**Run migrations:**
```bash
make migrate
```

## 🚀 Used technologies:
- [uv](https://docs.astral.sh/uv/) (an extremely fast Python package and project manager)
- [Aiogram 3.x](https://github.com/aiogram/aiogram) (Telegram bot framework)
- [PostgreSQL](https://www.postgresql.org/) (persistent relational database)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Redis](https://redis.io/docs/) (in-memory data storage for FSM and caching)
- [Project Fluent](https://projectfluent.org/) (modern localization system)

## 🤝 Contributions

### 🐛 Bug Reports / ✨ Feature Requests

If you want to report a bug or request a new feature, feel free to open a [new issue](https://github.com/itanarchy/split-bot/issues/new).

### Pull Requests

If you want to help us improve the bot, you can create a new [Pull Request](https://github.com/itanarchy/split-bot/pulls).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
