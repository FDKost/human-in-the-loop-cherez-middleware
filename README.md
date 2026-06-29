# Human-in-the-Loop через middleware

## Requirements
- [high] Импорт и настройка агента: Добавить импорты: create_agent, HumanInTheLoopMiddleware, MemorySaver, Command. Создать MemorySaver, настроить create_agent с middleware и checkpointer, указать interrupt_on для нужного инструмента.
- [high] Вызов агента с thread_id: Вызвать agent.invoke с сообщением пользователя и config={'configurable':{'thread_id':'сессия-1'}}. Проверить наличие ключа '__interrupt__' в результате.
- [high] Обработка паузы и сбор решений: Если есть '__interrupt__', извлечь action_requests и review_configs, вывести информацию о каждом запросе в консоль, запросить у пользователя approve/reject (и при желании edit). Сформировать список decisions в том же порядке, что и action_requests.
- [high] Возобновление работы агента: Передать decisions через Command(resume={'decisions': decisions}) в agent.invoke с тем же config. Получить окончательный результат.
- [normal] Обновление requirements.txt: Добавить зависимости: langchain, langgraph, langchain-community (если используется), и любые другие необходимые пакеты для работы middleware и checkpointer.
