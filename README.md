agent-ants 🐜
🌌 Swarm-based CLI AI Agents that think, log, and grow together.

✨ Описание

agent-ants — это лёгкая, модульная система AI-агентов, которые:
🧰 Получают задачи ("assign")
🤔 Думают и формируют ответы
📅 Хранят память о прошлых задачах
📉 Логируют своё поведение
👥 Живут в улье (Swarm), которым можно управлять
⌛ Работают с локальной LLM или через API
🚀 Быстрый старт

# Установка
make install  # или pip install -e .

# Запуск CLI
python app.py

В CLI:
> create analyst "Проводит анализ рисков"
> assign analyst "Что будет с AGI в ближайшие 3 года?"
> log analyst
> list
> exit

🎓 Структура проекта

agent-ants/
├── app.py                  # CLI REPL
├── cli/agentctl.py         # Typer CLI
├── agents/                 # Классы агентов (base, analyst, etc.)
├── core/                   # LLM, логгер, таймер, swarm
├── memory/                 # Хранилище задач и векторов
├── prompts/                # Системные промпты для агентов
├── data/                   # Saved memory файлов
├── logs/                   # Логи агентов
├── cluster/                # ClusterManager (в разработке)
├── tools/                  # Парсеры и поиск
├── tests/                  # Pytest тесты + фикстуры

🔍 Примеры системных промптов (prompts/)
  analyst.txt:
    Ты профессиональный аналитик рисков. Отвечай лаконично, опираясь на факты. Если задача слишком общая — уточни контекст.

  researcher.txt:
    Ты исследователь. Твоя задача — найти релевантную информацию, разобрать по пунктам, указать источники и сделать выводы. Излагай структурированно.

🔧 Тестирование
make test-all  # PYTHONPATH=. pytest -v --tb=short tests/

Покрытие включает:
Юнит-тесты агентов (think, memory, log)
Тесты CLI (create, assign, list, log, exit)
Тестирование Swarm и взаимодействия

TBA: Roadmap


👋 Вклад
Fork it, star it, hack it. Pull requests welcome — или просто заходи поболтать в REPL

📄 Лицензия
MIT License

—

Powered by caffeine, curiosity, and ants that dream big
(Readme is AI generated)