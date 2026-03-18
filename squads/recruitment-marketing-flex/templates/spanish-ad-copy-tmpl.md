# Spanish-Language Ad Copy — {{ROLE}} {{MARKET}}

> Template for creating bilingual ad variants across all channels
> Use when JD mentions Spanish support or market has >20% Hispanic population
> Markets with high Hispanic population: Dallas, Houston, Austin, Phoenix, Las Vegas, Orlando, Chicago

## Campaign Details

| Field | English | Spanish |
|-------|---------|---------|
| **Role** | {{ROLE_EN}} | {{ROLE_ES}} |
| **Client** | {{CLIENT}} | {{CLIENT}} |
| **Market** | {{CITY, STATE}} | {{CITY, STATE}} |
| **Pay** | ${{PAY_MIN}}-${{PAY_MAX}}/hr | ${{PAY_MIN}}-${{PAY_MAX}}/hora |
| **Landing Page** | {{URL}} | {{URL}} (same LP, Spanish support noted) |

## Role Translation Reference

| English | Spanish |
|---------|---------|
| Server | Mesero/a |
| Banquet Server | Mesero/a de Banquetes |
| Event Staff | Personal de Eventos |
| Bartender | Bartender / Cantinero/a |
| Housekeeper | Ama de Llaves / Limpieza |
| Line Cook | Cocinero/a de Línea |
| Prep Cook | Cocinero/a de Preparación |
| Dishwasher | Lavaplatos |
| Warehouse Worker | Trabajador de Almacén |
| Picker Packer | Empacador/a |
| Forklift Driver | Operador/a de Montacargas |
| General Labor | Trabajo General |
| Loader/Crew | Cargador / Equipo de Carga |
| Delivery Driver | Conductor de Entregas |

---

## Google Ads — Spanish Ad Group

### Headlines (10, 30 chars max each)

1. {{ROLE_ES}} — ${{PAY_MAX}}/hora
2. Trabajo en {{CITY}} — Aplica Ya
3. Contratando {{ROLE_ES}} Hoy
4. ${{PAY_MAX}}/hora — Horarios Flexibles
5. {{ROLE_ES}} — Eventos de Lujo
6. Turnos de Fin de Semana
7. Aplica en 2 Minutos
8. Sin Compromiso a Largo Plazo
9. Pago Semanal Garantizado
10. ¿Buscas Trabajo de {{ROLE_ES}}?

### Descriptions (3, 90 chars max each)

1. Buscamos {{ROLE_ES}} en {{CITY}}. ${{PAY_MIN}}-${{PAY_MAX}}/hora. Horarios flexibles, pago semanal. Aplica hoy.
2. Trabaja en los mejores eventos de {{CITY}}. Entrevista por IA en español. Empieza esta semana.
3. {{NUMBER}} posiciones abiertas de {{ROLE_ES}}. Sin experiencia previa requerida. Aplica ahora — es gratis.

### Display URL Paths
- Path 1: `{{ROLE_ES_SLUG}}` (e.g., "Mesero")
- Path 2: `{{CITY_SLUG}}` (e.g., "Dallas")

### Notes
- Set language targeting to **Spanish** in the ad group
- Use separate ad group from English (don't mix languages in same AG)
- Bid adjustment: start at same as English, adjust based on performance

---

## Meta Ads — Spanish Variant

### Primary Text
{{ROLE_ES}} en {{CITY}} — ${{PAY_MIN}}-${{PAY_MAX}}/hora. Elige tus turnos: almuerzos entre semana, cenas de fin de semana. Entrevista disponible en español. Aplica ahora — es gratis y toma menos de 2 minutos.

### Headline
{{ROLE_ES}} — ${{PAY_MAX}}/hora — {{CITY}}

### Description
Horarios flexibles. Pago semanal. Aplica hoy.

### CTA
Aplicar Ahora

### Targeting Notes
- Language: Spanish
- Same interest/behavior targeting as English variant
- Consider adding: Interests in "Hispanic culture", "Univision", "Telemundo"

---

## Reddit — Spanish Variant

### Free-Form Ad
> **Title:** ${{PAY_MIN}}-${{PAY_MAX}}/hora como {{ROLE_ES}} en {{CITY}} — turnos flexibles
>
> **Body:** Estamos buscando {{ROLE_ES}} para eventos exclusivos en {{CITY}}. Elige tus turnos, recibe pago semanal. La entrevista es por IA y disponible en español — toma como 10 minutos. Si tienes experiencia en hospitalidad, esto es para ti.
>
> **CTA:** Learn More
> **Comments:** Enabled

### Notes
- Post in r/{{CITY}} — many local subs have bilingual users
- Tone: conversational, not corporate
- Don't over-translate — use natural Spanglish where appropriate for authenticity

---

## Craigslist — Spanish Posting

### Title
{{ROLE_ES}} — ${{PAY_MIN}}-${{PAY_MAX}}/hora — Eventos Exclusivos en {{CITY}} (Tiempo Parcial, Flexible)

### Body
```
Entrevistas y apoyo disponibles en español

{{ROLE_ES}} | Eventos de Lujo y Funciones Privadas

Ubicación: Área de {{CITY}}
Compensación: ${{PAY_MIN}}-${{PAY_MAX}}/hora
Disponibilidad: Almuerzos entre semana, cenas de fin de semana, eventos especiales

Lo que ofrecemos:
- Horarios flexibles — tú eliges cuándo trabajar
- Pago semanal
- Eventos en los mejores lugares de {{CITY}}
- Entrevista por IA en español (solo 10 minutos)

Requisitos:
- Experiencia en hospitalidad preferida
- Bilingüe inglés/español preferido
- {{CERTIFICATION_ES}} requerido/a
- Disponibilidad para estar de pie por periodos prolongados

Aplica ahora: {{URL}}

Indeed Flex — Trabajo flexible, a tu manera.
```

### Notes
- Post in: gigs > event gigs AND food/bev/hosp section
- Refresh every 48 hours for visibility
- Include pay in title (Craigslist best practice)

---

## Braze — Spanish Push/SMS

### Push Notification
**Title:** Nuevo trabajo de {{ROLE_ES}} en {{CITY}}
**Body:** ${{PAY_MAX}}/hora — Elige tus turnos. Aplica ahora en la app.

### SMS
Hola! Hay turnos nuevos de {{ROLE_ES}} en {{CITY}} — ${{PAY_MIN}}-${{PAY_MAX}}/hora. Abre la app para reservar: {{SHORT_URL}}

### Notes
- Only send to users with language preference = Spanish OR who completed AI interview in Spanish
- Respect Braze frequency caps

---

## Quality Checklist

- [ ] All Spanish copy proofread (no machine-translation errors)
- [ ] Pay rate matches JD exactly
- [ ] City/market is correct
- [ ] Landing page URL has correct UTM parameters per channel
- [ ] Role translation uses natural terms (not literal translations)
- [ ] Spanish ad group is SEPARATE from English (never mix)
- [ ] Tone matches channel norms (Reddit = conversational, Google = direct, CL = simple)
