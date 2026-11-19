---
name: flujo-piezas-a-pedido
description: "How Achilata pieces get made: the schedule is a flexible base; build each piece only when asked, choosing from the whole gallery, then send the images and caption to the user's WhatsApp"
metadata:
  type: feedback
---

The user asked for this on 2026-11-19.

- **The schedule is a base, not fixed.** The user can ask any day for a piece that isn't planned, such as "a story with the prices for today". Make it right away, then adapt `fuente/datos.py`: drop or move whatever it replaces, and leave the rest as it is.
- **Never pre-build all the pieces.** Build each one only when it is asked for:
  1. Search the whole gallery and pick the best photo.
  2. Study the photo, then edit it and adapt it to the format.
  3. Design the piece following the manual.
- **When a piece is done:**
  1. Send every image to the user's WhatsApp "yo" chat as a document, in order.
  2. Send the clean caption in a separate message, so it is easy to copy.
  3. Save the piece in its folder's `final/` and log it.
- **The account must be very active:** something every day, and more from Thursday to Sunday.

**Why:** The user wants each piece made with the best images available at that moment, and posts from their phone.

**How to apply:** Follow the project CLAUDE.md "Cronograma y piezas" section. Related: [[reglas-contenido-achilata]], [[proyecto-achilata-salta]]
