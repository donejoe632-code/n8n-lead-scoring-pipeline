# AI Lead Scoring & CRM Router (n8n Production Workflow)

Автоматизированный сквозной воркфлоу для n8n, принимающий лиды из веб-форм, Telegram и внешних сервисов, валидирующий данные, обогащающий их через LLM (JSON-mode скоринг) и распределяющий по статусам в Google Таблицы и Telegram-чаты сейлз-команды.

---

## Архитектура воркфлоу

```
[Входящий лид: Вебхук / API]
       │
       ▼
[Node: Валидация & Нормализация JS]
       │
       ▼
[Node: LLM Lead Scorer (JSON Mode)]
       │
       ├─► Определение намерения (intent)
       ├─► Оценка бюджета (budget_tier)
       ├─► Вычисление скора (1–10)
       │
       ▼
[Node: Switch / Priority Router]
       │
       ├─► [HOT Leads: score >= 7] ──► [Google Sheets: HOT_LEADS] ──► [Telegram Alert с кнопками]
       │
       ├─► [WARM Leads: score 4-6] ──► [Google Sheets: WARM_ARCHIVE]
       │
       └─► [COLD / Спам: score <= 3] ──► [Архив / Игнорирование]
```

## Преимущества решения:
* **Время реакции < 5 секунд:** Менеджер получает пуш в Telegram с контактами и выжимкой задачи моментально.
* **100% защита от потери данных:** Встроенный обработчик `Error Trigger Handler` перехватывает сбои API и логирует сырой payload.
* **Импорт в 1 клик:** Готовый файл `workflow_lead_scoring_crm.json` совместим с любой версией n8n (Community и Cloud).

## Как запустить локально:
1. Откройте n8n: `Settings -> Workflows -> Import from File` и выберите `workflow_lead_scoring_crm.json`.
2. Задайте свои ключи в нодах:
   * Google Sheets: `Spreadsheet ID`
   * Telegram: `Bot Token` и `Chat ID`
   * OpenAI / RunPod: `API Key`
3. Запустите симуляцию лидов:
```bash
python simulate_leads.py
```
