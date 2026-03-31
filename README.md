# ☁️ aLCloud — Локальное облачное хранилище

Безсерверная архитектура с прямым подключением к облачным провайдерам. Все данные и токены хранятся локально на вашем устройстве.

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![React](https://img.shields.io/badge/React-19-blue?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-38bdf8?logo=tailwindcss)

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

## 🚀 Как запустить (веб-версия)

### Требования

- **Node.js** 18+ (рекомендуется 20+)
- **Bun** (рекомендуется) или npm/yarn
- **Git**

### 1. Клонировать репозиторий

```bash
git clone https://github.com/vfyov6621-coder/aLCloud.git
cd aLCloud
```

### 2. Установить зависимости

```bash
bun install
```

> Если не используете Bun: `npm install`

### 3. Настроить переменные окружения

```bash
cp .env.example .env
```

Отредактируйте `.env` — укажите данные для подключения провайдеров (OAuth-клиенты):

```env
# База данных (SQLite)
DATABASE_URL="file:./db/custom.db"

# Google Drive
GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="your-google-client-secret"

# GitHub
GITHUB_CLIENT_ID="your-github-client-id"
GITHUB_CLIENT_SECRET="your-github-client-secret"

# Яндекс.Диск
YANDEX_CLIENT_ID="your-yandex-client-id"
YANDEX_CLIENT_SECRET="your-yandex-client-secret"

# Mail.ru Cloud
MAILRU_CLIENT_ID="your-mailru-client-id"
MAILRU_CLIENT_SECRET="your-mailru-client-secret"

# Telegram
TELEGRAM_API_ID="your-telegram-api-id"
TELEGRAM_API_HASH="your-telegram-api-hash"
```

> 💡 Для быстрого старта можно оставить credentials пустыми — приложение будет работать в демонстрационном режиме.

### 4. Инициализировать базу данных

```bash
bun run db:push
```

### 5. Запустить в режиме разработки

```bash
bun run dev
```

Приложение будет доступно по адресу: **http://localhost:3000**

---

## 🖥️ Как сделать .exe (десктоп-версия)

### Вариант A: Electron (рекомендуется для Windows)

#### Установка Electron

```bash
bun add -d electron electron-builder
```

#### Сборка .exe

```bash
# 1. Собрать Next.js приложение
bun run build

# 2. Упаковать в Electron .exe
bun run electron:build
```

Готовый установщик появится в папке `dist/`.

#### Для разработки (Electron)

```bash
bun run electron:dev
```

### Вариант B: Tauri (легче, быстрее)

Tauri создаёт значительно меньшие .exe файлы за счёт использования системного WebView вместо встроенного Chromium.

```bash
# Установка Tauri CLI
cargo install tauri-cli

# Инициализация Tauri
bunx tauri init

# Сборка .exe
bunx tauri build
```

> ⚠️ Для Tauri требуется установленный [Rust](https://rustup.rs/) и Visual Studio Build Tools (на Windows).

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
├── prisma/
│   └── schema.prisma               # Схема базы данных
├── electron/                       # Electron конфигурация
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
| Десктоп | Electron / Tauri |

---

## 📝 Скрипты

```bash
bun run dev          # Запуск в режиме разработки
bun run build        # Сборка production
bun run start        # Запуск production-сервера
bun run lint         # Проверка кода
bun run db:push      # Применить схему БД
bun run db:generate  # Сгенерировать Prisma клиент
```

---

## 📄 Лицензия

MIT
