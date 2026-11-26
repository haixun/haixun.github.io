# Lessons 21-30: paragraph 2, sentences 1 to 19.  Same markup as lessons_a.py.
# para=2 means the sentence numbers in "new" and "review" are local to paragraph 2.

LESSONS_C = [

# ------------------------------------------------------------------ 21
dict(
  para=2, title="The gypsies return",
  kind="lesson", new=[1, 2, 3], review=[],
  objectives=[
    "Understand sentences 1 to 3 of the second paragraph.",
    "Recognise the preterite \"they\" endings <b>-aron</b> and <b>-ieron</b>.",
    "Use <es>esta</es> (this) beside <es>aquella</es> (that), and know why <es>y</es> sometimes becomes <es>e</es>.",
  ],
  intro="""<p>Part 2 picks up exactly where the first paragraph stopped: it is March again, and the gypsies are back with new marvels.
  You already own the sounds of Spanish and the commonest two hundred word forms, so these lessons move faster: two or three sentences at a time.</p>
  <p>Before you start, play the whole of paragraph 2 once on the <a href="paragraph-2.html">text page</a> and notice how much you already catch.</p>""",
  grammar=[
    ("<es>volvieron</es>, <es>exhibieron</es>, <es>sentaron</es>, <es>instalaron</es>", """<p>Four completed actions by "they". In paragraph 1 you met <b>-aron</b> (<es>llevaron</es>, <es>lograron</es>), the ending for -ar verbs.
    Verbs in -er and -ir take <b>-ieron</b>: <es>volver</es> → <es>volvieron</es> (they came back), <es>exhibir</es> → <es>exhibieron</es> (they exhibited).</p>
    <table class="mini"><tr><th>Preterite</th><th>-ar verbs</th><th>-er / -ir verbs</th></tr>
    <tr><td>he, she, it</td><td>-ó: <es>llevó</es></td><td>-ió: <es>consiguió</es></td></tr>
    <tr><td>they</td><td>-aron: <es>sentaron</es></td><td>-ieron: <es>volvieron</es></td></tr></table>"""),
    ("<es>llevaban</es>", """<p>Imperfect, among all those preterites: it describes what they <em>had with them</em> when they arrived. It is the fourth form of <es>llevar</es> you have met.</p>"""),
    ("<es>Esta vez</es>", """<p><es>esta</es> is "this", for what is near; <es>aquella</es> was "that", far away. <es>vez</es> is "time" in the sense of an occasion: <es>esta vez</es>, "this time".</p>"""),
    ("<es>una lupa del tamaño de un tambor</es>", """<p><es>del tamaño de</es>: "of the size of". Spanish needs both <es>de</es>'s where English says simply "the size of a drum".</p>"""),
    ("<es>el último descubrimiento</es>", """<p><es>último</es> before a noun means "latest". Compare the sales talk in paragraph 1, <es>la octava maravilla de los sabios alquimistas de Macedonia</es>: the same structure, a new exotic source.</p>"""),
    ("<es>Sentaron una gitana</es>", """<p><es>sentar</es> is to seat somebody; <es>sentarse</es>, with <es>se</es>, is to sit down oneself. You will meet <es>se sentó</es> in the last lines of this paragraph. <es>gitana</es> is the feminine of <es>gitano</es>.</p>"""),
    ("<es>e instalaron</es>", """<p><es>y</es> (and) changes to <es>e</es> before a word that starts with the sound <b>i</b>, to keep the two from running together: <es>e instalaron</es>.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>volvieron</es>: both v's are soft b's, <rs>bol-BYEH-ron</rs>.</li><li><es>catalejo</es>: j as breathy h, <rs>ka-ta-LEH-ho</rs>.</li>
    <li><es>tamaño</es>: <rs>ta-MA-nyo</rs>.</li><li><es>exhibieron</es>: silent h, x as ks, <rs>ek-see-BYEH-ron</rs>.</li>
    <li><es>judíos</es>: <rs>hu-DEE-os</rs>, three syllables.</li><li><es>Ámsterdam</es>: stress on the first syllable.</li>
    <li><es>descubrimiento</es>: five syllables, <rs>des-ku-bree-MYEN-to</rs>.</li></ul>"""),
  ],
  exercises=[
    ("When did the gypsies return?", "In March: <es>En marzo volvieron los gitanos</es>."),
    ("What two things did they bring?", "<es>un catalejo</es> (a telescope) and <es>una lupa del tamaño de un tambor</es> (a magnifying glass the size of a drum)."),
    ("Whose discovery did they say it was?", "<es>de los judíos de Ámsterdam</es>: of the Jews of Amsterdam."),
    ("Where did they put the gypsy woman, and where the telescope?", "Her at one end of the village (<es>en un extremo de la aldea</es>); the telescope at the entrance of the tent (<es>a la entrada de la carpa</es>)."),
    ("Why <es>e</es> and not <es>y</es> before <es>instalaron</es>?", "Because <es>instalaron</es> begins with the sound i."),
    ("Give the \"they\" preterite of <es>volver</es> and of <es>sentar</es>.", "<es>volvieron</es>; <es>sentaron</es>."),
  ],
  review_html="""<p>Recite the last sentence of paragraph 1 (<es>Cuando José Arcadio Buendía y los cuatro hombres...</es>) and go straight into <es>En marzo volvieron los gitanos</es>. The two paragraphs should feel like one story.</p>""",
  memo="""<p><b>Arrive, show, set up.</b> Three sentences, three actions: they came back; they brought and exhibited; they seated and installed.
  Sentence 3 is two matching halves: <es>Sentaron una gitana</es> + where, <es>e instalaron el catalejo</es> + where.</p>""",
),

# ------------------------------------------------------------------ 22
dict(
  para=2, title="The telescope, and a prophecy",
  kind="lesson", new=[4, 5, 6], review=[1, 2, 3],
  objectives=[
    "Understand sentences 4 to 6.",
    "Recognise two new tenses in Melquíades' speech: the present perfect (<es>ha eliminado</es>) and the future (<es>podrá</es>).",
    "Use the \"personal a\" and <es>sin</es> + infinitive.",
  ],
  intro="""<p>For five reales the villagers look through the telescope. Then Melquíades makes a prediction that the twentieth century fulfilled: one day people will see anywhere on earth without leaving home.</p>""",
  grammar=[
    ("<es>la gente se asomaba ... y veía</es>", """<p><es>la gente</es>, "people", is a singular noun in Spanish, so its verbs are singular. Both are imperfect because this went on all day, customer after customer.
    <es>asomarse a</es> is to put your face to something in order to look.</p>"""),
    ("<es>veía a la gitana</es>: the personal <es>a</es>", """<p>When the direct object of a verb is a particular person, Spanish puts <es>a</es> in front of it. It is not translated: <es>veía a la gitana</es>, "saw the gypsy woman".</p>"""),
    ("<es>al alcance de su mano</es>", """<p>"Within reach of their hand." <es>su</es> refers back to <es>la gente</es>.</p>"""),
    ("<es>ha eliminado</es>: the present perfect", """<p><es>ha</es> (has) + a participle in <b>-ado</b> or <b>-ido</b>, exactly like English "has eliminated". You met <es>ha</es> in <es>ha de sobrarnos</es>, and <es>había</es> + participle in <es>se les había buscado</es>.</p>"""),
    ("<es>podrá ver</es>: the future", """<p>The future is formed by adding endings to the infinitive; <b>-á</b> is "he, she, it will". <es>poder</es> (to be able) is slightly irregular: <es>podrá</es>, "will be able to".
    <es>el hombre</es> here means mankind.</p>"""),
    ("<es>lo que ocurre en cualquier lugar de la tierra</es>", """<p><es>lo que</es>, "what", as in <es>lo que él mismo llamaba</es>. <es>cualquier</es> + noun is "any ... at all". <es>la tierra</es> here is the whole earth; in paragraph 1 it was the ground.</p>"""),
    ("<es>sin moverse</es>", """<p>After a preposition Spanish uses the infinitive where English uses "-ing": <es>sin moverse</es>, "without moving".</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>mediante</es>: <rs>me-DYAN-te</rs>.</li><li><es>reales</es>: rolled r, three syllables, <rs>rre-A-les</rs>.</li>
    <li><es>gente</es>: g before e as breathy h, <rs>HEN-te</rs>.</li><li><es>veía</es>: <rs>be-EE-a</rs>.</li>
    <li><es>ciencia</es>: two syllables, <rs>SYEN-sya</rs>.</li><li><es>podrá</es>: stress on the last syllable.</li>
    <li><es>cualquier</es>: <rs>kwal-KYER</rs>.</li></ul>"""),
    ("Two voices", """<p>As in paragraph 1, give Melquíades a public, announcing voice for the two quotations, and drop back for <es>pregonaba Melquíades</es>.</p>"""),
  ],
  exercises=[
    ("How much did a look cost?", "Five reales: <es>el pago de cinco reales</es>."),
    ("What did people see through the telescope?", "The gypsy woman, as if within reach of their hand: <es>al alcance de su mano</es>."),
    ("Why is it <es>asomaba</es> and not <es>asomaban</es>?", "The subject, <es>la gente</es>, is grammatically singular."),
    ("What is the <es>a</es> doing in <es>veía a la gitana</es>?", "It is the personal <es>a</es>, required before a direct object that is a person. It is not translated."),
    ("Translate: <es>La ciencia ha eliminado las distancias</es>.", "Science has eliminated distances."),
    ("What tense is <es>podrá</es>, and what does it mean?", "Future: \"will be able to\"."),
  ],
  review_html="""<p>Recite sentences 1 to 3. Which verbs in them are preterite and which one is imperfect?</p>""",
  memo="""<p><b>Pay, look, see.</b> Sentence 4 follows the customer: the payment, the eye at the telescope, the gypsy within reach.</p>
  <p>The two quotations are worth knowing as a pair: a claim about now (<es>ha eliminado</es>) and a promise about the future (<es>podrá ver</es>).</p>""",
),

# ------------------------------------------------------------------ 23
dict(
  para=2, title="Fire from the sun",
  kind="lesson", new=[7, 8], review=[4, 5, 6],
  objectives=[
    "Understand sentences 7 and 8.",
    "Recognise three irregular preterites: <es>hicieron</es>, <es>pusieron</es>, <es>prendieron</es>.",
    "Tell <es>aún</es> (still) from <es>aun</es> (even).",
  ],
  intro="""<p>The second marvel is the giant magnifying glass. José Arcadio Buendía, still sore about the magnets, sees in it not a toy but a weapon.</p>""",
  grammar=[
    ("<es>Un mediodía ardiente</es>", """<p><es>un</es> + a time word means "one": "one burning noon". <es>mediodía</es> is <es>medio</es> (half) + <es>día</es> (day).</p>"""),
    ("<es>hicieron</es>, <es>pusieron</es>", """<p>The "they" preterites of <es>hacer</es> and <es>poner</es>, both irregular. You know the singular <es>hizo</es> from <es>hizo una truculenta demostración pública</es>;
    here is its plural with almost the same object: <es>hicieron una asombrosa demostración</es>.</p>"""),
    ("The colon", """<p>The colon after <es>gigantesca</es> announces the demonstration itself: what follows explains what came before.</p>"""),
    ("<es>le prendieron fuego</es>", """<p><es>prender fuego a</es> something is to set fire to it. <es>le</es>, "to it", stands for the heap of dry grass.</p>"""),
    ("<es>mediante la concentración de los rayos solares</es>", """<p><es>mediante</es>, "by means of", for the second time. This phrase returns word for word in sentence 14.</p>"""),
    ("<es>que aún no acababa de consolarse</es>", """<p><es>aún</es> with an accent is "still, yet". <es>no acabar de</es> + infinitive is "not quite to manage to": he had still not quite got over it.
    Without the accent, <es>aun</es> is "even", as in <es>aun los objetos perdidos</es>.</p>"""),
    ("<es>concibió la idea de utilizar</es>", """<p><es>la idea de</es> + infinitive: "the idea of using". <es>aquel invento</es> echoes <es>aquella invención inútil</es> in paragraph 1.</p>"""),
    ("<es>un arma de guerra</es>", """<p><es>arma</es> is feminine, but like <es>el ánima</es> it begins with a stressed a-, so it takes <es>un</es> and <es>el</es> in the singular. Its adjective stays feminine: <es>su arma novedosa</es> in sentence 16.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>mediodía</es>: four syllables, <rs>me-dyo-DEE-a</rs>.</li><li><es>hicieron</es>: silent h, <rs>ee-SYEH-ron</rs>.</li>
    <li><es>gigantesca</es>: the first g is a breathy h, the second is hard: <rs>hee-gan-TES-ka</rs>.</li><li><es>hierba</es>: <rs>YER-ba</rs>.</li>
    <li><es>calle</es>: <rs>KA-ye</rs>.</li><li><es>fuego</es>: <rs>FWEH-go</rs>.</li><li><es>aún</es>: two syllables, <rs>a-OON</rs>, against one for <es>aun</es>.</li>
    <li><es>guerra</es>: gu before e is a hard g with silent u, and rr is rolled: <rs>GEH-rra</rs>.</li><li><es>concibió</es>: <rs>kon-see-BYO</rs>.</li></ul>"""),
  ],
  exercises=[
    ("What did the gypsies burn, and where?", "A heap of dry grass (<es>un montón de hierba seca</es>) in the middle of the street (<es>en mitad de la calle</es>)."),
    ("How did they light it?", "By concentrating the sun's rays: <es>mediante la concentración de los rayos solares</es>."),
    ("What had José Arcadio still not got over?", "The failure of his magnets: <es>el fracaso de sus imanes</es>."),
    ("What did he want to use the magnifying glass for?", "As a weapon of war: <es>como un arma de guerra</es>."),
    ("<es>aún</es> or <es>aun</es>: which means \"still\"?", "<es>aún</es>, with the accent."),
    ("Why <es>un arma</es> when <es>arma</es> is feminine?", "Feminine nouns that begin with a stressed a- take <es>un</es> and <es>el</es> in the singular."),
  ],
  review_html="""<p>Recite sentences 4 to 6. Then say Melquíades' two quotations without the narrator's words between them.</p>""",
  memo="""<p><b>Demonstration, then idea.</b> Sentence 7 is announcement + colon + two actions (<es>pusieron</es>, <es>prendieron</es>). Sentence 8 has the frame you know from paragraph 1:
  <es>José Arcadio Buendía</es> + an aside in commas + what he thought of doing.</p>""",
),

# ------------------------------------------------------------------ 24
dict(
  para=2, title="Úrsula's gold",
  kind="lesson", new=[9, 10, 11, 12], review=[7, 8],
  objectives=[
    "Understand sentences 9 to 12.",
    "Recognise the pluperfect: <es>había acumulado</es>, <es>había enterrado</es>.",
    "Use <es>otra vez</es>, <es>terminar por</es>, and <es>a cambio de</es>.",
  ],
  intro="""<p>The bargain scene of paragraph 1 replays, faster and more painfully: this time the price is Úrsula's inheritance.</p>""",
  grammar=[
    ("<es>Melquíades, otra vez, trató de disuadirlo</es>", """<p><es>otra vez</es>, "again". <es>tratar de</es> + infinitive, "to try to": you met its gerund in <es>tratando de desenclavarse</es>.
    And <es>disuadirlo</es> is the very word that ended Úrsula's sentence in paragraph 1: <es>no consiguió disuadirlo</es>.</p>"""),
    ("<es>Pero terminó por aceptar</es>", """<p><es>terminar por</es> + infinitive: "to end up doing". The subject is still Melquíades.</p>"""),
    ("<es>a cambio de la lupa</es>", """<p><es>a cambio de</es>, "in exchange for". In paragraph 1 the same idea used the verb: <es>cambió su mulo ... por los dos lingotes imantados</es>. Now the ingots themselves go back as part of the price.</p>"""),
    ("<es>Úrsula lloró de consternación</es>", """<p><es>de</es> gives the cause of an emotion or a bodily reaction: wept <em>with</em> dismay. Later: <es>temblando de fiebre</es>.</p>"""),
    ("<es>había acumulado</es>, <es>había enterrado</es>", """<p>The pluperfect, "had done": <es>había</es> + participle. It reaches back before the story's present: her father <em>had accumulated</em> the coins, and she <em>had buried</em> them.
    <es>enterrado</es> is the opposite of <es>desenterrar</es> in paragraph 1: <b>en-</b> + <es>tierra</es>.</p>"""),
    ("<es>su padre</es>, <es>ella</es>", """<p><es>su padre</es> here is <em>her</em> father. Spanish normally leaves subject pronouns out; <es>ella</es> is stated because the subject changes from her father to her.</p>"""),
    ("<es>para invertirlas</es>", """<p><es>las</es> = <es>las monedas</es> (feminine plural), attached to the infinitive as in <es>mencionarlas</es>.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>terminó</es>, <es>trató</es>, <es>lloró</es>: all stressed on the final ó. <es>lloró</es> is <rs>yo-RO</rs>.</li>
    <li><es>consternación</es>: <rs>kons-ter-na-SYON</rs>.</li><li><es>privaciones</es>: <rs>pree-ba-SYO-nes</rs>.</li>
    <li><es>ella</es>: <rs>EH-ya</rs>.</li><li><es>debajo</es>: <rs>de-BA-ho</rs>.</li><li><es>ocasión</es>: <rs>o-ka-SYON</rs>.</li></ul>"""),
    ("Three short sentences", """<p>Sentences 9, 10 and 11 are brisk. Read them quickly and flatly, then slow down for the long sentence about the coins, which carries the feeling.</p>"""),
  ],
  exercises=[
    ("What did Melquíades try to do, again?", "Dissuade him: <es>trató de disuadirlo</es>."),
    ("What did he accept for the magnifying glass?", "The two magnetised ingots and three pieces of colonial money."),
    ("Where did the money come from?", "From a chest of gold coins that Úrsula's father had saved over a lifetime of hardship."),
    ("Where had Úrsula kept it, and why?", "Buried under the bed (<es>debajo de la cama</es>), waiting for a good opportunity to invest it."),
    ("Translate: <es>había enterrado</es>.", "Had buried."),
    ("What does <es>las</es> in <es>invertirlas</es> stand for?", "<es>las monedas</es>, the coins."),
  ],
  review_html="""<p>Recite sentences 7 and 8. Then, from paragraph 1, say what José Arcadio traded for the magnets and what Úrsula failed to do.</p>""",
  memo="""<p><b>Tried, yielded, wept, why.</b> Four sentences, one beat each. For the long sentence 12 keep the order of the coins' history:
  part of a chest → her father saved it → she buried it → under the bed → waiting → to invest.</p>""",
),

# ------------------------------------------------------------------ 25
dict(
  para=2, title="Checkpoint 5: the telescope and the burning glass",
  kind="review", new=[], review=list(range(1, 13)),
  objectives=[
    "Read sentences 1 to 12 aloud as one passage.",
    "Place each verb tense you now know on a timeline.",
    "Recite sentences 1 to 12 from memory.",
  ],
  intro="""<p>Two scenes are complete: the telescope (sentences 1 to 6) and the burning glass (7 to 12). This checkpoint fixes them before the long middle of the paragraph.</p>""",
  grammar=[
    ("Five tenses on one line", """<table class="mini"><tr><th>Tense</th><th>When</th><th>Examples so far</th></tr>
    <tr><td>Pluperfect</td><td>before the story</td><td><es>había acumulado</es>, <es>había enterrado</es></td></tr>
    <tr><td>Imperfect</td><td>background, habit</td><td><es>llevaban</es>, <es>se asomaba</es>, <es>veía</es>, <es>pregonaba</es>, <es>no acababa</es>, <es>formaba</es></td></tr>
    <tr><td>Preterite</td><td>events</td><td><es>volvieron</es>, <es>exhibieron</es>, <es>sentaron</es>, <es>instalaron</es>, <es>hicieron</es>, <es>pusieron</es>, <es>prendieron</es>, <es>concibió</es>, <es>trató</es>, <es>terminó</es>, <es>lloró</es></td></tr>
    <tr><td>Present perfect</td><td>up to now (in speech)</td><td><es>ha eliminado</es></td></tr>
    <tr><td>Future</td><td>to come (in speech)</td><td><es>podrá</es></td></tr></table>"""),
    ("Echoes of paragraph 1", """<p>The second paragraph is built on the first. <es>En marzo</es> ↔ <es>por el mes de marzo</es>; <es>el último descubrimiento de los judíos de Ámsterdam</es> ↔ <es>la octava maravilla de los sabios alquimistas de Macedonia</es>;
    <es>hicieron una asombrosa demostración</es> ↔ <es>hizo una truculenta demostración pública</es>; <es>trató de disuadirlo</es> ↔ <es>no consiguió disuadirlo</es>; <es>los dos lingotes imantados</es> word for word.
    Use each echo as a hook.</p>"""),
    ("Small words gained", """<p><es>esta</es> (this), <es>e</es> (and, before i-), <es>mediante</es> (by means of), <es>sin</es> (without), <es>aún</es> (still), <es>otra</es> (another), <es>ella</es> (she), <es>debajo de</es> (under), <es>cualquier</es> (any).</p>"""),
  ],
  pron=[
    ("Stress in the preterite", """<p>The "he / she" preterite is stressed on its last syllable, and that stress is what separates it from other forms: <es>trató</es>, <es>terminó</es>, <es>lloró</es>, <es>concibió</es>.
    The "they" form is stressed one syllable from the end: <es>vol-VIE-ron</es>, <es>sen-TA-ron</es>, <es>hi-CIE-ron</es>. Read the list aloud, leaning on the right syllable.</p>"""),
    ("Shadowing", """<p>Play sentences 1 to 12 at 0.75× and shadow the narrator. Then once at full speed.</p>"""),
  ],
  exercises=[
    ("Name the two inventions of this visit.", "<es>el catalejo</es> (the telescope) and <es>la lupa</es> (the magnifying glass)."),
    ("Translate: <es>sin moverse de su casa</es>.", "Without stirring from his house."),
    ("Which sentence has no verb in a past tense?", "Sentence 6, Melquíades' prophecy: <es>podrá</es> is future and <es>ocurre</es> present."),
    ("Complete: <es>que aún no acababa de consolarse por...</es>", "<es>...el fracaso de sus imanes</es>."),
    ("Who is the subject of <es>terminó por aceptar</es>?", "Melquíades."),
    ("Give the Spanish for: grass, street, fire, money, bed, coins.", "<es>hierba, calle, fuego, dinero, cama, monedas</es>."),
    ("What are the first two words of sentences 1, 2, 3, 4, 7 and 12?", "<es>En marzo</es> · <es>Esta vez</es> · <es>Sentaron una</es> · <es>Mediante el</es> · <es>Un mediodía</es> · <es>Aquel dinero</es>."),
  ],
  review_html="""<p>Work through the twelve sentences: play, shadow, read alone. Then read 1 to 12 from the top without stopping.</p>""",
  memo="""<p><b>Two scenes, two inventions.</b> Scene one: return → telescope and glass → set-up → the customers → two quotations. Scene two: the fire → the idea → the attempt to dissuade → the trade → Úrsula weeps → the coins.</p>
  <p>Recite each scene in the practice box, then both together.</p>""",
),

# ------------------------------------------------------------------ 26
dict(
  para=2, title="The experimenter",
  kind="lesson", new=[13, 14], review=[11, 12],
  objectives=[
    "Understand sentences 13 and 14.",
    "Use <es>no ... siquiera</es> (not even) and the patterns <es>convertirse en</es> and <es>tardar en</es>.",
    "Recognise a participle that opens a long description: <es>entregado</es>.",
  ],
  intro="""<p>He does not comfort his wife; he is already at work. Then he tests the weapon on the only soldier available: himself.</p>""",
  grammar=[
    ("<es>no trató siquiera de consolarla</es>", """<p><es>siquiera</es> with a negative is "even": "did not even try to console her". <es>consolarla</es> = <es>consolar</es> + <es>la</es> (her). Compare <es>consolarse</es> in sentence 8: he could not console himself, and does not console her.</p>"""),
    ("<es>entregado por entero a sus experimentos tácticos</es>", """<p><es>entregado</es> is a participle describing him: "given over", "devoted". <es>por entero</es> is "entirely". The whole phrase hangs on the main clause the way an "-ed" phrase does in English.</p>"""),
    ("<es>con la abnegación de un científico</es>", """<p>"With the self-denial of a scientist". The irony is the narrator's: his science is setting himself on fire.</p>"""),
    ("<es>y aun a riesgo de su propia vida</es>", """<p><es>aun</es> without an accent: "even". <es>a riesgo de</es>, "at the risk of". <es>propia</es> before the noun means "own": <es>su propia vida</es>, "his own life".
    (After the noun it meant "of their own": <es>vida propia</es>.)</p>"""),
    ("<es>se expuso él mismo</es>", """<p><es>expuso</es> is the irregular preterite of <es>exponer</es>, formed like <es>poner</es> → <es>puso</es>. <es>se</es> makes it reflexive and <es>él mismo</es> underlines it: "he exposed himself, in person".</p>"""),
    ("<es>quemaduras que se convirtieron en úlceras</es>", """<p><es>convertirse en</es>: "to turn into". <es>quemadura</es> comes from <es>quemar</es>, to burn; the ending <b>-dura</b> makes the result of an action.</p>"""),
    ("<es>tardaron mucho tiempo en sanar</es>", """<p><es>tardar</es> + a length of time + <es>en</es> + infinitive: "to take that long to". The burns are the subject: they "took a long time to heal".
    <es>mucho tiempo</es> you know from <es>desde hacía mucho tiempo</es>.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>siquiera</es>: <rs>see-KYEH-ra</rs>.</li><li><es>abnegación</es>: <rs>ab-ne-ga-SYON</rs>.</li>
    <li><es>científico</es>: <rs>syen-TEE-fee-ko</rs>.</li><li><es>riesgo</es>: rolled r, <rs>RRYES-go</rs>.</li>
    <li><es>expuso</es>: <rs>eks-POO-so</rs>.</li><li><es>quemaduras</es>: qu as k, <rs>ke-ma-DOO-ras</rs>.</li>
    <li><es>convirtieron</es>: <rs>kon-beer-TYEH-ron</rs>.</li><li><es>úlceras</es>: stress on the first syllable.</li></ul>"""),
  ],
  exercises=[
    ("Did he comfort Úrsula?", "No: <es>no trató siquiera de consolarla</es>, he did not even try."),
    ("What was he given over to?", "<es>sus experimentos tácticos</es>: his tactical experiments."),
    ("What was he trying to demonstrate?", "The effects of the magnifying glass on enemy troops: <es>los efectos de la lupa en la tropa enemiga</es>."),
    ("What happened to him?", "He suffered burns that turned into sores and took a long time to heal."),
    ("<es>aun</es> in <es>aun a riesgo de su propia vida</es>: \"still\" or \"even\"?", "\"Even\": there is no accent."),
    ("Translate: <es>tardaron mucho tiempo en sanar</es>.", "They took a long time to heal."),
  ],
  review_html="""<p>Recite sentences 11 and 12: Úrsula weeps, and the history of the coins. Today's first sentence is his answer to her tears.</p>""",
  memo="""<p><b>Cause and consequence.</b> Sentence 14 is a chain: trying to demonstrate → he exposed himself → he suffered burns → they became sores → they were slow to heal. Each link causes the next.</p>
  <p>Sentence 13: what he did not do, then three phrases of what absorbed him, <es>entregado...</es>, <es>con la abnegación...</es>, <es>y aun a riesgo...</es></p>""",
),

# ------------------------------------------------------------------ 27
dict(
  para=2, title="Nearly burning the house, and the manual",
  kind="lesson", new=[15, 16], review=[13, 14],
  objectives=[
    "Understand sentences 15 and 16.",
    "Meet <es>estar</es>, the second verb \"to be\", in <es>estuvo a punto de</es>.",
    "Use <es>hasta que</es> (until) and the gerund ending <b>-iendo</b>.",
  ],
  intro="""<p>A short sentence of domestic danger, then a long one of solitary study that ends in a triumph on paper: a manual.</p>""",
  grammar=[
    ("<es>Ante las protestas de su mujer</es>", """<p><es>ante</es> is "before", "in the face of". It appears again in <es>ante los poderes militares</es> and <es>ante Melquíades</es>.</p>"""),
    ("<es>alarmada por tan peligrosa inventiva</es>", """<p><es>alarmada</es> is feminine because it describes <es>su mujer</es>. <es>tan</es> + adjective + noun, with no <es>que</es>, means "such": "such dangerous inventiveness".</p>"""),
    ("<es>estuvo a punto de incendiar la casa</es>", """<p>Spanish has two verbs "to be". <es>ser</es> (<es>era</es>, <es>fue</es>, <es>es</es>) says what something is. <es>estar</es> says where or in what state it is.
    <es>estuvo</es> is the preterite of <es>estar</es>. <es>estar a punto de</es> + infinitive is "to be on the point of", "to come close to". You will read it three times in this paragraph.</p>"""),
    ("<es>Pasaba largas horas</es>", """<p><es>pasar</es> + time is "to spend". Imperfect: he would do this day after day. <es>largas</es> means long, not large.</p>"""),
    ("<es>haciendo cálculos</es>", """<p>The gerund of -er and -ir verbs ends in <b>-iendo</b>: <es>hacer</es> → <es>haciendo</es>, beside <b>-ando</b> for -ar verbs (<es>arrastrando</es>).</p>"""),
    ("<es>hasta que logró componer un manual</es>", """<p><es>hasta que</es>, "until". <es>logró</es> + infinitive you know from <es>lo único que logró desenterrar</es>: then an armour, now a book.</p>"""),
    ("Two phrases describing the manual", """<p><es>de una asombrosa claridad didáctica</es> and <es>(de) un poder de convicción irresistible</es>. Each noun has a colouring adjective in front or a plain one behind: astonishing <em>instructional</em> clarity; an <em>irresistible</em> power of persuasion.
    <es>asombrosa</es> is the adjective used for the demonstration in sentence 7.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>peligrosa</es>: <rs>pe-lee-GRO-sa</rs>.</li><li><es>estuvo</es>: <rs>es-TOO-bo</rs>.</li><li><es>incendiar</es>: <rs>een-sen-DYAR</rs>.</li>
    <li><es>haciendo</es>: silent h, <rs>a-SYEN-do</rs>.</li><li><es>cálculos</es>, <es>estratégicas</es>, <es>didáctica</es>: each has its written accent on the stressed syllable.</li>
    <li><es>posibilidades</es>: six even syllables, <rs>po-see-bee-lee-DA-des</rs>.</li><li><es>convicción</es>: cc is "ks", <rs>kon-beek-SYON</rs>.</li></ul>"""),
    ("Long adjectives in a row", """<p><es>posibilidades estratégicas</es>, <es>claridad didáctica</es>, <es>convicción irresistible</es>: build each pair from its last syllable backwards, as in Lesson 8.</p>"""),
  ],
  exercises=[
    ("What nearly happened to the house?", "He was on the point of setting it on fire: <es>estuvo a punto de incendiar la casa</es>."),
    ("Why is it <es>alarmada</es>, with -a?", "It agrees with <es>su mujer</es>."),
    ("What did he do for long hours in his room?", "Made calculations about the strategic possibilities of his new weapon."),
    ("What did he finally produce?", "A manual, astonishingly clear and irresistibly convincing."),
    ("Which verb \"to be\" is <es>estuvo</es> from?", "<es>estar</es>."),
    ("Give the gerund of <es>hacer</es>.", "<es>haciendo</es>."),
  ],
  review_html="""<p>Recite sentences 13 and 14. Then name the chain of five links in sentence 14.</p>""",
  memo="""<p><b>Room, sums, book.</b> Sentence 16: where and how long (<es>Pasaba largas horas en su cuarto</es>) → doing what (<es>haciendo cálculos sobre...</es>) → until what (<es>hasta que logró componer un manual</es>) → what kind of manual (two phrases).</p>""",
),

# ------------------------------------------------------------------ 28
dict(
  para=2, title="The messenger",
  kind="lesson", new=[17], review=[15, 16],
  objectives=[
    "Understand sentence 17, the longest of the paragraph (65 words).",
    "See its shape: what he sent, what went with it, who carried it, and the messenger's four adventures.",
    "Read it aloud in six breaths.",
  ],
  intro="""<p>One sentence carries the manual from Macondo to the capital, and it is as long and difficult as the journey. Like sentence 7 of paragraph 1, it is a list; find the list and it opens up.</p>""",
  grammar=[
    ("The shape", """<ol><li><es>Lo envió a las autoridades</es>: he sent it to the authorities.</li>
    <li><es>acompañado de</es> A <es>y de</es> B: accompanied by accounts and by drawings.</li>
    <li><es>al cuidado de un mensajero que...</es>: in the care of a messenger who...</li>
    <li>four verbs: <es>atravesó</es>, <es>se extravió</es>, <es>remontó</es>, <es>estuvo a punto de perecer</es>.</li>
    <li><es>antes de conseguir...</es>: before finding the mail route.</li></ol>"""),
    ("<es>Lo envió</es>", """<p><es>lo</es> is "it", the manual, standing before the verb. <es>acompañado</es> is masculine singular to match it.</p>"""),
    ("<es>numerosos testimonios sobre sus experiencias</es>", """<p><es>experiencias</es> is used in an older sense, "experiments". <es>sobre</es> is "about", as in <es>cálculos sobre las posibilidades</es>.</p>"""),
    ("<es>varios pliegos de dibujos explicativos</es>", """<p><es>varios</es> you know from <es>Durante varios meses</es>. A <es>pliego</es> is a large sheet of paper.</p>"""),
    ("The four adventures", """<p>All four verbs are preterites with the stress on the last syllable, and each has its own landscape: <es>atravesó la sierra</es> (mountains), <es>se extravió en pantanos desmesurados</es> (swamps),
    <es>remontó ríos tormentosos</es> (rivers), <es>estuvo a punto de perecer bajo el azote de las fieras, la desesperación y la peste</es> (beasts, despair, plague). <es>la desesperación</es> you met among the nails and screws of paragraph 1.</p>"""),
    ("<es>antes de conseguir una ruta de enlace con las mulas del correo</es>", """<p><es>antes de</es> + infinitive: "before finding". <es>conseguir</es> is the infinitive of <es>consiguió</es>. <es>mulas</es> is the feminine of <es>mulo</es>, the animal he traded away in paragraph 1.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>envió</es>: <rs>en-BYO</rs>.</li><li><es>autoridades</es>: <rs>aw-to-ree-DA-des</rs>.</li><li><es>testimonios</es>: <rs>tes-tee-MO-nyos</rs>.</li>
    <li><es>pliegos</es>: <rs>PLYEH-gos</rs>.</li><li><es>dibujos</es>, <es>mensajero</es>: j as breathy h.</li><li><es>atravesó</es>, <es>extravió</es>, <es>remontó</es>: final stress; rolled r in <es>remontó</es> and <es>ríos</es>.</li>
    <li><es>desmesurados</es>: <rs>des-me-su-RA-dos</rs>.</li><li><es>perecer</es>: <rs>pe-re-SER</rs>.</li><li><es>azote</es>: <rs>a-SO-te</rs>.</li></ul>"""),
    ("Six breaths", """<ol><li><es>Lo envió a las autoridades</es></li><li><es>acompañado de numerosos testimonios sobre sus experiencias y de varios pliegos de dibujos explicativos,</es></li>
    <li><es>al cuidado de un mensajero que atravesó la sierra,</es></li><li><es>se extravió en pantanos desmesurados, remontó ríos tormentosos</es></li>
    <li><es>y estuvo a punto de perecer bajo el azote de las fieras, la desesperación y la peste,</es></li><li><es>antes de conseguir una ruta de enlace con las mulas del correo.</es></li></ol>"""),
  ],
  exercises=[
    ("What does <es>lo</es> in <es>Lo envió</es> stand for?", "The manual, <es>el manual</es>."),
    ("What two things went with it?", "Numerous accounts of his experiments, and several sheets of explanatory drawings."),
    ("Name the messenger's four adventures.", "He crossed the mountains, got lost in boundless swamps, went up stormy rivers, and nearly perished."),
    ("Under the scourge of which three things did he nearly perish?", "<es>las fieras, la desesperación y la peste</es>: wild beasts, despair and plague."),
    ("What did he find in the end?", "A route linking up with the mail mules: <es>una ruta de enlace con las mulas del correo</es>."),
    ("Translate: <es>antes de conseguir</es>.", "Before finding (getting)."),
  ],
  review_html="""<p>Recite sentences 15 and 16, ending on <es>un poder de convicción irresistible</es>. Today's <es>Lo</es> points straight back at that manual.</p>""",
  memo="""<p><b>A map.</b> Draw the journey as a line with four stations: mountains, swamps, rivers, death's door, and the mail mules at the far end. Recite while tracing it.</p>
  <p>The packet is easy to remember as three things in a bag: the manual, the accounts, the drawings.</p>""",
),

# ------------------------------------------------------------------ 29
dict(
  para=2, title="A promise, and years of waiting",
  kind="lesson", new=[18, 19], review=[17],
  objectives=[
    "Understand sentences 18 and 19.",
    "Meet the subjunctive in <es>tan pronto como se lo ordenara</es>.",
    "Use <es>a pesar de que</es> (although), <es>con el fin de</es> (in order to) and adverbs in <b>-mente</b>.",
  ],
  intro="""<p>Fifty-five words of eager promises, then six words of silence. The contrast is the joke.</p>""",
  grammar=[
    ("<es>A pesar de que...</es>", """<p>"In spite of the fact that", "although". The clause it opens runs to <es>imposible</es>.</p>"""),
    ("<es>era en aquel tiempo poco menos que imposible</es>", """<p><es>en aquel tiempo</es> you know from paragraph 1. <es>poco menos que</es>, literally "little less than", means "little short of".</p>"""),
    ("<es>prometía intentarlo</es>", """<p>Imperfect: he kept promising. <es>intentarlo</es> = <es>intentar</es> + <es>lo</es>, "to attempt it", the journey.</p>"""),
    ("<es>tan pronto como se lo ordenara el gobierno</es>", """<p>Your first <b>subjunctive</b>. Spanish uses a special set of verb forms for things that are not facts: wishes, purposes, events that have not happened yet.
    The government had not ordered anything, so "as soon as it ordered him" takes the subjunctive <es>ordenara</es>, not the factual <es>ordenó</es>. For now, simply recognise the ending <b>-ara</b> (or <b>-iera</b>) as its sign.</p>
    <p><es>se lo</es> is "it to him": <es>le</es> (to him) changes to <es>se</es> when it stands before <es>lo</es>. The subject, <es>el gobierno</es>, comes last.</p>"""),
    ("<es>con el fin de hacer demostraciones prácticas</es>", """<p><es>con el fin de</es> + infinitive is a formal "in order to". Two infinitives depend on it: <es>hacer</es> and <es>adiestrarlos</es>.</p>"""),
    ("<es>adiestrarlos personalmente</es>", """<p><es>los</es>, "them", the military authorities. <b>-mente</b> added to an adjective makes an adverb, like English "-ly": <es>personal</es> → <es>personalmente</es>.</p>"""),
    ("<es>las complicadas artes de la guerra solar</es>", """<p><es>arte</es> is feminine in the plural: <es>las artes</es>. "The complicated arts of solar war", which exist only in his manual.</p>"""),
    ("<es>Durante varios años esperó la respuesta</es>", """<p>Built exactly like <es>Durante varios meses se empeñó...</es> in paragraph 1. <es>esperar</es> means both "to wait for" and "to hope for", with no preposition.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>viaje</es>: <rs>BYA-he</rs>.</li><li><es>prometía</es>: <rs>pro-me-TEE-a</rs>.</li><li><es>ordenara</es>: stress on <rs>NA</rs>: <rs>or-de-NA-ra</rs>.</li>
    <li><es>gobierno</es>: <rs>go-BYER-no</rs>.</li><li><es>demostraciones</es>: <rs>de-mos-tra-SYO-nes</rs>.</li><li><es>adiestrarlos</es>: <rs>a-dyes-TRAR-los</rs>.</li>
    <li><es>personalmente</es>: two stresses, <rs>per-so-NAL-MEN-te</rs>.</li><li><es>respuesta</es>: rolled r, <rs>rres-PWES-ta</rs>.</li></ul>"""),
    ("Pacing", """<p>Take sentence 18 in four breaths, at the commas. Then leave a full second of silence, and say sentence 19 slowly.</p>"""),
  ],
  exercises=[
    ("How hard was the journey to the capital?", "Little short of impossible: <es>poco menos que imposible</es>."),
    ("What did he promise?", "To attempt it as soon as the government ordered him to."),
    ("For what two purposes?", "To give practical demonstrations of his invention before the military authorities, and to train them personally in solar warfare."),
    ("Why <es>ordenara</es> and not <es>ordenó</es>?", "The order had not been given; an event still to come after <es>tan pronto como</es> takes the subjunctive."),
    ("What does <b>-mente</b> correspond to in English?", "-ly."),
    ("How long did he wait?", "Several years: <es>Durante varios años esperó la respuesta</es>."),
  ],
  review_html="""<p>Recite sentence 17 with your map of the messenger's journey.</p>""",
  memo="""<p><b>Although, promise, when, why.</b> Sentence 18: the difficulty (<es>A pesar de que...</es>) → the promise (<es>prometía intentarlo</es>) → the condition (<es>tan pronto como...</es>) → the purpose in two parts (<es>hacer demostraciones</es>, <es>adiestrarlos</es>).</p>
  <p>Sentence 19 you can learn in ten seconds; set it beside <es>Durante varios meses...</es> from paragraph 1.</p>""",
),

# ------------------------------------------------------------------ 30
dict(
  para=2, title="Checkpoint 6: the weapon of war",
  kind="review", new=[], review=list(range(13, 20)),
  objectives=[
    "Read sentences 13 to 19 aloud as one scene.",
    "Sort the paragraph's verb-plus-preposition patterns.",
    "Recite sentences 13 to 19, and read 1 to 19 from the top.",
  ],
  intro="""<p>The middle of the paragraph is the hardest stretch: long sentences, abstract nouns. Give this checkpoint the time it needs.</p>""",
  grammar=[
    ("Verbs that bring a preposition", """<table class="mini"><tr><th>Pattern</th><th>Meaning</th><th>Where</th></tr>
    <tr><td><es>tratar de</es> + infinitive</td><td>to try to</td><td>9, 13, 14</td></tr>
    <tr><td><es>terminar por</es> + infinitive</td><td>to end up doing</td><td>10</td></tr>
    <tr><td><es>no acabar de</es> + infinitive</td><td>not quite to manage to</td><td>8</td></tr>
    <tr><td><es>convertirse en</es></td><td>to turn into</td><td>14</td></tr>
    <tr><td><es>tardar en</es> + infinitive</td><td>to take (time) to</td><td>14</td></tr>
    <tr><td><es>estar a punto de</es> + infinitive</td><td>to be on the point of</td><td>15, 17</td></tr>
    <tr><td><es>lograr</es> + infinitive</td><td>to manage to (no preposition)</td><td>16</td></tr></table>"""),
    ("Infinitive after a preposition", """<p><es>sin moverse</es> · <es>antes de conseguir</es> · <es>con el fin de hacer</es> · <es>a punto de incendiar</es>. Where English says "without moving", "before finding", Spanish always uses the infinitive.</p>"""),
    ("Feminine endings worth knowing", """<p>Nouns in <b>-ción</b>, <b>-dad</b> and <b>-ez</b> are feminine: <es>la abnegación</es>, <es>la concentración</es>, <es>la convicción</es>, <es>la desesperación</es>; <es>la claridad</es>, <es>las posibilidades</es>, <es>las autoridades</es>; <es>la honradez</es>.
    Their adjectives follow: <es>asombrosa claridad didáctica</es>.</p>"""),
  ],
  pron=[
    ("Even syllables in long words", """<p>Tap each syllable of <es>po-si-bi-li-da-des es-tra-té-gi-cas</es> and <es>de-mos-tra-cio-nes prác-ti-cas</es>. No syllable is swallowed.</p>"""),
    ("Shadow the scene", """<p>Play sentences 13 to 19 at 0.75×, shadowing. Sentence 17 twice.</p>"""),
  ],
  exercises=[
    ("Put the events of sentences 13 to 19 in order, in English.", "He ignores Úrsula and experiments; burns himself; nearly burns the house; writes a manual; sends it by messenger; promises to go to the capital; waits for years."),
    ("Translate: <es>estuvo a punto de perecer</es>.", "He was on the point of perishing."),
    ("Which phrase occurs word for word in both sentence 7 and sentence 14?", "<es>la concentración de los rayos solares</es>."),
    ("Complete: <es>hasta que logró componer un manual de una asombrosa...</es>", "<es>...claridad didáctica y un poder de convicción irresistible</es>."),
    ("Give the Spanish for: burns, room, messenger, swamps, journey, government, answer.", "<es>quemaduras, cuarto, mensajero, pantanos, viaje, gobierno, respuesta</es>."),
    ("What are the first words of sentences 13 to 19?", "<es>José Arcadio Buendía no trató</es> · <es>Tratando de</es> · <es>Ante las</es> · <es>Pasaba largas</es> · <es>Lo envió</es> · <es>A pesar</es> · <es>Durante varios</es>."),
  ],
  review_html="""<p>Sentences 13 to 19: play, shadow, read alone. Then read sentences 1 to 19 from the top with the text visible.</p>""",
  memo="""<p><b>From tears to silence.</b> The scene runs: no comfort → burns → near-fire → manual → messenger → promise → waiting. Seven sentences, seven openers; learn the openers as a chain, then recite.</p>""",
),
]
