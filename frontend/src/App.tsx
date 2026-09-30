import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

type Mode = {
  value: string
  label: string
}

const modes: Mode[] = [
  { value: 'free', label: 'Свободный запрос' },
  { value: 'plan', label: 'План' },
  { value: 'checklist', label: 'Чек-лист' },
  { value: 'text', label: 'Написать текст' },
  { value: 'ideas', label: 'Предложить идеи' },
  { value: 'explain', label: 'Объяснить тему' },
]

function App() {
  const [message, setMessage] = useState('')
  const [mode, setMode] = useState('free')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async () => {
    if (!message.trim() || loading) return

    setLoading(true)
    setError('')
    setAnswer('')

    try {
      const response = await fetch('https://neurohelper.onrender.com/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.trim(),
          mode,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Не удалось получить ответ.')
      }

      setAnswer(data.answer)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Произошла неизвестная ошибка.'
      )
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setMessage('')
    setAnswer('')
    setError('')
    setMode('free')
  }

  return (
    <main className="app">
      <section className="assistant-card">
        <header className="header">
          <div className="logo">Н</div>

          <div>
            <h1>Нейропомощник</h1>
            <p>
              AI-помощник для повседневных, учебных и рабочих задач
            </p>
          </div>
        </header>

        <div className="form">
          <label htmlFor="mode">Режим работы</label>

          <select
            id="mode"
            value={mode}
            onChange={(event) => setMode(event.target.value)}
            disabled={loading}
          >
            {modes.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>

          <label htmlFor="message">Ваша задача</label>

          <textarea
            id="message"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="Например: составь план подготовки презентации на 7 дней..."
            rows={7}
            disabled={loading}
          />

          <div className="actions">
            <button
              className="primary-button"
              type="button"
              onClick={handleSubmit}
              disabled={!message.trim() || loading}
            >
              {loading ? 'Нейропомощник думает...' : 'Отправить'}
            </button>

            <button
              className="secondary-button"
              type="button"
              onClick={handleClear}
              disabled={loading}
            >
              Очистить
            </button>
          </div>
        </div>

        <section className="answer-section">
          <h2>Ответ</h2>

          {!answer && !error && !loading && (
            <p className="placeholder">
              Здесь появится ответ Нейропомощника.
            </p>
          )}

          {loading && (
            <p className="loading">
              Формирую ответ...
            </p>
          )}

          {error && (
            <div className="error">
              {error}
            </div>
          )}

           {answer && (
          <div className="answer">
          <ReactMarkdown>{answer}</ReactMarkdown>
          </div>
          )}
        </section>
      </section>
    </main>
  )
}

export default App