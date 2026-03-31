# ☁️ aLCloud — Локальное облачное хранилище

Безсерверная архитектура с прямым подключением к облачным провайдерам. Все данные и токены хранятся локально на вашем устройстве.

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![React](https://img.shields.io/badge/React-19-blue?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-38bdf8?logo=tailwindcss)
![Electron](https://img.shields.io/badge/Electron-41-47848f?logo=electron)

---

## Возможности

- 🌐 **5 облачных провайдеров**: Google Drive, Telegram, Яндекс.Диск, Mail.ru Cloud, GitHub
- 🔐 **Безсерверная авторизация**: OAuth 2.0 с PKCE — токены только на вашем устройстве
- 📁 **Единый интерфейс**: один файловый менеджер для всех провайдеров
- 🔍 **Универсальный поиск**: поиск файлов по всем подключённым хранилищам
- 🎨 **Grid / List виды**: удобное отображение файлов в двух режимах
- 🌓 **Тёмная / светлая тема**: автоматическое переключение
- 📤 **Drag & Drop**: загрузка файлов перетаскиванием
- 💾 **Локальная база данных**: SQLite для индексации и кеширования
- 🖥️ **Десктоп-версия**: .exe для Windows, AppImage для Linux, .dmg для macOS

---

## Поддерживаемые провайдеры

| Провайдер | Метод | Макс. файл |
|-----------|-------|-----------|
| Google Drive | OAuth 2.0 + Drive API v3 | 5 ТБ |
| Telegram | MTProto (gram.js) | 2 ГБ |
| Яндекс.Диск | OAuth 2.0 + REST API | 50 ГБ |
| Mail.ru Cloud | OAuth 2.0 + Cloud API | 2 ГБ |
| GitHub | OAuth 2.0 + REST API | 100 МБ |

---

## ⬇️ Готовые сборки

Скомпилированные файлы доступны в папке **`electron-dist/`** после сборки:

| Платформа | Формат | Команда сборки | Результат |
|-----------|--------|---------------|-----------|
| **Windows** | `.exe` (NSIS installer) | `bun run build:win` | `electron-dist/aLCloud Setup 1.0.0.exe` |
| **Linux** | `.AppImage` | `bun run build:linux` | `electron-dist/aLCloud-1.0.0.AppImage` |
| **macOS** | `.dmg` | `bun run build:mac` | `electron-dist/aLCloud-1.0.0.dmg` |

### Как запустить готовый файл

**Windows**: просто запустите `aLCloud Setup 1.0.0.exe` — появится установщик. Приложение запустится автоматически после установки.

**Linux**:
```bash
chmod +x aLCloud-1.0.0.AppImage
./aLCloud-1.0.0.AppImage
```

**macOS**: откройте `.dmg` и перетащите aLCloud в Applications.

---

## 🚀 Сборка из исходников

### Требования

- **Node.js** 18+ (рекомендуется 20+)
- **Bun** (рекомендуется) или npm
- **Git**
- Для десктоп-сборки: **Python 3**, **make**, **g++** (Linux) или **Visual Studio Build Tools** (Windows)

### 1. Клонировать и установить

```bash
git clone https://github.com/vfyov6621-coder/aLCloud.git
cd aLCloud
bun install
```

### 2. Настроить переменные окружения

```bash
cp .env.example .env
```

Отредактируйте `.env` — укажите OAuth-клиенты провайдеров:

```env
DATABASE_URL="file:./db/custom.db"
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
GITHUB_CLIENT_ID=""
GITHUB_CLIENT_SECRET=""
YANDEX_CLIENT_ID=""
YANDEX_CLIENT_SECRET=""
MAILRU_CLIENT_ID=""
MAILRU_CLIENT_SECRET=""
TELEGRAM_API_ID=""
TELEGRAM_API_HASH=""
```

> 💡 Credentials можно оставить пустыми — приложение работает в демо-режиме.

### 3. Инициализировать базу данных

```bash
bun run db:push
```

---

## 📋 Все скрипты

### Веб-версия

| Команда | Описание |
|---------|----------|
| `bun run dev` | Запуск в режиме разработки → http://localhost:3000 |
| `bun run build` | Сборка Next.js для production |
| `bun run start` | Запуск production-сервера |

### Десктоп-версия (Electron)

| Команда | Описание |
|---------|----------|
| `bun run build:win` | Полная сборка → `electron-dist/aLCloud Setup 1.0.0.exe` |
| `bun run build:linux` | Полная сборка → `electron-dist/aLCloud-1.0.0.AppImage` |
| `bun run build:mac` | Полная сборка → `electron-dist/aLCloud-1.0.0.dmg` |
| `bun run electron:build` | Сборка только обёртки (без пересборки Next.js) |
| `bun run electron:dev` | Запуск Electron в режиме разработки |

### База данных

| Команда | Описание |
|---------|----------|
| `bun run db:push` | Применить схему БД |
| `bun run db:generate` | Сгенерировать Prisma-клиент |
| `bun run db:migrate` | Выполнить миграции |

---

## 🖥️ Как собрать .exe (подробно)

### Автоматическая сборка (одна команда)

На **Windows** (в PowerShell или CMD):

```bash
bun install
bun run db:push
bun run build:win
```

Результат: **`electron-dist/aLCloud Setup 1.0.0.exe`** — полноценный NSIS-установщик (~200 МБ).

### Пошаговая сборка

```bash
# 1. Собрать Next.js
bun run build

# 2. Установить Electron (если ещё не установлен)
bun add -d electron electron-builder

# 3. Собрать .exe
bun run electron:build --win
```

### Структура electron-dist/

```
electron-dist/
├── aLCloud Setup 1.0.0.exe    # Windows-установщик
├── aLCloud-1.0.0.AppImage     # Linux AppImage
├── aLCloud-1.0.0.dmg          # macOS DMG
├── app/                        # Встроенный Next.js standalone-сервер
│   ├── server.js               # Точка входа сервера
│   ├── .next/                  # Скомпилированное приложение
│   ├── node_modules/           # Зависимости сервера
│   ├── public/                 # Статические файлы
│   ├── prisma/                 # Схема и миграции БД
│   └── db/                     # Папка для SQLite базы
├── linux-unpacked/             # Распакованная Linux-версия
├── builder-debug.yml           # Лог сборки
└── latest-linux.yml            # Метаданные
```

### Как это работает

1. `bun run build` собирает Next.js в **standalone**-режиме — получается автономный Node.js сервер
2. `electron-dist/app/` содержит этот сервер + статика + Prisma
3. `electron-builder` упаковывает Electron + сервер в единый установщик
4. При запуске .exe Electron автоматически стартует встроенный сервер и открывает окно
5. База данных SQLite создаётся в пользовательской папке (`%APPDATA%/aLCloud/`)

---

## 📁 Структура проекта

```
aLCloud/
├── src/
│   ├── app/
│   │   ├── api/                    # API маршруты
│   │   │   ├── providers/          # CRUD провайдеров, OAuth
│   │   │   └── files/              # Универсальный поиск
│   │   ├── layout.tsx              # Корневой layout
│   │   └── page.tsx                # Главная страница
│   ├── components/
│   │   ├── file-browser/           # Файловый менеджер
│   │   ├── sidebar/                # Боковая панель
│   │   ├── provider/               # Диалоги подключения
│   │   ├── search/                 # Поиск
│   │   ├── file-info/              # Информация о файле
│   │   ├── theme/                  # Переключатель темы
│   │   └── ui/                     # shadcn/ui компоненты
│   └── lib/
│       ├── providers/              # Абстракция провайдеров
│       │   ├── types.ts            # Интерфейс IProvider
│       │   ├── base-provider.ts    # Базовый класс
│       │   ├── google-drive.ts
│       │   ├── telegram.ts
│       │   ├── yandex-disk.ts
│       │   ├── mailru-cloud.ts
│       │   ├── github.ts
│       │   └── index.ts            # Реестр провайдеров
│       ├── store.ts                # Zustand store
│       └── db.ts                   # Prisma клиент
├── electron/                       # Electron обёртка
│   ├── main.js                     # Точка входа Electron
│   └── preload.js                  # Preload-скрипт
├── electron-dist/                  # ⬅️ Готовые сборки (.exe, .AppImage, .dmg)
├── prisma/
│   └── schema.prisma               # Схема базы данных
├── public/                         # Статические файлы
└── package.json
```

---

## 🛠️ Технологии

| Компонент | Технология |
|-----------|-----------|
| Фреймворк | Next.js 16 (App Router) |
| UI | React 19 + TypeScript 5 |
| Компоненты | shadcn/ui + Lucide Icons |
| Стилизация | Tailwind CSS 4 |
| База данных | Prisma ORM + SQLite |
| Состояние | Zustand |
| Анимации | Framer Motion |
| Drag & Drop | @dnd-kit |
| Десктоп | Electron 41 + electron-builder |

---

## 📄 Лицензия

MIT
