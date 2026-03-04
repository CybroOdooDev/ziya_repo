 Predict Late Payments — Google Gemini AI Edition
**Odoo 19 Module · Version 19.0.5.0.0**

AI-powered customer payment risk scoring using **Google Gemini 2.5 Flash**.

## Setup (2 minutes, no credit card)

### Step 1 — Get a free Gemini API key
1. Go to https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click **Create API key** → Copy it

### Step 2 — Configure in Odoo
```
Settings → General Settings → Payment Risk AI
→ Paste API key → Select model → Save → Test Connection
```

### Step 3 — Run scoring
```
Accounting → Payment Risk → Compute All Scores
```

---

## Free Tier Limits

| Model               | Requests/day (free) | Best for |
|---------------------|---------------------|----------|
| gemini-2.5-flash    | 250                 | Most users (recommended) |
| gemini-2.5-flash-lite | 1,000             | High volume / batch |
| gemini-2.0-flash    | 250                 | Stable alternative |
| gemini-2.5-pro      | 50                  | Highest quality |

---

## How It Works

```
Odoo invoice/payment data
        ↓
_collect_invoice_stats()   ← pure Python, no AI
        ↓
POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions
     model: gemini-2.5-flash
        ↓
JSON: score, risk_level, AI reasoning,
      follow-up suggestion, drafted email
        ↓
payment.risk.score record updated in Odoo
Risk badges shown on Customer + Invoice screens
```

Gemini uses the **OpenAI-compatible endpoint**, so the integration
is a simple REST call — no special SDK needed.

## Fallback
If the API key is missing or the free quota is exceeded,
the module automatically falls back to statistical rule-based
scoring. Nothing breaks.
