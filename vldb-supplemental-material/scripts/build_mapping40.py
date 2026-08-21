#!/usr/bin/env python3
"""
Author + deterministically construct the FROZEN 40-item structural-mapping set.

Design (Roadmap Phase 1, superseding the n=6 mapping_pilot.json prototype):
  40 items = 10 role_rebinding + 10 causal_direction + 10 edge_redirection
             + 10 participant_reassignment.
  Each item: query in domain A; BOTH candidates in the same foreign domain B.
    * cand_correct  is graph-isomorphic to the query (gold map = identity on roles);
      so its gold scaffold IS the query scaffold.
    * cand_counterfactual = cand_correct with EXACTLY ONE declared directed-edge
      edit, predicate multiset preserved.

Phase 1.2 node-inventory balancing (the fix for the pilot's node_only leak):
  For every item the two candidates share IDENTICAL node inventories AND identical
  predicate multisets. THIRD_PARTY-introducing families keep THIRD_PARTY present in
  BOTH candidates; an edit only RE-POINTS an existing edge between already-present
  nodes -- it never adds a node. Result: node_only is forced to a tie on all four
  families (asserted by validate_mapping40.py), so the ranking signal cannot come
  from node counts.

Phase 1.4b far-analogy lexical distance (the fix for near-paraphrase candidates):
  cand_correct must be a genuine FAR analogy of the query -- same relational
  structure, DIFFERENT domain AND different surface vocabulary. Candidate prose is
  authored to share only function words with its query (token-Jaccard bounded by
  validate_mapping40.py assert A7), so success cannot come from string copying.
  The two candidates remain a tight single-edit minimal pair with each other.

Prose is hand-authored here; the GRAPHS are generated from a compact spec so that
query == cand_correct and cand_counterfactual differs by exactly the declared edit
BY CONSTRUCTION. This script does not call any model. Human adjudication of prose
realization (Phase 1.5 step 4) is a downstream checkpoint and is NOT performed here.

Writes:
  data/mapping_frozen_40.json
  data/mapping_frozen_40.manifest.json  (sha256 over the canonical item payload)
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "mapping_frozen_40.json"
MANIFEST = ROOT / "data" / "mapping_frozen_40.manifest.json"

NEG = "actually_negative"
POS = "actually_positive"
ACT = "ACTUALITY"
A, T, P = "AGENT", "TARGET", "THIRD_PARTY"

EDIT_DESC = {
    "reverse": "reverse the direction of the {p} edge (swap its two endpoints)",
    "retarget_object": "re-point the object of the {p} edge from an existing node to another already-present node",
    "retarget_subject": "re-assign the subject of the {p} edge from one existing node to another already-present node",
}


# --------------------------------------------------------------------------
# 40 authored items: prose + compact structural spec.
# base = cand_correct (== query) directed triples; edit picks ONE edge of base.
# Candidates are authored to be FAR analogies of the query (different domain AND
# different surface vocabulary), while cand_correct/cand_counterfactual stay a
# single-edit minimal pair.
# --------------------------------------------------------------------------
ITEMS = [
    # ==================== role_rebinding (reverse one role<->role edge) =========
    dict(id=301, family="role_rebinding", domain_a="workplace", domain_b="family",
         query="The manager deceived the new hire, leaned on her goodwill to cover his own missed targets, and knew all along it would set her back.",
         cand_correct="The stepfather spun a web of half-truths for his stepdaughter, leaned on her to cover the debts he'd run up, and knew all along the fallout would wreck her future.",
         cand_counterfactual="The stepdaughter spun a web of half-truths for her stepfather, while he leaned on her to cover the debts he'd run up, knowing all along the fallout would wreck her future.",
         base=[[A, "deceives", T], [A, "exploits", T], [A, "intends", NEG]], edit=("reverse", 0)),
    dict(id=302, family="role_rebinding", domain_a="finance", domain_b="medicine",
         query="The advisor misled the client, leaned on her trust to bury his own losses, and understood all along it would ruin her.",
         cand_correct="The physician strung the patient along with false reassurances, billed her relentlessly to bury his own botched treatment, certain it would leave her far worse off.",
         cand_counterfactual="The patient strung the physician along with false reassurances, while he billed her relentlessly to bury his own botched treatment, certain it would leave her far worse off.",
         base=[[A, "deceives", T], [A, "exploits", T], [A, "intends", NEG]], edit=("reverse", 0)),
    dict(id=303, family="role_rebinding", domain_a="academia", domain_b="sports",
         query="The professor exploited the grad student, lied to her about the credit, and hid what he was really after.",
         cand_correct="The team captain milked his rookie for everything she was worth, spun her a story about the scouting deal, and kept his real motive buried.",
         cand_counterfactual="The rookie milked her team captain for everything he was worth, while he spun her a story about the scouting deal and kept his real motive buried.",
         base=[[A, "exploits", T], [A, "deceives", T], [A, "conceals", ACT]], edit=("reverse", 0)),
    dict(id=304, family="role_rebinding", domain_a="politics", domain_b="religion",
         query="The senator kept testing his aide's loyalty, took credit for her work, and meant all along to discard her.",
         cand_correct="The abbot kept probing whether the young monk was truly devoted to him, passed off the monk's translations as his own scholarship, and had already resolved to cast him out.",
         cand_counterfactual="The young monk kept probing whether the abbot was truly devoted to him, while the abbot passed off the monk's translations as his own scholarship and had already resolved to cast him out.",
         base=[[A, "tests_loyalty", T], [A, "misattributes_credit", T], [A, "intends", NEG]], edit=("reverse", 0)),
    dict(id=305, family="role_rebinding", domain_a="military", domain_b="corporate",
         query="The commander deceived the young recruit, gave up his own standing to shield her, and hid the real cost.",
         cand_correct="The founder fed the junior partner a rosy lie; he burned his own reputation to take the fall for her, and kept the true damage hidden.",
         cand_counterfactual="The founder fed the junior partner a rosy lie; still trusting him, she burned her own reputation to take the fall for him, while he kept the true damage hidden.",
         base=[[A, "deceives", T], [A, "sacrifices_for", T], [A, "conceals", ACT]], edit=("reverse", 1)),
    dict(id=306, family="role_rebinding", domain_a="media", domain_b="law",
         query="The editor took credit for the reporter's scoop, leaned on her to keep producing, and planned to sideline her.",
         cand_correct="The senior partner claimed the associate's winning argument as his own work, drove her past exhaustion to keep the billables high, and was already scheming to freeze her out.",
         cand_counterfactual="The associate quietly claimed the senior partner's winning argument as her own before the committee, while he drove her past exhaustion to keep the billables high and was already scheming to freeze her out.",
         base=[[A, "misattributes_credit", T], [A, "exploits", T], [A, "intends", NEG]], edit=("reverse", 0)),
    dict(id=307, family="role_rebinding", domain_a="family", domain_b="school",
         query="The mother's constant rescuing kept her son helpless, she hid how dependent he'd become, and some part of her wanted it that way.",
         cand_correct="The tutor's constant propping-up left the pupil unable to manage on his own; she glossed over just how reliant he'd grown, and deep down preferred it that way.",
         cand_counterfactual="The pupil's constant propping-up left the tutor unable to manage on her own; the tutor glossed over just how reliant she'd grown, and deep down preferred it that way.",
         base=[[A, "harms_by_helping", T], [A, "conceals", ACT], [A, "intends", NEG]], edit=("reverse", 0)),
    dict(id=308, family="role_rebinding", domain_a="healthcare", domain_b="nonprofit",
         query="The doctor kept the grim prognosis from the patient to spare her, softened the truth when asked, and truly believed it was kindness.",
         cand_correct="The director held back news of the funding collapse from the volunteer to spare her, downplayed it whenever she pressed, and honestly believed she was being kind.",
         cand_counterfactual="The volunteer held back news of the funding collapse from the director to spare him; the director, for his part, downplayed the danger whenever she pressed, and honestly believed he was being kind.",
         base=[[A, "protects_by_withholding", T], [A, "deceives", T], [A, "intends", POS]], edit=("reverse", 0)),
    dict(id=309, family="role_rebinding", domain_a="sports", domain_b="music",
         query="The coach lied to his star player, kept testing her devotion with cruel little trials, and meant to cut her loose.",
         cand_correct="The maestro fed his lead singer a string of lies, kept staging cruel little tests of her devotion, and intended to drop her from the roster.",
         cand_counterfactual="The maestro fed his lead singer a string of lies; she, forever insecure, kept staging little tests of his devotion to her, and he intended to drop her from the roster.",
         base=[[A, "deceives", T], [A, "tests_loyalty", T], [A, "intends", NEG]], edit=("reverse", 1)),
    dict(id=310, family="role_rebinding", domain_a="tech", domain_b="restaurant",
         query="The startup founder overworked his engineer, kept inventing crises to keep her scared, and hid that the company was fine.",
         cand_correct="The head chef leaned on his sous-chef for everything, piling his own workload onto her, kept conjuring fake emergencies to keep her on edge, and hid that the kitchen was actually thriving.",
         cand_counterfactual="The sous-chef leaned on the head chef for everything, piling her own workload onto him, while he kept conjuring fake emergencies to keep her on edge and hid that the kitchen was actually thriving.",
         base=[[A, "exploits", T], [A, "manufactures_threat", T], [A, "conceals", ACT]], edit=("reverse", 0)),

    # ==================== causal_direction (reverse the causes edge) ============
    dict(id=311, family="causal_direction", domain_a="ecology", domain_b="economics",
         query="The new dam dries out the wetland downstream, it quietly powers the town that barely notices, and the agency buries its own impact study.",
         cand_correct="Heavy import duties are strangling the regional factories; those same duties prop up a protected cartel nobody scrutinizes, and the trade bureau has shelved the report that shows the harm.",
         cand_counterfactual="As the regional factories buckled, the political outcry drove the government to pile on even heavier import duties; those same duties prop up a protected cartel nobody scrutinizes, and the trade bureau has shelved the report that shows the harm.",
         base=[[A, "causes", T], [A, "enables", P], [A, "conceals", ACT]], edit=("reverse", 0)),
    dict(id=312, family="causal_direction", domain_a="health", domain_b="organization",
         query="Chronic stress brings on her migraines, it blocks the recovery she keeps chasing, and she hides how bad it's gotten.",
         cand_correct="Relentless layoffs are driving the staff into burnout; those same layoffs smother the turnaround leadership keeps promising, and management won't admit how far things have slid.",
         cand_counterfactual="The staff's burnout keeps tanking output, and that collapse is exactly what triggers each new round of layoffs; those same layoffs smother the turnaround leadership keeps promising, and management won't admit how far things have slid.",
         base=[[A, "causes", T], [A, "prevents", P], [A, "conceals", ACT]], edit=("reverse", 0)),
    dict(id=313, family="causal_direction", domain_a="climate", domain_b="finance",
         query="The drought triggers the wildfire season, it feeds the salvage industry that lobbies quietly, and the state hides the real acreage lost.",
         cand_correct="The sudden rate hike is choking off business lending; the same squeeze fattens the distressed-debt funds that lobby behind closed doors, and the central bank keeps the true default numbers under wraps.",
         cand_counterfactual="It was the freeze in business lending that spooked the markets into demanding a sudden rate hike; that hike still fattens the distressed-debt funds that lobby behind closed doors, and the central bank keeps the true default numbers under wraps.",
         base=[[A, "causes", T], [A, "enables", P], [A, "conceals", ACT]], edit=("reverse", 0)),
    dict(id=314, family="causal_direction", domain_a="biology", domain_b="workplace",
         query="The invasive weed chokes the native fish, it stalls the cleanup the rangers push for, and the department downplays the die-off.",
         cand_correct="A vicious rumor mill is wrecking the new hire's standing; the mill also derails the promotion her mentor keeps pushing, and the office quietly waves away the whole mess.",
         cand_counterfactual="The new hire's collapsing standing is exactly what gives the rumor mill fresh fuel; the mill in turn derails the promotion her mentor keeps pushing, and the office quietly waves away the whole mess.",
         base=[[A, "causes", T], [A, "prevents", P], [A, "conceals", ACT]], edit=("reverse", 0)),
    dict(id=315, family="causal_direction", domain_a="engineering", domain_b="education",
         query="The overheating reactor corrodes the pipes, it keeps the contractor endlessly employed, and the operator hides the inspection logs.",
         cand_correct="The rigid curriculum is grinding the students down; the same rigidity keeps the test-prep vendors permanently in business, and the district sits on the dropout figures.",
         cand_counterfactual="It's the students' collapsing scores that panic officials into doubling down on the rigid curriculum; that curriculum keeps the test-prep vendors permanently in business, and the district sits on the dropout figures.",
         base=[[A, "causes", T], [A, "enables", P], [A, "conceals", ACT]], edit=("reverse", 0)),
    dict(id=316, family="causal_direction", domain_a="medicine", domain_b="politics",
         query="The untreated infection inflames the joint, it stops the physical therapy from taking hold, and the clinic omits it from the chart.",
         cand_correct="The propaganda blitz is inflaming the border province; the blitz also keeps the peace talks from ever gaining traction, and the regime scrubs any mention of it from the official record.",
         cand_counterfactual="It's the border province's unrest that hands the regime fresh material for its propaganda blitz; the blitz still keeps the peace talks from ever gaining traction, and the regime scrubs any mention of it from the official record.",
         base=[[A, "causes", T], [A, "prevents", P], [A, "conceals", ACT]], edit=("reverse", 0)),
    dict(id=317, family="causal_direction", domain_a="agriculture", domain_b="tech",
         query="The pesticide runoff kills the pollinators, it props up the artificial-pollination startup, and the co-op stays quiet about the cause.",
         cand_correct="The addictive feed is steadily eroding users' attention spans; that erosion bankrolls a booming market for focus apps, and the platform stays tight-lipped about what's really driving it.",
         cand_counterfactual="Users' already-collapsing attention spans are exactly what the addictive feed was built to exploit; that feed in turn bankrolls a booming market for focus apps, and the platform stays tight-lipped about what's really driving it.",
         base=[[A, "causes", T], [A, "enables", P], [A, "conceals", ACT]], edit=("reverse", 0)),
    dict(id=318, family="causal_direction", domain_a="urban", domain_b="family",
         query="The new highway hollows out the old district, it chokes off the revival the residents want, and city hall shelves the study.",
         cand_correct="The father's steady drinking is hollowing out the whole household; it also strangles any hope of the stability the kids long for, and the family never breathes a word of it to outsiders.",
         cand_counterfactual="It's the household's slow unraveling that drives the father deeper into drink; his drinking still strangles any hope of the stability the kids long for, and the family never breathes a word of it to outsiders.",
         base=[[A, "causes", T], [A, "prevents", P], [A, "conceals", ACT]], edit=("reverse", 0)),
    dict(id=319, family="causal_direction", domain_a="biology", domain_b="economics",
         query="The algal bloom starves the lake of oxygen, it feeds the cleanup contractors who cheer it on, and the agency looks away.",
         cand_correct="The runaway subsidy is inflating a bloated sugar market; the same subsidy lines the pockets of brokers who happily egg it on, and the regulator conveniently looks the other way.",
         cand_counterfactual="It's the booming sugar market that lobbies hard to keep the runaway subsidy alive; that subsidy still lines the pockets of brokers who happily egg it on, and the regulator conveniently looks the other way.",
         base=[[A, "causes", T], [A, "enables", P], [A, "conceals", ACT]], edit=("reverse", 0)),
    dict(id=320, family="causal_direction", domain_a="psychology", domain_b="business",
         query="His insomnia deepens his anxiety, it blocks the therapy from working, and he won't admit the spiral to anyone.",
         cand_correct="The bruising price war keeps deepening the firm's losses; that same war chokes off any turnaround the board attempts, and leadership refuses to own up to the downward spiral.",
         cand_counterfactual="It's the firm's mounting losses that panic it into slashing prices even further, driving the war deeper; that war still chokes off any turnaround the board attempts, and leadership refuses to own up to the downward spiral.",
         base=[[A, "causes", T], [A, "prevents", P], [A, "conceals", ACT]], edit=("reverse", 0)),

    # ==================== edge_redirection (re-point an edge's OBJECT) ==========
    dict(id=321, family="edge_redirection", domain_a="workplace", domain_b="military",
         query="The manager deceived the analyst, kept probing the intern's loyalty, and leaned on the analyst to cover his missed targets.",
         cand_correct="The colonel fed the lieutenant false intel, kept probing the sergeant's loyalty, and squeezed the lieutenant to cover up his own blunders.",
         cand_counterfactual="The colonel fed the lieutenant false intel, kept probing the sergeant's loyalty, and squeezed the sergeant to cover up his own blunders.",
         base=[[A, "deceives", T], [A, "tests_loyalty", P], [A, "exploits", T]], edit=("retarget_object", 2)),
    dict(id=322, family="edge_redirection", domain_a="family", domain_b="academia",
         query="The mother shielded her daughter from the debt, lied to her son about it, and her constant rescuing quietly crippled the daughter.",
         cand_correct="The dean kept the brewing scandal from his protege, misled the provost about the whole affair, and his relentless coddling left the protege unable to cope alone.",
         cand_counterfactual="The dean kept the brewing scandal from his protege, misled the provost about the whole affair, and his relentless coddling left the provost unable to cope alone.",
         base=[[A, "protects_by_withholding", T], [A, "deceives", P], [A, "harms_by_helping", T]], edit=("retarget_object", 2)),
    dict(id=323, family="edge_redirection", domain_a="medicine", domain_b="finance",
         query="The surgeon misled the patient, propped up the drug rep who fed him referrals, and billed the patient for procedures she didn't need.",
         cand_correct="The broker spun the retiree a comforting fantasy, bankrolled the auditor who kept steering deals his way, and churned the retiree's account purely to rack up commissions.",
         cand_counterfactual="The broker spun the retiree a comforting fantasy, bankrolled the auditor who kept steering deals his way, and churned the auditor's account purely to rack up commissions.",
         base=[[A, "deceives", T], [A, "enables", P], [A, "exploits", T]], edit=("retarget_object", 2)),
    dict(id=324, family="edge_redirection", domain_a="politics", domain_b="sports",
         query="The senator kept the rival threat alive to scare the base, spent his capital shielding his donor, and fed the base a steady stream of lies.",
         cand_correct="The coach kept hyping a phantom rival to keep the squad on edge, burned his goodwill protecting his star player, and fed the squad one lie after another.",
         cand_counterfactual="The coach kept hyping a phantom rival to keep the squad on edge, burned his goodwill protecting his star player, and fed the star player one lie after another.",
         base=[[A, "manufactures_threat", T], [A, "sacrifices_for", P], [A, "deceives", T]], edit=("retarget_object", 2)),
    dict(id=325, family="edge_redirection", domain_a="tech", domain_b="religion",
         query="The founder lied to the engineers, kept testing the investor's faith, and worked the engineers to exhaustion.",
         cand_correct="The preacher deceived his flock, kept putting the head elder's faith to the test, and drove the flock to the point of collapse with endless duties.",
         cand_counterfactual="The preacher deceived his flock, kept putting the head elder's faith to the test, and drove the head elder to the point of collapse with endless duties.",
         base=[[A, "deceives", T], [A, "tests_loyalty", P], [A, "exploits", T]], edit=("retarget_object", 2)),
    dict(id=326, family="edge_redirection", domain_a="law", domain_b="family",
         query="The attorney kept the plea details from his client, misled the client's wife, and his relentless 'help' ended up sinking the client.",
         cand_correct="The uncle hid the terms of the will from his nephew, spun a false story for the boy's sister, and his smothering 'support' ended up ruining the nephew.",
         cand_counterfactual="The uncle hid the terms of the will from his nephew, spun a false story for the boy's sister, and his smothering 'support' ended up ruining the sister.",
         base=[[A, "protects_by_withholding", T], [A, "deceives", P], [A, "harms_by_helping", T]], edit=("retarget_object", 2)),
    dict(id=327, family="edge_redirection", domain_a="military", domain_b="corporate",
         query="The general lied to the front-line troops, bankrolled the militia that flattered him, and spent the troops recklessly.",
         cand_correct="The CEO peddled falsehoods to the rank and file, showered budget on the consultants who kept flattering him, and burned through the rank and file without a second thought.",
         cand_counterfactual="The CEO peddled falsehoods to the rank and file, showered budget on the consultants who kept flattering him, and burned through the consultants without a second thought.",
         base=[[A, "deceives", T], [A, "enables", P], [A, "exploits", T]], edit=("retarget_object", 2)),
    dict(id=328, family="edge_redirection", domain_a="education", domain_b="medicine",
         query="The principal kept a budget-cut scare over the teachers, poured resources into the star pupil, and kept lying to the teachers.",
         cand_correct="The chief kept a malpractice scare hanging over the nurses, funneled the department's resources to her star surgeon, and lied to the nurses at every turn.",
         cand_counterfactual="The chief kept a malpractice scare hanging over the nurses, funneled the department's resources to her star surgeon, and lied to that surgeon at every turn.",
         base=[[A, "manufactures_threat", T], [A, "sacrifices_for", P], [A, "deceives", T]], edit=("retarget_object", 2)),
    dict(id=329, family="edge_redirection", domain_a="finance", domain_b="ecology",
         query="The fund manager misled the small investors, kept testing his analyst's loyalty, and bled the small investors with fees.",
         cand_correct="The park warden deceived the local villagers, kept probing his deputy's loyalty, and worked the villagers half to death clearing trails for no pay.",
         cand_counterfactual="The park warden deceived the local villagers, kept probing his deputy's loyalty, and worked his deputy half to death clearing trails for no pay.",
         base=[[A, "deceives", T], [A, "tests_loyalty", P], [A, "exploits", T]], edit=("retarget_object", 2)),
    dict(id=330, family="edge_redirection", domain_a="sports", domain_b="politics",
         query="The coach hid the injury risk from his captain, misled the team doctor, and his 'protective' benching quietly wrecked the captain's career.",
         cand_correct="The chief of staff kept the looming scandal from the senator, fed the press secretary a cover story, and his 'protective' spin quietly torpedoed the senator's career.",
         cand_counterfactual="The chief of staff kept the looming scandal from the senator, fed the press secretary a cover story, and his 'protective' spin quietly torpedoed the press secretary's career.",
         base=[[A, "protects_by_withholding", T], [A, "deceives", P], [A, "harms_by_helping", T]], edit=("retarget_object", 2)),

    # ============ participant_reassignment (re-assign an edge's SUBJECT) ========
    dict(id=331, family="participant_reassignment", domain_a="workplace", domain_b="politics",
         query="The manager took credit for the analyst's overhaul, lied to the director about who did it, and quietly planned to push the analyst out.",
         cand_correct="The chief of staff claimed the aide's policy overhaul as his own, lied to the senator about who really drafted it, and was quietly maneuvering to force the aide out.",
         cand_counterfactual="The senator claimed the aide's policy overhaul as his own, while the chief of staff lied to that same senator about who really drafted it and was quietly maneuvering to force the aide out.",
         base=[[A, "misattributes_credit", T], [A, "deceives", P], [A, "intends", NEG]], edit=("retarget_subject", 0)),
    dict(id=332, family="participant_reassignment", domain_a="academia", domain_b="film",
         query="The advisor claimed the PhD student's discovery as his own, misled the department chair, and meant to keep the student down.",
         cand_correct="The director passed off the screenwriter's story idea as his own creation, misled the producer about its origins, and intended to keep the writer in the shadows.",
         cand_counterfactual="The producer passed off the screenwriter's story idea as his own creation, while the director misled the producer about its origins and intended to keep the writer in the shadows.",
         base=[[A, "misattributes_credit", T], [A, "deceives", P], [A, "intends", NEG]], edit=("retarget_subject", 0)),
    dict(id=333, family="participant_reassignment", domain_a="family", domain_b="corporate",
         query="The father's endless bailouts left his son helpless, he lied to the grandmother about the money, and buried how dire it had become.",
         cand_correct="The mentor's constant bailouts left the trainee unable to function on his own; he fed HR a false account of the lapses, and buried just how dire things had gotten.",
         cand_counterfactual="HR's constant bailouts left the trainee unable to function on his own, while the mentor fed HR a false account of the lapses and buried just how dire things had gotten.",
         base=[[A, "harms_by_helping", T], [A, "deceives", P], [A, "conceals", ACT]], edit=("retarget_subject", 0)),
    dict(id=334, family="participant_reassignment", domain_a="healthcare", domain_b="education",
         query="The chief physician overworked the residents, kept probing the head nurse's loyalty, and intended to thin the ranks.",
         cand_correct="The principal ran the teachers into the ground, kept probing the vice-principal's loyalty, and meant to cull the staff before long.",
         cand_counterfactual="The vice-principal ran the teachers into the ground, while the principal kept probing the vice-principal's loyalty and meant to cull the staff before long.",
         base=[[A, "exploits", T], [A, "tests_loyalty", P], [A, "intends", NEG]], edit=("retarget_subject", 0)),
    dict(id=335, family="participant_reassignment", domain_a="sports", domain_b="music",
         query="The coach took the credit for the striker's season, lied to the club president about it, and planned to sell her off.",
         cand_correct="The conductor claimed the soloist's breakout season as his own doing, misrepresented it to the board, and was already planning to let her go.",
         cand_counterfactual="The board claimed the soloist's breakout season as its own doing, while the conductor misrepresented it to the board and was already planning to let her go.",
         base=[[A, "misattributes_credit", T], [A, "deceives", P], [A, "intends", NEG]], edit=("retarget_subject", 0)),
    dict(id=336, family="participant_reassignment", domain_a="law", domain_b="tech",
         query="The senior partner's constant covering-for left the associate incompetent, he misled the ethics board, and hid the real record.",
         cand_correct="The lead engineer's habit of always cleaning up after the junior left the junior unable to code alone; he misled the review board, and hid the true commit history.",
         cand_counterfactual="The review board's habit of always cleaning up after the junior left the junior unable to code alone, while the lead engineer misled the review board and hid the true commit history.",
         base=[[A, "harms_by_helping", T], [A, "deceives", P], [A, "conceals", ACT]], edit=("retarget_subject", 0)),
    dict(id=337, family="participant_reassignment", domain_a="politics", domain_b="family",
         query="The party boss used the young canvassers, kept testing the deputy's loyalty, and meant to discard them after the election.",
         cand_correct="The patriarch made tools of the younger cousins, kept probing the eldest son's loyalty, and meant to cast them aside once the inheritance was settled.",
         cand_counterfactual="The eldest son made tools of the younger cousins, while the patriarch kept probing the eldest son's loyalty and meant to cast them aside once the inheritance was settled.",
         base=[[A, "exploits", T], [A, "tests_loyalty", P], [A, "intends", NEG]], edit=("retarget_subject", 0)),
    dict(id=338, family="participant_reassignment", domain_a="finance", domain_b="medicine",
         query="The portfolio lead claimed the quant's model as his own, lied to the risk committee, and set out to sideline the quant.",
         cand_correct="The attending physician claimed sole authorship of the resident's treatment protocol, misrepresented where it had come from to the hospital board, and was determined to push the resident to the margins.",
         cand_counterfactual="The hospital board claimed sole authorship of the resident's treatment protocol, while the attending physician misrepresented where it had come from to that board and was determined to push the resident to the margins.",
         base=[[A, "misattributes_credit", T], [A, "deceives", P], [A, "intends", NEG]], edit=("retarget_subject", 0)),
    dict(id=339, family="participant_reassignment", domain_a="military", domain_b="startup",
         query="The general's constant interventions left the junior officers unable to lead, he misled the oversight committee, and concealed the true readiness.",
         cand_correct="The founder's constant meddling left his managers unable to make a decision on their own; he fed the investors a rosy distortion, and hid the company's true burn rate.",
         cand_counterfactual="The investors' constant meddling left the managers unable to make a decision on their own, while the founder fed the investors a rosy distortion and hid the company's true burn rate.",
         base=[[A, "harms_by_helping", T], [A, "deceives", P], [A, "conceals", ACT]], edit=("retarget_subject", 0)),
    dict(id=340, family="participant_reassignment", domain_a="education", domain_b="sports",
         query="The dean exploited the adjuncts, kept testing the department head's loyalty, and planned to cut them loose.",
         cand_correct="The team owner wrung everything out of the rookies, kept probing the head coach's loyalty, and planned to release them the moment they slipped.",
         cand_counterfactual="The head coach wrung everything out of the rookies, while the team owner kept probing the head coach's loyalty and planned to release them the moment they slipped.",
         base=[[A, "exploits", T], [A, "tests_loyalty", P], [A, "intends", NEG]], edit=("retarget_subject", 0)),
]


def role_nodes(base):
    seen = []
    for s, _, o in base:
        for n in (s, o):
            if n in (A, T, P) and n not in seen:
                seen.append(n)
    return seen


def apply_edit(base, edit):
    op, idx = edit[0], edit[1]
    out = [list(e) for e in base]
    s, p, o = out[idx]
    if op == "reverse":
        out[idx] = [o, p, s]
    elif op == "retarget_object":
        out[idx] = [s, p, P]          # re-point to the already-present THIRD_PARTY
    elif op == "retarget_subject":
        out[idx] = [P, p, o]          # re-assign subject to already-present THIRD_PARTY
    else:
        raise ValueError(op)
    return out


def build():
    items = []
    for spec in ITEMS:
        base = spec["base"]
        edit = spec["edit"]
        cm = apply_edit(base, edit)
        changed = base[edit[1]]
        pred = base[edit[1]][1]
        rn = role_nodes(base)
        item = {
            "id": spec["id"],
            "family": spec["family"],
            "domain_a": spec["domain_a"],
            "domain_b": spec["domain_b"],
            "query": spec["query"],
            "cand_correct": spec["cand_correct"],
            "cand_counterfactual": spec["cand_counterfactual"],
            "predicate_multiset": sorted(p for _, p, _ in base),
            "edit_type": EDIT_DESC[edit[0]].format(p=pred),
            "edit_op": edit[0],
            "changed_query_edge": [changed[0], changed[1], changed[2]],
            "gold_scaffold": {
                "query": {"roles": rn, "relations": [list(e) for e in base]},
                "cand_correct": {"roles": rn, "relations": [list(e) for e in base]},
                "cand_counterfactual": {"roles": role_nodes(cm), "relations": cm},
            },
        }
        items.append(item)

    data = {
        "metadata": {
            "name": "Frozen Structural-Mapping Test (40 items)",
            "version": "1.0.0-frozen-pending-adjudication",
            "status": "AUTHOR-VALIDATED; HUMAN ADJUDICATION PENDING (Roadmap Phase 1.5 step 4). "
                      "The frozen extractor has NOT been run on these texts yet (Phase 1.5 step 6).",
            "supersedes": "data/mapping_pilot.json (n=6 PROTOTYPE/DEV) and "
                          "data/relation_only_candidates.json (n=24 pilot/DEV).",
            "freeze_doc": "data/FREEZE_mapping40.md",
            "design": "Query in domain A; BOTH candidates in the same foreign domain B. "
                      "cand_correct is graph-isomorphic to the query (gold map = identity "
                      "on roles); cand_counterfactual = cand_correct with EXACTLY ONE "
                      "directed-edge edit, predicate multiset preserved.",
            "node_inventory_balancing": "Both candidates share identical node inventories "
                      "AND identical predicate multisets on ALL four families, so node_only "
                      "is forced to a tie (verified by validate_mapping40.py). Edits only "
                      "re-point existing edges between already-present nodes.",
            "far_analogy_lexical_distance": "cand_correct is authored as a FAR analogy of the "
                      "query -- same structure, different domain AND different surface "
                      "vocabulary (shares only function words). Bounded by validate_mapping40.py "
                      "assert A7 (token-Jaccard(query, candidate) <= 0.35), so a match cannot "
                      "come from string copying.",
            "families": {
                "role_rebinding": "reverse a role<->role (non-causal) edge",
                "causal_direction": "reverse the directed `causes` edge",
                "edge_redirection": "re-point an edge's OBJECT to another present node",
                "participant_reassignment": "re-assign an edge's SUBJECT to another present node",
            },
            "predicate_vocabulary_frozen": True,
            "plausibility_note": "Counterfactual edits keep BOTH candidates pragmatically "
                      "plausible so no implausibility cue can substitute for structural mapping.",
        },
        "items": items,
    }
    OUT.write_text(json.dumps(data, indent=2))

    payload = json.dumps(items, sort_keys=True, ensure_ascii=False).encode("utf-8")
    checksum = hashlib.sha256(payload).hexdigest()
    manifest = {
        "file": OUT.name,
        "n_items": len(items),
        "per_family": {f: sum(1 for it in items if it["family"] == f)
                       for f in sorted({it["family"] for it in items})},
        "item_payload_sha256": checksum,
        "predicate_ontology_source": "scripts/llm_experiments.py::RELATION_VOCAB",
        "role_vocabulary": [A, T, P, ACT],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2))
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(items)} items)")
    print(f"wrote {MANIFEST.relative_to(ROOT)}")
    print(f"item_payload_sha256 = {checksum}")
    for f, k in manifest["per_family"].items():
        print(f"  {f:<26} {k}")


if __name__ == "__main__":
    build()
