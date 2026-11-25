# Lessons 1-10.  Markup used inside strings:
#   <es>...</es>  Spanish text (tap to hear the browser voice)
#   <rs>...</rs>  rough English-style respelling, stressed syllable in capitals
# "new" lists the sentences taught; "part" optionally narrows to a chunk range (1-based, inclusive).

LESSONS_A = [

# ------------------------------------------------------------------ 1
dict(
  title="The five vowels, stress, and the opening words",
  kind="lesson", new=[1], part=(1, 1, 2), review=[],
  objectives=[
    "Pronounce the five Spanish vowels, each with one unchanging sound.",
    "Work out which syllable of any Spanish word is stressed, and what an accent mark does.",
    "Understand and say the first two phrases: <es>Muchos años después, frente al pelotón de fusilamiento</es>.",
  ],
  intro="""<p>Spanish spelling is honest: once you know a handful of rules you can read any word in this paragraph aloud,
  even before you know what it means. This lesson gives you the two rules that matter most, the vowels and the stress,
  and uses them on the first nine words of the novel.</p>
  <p>The printed text opens with <es>MUCHOS</es> in capitals. That is only a typographic flourish at the start of a chapter;
  read it as the ordinary word <es>muchos</es>.</p>""",
  grammar=[
    ("Every noun has a gender", """<p>Spanish nouns are either masculine or feminine, and the words around them change to match.
    <es>año</es> (year) is masculine, so "many years" is <es>muchos años</es>, with the masculine plural ending <b>-os</b>.
    With a feminine noun it would be <es>muchas</es>, which you will meet in sentence 3 (<es>muchas cosas</es>).</p>"""),
    ("Time first, then <es>después</es>", """<p><es>después</es> means "later" or "afterwards". The amount of time comes first, exactly as in English:
    <es>muchos años después</es>, "many years later".</p>"""),
    ("<es>al</es> = <es>a</es> + <es>el</es>", """<p><es>frente a</es> means "facing". When <es>a</es> (to, at) meets <es>el</es> (the, masculine) the two always fuse
    into <es>al</es>. So <es>frente al pelotón</es> is "facing the squad".</p>"""),
    ("Nouns joined by <es>de</es>", """<p>English stacks nouns: "firing squad". Spanish reverses the order and puts <es>de</es> (of) between them:
    <es>pelotón de fusilamiento</es>, literally "squad of shooting". <es>fusilamiento</es> comes from <es>fusil</es>, "rifle".
    You will see this <es>X de Y</es> pattern more than thirty times in the paragraph.</p>"""),
  ],
  pron=[
    ("Five vowels, five sounds", """<p>Each vowel has one short, clean sound. It never slides into another vowel and never weakens to "uh".</p>
    <ul><li><b>a</b> as in f<b>a</b>ther: <es>años</es>, <es>casa</es></li>
    <li><b>e</b> as in b<b>e</b>t: <es>frente</es>, <es>de</es></li>
    <li><b>i</b> as in mach<b>i</b>ne: <es>fusilamiento</es></li>
    <li><b>o</b> as in m<b>o</b>re, cut short: <es>muchos</es>, <es>pelotón</es></li>
    <li><b>u</b> as in r<b>u</b>le: <es>muchos</es>, <es>fusilamiento</es></li></ul>
    <p>English speakers tend to say "MOO-chose" and "duh". Aim for <rs>MOO-chos</rs> and <rs>deh</rs>.</p>"""),
    ("Where the stress falls", """<ol><li>If a word ends in a <b>vowel, n or s</b>, stress the <b>second-to-last</b> syllable:
    <es>muchos</es> <rs>MU-chos</rs>, <es>años</es> <rs>A-ños</rs>, <es>frente</es> <rs>FREN-te</rs>, <es>fusilamiento</es> <rs>fu-si-la-MIEN-to</rs>.</li>
    <li>If it ends in <b>any other consonant</b>, stress the <b>last</b> syllable: <es>coronel</es> <rs>co-ro-NEL</rs>, <es>recordar</es> <rs>re-cor-DAR</rs>.</li>
    <li>A <b>written accent</b> overrides both rules and simply marks the stressed vowel: <es>después</es> <rs>des-PUÉS</rs>, <es>pelotón</es> <rs>pe-lo-TÓN</rs>.</li></ol>
    <p>The vocabulary reference shows every word split into syllables with the stressed one in capitals, so you never have to guess.</p>"""),
    ("Two vowels that share a syllable", """<p>When <b>i</b> or <b>u</b> sits next to another vowel, the two glide together in one syllable:
    <es>después</es> is two syllables (<rs>des-PWES</rs>), and <es>fusilamiento</es> has five (<rs>foo-see-la-MYEN-to</rs>), not six.</p>"""),
    ("<b>ñ</b> and <b>ch</b>", """<p><b>ñ</b> is the "ny" of canyon: <es>años</es> <rs>A-nyos</rs>. Take care with this one: it is a different letter from n.
    <b>ch</b> is always the "ch" of church: <es>muchos</es>.</p>"""),
  ],
  exercises=[
    ("Which syllable is stressed in <es>pelotón</es>, and how do you know?", "The last: <rs>pe-lo-TÓN</rs>. The written accent marks it. Without the accent, a word ending in -n would be stressed on the second-to-last syllable."),
    ("Which syllable is stressed in <es>fusilamiento</es>? There is no accent mark to help.", "<rs>fu-si-la-MIEN-to</rs>. It ends in a vowel, so the stress falls on the second-to-last syllable; <b>ie</b> glides together as one syllable."),
    ("Which two words are hidden inside <es>al</es>?", "<es>a</es> (to, at) + <es>el</es> (the)."),
    ("Why is it <es>muchos años</es> and not <es>muchas años</es>?", "<es>año</es> is a masculine noun, so the adjective takes the masculine plural ending -os."),
    ("Put into English: <es>frente al pelotón de fusilamiento</es>.", "Facing the firing squad."),
    ("Say \"many years later\" in Spanish without looking.", "<es>Muchos años después</es>."),
  ],
  review_html="""<p>Nothing to review yet. Instead, read the five vowels aloud three times, <es>a, e, i, o, u</es>, keeping each one short and pure.</p>""",
  memo="""<p><b>Back-chaining.</b> Long phrases are easiest to learn from the end. Say each line five times, then add the piece in front of it:</p>
  <ol><li><es>fusilamiento</es></li><li><es>de fusilamiento</es></li><li><es>pelotón de fusilamiento</es></li>
  <li><es>frente al pelotón de fusilamiento</es></li><li><es>Muchos años después, frente al pelotón de fusilamiento</es></li></ol>
  <p>Then cover the screen and say the whole line twice from memory.</p>""",
),

# ------------------------------------------------------------------ 2
dict(
  title="The consonants, and the whole first sentence",
  kind="lesson", new=[1], review=[],
  objectives=[
    "Pronounce the consonants that differ from English: silent h, ll, b and v, r and rr, c, qu.",
    "Understand every word of sentence 1, including <es>había de recordar</es> and <es>lo llevó</es>.",
    "Read sentence 1 aloud in four breath groups and recite it from memory.",
  ],
  intro="""<p>The first sentence is one of the most famous in any language. It looks forward to an execution and back to a childhood afternoon
  in a single breath. Today you finish it.</p>""",
  grammar=[
    ("<es>había de recordar</es>: \"was to remember\"", """<p><es>haber de</es> + an infinitive is a slightly solemn way of saying that something is bound to happen.
    <es>había</es> is a past form of <es>haber</es>, so <es>había de recordar</es> means "was to remember", "would one day remember".
    The narrator already knows the colonel's future. The infinitive, the dictionary form of a verb, always ends in <b>-ar</b>, <b>-er</b> or <b>-ir</b>:
    <es>recordar</es>, <es>conocer</es>.</p>"""),
    ("<es>aquella tarde remota</es>", """<p>Spanish has a special word for "that" when the thing is far away in space or time: <es>aquel</es> (masculine), <es>aquella</es> (feminine).
    <es>tarde</es> (afternoon) is feminine, so both words around it take feminine forms: <es>aquella tarde remota</es>.
    Notice that the describing word <es>remota</es> comes <b>after</b> the noun. That is the normal position in Spanish.</p>"""),
    ("<es>en que</es>", """<p>Literally "in which". After a time word it does the job of English "when": <es>aquella tarde en que...</es>, "that afternoon when...".</p>"""),
    ("<es>lo llevó</es>: the pronoun goes first", """<p><es>llevó</es> means "he took". The ending <b>-ó</b> marks a single completed action in the past by he, she or it.
    Spanish usually leaves out the word "he": the verb ending says it. <es>lo</es> means "him", and it stands <b>before</b> the verb:
    <es>su padre lo llevó</es>, "his father him took".</p>"""),
    ("<es>a conocer el hielo</es>", """<p><es>conocer</es> is "to become acquainted with". <es>llevar a alguien a conocer</es> something is to take someone to see it for the first time.
    Spanish says <es>el hielo</es>, "the ice", where English says just "ice".</p>"""),
  ],
  pron=[
    ("<b>h</b> is always silent", """<p><es>había</es> is <rs>a-BEE-a</rs>, <es>hielo</es> is <rs>YEH-lo</rs>. Never breathe an English h.</p>"""),
    ("<b>ll</b> sounds like English y", """<p><es>aquella</es> <rs>a-KEH-ya</rs>, <es>llevó</es> <rs>yeh-BO</rs>.</p>"""),
    ("<b>b</b> and <b>v</b> are the same sound", """<p>Both are a soft b. <es>llevó</es> has a b-sound in the middle, and <es>había</es> the same one.</p>"""),
    ("<b>r</b> and <b>rr</b>", """<p>A single <b>r</b> inside a word is one quick tap of the tongue, like the middle sound of American "butter": <es>coronel</es>, <es>padre</es>, <es>tarde</es>.
    At the <b>start</b> of a word, and whenever it is written <b>rr</b>, it is rolled: <es>recordar</es>, <es>remota</es>.
    If you cannot roll it yet, use a firm tap and keep going. It will come.</p>"""),
    ("<b>c</b> and <b>qu</b>", """<p><b>c</b> is k before a, o, u or a consonant: <es>coronel</es>, <es>recordar</es>. Before e or i it is s in Latin America and th (as in "think") in most of Spain:
    <es>conocer</es> is <rs>ko-no-SER</rs> or <rs>ko-no-THER</rs>. Listen to which one the narrator uses and copy it.
    <b>qu</b> is always a plain k, with the u silent: <es>que</es> <rs>keh</rs>, <es>aquella</es>.</p>"""),
    ("<b>-ía</b> is two syllables", """<p>The accent on the í keeps it apart from the a: <es>había</es> <rs>a-BEE-a</rs>, <es>Buendía</es> <rs>bwen-DEE-a</rs>.</p>"""),
  ],
  exercises=[
    ("Who took whom to see the ice?", "His father took him, the future colonel: <es>su padre lo llevó</es>. <es>lo</es> = him."),
    ("What does <es>había de recordar</es> mean, and what would plain \"remembered\" lose?", "\"Was to remember.\" It tells you the remembering lies in the future of the story, as fate."),
    ("Why <es>aquella</es> and <es>remota</es>, both ending in -a?", "They agree with <es>tarde</es>, a feminine noun."),
    ("Which letter is silent in <es>hielo</es> and <es>había</es>?", "The h."),
    ("How many syllables in <es>Buendía</es>, and which is stressed?", "Three: <rs>Buen-DÍ-a</rs>, stress on dí."),
    ("Translate: <es>su padre lo llevó a conocer el hielo</es>.", "His father took him to see (to discover) ice."),
  ],
  review_html="""<p>Start by saying yesterday's two phrases from memory. Then name the stress rule that explains each of these:
  <es>coronel</es>, <es>remota</es>, <es>después</es>.</p>""",
  memo="""<p><b>Four breath groups.</b> The narrator pauses after <es>después</es> and after <es>fusilamiento</es>. Learn the sentence in four pieces, then join them:</p>
  <ol><li><es>Muchos años después,</es></li><li><es>frente al pelotón de fusilamiento,</es></li>
  <li><es>el coronel Aureliano Buendía había de recordar</es></li><li><es>aquella tarde remota en que su padre lo llevó a conocer el hielo.</es></li></ol>
  <p>Use the practice box below. Move up one level each time you get through without a mistake.</p>""",
),

# ------------------------------------------------------------------ 3
dict(
  title="Macondo: a village by a river",
  kind="lesson", new=[2], review=[1],
  objectives=[
    "Understand sentence 2 and its chain of <es>de</es> phrases.",
    "Recognise <es>era</es> and the <b>-aban</b> ending as the tense used for description in the past.",
    "Make adjectives agree with nouns, and link words together smoothly when reading aloud.",
  ],
  intro="""<p>Sentence 2 is a slow camera shot: the village, the houses, the river, the stones. Nothing happens; everything is described.
  Spanish has a past tense made for exactly that.</p>""",
  grammar=[
    ("<es>era</es>: the describing past", """<p><es>era</es> means "was". It is the <b>imperfect</b> of <es>ser</es> (to be), the tense for how things were, with no beginning or end in view.
    Compare <es>llevó</es> in sentence 1, a single finished event. The whole paragraph moves between these two past tenses:
    imperfect for background and habits, <b>preterite</b> for events.</p>"""),
    ("<es>se precipitaban</es>", """<p>The ending <b>-aban</b> is the imperfect for "they" of an -ar verb: the waters <em>were rushing</em>, <em>used to rush</em>.
    The little word <es>se</es> goes with certain verbs to show the subject is acting on itself: <es>precipitarse</es>, to hurl oneself down.</p>"""),
    ("<es>de</es> for material and belonging", """<p><es>casas de barro y cañabrava</es>: houses <em>made of</em> mud and wild cane. <es>un río de aguas diáfanas</es>: a river <em>with</em> clear waters.
    <es>un lecho de piedras</es>: a bed <em>of</em> stones. English uses three different constructions; Spanish uses <es>de</es> for all of them.</p>"""),
    ("Adjectives follow the noun and copy its ending", """<p><es>casas ... construidas</es>, <es>aguas diáfanas</es>, <es>piedras pulidas, blancas y enormes</es>: all feminine plural, so the adjectives end in <b>-as</b>
    (or <b>-es</b> for adjectives like <es>enorme</es> that have one form for both genders). <es>huevos prehistóricos</es> is masculine plural: <b>-os</b>.
    <es>construidas</es> and <es>pulidas</es> are past participles (built, polished) doing the job of adjectives.</p>"""),
    ("<es>que</es> and <es>como</es>", """<p><es>que</es> after a noun means "that" or "which": <es>aguas ... que se precipitaban</es>, waters that rushed down. <es>como</es> means "like": <es>como huevos prehistóricos</es>.</p>"""),
  ],
  pron=[
    ("Linking words", """<p>Spanish is spoken in unbroken chains. When one word ends in a vowel and the next begins with one, they flow together with no gap:
    <es>una aldea</es> sounds like <rs>u-nal-DE-a</rs>, <es>de aguas</es> like <rs>DEA-gwas</rs>, <es>la orilla</es> like <rs>lao-REE-ya</rs>.
    Do not stop between words the way careful English does.</p>"""),
    ("New letter sounds in this sentence", """<ul><li><b>gu</b> + a is "gw": <es>aguas</es> <rs>A-gwas</rs>.</li>
    <li><b>hu</b> + vowel is "w": <es>huevos</es> <rs>WEH-bos</rs> (silent h, v like b).</li>
    <li><b>rr</b> rolled: <es>barro</es>. Initial r rolled: <es>río</es> <rs>RREE-o</rs>, two syllables.</li>
    <li><b>ñ</b>: <es>cañabrava</es> <rs>ka-nya-BRA-ba</rs>.</li>
    <li><b>ei</b> glides: <es>veinte</es> <rs>BEYN-te</rs>.</li>
    <li><es>prehistóricos</es>: the h is silent, so <rs>pre-is-TO-ri-kos</rs>.</li>
    <li><es>diáfanas</es>: stress on the accented á, <rs>DYA-fa-nas</rs>.</li></ul>"""),
  ],
  exercises=[
    ("How many houses did Macondo have, and what were they made of?", "Twenty (<es>veinte casas</es>), of mud and wild cane (<es>de barro y cañabrava</es>)."),
    ("What does <es>construidas</es> agree with?", "<es>casas</es>: feminine plural."),
    ("Three adjectives describe the stones. Which?", "<es>pulidas</es> (polished), <es>blancas</es> (white), <es>enormes</es> (enormous)."),
    ("Why <es>era</es> here but <es>llevó</es> in sentence 1?", "<es>era</es> describes a lasting state (imperfect); <es>llevó</es> reports one completed event (preterite)."),
    ("Translate: <es>a la orilla de un río</es>.", "On the bank of a river."),
    ("What does <es>como</es> mean in <es>como huevos prehistóricos</es>?", "Like."),
  ],
  review_html="""<p>Play sentence 1, then recite it from memory before you start. If you needed more than two peeks, repeat yesterday's four breath groups once.</p>""",
  memo="""<p><b>Follow the camera.</b> The sentence zooms in step by step. Fix the order of the images and the words will follow:
  village → houses → mud and cane → riverbank → clear water → rushing → bed of stones → white, enormous → eggs.</p>
  <p>Draw the nine images as a quick sketch on paper, then say the sentence while pointing at each one.</p>""",
),

# ------------------------------------------------------------------ 4
dict(
  title="A world without names",
  kind="lesson", new=[3], review=[1, 2],
  objectives=[
    "Understand sentence 3 and the pattern <es>tan ... que</es> (so ... that).",
    "Recognise object pronouns attached to the end of an infinitive: <es>mencionarlas</es>, <es>señalarlas</es>.",
    "Tell apart <es>había de</es> (was to) and <es>había que</es> (it was necessary to).",
  ],
  intro="""<p>A short sentence with a big idea: the world is so new that things have no names yet. It is also a compact lesson in how Spanish
  hooks pronouns onto verbs.</p>""",
  grammar=[
    ("<es>tan reciente, que...</es>", """<p><es>tan</es> + adjective + <es>que</es> is "so ... that": <es>El mundo era tan reciente, que muchas cosas carecían de nombre</es>.</p>"""),
    ("<es>carecían de nombre</es>", """<p><es>carecer de</es> means "to lack". The verb always brings <es>de</es> with it, and no article is needed: <es>carecían de nombre</es>, "lacked a name".
    The ending <b>-ían</b> is the imperfect "they" form of -er and -ir verbs, the partner of <b>-aban</b> for -ar verbs.</p>
    <table class="mini"><tr><th></th><th>-ar verbs</th><th>-er / -ir verbs</th></tr>
    <tr><td>he, she, it</td><td>-aba: <es>plantaba</es></td><td>-ía: <es>había</es>, <es>tenía</es></td></tr>
    <tr><td>they</td><td>-aban: <es>precipitaban</es></td><td>-ían: <es>carecían</es></td></tr></table>"""),
    ("<es>para</es> + infinitive", """<p><es>para</es> before an infinitive means "in order to": <es>para mencionarlas</es>, "in order to mention them".</p>"""),
    ("Pronouns glued to the infinitive", """<p><es>las</es> here means "them", standing for <es>las cosas</es> (feminine plural). With an infinitive, the pronoun is attached to the end
    and written as one word: <es>mencionar</es> + <es>las</es> → <es>mencionarlas</es>; <es>señalar</es> + <es>las</es> → <es>señalarlas</es>.
    With a conjugated verb it goes in front instead, as in <es>lo llevó</es>.</p>"""),
    ("<es>había que</es>", """<p><es>haber que</es> + infinitive expresses a need with no particular person in mind: <es>había que señalarlas</es>, "one had to point at them".
    Do not confuse it with <es>había de recordar</es> in sentence 1: <es>de</es> points to destiny, <es>que</es> to necessity.</p>"""),
    ("<es>con el dedo</es>", """<p>With parts of the body Spanish says "the", not "my" or "one's": <es>con el dedo</es>, "with the finger".</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>reciente</es>: rolled initial r; c before i is s (or th): <rs>rre-SYEN-te</rs>.</li>
    <li><es>carecían</es>: four syllables, <rs>ka-re-SEE-an</rs>.</li>
    <li><es>señalarlas</es>: ñ again, <rs>se-nya-LAR-las</rs>.</li>
    <li><es>dedo</es>: a d between vowels is very soft, almost the th of "this": <rs>DEH-tho</rs>.</li>
    <li><es>había que</es>: <rs>a-BEE-a ke</rs>.</li></ul>"""),
    ("The comma is a breath", """<p>The narrator pauses after <es>reciente</es>. Use that pause; then take <es>y para mencionarlas había que señalarlas con el dedo</es> in one flowing breath.</p>"""),
  ],
  exercises=[
    ("Why did people have to point at things?", "Because many things lacked a name: <es>muchas cosas carecían de nombre</es>."),
    ("What does <es>las</es> in <es>mencionarlas</es> stand for?", "<es>las cosas</es>, the things."),
    ("Translate <es>había que señalarlas</es>.", "It was necessary to point at them; one had to point at them."),
    ("<es>había de</es> or <es>había que</es>: which one speaks of necessity?", "<es>había que</es>."),
    ("Give the infinitive of <es>carecían</es>, and the small word it always takes.", "<es>carecer</es>, followed by <es>de</es>."),
    ("Say \"so recent that\" in Spanish.", "<es>tan reciente que</es>."),
  ],
  review_html="""<p>Recite sentence 1, then sentence 2 with your sketch from Lesson 3. Find the two imperfect verbs in sentence 2 (<es>era</es>, <es>se precipitaban</es>).</p>""",
  memo="""<p><b>Cause, then two matching verbs.</b> The sentence is a small argument: so recent → no names → to mention → to point.
  The last two verbs rhyme, <es>mencionarlas</es> and <es>señalarlas</es>, and they come in logical order: first what you want to do, then how you must do it.</p>
  <p>Say the sentence while actually pointing at something with your finger on <es>con el dedo</es>. Gestures make a strong memory hook.</p>""",
),

# ------------------------------------------------------------------ 5
dict(
  title="The gypsies arrive, and the magnet",
  kind="lesson", new=[4, 5], review=[1, 2, 3],
  objectives=[
    "Understand sentences 4 and 5.",
    "See how the imperfect expresses a habit (every year) and the preterite a single event (first they brought...).",
    "Pronounce g before i, and z.",
  ],
  intro="""<p>Sentence 4 describes a yearly ritual; sentence 5, only four words long, is the first real event of the story after the opening.
  Listen for the change of tense between them.</p>""",
  grammar=[
    ("<es>Todos los años</es>, <es>por el mes de marzo</es>", """<p><es>todos los</es> + plural noun means "every": <es>todos los años</es>, "every year". <es>por</es> with a time is deliberately loose,
    "around": <es>por el mes de marzo</es>, "around the month of March". Months take no capital letter in Spanish.</p>"""),
    ("Habit: <es>plantaba</es>, <es>daban</es>", """<p>Both verbs are imperfect, because this happened year after year: <es>plantaba su carpa</es>, "would pitch its tent".
    The subject is <es>una familia</es>, singular, so the verb is singular (<b>-aba</b>). By the end of the sentence the writer is thinking of the gypsies themselves,
    and the verb slips into the plural: <es>daban</es>, "they gave".</p>"""),
    ("<es>daban a conocer</es>", """<p>An idiom: <es>dar a conocer</es>, literally "to give to know", means to make something known, to present it.
    You already know <es>conocer</es> from <es>conocer el hielo</es>.</p>"""),
    ("<es>un grande alboroto</es>", """<p>Before a singular noun <es>grande</es> normally shortens to <es>gran</es>. Keeping the full form is an old-fashioned,
    storyteller's touch. Before a noun it means "great" rather than physically "big".</p>"""),
    ("Event: <es>Primero llevaron el imán</es>", """<p><es>llevaron</es> is the preterite "they" form of <es>llevar</es>, the same verb as <es>llevó</es> in sentence 1. Here it means "brought".
    The ending <b>-aron</b> (they, one completed action) contrasts with <b>-aban</b> (they, ongoing or habitual).</p>
    <table class="mini"><tr><th>llevar</th><th>one event (preterite)</th><th>habit or background (imperfect)</th></tr>
    <tr><td>he / she</td><td><es>llevó</es></td><td><es>llevaba</es></td></tr>
    <tr><td>they</td><td><es>llevaron</es></td><td><es>llevaban</es></td></tr></table>"""),
  ],
  pron=[
    ("<b>g</b> before e or i", """<p>Before e or i, <b>g</b> is a strong, breathy h made at the back of the mouth: <es>gitanos</es> <rs>hee-TA-nos</rs>.
    Before a, o, u it is the hard g of "go": <es>grande</es>, <es>gorrión</es>.</p>"""),
    ("<b>z</b>", """<p>Never the buzzing English z. It is s in Latin America and th in Spain: <es>marzo</es> <rs>MAR-so</rs>.</p>"""),
    ("Other points", """<ul><li><es>desarrapados</es>: rolled rr, six syllables, <rs>de-sa-rra-PA-dos</rs>.</li>
    <li><es>familia</es>: three syllables, <rs>fa-MEE-lya</rs>.</li>
    <li><es>nuevos inventos</es>: both v's sound like b, <rs>NWEH-bos een-BEN-tos</rs>.</li>
    <li><es>imán</es>: stress on the accented last syllable, <rs>ee-MAN</rs>.</li>
    <li><es>y con un grande alboroto</es>: link <es>grande alboroto</es> into one chain.</li></ul>"""),
  ],
  exercises=[
    ("When did the gypsies come, and how often?", "Every year, around the month of March: <es>todos los años, por el mes de marzo</es>."),
    ("What instruments announced them?", "<es>pitos y timbales</es>: whistles (pipes) and kettledrums."),
    ("Why <es>plantaba</es> (imperfect) but <es>llevaron</es> (preterite)?", "Pitching the tent was a yearly habit; bringing the magnet was one particular event."),
    ("What does <es>daban a conocer</es> mean?", "They made known, they presented (the new inventions)."),
    ("What is <es>el imán</es>?", "The magnet."),
    ("Say sentence 5 from memory.", "<es>Primero llevaron el imán.</es>"),
  ],
  review_html="""<p>Recite sentences 1 to 3 in a row. Then answer without looking: what is the difference between <es>había de</es> and <es>había que</es>?</p>""",
  memo="""<p><b>When, who, what, how, why.</b> Sentence 4 answers five questions in order:
  when (<es>Todos los años, por el mes de marzo</es>), who (<es>una familia de gitanos desarrapados</es>), what (<es>plantaba su carpa cerca de la aldea</es>),
  how (<es>con un grande alboroto de pitos y timbales</es>), why (<es>daban a conocer los nuevos inventos</es>).</p>
  <p>Ask yourself each question aloud in English and answer in Spanish. Then add sentence 5 as the punchline.</p>""",
),

# ------------------------------------------------------------------ 6
dict(
  title="Checkpoint 1: sentences 1 to 5, with rhythm",
  kind="review", new=[], review=[1, 2, 3, 4, 5],
  objectives=[
    "Read sentences 1 to 5 aloud as one continuous passage, pausing where the narrator pauses.",
    "Explain the difference between the two past tenses met so far.",
    "Recite sentences 1 to 5 from memory with no more than a few prompts.",
  ],
  intro="""<p>No new text today. You now hold the opening movement of the paragraph: the memory, the village, the nameless world, the gypsies, the magnet.
  This lesson makes it secure before the long sentences begin.</p>""",
  grammar=[
    ("The two past tenses so far", """<table class="mini"><tr><th>Imperfect: background, description, habit</th><th>Preterite: single completed events</th></tr>
    <tr><td><es>había de recordar</es>, <es>era</es> (twice), <es>se precipitaban</es>, <es>carecían</es>, <es>había que</es>, <es>plantaba</es>, <es>daban</es></td>
    <td><es>llevó</es>, <es>llevaron</es></td></tr></table>
    <p>Eight imperfects and two preterites: the opening is nearly all scenery. From sentence 6 on, the preterite takes over as things start to happen.</p>"""),
    ("Small words you now know", """<p><es>de</es> (of), <es>a</es> (to), <es>en</es> (in), <es>por</es> (along, around), <es>para</es> (in order to), <es>con</es> (with),
    <es>y</es> (and), <es>que</es> (that), <es>como</es> (like); the articles <es>el, la, los, las, un, una</es>; and the contraction <es>al</es>.
    These few words make up over a third of the whole paragraph.</p>"""),
    ("Agreement at a glance", """<p><es>muchos años</es> · <es>aquella tarde remota</es> · <es>aguas diáfanas</es> · <es>piedras pulidas, blancas y enormes</es> ·
    <es>huevos prehistóricos</es> · <es>muchas cosas</es> · <es>gitanos desarrapados</es> · <es>los nuevos inventos</es>. In each pair, check that you can say why the endings match.</p>"""),
  ],
  pron=[
    ("Even syllables", """<p>English stretches stressed syllables and swallows the rest. Spanish gives every syllable nearly the same length, like steady taps on a table,
    with the stressed one only a little louder. Tap a finger for each syllable of <es>Ma-con-do e-ra en-ton-ces u-na al-de-a</es> and keep the taps even.</p>"""),
    ("Breath groups", """<p>Play the five sentences and notice where the narrator pauses: after <es>después</es>, after <es>fusilamiento</es>, after <es>pulidas</es>,
    after <es>reciente</es>, after <es>marzo</es>, after <es>aldea</es>. Inside each group the words run together without a break. Mark those pauses in your mind and breathe only there.</p>"""),
    ("Shadowing", """<p>Set the speed to 0.75× and speak along with the recording, a fraction of a second behind the narrator, like an echo.
    Do not stop to fix mistakes. Three passes of shadowing do more for rhythm than ten careful solo readings.</p>"""),
  ],
  exercises=[
    ("Translate without looking: <es>aquella tarde remota</es>.", "That distant afternoon."),
    ("Which sentence has no imperfect verb at all?", "Sentence 5: <es>Primero llevaron el imán</es>."),
    ("Give the Spanish for: village, river, stones, things, finger, year, magnet.", "<es>aldea, río, piedras, cosas, dedo, año, imán</es>."),
    ("Where is the stress in <es>entonces</es>, <es>alboroto</es>, <es>timbales</es>?", "<rs>en-TON-ces</rs>, <rs>al-bo-RO-to</rs>, <rs>tim-BA-les</rs>: each ends in a vowel or s, so second-to-last."),
    ("In <es>lo llevó</es>, who is <es>lo</es>?", "Him: the boy who will become Colonel Aureliano Buendía."),
    ("What are the first two words of each of sentences 1 to 5?", "<es>Muchos años</es> · <es>Macondo era</es> · <es>El mundo</es> · <es>Todos los</es> · <es>Primero llevaron</es>."),
  ],
  review_html="""<p>Work through the five sentences one at a time: play, shadow at 0.75×, then read alone at full speed. Tick each sentence only when you can read it without stumbling.</p>""",
  memo="""<p><b>Cue chain.</b> Memorise the five openers as a list: <es>Muchos años</es> → <es>Macondo era</es> → <es>El mundo</es> → <es>Todos los</es> → <es>Primero</es>.
  When you recite, each opener is the handle that pulls out its sentence. Then use the practice box: aim to finish level 3 (three words in four hidden) today.</p>""",
),

# ------------------------------------------------------------------ 7
dict(
  title="Enter Melquíades",
  kind="lesson", new=[6], review=[4, 5],
  objectives=[
    "Understand sentence 6, with its two descriptive asides before the main verb.",
    "Recognise three irregular or reflexive preterites: <es>se presentó</es>, <es>hizo</es>, and the imperfect <es>llamaba</es>.",
    "Use <es>lo que</es> (what) and <es>él mismo</es> (he himself).",
  ],
  intro="""<p>The main statement of this sentence is simple: <es>Un gitano ... hizo una ... demostración</es>, "a gypsy put on a demonstration".
  Everything else is decoration hung on that frame. Find the frame first and the long sentence becomes easy.</p>""",
  grammar=[
    ("The frame and its asides", """<p><es>Un gitano corpulento</es> | <em>aside 1:</em> <es>de barba montaraz y manos de gorrión</es> | <em>aside 2:</em> <es>que se presentó con el nombre de Melquíades</es> |
    <es>hizo una truculenta demostración pública</es> | <es>de lo que él mismo llamaba la octava maravilla...</es></p>
    <p>The commas in the text mark the asides exactly.</p>"""),
    ("Describing people with <es>de</es>", """<p><es>de barba montaraz y manos de gorrión</es>: "of wild beard and sparrow hands". Spanish describes a person's features with <es>de</es> where English uses "with".
    <es>mano</es> is feminine even though it ends in -o.</p>"""),
    ("<es>se presentó</es>", """<p><es>presentar</es> is "to introduce"; with <es>se</es> the action turns back on the doer: <es>se presentó</es>, "he introduced himself". The <b>-ó</b> ending is the preterite you met in <es>llevó</es>.</p>"""),
    ("<es>hizo</es>", """<p>The preterite of <es>hacer</es> (to do, to make), and irregular: <es>hizo</es>, "he made". <es>hacer una demostración</es> is to give or put on a demonstration.</p>"""),
    ("<es>truculenta</es>: a false friend", """<p>It does not mean "truculent". In Spanish it means lurid, sensational, calculated to shock. It stands <b>before</b> the noun here;
    an adjective placed in front carries the speaker's attitude rather than a plain fact. <es>pública</es>, the plain fact, comes after.</p>"""),
    ("<es>lo que él mismo llamaba</es>", """<p><es>lo que</es> means "what" in the sense of "the thing that". <es>él</es> with an accent is "he" (without the accent, <es>el</es> is "the").
    <es>mismo</es> after a pronoun adds "-self": <es>él mismo</es>, "he himself". <es>llamaba</es> is imperfect because it was his habitual name for it.</p>"""),
    ("<es>la octava maravilla</es>", """<p><es>octava</es> is "eighth", feminine to match <es>maravilla</es> (wonder). <es>los sabios alquimistas</es>: "the learned alchemists"; <es>alquimista</es> ends in -a but is masculine here.</p>"""),
  ],
  pron=[
    ("Names and hard words", """<ul><li><es>Melquíades</es>: four syllables, <rs>mel-KEE-a-des</rs>. The qu is k; the accent keeps í and a apart.</li>
    <li><es>gorrión</es>: hard g, rolled rr, <rs>go-RRYON</rs>.</li>
    <li><es>hizo</es>: silent h, z as s: <rs>EE-so</rs>.</li>
    <li><es>montaraz</es>: ends in z, so stress the last syllable: <rs>mon-ta-RAS</rs>.</li>
    <li><es>demostración pública</es>: <rs>de-mos-tra-SYON POO-bli-ka</rs>.</li>
    <li><es>llamaba</es>: <rs>ya-MA-ba</rs>.</li>
    <li><es>alquimistas</es>: <rs>al-kee-MEES-tas</rs>.</li></ul>"""),
    ("Reading the asides", """<p>Drop your voice slightly for the two asides and lift it again at <es>hizo</es>. That is how a listener hears which words form the main sentence.</p>"""),
  ],
  exercises=[
    ("What is the main verb of the sentence?", "<es>hizo</es>: a gypsy ... <em>made</em> (put on) a demonstration."),
    ("Describe Melquíades in English from the Spanish.", "Heavy-set (<es>corpulento</es>), with a wild beard (<es>barba montaraz</es>) and sparrow-like hands (<es>manos de gorrión</es>)."),
    ("What does <es>truculenta</es> mean here?", "Lurid, sensational; not \"truculent\"."),
    ("What is the difference between <es>el</es> and <es>él</es>?", "<es>el</es> = the; <es>él</es> = he."),
    ("Translate: <es>lo que él mismo llamaba</es>.", "What he himself called."),
    ("What did he call the magnets?", "<es>la octava maravilla de los sabios alquimistas de Macedonia</es>: the eighth wonder of the learned alchemists of Macedonia."),
  ],
  review_html="""<p>Recite sentences 4 and 5 so that they lead straight into today's sentence: the magnet arrives, and then the man who carries it.</p>""",
  memo="""<p><b>Frame first.</b> Learn the skeleton until it is automatic: <es>Un gitano corpulento ... hizo una truculenta demostración pública</es>.
  Then add one aside at a time: first the beard and hands, then the name, then the tail about the eighth wonder.</p>""",
),

# ------------------------------------------------------------------ 8
dict(
  title="The magnets at work (first half of the longest sentence)",
  kind="lesson", new=[7], part=(7, 1, 10), review=[5, 6],
  objectives=[
    "Understand the first half of sentence 7, up to <es>tratando de desenclavarse</es>.",
    "Recognise the gerund (<b>-ando</b>), <es>al</es> + infinitive, and <es>tratar de</es> + infinitive.",
    "Take long words apart into pieces you can pronounce and understand.",
  ],
  intro="""<p>Sentence 7 has 78 words, a fifth of the paragraph, so it gets two lessons. It is a list of four things that happen, each starting with <es>y</es> (and).
  Today: Melquíades walks, people panic, pots fall, wood creaks.</p>""",
  grammar=[
    ("<es>Fue de casa en casa</es>", """<p><es>fue</es> is the preterite of <es>ir</es> (to go): "he went". It is completely irregular and worth learning as a word on its own.
    <es>de casa en casa</es>, "from house to house", follows the pattern <es>de X en X</es>.</p>"""),
    ("The gerund: <es>arrastrando</es>", """<p>Replace -ar with <b>-ando</b> and you have the "-ing" form: <es>arrastrar</es> → <es>arrastrando</es>, "dragging";
    later <es>tratar</es> → <es>tratando</es>, "trying". It describes an action going on alongside the main one.</p>"""),
    ("<es>todo el mundo se espantó</es>", """<p><es>todo el mundo</es>, literally "all the world", is the everyday way to say "everybody", and it takes a singular verb.
    <es>espantarse</es> is to take fright: <es>se espantó</es>, "was terrified".</p>"""),
    ("<es>al ver que...</es>", """<p><es>al</es> + infinitive means "on doing" or "when ... did": <es>al ver</es>, "on seeing".</p>"""),
    ("A list with articles", """<p><es>los calderos, las pailas, las tenazas y los anafes</es>: every item keeps its own article, <es>los</es> for masculine plural and <es>las</es> for feminine plural.
    Four kitchen objects: cauldrons, pans, tongs, braziers. <es>paila</es> and <es>anafe</es> are regional, homely words.</p>"""),
    ("<es>se caían</es>, <es>crujían</es>", """<p>Both imperfect, because the falling and creaking go on and on as he walks. <es>caerse de</es> is to fall off or down from somewhere: <es>se caían de su sitio</es>, "were falling from their place".</p>"""),
    ("<es>por la desesperación de...</es>", """<p>Here <es>por</es> gives the cause: the timbers creaked <em>because of</em> the desperation of the nails and screws.</p>"""),
    ("<es>tratando de desenclavarse</es>", """<p><es>tratar de</es> + infinitive means "to try to". <es>desenclavarse</es> is built in layers:
    <b>des-</b> (un-) + <b>en-</b> + <b>clav</b> (from <es>clavo</es>, nail, which you have just read) + <b>-ar</b> + <b>-se</b> (themselves): "to un-nail themselves".</p>"""),
  ],
  pron=[
    ("<b>j</b>", """<p><b>j</b> is always the breathy h-sound you met in <es>gitanos</es>: <es>crujían</es> <rs>kroo-HEE-an</rs>.</p>"""),
    ("Stacked vowels", """<p><es>caían</es> is three syllables, <rs>ka-EE-an</rs>; <es>fue</es> is one, <rs>fweh</rs>. The accent mark on í is what splits the vowels apart.</p>"""),
    ("Long words: build from the end", """<p>Say <es>ción</es>, then <es>ra-ción</es>, <es>pe-ra-ción</es>, <es>ses-pe-ra-ción</es>, <es>de-ses-pe-ra-ción</es>. Do the same with
    <es>des-en-cla-var-se</es> and <es>a-rras-tran-do</es>. Each syllable gets equal time.</p>"""),
    ("Other points", """<ul><li><es>tornillos</es>: ll as y, <rs>tor-NEE-yos</rs>.</li><li><es>tenazas</es>: <rs>te-NA-sas</rs>.</li>
    <li><es>metálicos</es>: stress on the accented á.</li><li><es>espantó</es>: stress on the final ó.</li></ul>"""),
  ],
  exercises=[
    ("What was Melquíades dragging?", "<es>dos lingotes metálicos</es>: two metal ingots."),
    ("Name the four kitchen objects.", "<es>los calderos, las pailas, las tenazas y los anafes</es>: cauldrons, pans, tongs and braziers."),
    ("Why did the timbers creak?", "From the desperation of the nails and screws trying to pull themselves out: <es>por la desesperación de los clavos y los tornillos tratando de desenclavarse</es>."),
    ("Break <es>desenclavarse</es> into its parts.", "<b>des</b> (un-) + <b>en</b> + <b>clav</b> (nail) + <b>ar</b> (verb ending) + <b>se</b> (themselves)."),
    ("How do you say \"everybody\"?", "<es>todo el mundo</es>."),
    ("What form is <es>arrastrando</es>, and what is its English equivalent?", "The gerund; \"dragging\"."),
  ],
  review_html="""<p>Recite sentences 5 and 6. Then recall from sentence 6: what did Melquíades call the magnets?</p>""",
  memo="""<p><b>A walk through a house.</b> Picture Melquíades going from door to door, and place each clause in a room:
  the street (<es>Fue de casa en casa arrastrando dos lingotes metálicos</es>), the doorway (<es>y todo el mundo se espantó</es>),
  the kitchen (<es>los calderos, las pailas, las tenazas y los anafes se caían de su sitio</es>), the walls and roof (<es>las maderas crujían...</es>).</p>
  <p>The kitchen list alternates <es>los, las, las, los</es>. Notice the symmetry and it stops being hard.</p>""",
),

# ------------------------------------------------------------------ 9
dict(
  title="Lost things return (second half of sentence 7)",
  kind="lesson", new=[7], part=(7, 11, 15), review=[6, 7],
  objectives=[
    "Understand the second half of sentence 7 and join the two halves.",
    "Recognise <es>desde hacía mucho tiempo</es> and the impersonal <es>se les había buscado</es>.",
    "Read all 78 words of sentence 7 aloud with a breathing plan.",
  ],
  intro="""<p>The sentence ends with its strangest image: things lost long ago crawl out of hiding and follow the magnets through the street.</p>""",
  grammar=[
    ("<es>aun</es>", """<p>Without an accent, <es>aun</es> means "even": <es>y aun los objetos perdidos</es>, "and even the lost objects". (With an accent, <es>aún</es> means "still".)</p>"""),
    ("<es>los objetos perdidos</es>", """<p><es>perdidos</es> is the past participle of <es>perder</es> (to lose), used as an adjective and agreeing with <es>objetos</es>.
    Participles of -ar verbs end in <b>-ado</b> (<es>buscado</es>), those of -er and -ir verbs in <b>-ido</b> (<es>perdido</es>).</p>"""),
    ("<es>desde hacía mucho tiempo</es>", """<p>Literally "since it-made much time". Spanish measures elapsed time with <es>hacer</es>: the objects had been lost <em>for a long time</em>. Learn it as one block.</p>"""),
    ("<es>por donde más se les había buscado</es>", """<p>The hardest phrase in the paragraph, so take it slowly:</p>
    <ul><li><es>por donde</es>: "around where", "in the places where";</li><li><es>más</es>: "most";</li>
    <li><es>se ... había buscado</es>: <es>había buscado</es> is "had searched", and <es>se</es> makes it impersonal, "one had searched";</li>
    <li><es>les</es>: "for them", the lost objects.</li></ul>
    <p>All together: "in the very places where people had searched for them most".</p>"""),
    ("<es>se arrastraban en desbandada turbulenta</es>", """<p><es>arrastrar</es> was "to drag" in the first half. With <es>se</es> it becomes "to drag oneself along, to crawl".
    <es>en desbandada</es> is "in a rout", like a crowd scattering.</p>"""),
    ("<es>detrás de los fierros mágicos</es>", """<p><es>detrás de</es>, "behind". <es>fierros</es> is a Latin American form of <es>hierros</es>, "irons". The same two bars are called <es>lingotes metálicos</es> at the start of the sentence
    and <es>fierros mágicos</es> at the end: from the metalworker's word to the villagers' word.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>aun</es>: one syllable, <rs>awn</rs>.</li><li><es>objetos</es>: j as h, <rs>ob-HEH-tos</rs>.</li>
    <li><es>hacía</es>: silent h, three syllables, <rs>a-SEE-a</rs>.</li><li><es>mágicos</es>: g before i as h, <rs>MA-hee-kos</rs>.</li>
    <li><es>fierros</es>: rolled rr, <rs>FYEH-rros</rs>.</li><li><es>detrás</es>: stress on the last syllable.</li></ul>"""),
    ("A breathing plan for all of sentence 7", """<p>The narrator pauses at the commas. Five breaths are enough:</p>
    <ol><li><es>Fue de casa en casa arrastrando dos lingotes metálicos,</es></li>
    <li><es>y todo el mundo se espantó al ver que los calderos, las pailas, las tenazas y los anafes se caían de su sitio,</es></li>
    <li><es>y las maderas crujían por la desesperación de los clavos y los tornillos tratando de desenclavarse,</es></li>
    <li><es>y aun los objetos perdidos desde hacía mucho tiempo aparecían por donde más se les había buscado,</es></li>
    <li><es>y se arrastraban en desbandada turbulenta detrás de los fierros mágicos de Melquíades.</es></li></ol>"""),
  ],
  exercises=[
    ("What does <es>aun</es> mean here?", "Even."),
    ("Where did the lost objects turn up?", "In the very places where they had been searched for most: <es>por donde más se les había buscado</es>."),
    ("Translate: <es>desde hacía mucho tiempo</es>.", "For a long time."),
    ("How does <es>se</es> change <es>arrastraban</es>?", "<es>arrastraban</es> = they dragged (something); <es>se arrastraban</es> = they dragged themselves along."),
    ("Which two expressions name the ingots in this sentence?", "<es>dos lingotes metálicos</es> and <es>los fierros mágicos de Melquíades</es>."),
    ("Four clauses of the sentence begin with the same word. Which?", "<es>y</es> (and): <es>y todo el mundo... y las maderas... y aun los objetos... y se arrastraban...</es>"),
  ],
  review_html="""<p>Say the first half of sentence 7 from memory (your walk through the house), then go straight on into today's half.</p>""",
  memo="""<p><b>Four times <es>y</es>.</b> After the opening clause, the sentence is four "ands": people (<es>y todo el mundo</es>), wood (<es>y las maderas</es>),
  lost things (<es>y aun los objetos perdidos</es>), the procession (<es>y se arrastraban</es>). Count them on four fingers as you recite.</p>
  <p>Practise the five breath groups separately, then two at a time, then all five.</p>""",
),

# ------------------------------------------------------------------ 10
dict(
  title="\"Things have a life of their own\", and Checkpoint 2",
  kind="lesson", new=[8], review=[6, 7],
  objectives=[
    "Understand sentence 8, the first words spoken aloud in the novel.",
    "Recognise the present tense (<es>tienen</es>, <es>es</es>) and Spanish quotation marks and dashes.",
    "Recite sentences 6 to 8 together.",
  ],
  intro="""<p>Melquíades speaks. Because it is direct speech the verbs jump into the present tense, the only present-tense verbs you have met so far.</p>""",
  grammar=[
    ("Quotation marks and dashes", """<p>Spanish books use angle quotes, <b>« »</b>, for speech. A remark by the narrator inside the speech is set off with long dashes:
    <es>—pregonaba el gitano con áspero acento—</es>. The quotation simply continues after the second dash.</p>"""),
    ("<es>Las cosas tienen vida propia</es>", """<p><es>tienen</es> is "they have", present tense of <es>tener</es>. <es>propia</es> after a noun means "of one's own": <es>vida propia</es>, "a life of their own".
    Note <es>Las cosas</es>: Spanish uses the article when speaking of things in general.</p>"""),
    ("<es>pregonaba el gitano</es>", """<p><es>pregonar</es> is what a town crier does: to proclaim in the street. The subject comes <b>after</b> the verb, which is usual with verbs of saying.
    <es>con áspero acento</es>: "with a harsh accent"; again the adjective in front, for colour.</p>"""),
    ("<es>todo es cuestión de...</es>", """<p><es>es</es> is "is" (present of <es>ser</es>; <es>era</es> was its imperfect). <es>ser cuestión de</es> + infinitive: "to be a matter of doing".</p>"""),
    ("<es>despertarles el ánima</es>", """<p>Literally "to wake to-them the soul". Where English says "their soul", Spanish often uses a pronoun for the owner (<es>les</es>, "to them") and a plain article for the thing.
    <es>les</es> is attached to the infinitive, like <es>las</es> in <es>mencionarlas</es>.</p>
    <p><es>ánima</es> is feminine, but feminine nouns that begin with a stressed <b>a</b> take <es>el</es> in the singular to avoid the clash of two a's: <es>el ánima</es>, <es>el agua</es>.</p>"""),
  ],
  pron=[
    ("Sounds to watch", """<ul><li><es>tienen</es>: two syllables, <rs>TYEH-nen</rs>.</li><li><es>propia</es>: two syllables, <rs>PRO-pya</rs>.</li>
    <li><es>áspero acento</es>: stress the first syllable of <es>áspero</es> and link the two words, <rs>AS-pe-roa-SEN-to</rs>.</li>
    <li><es>cuestión</es>: <rs>kwes-TYON</rs>.</li><li><es>ánima</es>: stress on the first syllable, <rs>A-ni-ma</rs>.</li></ul>"""),
    ("Give it a voice", """<p>This is a street performer selling a marvel. Say the quoted words more loudly and slowly than the narrator's aside, and drop your voice for
    <es>pregonaba el gitano con áspero acento</es>.</p>"""),
  ],
  exercises=[
    ("What does Melquíades claim about things?", "That they have a life of their own, <es>tienen vida propia</es>, and that it is all a matter of waking up their souls."),
    ("Which two verbs in this sentence are in the present tense?", "<es>tienen</es> and <es>es</es>."),
    ("Why <es>el ánima</es> if the noun is feminine?", "Feminine nouns beginning with a stressed a- take <es>el</es> in the singular."),
    ("Who does <es>les</es> refer to in <es>despertarles</es>?", "<es>las cosas</es>, the things."),
    ("From sentence 6: translate <es>de barba montaraz y manos de gorrión</es>.", "With a wild beard and sparrow hands."),
    ("From sentence 7: complete <es>y aun los objetos perdidos desde hacía mucho tiempo aparecían por donde...</es>", "<es>...más se les había buscado</es>."),
    ("Say the first three words of sentences 6, 7 and 8.", "<es>Un gitano corpulento</es> · <es>Fue de casa</es> · <es>Las cosas tienen</es>."),
  ],
  review_html="""<p><b>Checkpoint 2.</b> Play sentences 6, 7 and 8 in a row and shadow them at 0.75×. Then read them alone. This is the Melquíades scene: his portrait, his demonstration, his sales pitch.</p>""",
  memo="""<p>Sentence 8 is short enough to learn in two minutes: say the quotation as a single line first, <es>Las cosas tienen vida propia, todo es cuestión de despertarles el ánima</es>,
  then slot the narrator's aside into the middle.</p>
  <p>Then test the whole scene, sentences 6 to 8, in the practice box, and finish with one run of sentences 1 to 8 with the text visible.</p>""",
),
]
