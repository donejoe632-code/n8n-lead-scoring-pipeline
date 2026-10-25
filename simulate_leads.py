"""
Скрипт эмуляции и тестирования пайплайна скоринга лидов.
Отправляет тестовые наборы лидов (горячий, средний, спам) на вебхук n8n или эмулирует ИИ-оценку локально.
"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import json
import time
import urllib.request
import urllib.error

SAMPLE_LEADS = [
    {
        "name": "Михаил Воронов (Директор по логистике)",
        "contact": "+7 (916) 777-88-99",
        "task_details": "Срочно нужно автоматизировать передачу заказов из Telegram-чатов в 1С и Google Таблицы. Сейчас менеджеры тратят по 4 часа в день на копипаст. Бюджет до $2,500, готовы стартовать на этой неделе.",
        "source": "Telegram Partner Channel"
    },
    {
        "name": "Елена Смирнова",
        "contact": "elena.smirnova@gmail.com",
        "task_details": "Здравствуйте, подскажите, а вы делаете ботов для записи клиентов на ноготочки? Сколько примерно стоит?",
        "source": "Website Form"
    },
    {
        "name": "Crypto Bot 2026",
        "contact": "@cryptospam_bot",
        "task_details": "FREE BITCOIN AIRDROP! Click http://spam-link.xyz to claim $500 right now!",
        "source": "Open Form"
    }
]

def evaluate_lead_mock(lead: dict) -> dict:
    """Локальная эмуляция работы LLM JSON-mode"""
    text = lead["task_details"].lower()
    if "срочно" in text or "бюджет" in text or "готовы стартовать" in text:
        return {
            "score": 9,
            "intent": "Автоматизация передачи данных (Telegram -> Sheets / 1C)",
            "budget_tier": "High ($2,500)",
            "priority": "HOT",
            "summary": "Критическая потребность в автоматизации логистических заказов с выделенным бюджетом.",
            "recommended_action": "Срочный звонок в течение 10 минут, назначить созвон с инженером."
        }
    elif "ноготочки" in text or "сколько примерно" in text:
        return {
            "score": 5,
            "intent": "Разработка простого бота записи для сферы услуг",
            "budget_tier": "Low (<$500)",
            "priority": "WARM",
            "summary": "Запрос стоимости базового бота онлайн-записи для малого бизнеса.",
            "recommended_action": "Отправить типовой прайс-лист и бриф на оценку."
        }
    else:
        return {
            "score": 1,
            "intent": "Спам / Нерелевантный запрос",
            "budget_tier": "None",
            "priority": "COLD",
            "summary": "Спам-рассылка криптовалютного бота.",
            "recommended_action": "Заблокировать контакт, отправить в архив."
        }

def test_local_simulation():
    print("=" * 65)
    print("n8n Lead Intake & Scoring Engine — Simulation Suite")
    print("=" * 65)
    
    for i, lead in enumerate(SAMPLE_LEADS, 1):
        print(f"\n[ТЕСТ #{i}] Получен лид от: {lead['name']}")
        print(f"Контакт: {lead['contact']}")
        print(f"Текст: {lead['task_details']}")
        
        evaluation = evaluate_lead_mock(lead)
        
        badge = "[HOT - МГНОВЕННЫЙ АЛЕРТ РОПУ]" if evaluation['priority'] == 'HOT' else \
                "[WARM - СТАНДАРТНАЯ ОЧЕРЕДЬ]" if evaluation['priority'] == 'WARM' else \
                "[COLD - АРХИВ / СПАМ]"
                
        print(f"Скор: {evaluation['score']}/10  |  Приоритет: {badge}")
        print(f"Саммари: {evaluation['summary']}")
        print(f"Рекомендация: {evaluation['recommended_action']}")
        print("-" * 65)

def send_to_webhook(webhook_url: str):
    """Отправка первого лида на реальный вебхук n8n"""
    lead = SAMPLE_LEADS[0]
    payload = json.dumps(lead).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"Успешная отправка в n8n! HTTP {response.status}")
    except Exception as e:
        print(f"Вебхук n8n недоступен ({e}). Локальный тест работает автономно.")

if __name__ == "__main__":
    test_local_simulation()
