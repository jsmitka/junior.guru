---
title: Zkušenosti s PrimaKurzy
template: main_legacy.html
topic_name: primakurzy
topic_link_text: PrimaKurzy
description: Hledáš někoho, kdo má zkušenosti s PrimaKurzy? Vyplatí se jít na jejich akreditované IT kurzy?
---
{% from 'topic.html' import intro, mentions, members_roll %}

{{ intro('Recenze na PrimaKurzy', page.meta.description) }}

{{ mentions(topic, 'PrimaKurzy') }}

{{ members_roll(pages, members, members_total_count, club_elapsed_months) }}
