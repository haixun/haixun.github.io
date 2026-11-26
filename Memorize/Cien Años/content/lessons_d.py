# Lessons 31-40: paragraph 2, sentences 20 to 30, then the whole paragraph.  Same markup as lessons_a.py.

LESSONS_D = [

# ------------------------------------------------------------------ 31
dict(
  para=2, title="Melquíades proves his honesty",
  kind="lesson", new=[20], review=[18, 19],
  objectives=[
    "Understand sentence 20.",
    "Recognise three more preterites: <es>dio</es>, <es>devolvió</es>, <es>dejó</es>.",
    "Notice how the sentence answers a doubt raised in paragraph 1.",
  ],
  intro="""<p>In paragraph 1, José Arcadio Buendía <es>no creía en aquel tiempo en la honradez de los gitanos</es>. Here the gypsy gives him <es>una prueba convincente de honradez</es>. One long sentence closes the account.</p>""",
  grammar=[
    ("<es>Por último, cansado de esperar</es>", """<p><es>por último</es>, "finally". <es>cansado de</es> + infinitive, "tired of doing". <es>esperar</es> is the infinitive of <es>esperó</es> in the sentence before.</p>"""),
    ("<es>se lamentó ante Melquíades del fracaso de su iniciativa</es>", """<p><es>lamentarse de</es> something <es>ante</es> someone: to complain of it to them. <es>del</es> = <es>de</es> + <es>el</es>.
    <es>fracaso</es> returns from sentence 8, <es>el fracaso de sus imanes</es>: a second failure.</p>"""),
    ("<es>el gitano dio entonces una prueba</es>", """<p><es>dio</es> is the irregular preterite of <es>dar</es> (to give), one syllable and no accent. You met its imperfect in <es>daban a conocer</es>.</p>"""),
    ("The colon, then two gifts", """<p>After the colon comes the proof itself, in two clauses that both begin with <es>le</es>, "to him":
    <es>le devolvió los doblones</es> (he gave him back the doubloons) and <es>le dejó además...</es> (and he left him as well...).
    <es>devolver</es> is <b>de-</b> + <es>volver</es>: to make something come back.</p>"""),
    ("<es>a cambio de la lupa</es>", """<p>The same four words that ended sentence 10. The trade is undone.</p>"""),
    ("<es>unos mapas portugueses y varios instrumentos de navegación</es>", """<p><es>unos</es> is the plural of <es>un</es>: "some". <es>mapa</es> is masculine although it ends in -a. Nationalities have no capital letter: <es>portugueses</es>.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>último</es>: stress on the first syllable.</li><li><es>lamentó</es>, <es>devolvió</es>, <es>dejó</es>: final stress; <es>dejó</es> is <rs>de-HO</rs>.</li>
    <li><es>iniciativa</es>: <rs>ee-nee-sya-TEE-ba</rs>.</li><li><es>dio</es>: one syllable, <rs>dyo</rs>.</li><li><es>convincente</es>: <rs>kon-been-SEN-te</rs>.</li>
    <li><es>doblones</es>: <rs>do-BLO-nes</rs>.</li><li><es>portugueses</es>: gu before e is a hard g, <rs>por-tu-GEH-ses</rs>.</li><li><es>navegación</es>: <rs>na-be-ga-SYON</rs>.</li></ul>"""),
    ("Breaths", """<p>The narrator pauses at each comma and at the colon. Let the colon be the longest pause: what follows is the reveal.</p>"""),
  ],
  exercises=[
    ("Why did he complain to Melquíades?", "He was tired of waiting, and his venture had failed: <es>del fracaso de su iniciativa</es>."),
    ("What proof of honesty did the gypsy give?", "He gave back the doubloons in exchange for the magnifying glass."),
    ("What else did he leave?", "Some Portuguese maps and several navigation instruments."),
    ("Which sentence of paragraph 1 does <es>honradez</es> answer?", "<es>no creía en aquel tiempo en la honradez de los gitanos</es> (paragraph 1, sentence 11)."),
    ("What is the infinitive of <es>dio</es>?", "<es>dar</es>, to give."),
    ("Translate: <es>le dejó además unos mapas</es>.", "He left him some maps as well."),
  ],
  review_html="""<p>Recite sentences 18 and 19. The years of waiting end in today's first words: <es>Por último, cansado de esperar...</es></p>""",
  memo="""<p><b>Complaint, proof, two gifts.</b> Before the colon: tired → complained → the gypsy gave a proof. After the colon: he returned the gold; he left maps and instruments.</p>
  <p>Hold up two fingers for the two <es>le</es> clauses.</p>""",
),

# ------------------------------------------------------------------ 32
dict(
  para=2, title="The monk's notes and the little room",
  kind="lesson", new=[21, 22], review=[20],
  objectives=[
    "Understand sentences 21 and 22.",
    "Recognise <es>para que</es> + subjunctive: <es>pudiera</es>, <es>perturbara</es>.",
    "Meet the diminutive <b>-ito</b> and the word <es>nadie</es>.",
  ],
  intro="""<p>Melquíades writes out a guide to the instruments, and José Arcadio shuts himself away with them through the rainy season.</p>""",
  grammar=[
    ("<es>De su puño y letra</es>", """<p>An idiom: "of his fist and handwriting", that is, in his own hand. The subject of <es>escribió</es> is still Melquíades.</p>"""),
    ("<es>una apretada síntesis de los estudios del monje Hermann</es>", """<p><es>apretada</es>, "tight", "compact", stands before the noun for colour. <es>síntesis</es> is feminine. <es>del</es> = <es>de</es> + <es>el</es>.</p>"""),
    ("<es>que dejó a su disposición</es>", """<p><es>dejó</es> again, from sentence 20. <es>a su disposición</es>: "at his disposal", José Arcadio's.</p>"""),
    ("<es>para que pudiera servirse de...</es>", """<p><es>para</es> + infinitive is "in order to" when the same person does both things. When someone else is to do the second thing, Spanish says <es>para que</es> + subjunctive:
    Melquíades left the notes <em>so that José Arcadio could</em> use the instruments. <es>pudiera</es> is the subjunctive of <es>poder</es>; compare <es>podrá</es>, its future.
    And <es>servirse de</es> is what he wanted to do with the magnets in paragraph 1.</p>"""),
    ("<es>del astrolabio, la brújula y el sextante</es>", """<p>Three instruments, each with its article. <es>del</es> covers only the first.</p>"""),
    ("<es>pasó los largos meses de lluvia</es>", """<p><es>pasó</es>, preterite: the whole season summed up as one event. In sentence 16 the same verb was imperfect, <es>pasaba largas horas</es>, for a habit. <es>meses</es> you know from paragraph 1.</p>"""),
    ("<es>encerrado en un cuartito</es>", """<p><es>encerrado</es>, "shut in", a participle describing him. <es>cuartito</es> is <es>cuarto</es> (sentence 16) with the diminutive <b>-ito</b>: a little room.</p>"""),
    ("<es>que construyó en el fondo de la casa</es>", """<p><es>construyó</es> is the preterite of <es>construir</es>; its participle, <es>construidas</es>, described the houses of Macondo. <es>el fondo</es> was the bottom of the river in paragraph 1; of a house, it is the back.</p>"""),
    ("<es>para que nadie perturbara sus experimentos</es>", """<p><es>para que</es> + subjunctive again. <es>nadie</es> is "nobody"; it needs no <es>no</es> when it comes before the verb.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>puño</es>: <rs>POO-nyo</rs>.</li><li><es>síntesis</es>: stress on the first syllable.</li><li><es>monje</es>: <rs>MON-he</rs>.</li>
    <li><es>pudiera</es>: <rs>pu-DYEH-ra</rs>.</li><li><es>brújula</es>: j as h, stress on the first syllable, <rs>BROO-hu-la</rs>.</li><li><es>sextante</es>: <rs>seks-TAN-te</rs>.</li>
    <li><es>lluvia</es>: <rs>YOO-bya</rs>.</li><li><es>encerrado</es>: rolled rr, <rs>en-se-RRA-do</rs>.</li><li><es>construyó</es>: <rs>kons-tru-YO</rs>.</li><li><es>nadie</es>: <rs>NA-dye</rs>.</li></ul>"""),
  ],
  exercises=[
    ("Who wrote the summary, and of what?", "Melquíades, in his own hand: a summary of the studies of the monk Hermann."),
    ("Name the three instruments.", "<es>el astrolabio, la brújula y el sextante</es>: the astrolabe, the compass and the sextant."),
    ("Where did José Arcadio spend the rainy months?", "Shut up in a little room he built at the back of the house."),
    ("Why did he build it?", "So that nobody would disturb his experiments: <es>para que nadie perturbara sus experimentos</es>."),
    ("Why <es>para que pudiera</es> and not <es>para poder</es>?", "The person who is to use the instruments (José Arcadio) is not the subject of the main verb (Melquíades), so Spanish needs <es>para que</es> + subjunctive."),
    ("What does <b>-ito</b> add to <es>cuarto</es>?", "Smallness: <es>cuartito</es>, a little room."),
  ],
  review_html="""<p>Recite sentence 20. Today's sentence 21 continues with the same subject, Melquíades, although his name is not repeated.</p>""",
  memo="""<p><b>Two "so that"s.</b> Each sentence ends with <es>para que</es>: the notes, so that he could use the instruments; the little room, so that nobody would disturb him.</p>
  <p>Fix the three instruments in the order the text gives them: astrolabe, compass, sextant.</p>""",
),

# ------------------------------------------------------------------ 33
dict(
  para=2, title="Nights under the stars",
  kind="lesson", new=[23, 24], review=[21, 22],
  objectives=[
    "Understand sentences 23 and 24.",
    "Recognise <es>habiendo</es> + participle (having done) and <es>hacerse</es> (to become).",
    "Follow a sentence that turns on three infinitives.",
  ],
  intro="""<p>He abandons the household entirely, watches the stars, and learns to travel the world without leaving his room: the very thing Melquíades prophesied in sentence 6.</p>""",
  grammar=[
    ("<es>Habiendo abandonado por completo las obligaciones domésticas</es>", """<p><es>habiendo</es> is the gerund of <es>haber</es>; with a participle it means "having done". <es>por completo</es>, "completely", is built like <es>por entero</es>.
    <es>domésticas</es> echoes <es>el desmedrado patrimonio doméstico</es> of paragraph 1.</p>"""),
    ("<es>permaneció noches enteras en el patio</es>", """<p><es>permanecer</es>, "to remain". <es>noches enteras</es>, "whole nights"; you met <es>entero</es> in <es>por entero</es>.</p>"""),
    ("<es>vigilando el curso de los astros</es>", """<p>A gerund again, for what he was doing all the while. <es>astro</es> is any heavenly body.</p>"""),
    ("<es>estuvo a punto de contraer una insolación</es>", """<p>The third <es>estuvo a punto de</es>. A man who nearly gets sunstroke by night-watching: the cause follows.</p>"""),
    ("<es>por tratar de establecer un método exacto para encontrar el mediodía</es>", """<p><es>por</es> + infinitive gives the cause: "from trying to". Then <es>tratar de</es> + infinitive, then <es>para</es> + infinitive: three infinitives in a chain. He wanted to find the exact moment of noon, hence the sun.</p>"""),
    ("<es>Cuando se hizo experto</es>", """<p><es>hacerse</es> + adjective is "to become". <es>hizo</es> alone was "made" in paragraph 1.</p>"""),
    ("<es>tuvo una noción del espacio que le permitió...</es>", """<p><es>tuvo</es> is the irregular preterite of <es>tener</es>; in the preterite it means "got", "came to have". <es>le permitió</es>: "allowed him".</p>"""),
    ("Three infinitives after <es>permitió</es>", """<p><es>navegar por mares incógnitos</es>, <es>visitar territorios deshabitados</es> <es>y trabar relación con seres espléndidos</es>: verb + noun + adjective, three times.
    <es>deshabitados</es> has the prefix <b>des-</b> you know: un-inhabited.</p>"""),
    ("<es>sin necesidad de abandonar su gabinete</es>", """<p>Compare sentence 6: <es>sin moverse de su casa</es>. The prophecy comes true, in his imagination.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>habiendo</es>: silent h, <rs>a-BYEN-do</rs>.</li><li><es>obligaciones</es>: <rs>o-blee-ga-SYO-nes</rs>.</li><li><es>permaneció</es>: <rs>per-ma-ne-SYO</rs>.</li>
    <li><es>vigilando</es>: g before i as h, <rs>bee-hee-LAN-do</rs>.</li><li><es>insolación</es>: <rs>een-so-la-SYON</rs>.</li><li><es>hizo</es>: <rs>EE-so</rs>.</li>
    <li><es>incógnitos</es>: stress on <rs>KOG</rs>.</li><li><es>deshabitados</es>: silent h, <rs>de-sa-bee-TA-dos</rs>.</li><li><es>espléndidos</es>: stress on <rs>PLEN</rs>.</li>
    <li><es>gabinete</es>: <rs>ga-bee-NEH-te</rs>.</li></ul>"""),
  ],
  exercises=[
    ("What had he abandoned?", "His household duties, completely: <es>las obligaciones domésticas</es>."),
    ("Where did he spend whole nights, doing what?", "In the courtyard, watching the course of the stars."),
    ("Why did he nearly get sunstroke?", "From trying to establish an exact method for finding noon."),
    ("What three things could he do without leaving his study?", "Sail unknown seas, visit uninhabited territories, and strike up relations with splendid beings."),
    ("Translate: <es>se hizo experto</es>.", "He became expert."),
    ("Which earlier phrase does <es>sin necesidad de abandonar su gabinete</es> recall?", "<es>sin moverse de su casa</es>, in Melquíades' prophecy (sentence 6)."),
  ],
  review_html="""<p>Recite sentences 21 and 22, and name the three instruments. Today he learns to use them.</p>""",
  memo="""<p><b>Three and three.</b> Sentence 23 turns on three verbs of his (<es>permaneció</es>, <es>vigilando</es>, <es>estuvo a punto de</es>); sentence 24 on three journeys (<es>navegar</es>, <es>visitar</es>, <es>trabar relación</es>).
  For the journeys, remember: seas, lands, beings, each with its adjective.</p>""",
),

# ------------------------------------------------------------------ 34
dict(
  para=2, title="Talking to himself",
  kind="lesson", new=[25], review=[23, 24],
  objectives=[
    "Understand sentence 25.",
    "Use <es>mientras</es> (while) and the idioms <es>hablar a solas</es> and <es>partirse el espinazo</es>.",
    "Pronounce six Caribbean crops.",
  ],
  intro="""<p>The sentence splits in two at <es>mientras</es>: on one side a man pacing and muttering, on the other a woman and children bent over the vegetable plot.</p>""",
  grammar=[
    ("<es>Fue esa la época en que...</es>", """<p><es>fue</es> = "was" (from <es>ser</es>). <es>esa</es> is "that", the middle distance between <es>esta</es> and <es>aquella</es>. Putting it before the noun phrase is emphatic: "That was the time when...".
    <es>en que</es> after a time word, as in <es>aquella tarde remota en que</es>.</p>"""),
    ("<es>adquirió el hábito de hablar a solas</es>", """<p><es>el hábito de</es> + infinitive. <es>a solas</es>, "alone"; <es>hablar a solas</es> is to talk to oneself.</p>"""),
    ("<es>paseándose por la casa</es>", """<p>The gerund of <es>pasearse</es> with <es>se</es> attached. Adding a syllable would shift the stress, so a written accent holds it in place: <es>paseando</es> → <es>paseándose</es>.</p>"""),
    ("<es>sin hacer caso de nadie</es>", """<p><es>hacer caso de</es>, "to pay attention to". After <es>sin</es>, Spanish uses the negative word: literally "without paying attention to nobody".</p>"""),
    ("<es>mientras Úrsula y los niños se partían el espinazo</es>", """<p><es>mientras</es>, "while", with the imperfect for what was going on in the background. <es>partirse el espinazo</es>, "to break one's back": the body part takes <es>el</es>, as in <es>con el dedo</es>.</p>"""),
    ("<es>cuidando...</es> and six crops", """<p><es>cuidar</es> is "to look after"; you met the noun in <es>al cuidado de</es>. Then three pairs, each joined by <es>y</es>:
    <es>el plátano y la malanga</es>, <es>la yuca y el ñame</es>, <es>la ahuyama y la berenjena</es>. Spanish names each crop in the singular with its article.</p>"""),
  ],
  pron=[
    ("The crops", """<ul><li><es>plátano</es>: stress on the first syllable, <rs>PLA-ta-no</rs>.</li><li><es>malanga</es>: <rs>ma-LAN-ga</rs>.</li><li><es>yuca</es>: <rs>YOO-ka</rs>.</li>
    <li><es>ñame</es>: <rs>NYA-me</rs>.</li><li><es>ahuyama</es>: silent h, <rs>a-u-YA-ma</rs>.</li><li><es>berenjena</es>: j as h, <rs>be-ren-HEH-na</rs>.</li></ul>"""),
    ("Other points", """<ul><li><es>época</es>, <es>hábito</es>: accent on the first syllable; the h of <es>hábito</es> and <es>hablar</es> is silent.</li><li><es>adquirió</es>: <rs>ad-kee-RYO</rs>.</li>
    <li><es>paseándose</es>: <rs>pa-se-AN-do-se</rs>.</li><li><es>espinazo</es>: <rs>es-pee-NA-so</rs>.</li><li><es>huerta</es>: <rs>WER-ta</rs>.</li></ul>"""),
  ],
  exercises=[
    ("What habit did he acquire?", "Talking to himself: <es>hablar a solas</es>."),
    ("How did he move about the house?", "Pacing, without paying attention to anyone: <es>sin hacer caso de nadie</es>."),
    ("What were Úrsula and the children doing meanwhile?", "Breaking their backs in the garden, tending the crops."),
    ("Name the six crops.", "<es>el plátano, la malanga, la yuca, el ñame, la ahuyama, la berenjena</es>: plantain, taro, cassava, yam, squash, aubergine."),
    ("Why does <es>paseándose</es> have a written accent?", "Attaching <es>se</es> adds a syllable; the accent keeps the stress on <rs>AN</rs>."),
    ("Translate: <es>Fue esa la época en que</es>.", "That was the time when."),
  ],
  review_html="""<p>Recite sentences 23 and 24. He travels the world in his head; today you see who pays for it.</p>""",
  memo="""<p><b>The hinge is <es>mientras</es>.</b> Before it: the time, the habit, the pacing, the ignoring. After it: who, doing what, where, and the six crops.</p>
  <p>The crops alternate gender within each pair: <es>el ... la</es>, <es>la ... el</es>, <es>la ... la</es>. Say them as three pairs with a small pause between.</p>""",
),

# ------------------------------------------------------------------ 35
dict(
  para=2, title="Checkpoint 7: the instruments",
  kind="review", new=[], review=list(range(20, 26)),
  objectives=[
    "Read sentences 20 to 25 aloud as one scene.",
    "Recognise the subjunctive when you see it.",
    "Recite sentences 20 to 25, and read 1 to 25 from the top.",
  ],
  intro="""<p>Five sixths of the paragraph is behind you. This scene has the most new nouns; the next and last has the fewest words and the biggest moment.</p>""",
  grammar=[
    ("The subjunctive, collected", """<table class="mini"><tr><th>Trigger</th><th>Form</th><th>Meaning</th></tr>
    <tr><td><es>tan pronto como</es> (a future event)</td><td><es>se lo ordenara</es></td><td>as soon as it ordered him</td></tr>
    <tr><td><es>para que</es></td><td><es>pudiera servirse</es></td><td>so that he could use</td></tr>
    <tr><td><es>para que</es></td><td><es>nadie perturbara</es></td><td>so that nobody would disturb</td></tr></table>
    <p>All three are in the past subjunctive, whose mark is <b>-ara</b> or <b>-iera</b>. Recognising it is enough for this course.</p>"""),
    ("Participles describing him", """<p><es>entregado por entero</es> (13) · <es>cansado de esperar</es> (20) · <es>encerrado en un cuartito</es> (22). Later: <es>hechizado</es> (27), <es>devastado</es> (29). A portrait in five participles.</p>"""),
    ("Gerunds: what was going on", """<p><b>-ando</b>: <es>tratando</es>, <es>vigilando</es>, <es>cuidando</es>, <es>temblando</es>. <b>-iendo</b>: <es>haciendo</es>, <es>habiendo</es>. With <es>se</es> attached: <es>paseándose</es>, <es>repitiéndose</es>.</p>"""),
    ("Ways to say \"without\"", """<p><es>sin moverse de su casa</es> · <es>sin necesidad de abandonar su gabinete</es> · <es>sin hacer caso de nadie</es>; and still to come, <es>sin ningún anuncio</es> and <es>sin dar crédito</es>.</p>"""),
  ],
  pron=[
    ("Stress three from the end", """<p>These all carry a written accent three syllables from the end: <es>último</es>, <es>síntesis</es>, <es>brújula</es>, <es>método</es>, <es>incógnitos</es>, <es>espléndidos</es>, <es>época</es>, <es>hábito</es>, <es>plátano</es>, <es>domésticas</es>. Read the list, hitting the accent each time.</p>"""),
    ("Shadow the scene", """<p>Sentences 20 to 25 at 0.75×, then at full speed.</p>"""),
  ],
  exercises=[
    ("What did Melquíades give back, and what did he leave?", "The doubloons; and Portuguese maps, navigation instruments, and a handwritten summary of the monk Hermann's studies."),
    ("Translate: <es>para que nadie perturbara sus experimentos</es>.", "So that nobody would disturb his experiments."),
    ("How many times has <es>estuvo a punto de</es> appeared, and of doing what?", "Three: of setting the house on fire (15), of perishing (17, the messenger), of getting sunstroke (23)."),
    ("Complete: <es>navegar por mares incógnitos, visitar...</es>", "<es>...territorios deshabitados y trabar relación con seres espléndidos</es>."),
    ("Give the Spanish for: maps, compass, rain, nights, stars, children, garden.", "<es>mapas, brújula, lluvia, noches, astros, niños, huerta</es>."),
    ("What are the first words of sentences 20 to 25?", "<es>Por último</es> · <es>De su puño</es> · <es>José Arcadio Buendía pasó</es> · <es>Habiendo abandonado</es> · <es>Cuando se hizo</es> · <es>Fue esa</es>."),
  ],
  review_html="""<p>Sentences 20 to 25: play, shadow, read alone. Then read sentences 1 to 25 from the top.</p>""",
  memo="""<p><b>Gift, guide, room, nights, journeys, garden.</b> Six sentences, six images. Recite them in the practice box, then try sentences 13 to 25 together.</p>""",
),

# ------------------------------------------------------------------ 36
dict(
  para=2, title="The spell breaks",
  kind="lesson", new=[26, 27, 28], review=[25],
  objectives=[
    "Understand sentences 26 to 28.",
    "Recognise the passive: <es>fue sustituida por</es>.",
    "Use <es>de pronto</es>, <es>por fin</es>, <es>en voz baja</es> and <es>a sí mismo</es>.",
  ],
  intro="""<p>The fever of activity stops. For days he mutters to himself; then, one Tuesday at lunch, it comes out. Three medium sentences, each with a time phrase at the front.</p>""",
  grammar=[
    ("<es>De pronto, sin ningún anuncio</es>", """<p><es>pronto</es> alone is "soon" (<es>Muy pronto ha de sobrarnos oro</es>); <es>de pronto</es> is "suddenly". <es>ningún</es> is <es>ninguno</es> shortened before a masculine noun: "without any warning".</p>"""),
    ("<es>su actividad febril se interrumpió</es>", """<p><es>se interrumpió</es>: "broke off", "stopped of itself". <es>febril</es> comes from <es>fiebre</es>, fever, which appears in sentence 29.</p>"""),
    ("<es>y fue sustituida por una especie de fascinación</es>", """<p>The passive: <es>ser</es> + participle + <es>por</es>, "was replaced by". The participle agrees with the subject: <es>actividad</es> is feminine, so <es>sustituida</es>. <es>una especie de</es>, "a kind of".</p>"""),
    ("<es>Estuvo varios días como hechizado</es>", """<p><es>estuvo</es>, from <es>estar</es>, for a state he was in. <es>como hechizado</es>, "as if bewitched"; <es>hechizo</es> is a spell.</p>"""),
    ("<es>repitiéndose a sí mismo en voz baja</es>", """<p><es>repetir</es> → gerund <es>repitiendo</es>, with <es>se</es> attached and an accent to hold the stress. <es>a sí mismo</es>, "to himself": <es>sí</es> is the form of <es>se</es> used after a preposition.
    <es>en voz baja</es> is the opposite of <es>en voz alta</es>: in paragraph 1 he recited the spell aloud; now he whispers.</p>"""),
    ("<es>un sartal de asombrosas conjeturas</es>", """<p><es>sartal</es> is a string of beads, hence a string of anything. <es>conjeturas</es> returns from <es>el acierto de sus conjeturas</es>, and <es>asombrosas</es> is this paragraph's favourite adjective.</p>"""),
    ("<es>sin dar crédito a su propio entendimiento</es>", """<p><es>dar crédito a</es>, "to believe". <es>propio</es> before the noun: "his own understanding".</p>"""),
    ("<es>Por fin, un martes de diciembre, a la hora del almuerzo</es>", """<p><es>por fin</es>, "at last": stronger than <es>por último</es>, it carries relief. Days and months have no capital. <es>a la hora de</es>: "at the time of".</p>"""),
    ("<es>soltó de un golpe toda la carga de su tormento</es>", """<p><es>soltar</es>, "to let go". <es>de un golpe</es>, "at one blow", all at once.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>ningún</es>: stress on the last syllable.</li><li><es>interrumpió</es>: rolled rr, <rs>een-te-rrum-PYO</rs>.</li><li><es>sustituida</es>: <rs>sus-tee-TWEE-da</rs>.</li>
    <li><es>fascinación</es>: sc before i is a single s in Latin America, <rs>fa-see-na-SYON</rs>.</li><li><es>hechizado</es>: silent h, <rs>e-chee-SA-do</rs>.</li>
    <li><es>repitiéndose</es>: <rs>rre-pee-TYEN-do-se</rs>.</li><li><es>entendimiento</es>: <rs>en-ten-dee-MYEN-to</rs>.</li><li><es>almuerzo</es>: <rs>al-MWER-so</rs>.</li></ul>"""),
    ("Quiet, then sudden", """<p>Read sentence 27 softly, as he does. In sentence 28 hold back through the three time phrases, then let <es>soltó de un golpe</es> come out fast.</p>"""),
  ],
  exercises=[
    ("What replaced his feverish activity?", "A kind of fascination: <es>una especie de fascinación</es>."),
    ("What did he do for several days?", "Went about as if bewitched, repeating astonishing conjectures to himself under his breath, not believing his own mind."),
    ("When exactly did he speak?", "One Tuesday in December, at lunchtime."),
    ("Why <es>sustituida</es>, with -a?", "The participle in a passive agrees with its subject, <es>su actividad</es>, which is feminine."),
    ("Give the opposite of <es>en voz baja</es>, from paragraph 1.", "<es>en voz alta</es>."),
    ("<es>pronto</es> and <es>de pronto</es>: what does each mean?", "\"Soon\"; \"suddenly\"."),
  ],
  review_html="""<p>Recite sentence 25, with its six crops. The children in the garden are about to become his audience.</p>""",
  memo="""<p><b>Three time signals.</b> <es>De pronto</es> (suddenly) → <es>Estuvo varios días</es> (for several days) → <es>Por fin</es> (at last). Each opens a sentence; learn them as a chain and the rest hangs from them.</p>
  <p>Sentence 28 narrows like a calendar: a Tuesday → in December → at lunchtime.</p>""",
),

# ------------------------------------------------------------------ 37
dict(
  para=2, title="\"The earth is round, like an orange\"",
  kind="lesson", new=[29, 30], review=[26, 27, 28],
  objectives=[
    "Understand sentences 29 and 30, the end of the paragraph.",
    "Hear the echo of the novel's first sentence in <es>habían de recordar</es>.",
    "Deliver the last line.",
  ],
  intro="""<p>The paragraph ends as the novel began: with a memory that lies in the future. Then seven of the simplest words in the whole text.</p>""",
  grammar=[
    ("<es>Los niños habían de recordar</es>", """<p>The first sentence of the novel: <es>el coronel Aureliano Buendía había de recordar aquella tarde remota</es>. Here is the same construction in the plural, <es>habían de recordar</es>, "were to remember".
    One of these children is that colonel.</p>"""),
    ("<es>por el resto de su vida</es>", """<p>"For the rest of their lives". <es>su</es> is "their"; Spanish keeps <es>vida</es> singular, one life each.</p>"""),
    ("<es>la augusta solemnidad con que su padre se sentó</es>", """<p><es>con que</es>, "with which". <es>se sentó</es>, "sat down": the reflexive partner of <es>sentaron una gitana</es> in sentence 3. <es>su padre</es> is "their father",
    and it too is in the novel's first sentence: <es>su padre lo llevó a conocer el hielo</es>.</p>"""),
    ("<es>a la cabecera de la mesa</es>", """<p><es>cabecera</es> comes from <es>cabeza</es>, head: the head of the table.</p>"""),
    ("Two descriptions between commas", """<p><es>temblando de fiebre</es>: a gerund, with <es>de</es> for the cause, as in <es>lloró de consternación</es>.
    <es>devastado por la prolongada vigilia y por el encono de su imaginación</es>: a participle with two causes, each introduced by <es>por</es>. <es>su imaginación</es> is the <es>desaforada imaginación</es> of paragraph 1.</p>"""),
    ("<es>y les reveló su descubrimiento:</es>", """<p><es>les</es>, "to them". <es>descubrimiento</es> appeared in sentence 2 as the gypsies' "latest discovery"; now he has one of his own. The colon hands over to his voice.</p>"""),
    ("<es>—La tierra es redonda como una naranja.</es>", """<p>A line of dialogue set on its own is introduced by a long dash, with no closing mark. <es>es</es>, from <es>ser</es>, because roundness is what the earth <em>is</em>.
    <es>redonda</es> agrees with <es>la tierra</es>. <es>como</es>, "like", as in <es>como huevos prehistóricos</es>.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>habían</es>: silent h, <rs>a-BEE-an</rs>.</li><li><es>augusta</es>: <rs>aw-GOOS-ta</rs>.</li><li><es>solemnidad</es>: <rs>so-lem-nee-DATH</rs>, with a very soft final d.</li>
    <li><es>cabecera</es>: <rs>ka-be-SEH-ra</rs>.</li><li><es>fiebre</es>: <rs>FYEH-bre</rs>.</li><li><es>vigilia</es>: g as h, <rs>bee-HEE-lya</rs>.</li>
    <li><es>redonda</es>: rolled initial r.</li><li><es>naranja</es>: j as h, <rs>na-RAN-ha</rs>.</li></ul>"""),
    ("The last line", """<p>Sentence 29 is one long approach: let it build through the commas and stop at the colon. Leave a real pause. Then say the last line simply and evenly, every syllable the same weight:
    <es>La tie-rra es re-don-da co-mo u-na na-ran-ja</es>. Listen to how the narrator does it.</p>"""),
  ],
  exercises=[
    ("What were the children to remember?", "The august solemnity with which their father sat down at the head of the table."),
    ("In what state was he?", "Trembling with fever, devastated by the long vigil and by the fury of his imagination."),
    ("What did he reveal?", "His discovery: <es>La tierra es redonda como una naranja</es>, the earth is round, like an orange."),
    ("Which sentence does <es>habían de recordar</es> echo?", "The first sentence of the novel: <es>había de recordar aquella tarde remota</es>."),
    ("Why <es>es</es> and not a form of <es>estar</es>?", "Being round is a permanent characteristic, what the earth is, so <es>ser</es>."),
    ("How does Spanish mark a line of dialogue set on its own?", "With a long dash at the start, and nothing at the end."),
  ],
  review_html="""<p>Recite sentences 26 to 28, ending on <es>toda la carga de su tormento</es>. Today's sentence shows the scene from the children's side.</p>""",
  memo="""<p><b>Frame, two asides, revelation.</b> The frame: <es>Los niños habían de recordar ... la augusta solemnidad con que su padre se sentó a la cabecera de la mesa ... y les reveló su descubrimiento</es>.
  Inside it, two asides: <es>temblando de fiebre</es>, and <es>devastado por ... y por ...</es></p>
  <p>The last line needs no technique. Say it three times and you have it for life.</p>""",
),

# ------------------------------------------------------------------ 38
dict(
  para=2, title="Checkpoint 8: the whole second paragraph aloud",
  kind="review", new=[], review=list(range(26, 31)),
  objectives=[
    "Read sentences 26 to 30 fluently, then the whole paragraph from start to finish.",
    "Hold the paragraph in your head as five scenes.",
    "Shadow the full recording.",
  ],
  intro="""<p>All thirty sentences are familiar now. As in Lesson 18, the work turns from understanding to fluency: one complete, unbroken reading of paragraph 2.</p>""",
  grammar=[
    ("The paragraph in five scenes", """<ol><li><b>The telescope</b> (sentences 1 to 6): the return, the telescope and the glass, the customers, the prophecy.</li>
    <li><b>The burning glass</b> (7 to 12): the fire, the idea, the trade, Úrsula's coins.</li>
    <li><b>The weapon of war</b> (13 to 19): experiments, burns, the manual, the messenger, the promise, the waiting.</li>
    <li><b>The instruments</b> (20 to 25): the gold returned, the monk's notes, the little room, the stars, the imagined voyages, the garden.</li>
    <li><b>The discovery</b> (26 to 30): the trance, the Tuesday in December, the orange.</li></ol>"""),
    ("The story in its preterites", """<p><es>volvieron</es> · <es>exhibieron</es> · <es>sentaron</es> · <es>instalaron</es> · <es>hicieron</es> · <es>pusieron</es> · <es>prendieron</es> · <es>concibió</es> · <es>trató</es> · <es>terminó</es> · <es>lloró</es> ·
    <es>se expuso</es> · <es>sufrió</es> · <es>estuvo</es> · <es>logró</es> · <es>envió</es> · <es>esperó</es> · <es>se lamentó</es> · <es>dio</es> · <es>devolvió</es> · <es>dejó</es> · <es>escribió</es> · <es>pasó</es> · <es>permaneció</es> ·
    <es>se hizo</es> · <es>tuvo</es> · <es>adquirió</es> · <es>se interrumpió</es> · <es>soltó</es> · <es>se sentó</es> · <es>reveló</es>. Read the list aloud: it is the plot.</p>"""),
    ("Threads between the two paragraphs", """<p><es>había de recordar</es> / <es>habían de recordar</es> · <es>la honradez de los gitanos</es> / <es>una prueba convincente de honradez</es> · <es>servirse de aquella invención inútil</es> / <es>para que pudiera servirse del astrolabio</es> ·
    <es>en voz alta</es> / <es>en voz baja</es> · <es>el acierto de sus conjeturas</es> / <es>un sartal de asombrosas conjeturas</es> · <es>desaforada imaginación</es> / <es>el encono de su imaginación</es> · <es>conocer el hielo</es> / <es>su descubrimiento</es>.</p>"""),
  ],
  pron=[
    ("Shadow, then solo", """<p>The narrator takes about six minutes forty. Shadow the whole paragraph at 0.75×, then at full speed, then read it alone. A comfortable first target is under ten minutes.</p>"""),
    ("Where to breathe", """<p>At full stops, and at the commas where the narrator pauses. Sentences 17 and 18 need a plan: go back to Lessons 28 and 29 if you run out of air.</p>"""),
    ("Record yourself", """<p>Record one full reading and listen against the text. Pick the three sentences that sound least secure and drill those alone.</p>"""),
  ],
  exercises=[
    ("Name the five scenes in order.", "The telescope; the burning glass; the weapon of war; the instruments; the discovery."),
    ("Give the first words of the sentence that opens each scene.", "<es>En marzo volvieron</es> (1) · <es>Un mediodía ardiente</es> (7) · <es>José Arcadio Buendía no trató</es> (13) · <es>Por último</es> (20) · <es>De pronto</es> (26)."),
    ("Translate: <es>su actividad febril se interrumpió</es>.", "His feverish activity broke off."),
    ("Translate: <es>soltó de un golpe toda la carga de su tormento</es>.", "He let out all at once the whole burden of his torment."),
    ("Complete: <es>devastado por la prolongada vigilia y por...</es>", "<es>...el encono de su imaginación</es>."),
    ("Which prophecy of Melquíades does José Arcadio fulfil in his study?", "<es>el hombre podrá ver lo que ocurre en cualquier lugar de la tierra, sin moverse de su casa</es>: he travels <es>sin necesidad de abandonar su gabinete</es>."),
  ],
  review_html="""<p>Sentences 26 to 30 first: play, shadow, read alone. Then the full read-through. Tick the box only after one complete reading with no restart.</p>""",
  memo="""<p><b>Scene by scene.</b> Recite each scene on its own in the practice box at whatever level is just hard enough. Scenes 3 and 4 will need the most time.</p>""",
),

# ------------------------------------------------------------------ 39
dict(
  para=2, title="Memorising the second paragraph",
  kind="review", new=[], review=list(range(1, 31)),
  objectives=[
    "Recite each of the five scenes from memory.",
    "Join them with a chain of thirty cue words.",
    "Recite the complete paragraph with first-letter prompts only.",
  ],
  intro="""<p>The method is the one that worked for paragraph 1: a map, handles, and retrieval with less and less help. This paragraph is longer, so spread the work over three or four days.</p>""",
  grammar=[
    ("The thirty handles", """<ol class="cues"><li><es>En marzo volvieron</es></li><li><es>Esta vez llevaban</es></li><li><es>Sentaron una gitana</es></li><li><es>Mediante el pago</es></li><li><es>«La ciencia</es></li>
    <li><es>«Dentro de poco</es></li><li><es>Un mediodía ardiente</es></li><li><es>José Arcadio Buendía, que aún</es></li><li><es>Melquíades, otra vez</es></li><li><es>Pero terminó</es></li>
    <li><es>Úrsula lloró</es></li><li><es>Aquel dinero</es></li><li><es>José Arcadio Buendía no trató</es></li><li><es>Tratando de demostrar</es></li><li><es>Ante las protestas</es></li>
    <li><es>Pasaba largas horas</es></li><li><es>Lo envió</es></li><li><es>A pesar de que</es></li><li><es>Durante varios años</es></li><li><es>Por último</es></li>
    <li><es>De su puño y letra</es></li><li><es>José Arcadio Buendía pasó</es></li><li><es>Habiendo abandonado</es></li><li><es>Cuando se hizo experto</es></li><li><es>Fue esa la época</es></li>
    <li><es>De pronto</es></li><li><es>Estuvo varios días</es></li><li><es>Por fin</es></li><li><es>Los niños habían de recordar</es></li><li><es>—La tierra</es></li></ol>
    <p>Three sentences begin with <es>José Arcadio Buendía</es> (8, 13, 22). Learn what follows the name in each: <es>que aún</es>, <es>no trató</es>, <es>pasó</es>.</p>"""),
    ("Known trouble spots", """<ul><li>Sentence 12: the order <es>acumulado</es> → <es>enterrado</es> → <es>en espera de</es> → <es>invertirlas</es>.</li>
    <li>Sentence 16: <es>asombrosa claridad didáctica</es>, then <es>poder de convicción irresistible</es>.</li>
    <li>Sentence 17: the messenger's four verbs in order, and <es>las fieras, la desesperación y la peste</es>.</li>
    <li>Sentence 18: <es>hacer demostraciones prácticas</es> before <es>adiestrarlos personalmente</es>.</li>
    <li>Sentence 24: seas, lands, beings.</li><li>Sentence 25: the six crops in three pairs.</li>
    <li><es>por último</es> (20) against <es>por fin</es> (28); <es>por entero</es> (13) against <es>por completo</es> (23).</li></ul>"""),
    ("Meaning first", """<p>Before each scene, read its English once. Then recite the Spanish while picturing the scene. A phrase you can picture is far harder to lose.</p>"""),
  ],
  pron=[
    ("Aloud, standing, at speaking volume", """<p>As before. If a word will not come, hum its rhythm, carry on, and check afterwards.</p>"""),
  ],
  exercises=[
    ("Say the thirty handles in order.", "See the list above; check yourself against it."),
    ("English to Spanish: \"In March the gypsies came back.\"", "<es>En marzo volvieron los gitanos.</es>"),
    ("English to Spanish: \"Science has eliminated distances.\"", "<es>La ciencia ha eliminado las distancias.</es>"),
    ("English to Spanish: \"Úrsula wept with dismay.\"", "<es>Úrsula lloró de consternación.</es>"),
    ("English to Spanish: \"For several years he waited for the answer.\"", "<es>Durante varios años esperó la respuesta.</es>"),
    ("What comes after <es>al cuidado de un mensajero que...</es>?", "<es>...atravesó la sierra, se extravió en pantanos desmesurados, remontó ríos tormentosos y estuvo a punto de perecer...</es>"),
    ("What comes after <es>y les reveló su descubrimiento:</es>?", "<es>—La tierra es redonda como una naranja.</es>"),
  ],
  review_html="""<p>Warm up with one full read-aloud of paragraph 2, shadowing the recording at normal speed.</p>""",
  memo="""<p><b>The ladder.</b></p>
  <ol><li>Each scene alone at level 4 (first letters only).</li><li>Scenes 1+2, then 3, then 4+5, still with first letters.</li>
  <li>The whole paragraph with first letters.</li><li>The whole paragraph at level 5, counting your peeks.</li></ol>
  <p><b>Space it out.</b> One scene a day for five days, each day starting with a quick recital of the scenes already done, works better than one long session.</p>""",
),

# ------------------------------------------------------------------ 40
dict(
  para=2, title="Final assessment: paragraph 2, and both together",
  kind="final", new=[], review=list(range(1, 31)),
  objectives=[
    "Show that you understand every sentence of paragraph 2.",
    "Read paragraph 2 aloud with steady rhythm and clear pronunciation.",
    "Recite paragraph 2 from memory, and then both paragraphs in one go.",
  ],
  intro="""<p>The same three tests as Lesson 20, for the second paragraph, and a last one that joins the two.</p>""",
  grammar=[
    ("Part A: Understanding", """<p>Answer the twenty questions under <b>Check yourself</b> before opening each answer. Sixteen or more correct is a pass. For any you miss, reread the lesson named in the answer.</p>"""),
    ("Part B: Reading aloud", """<p>Record yourself reading the whole of paragraph 2 once, with no restarts. Listen against the narrator and tick what is true:</p>
    <ul class="checks">
    <li data-check="b1">I read to the end without restarting.</li>
    <li data-check="b2">My vowels stayed pure in the small words (<es>de</es>, <es>que</es>, <es>en</es>, <es>por</es>).</li>
    <li data-check="b3">Preterites kept their final stress (<es>trató</es>, <es>envió</es>, <es>devolvió</es>, <es>soltó</es>).</li>
    <li data-check="b4">Long words came out even (<es>posibilidades estratégicas</es>, <es>demostraciones prácticas</es>, <es>personalmente</es>).</li>
    <li data-check="b5">I got through sentences 17 and 18 breathing only at the commas.</li>
    <li data-check="b6">My reading took less than ten minutes.</li></ul>
    <p>Five ticks out of six is a pass.</p>"""),
    ("Part C: Reciting from memory", """<p>Open the practice box below at level 5 with paragraph 2 selected and recite it aloud. Reveal a word only when truly stuck, and count the reveals.</p>
    <ul class="checks">
    <li data-check="c1">I recited all thirty sentences in order.</li>
    <li data-check="c2">I needed fifteen reveals or fewer.</li>
    <li data-check="c3">I needed five reveals or fewer.</li>
    <li data-check="c4">For any sentence chosen at random, I can say in English what it means.</li></ul>
    <p>The first, second and fourth ticks are a pass. The third is mastery.</p>"""),
    ("Part D: Both paragraphs", """<p>Choose "Both paragraphs" in the practice box and recite from <es>Muchos años después</es> to <es>como una naranja</es>: forty-seven sentences, about eleven minutes at the narrator's pace.</p>
    <ul class="checks">
    <li data-check="d1">I recited both paragraphs in one sitting.</li>
    <li data-check="d2">I can explain the link between the first sentence of paragraph 1 and the next-to-last sentence of paragraph 2.</li></ul>"""),
  ],
  pron=[],
  exercises=[
    ("1. What did the gypsies bring this time?", "A telescope and a magnifying glass the size of a drum. (Lesson 21)"),
    ("2. Why <es>e instalaron</es> and not <es>y instalaron</es>?", "<es>y</es> becomes <es>e</es> before the sound i. (Lesson 21)"),
    ("3. What did people see through the telescope?", "The gypsy woman, as if within reach of their hand. (Lesson 22)"),
    ("4. Translate <es>el hombre podrá ver</es>.", "Man will be able to see. (Lesson 22)"),
    ("5. How did the gypsies set the grass on fire?", "By concentrating the sun's rays with the magnifying glass. (Lesson 23)"),
    ("6. What use did José Arcadio see for it?", "As a weapon of war. (Lesson 23)"),
    ("7. What did Melquíades accept for it?", "The two magnetised ingots and three pieces of colonial money. (Lesson 24)"),
    ("8. Where had Úrsula kept her father's coins?", "Buried under the bed. (Lesson 24)"),
    ("9. Translate <es>no trató siquiera de consolarla</es>.", "He did not even try to console her. (Lesson 26)"),
    ("10. What happened when he tested the glass on himself?", "He suffered burns that turned into sores and were slow to heal. (Lesson 26)"),
    ("11. What does <es>estuvo a punto de</es> mean?", "He was on the point of; he almost. (Lesson 27)"),
    ("12. What did he compose?", "A manual, astonishingly clear and irresistibly convincing. (Lesson 27)"),
    ("13. Name two of the messenger's hardships.", "Any two: crossing the mountains, getting lost in swamps, going up stormy rivers, nearly perishing from beasts, despair and plague. (Lesson 28)"),
    ("14. What did he promise the government?", "To make the journey as soon as ordered, to demonstrate the invention and train the military. (Lesson 29)"),
    ("15. How did Melquíades prove his honesty?", "He gave back the doubloons in exchange for the magnifying glass. (Lesson 31)"),
    ("16. Name the three instruments.", "The astrolabe, the compass and the sextant. (Lesson 32)"),
    ("17. Translate <es>para que nadie perturbara sus experimentos</es>.", "So that nobody would disturb his experiments. (Lesson 32)"),
    ("18. What were Úrsula and the children doing while he paced?", "Breaking their backs in the garden, tending the crops. (Lesson 34)"),
    ("19. When did he announce his discovery?", "One Tuesday in December, at lunchtime. (Lesson 36)"),
    ("20. What was it?", "<es>La tierra es redonda como una naranja</es>: the earth is round, like an orange. (Lesson 37)"),
  ],
  review_html="""<p>Before you begin, play the whole of paragraph 2 once and simply listen, eyes closed. You should understand all of it.</p>""",
  memo="""<p>This box is your Part C and Part D. Set it to level 5 and begin with <es>En marzo volvieron los gitanos.</es></p>""",
),
]
