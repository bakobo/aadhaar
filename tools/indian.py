#!/usr/bin/env python3
"""Extraction guards for Indian sources — the watermark, and the mojibake.

`method.md` §6: extraction is where corpora quietly go wrong, and the recurring shape is that **the
broken output looks fine**. India supplies two instances of that shape in one corpus, and both are
non-empty and plausible.

**(a) The watermark, which reorders.** Every PDF India Code serves is stamped with a diagonal "India
Code", and `pdftotext` emits its glyphs as separate fragments. In `-layout` mode — which is
`lawcorpus.pdf.extract`'s default — the fragments do not merely pollute the text, they **displace**
it: the 2021 Regulations' "…publication in the Official\n e Gazette." puts the last two words of a
sentence *above* the line that opens it, so `publication in the Official Gazette` greps to zero in a
document that says it. `layout=False` keeps the reading order and leaves the glyphs on lines of
their own, which is better and still not clean: 140 glyph-only lines in one 32-page instrument, and
the tokens are `e`, `od`, `aC`, `di` and `In` — none of which a blind filter can remove, since `In`
opens a sentence in this very corpus.

So the stored text is the publisher's own `TEXT` bundle, which is watermark-free, and our own
`layout=False` extraction is kept as the control that the publisher's text is complete
(`this.i` @yt6p5u4j). Neither source vouches for itself.

**(b) The mojibake, which reads as English.** India Code's bilingual Gazette scans extract to
character-level noise that stays legible enough to pass a skim: `p.ocedu.es for processing
ofcertificates`, `Recognized Foreign Certifling Authority`, `f- Uh,e 6nz, sTfiEtRUT of Slndio`. This
is Thailand's failure of `method.md` §6 in a different script, and it needs an answer with one more
joint in it than Thailand's: a 2016 Gazette page sets its *Hindi* in a legacy non-Unicode font, so
the Hindi extracts as Latin rubbish while the English beside it is untouched. Judged whole, that page
scores exactly where a genuinely corrupt document scores. So soundness is measured in windows and a
document below the floor is stored only if the passages it was declared for are themselves sound
(`this.i` @nppnqlxn) — and where even that runs out, `candidates.py` refuses a document by hand and
says why.
"""

from __future__ import annotations

import re

from lawcorpus.errors import LawcorpusError

# The nine glyphs of the "India Code" watermark, emitted in reverse order down a page. Used to
# *measure* contamination, never to remove it.
WATERMARK_TOKENS = ("e", "od", "aC", "di", "In", "d", "o", "C", "a", "i", "n", "I")

# Function words that are essentially unavoidable in Indian statutory English. A clean extraction of
# any instrument in this corpus runs 0.25–0.35 of all alphabetic tokens; a corrupted one collapses,
# because the corruption falls on short words as readily as long ones.
_COMMON = frozenset(
    "the of and to in shall be for or a is that by any under this such as on with an not it "
    "which may section act said person data information".split()
)
_TOKEN = re.compile(r"[A-Za-z]+")
_VOWEL = re.compile(r"[aeiouAEIOU]")
# A lowercase letter followed by an uppercase one inside a word — `sTfiEtRUT`, `Certifling` in the
# company of `Slndio`. English produces this in `eKYC` and `McDonald` and almost nowhere else.
_CAMEL = re.compile(r"[a-z][A-Z]")

# Measured across this corpus, 2026-09-16. Over a whole clean document: common 0.389–0.443,
# vowel-less 0.000–0.006, camel 0.000–0.012. Over the one document whose English is itself corrupt:
# common 0.165, vowel-less 0.165, camel 0.099. Three signals rather than one because a single
# threshold with a 2× margin is a threshold somebody will tune away; these have a 30× margin.
#
# **An internal-full-stop rate was tried and dropped.** `p.ocedu.es` looks like the signature of the
# failure, and it is — but ordinary Indian statutory citation (`s. 2(1)(p)`, `w.e.f.`) produces the
# same rate: 0.0045 in a clean document against 0.0078 in the corrupt one, which is no separation at
# all. It is recorded here because it is the obvious test to reach for and it does not work.
COMMON_FLOOR = 0.25
VOWELLESS_CEILING = 0.03
CAMEL_CEILING = 0.04
MIN_TOKENS = 40

# The measurement is **windowed**, because whole-document rates answer the wrong question. A Gazette
# page from 2016 sets its Hindi in a legacy non-Unicode Devanagari font, which extracts as Latin
# rubbish — `jftLVªh laö Mhö ,yö&33004@99`, `dk-vk- 2927¼v½` — sitting beside English that is
# *perfect*. Judged whole, S.O. 2927(E) scores 0.176 common and 0.228 vowel-less and reads exactly
# like the genuinely corrupt document; judged in windows, two of its seven windows are sound and they
# are the ones carrying the operative sentence. A guard that refused it would be refusing a good
# document, which is how guards get turned off (`method.md` §6, on why `thai.py` also tests the
# Latin). Window and step are in tokens, and the step is half the window so that a short passage
# cannot fall across a boundary and be scored twice as noise.
WINDOW, STEP = 60, 30
SOUND_SHARE_FLOOR = 0.70
# Clean documents run 0.728–1.000 windowed; the three damaged ones run 0.286, 0.500 and 0.317.

# The publisher's own extraction may be silently truncated: India Code's TEXT bundle for the DPDP
# Rules, 2025 stops at **exactly 100,000 characters**, mid-sentence, with no marker, where our own
# extraction of the same PDF runs to 119,414 and ends with the colophon. Every other document in
# this corpus has a publisher text 1.01–1.27× the length of ours, because ours loses the watermark
# lines. So a publisher text materially *shorter* than ours is the signature of a truncated tail —
# the failure `lawcorpus.completeness` was written for, in a place an inventory check cannot see it,
# because a schedule at the end of an instrument restarts its numbering and contributes no heading
# the body has not already used.
LENGTH_FLOOR = 0.98


class ExtractionRefused(LawcorpusError):
    """An extraction that is non-empty, plausible-looking, and not fit to quote."""

    code = "e.input.corrupt.extraction.f"


def watermark_lines(text: str) -> int:
    """Lines that are nothing but a watermark fragment. A measure, not a remedy."""
    return sum(1 for line in text.split("\n") if line.strip() in WATERMARK_TOKENS)


def displaced_lines(text: str) -> int:
    """Lines where a watermark fragment has absorbed body text — the reordering failure."""
    return len(re.findall(r"(?m)^[ \t]*(?:e|od|aC|di|In)[ \t]+\S", text))


def latin_health(text: str) -> dict:
    """Three rates over the Latin text only, plus the token count they are computed from."""
    tokens = _TOKEN.findall(text)
    if not tokens:
        return {"common": 0.0, "vowelless": 1.0, "camel": 1.0, "tokens": 0}
    long_tokens = [t for t in tokens if len(t) >= 3] or tokens
    return {
        "common": sum(1 for t in tokens if t.lower() in _COMMON) / len(tokens),
        "vowelless": sum(1 for t in long_tokens if not _VOWEL.search(t)) / len(long_tokens),
        "camel": sum(1 for t in long_tokens if _CAMEL.search(t)) / len(long_tokens),
        "tokens": len(tokens),
    }


def is_sound(text: str) -> bool:
    """Does this span read as English rather than as the wreck of a font the extractor could not?"""
    health = latin_health(text)
    return (
        health["common"] >= COMMON_FLOOR
        and health["vowelless"] <= VOWELLESS_CEILING
        and health["camel"] <= CAMEL_CEILING
    )


def sound_share(text: str) -> tuple:
    """(share, windows, sound windows) — how much of a document reads as English."""
    tokens = _TOKEN.findall(text)
    windows = [
        tokens[i : i + WINDOW] for i in range(0, max(len(tokens) - WINDOW + 1, 1), STEP)
    ]
    good = sum(1 for w in windows if is_sound(" ".join(w)))
    return (good / len(windows) if windows else 0.0, len(windows), good)


def span_is_sound(text: str, phrase: str, radius: int = 400) -> bool:
    """Is the passage around `phrase` sound, wherever in the document it sits?

    `search_key` is not used here: this asks about the *characters* around a phrase, and the folding
    that makes a phrase findable would also hide the damage being looked for. So the search is a
    whitespace-collapsed literal one, which is enough for a declared phrase we wrote ourselves.
    """
    flat = " ".join(text.split())
    at = flat.find(" ".join(phrase.split()))
    if at < 0:
        return False
    return is_sound(flat[max(at - radius, 0) : at + len(phrase) + radius])


def check_latin(text: str, what: str, phrases=()) -> str:
    """Refuse an extraction whose English cannot be quoted. Returns a qualifier, possibly empty.

    The guard is deliberately about the **Latin** text: this corpus quotes the English, which
    Article 348(1)(b) of the Constitution makes the authoritative text of every central Act and of
    the whole delegated layer. It makes no claim about Devanagari, whose corruption survives every
    ratio test — `जडजिटल` for `डिजिटल` is Devanagari of the right shape and the wrong letters.

    **Two things can be wrong and they need different answers.** The 2013 foreign-CA Regulation is
    corrupt *in its English*: `Recognized Foreign Certifling Authority`, `p.ocedu.es for processing
    ofcertificates`. Nothing in it can be quoted, so it is refused. A 2016 Gazette notification is
    an entirely different case: its Hindi is set in a legacy non-Unicode font and extracts as Latin
    rubbish, while its English is untouched. Refusing that would throw away a sound instrument, so
    it is stored **if the passages it is carried for are themselves sound**, with a qualifier that
    travels with every quotation saying which half of the page is readable.
    """
    health = latin_health(text)
    if health["tokens"] < MIN_TOKENS:
        raise ExtractionRefused(
            f"{what} extracted to {health['tokens']} Latin tokens, which is too few to judge and too "
            f"few to be the instrument. Read the file by hand before storing it."
        )
    share, total, good = sound_share(text)
    if share >= SOUND_SHARE_FLOOR:
        return ""
    unsound = [p for p in phrases if not span_is_sound(text, p)]
    if not phrases or unsound:
        raise ExtractionRefused(
            f"{what} will not be stored: only {good} of its {total} windows of text read as "
            f"English ({share:.2f}, floor {SOUND_SHARE_FLOOR}), and "
            + (
                "no declared phrase was given to test whether the part we want is among them"
                if not phrases
                else f"the declared phrase(s) {unsound} are not in a sound passage"
            )
            + ". A bilingual Gazette scan extracts to text that is non-empty and plausible and "
            "cannot be quoted — 'Recognized Foreign Certifling Authority' is what this looks like "
            "from the inside. Route it to OCR or find a clean source."
        )
    return (
        f"only {share:.0%} of this document extracts as readable English — its Hindi is set in a "
        f"legacy non-Unicode font and is not quotable at all; the English passages are sound and "
        f"each declared quotation was checked in place"
    )


def check_length(publisher: str, ours: str, what: str) -> None:
    """The publisher's text must not be materially shorter than our own extraction of the same PDF.

    This is the truncated-tail half of `lawcorpus.completeness`'s job, in the one place an inventory
    check cannot do it. See `LENGTH_FLOOR` above for the instrument that produced the rule.
    """
    if not ours:
        return
    ratio = len(publisher) / len(ours)
    if ratio < LENGTH_FLOOR:
        raise ExtractionRefused(
            f"The publisher's text of {what} is {len(publisher)} characters against {len(ours)} in "
            f"our own extraction of the same PDF ({ratio:.3f} of it, floor {LENGTH_FLOOR}). Ours "
            f"loses lines to the watermark and is still longer, so the publisher's text stops early. "
            f"A round number — 100,000 exactly — is a cap rather than a document length."
        )


_LONG = re.compile(r"[A-Za-z]{4,}")


def vocabulary(texts, floor: int = 3) -> set:
    """The words this corpus uses, built from the corpus itself. No dictionary, no dependency.

    A corpus of Indian statutory English is a better lexicon for judging Indian statutory English
    than any general word list, and it is already on disk. A word must appear `floor` times to
    count, so one damaged document cannot teach the vocabulary its own errors.
    """
    counts = {}
    for text in texts:
        for token in _LONG.findall(text):
            token = token.lower()
            counts[token] = counts.get(token, 0) + 1
    return {w for w, n in counts.items() if n >= floor}


def oov_rate(text: str, vocab: set) -> float:
    """How much of a document is words this corpus has never otherwise used.

    **A diagnostic, not a gate, and the distinction is the finding.** Measured against the Act
    layer, every sound instrument here runs 0.149–0.399 and the one whose English is corrupt runs
    0.619 — which looks decisive until the 2016 Gazette notifications, whose English is perfect, run
    0.480 and 0.667 because their legacy-font Hindi extracts as Latin rubbish. Windowing it does not
    rescue it either: around the passage that matters, the corrupt 2013 Regulation scores 0.195 and
    a sound notification scores 0.200. So this number goes in the harvest log for a person to read,
    and `candidates.py` excludes a document by hand where a person has read it.
    """
    tokens = [t.lower() for t in _LONG.findall(text)]
    return sum(1 for t in tokens if t not in vocab) / len(tokens) if tokens else 1.0


def inventory(text: str) -> list:
    """Every provision number appearing as a heading, as `lawcorpus.completeness.scan` reads them.

    Used to compare two extractions of the same document. Indian delegated instruments write a
    heading as a bare `13A.`, with no label, so the scan is label-less with a full stop as its
    terminator — which `scan` permits precisely because the terminator is what keeps a label-less
    pattern from matching every line that opens with a digit.
    """
    from lawcorpus.completeness import scan

    return [str(p) for p in scan(text, "", terminator=r"\.")]


def agree(publisher: str, ours: str, what: str) -> list:
    """Nothing our extraction finds may be missing from the publisher's. Returns the inventory.

    This is the control that keeps the publisher's text from vouching for itself. It is a comparison
    of *inventories* rather than of characters, because the two extractions differ in whitespace and
    in whether the watermark is present at all — what must agree is what provisions the document
    contains, which is the thing a corpus can be silently incomplete about.

    **It reports and does not refuse, and that is a retreat from how it was first written.** The
    first version refused on any heading our extraction found and the publisher's did not, which is
    the direction that would mean a truncated instrument. It fired twice, and both times on noise: a
    page number at the start of a line in the Enrolment and Update Regulations, and seventeen page
    numbers in the Constitution — `1188`, `2650`, `413` — which `scan` reads as headings because in a
    label-less scan that is exactly what a heading looks like. A gate whose only firings are false
    is worse than no gate, because the next person turns it off in a hurry and does not read what
    else it was doing. **`check_length` is the gate for the failure this was meant to catch**, and it
    catches it in a form page numbers cannot imitate: a publisher text materially shorter than ours.
    """
    theirs, mine = inventory(publisher), inventory(ours)
    return sorted(set(mine) - set(theirs))
