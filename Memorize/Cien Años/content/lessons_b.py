# Lessons 11-20.  Same markup as lessons_a.py.

LESSONS_B = [

# ------------------------------------------------------------------ 11
dict(
  title="José Arcadio Buendía has an idea",
  kind="lesson", new=[9], review=[7, 8],
  objectives=[
    "Understand sentence 9: a subject, a long aside about his imagination, then <es>pensó que...</es>",
    "Use <es>cuya</es> (whose), comparisons with <es>más ... que</es>, and <es>más allá de</es> (beyond).",
    "Pronounce j and g in names and abstract nouns.",
  ],
  intro="""<p>The colonel's father steps forward. Like sentence 6, this one has a simple frame, <es>José Arcadio Buendía ... pensó que era posible...</es>,
  with a long aside between the subject and the verb.</p>""",
  grammar=[
    ("<es>cuya desaforada imaginación</es>", """<p><es>cuyo</es> means "whose". Unlike English, it agrees with the thing <b>owned</b>, not the owner: <es>imaginación</es> is feminine, so <es>cuya</es>,
    even though the owner is a man. Nouns ending in <b>-ción</b> are always feminine. <es>desaforada</es>, "unbridled", stands before the noun for emphasis.</p>"""),
    ("<es>iba siempre más lejos que...</es>", """<p><es>iba</es> is the imperfect of <es>ir</es> (to go): "used to go", "always went". You met its preterite, <es>fue</es>, in sentence 7.
    <es>más lejos que</es>: "farther than". Comparisons are <es>más</es> + adjective or adverb + <es>que</es>.</p>"""),
    ("<es>y aun más allá del milagro y la magia</es>", """<p><es>aun</es>, "even", as in sentence 7. <es>más allá de</es> is "beyond", and <es>de</es> + <es>el</es> fuses into <es>del</es>,
    the partner of <es>al</es>: <es>más allá del milagro</es>.</p>"""),
    ("<es>pensó que era posible servirse de...</es>", """<p><es>pensó</es>: preterite, "he thought" (one particular thought, on one occasion). <es>era posible</es> + infinitive: "it was possible to".
    <es>servirse de</es>: "to make use of".</p>"""),
    ("<es>aquella invención inútil</es>", """<p><es>aquella</es> again, as in <es>aquella tarde remota</es>. <es>inútil</es> is <b>in-</b> (not) + <es>útil</es> (useful).
    The narrator calls the magnets useless even as José Arcadio plans to use them.</p>"""),
    ("<es>para desentrañar el oro de la tierra</es>", """<p><es>para</es> + infinitive, "in order to". <es>desentrañar</es> contains <es>entraña</es>, "entrail": to pull something out of the guts of the earth.
    Compare <es>desenclavarse</es>: the prefix <b>des-</b> undoes or removes.</p>"""),
  ],
  pron=[
    ("Names", """<p><es>José</es>: j as breathy h, stress on the accented é, <rs>ho-SEH</rs>. <es>Arcadio</es>: three syllables, <rs>ar-KA-dyo</rs>. <es>Buendía</es>: <rs>bwen-DEE-a</rs>.</p>"""),
    ("g and j", """<ul><li><es>imaginación</es>: g before i as h, <rs>ee-ma-hee-na-SYON</rs>.</li><li><es>ingenio</es>: <rs>een-HEH-nyo</rs>.</li>
    <li><es>magia</es>: two syllables, <rs>MA-hya</rs>.</li><li><es>milagro</es>: hard g before r, <rs>mee-LA-gro</rs>.</li></ul>"""),
    ("Other points", """<ul><li><es>naturaleza</es>: five even syllables, <rs>na-tu-ra-LEH-sa</rs>.</li><li><es>inútil</es>: stress on ú.</li>
    <li><es>desentrañar</es>: <rs>de-sen-tra-NYAR</rs>.</li><li><es>tierra</es>: rolled rr, <rs>TYEH-rra</rs>.</li><li><es>allá</es>: <rs>a-YA</rs>.</li></ul>"""),
  ],
  exercises=[
    ("What did José Arcadio Buendía think was possible?", "To use the magnets to extract gold from the earth: <es>servirse de aquella invención inútil para desentrañar el oro de la tierra</es>."),
    ("Why <es>cuya</es> and not <es>cuyo</es>, when the owner is a man?", "It agrees with the thing owned, <es>imaginación</es>, which is feminine."),
    ("His imagination went beyond three things. Name them.", "<es>el ingenio de la naturaleza</es> (nature's ingenuity), <es>el milagro</es> (miracle) and <es>la magia</es> (magic)."),
    ("What two words make up <es>del</es>?", "<es>de</es> + <es>el</es>."),
    ("Which verb is the preterite of <es>ir</es>, and which the imperfect?", "Preterite <es>fue</es> (sentence 7); imperfect <es>iba</es> (this sentence)."),
    ("Translate: <es>más lejos que</es>.", "Farther than."),
  ],
  review_html="""<p>Recite sentence 8, Melquíades' sales pitch. Today's sentence is the effect of that pitch on one listener.</p>""",
  memo="""<p><b>Three steps up, then the plan.</b> The aside climbs a ladder: farther than <es>el ingenio de la naturaleza</es>, beyond <es>el milagro</es>, beyond <es>la magia</es>.
  Then comes the plan in three infinitives: <es>servirse</es> (use) → <es>desentrañar</es> (extract) → <es>el oro</es> (gold).</p>
  <p>Learn frame, ladder and plan as three pieces, then join them.</p>""",
),

# ------------------------------------------------------------------ 12
dict(
  title="A warning ignored, and a bad trade",
  kind="lesson", new=[10, 11], review=[8, 9],
  objectives=[
    "Understand sentences 10 and 11.",
    "Use <es>le</es> (to him), the negative <es>no</es>, and the connectors <es>pero</es> (but) and <es>así que</es> (so).",
    "Pronounce r after n, and the stressed endings <b>-ez</b> and <b>-ó</b>.",
  ],
  intro="""<p>Two sentences of plain plot: Melquíades warns him, he does not listen, he trades away the family's animals. The grammar is lighter here, a good moment to pick up speed.</p>""",
  grammar=[
    ("<es>que era un hombre honrado</es>", """<p>An aside between commas, introduced by <es>que</es> ("who"). <es>era</es> describes his character, so imperfect.</p>"""),
    ("<es>le previno</es>", """<p><es>le</es> means "to him" (José Arcadio); it stands before the verb, like <es>lo</es>. <es>previno</es> is the irregular preterite of <es>prevenir</es>, "to warn".
    <es>lo</es> is the direct object (he took <em>him</em>); <es>le</es> is the indirect object (he gave a warning <em>to him</em>).</p>"""),
    ("<es>«Para eso no sirve»</es>", """<p>Word for word: "For that not it-serves". <es>servir para</es> is "to be good for"; <es>eso</es> is "that" in the sense of "that purpose".
    <es>no</es> always goes directly in front of the verb. Putting <es>Para eso</es> first gives it the stress: <em>for that</em>, it is no use. <es>sirve</es> is present tense, because he is speaking.</p>"""),
    ("<es>Pero ... no creía en ...</es>", """<p><es>pero</es> = "but". <es>creer en</es> = "to believe in". <es>no creía</es> is imperfect: it was his standing attitude.
    <es>en aquel tiempo</es>, "at that time", uses <es>aquel</es>, the masculine of <es>aquella</es>.</p>"""),
    ("<es>la honradez de los gitanos</es>", """<p><es>honradez</es> (honesty) is the noun made from <es>honrado</es> (honest), which you met one sentence earlier. Many qualities end in <b>-ez</b> and are feminine.</p>"""),
    ("<es>así que cambió ... por ...</es>", """<p><es>así que</es> = "so", "and so". <es>cambiar A por B</es> = "to exchange A for B": <es>cambió su mulo y una partida de chivos por los dos lingotes imantados</es>.
    <es>una partida de</es> is a batch or lot of something. <es>imantados</es>, "magnetised", comes from <es>imán</es>, the magnet of sentence 5.</p>"""),
  ],
  pron=[
    ("r after n is rolled", """<p><es>honrado</es> and <es>honradez</es>: the h is silent and the r, coming after n, is rolled like an initial r: <rs>on-RRA-do</rs>, <rs>on-rra-DES</rs>.</p>"""),
    ("Stressed endings", """<ul><li><es>honradez</es> ends in z, so the last syllable is stressed.</li><li><es>cambió</es>: two syllables, <rs>kam-BYO</rs>.</li>
    <li><es>creía</es>: three syllables, <rs>kre-EE-a</rs>.</li><li><es>así</es>: <rs>a-SEE</rs>.</li><li><es>previno</es>: <rs>pre-BEE-no</rs>.</li></ul>"""),
    ("<b>ch</b>", """<p><es>chivos</es> <rs>CHEE-bos</rs>: ch as in church, v as b.</p>"""),
    ("Delivery", """<p>The narrator pauses before the quotation. Make <es>Para eso no sirve</es> short and flat, the voice of a man stating a fact.</p>"""),
  ],
  exercises=[
    ("What kind of man was Melquíades?", "<es>un hombre honrado</es>: an honest man."),
    ("What did he warn?", "<es>«Para eso no sirve»</es>: it is no good for that."),
    ("Why did José Arcadio not listen?", "He did not believe in the honesty of gypsies: <es>no creía ... en la honradez de los gitanos</es>."),
    ("What did he give, and what did he get?", "He gave his mule and a lot of goats (<es>su mulo y una partida de chivos</es>) for the two magnetised ingots (<es>los dos lingotes imantados</es>)."),
    ("Where does <es>no</es> go in a Spanish sentence?", "Immediately before the verb (and before any pronoun attached in front of it)."),
    ("Which earlier word is <es>imantados</es> related to?", "<es>imán</es>, magnet (sentence 5)."),
  ],
  review_html="""<p>Recite sentence 9 with its ladder (nature, miracle, magic). Then listen to sentences 8 to 11 in a row to hear the conversation as a scene.</p>""",
  memo="""<p><b>Honest ↔ honesty.</b> The two sentences are hinged on one word family: Melquíades was <es>honrado</es>, but José Arcadio did not believe in <es>la honradez</es> of gypsies.
  Remember the hinge and you have both sentences' middles.</p>
  <p>For the trade, picture a pair of scales: on the left pan a mule and goats, on the right two bars of metal, with <es>por</es> as the pivot.</p>""",
),

# ------------------------------------------------------------------ 13
dict(
  title="Úrsula objects",
  kind="lesson", new=[12, 13], review=[10, 11],
  objectives=[
    "Understand sentences 12 and 13.",
    "Recognise <es>contar con</es>, <es>conseguir</es> + infinitive, and the present-tense <es>ha de</es> + infinitive.",
    "Cope with <es>su</es> meaning \"his\" in one sentence and \"her\" in the next.",
  ],
  intro="""<p>Úrsula is the practical one: those goats were the household's savings. Her husband answers with the paragraph's second line of speech.</p>""",
  grammar=[
    ("<es>Úrsula Iguarán, su mujer</es>", """<p><es>mujer</es> means both "woman" and "wife". <es>su mujer</es>, between commas, tells us who Úrsula is: "his wife".</p>"""),
    ("<es>que contaba con aquellos animales</es>", """<p><es>contar con</es> = "to count on". Imperfect, because she had been relying on them all along. <es>aquellos</es> is the masculine plural of <es>aquel</es>.</p>"""),
    ("<es>para ensanchar el desmedrado patrimonio doméstico</es>", """<p><es>ensanchar</es> comes from <es>ancho</es>, "wide": to widen, to enlarge. The noun <es>patrimonio</es> is wrapped in two adjectives,
    one in front for the narrator's judgement (<es>desmedrado</es>, "meagre") and one behind for the plain category (<es>doméstico</es>, "household").</p>"""),
    ("<es>no consiguió disuadirlo</es>", """<p><es>conseguir</es> + infinitive = "to manage to". <es>consiguió</es> is its preterite. <es>disuadirlo</es> = <es>disuadir</es> + <es>lo</es> (him), attached to the infinitive
    as in <es>mencionarlas</es>.</p>"""),
    ("<es>«Muy pronto ha de sobrarnos oro...»</es>", """<p><es>ha de</es> + infinitive is the present-tense twin of <es>había de</es> in sentence 1: "is bound to". <es>sobrar</es> means "to be more than enough".
    <es>nos</es>, "to us", is attached to it. The subject, <es>oro</es>, comes after the verb. Literally: "Very soon gold is bound to be left over to us" – we shall have gold to spare.</p>"""),
    ("<es>para empedrar la casa</es>", """<p><es>empedrar</es> is <b>em-</b> + <es>piedra</es> (stone, from sentence 2): to pave with stones. He plans to pave the house with gold.</p>"""),
    ("<es>replicó su marido</es>", """<p>Verb first, then subject, as in <es>pregonaba el gitano</es>. Here <es>su</es> means "her": <es>su marido</es>, "her husband". <es>su</es> can be his, her, its or their; the context decides.</p>"""),
  ],
  pron=[
    ("Names", """<p><es>Úrsula</es>: stress on the first syllable, <rs>OOR-su-la</rs>. <es>Iguarán</es>: gu + a is "gw", <rs>ee-gwa-RAN</rs>.</p>"""),
    ("gu before i", """<p>In <es>consiguió</es> the u after g is silent; it is only there to keep the g hard: <rs>kon-see-GYO</rs>. Compare <es>Iguarán</es>, where gu before a is pronounced "gw".</p>"""),
    ("Other points", """<ul><li><es>mujer</es>: j as h, stress on the last syllable, <rs>mu-HER</rs>.</li><li><es>muy</es>: one syllable, <rs>mwee</rs>.</li>
    <li><es>disuadirlo</es>: <rs>dee-swa-DEER-lo</rs>.</li><li><es>ensanchar</es>: <rs>en-san-CHAR</rs>.</li><li><es>doméstico</es>: stress on mé.</li>
    <li><es>replicó</es>: stress on the final ó; rolled initial r.</li></ul>"""),
  ],
  exercises=[
    ("Who is Úrsula Iguarán?", "José Arcadio Buendía's wife: <es>su mujer</es>."),
    ("What was she counting on the animals for?", "To enlarge the meagre household estate: <es>para ensanchar el desmedrado patrimonio doméstico</es>."),
    ("Did she succeed in changing his mind?", "No: <es>no consiguió disuadirlo</es>."),
    ("What does he promise?", "That very soon they will have more than enough gold to pave the house."),
    ("Which phrase here echoes <es>había de recordar</es> from sentence 1?", "<es>ha de sobrarnos</es>: the same construction, <es>haber de</es> + infinitive, in the present tense."),
    ("In <es>replicó su marido</es>, whose husband?", "Hers, Úrsula's. <es>su</es> = her here."),
  ],
  review_html="""<p>Recite sentences 10 and 11. Then say what Melquíades warned and what José Arcadio traded, in Spanish.</p>""",
  memo="""<p><b>Objection and reply.</b> Sentence 12 is her case, sentence 13 his answer. For sentence 12 keep the frame, <es>Úrsula Iguarán ... no consiguió disuadirlo</es>, and hang the reason inside it.</p>
  <p>Sentence 13 is worth learning as a quotation you could use yourself. Say it with a confident smile: <es>Muy pronto ha de sobrarnos oro para empedrar la casa</es>.</p>""",
),

# ------------------------------------------------------------------ 14
dict(
  title="Checkpoint 3: the bargain scene, and a run from the top",
  kind="review", new=[], review=[9, 10, 11, 12, 13],
  objectives=[
    "Read sentences 9 to 13 aloud as one scene.",
    "Sort out the object pronouns of the paragraph: <es>lo, le, las, les, nos, se</es>.",
    "Read sentences 1 to 13 aloud without stopping, and recite 9 to 13 from memory.",
  ],
  intro="""<p>You have now met three quarters of the paragraph and nearly all of its grammar. Today is for consolidation: one tidy table of pronouns, then long stretches of reading and reciting.</p>""",
  grammar=[
    ("The pronouns in one place", """<table class="mini"><tr><th>Pronoun</th><th>Meaning</th><th>Where you met it</th></tr>
    <tr><td><es>lo</es></td><td>him (direct object)</td><td><es>lo llevó</es>, <es>disuadirlo</es></td></tr>
    <tr><td><es>le</es></td><td>to him (indirect object)</td><td><es>le previno</es></td></tr>
    <tr><td><es>las</es></td><td>them, feminine</td><td><es>mencionarlas</es>, <es>señalarlas</es></td></tr>
    <tr><td><es>les</es></td><td>to them, for them</td><td><es>se les había buscado</es>, <es>despertarles</es></td></tr>
    <tr><td><es>nos</es></td><td>to us</td><td><es>sobrarnos</es></td></tr>
    <tr><td><es>se</es></td><td>himself, itself, themselves</td><td><es>se precipitaban</es>, <es>se presentó</es>, <es>se espantó</es>, <es>se caían</es>, <es>desenclavarse</es>, <es>se arrastraban</es>, <es>servirse</es></td></tr></table>
    <p>The rule of position: <b>before</b> a conjugated verb, <b>attached to the end</b> of an infinitive.</p>"""),
    ("<es>haber</es> in four disguises", """<p><es>había de recordar</es> (was to) · <es>había que señalarlas</es> (it was necessary to) · <es>se les había buscado</es> (had searched) · <es>ha de sobrarnos</es> (is bound to).
    One verb, <es>haber</es>, carries all four.</p>"""),
    ("Adjective in front, adjective behind", """<p><es>truculenta demostración pública</es> · <es>desaforada imaginación</es> · <es>áspero acento</es> · <es>desmedrado patrimonio doméstico</es>.
    The word in front is the storyteller's colouring; the word behind is the plain fact.</p>"""),
  ],
  pron=[
    ("Speed and evenness", """<p>Play sentence 9 and count how long the narrator takes. Read it yourself against a clock. You are not trying to be faster; you are trying to be as <em>even</em>, with no pile-ups at hard words.
    Any word that trips you, look it up in the vocabulary reference, say its syllables five times, and reinsert it.</p>"""),
    ("The h-sound family", """<p>Say these in a row, all with the same breathy sound: <es>José</es>, <es>gitano</es>, <es>imaginación</es>, <es>ingenio</es>, <es>magia</es>, <es>mujer</es>, <es>objetos</es>, <es>crujían</es>, <es>mágicos</es>.
    And these with silent h: <es>había</es>, <es>hielo</es>, <es>huevos</es>, <es>hizo</es>, <es>hacía</es>, <es>hombre</es>, <es>honrado</es>.</p>"""),
  ],
  exercises=[
    ("Put the five events of this scene in order, in English.", "He has the idea of mining gold with magnets; Melquíades warns him; he trades his animals for the ingots; Úrsula fails to dissuade him; he promises gold enough to pave the house."),
    ("<es>lo</es> or <es>le</es>? \"His father took him\"; \"Melquíades warned him\".", "<es>su padre lo llevó</es>; <es>Melquíades le previno</es>."),
    ("Give the opposites in the text: honest man / (dis)belief in...", "<es>un hombre honrado</es> / <es>no creía en la honradez de los gitanos</es>."),
    ("Translate: <es>más allá del milagro y la magia</es>.", "Beyond miracle and magic."),
    ("Translate: <es>para eso no sirve</es>.", "It is no good for that."),
    ("What are the first two words of sentences 9 to 13?", "<es>José Arcadio</es> · <es>Melquíades, que</es> · <es>Pero José</es> · <es>Úrsula Iguarán</es> · <es>Muy pronto</es>."),
    ("From the top: recite sentence 1 without looking.", "<es>Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de recordar aquella tarde remota en que su padre lo llevó a conocer el hielo.</es>"),
  ],
  review_html="""<p>First, sentences 9 to 13: play, shadow at 0.75×, read alone. Then read sentences 1 to 13 from the top without stopping, text visible. Note which sentence feels weakest and give it five minutes of its own.</p>""",
  memo="""<p><b>Who speaks next?</b> The scene is a three-way exchange. Fix the order of the people and each sentence follows:
  <es>José Arcadio Buendía</es> (idea) → <es>Melquíades</es> (warning) → <es>Pero José Arcadio Buendía</es> (trade) → <es>Úrsula Iguarán</es> (objection) → <es>su marido</es> (reply).</p>
  <p>Recite sentences 9 to 13 in the practice box, then try sentences 1 to 13 at level 2.</p>""",
),

# ------------------------------------------------------------------ 15
dict(
  title="Months of searching",
  kind="lesson", new=[14, 15], review=[12, 13],
  objectives=[
    "Understand sentences 14 and 15.",
    "Use <es>empeñarse en</es>, the pattern <es>palmo a palmo</es>, and <es>en voz alta</es>.",
    "Pronounce x, and link a final consonant to a following vowel.",
  ],
  intro="""<p>The man sets to work. These two sentences are full of energy: a stubborn verb, then a string of actions with no subject stated at all, because Spanish does not need one.</p>""",
  grammar=[
    ("<es>Durante varios meses</es>", """<p><es>durante</es> = "during", "for" a stretch of time. <es>meses</es> is the plural of <es>mes</es> (month), which you met in <es>el mes de marzo</es>.</p>"""),
    ("<es>se empeñó en demostrar</es>", """<p><es>empeñarse en</es> + infinitive: to set one's mind stubbornly on doing something. The preterite sums up the whole period as one completed effort.</p>"""),
    ("<es>el acierto de sus conjeturas</es>", """<p><es>acierto</es> is "rightness", being on target. <es>sus</es> is the plural of <es>su</es>, used because <es>conjeturas</es> is plural. The possessive agrees with the thing owned, not with the owner.</p>"""),
    ("<es>Exploró palmo a palmo la región</es>", """<p><es>exploró</es>: preterite, "he explored". No word for "he" is needed. A <es>palmo</es> is a handspan; <es>palmo a palmo</es> is "inch by inch".
    The same pattern gives <es>poco a poco</es> (little by little) and <es>paso a paso</es> (step by step).</p>"""),
    ("<es>inclusive el fondo del río</es>", """<p><es>inclusive</es> = "even", "including". <es>del</es> = <es>de</es> + <es>el</es>. <es>el fondo del río</es>, "the bottom of the river": the same river of clear water as in sentence 2.</p>"""),
    ("Two gerunds: <es>arrastrando</es>, <es>recitando</es>", """<p>He explored <em>dragging</em> and <em>reciting</em>. You know <es>arrastrando</es> from sentence 7, where Melquíades did the dragging. Now José Arcadio copies him.</p>"""),
    ("<es>en voz alta</es>", """<p>Literally "in high voice": aloud. <es>el conjuro de Melquíades</es>, "Melquíades' spell", is his own phrase from sentence 8, recited now as a magic formula.</p>"""),
    ("Four names for two iron bars", """<p><es>lingotes metálicos</es> (7) → <es>fierros mágicos</es> (7) → <es>lingotes imantados</es> (11) → <es>lingotes de hierro</es> (15). Metal, magic, magnetised, iron: the wording cools as the hope fades.</p>"""),
  ],
  pron=[
    ("<b>x</b>", """<p>Before a consonant, x is "ks" (often just "s" in relaxed speech): <es>exploró</es> <rs>eks-plo-RO</rs>.</p>"""),
    ("Consonant to vowel linking", """<p>A final consonant jumps onto a following vowel: <es>voz alta</es> sounds like <rs>bo-SAL-ta</rs>, <es>el acierto</es> like <rs>e-la-SYER-to</rs>.</p>"""),
    ("Other points", """<ul><li><es>empeñó</es>: <rs>em-pe-NYO</rs>.</li><li><es>conjeturas</es>, <es>conjuro</es>: j as h, <rs>kon-he-TU-ras</rs>, <rs>kon-HU-ro</rs>.</li>
    <li><es>región</es>: rolled r, g as h, <rs>rre-HYON</rs>.</li><li><es>hierro</es>: silent h, rolled rr, <rs>YEH-rro</rs>.</li><li><es>río</es>: two syllables.</li></ul>"""),
  ],
  exercises=[
    ("How long did he keep trying?", "<es>Durante varios meses</es>: for several months."),
    ("What was he trying to prove?", "<es>el acierto de sus conjeturas</es>: that his conjectures were right."),
    ("Where did he search?", "The whole region inch by inch, even the bottom of the river: <es>palmo a palmo la región, inclusive el fondo del río</es>."),
    ("What was he doing while he explored?", "Dragging the two iron ingots and reciting Melquíades' incantation aloud."),
    ("Why <es>sus</es> and not <es>su</es>?", "Because <es>conjeturas</es> is plural."),
    ("Say \"aloud\" in Spanish.", "<es>en voz alta</es>."),
  ],
  review_html="""<p>Recite sentences 12 and 13. Úrsula has lost the argument; today you see what her husband does with the magnets.</p>""",
  memo="""<p><b>Verb, place, two actions.</b> Sentence 15 has a clean shape: <es>Exploró</es> + where (<es>la región</es>, <es>el fondo del río</es>) + how (<es>arrastrando...</es>, <es>recitando...</es>).
  Walk slowly across the room as you say it, miming the dragging.</p>
  <p>Sentence 14 is three short beats: time (<es>Durante varios meses</es>), effort (<es>se empeñó en demostrar</es>), aim (<es>el acierto de sus conjeturas</es>).</p>""",
),

# ------------------------------------------------------------------ 16
dict(
  title="The armour",
  kind="lesson", new=[16], review=[14, 15],
  objectives=[
    "Understand sentence 16.",
    "Use <es>lo único que</es> (the only thing that) and <es>lograr</es> + infinitive, and recognise <es>fue</es> as \"was\".",
    "Read a Roman-numeral century aloud.",
  ],
  intro="""<p>All that effort, and what comes out of the ground is not gold but a rusted suit of armour. The sentence is built to disappoint: <es>Lo único...</es>, "the only thing...".</p>""",
  grammar=[
    ("<es>Lo único que logró desenterrar</es>", """<p><es>lo</es> + adjective makes an abstract "the ... thing": <es>lo único</es>, "the only thing". <es>lograr</es> + infinitive is "to manage to", "to succeed in";
    there is no preposition between the two verbs. <es>desenterrar</es> = <b>des-</b> + <b>en-</b> + <es>tierra</es>: to un-earth. That is the third <b>des-</b> verb of digging and pulling out.</p>"""),
    ("<es>fue</es>: \"was\"", """<p>In sentence 7 <es>fue</es> meant "went". Here it means "was". The verbs <es>ir</es> (to go) and <es>ser</es> (to be) share their whole preterite. Context always tells them apart:
    <es>fue de casa en casa</es> (went), <es>fue una armadura</es> (was).</p>"""),
    ("<es>del siglo XV</es>", """<p>Centuries are written in Roman numerals and read as ordinary numbers: <es>siglo quince</es>, "century fifteen". With <es>de</es> + <es>el</es>: <es>del siglo XV</es>.</p>"""),
    ("<es>con todas sus partes soldadas por un cascote de óxido</es>", """<p><es>todas sus partes</es>, "all its parts": <es>todas</es> and <es>soldadas</es> are feminine plural to match <es>partes</es>.
    <es>por</es> here is the "by" that follows a participle: welded <em>by</em> a crust of rust.</p>"""),
    ("<es>cuyo interior tenía...</es>", """<p><es>cuyo</es>, "whose", is masculine this time because <es>interior</es> is masculine (compare <es>cuya imaginación</es>). <es>tenía</es> is the imperfect of <es>tener</es>, "had".</p>"""),
    ("<es>la resonancia hueca de un enorme calabazo lleno de piedras</es>", """<p>"The hollow resonance of an enormous gourd full of stones." <es>lleno de</es> = "full of". And there are <es>piedras</es> again, as in the riverbed of sentence 2, with <es>enorme</es> beside them once more.</p>"""),
  ],
  pron=[
    ("Stress on the third-from-last syllable", """<p>Three words here carry an accent on the third syllable from the end: <es>único</es> <rs>OO-nee-ko</rs>, <es>óxido</es> <rs>OK-see-do</rs>, and earlier <es>mágicos</es>, <es>metálicos</es>.
    Such words always have a written accent, so you can never miss them.</p>"""),
    ("<b>x</b> between vowels", """<p>In <es>óxido</es> x is a clear "ks".</p>"""),
    ("Other points", """<ul><li><es>siglo XV</es>: say <rs>SEE-glo KEEN-se</rs>.</li><li><es>hueca</es>: <rs>WEH-ka</rs>.</li><li><es>cuyo</es>: <rs>KOO-yo</rs>.</li>
    <li><es>calabazo</es>: <rs>ka-la-BA-so</rs>.</li><li><es>lleno</es>: <rs>YEH-no</rs>.</li><li><es>resonancia</es>: rolled initial r, <rs>rre-so-NAN-sya</rs>.</li></ul>"""),
  ],
  exercises=[
    ("What was the only thing he dug up?", "A suit of armour from the fifteenth century: <es>una armadura del siglo XV</es>."),
    ("What held its parts together?", "A crust of rust: <es>un cascote de óxido</es>."),
    ("What did the inside sound like?", "Like an enormous gourd full of stones: <es>un enorme calabazo lleno de piedras</es>."),
    ("<es>fue</es> appears in sentences 7 and 16. What does it mean in each?", "\"Went\" in 7 (from <es>ir</es>); \"was\" in 16 (from <es>ser</es>)."),
    ("How do you read <es>siglo XV</es> aloud?", "<es>siglo quince</es>."),
    ("Why <es>cuyo</es> here but <es>cuya</es> in sentence 9?", "It agrees with what is owned: <es>interior</es> is masculine, <es>imaginación</es> feminine."),
  ],
  review_html="""<p>Recite sentences 14 and 15, the months of dragging and chanting, and go straight into today's <es>Lo único que...</es>.</p>""",
  memo="""<p><b>Outside, then inside.</b> The sentence moves from the outside of the armour to the inside: found it (<es>Lo único que logró desenterrar fue una armadura del siglo XV</es>) →
  its surface (<es>con todas sus partes soldadas por un cascote de óxido</es>) → its inside (<es>cuyo interior tenía la resonancia hueca...</es>) → the sound (<es>de un enorme calabazo lleno de piedras</es>).</p>
  <p>Knock on a table at <es>resonancia hueca</es>. A sound is a good anchor for a sound.</p>""",
),

# ------------------------------------------------------------------ 17
dict(
  title="What was inside",
  kind="lesson", new=[17], review=[15, 16],
  objectives=[
    "Understand sentence 17, the last of the paragraph.",
    "Recognise the preterite \"they\" ending <b>-aron</b> and <es>llevar</es> in the sense of \"to wear\".",
    "Read the final sentence with a falling, closing rhythm.",
  ],
  intro="""<p>The paragraph ends on a small, tender detail: inside the armour a skeleton, and at its neck a locket with a curl of a woman's hair.
  After all the noise of the magnets, the last words are quiet.</p>""",
  grammar=[
    ("<es>Cuando ... lograron desarticular la armadura</es>", """<p><es>cuando</es> = "when". The subject is plural, José Arcadio Buendía <em>and</em> the four men, so the verb takes the plural preterite ending <b>-aron</b>: <es>lograron</es>, "they managed".
    Compare <es>logró</es> in sentence 16, when he was alone. <es>desarticular</es> = <b>des-</b> + <es>articular</es>: to take apart at the joints.</p>"""),
    ("<es>los cuatro hombres de su expedición</es>", """<p><es>hombres</es> is the plural of <es>hombre</es> (sentence 10). His gold hunt has become an "expedition" with a team of four.</p>"""),
    ("<es>encontraron dentro un esqueleto calcificado</es>", """<p><es>encontraron</es>: "they found", the same <b>-aron</b> ending. <es>dentro</es> = "inside". <es>calcificado</es> is one more participle used as an adjective.</p>"""),
    ("<es>que llevaba colgado en el cuello</es>", """<p><es>llevar</es> returns for the third time: "took" (1), "brought" (5), and now "wore". <es>llevaba</es> is imperfect, a state.
    <es>llevar</es> + participle describes what someone has on them: <es>llevaba colgado ... un relicario</es>, "had a locket hanging".
    <es>colgado</es> agrees with <es>relicario</es>. And <es>en el cuello</es>, "at the neck": the article for a body part, as in <es>con el dedo</es>.</p>"""),
    ("<es>un relicario de cobre con un rizo de mujer</es>", """<p>Two more <es>de</es> phrases: <es>de cobre</es>, made of copper; <es>un rizo de mujer</es>, a woman's curl. With no article, <es>de mujer</es> names the kind of curl rather than a particular woman.
    This <es>mujer</es> means "woman"; in sentence 12 it meant "wife".</p>"""),
  ],
  pron=[
    ("<b>cu</b> + vowel is \"kw\"", """<p><es>cuando</es> <rs>KWAN-do</rs>, <es>cuatro</es> <rs>KWA-tro</rs>, <es>cuello</es> <rs>KWEH-yo</rs>. Each <b>cu</b> + vowel is a single syllable.</p>"""),
    ("Other points", """<ul><li><es>expedición</es>: <rs>eks-pe-dee-SYON</rs>.</li><li><es>esqueleto</es>: qu as k, <rs>es-ke-LEH-to</rs>.</li>
    <li><es>calcificado</es>: five even syllables.</li><li><es>llevaba</es>: <rs>yeh-BA-ba</rs>.</li>
    <li><es>relicario</es>, <es>rizo</es>: rolled initial r; <rs>rre-lee-KA-ryo</rs>, <rs>RREE-so</rs>.</li><li><es>mujer</es>: <rs>mu-HER</rs>.</li></ul>"""),
    ("Landing the ending", """<p>Let your pitch step down through the last three phrases, <es>en el cuello</es> / <es>un relicario de cobre</es> / <es>con un rizo de mujer</es>, and slow slightly on the final two words.
    Listen to how the narrator closes the paragraph and copy the fall.</p>"""),
  ],
  exercises=[
    ("Who took the armour apart?", "José Arcadio Buendía and the four men of his expedition."),
    ("What did they find inside?", "<es>un esqueleto calcificado</es>: a calcified skeleton."),
    ("What was it wearing, and where?", "A copper locket hanging at its neck: <es>llevaba colgado en el cuello un relicario de cobre</es>."),
    ("What was in the locket?", "<es>un rizo de mujer</es>: a curl of a woman's hair."),
    ("Why <es>lograron</es> here and <es>logró</es> in sentence 16?", "The subject is now plural (he and four men): the ending -aron is \"they\", -ó is \"he\"."),
    ("Give the three meanings of <es>llevar</es> in this paragraph.", "To take (<es>lo llevó</es>), to bring (<es>llevaron el imán</es>), to wear (<es>llevaba colgado</es>)."),
  ],
  review_html="""<p>Recite sentences 15 and 16 first. Then listen to sentences 14 to 17 as one scene: search, armour, skeleton.</p>""",
  memo="""<p><b>A zoom to one curl.</b> Like sentence 2, this one zooms in: the men → the armour → a skeleton → its neck → a locket → a curl. Each step is smaller than the last.</p>
  <p>Learn the final three phrases first, as in Lesson 1, and work backwards: the ending is what an audience remembers, so it should be the part you know best.</p>""",
),

# ------------------------------------------------------------------ 18
dict(
  title="Checkpoint 4: the whole paragraph aloud",
  kind="review", new=[], review=[14, 15, 16, 17],
  objectives=[
    "Read sentences 14 to 17 fluently, then the whole paragraph from start to finish.",
    "Hold the paragraph in your head as five scenes.",
    "Shadow the full recording at 0.75× and then at normal speed.",
  ],
  intro="""<p>Every sentence is now familiar. From here on the work changes: no new language, only fluency and memory. Today's goal is one complete, unbroken reading aloud.</p>""",
  grammar=[
    ("The paragraph in five scenes", """<ol><li><b>The memory</b> (sentence 1): firing squad, father, ice.</li>
    <li><b>The village</b> (2 and 3): Macondo, the river, a world without names.</li>
    <li><b>The gypsies</b> (4 to 8): the yearly visit, the magnet, Melquíades, the demonstration, his pitch.</li>
    <li><b>The bargain</b> (9 to 13): the idea, the warning, the trade, Úrsula, the promise of gold.</li>
    <li><b>The search</b> (14 to 17): months of digging, the armour, the skeleton, the curl.</li></ol>"""),
    ("The verbs tell the story", """<p>Read just the preterites in order and you have the plot: <es>llevó</es> · <es>llevaron</es> · <es>se presentó</es> · <es>hizo</es> · <es>fue</es> · <es>se espantó</es> · <es>pensó</es> · <es>previno</es> ·
    <es>cambió</es> · <es>consiguió</es> · <es>replicó</es> · <es>se empeñó</es> · <es>exploró</es> · <es>logró</es> · <es>fue</es> · <es>lograron</es> · <es>encontraron</es>. Everything else is description hung on those seventeen pegs.</p>"""),
    ("Words that come back", """<p><es>llevar</es> (1, 5, 17) · <es>conocer</es> (1, 4) · <es>piedras</es> and <es>enorme</es> (2, 16) · <es>río</es> (2, 15) · <es>arrastrando</es> (7, 15) · <es>aquella</es> (1, 9) · <es>haber de</es> (1, 13) ·
    <es>mujer</es> (12, 17) · <es>hombre</es> (10, 17). Noticing the echoes ties distant sentences together in memory.</p>"""),
  ],
  pron=[
    ("Shadow, then solo", """<p>1. Play the whole paragraph at 0.75× and shadow it without stopping. 2. Do it again at normal speed; fall behind if you must, but keep going. 3. Read it alone.
    The narrator takes about four minutes. A comfortable first target for you is under six.</p>"""),
    ("Mark your breaths", """<p>Breathe at full stops and at the commas where the narrator pauses. If you run out of air in sentence 7, go back to the five-breath plan in Lesson 9.</p>"""),
    ("Record yourself", """<p>Use your phone's voice recorder for one full reading, then listen while following the text. Note three words that sound least like the narrator and drill only those.</p>"""),
  ],
  exercises=[
    ("Name the five scenes in order.", "The memory; the village; the gypsies; the bargain; the search."),
    ("Which sentence begins each scene? Give the first words.", "<es>Muchos años después</es> (1) · <es>Macondo era entonces</es> (2) · <es>Todos los años</es> (4) · <es>José Arcadio Buendía, cuya</es> (9) · <es>Durante varios meses</es> (14)."),
    ("Translate: <es>se empeñó en demostrar el acierto de sus conjeturas</es>.", "He strove stubbornly to prove that his conjectures were right."),
    ("Translate: <es>lo único que logró desenterrar</es>.", "The only thing he managed to dig up."),
    ("Complete: <es>un relicario de cobre con...</es>", "<es>...un rizo de mujer</es>."),
    ("Which three verbs of pulling things out begin with <b>des-</b>?", "<es>desenclavarse</es> (7), <es>desentrañar</es> (9), <es>desenterrar</es> (16); and <es>desarticular</es> (17) makes a fourth, to take apart."),
  ],
  review_html="""<p>Sentences 14 to 17 first: play, shadow, read alone, tick. Then the full read-through described above. Tick the box only after one complete reading with no restart.</p>""",
  memo="""<p><b>Scene by scene.</b> Recite each scene on its own in the practice box, at whatever level is just hard enough. Scenes 1 and 2 should already be at the top level;
  give most of your time to scenes 3 and 5.</p>""",
),

# ------------------------------------------------------------------ 19
dict(
  title="Memorising the whole paragraph",
  kind="review", new=[], review=list(range(1, 18)),
  objectives=[
    "Recite each of the five scenes from memory.",
    "Join the scenes with a chain of seventeen cue words.",
    "Recite the complete paragraph with first-letter prompts only.",
  ],
  intro="""<p>Memory for a long text is built from three things: a map (the scenes), handles (the first words of each sentence), and repeated retrieval with less and less help.
  Reading the text again and again does little. <em>Trying to say it</em> and checking afterwards is what works.</p>""",
  grammar=[
    ("The seventeen handles", """<ol class="cues"><li><es>Muchos años después</es></li><li><es>Macondo era</es></li><li><es>El mundo era</es></li><li><es>Todos los años</es></li><li><es>Primero llevaron</es></li>
    <li><es>Un gitano corpulento</es></li><li><es>Fue de casa en casa</es></li><li><es>«Las cosas tienen</es></li><li><es>José Arcadio Buendía, cuya</es></li><li><es>Melquíades, que era</es></li>
    <li><es>Pero José Arcadio Buendía</es></li><li><es>Úrsula Iguarán</es></li><li><es>«Muy pronto</es></li><li><es>Durante varios meses</es></li><li><es>Exploró palmo a palmo</es></li>
    <li><es>Lo único que</es></li><li><es>Cuando José Arcadio Buendía</es></li></ol>
    <p>Learn this list by itself until you can say it in under thirty seconds. If you know what comes next, you will rarely get stuck.</p>"""),
    ("Understanding while reciting", """<p>The goal is to recite <em>with</em> the meaning, not as a string of sounds. For each sentence, glance at the English first and then say the Spanish.
    If a phrase comes out without your knowing what it means, stop and look it up. A phrase you understand is far harder to forget.</p>"""),
    ("Known trouble spots", """<ul><li>Sentence 2: the order <es>pulidas, blancas y enormes</es>.</li><li>Sentence 4: <es>plantaba</es> (singular) then <es>daban</es> (plural).</li>
    <li>Sentence 7: the kitchen list, and <es>por donde más se les había buscado</es>.</li><li>Sentence 9: <es>el ingenio de la naturaleza</es>, then <es>el milagro y la magia</es>.</li>
    <li>Sentence 12: <es>el desmedrado patrimonio doméstico</es>.</li><li>Sentences 7, 11 and 15: which name for the ingots goes where (<es>metálicos</es>, <es>fierros mágicos</es>, <es>imantados</es>, <es>de hierro</es>).</li></ul>"""),
  ],
  pron=[
    ("Recite aloud, always", """<p>Silent rehearsal feels the same but trains less. Say it out loud, at speaking volume, standing if you can.</p>"""),
    ("Keep the rhythm when memory fails", """<p>If a word will not come, hum its syllables in rhythm and carry on, then check afterwards. Stopping dead teaches you to stop at that spot.</p>"""),
  ],
  exercises=[
    ("Say the seventeen handles in order.", "See the list above; check yourself against it."),
    ("English to Spanish: \"The world was so recent that many things lacked names.\"", "<es>El mundo era tan reciente, que muchas cosas carecían de nombre.</es>"),
    ("English to Spanish: \"First they brought the magnet.\"", "<es>Primero llevaron el imán.</es>"),
    ("English to Spanish: \"It is no good for that.\"", "<es>Para eso no sirve.</es>"),
    ("English to Spanish: \"Things have a life of their own.\"", "<es>Las cosas tienen vida propia.</es>"),
    ("What comes after <es>y todo el mundo se espantó al ver que...</es>?", "<es>...los calderos, las pailas, las tenazas y los anafes se caían de su sitio</es>."),
    ("What comes after <es>encontraron dentro...</es>?", "<es>...un esqueleto calcificado que llevaba colgado en el cuello un relicario de cobre con un rizo de mujer</es>."),
  ],
  review_html="""<p>Warm up with one full read-aloud, text visible, shadowing the recording at normal speed.</p>""",
  memo="""<p><b>Today's ladder.</b></p>
  <ol><li>Each scene alone at level 4 (first letters only): scenes 1, 2, 3, 4, 5.</li>
  <li>Scenes joined in pairs: 1+2, 3, 4+5, still with first letters.</li>
  <li>The whole paragraph with first letters.</li>
  <li>The whole paragraph at level 5 (everything hidden), peeking only when stuck. Count your peeks.</li></ol>
  <p><b>Then space it out.</b> Recite once more tonight, once tomorrow morning, and once the day after before starting Lesson 20. Three short recalls spread over two days beat an hour in one sitting.</p>""",
),

# ------------------------------------------------------------------ 20
dict(
  title="Final assessment",
  kind="final", new=[], review=list(range(1, 18)),
  objectives=[
    "Show that you understand every sentence.",
    "Read the whole paragraph aloud with steady rhythm and clear pronunciation.",
    "Recite the whole paragraph from memory, knowing what you are saying.",
  ],
  intro="""<p>Three tests, one for each goal of the course. Do them in order, in one sitting if you can. Be honest with the checklists: they are saved on this device, and you can come back and improve any part.</p>""",
  grammar=[
    ("Part A: Understanding", """<p>Answer the twenty questions under <b>Check yourself</b> aloud or on paper before opening each answer. Sixteen or more correct is a pass.
    For any you miss, reread the lesson named in the answer.</p>"""),
    ("Part B: Reading aloud", """<p>Record yourself reading the whole paragraph once, with no restarts. Then listen to your recording against the narrator and tick what is true:</p>
    <ul class="checks">
    <li data-check="b1">I read to the end without restarting.</li>
    <li data-check="b2">My vowels stayed pure: no English "uh" in <es>de</es>, <es>que</es>, <es>el</es>.</li>
    <li data-check="b3">Silent h and the breathy j / g were right (<es>había</es>, <es>hielo</es>; <es>José</es>, <es>gitano</es>, <es>mujer</es>).</li>
    <li data-check="b4">Stress fell on the right syllable in accented words (<es>pelotón</es>, <es>Melquíades</es>, <es>único</es>, <es>óxido</es>).</li>
    <li data-check="b5">I paused at punctuation and linked the words inside each breath group.</li>
    <li data-check="b6">My reading took less than six minutes.</li></ul>
    <p>Five ticks out of six is a pass.</p>"""),
    ("Part C: Reciting from memory", """<p>Open the practice box below at level 5, with everything hidden, and recite the whole paragraph aloud. Reveal a word only when you are truly stuck, and count the reveals.</p>
    <ul class="checks">
    <li data-check="c1">I recited all seventeen sentences in order.</li>
    <li data-check="c2">I needed ten reveals or fewer.</li>
    <li data-check="c3">I needed three reveals or fewer.</li>
    <li data-check="c4">For any sentence chosen at random, I can say in English what it means.</li></ul>
    <p>The first, second and fourth ticks are a pass. The third is mastery.</p>"""),
    ("Where to go next", """<p>Keep the paragraph alive by reciting it once a week. Then go on to <a href="lesson-21.html">Part 2</a>: lessons 21 to 40 do the same for the second paragraph,
    which continues the story with the telescope and the magnifying glass. You already know most of its small words, and the recording carries straight on into it.</p>"""),
  ],
  pron=[],
  exercises=[
    ("1. Who is facing the firing squad, and what does he remember?", "Colonel Aureliano Buendía; the distant afternoon when his father took him to see ice. (Lessons 1 and 2)"),
    ("2. Translate <es>había de recordar</es>.", "Was to remember. (Lesson 2)"),
    ("3. What were Macondo's houses made of?", "Mud and wild cane: <es>de barro y cañabrava</es>. (Lesson 3)"),
    ("4. What are the river stones compared to?", "Prehistoric eggs: <es>huevos prehistóricos</es>. (Lesson 3)"),
    ("5. Why did people point at things?", "The world was so new that many things had no name. (Lesson 4)"),
    ("6. What is the difference between <es>había de</es> and <es>había que</es>?", "<es>había de</es> = was to (destiny); <es>había que</es> = it was necessary to. (Lesson 4)"),
    ("7. When did the gypsies come each year?", "Around March: <es>por el mes de marzo</es>. (Lesson 5)"),
    ("8. What was the first invention they brought?", "The magnet: <es>el imán</es>. (Lesson 5)"),
    ("9. Describe Melquíades.", "A burly gypsy with a wild beard and sparrow hands. (Lesson 7)"),
    ("10. What does <es>truculenta</es> mean?", "Lurid, sensational. (Lesson 7)"),
    ("11. Name two of the kitchen things that fell.", "Any two of <es>calderos, pailas, tenazas, anafes</es>. (Lesson 8)"),
    ("12. Translate <es>todo el mundo se espantó</es>.", "Everybody was terrified. (Lesson 8)"),
    ("13. Where did the lost objects reappear?", "Where they had been looked for most. (Lesson 9)"),
    ("14. What, according to Melquíades, do things have?", "A life of their own: <es>vida propia</es>. (Lesson 10)"),
    ("15. What did José Arcadio want to do with the magnets?", "Extract gold from the earth. (Lesson 11)"),
    ("16. What did he trade for them?", "His mule and a lot of goats. (Lesson 12)"),
    ("17. Translate <es>no consiguió disuadirlo</es>.", "She did not manage to dissuade him. (Lesson 13)"),
    ("18. What does he promise Úrsula?", "Gold to spare, enough to pave the house. (Lesson 13)"),
    ("19. What was the only thing he dug up?", "A fifteenth-century suit of armour, rusted solid. (Lesson 16)"),
    ("20. What was inside, and what hung at its neck?", "A calcified skeleton with a copper locket containing a curl of a woman's hair. (Lesson 17)"),
  ],
  review_html="""<p>Before you begin, play the whole paragraph once and simply listen, eyes closed. You should understand all of it.</p>""",
  memo="""<p>This box is your Part C. Set it to level 5 and begin with <es>Muchos años después...</es></p>""",
),
]
