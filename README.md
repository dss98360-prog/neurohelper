# Нейропомощник

Простое веб-приложение с искусственным интеллектом для решения повседневных, учебных и рабочих задач.

Пользователь вводит запрос, выбирает режим ответа и получает результат от AI-модели через VseGPT API.

## Возможности

- свободный ответ на вопрос;

- составление пошагового плана;

- создание чек-листа;

- написание готового текста;

- генерация идей;

- объяснение сложной темы простыми словами;

- отображение ответа с Markdown-форматированием;

- очистка формы и результата;

- обработка ошибок и состояния загрузки.

## Технологии

### Frontend

- React

- TypeScript

- Vite

- React Markdown

- CSS

### Backend

- Python

- FastAPI

- Uvicorn

- OpenAI-compatible API

- VseGPT API

## Структура проекта

```text

neurohelper/

├── backend/

│   ├── [app.py](http://app.py)

│   └── requirements.txt

├── frontend/

│   ├── src/

│   ├── public/

│   └── package.json

├── .env.example

├── .gitignore

└── [README.md](http://README.md)

```

## Настройка API-ключа

В корне проекта создайте файл `.env`:

```env

VSEGPT_API_KEY=your_vsegpt_api_key_here

```

API-ключ не должен добавляться в Git.

## Локальный запуск

### 1. Backend

Перейдите в корень проекта:

```bash

cd ~/neurohelper

```

Активируйте виртуальное окружение:

```bash

source .venv/bin/activate

```

Установите зависимости:

```bash

pip install -r backend/requirements.txt

```

Запустите FastAPI:

```bash

uvicorn [backend.app](http://backend.app):app --reload --host 127.0.0.1 --port 8000

```

Backend будет доступен по адресу `http://127.0.0.1:8000`.

### 2. Frontend

Откройте второй терминал:

```bash

cd ~/neurohelper/frontend

npm install

npm run dev

```

После запуска откройте адрес, который покажет Vite, обычно `http://localhost:5173`.

## Production-сборка frontend

```bash

cd ~/neurohelper/frontend

npm run build

```

Готовая production-сборка создаётся в папке:

```text

frontend/dist/

```

## Как пользоваться

1. Откройте приложение в браузере.

2. Выберите режим ответа.

3. Введите запрос.

4. Нажмите **«Отправить»**.

5. Получите ответ Нейропомощника.

6. Кнопка **«Очистить»** удаляет текущий запрос и ответ.

## Архитектура

```text

Пользователь

    ↓

React + TypeScript

    ↓

Vite proxy /api

    ↓

FastAPI

    ↓

VseGPT API

    ↓

AI-модель

    ↓

FastAPI → React → браузер

```

API-ключ хранится на стороне backend и не передаётся во frontend.

## Результат

Создано одностраничное AI-приложение «Нейропомощник» с React-интерфейсом и FastAPI-backend. Приложение принимает запрос пользователя, отправляет его в AI-модель через VseGPT API и отображает структурированный ответ в браузере.