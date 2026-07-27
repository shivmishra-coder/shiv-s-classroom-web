"""
Shiv's Classroom (SSC CGL Base Architecture)
A fully standalone, session-state-driven Streamlit study companion for
SSC CGL / CHSL / MTS / RRB NTPC / CPO aspirants.

Run with:  streamlit run app.py
"""

import math
from datetime import date, timedelta
from urllib.parse import quote_plus

import streamlit as st

# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIG (must be first Streamlit call)
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Shiv's Classroom | SSC CGL Base Architecture",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# STATIC DATA
# ──────────────────────────────────────────────────────────────────────────

EXAMS = ["SSC CGL (Base)", "SSC CHSL", "SSC MTS", "RRB NTPC", "SSC CPO / Delhi Police"]

EXAM_CONFIG = {
    "SSC CGL (Base)":          {"Maths": 1.00, "English": 1.00, "Reasoning": 1.00, "GS": 1.00, "advanced": True},
    "SSC CHSL":                {"Maths": 0.85, "English": 1.00, "Reasoning": 0.90, "GS": 0.85, "advanced": False},
    "SSC MTS":                 {"Maths": 0.55, "English": 0.55, "Reasoning": 0.60, "GS": 0.60, "advanced": False},
    "RRB NTPC":                {"Maths": 0.90, "English": 0.50, "Reasoning": 0.90, "GS": 1.10, "advanced": False},
    "SSC CPO / Delhi Police":  {"Maths": 1.00, "English": 0.90, "Reasoning": 1.10, "GS": 1.00, "advanced": True},
}

TOPICS = {
    "Maths": [
        ("Number System", 12, False),
        ("HCF & LCM", 6, False),
        ("Simplification & Approximation", 8, False),
        ("Percentage", 10, False),
        ("Profit & Loss", 15, False),
        ("Simple & Compound Interest", 12, False),
        ("Ratio & Proportion", 8, False),
        ("Average", 6, False),
        ("Mixture & Alligation", 8, False),
        ("Time, Speed & Distance", 12, False),
        ("Time & Work", 12, False),
        ("Algebra", 15, False),
        ("Geometry", 22, True),
        ("Mensuration (2D & 3D)", 18, True),
        ("Trigonometry", 14, True),
        ("Height & Distance", 8, True),
        ("Data Interpretation", 12, False),
        ("Statistics", 6, True),
    ],
    "English": [
        ("Reading Comprehension", 15, False),
        ("Cloze Test", 8, False),
        ("Para Jumbles", 8, False),
        ("Error Spotting", 10, False),
        ("Sentence Improvement", 8, False),
        ("Fill in the Blanks", 6, False),
        ("One Word Substitution", 10, False),
        ("Idioms & Phrases", 10, False),
        ("Synonyms & Antonyms", 10, False),
        ("Spelling Correction", 5, False),
        ("Active-Passive Voice", 8, False),
        ("Direct-Indirect Speech", 8, False),
    ],
    "Reasoning": [
        ("Analogy", 6, False),
        ("Classification", 5, False),
        ("Series (Number/Alphabet)", 8, False),
        ("Coding-Decoding", 8, False),
        ("Blood Relations", 8, False),
        ("Direction Sense", 6, False),
        ("Syllogism", 10, False),
        ("Seating Arrangement", 12, False),
        ("Puzzle", 14, False),
        ("Non-Verbal Reasoning (Mirror/Water/Paper Folding)", 8, False),
        ("Venn Diagram", 6, False),
        ("Matrix", 5, False),
        ("Word Formation", 4, False),
    ],
    "GS": [
        ("Static GK (Books, Awards, Days)", 15, False),
        ("History - Ancient & Medieval", 10, False),
        ("History - Modern (Freedom Struggle)", 12, False),
        ("Geography - Indian & World", 12, False),
        ("Indian Polity & Constitution", 15, False),
        ("Economics - Basics", 10, False),
        ("Physics - Basics", 12, True),
        ("Chemistry - Basics", 12, True),
        ("Biology - Basics", 12, True),
        ("Computer Awareness", 6, False),
        ("Current Affairs (Last 6 Months)", 20, False),
    ],
}

SUBJECT_ORDER = ["Maths", "Reasoning", "English", "GS"]
SUBJECT_COLORS = {"Maths": "#06b6d4", "Reasoning": "#A855F7", "English": "#F59E0B", "GS": "#10B981"}

GRAMMAR_TOPICS = [
    "Subject-Verb Agreement Basics", "Neither-Nor Subject Agreement", "Either-Or Subject Agreement",
    "Collective Nouns Agreement", "Uncountable Noun Exceptions", "Countable vs Uncountable Nouns",
    "Articles - A/An/The Usage", "Article Omission Rules", "Tense - Present Simple vs Continuous",
    "Tense - Present Perfect vs Past Simple", "Tense - Past Perfect Usage", "Tense - Future Forms",
    "Sequence of Tenses", "1st Conditional Sentences", "2nd Conditional Sentences",
    "3rd Conditional Sentences", "Mixed Conditionals", "Modals - Can/Could/May/Might",
    "Modals - Must/Have to/Should", "Modals of Deduction", "Active-Passive Voice - Simple Tenses",
    "Active-Passive Voice - Perfect Tenses", "Active-Passive Voice - Modals", "Direct-Indirect Speech - Statements",
    "Direct-Indirect Speech - Questions", "Direct-Indirect Speech - Commands & Requests",
    "Confusable Words (Affect/Effect etc.)", "Prepositions of Time", "Prepositions of Place",
    "Prepositions after Adjectives", "Prepositions after Verbs", "Phrasal Verbs - Common Set 1",
    "Phrasal Verbs - Common Set 2", "Degrees of Comparison", "Adjective Order Rules",
    "Adverb Placement Rules", "Gerund vs Infinitive", "Pronoun-Antecedent Agreement",
    "Reflexive Pronouns Usage", "Relative Clauses - Defining", "Relative Clauses - Non-Defining",
    "Conjunctions - Coordinating", "Conjunctions - Subordinating", "Parallelism in Sentences",
    "Redundancy & Tautology", "Homophones Common Errors", "Punctuation - Comma Rules",
    "Punctuation - Apostrophe Rules", "Idiomatic Prepositional Phrases", "One Word Substitution - Person Types",
    "One Word Substitution - Places & Groups", "Synonyms - High Frequency PYQ Set",
    "Antonyms - High Frequency PYQ Set", "Spelling Rules - Common Errors", "Narration Changes with Modals",
    "Question Tag Formation", "Double Negatives Errors", "Comparative Structures - As...As",
    "Inversion Structures", "Cleft Sentences",
]

MOCK_SECTIONAL_TARGET = 500
MOCK_FULL_TARGET = 200
MOCK_SECTIONAL_PER_SUBJECT = 125
TOTAL_PLAN_DAYS = 330
INITIAL_LEAVE_BALANCE = 10
MAX_LEAVE_BALANCE = 30
WEEKLY_MEDAL_THRESHOLD = 0.80
STAGES = ["concept", "pyq", "rev1", "rev2"]
STAGE_LABELS = ["Concept / Video", "100+ PYQs", "1st Revision", "2nd Revision"]

# ──────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ──────────────────────────────────────────────────────────────────────────

def default_micro_state():
    return {"concept": False, "pyq": False, "rev1": False, "rev2": False}


def init_state():
    ss = st.session_state
    
    # Ye condition lagana ZARURI hai taaki rerun hone par values WIPE-OUT / RESET na hon
    if "initialized" not in ss:
        ss.initialized = True
        ss.student_name = ""
        ss.student_address = ""
        ss.student_mobile = ""
        ss.student_age = 0
        ss.student_telegram = ""
        ss.master_schedule_visible = False
        ss.engine_started = False
        ss.engine_locked_start_date = None
        ss.engine_frozen_days = 0
        ss.topic_actual_hours = {}
        ss.exam = EXAMS[0]
        ss.mode = "Foundation Scaling Mode (Recommended for Beginners)"
        ss.active_day = 1
        ss.streak = 0
        ss.consecutive_leaves = 0
        ss.warmup_pending = False
        ss.leave_balance = INITIAL_LEAVE_BALANCE
        ss.leave_log = []
        ss.leave_audit = []
        ss.leave_earn_streak_milestone = 0
        ss.leave_earn_hours_milestone = 0
        ss.total_focus_hours = 0.0
        ss.today_logged_hours = 0.0
        ss.syllabus_finished_manual = False
        ss.topic_progress = {}
        ss.exam_date = date.today() + timedelta(days=330)
        ss.start_date = date.today()
        ss.weekly_hours = {}
        ss.topic_mastery_day = {}
        ss.gold_medals = []
        ss.evaluated_weeks = set()
        ss.vocab_items = []
        ss.vocab_next_id = 1
        ss.grammar_state = {t: default_micro_state() for t in GRAMMAR_TOPICS}
        ss.micro_topic_state = {}
        ss.speed_test_log = []
        ss.mock_logs = []
        ss.mock_hub_logs = []
        ss.bookmarks = []
        ss.bookmark_next_id = 1
        ss.rapid_mock_log = []
        ss.selected_certificate_week = None

# Pure script me initialization bas yahan se trigger hogi:
# Sirf EK BAAR call hoga jab session_state truly uninitialized ho — is se
# rerun (button click, widget change, etc.) par values kabhi wipe-out nahi hongi.
if "initialized" not in st.session_state:
    init_state()

ss = st.session_state

# Backward-compatible migration for existing sessions
def migrate_session():
    defaults = {
        "student_name": "",
        "student_address": "",
        "student_mobile": "",
        "student_age": 0,
        "student_telegram": "",
        "master_schedule_visible": False,
        "engine_started": False,
        "engine_locked_start_date": None,
        "engine_frozen_days": 0,
        "topic_actual_hours": {},
        "leave_audit": [],
        "leave_earn_streak_milestone": 0,
        "leave_earn_hours_milestone": 0,
        "weekly_hours": {},
        "topic_mastery_day": {},
        "gold_medals": [],
        "evaluated_weeks": set(),
        "micro_topic_state": {},
        "mock_hub_logs": [],
        "selected_certificate_week": None,
    }
    for key, val in defaults.items():
        if key not in ss:
            ss[key] = val
    if ss.leave_balance > MAX_LEAVE_BALANCE:
        ss.leave_balance = MAX_LEAVE_BALANCE
    # Auto-start engine for sessions that already had progress
    if not ss.engine_started and (ss.active_day > 1 or ss.total_focus_hours > 0):
        ss.engine_started = True
        if ss.engine_locked_start_date is None:
            ss.engine_locked_start_date = ss.start_date
    if ss.engine_started and ss.engine_locked_start_date is None:
        ss.engine_locked_start_date = ss.start_date


migrate_session()

# ──────────────────────────────────────────────────────────────────────────
# CSS — Testbook-Inspired Dark Theme
# ──────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #0a1020 50%, #05070c 100%);
    color: #E2E8F0;
}

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

.block-container { padding-top: 1rem; }

/* Fixed top stats bar */
.top-stats-bar {
    position: sticky;
    top: 0;
    z-index: 999;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(6, 182, 212, 0.35);
    border-radius: 14px;
    padding: 12px 18px;
    margin-bottom: 18px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.45);
    backdrop-filter: blur(12px);
}
.top-stat-item {
    text-align: center;
    padding: 6px 8px;
}
.top-stat-label {
    font-size: 0.68rem;
    color: #94A3B8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.top-stat-value {
    font-size: 1.15rem;
    font-weight: 800;
    color: #F8FAFC;
    margin-top: 2px;
}
.top-stat-value.teal { color: #06b6d4; }
.top-stat-value.gold { color: #FBBF24; }
.top-stat-value.green { color: #34D399; }

.glass-card {
    background: #1e293b;
    border: 1px solid rgba(6, 182, 212, 0.18);
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 14px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.3);
}

.hero-title {
    font-size: 2.3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #06b6d4, #22d3ee 45%, #FBBF24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    letter-spacing: -0.5px;
}
.hero-sub { color: #94A3B8; font-size: 0.95rem; margin-top: 4px; font-weight: 500; }

.metric-card {
    border-radius: 14px;
    padding: 16px 18px;
    background: #1e293b;
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: "";
    position: absolute;
    top: -40%; left: -20%;
    width: 140%; height: 140%;
    background: radial-gradient(circle, var(--glow-color) 0%, transparent 65%);
    opacity: 0.15;
    pointer-events: none;
}
.metric-label { font-size: 0.75rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.metric-value { font-size: 1.75rem; font-weight: 800; margin-top: 4px; color: #F8FAFC; }
.metric-delta { font-size: 0.78rem; color: #64748B; margin-top: 2px; }

.glow-emerald { --glow-color: #34D399; }
.glow-blue    { --glow-color: #06b6d4; }
.glow-amber   { --glow-color: #FBBF24; }
.glow-purple  { --glow-color: #A855F7; }

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #06b6d4, #22d3ee);
    border-radius: 8px;
}
.stProgress > div > div > div { background: rgba(255,255,255,0.08); border-radius: 8px; }

.stButton>button {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    color: #E2E8F0;
    border: 1px solid rgba(6, 182, 212, 0.35);
    border-radius: 10px;
    padding: 0.45rem 1rem;
    font-weight: 600;
    transition: all 0.18s ease;
}
.stButton>button:hover {
    border-color: #06b6d4;
    box-shadow: 0 0 14px rgba(6, 182, 212, 0.4);
    transform: translateY(-1px);
    color: #fff;
}
.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, #06b6d4, #0891b2);
    border: none;
    color: #0f172a;
}
.stButton>button[kind="primary"]:hover {
    box-shadow: 0 0 18px rgba(6, 182, 212, 0.55);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #1e293b;
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(6, 182, 212, 0.15);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #94A3B8;
    font-weight: 600;
    padding: 8px 14px;
}
.stTabs [aria-selected="true"] {
    background: rgba(6, 182, 212, 0.2);
    color: #F8FAFC !important;
}

.pill {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
}
.pill-green { background: rgba(52,211,153,0.15); color: #34D399; border: 1px solid rgba(52,211,153,0.35); }
.pill-amber { background: rgba(251,191,36,0.15); color: #FBBF24; border: 1px solid rgba(251,191,36,0.35); }
.pill-blue  { background: rgba(6,182,212,0.15); color: #06b6d4; border: 1px solid rgba(6,182,212,0.35); }
.pill-red   { background: rgba(248,113,113,0.15); color: #F87171; border: 1px solid rgba(248,113,113,0.35); }
.pill-gold  { background: rgba(251,191,36,0.2); color: #FBBF24; border: 1px solid rgba(251,191,36,0.5); }

.topic-row { border-bottom: 1px solid rgba(255,255,255,0.06); padding: 10px 0; }
hr { border-color: rgba(255,255,255,0.08); }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid rgba(6, 182, 212, 0.12);
}

.micro-stage-header { font-size: 0.72rem; color: #94A3B8; font-weight: 600; text-align: center; }

.certificate-wrap {
    background: linear-gradient(145deg, #fffef8 0%, #fef3c7 100%);
    border: 4px double #B45309;
    border-radius: 12px;
    padding: 36px 40px;
    color: #1e293b;
    text-align: center;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
    position: relative;
    overflow: hidden;
}
.certificate-wrap::before {
    content: "";
    position: absolute;
    inset: 12px;
    border: 2px solid rgba(180, 83, 9, 0.35);
    border-radius: 8px;
    pointer-events: none;
}
.cert-title { font-size: 1.5rem; font-weight: 800; color: #0f172a; letter-spacing: 0.04em; margin-bottom: 6px; }
.cert-subtitle { font-size: 0.85rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; }
.cert-name { font-size: 2rem; font-weight: 800; color: #B45309; margin: 18px 0; font-family: Georgia, serif; }
.cert-body { font-size: 0.95rem; color: #334155; line-height: 1.7; margin: 16px 0; }
.cert-seal {
    display: inline-block;
    width: 80px; height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle, #FBBF24, #B45309);
    color: #fff;
    font-size: 2rem;
    line-height: 80px;
    margin-top: 12px;
    box-shadow: 0 4px 16px rgba(180, 83, 9, 0.4);
}
.medal-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid rgba(251, 191, 36, 0.4);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 10px;
}
.profile-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid rgba(6, 182, 212, 0.45);
    border-radius: 14px;
    padding: 14px 20px;
    margin-bottom: 14px;
    box-shadow: 0 4px 20px rgba(6, 182, 212, 0.12);
}
.profile-card-line {
    font-size: 0.92rem;
    color: #E2E8F0;
    font-weight: 600;
    letter-spacing: 0.01em;
}
.profile-card-line span { color: #06b6d4; }
.engine-setup-banner {
    background: linear-gradient(135deg, rgba(6,182,212,0.15), rgba(251,191,36,0.1));
    border: 2px dashed rgba(6, 182, 212, 0.5);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    margin-bottom: 18px;
}
.engine-frozen-banner {
    background: rgba(251, 191, 36, 0.12);
    border: 1px solid rgba(251, 191, 36, 0.45);
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 14px;
}
.engine-live-banner {
    background: rgba(52, 211, 153, 0.1);
    border: 1px solid rgba(52, 211, 153, 0.35);
    border-radius: 14px;
    padding: 10px 16px;
    margin-bottom: 14px;
    font-size: 0.88rem;
    color: #34D399;
    font-weight: 600;
}
.candidate-card {
    background: linear-gradient(120deg, #0f172a 0%, #1e293b 55%, #0f172a 100%);
    border: 1px solid rgba(251, 191, 36, 0.4);
    border-radius: 18px;
    padding: 0;
    margin-bottom: 16px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
.candidate-card-strip {
    background: linear-gradient(90deg, #06b6d4, #FBBF24);
    padding: 6px 20px;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    color: #0f172a;
    text-transform: uppercase;
}
.candidate-card-body {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    align-items: center;
    padding: 16px 22px 18px 22px;
}
.candidate-avatar {
    width: 58px; height: 58px;
    min-width: 58px;
    border-radius: 50%;
    background: linear-gradient(135deg, #06b6d4, #0891b2);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; font-weight: 800; color: #0f172a;
    border: 2px solid rgba(251, 191, 36, 0.6);
}
.candidate-field-label { font-size: 0.66rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700; }
.candidate-field-value { font-size: 0.95rem; color: #F8FAFC; font-weight: 700; margin-top: 1px; }
.candidate-id-tag {
    margin-left: auto;
    text-align: right;
    font-size: 0.72rem;
    color: #FBBF24;
    font-weight: 700;
}
.morning-banner {
    background: linear-gradient(120deg, rgba(251,191,36,0.16), rgba(6,182,212,0.14));
    border: 1px solid rgba(251, 191, 36, 0.4);
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 14px;
}
.morning-banner-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #F8FAFC;
    margin-bottom: 4px;
}
.morning-banner-sub { color: #CBD5E1; font-size: 0.88rem; font-weight: 500; }
.telegram-card {
    background: linear-gradient(135deg, rgba(6,182,212,0.12), rgba(15,23,42,0.4));
    border: 1px solid rgba(6, 182, 212, 0.35);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 14px;
}
.master-schedule-item {
    border-left: 3px solid #06b6d4;
    padding: 8px 14px;
    margin-bottom: 8px;
    background: rgba(255,255,255,0.03);
    border-radius: 0 8px 8px 0;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────

def get_active_topics():
    cfg = EXAM_CONFIG[ss.exam]
    out = {}
    for subj, items in TOPICS.items():
        mult = cfg[subj]
        lst = []
        for name, hrs, adv in items:
            if adv and not cfg["advanced"]:
                continue
            lst.append((name, round(hrs * mult, 1)))
        out[subj] = lst
    return out


def topic_key(subject, name):
    return f"{subject}::{name}"


def grammar_key(name):
    return f"Grammar::{name}"


def ensure_micro_state(key):
    if key not in ss.micro_topic_state:
        ss.micro_topic_state[key] = default_micro_state()
    return ss.micro_topic_state[key]


def migrate_grammar_state():
    """Upgrade legacy 3-field grammar state to 4-stage micro state."""
    for t in GRAMMAR_TOPICS:
        gk = grammar_key(t)
        if gk in ss.micro_topic_state:
            continue
        old = ss.grammar_state.get(t, {})
        if isinstance(old, dict) and "learnt" in old:
            ss.micro_topic_state[gk] = {
                "concept": old.get("learnt", False),
                "pyq": old.get("pyq", False),
                "rev1": old.get("revision", False),
                "rev2": False,
            }
        else:
            ss.micro_topic_state[gk] = default_micro_state()


def init_all_micro_topics():
    migrate_grammar_state()
    active = get_active_topics()
    for subj, items in active.items():
        for name, _ in items:
            ensure_micro_state(topic_key(subj, name))


def is_topic_mastered(state):
    return all(state.get(s, False) for s in STAGES)


def get_completed(subject, name):
    return ss.topic_progress.get(topic_key(subject, name), 0.0)


def set_completed(subject, name, hours):
    ss.topic_progress[topic_key(subject, name)] = hours


def get_actual_hours(key):
    return ss.topic_actual_hours.get(key, 0.0)


def set_actual_hours(key, hours):
    ss.topic_actual_hours[key] = max(0.0, float(hours))


def get_baseline_for_key(key):
    if key.startswith("Grammar::"):
        return 1.0
    if "::" in key:
        subj, name = key.split("::", 1)
        for n, hrs in get_active_topics().get(subj, []):
            if n == name:
                return hrs
    return 0.0


def get_total_actual_hours():
    return sum(ss.topic_actual_hours.values())


def calculate_personal_pace():
    baseline_sum = 0.0
    actual_sum = 0.0
    for key, actual in ss.topic_actual_hours.items():
        if actual > 0:
            baseline = get_baseline_for_key(key)
            if baseline > 0:
                baseline_sum += baseline
                actual_sum += actual
    if actual_sum <= 0:
        return None, "Log actual hours on topics to calculate your pace"
    pace = baseline_sum / actual_sum
    if pace >= 1.05:
        label = f"Your Personal Pace: {pace:.1f}x Average Student Speed 🚀"
    elif pace <= 0.95:
        label = f"Your Personal Pace: {pace:.1f}x Pace (Take extra revision time)"
    else:
        label = f"Your Personal Pace: {pace:.1f}x — On Par with Average"
    return pace, label


def profile_complete():
    return bool(
        ss.student_name.strip()
        and ss.student_address.strip()
        and ss.student_mobile.strip()
    )


def can_start_engine():
    return profile_complete() and not ss.engine_started


def effective_start_date():
    return ss.engine_locked_start_date or ss.start_date


def calendar_date_for_day(day_number):
    return effective_start_date() + timedelta(days=day_number - 1)


def render_profile_card():
    name = ss.student_name.strip() or "Not Set"
    mobile = ss.student_mobile.strip() or "Not Set"
    address = ss.student_address.strip() or "Not Set"
    age = ss.student_age if ss.student_age and ss.student_age > 0 else "—"
    telegram = ss.student_telegram.strip() or "Not Linked"
    initial = (ss.student_name.strip()[:1] or "S").upper()
    st.markdown(f"""
    <div class="candidate-card">
        <div class="candidate-card-strip">🎓 Testbook-Style Candidate Card · Shiv's Classroom</div>
        <div class="candidate-card-body">
            <div class="candidate-avatar">{initial}</div>
            <div>
                <div class="candidate-field-label">Candidate Name</div>
                <div class="candidate-field-value">{name}</div>
            </div>
            <div>
                <div class="candidate-field-label">Age</div>
                <div class="candidate-field-value">{age}</div>
            </div>
            <div>
                <div class="candidate-field-label">📱 Mobile</div>
                <div class="candidate-field-value">{mobile}</div>
            </div>
            <div>
                <div class="candidate-field-label">📍 City / District</div>
                <div class="candidate-field-value">{address}</div>
            </div>
            <div>
                <div class="candidate-field-label">📨 Telegram</div>
                <div class="candidate-field-value">{telegram}</div>
            </div>
            <div class="candidate-id-tag">
                🎯 {ss.exam}<br>Day {ss.active_day} / {TOTAL_PLAN_DAYS}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_morning_banner():
    name = ss.student_name.strip() or "Aspirant"
    age_txt = f" (Age: {ss.student_age})" if ss.student_age and ss.student_age > 0 else ""
    mission_status = "🔓 Unlocked" if ss.master_schedule_visible else "🔒 Locked"
    st.markdown(f"""
    <div class="morning-banner">
        <div class="morning-banner-title">☀️ Good Morning, {name}{age_txt}!</div>
        <div class="morning-banner-sub">
            Day {ss.active_day} of your {ss.exam} Prep &nbsp;•&nbsp; Today's Mission is {mission_status}
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📋 LOAD TODAY'S MASTER SCHEDULE", type="primary", use_container_width=True):
        ss.master_schedule_visible = not ss.master_schedule_visible
        st.rerun()


def render_todays_master_schedule():
    st.markdown("##### 📋 Today's Master Schedule — Micro-Topics + Est. vs Actual Time")
    if rapid_mock_active():
        st.info("Rapid Mock Mode is active — today's mission is 2 Mocks + Deep Analysis. See the 🎯 Rapid Mock Mode tab.")
        return
    active_topics = get_active_topics()
    daily_target = get_daily_target_hours(ss.active_day)
    focus_topics = []
    for subj in SUBJECT_ORDER:
        for name, target in active_topics[subj]:
            done = get_completed(subj, name)
            if done < target:
                focus_topics.append((subj, name, done, target))
                break
    if not focus_topics:
        st.success("🎉 All topics completed! Consider Rapid Mock Mode.")
        return
    per_topic_alloc = round(daily_target / len(focus_topics), 1)
    for subj, name, done, target in focus_topics:
        tk = topic_key(subj, name)
        mstate = ensure_micro_state(tk)
        stages_done = sum(1 for s in STAGES if mstate[s])
        actual = get_actual_hours(tk)
        est = min(per_topic_alloc, target - done)
        st.markdown(f"""
        <div class="master-schedule-item">
            <span class="pill pill-blue">{subj}</span> <b>{name}</b>
            <div style="color:#94A3B8;font-size:0.82rem;margin-top:3px;">
                Stages: {stages_done}/4 &nbsp;•&nbsp; Estimated Today: <b>{est:.1f}h</b> &nbsp;•&nbsp;
                Actual Logged: <b>{actual:.1f}h</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.caption("Full checklist and hour logging available in the 📚 Syllabus & Schedule and ✅ Micro-Topic Tracker tabs.")


def render_telegram_alert_card():
    with st.expander("📨 Telegram Daily Wake-Up Alert Integration", expanded=False):
        handle = ss.student_telegram.strip()
        st.markdown('<div class="telegram-card">', unsafe_allow_html=True)
        st.markdown("**How to receive automated daily wake-up reminders on your phone:**")
        st.markdown(
            "1. Open Telegram and search for **@ShivsClassroomBot** (or your own reminder bot).\n"
            "2. Tap **Start** to activate the chat.\n"
            "3. Send `/subscribe` along with your Student Name so the bot can identify you.\n"
            "4. The bot will message your saved Telegram username/chat ID every morning with "
            "your Day number, target hours, and today's focus topics.\n"
            "5. For a custom webhook, connect this app's daily-complete event to a Telegram Bot "
            "API `sendMessage` call using your Bot Token + Chat ID."
        )
        if handle:
            clean_handle = handle.lstrip("@")
            st.markdown(f"🔗 [Open your Telegram chat](https://t.me/{clean_handle})")
        else:
            st.caption("Add your Telegram Username / Chat ID in the sidebar Student Profile section to personalize this.")
        st.markdown("</div>", unsafe_allow_html=True)


def count_micro_topics_mastered(subject_filter=None):
    init_all_micro_topics()
    active = get_active_topics()
    mastered = 0
    total = 0
    per_subject = {s: {"mastered": 0, "total": 0} for s in SUBJECT_ORDER}
    for subj, items in active.items():
        for name, _ in items:
            total += 1
            per_subject[subj]["total"] += 1
            state = ensure_micro_state(topic_key(subj, name))
            if is_topic_mastered(state):
                mastered += 1
                per_subject[subj]["mastered"] += 1
    if subject_filter:
        return per_subject.get(subject_filter, {"mastered": 0, "total": 0})
    return mastered, total, per_subject


def update_mastery_tracking(key):
    state = ensure_micro_state(key)
    if is_topic_mastered(state):
        if key not in ss.topic_mastery_day:
            ss.topic_mastery_day[key] = ss.active_day
    elif key in ss.topic_mastery_day:
        del ss.topic_mastery_day[key]


def get_week_number(day_number=None):
    day_number = day_number or ss.active_day
    return max(1, math.ceil(day_number / 7))


def calendar_date_for_day(day_number):
    return effective_start_date() + timedelta(days=day_number - 1)


def get_weekly_topic_target():
    _, total_topics, _ = count_micro_topics_mastered()
    total_weeks = math.ceil(TOTAL_PLAN_DAYS / 7)
    return max(1, math.ceil(total_topics / total_weeks))


def count_topics_mastered_in_week(week_num):
    start_day = (week_num - 1) * 7 + 1
    end_day = week_num * 7
    count = 0
    for _key, mastery_day in ss.topic_mastery_day.items():
        if start_day <= mastery_day <= end_day:
            count += 1
    return count


def get_weekly_hours(week_num):
    return ss.weekly_hours.get(week_num, 0.0)


def evaluate_week_medals(up_to_week=None):
    """Award gold medals for completed weeks meeting 80% target."""
    current_week = get_week_number()
    check_until = up_to_week or (current_week - 1)
    target = get_weekly_topic_target()
    for week in range(1, check_until + 1):
        if week in ss.evaluated_weeks:
            continue
        if week >= current_week and up_to_week is None:
            continue
        done = count_topics_mastered_in_week(week)
        if target > 0 and done >= WEEKLY_MEDAL_THRESHOLD * target:
            ss.gold_medals.append({
                "week": week,
                "date": calendar_date_for_day(week * 7).isoformat(),
                "topics_mastered": done,
                "weekly_target": target,
                "hours": get_weekly_hours(week),
                "title": f"Week {week} Ranker Gold Medal",
            })
        ss.evaluated_weeks.add(week)


def process_leave_earnings():
    """Award bonus leave for streak milestones (every 10 days) and focus hours (every 50h)."""
    while ss.streak >= ss.leave_earn_streak_milestone + 10:
        ss.leave_earn_streak_milestone += 10
        if ss.leave_balance < MAX_LEAVE_BALANCE:
            ss.leave_balance = min(MAX_LEAVE_BALANCE, ss.leave_balance + 1)
    hours_milestone = int(ss.total_focus_hours // 50) * 50
    while hours_milestone > ss.leave_earn_hours_milestone:
        ss.leave_earn_hours_milestone += 50
        if ss.leave_balance < MAX_LEAVE_BALANCE:
            ss.leave_balance = min(MAX_LEAVE_BALANCE, ss.leave_balance + 1)


def syllabus_totals():
    active = get_active_topics()
    total_target = 0.0
    total_done = 0.0
    per_subject = {}
    for subj, items in active.items():
        s_target = sum(h for _, h in items)
        s_done = sum(min(get_completed(subj, n), h) for n, h in items)
        per_subject[subj] = (s_done, s_target)
        total_target += s_target
        total_done += s_done
    pct = (total_done / total_target * 100) if total_target > 0 else 0.0
    return total_done, total_target, pct, per_subject


def is_ranker_phase():
    if ss.mode.startswith("Ranker"):
        return True
    return ss.active_day > 90


def weekday_for_day(day_number):
    d = effective_start_date() + timedelta(days=day_number - 1)
    return d.weekday()


def get_daily_target_hours(day_number):
    if ss.warmup_pending:
        return 5.0
    if not is_ranker_phase():
        return 5.0
    wd = weekday_for_day(day_number)
    return 6.0 if wd >= 5 else 8.0


def youtube_masterclass_link(topic_name):
    query = f"SSC CGL {topic_name} Full Course Masterclass"
    return f"https://www.youtube.com/results?search_query={quote_plus(query)}&sp=CAM%253D"


def youtube_link(query):
    return f"https://www.youtube.com/results?search_query={quote_plus(query)}"


def in_last_50_days():
    return ss.active_day >= (TOTAL_PLAN_DAYS - 50)


def rapid_mock_active():
    _, _, pct, _ = syllabus_totals()
    return pct >= 100 or ss.syllabus_finished_manual or in_last_50_days()


def metric_card(col, label, value, glow_class, delta=""):
    col.markdown(f"""
    <div class="metric-card {glow_class}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta">{delta}</div>
    </div>
    """, unsafe_allow_html=True)


def day_bucket(day_added, today_day):
    diff = today_day - day_added
    if diff <= 0:
        return "Fresh Today"
    elif diff == 1:
        return "Yesterday"
    elif diff == 2:
        return "2 Days Ago"
    elif diff == 3:
        return "3 Days Ago"
    return "Older"


def mock_hub_counts():
    sectional = sum(1 for m in ss.mock_hub_logs if m["type"] == "Sectional")
    full = sum(1 for m in ss.mock_hub_logs if m["type"] == "Full Length")
    by_subject = {s: 0 for s in SUBJECT_ORDER}
    for m in ss.mock_hub_logs:
        if m["type"] == "Sectional" and m.get("subject"):
            by_subject[m["subject"]] = by_subject.get(m["subject"], 0) + 1
    return sectional, full, by_subject


def generate_certificate_html(medal):
    addr = ss.student_address.strip() or "—"
    mobile = ss.student_mobile.strip() or "—"
    age_txt = str(ss.student_age) if ss.student_age and ss.student_age > 0 else "—"
    return f"""
    <div class="certificate-wrap">
        <div class="cert-subtitle">Shiv's Classroom Presents</div>
        <div class="cert-title">SHIV'S CLASSROOM — WEEKLY TOP PERFORMER CERTIFICATE</div>
        <div class="cert-name">{ss.student_name.strip() or 'Candidate'}</div>
        <div class="cert-body">
            Has demonstrated exceptional dedication and achieved Top Performer status for<br>
            <strong style="color:#B45309;">Week {medal['week']}</strong> of the preparation journey.<br><br>
            <strong>Candidate:</strong> {ss.student_name.strip() or '—'} &nbsp;|&nbsp;
            <strong>Age:</strong> {age_txt} &nbsp;|&nbsp;
            <strong>Mobile:</strong> {mobile} &nbsp;|&nbsp;
            <strong>Location:</strong> {addr}<br><br>
            <strong>Topics Mastered:</strong> {medal['topics_mastered']} / {medal['weekly_target']} weekly target &nbsp;|&nbsp;
            <strong>Focus Hours:</strong> {medal['hours']:.1f}h<br>
            <strong>Award:</strong> {medal['title']} 🥇
        </div>
        <div class="cert-seal">🥇</div>
        <div style="margin-top:16px;font-size:0.82rem;color:#64748B;">
            Issued on {medal['date']} &nbsp;•&nbsp; Target Exam: {ss.exam}
        </div>
    </div>
    """


def render_micro_checklist(key, prefix, topic_label, show_youtube=True, show_actual_hours=True):
    state = ensure_micro_state(key)
    baseline = get_baseline_for_key(key)
    cols = st.columns([3, 1, 1, 1, 1, 1])
    cols[0].markdown(f"**{topic_label}**")
    for i, stage in enumerate(STAGES):
        state[stage] = cols[i + 1].checkbox(
            STAGE_LABELS[i],
            value=state[stage],
            key=f"{prefix}_{stage}_{key}",
            label_visibility="collapsed",
        )
    if show_youtube:
        yt_url = youtube_masterclass_link(topic_label.split("::")[-1] if "::" in topic_label else topic_label)
        cols[5].markdown(f"[▶️ Watch]({yt_url})")
    update_mastery_tracking(key)
    if key.startswith("Grammar::"):
        topic_name = key.split("::", 1)[1]
        ss.grammar_state[topic_name] = state
    if show_actual_hours:
        actual = get_actual_hours(key)
        acol1, acol2, acol3 = st.columns([2, 2, 4])
        with acol1:
            st.caption(f"Baseline: **{baseline:.1f} hrs**")
        with acol2:
            new_actual = st.number_input(
                "Actual hrs spent",
                min_value=0.0, max_value=200.0, value=float(actual), step=0.5,
                key=f"actual_{prefix}_{key}", label_visibility="collapsed",
            )
            if new_actual != actual:
                set_actual_hours(key, new_actual)
        with acol3:
            if actual > 0 and baseline > 0:
                ratio = baseline / actual
                st.caption(f"Topic pace: **{ratio:.1f}x** baseline ({actual:.1f}h actual vs {baseline:.1f}h avg)")


def render_top_stats_bar(pct, mastered, total_topics):
    medals_count = len(ss.gold_medals)
    engine_label = "🟢 LIVE" if ss.engine_started else "⚙️ SETUP"
    frozen_label = f" · 🌴 Frozen {ss.engine_frozen_days}d" if ss.engine_frozen_days > 0 else ""
    st.markdown(f"""
    <div class="top-stats-bar">
        <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;">
            <div class="top-stat-item"><div class="top-stat-label">🎯 Target Exam</div>
                <div class="top-stat-value teal">{ss.exam.split(' (')[0]}</div></div>
            <div class="top-stat-item"><div class="top-stat-label">🚀 Engine</div>
                <div class="top-stat-value green">{engine_label}{frozen_label}</div></div>
            <div class="top-stat-item"><div class="top-stat-label">🔥 Active Streak</div>
                <div class="top-stat-value green">{ss.streak} days</div></div>
            <div class="top-stat-item"><div class="top-stat-label">🌴 Leave Balance</div>
                <div class="top-stat-value">{ss.leave_balance} / {MAX_LEAVE_BALANCE}</div></div>
            <div class="top-stat-item"><div class="top-stat-label">📊 Syllabus Done</div>
                <div class="top-stat-value teal">{pct:.1f}%</div></div>
            <div class="top-stat-item"><div class="top-stat-label">🥇 Weekly Medals</div>
                <div class="top-stat-value gold">{medals_count}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Initialise micro topics & evaluate medals on load
init_all_micro_topics()
evaluate_week_medals()

total_done, total_target, pct, per_subject = syllabus_totals()
mastered_count, total_micro, per_micro = count_micro_topics_mastered()

# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🎯 Shiv's Classroom")
    st.caption("Testbook-Style SSC Tracker")
    st.markdown("---")

    st.markdown("#### 👤 Student Profile & Onboarding")
    ss.student_name = st.text_input("👤 Student Full Name", value=ss.student_name)
    ss.student_age = st.number_input(
        "🎂 Age", min_value=0, max_value=100, value=int(ss.student_age or 0), step=1,
    )
    ss.student_mobile = st.text_input("📱 Mobile Number", value=ss.student_mobile)
    ss.student_address = st.text_input("📍 City / District", value=ss.student_address)
    ss.student_telegram = st.text_input(
        "📨 Telegram Username / Chat ID", value=ss.student_telegram,
        placeholder="e.g. @yourhandle or chat ID",
        help="Used for daily wake-up alerts via the Telegram Alert Integration card.",
    )
    ss.exam = st.selectbox("🌐 Exam Target", EXAMS, index=EXAMS.index(ss.exam))

    st.markdown("---")
    st.markdown("#### 🚀 Preparation Engine Lock")
    if ss.engine_started:
        frozen_txt = f" · 🌴 Frozen {ss.engine_frozen_days}d" if ss.engine_frozen_days > 0 else ""
        st.markdown(
            f'<div class="engine-live-banner">🟢 Engine LIVE — Calendar locked from '
            f'{effective_start_date().strftime("%d %b %Y")}{frozen_txt}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="engine-setup-banner">⚙️ Complete your profile (Name, Mobile, City) '
            'to unlock the Preparation Engine.</div>',
            unsafe_allow_html=True,
        )
        if st.button("🚀 START MY PREPARATION ENGINE", type="primary", use_container_width=True):
            if profile_complete():
                ss.engine_started = True
                ss.engine_locked_start_date = ss.start_date
                st.success("🚀 Preparation Engine started! Your calendar is now locked in.")
                st.rerun()
            else:
                st.warning("⚠️ Please fill in Name, Mobile & City above before starting the engine.")
        if not profile_complete():
            st.caption("Fill in Name, Mobile & City above to enable the button.")

    st.markdown("#### ⚙️ Study Mode")
    ss.mode = st.radio(
        "Choose your mode",
        [
            "Foundation Scaling Mode (Recommended for Beginners)",
            "Ranker Mode (Direct Unlock for Repeaters)",
        ],
        index=0 if ss.mode.startswith("Foundation") else 1,
        label_visibility="collapsed",
    )
    if ss.mode.startswith("Foundation"):
        st.caption("Days 1–90 → 5 hrs/day. Day 91+ → Ranker schedule.")
    else:
        st.caption("Day 1 onward → 8 hrs (Mon–Fri) / 6 hrs (Sat–Sun).")

    st.markdown("---")
    st.markdown("#### 📅 Settings")
    ss.start_date = st.date_input("Preparation Start Date (Day 1)", value=ss.start_date)
    current_cal_date = calendar_date_for_day(ss.active_day)
    projected_end = ss.start_date + timedelta(days=TOTAL_PLAN_DAYS - 1)
    st.caption(f"Today maps to **{current_cal_date.strftime('%a, %d %b %Y')}** (Day {ss.active_day})")
    st.caption(f"Projected completion: **{projected_end.strftime('%d %b %Y')}**")

    st.markdown("---")
    st.markdown("#### 📅 Day Tracker")
    st.metric("Active Study Day", f"{ss.active_day} / {TOTAL_PLAN_DAYS}")
    if ss.warmup_pending:
        st.markdown('<span class="pill pill-amber">🌤 Soft Warmup Day (5h)</span>', unsafe_allow_html=True)

    hrs_left_input = st.number_input(
        "Hours completed today", min_value=0.0, max_value=16.0,
        value=float(ss.today_logged_hours), step=0.5, key="hrs_today_input",
    )
    ss.today_logged_hours = hrs_left_input

    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Complete Day", type="primary", use_container_width=True):
            week = get_week_number(ss.active_day)
            ss.weekly_hours[week] = ss.weekly_hours.get(week, 0.0) + ss.today_logged_hours
            ss.total_focus_hours += ss.today_logged_hours
            ss.streak += 1
            prev_week = get_week_number(ss.active_day)
            ss.active_day += 1
            new_week = get_week_number(ss.active_day)
            if new_week > prev_week:
                evaluate_week_medals(up_to_week=prev_week)
            if ss.consecutive_leaves >= 2:
                ss.warmup_pending = True
            else:
                ss.warmup_pending = False
            ss.consecutive_leaves = 0
            ss.today_logged_hours = 0.0
            process_leave_earnings()
            st.rerun()
    with c2:
        if st.button("🌴 Quick Leave (-1)", use_container_width=True, disabled=ss.leave_balance <= 0):
            ss.leave_balance -= 1
            ss.leave_log.append(ss.active_day)
            ss.leave_audit.append({
                "date": current_cal_date.isoformat(),
                "days": 1,
                "category": "Quick",
                "reason": "Single-day quick leave from sidebar",
                "balance_after": ss.leave_balance,
            })
            ss.consecutive_leaves += 1
            ss.streak = 0
            st.rerun()

    st.markdown("---")
    st.markdown("#### 🌴 Leave Request Form")
    with st.form("leave_request_form"):
        lv_days = st.number_input("Days requested", min_value=1, max_value=7, value=1)
        lv_category = st.selectbox("Category", ["Medical", "Family", "Burnout", "Emergency"])
        lv_reason = st.text_area("Reason (mandatory)", placeholder="Describe why you need leave...")
        lv_submit = st.form_submit_button("Submit Leave Request", type="primary")
        if lv_submit:
            if not lv_reason.strip():
                st.error("Reason is mandatory.")
            elif lv_days > ss.leave_balance:
                st.error(f"Insufficient balance. You have {ss.leave_balance} passes.")
            else:
                ss.leave_balance -= int(lv_days)
                for _ in range(int(lv_days)):
                    ss.leave_log.append(ss.active_day)
                ss.leave_audit.append({
                    "date": current_cal_date.isoformat(),
                    "days": int(lv_days),
                    "category": lv_category,
                    "reason": lv_reason.strip(),
                    "balance_after": ss.leave_balance,
                })
                ss.consecutive_leaves += int(lv_days)
                ss.streak = 0
                st.success(f"Leave approved. Balance: {ss.leave_balance}")
                st.rerun()

    st.progress(ss.leave_balance / MAX_LEAVE_BALANCE, text=f"{ss.leave_balance} / {MAX_LEAVE_BALANCE} passes")
    st.caption(f"Started with {INITIAL_LEAVE_BALANCE} · Earn +1 every 10 streak days or 50 focus hours (cap {MAX_LEAVE_BALANCE})")

    st.markdown("---")
    ss.syllabus_finished_manual = st.checkbox(
        "🏁 Mark Syllabus as Finished (activates Rapid Mock Mode)",
        value=ss.syllabus_finished_manual,
    )
    ss.exam_date = st.date_input("📌 Exam Date (countdown)", value=ss.exam_date)

    st.markdown("---")
    if st.button("🔄 Reset Entire Tracker", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ──────────────────────────────────────────────────────────────────────────
# HEADER + TOP STATS BAR
# ──────────────────────────────────────────────────────────────────────────

render_top_stats_bar(pct, mastered_count, total_micro)

render_profile_card()
render_morning_banner()
if ss.master_schedule_visible:
    render_todays_master_schedule()
render_telegram_alert_card()

hcol1, hcol2 = st.columns([3, 1])
with hcol1:
    st.markdown('<div class="hero-title">Shiv\'s Classroom</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="hero-sub">Target: <b>{ss.exam}</b> &nbsp;•&nbsp; '
        f'Mode: <b>{"Ranker" if is_ranker_phase() else "Foundation"}</b> &nbsp;•&nbsp; '
        f'Day <b>{ss.active_day}</b> of {TOTAL_PLAN_DAYS} &nbsp;•&nbsp; '
        f'📅 {current_cal_date.strftime("%d %b %Y")}</div>',
        unsafe_allow_html=True,
    )
with hcol2:
    days_to_exam = (ss.exam_date - date.today()).days
    st.markdown(
        f'<div class="glass-card" style="text-align:center;padding:14px;">'
        f'<div class="metric-label">⏳ Exam Countdown</div>'
        f'<div class="metric-value" style="font-size:1.5rem;">{max(days_to_exam, 0)} days</div></div>',
        unsafe_allow_html=True,
    )

m1, m2, m3, m4 = st.columns(4)
metric_card(m1, "📈 Syllabus Progress", f"{pct:.1f}%", "glow-blue", f"{total_done:.1f} / {total_target:.1f} hrs")
metric_card(m2, "✅ Micro-Topics Mastered", f"{mastered_count}/{total_micro}", "glow-emerald", "All 4 stages complete")
metric_card(m3, "⏱ Total Focus Hours", f"{ss.total_focus_hours:.1f} h", "glow-purple", "Lifetime logged")
weekly_target = get_weekly_topic_target()
week_done = count_topics_mastered_in_week(get_week_number())
metric_card(m4, f"📅 Week {get_week_number()} Progress", f"{week_done}/{weekly_target}", "glow-amber", "Micro-topics this week")

st.markdown("")

if rapid_mock_active():
    st.markdown(
        '<div class="glass-card" style="border-color:rgba(251,191,36,0.5);">'
        '<span class="pill pill-amber">🎯 RAPID MOCK MODE ACTIVE</span> '
        '&nbsp;Syllabus schedule replaced with 2 Mocks/Day + Deep Analysis Routine.</div>',
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────────────────────────────────

tab_dash, tab_syllabus, tab_micro, tab_achieve, tab_revision, tab_grammar, tab_speed, tab_formula, tab_rapid = st.tabs([
    "📊 Dashboard", "📚 Syllabus & Schedule", "✅ Micro-Topic Tracker",
    "🏆 Achievements & Medals", "🔄 Rolling Revision", "📖 Grammar Tracker",
    "⚡ Speed & Mock Hub", "🗂️ Formula Chest", "🎯 Rapid Mock Mode",
])

# ---------------------------------------------------------------- DASHBOARD
with tab_dash:
    st.markdown("#### Live Progress Analytics")
    remaining_micro = total_micro - mastered_count
    remaining_hrs = max(0, total_target - total_done)
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("**Remaining Micro-Topics**")
        st.progress(mastered_count / total_micro if total_micro else 0, text=f"{remaining_micro} left · {mastered_count} mastered")
    with d2:
        st.markdown("**Target Hours Left**")
        st.progress(total_done / total_target if total_target else 0, text=f"{remaining_hrs:.1f} hrs remaining")
    with d3:
        st.markdown("**Syllabus Completion %**")
        st.progress(pct / 100, text=f"{pct:.1f}% complete")

    st.markdown("---")
    st.markdown("#### Subject-wise Micro-Topic Mastery")
    dcols = st.columns(4)
    for i, subj in enumerate(SUBJECT_ORDER):
        sm = per_micro.get(subj, {"mastered": 0, "total": 0})
        spct = (sm["mastered"] / sm["total"] * 100) if sm["total"] > 0 else 0
        with dcols[i]:
            st.markdown(f"**{subj}** — {sm['mastered']}/{sm['total']} Mastered")
            st.progress(min(spct / 100, 1.0), text=f"{spct:.0f}%")

    st.markdown("---")
    st.markdown("#### Subject-wise Hours Progress")
    hcols = st.columns(4)
    for i, subj in enumerate(SUBJECT_ORDER):
        done, target = per_subject.get(subj, (0, 0))
        spct = (done / target * 100) if target > 0 else 0
        with hcols[i]:
            st.markdown(f"**{subj}**")
            st.progress(min(spct / 100, 1.0), text=f"{spct:.0f}% ({done:.1f}/{target:.1f} h)")

    chart_data = {subj: per_subject.get(subj, (0, 0))[0] for subj in SUBJECT_ORDER}
    st.markdown("#### Hours Completed by Subject")
    st.bar_chart(chart_data)

    st.markdown("---")
    gcol1, gcol2 = st.columns(2)
    with gcol1:
        st.markdown("#### 📖 Grammar Checklist Progress")
        g_mastered = sum(1 for t in GRAMMAR_TOPICS if is_topic_mastered(ensure_micro_state(grammar_key(t))))
        total_g = len(GRAMMAR_TOPICS)
        st.progress(g_mastered / total_g, text=f"Fully Mastered: {g_mastered}/{total_g}")
    with gcol2:
        st.markdown("#### 📝 Recent Mock Test Logs")
        if ss.mock_logs:
            for log in ss.mock_logs[-5:][::-1]:
                st.markdown(
                    f'<div class="topic-row"><b>{log["exam_name"]}</b> — Score: {log["score"]} '
                    f'&nbsp;|&nbsp; Weak Area: <span class="pill pill-red">{log["weak_area"]}</span></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No mock tests logged yet.")

    if ss.leave_audit:
        st.markdown("---")
        st.markdown("#### 🌴 Leave Audit Table")
        st.dataframe(ss.leave_audit[::-1], use_container_width=True, hide_index=True)

# ------------------------------------------------------------ SYLLABUS TAB
with tab_syllabus:
    if rapid_mock_active():
        st.info("Syllabus schedule is paused — Rapid Mock Mode is active.")
    else:
        active_topics = get_active_topics()
        daily_target = get_daily_target_hours(ss.active_day)
        st.markdown(
            f"#### Today's Target: **{daily_target} hours** &nbsp; "
            f"({'🌤 Soft Warmup' if ss.warmup_pending else ('Ranker Phase' if is_ranker_phase() else 'Foundation Phase')}) "
            f"&nbsp;•&nbsp; 📅 {current_cal_date.strftime('%A, %d %b %Y')}"
        )

        focus_topics = []
        for subj in SUBJECT_ORDER:
            for name, target in active_topics[subj]:
                done = get_completed(subj, name)
                if done < target:
                    focus_topics.append((subj, name, done, target))
                    break

        if focus_topics:
            per_topic_alloc = round(daily_target / len(focus_topics), 1)
            st.markdown("##### 🎯 Today's Focus Topics")
            for subj, name, done, target in focus_topics:
                remaining = target - done
                est_days = max(1, math.ceil(remaining / max(per_topic_alloc, 0.5)))
                tk = topic_key(subj, name)
                mstate = ensure_micro_state(tk)
                stages_done = sum(1 for s in STAGES if mstate[s])
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card">
                        <span class="pill pill-blue">{subj}</span>&nbsp;
                        <b style="font-size:1.05rem;">{name}</b>
                        <div style="color:#94A3B8;font-size:0.85rem;margin-top:4px;">
                            {done:.1f} / {target:.1f} hrs &nbsp;•&nbsp; Stages: {stages_done}/4 &nbsp;•&nbsp;
                            ~{est_days} day(s) left &nbsp;•&nbsp; today: {min(per_topic_alloc, remaining):.1f}h
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(min(done / target, 1.0) if target > 0 else 0)
                    lcol1, lcol2, lcol3 = st.columns([2, 2, 3])
                    with lcol1:
                        add_hrs = st.number_input(
                            f"Log hours — {name}", min_value=0.0, max_value=10.0,
                            value=0.0, step=0.5, key=f"log_{subj}_{name}",
                        )
                    with lcol2:
                        if st.button("➕ Add Progress", key=f"btn_{subj}_{name}"):
                            new_val = min(done + add_hrs, target)
                            set_completed(subj, name, new_val)
                            st.rerun()
                    with lcol3:
                        st.markdown(f"[▶️ Watch Best Lecture]({youtube_masterclass_link(name)})")
        else:
            st.success("🎉 All topics completed! Consider Rapid Mock Mode.")

        st.markdown("---")
        st.markdown("##### ⚡ Sectional Speed Test Slot (15–20 min, weekdays)")
        st.caption("Last weekday slot → timed sectional test (25 PYQs).")

        st.markdown("---")
        with st.expander("📋 Full Syllabus Breakdown"):
            for subj in SUBJECT_ORDER:
                st.markdown(f"**{subj}**")
                for name, target in active_topics[subj]:
                    done = get_completed(subj, name)
                    tk = topic_key(subj, name)
                    ms = ensure_micro_state(tk)
                    st_done = sum(1 for s in STAGES if ms[s])
                    st.markdown(f"- {name}: {done:.1f}/{target:.1f} hrs · Stages {st_done}/4")

# ------------------------------------------------------- MICRO-TOPIC TRACKER
with tab_micro:
    st.markdown("#### ✅ 4-Stage Micro-Topic Checklist (All Subjects)")
    st.caption("Concept / Video → 100+ PYQs → 1st Revision → 2nd Revision. All 4 = Mastered.")
    active_topics = get_active_topics()
    subj_filter = st.selectbox("Filter subject", ["All"] + SUBJECT_ORDER, key="micro_filter")
    search_micro = st.text_input("🔎 Search micro-topics", "")

    hdr = st.columns([3, 1, 1, 1, 1, 1])
    hdr[0].markdown("**Micro-Topic**")
    for i, lbl in enumerate(STAGE_LABELS):
        hdr[i + 1].markdown(f'<div class="micro-stage-header">{lbl}</div>', unsafe_allow_html=True)
    hdr[5].markdown('<div class="micro-stage-header">Lecture</div>', unsafe_allow_html=True)

    subjects_to_show = SUBJECT_ORDER if subj_filter == "All" else [subj_filter]
    for subj in subjects_to_show:
        st.markdown(f"### {subj} <span class='pill pill-blue'>{per_micro[subj]['mastered']}/{per_micro[subj]['total']} Mastered</span>", unsafe_allow_html=True)
        for name, _ in active_topics[subj]:
            if search_micro and search_micro.lower() not in name.lower():
                continue
            tk = topic_key(subj, name)
            render_micro_checklist(tk, "micro", name, show_youtube=True)
        st.markdown("---")

# ---------------------------------------------------- ACHIEVEMENTS & MEDALS
with tab_achieve:
    st.markdown("#### 🏆 Achievements & Medals")
    current_week = get_week_number()
    week_target = get_weekly_topic_target()
    week_done_count = count_topics_mastered_in_week(current_week)
    week_pct = (week_done_count / week_target * 100) if week_target else 0

    ac1, ac2, ac3 = st.columns(3)
    ac1.metric("Active Week", f"Week {current_week}")
    ac2.metric("This Week's Topics", f"{week_done_count} / {week_target}")
    ac3.metric("Weekly Target %", f"{week_pct:.0f}%")

    st.progress(min(week_pct / 100, 1.0), text=f"Need ≥{WEEKLY_MEDAL_THRESHOLD*100:.0f}% for Gold Medal 🥇")
    if week_pct >= WEEKLY_MEDAL_THRESHOLD * 100:
        st.success(f"🎉 Week {current_week} is on track for a Gold Medal! Keep going!")
    else:
        needed = max(0, math.ceil(WEEKLY_MEDAL_THRESHOLD * week_target) - week_done_count)
        st.info(f"Complete {needed} more micro-topic(s) this week to unlock the Gold Medal.")

    st.markdown("---")
    st.markdown("##### 🥇 Gold Medals Unlocked")
    if ss.gold_medals:
        for medal in ss.gold_medals[::-1]:
            st.markdown(f"""
            <div class="medal-card">
                <span class="pill pill-gold">🥇 {medal['title']}</span><br>
                <span style="color:#94A3B8;font-size:0.85rem;">
                    {medal['topics_mastered']} topics · {medal['hours']:.1f}h · {medal['date']}
                </span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No gold medals yet. Hit 80%+ weekly micro-topic target to earn one!")

    st.markdown("---")
    st.markdown("##### 📜 Weekly Top Performer Certificate")
    if ss.gold_medals:
        cert_weeks = [m["week"] for m in ss.gold_medals]
        selected = st.selectbox("Select week certificate", cert_weeks, format_func=lambda w: f"Week {w} — Gold Medal")
        medal = next(m for m in ss.gold_medals if m["week"] == selected)
        st.markdown(generate_certificate_html(medal), unsafe_allow_html=True)
        if week_pct >= WEEKLY_MEDAL_THRESHOLD * 100 and current_week not in cert_weeks:
            st.balloons()
    else:
        st.markdown(
            '<div class="glass-card" style="text-align:center;color:#94A3B8;">'
            "Complete ≥80% of your weekly micro-topic target to unlock your first certificate!</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("##### 📊 Weekly History")
    for w in range(1, current_week + 1):
        w_start = calendar_date_for_day((w - 1) * 7 + 1).strftime("%d %b")
        w_end = calendar_date_for_day(min(w * 7, TOTAL_PLAN_DAYS)).strftime("%d %b")
        w_done = count_topics_mastered_in_week(w)
        w_hrs = get_weekly_hours(w)
        has_medal = any(m["week"] == w for m in ss.gold_medals)
        badge = "🥇" if has_medal else ("✅" if w_done >= WEEKLY_MEDAL_THRESHOLD * week_target else "⏳")
        st.markdown(f"{badge} **Week {w}** ({w_start} – {w_end}): {w_done}/{week_target} topics · {w_hrs:.1f}h")

# ------------------------------------------------------------ REVISION TAB
with tab_revision:
    st.markdown("#### 🔄 Rolling Revision Engine — 25 Fresh + 25×3 Rolling")
    st.caption("Daily target: 100 items = 25 Fresh + 25 Yesterday + 25 (2d ago) + 25 (3d ago)")

    with st.form("add_vocab_form", clear_on_submit=True):
        vc1, vc2, vc3 = st.columns([2, 3, 2])
        with vc1:
            v_cat = st.selectbox("Category", ["OWS", "Idiom", "Synonym/Antonym", "Static GK/GS Fact"])
        with vc2:
            v_term = st.text_input("Term / Fact")
        with vc3:
            v_meaning = st.text_input("Meaning / Detail")
        submitted = st.form_submit_button("➕ Add to Rolling Pool", type="primary")
        if submitted and v_term.strip():
            ss.vocab_items.append({
                "id": ss.vocab_next_id, "term": v_term, "meaning": v_meaning,
                "category": v_cat, "day_added": ss.active_day, "reviewed_days": set(),
            })
            ss.vocab_next_id += 1
            st.rerun()

    st.markdown("---")
    buckets = {"Fresh Today": [], "Yesterday": [], "2 Days Ago": [], "3 Days Ago": []}
    for item in ss.vocab_items:
        b = day_bucket(item["day_added"], ss.active_day)
        if b in buckets:
            buckets[b].append(item)

    bcols = st.columns(4)
    for i, (bname, items) in enumerate(buckets.items()):
        with bcols[i]:
            reviewed_count = sum(1 for it in items if ss.active_day in it["reviewed_days"])
            st.markdown(f"**{bname}**")
            st.progress(min(reviewed_count / 25, 1.0), text=f"{reviewed_count}/25 reviewed")
            for it in items[:25]:
                checked = ss.active_day in it["reviewed_days"]
                new_val = st.checkbox(f"{it['term']} — {it['category']}", value=checked, key=f"vocab_{it['id']}")
                if new_val and not checked:
                    it["reviewed_days"].add(ss.active_day)
                elif not new_val and checked:
                    it["reviewed_days"].discard(ss.active_day)

    if not ss.vocab_items:
        st.caption("No items yet. Add vocabulary or static GK facts above.")

# ------------------------------------------------------------- GRAMMAR TAB
with tab_grammar:
    st.markdown(f"#### 📖 Grammar Micro-Topics ({len(GRAMMAR_TOPICS)} concepts) — 4-Stage Checklist")
    search = st.text_input("🔎 Filter topics", "", key="grammar_search")
    filtered = [t for t in GRAMMAR_TOPICS if search.lower() in t.lower()] if search else GRAMMAR_TOPICS

    g_mastered = sum(1 for t in GRAMMAR_TOPICS if is_topic_mastered(ensure_micro_state(grammar_key(t))))
    st.progress(g_mastered / len(GRAMMAR_TOPICS), text=f"{g_mastered}/{len(GRAMMAR_TOPICS)} Fully Mastered")

    hdr = st.columns([3, 1, 1, 1, 1, 1])
    hdr[0].markdown("**Topic**")
    for i, lbl in enumerate(STAGE_LABELS):
        hdr[i + 1].markdown(f'<div class="micro-stage-header">{lbl}</div>', unsafe_allow_html=True)
    hdr[5].markdown('<div class="micro-stage-header">Lecture</div>', unsafe_allow_html=True)

    for t in filtered:
        render_micro_checklist(grammar_key(t), "gr", t, show_youtube=True)

# --------------------------------------------------------------- SPEED TAB
with tab_speed:
    st.markdown("#### 🎯 Testbook-Style Mock Test Hub (700+ Target)")
    sectional_count, full_count, subj_counts = mock_hub_counts()

    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown("**Sectional Mocks** (Target: 500)")
        st.progress(sectional_count / MOCK_SECTIONAL_TARGET, text=f"{sectional_count} / {MOCK_SECTIONAL_TARGET}")
    with mc2:
        st.markdown("**Full-Length Mocks** (Target: 200)")
        st.progress(full_count / MOCK_FULL_TARGET, text=f"{full_count} / {MOCK_FULL_TARGET}")

    scols = st.columns(4)
    for i, subj in enumerate(SUBJECT_ORDER):
        with scols[i]:
            st.markdown(f"**{subj}** Sectional")
            st.progress(subj_counts[subj] / MOCK_SECTIONAL_PER_SUBJECT, text=f"{subj_counts[subj]} / {MOCK_SECTIONAL_PER_SUBJECT}")

    st.markdown("---")
    with st.form("mock_hub_form", clear_on_submit=True):
        st.markdown("##### Log Mock Test")
        mh1, mh2, mh3 = st.columns(3)
        with mh1:
            mh_date = st.date_input("Date", value=date.today())
            mh_type = st.selectbox("Type", ["Sectional", "Full Length"])
        with mh2:
            mh_subject = st.selectbox("Subject", ["N/A"] + SUBJECT_ORDER)
            mh_score = st.number_input("Score", min_value=0, max_value=500, value=20)
        with mh3:
            mh_total = st.number_input("Total Marks", min_value=1, max_value=500, value=25)
            mh_pctile = st.number_input("Percentile", min_value=0.0, max_value=100.0, value=75.0)
        if st.form_submit_button("➕ Log Mock", type="primary"):
            accuracy = (mh_score / mh_total * 100) if mh_total > 0 else 0
            ss.mock_hub_logs.append({
                "date": mh_date.isoformat(),
                "day": ss.active_day,
                "type": mh_type,
                "subject": mh_subject if mh_type == "Sectional" else "All",
                "score": mh_score,
                "total": mh_total,
                "accuracy": round(accuracy, 1),
                "percentile": mh_pctile,
            })
            st.rerun()

    if ss.mock_hub_logs:
        st.markdown("##### Recent Mock Hub Logs")
        st.dataframe(ss.mock_hub_logs[::-1][:20], use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### ⚡ Sectional Speed Test Log")
    with st.form("speed_form", clear_on_submit=True):
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            sp_subject = st.selectbox("Subject", SUBJECT_ORDER, key="speed_subject")
        with sc2:
            sp_score = st.number_input("Correct", min_value=0, max_value=100, value=20)
        with sc3:
            sp_total = st.number_input("Total Qs", min_value=1, max_value=100, value=25)
        with sc4:
            sp_minutes = st.number_input("Minutes Taken", min_value=1, max_value=60, value=18)
        if st.form_submit_button("➕ Log Speed Test", type="primary"):
            ss.speed_test_log.append({
                "day": ss.active_day, "subject": sp_subject, "score": sp_score,
                "total": sp_total, "minutes": sp_minutes,
            })
            st.rerun()

    if ss.speed_test_log:
        st.markdown("##### Recent Speed Tests")
        for log in ss.speed_test_log[-8:][::-1]:
            acc = log["score"] / log["total"] * 100
            st.markdown(
                f'<div class="topic-row">Day {log["day"]} — <b>{log["subject"]}</b>: '
                f'{log["score"]}/{log["total"]} ({acc:.0f}%) in {log["minutes"]} min</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("#### 📝 Mock Test Error Log")
    with st.form("mock_form", clear_on_submit=True):
        mc1, mc2 = st.columns(2)
        with mc1:
            m_name = st.text_input("Exam / Mock Name")
            m_score = st.text_input("Score (e.g. 132/200)")
            m_weak = st.text_input("Weak Area")
        with mc2:
            m_incorrect = st.text_area("Incorrect Questions (one per line)")
            m_reason = st.selectbox("Reason", ["Conceptual Gap", "Calculation Error", "Rushed / Time Pressure", "Silly Mistake", "Unattempted"])
            m_concept = st.text_area("Correct Concept / Fix")
        if st.form_submit_button("➕ Add to Error Log", type="primary") and m_name.strip():
            ss.mock_logs.append({
                "day": ss.active_day, "exam_name": m_name, "score": m_score, "weak_area": m_weak or "General",
                "incorrect_qs": m_incorrect, "reason": m_reason, "concept": m_concept,
            })
            st.rerun()

    if ss.mock_logs:
        st.markdown("##### 📌 Weekend Revision Focus")
        weak_freq = {}
        for log in ss.mock_logs:
            weak_freq[log["weak_area"]] = weak_freq.get(log["weak_area"], 0) + 1
        for area, count in sorted(weak_freq.items(), key=lambda x: -x[1]):
            st.markdown(f'<span class="pill pill-red">{area} ×{count}</span>', unsafe_allow_html=True)

        st.markdown("##### Full Error Log")
        for log in ss.mock_logs[::-1]:
            with st.expander(f"Day {log['day']} — {log['exam_name']} — {log['score']}"):
                st.markdown(f"**Weak Area:** {log['weak_area']}  \n**Reason:** {log['reason']}")
                st.markdown(f"**Incorrect Qs:**\n{log['incorrect_qs']}")
                st.markdown(f"**Correct Concept:**\n{log['concept']}")

# ------------------------------------------------------------- FORMULA TAB
with tab_formula:
    st.markdown("#### 🗂️ Formula Chest & PYQ Bookmarker")
    st.caption("Bookmark difficult PYQs, shortcuts, and formulas for rapid review.")
    with st.form("bookmark_form", clear_on_submit=True):
        bc1, bc2 = st.columns(2)
        with bc1:
            b_type = st.selectbox("Type", ["Formula", "Shortcut", "Difficult PYQ"])
            b_subject = st.selectbox("Subject", SUBJECT_ORDER, key="bookmark_subject")
        with bc2:
            b_content = st.text_area("Content")
        if st.form_submit_button("➕ Bookmark", type="primary") and b_content.strip():
            ss.bookmarks.append({"id": ss.bookmark_next_id, "type": b_type, "subject": b_subject, "content": b_content})
            ss.bookmark_next_id += 1
            st.rerun()

    st.markdown("---")
    filt_subj = st.selectbox("Filter by subject", ["All"] + SUBJECT_ORDER, key="filter_bookmark")
    shown = ss.bookmarks if filt_subj == "All" else [b for b in ss.bookmarks if b["subject"] == filt_subj]
    for b in shown[::-1]:
        cols = st.columns([5, 1])
        with cols[0]:
            st.markdown(
                f'<div class="glass-card"><span class="pill pill-blue">{b["subject"]}</span> '
                f'<span class="pill pill-green">{b["type"]}</span><br><br>{b["content"]}</div>',
                unsafe_allow_html=True,
            )
        with cols[1]:
            if st.button("🗑️ Delete", key=f"del_bm_{b['id']}"):
                ss.bookmarks = [x for x in ss.bookmarks if x["id"] != b["id"]]
                st.rerun()
    if not shown:
        st.caption("No bookmarks yet.")

# --------------------------------------------------------------- RAPID TAB
with tab_rapid:
    st.markdown("#### 🎯 Rapid Mock Mode — 2 Mocks/Day + Deep Analysis")
    if not rapid_mock_active():
        st.info(
            "Rapid Mock Mode activates when syllabus hits 100%, you're in the final 50 days, "
            "or you manually mark syllabus finished in the sidebar."
        )
    else:
        st.success("Rapid Mock Mode is LIVE.")
        days_to_exam = (ss.exam_date - date.today()).days
        st.metric("⏳ Days to Exam", max(days_to_exam, 0))
        st.markdown("##### Daily Checklist")
        st.checkbox("Mock 1 Completed (Full Length, Timed)", key="rapid_mock1")
        st.checkbox("Mock 2 Completed (Full Length, Timed)", key="rapid_mock2")
        st.checkbox("Deep Error Analysis Done for Both Mocks", key="rapid_analysis")
        st.checkbox("Weak Topics Revised from Formula Chest", key="rapid_revision")

        st.markdown("---")
        with st.form("rapid_form", clear_on_submit=True):
            rc1, rc2, rc3, rc4 = st.columns(4)
            with rc1:
                r_no = st.number_input("Mock #", min_value=1, value=1)
            with rc2:
                r_score = st.number_input("Score", min_value=0, max_value=200, value=100)
            with rc3:
                r_acc = st.number_input("Accuracy %", min_value=0.0, max_value=100.0, value=75.0)
            with rc4:
                r_pct = st.number_input("Percentile", min_value=0.0, max_value=100.0, value=90.0)
            if st.form_submit_button("➕ Log Mock Result", type="primary"):
                ss.rapid_mock_log.append({
                    "day": ss.active_day, "mock_no": r_no, "score": r_score,
                    "accuracy": r_acc, "percentile": r_pct,
                })
                st.rerun()

        if ss.rapid_mock_log:
            st.markdown("##### 📈 Score / Percentile Trend")
            scores = [m["score"] for m in ss.rapid_mock_log]
            st.line_chart({"Score": scores})
            st.markdown("##### Log")
            for m in ss.rapid_mock_log[::-1][:15]:
                st.markdown(
                    f'<div class="topic-row">Day {m["day"]} — Mock #{m["mock_no"]}: Score {m["score"]}, '
                    f'Accuracy {m["accuracy"]}%, Percentile {m["percentile"]}</div>',
                    unsafe_allow_html=True,
                )

st.markdown("---")
st.caption("Shiv's Classroom · Testbook-inspired tracker · Session-based · No external database required.")
