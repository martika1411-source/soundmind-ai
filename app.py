import streamlit as st
import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
import warnings
try:
    import langdetect
    LANGDETECT_AVAILABLE = True
except:
    LANGDETECT_AVAILABLE = False
warnings.filterwarnings('ignore')

st.set_page_config(page_title="SoundMind AI", page_icon="🎵", layout="wide")

# Prevodi
TRANSLATIONS = {
    "sl": {
        "title": "✨ SoundMind AI ✨",
        "subtitle": "✦ PROFESIONALNI AI ANALIZATOR GLASBE ✦",
        "enter_lyrics": "🎤 Vnesi besedilo pesmi (za zaznavanje jezika)",
        "lyrics_placeholder": "Prilepi nekaj vrstic besedila pesmi sem...",
        "upload": "🎵 Naloži svojo pesem (MP3 ali WAV)",
        "analyzing": "✨ Analiziram tvojo glasbo... Prosim počakaj!",
        "analysis_done": "✅ Analiza uspešno končana!",
        "results": "📊 Rezultati analize",
        "tempo": "🥁 TEMPO",
        "energy": "⚡ ENERGIJA",
        "duration": "⏱️ TRAJANJE",
        "key": "🎼 TONALITETA",
        "mood_title": "😊 Razpoloženje pesmi",
        "instruments_title": "🎸 Zaznani instrumenti",
        "visual_title": "📈 Vizualna analiza",
        "tips_title": "💡 Priporočila za tvojo pesem",
        "strongest_part": "🔥 Najmočnejši del pesmi je pri",
        "second": "sekundi",
        "radio_title": "📻 Priporočene radijske postaje",
        "best_time": "Najboljši čas predvajanja",
        "markets_title": "🌍 Priporočeni glasbeni trgi",
        "pdf_title": "📄 Prenesi svoje poročilo",
        "pdf_button": "⬇️ PRENESI PDF POROČILO",
        "promo_tip": "🎯 Nasvet za promocijo",
        "promo_desc": "Deli pesem na TikTok, Instagram Reels in YouTube Shorts!",
        "best_post_time": "📱 Najboljši čas objave",
        "best_post_desc": "Objavi med 18:00 in 21:00 za največjo poslušanost",
        "slow_ballad": "🎵 Počasna balada",
        "mid_tempo": "🎵 Srednji tempo",
        "fast_song": "🎵 Hitra pesem",
        "very_fast": "🎵 Zelo hitra",
        "high_energy": "💥 Visoka energija",
        "mid_energy": "✨ Srednja energija",
        "low_energy": "🌙 Nizka energija",
        "good_radio": "📻 Dobra za radio",
        "ideal_length": "✅ Idealna dolžina",
        "too_long": "⚠️ Malo dolga",
        "lang_detected": "✅ Zaznan jezik",
        "lang_not_detected": "🌍 Jezik ni zaznan - uporabljam mednarodni trg",
        "enter_lyrics_tip": "💡 Vnesi besedilo za natančnejše priporočilo radijskih postaj!",
        "welcome1_title": "🎵 Osnovna analiza",
        "welcome1_desc": "🥁 Tempo v BPM<br>⚡ Energija pesmi<br>⏱️ Trajanje<br>🎼 Tonaliteta",
        "welcome2_title": "✨ Napredna analiza",
        "welcome2_desc": "😊 Razpoloženje<br>🎸 Instrumenti<br>📊 Vizualni grafi<br>💡 Priporočila",
        "welcome3_title": "🌍 Bonus funkcije",
        "welcome3_desc": "📻 Radijske postaje<br>📄 PDF poročilo<br>🔥 Vrhunec pesmi<br>📱 Nasveti za promocijo",
        "moods": {
            "energetic": ("🔥 Energično in veselo", "Pesem je polna energije in pozitivnih vibracij!"),
            "melancholic": ("😢 Melanholično in čustveno", "Pesem prenaša globoka čustva in nostalgijo."),
            "relaxed": ("😌 Sproščeno in pozitivno", "Lahkotna in prijetna pesem."),
            "dramatic": ("💪 Močno in dramatično", "Pesem ima dramatičen in močan občutek."),
            "balanced": ("🎵 Uravnoteženo", "Pesem ima uravnoteženo razpoloženje.")
        },
        "instruments": {
            "electric_guitar": "🎸 Električna kitara",
            "piano": "🎹 Piano",
            "drums": "🥁 Bobni",
            "strings": "🎻 Godala",
            "vocals": "🎤 Vokal",
            "acoustic": "🎵 Akustični instrumenti"
        },
        "chorus_late": "⚠️ Vrhunec pesmi pride prepozno! Razmisli o premiku.",
        "chorus_early": "⚠️ Vrhunec pride zelo zgodaj!",
        "chorus_ok": "✅ Vrhunec pesmi je na odličnem mestu!",
        "advice": "💡 Nasvet",
        "choose_language": "🌍 Izberi jezik strani",
    },
    "en": {
        "title": "✨ SoundMind AI ✨",
        "subtitle": "✦ PROFESSIONAL AI MUSIC ANALYZER ✦",
        "enter_lyrics": "🎤 Enter song lyrics (for language detection)",
        "lyrics_placeholder": "Paste a few lines of song lyrics here...",
        "upload": "🎵 Upload your song (MP3 or WAV)",
        "analyzing": "✨ Analyzing your music... Please wait!",
        "analysis_done": "✅ Analysis successfully completed!",
        "results": "📊 Analysis Results",
        "tempo": "🥁 TEMPO",
        "energy": "⚡ ENERGY",
        "duration": "⏱️ DURATION",
        "key": "🎼 KEY",
        "mood_title": "😊 Song Mood",
        "instruments_title": "🎸 Detected Instruments",
        "visual_title": "📈 Visual Analysis",
        "tips_title": "💡 Recommendations for your song",
        "strongest_part": "🔥 The strongest part of the song is at",
        "second": "second",
        "radio_title": "📻 Recommended Radio Stations",
        "best_time": "Best airtime",
        "markets_title": "🌍 Recommended Music Markets",
        "pdf_title": "📄 Download your report",
        "pdf_button": "⬇️ DOWNLOAD PDF REPORT",
        "promo_tip": "🎯 Promotion tip",
        "promo_desc": "Share your song on TikTok, Instagram Reels and YouTube Shorts!",
        "best_post_time": "📱 Best posting time",
        "best_post_desc": "Post between 6PM and 9PM for maximum listeners",
        "slow_ballad": "🎵 Slow ballad",
        "mid_tempo": "🎵 Mid tempo",
        "fast_song": "🎵 Fast song",
        "very_fast": "🎵 Very fast",
        "high_energy": "💥 High energy",
        "mid_energy": "✨ Medium energy",
        "low_energy": "🌙 Low energy",
        "good_radio": "📻 Good for radio",
        "ideal_length": "✅ Ideal length",
        "too_long": "⚠️ A bit long",
        "lang_detected": "✅ Detected language",
        "lang_not_detected": "🌍 Language not detected - using international market",
        "enter_lyrics_tip": "💡 Enter lyrics for more accurate radio station recommendations!",
        "welcome1_title": "🎵 Basic Analysis",
        "welcome1_desc": "🥁 Tempo in BPM<br>⚡ Song energy<br>⏱️ Duration<br>🎼 Key",
        "welcome2_title": "✨ Advanced Analysis",
        "welcome2_desc": "😊 Mood<br>🎸 Instruments<br>📊 Visual graphs<br>💡 Recommendations",
        "welcome3_title": "🌍 Bonus Features",
        "welcome3_desc": "📻 Radio stations<br>📄 PDF report<br>🔥 Song peak<br>📱 Promotion tips",
        "moods": {
            "energetic": ("🔥 Energetic and happy", "The song is full of energy and positive vibes!"),
            "melancholic": ("😢 Melancholic and emotional", "The song conveys deep emotions and nostalgia."),
            "relaxed": ("😌 Relaxed and positive", "A light and pleasant song."),
            "dramatic": ("💪 Powerful and dramatic", "The song has a dramatic and powerful feel."),
            "balanced": ("🎵 Balanced", "The song has a balanced mood.")
        },
        "instruments": {
            "electric_guitar": "🎸 Electric Guitar",
            "piano": "🎹 Piano",
            "drums": "🥁 Drums",
            "strings": "🎻 Strings",
            "vocals": "🎤 Vocals",
            "acoustic": "🎵 Acoustic Instruments"
        },
        "chorus_late": "⚠️ Song peak comes too late! Consider moving it earlier.",
        "chorus_early": "⚠️ Peak comes very early!",
        "chorus_ok": "✅ Song peak is in an excellent position!",
        "advice": "💡 Tip",
        "choose_language": "🌍 Choose page language",
    },
    "fr": {
        "title": "✨ SoundMind AI ✨",
        "subtitle": "✦ ANALYSEUR MUSICAL AI PROFESSIONNEL ✦",
        "enter_lyrics": "🎤 Entrez les paroles (pour détecter la langue)",
        "lyrics_placeholder": "Collez quelques lignes de paroles ici...",
        "upload": "🎵 Téléchargez votre chanson (MP3 ou WAV)",
        "analyzing": "✨ Analyse de votre musique... Veuillez patienter!",
        "analysis_done": "✅ Analyse terminée avec succès!",
        "results": "📊 Résultats de l'analyse",
        "tempo": "🥁 TEMPO",
        "energy": "⚡ ÉNERGIE",
        "duration": "⏱️ DURÉE",
        "key": "🎼 TONALITÉ",
        "mood_title": "😊 Ambiance de la chanson",
        "instruments_title": "🎸 Instruments détectés",
        "visual_title": "📈 Analyse visuelle",
        "tips_title": "💡 Recommandations pour votre chanson",
        "strongest_part": "🔥 La partie la plus forte est à",
        "second": "seconde",
        "radio_title": "📻 Stations de radio recommandées",
        "best_time": "Meilleure heure de diffusion",
        "markets_title": "🌍 Marchés musicaux recommandés",
        "pdf_title": "📄 Téléchargez votre rapport",
        "pdf_button": "⬇️ TÉLÉCHARGER LE RAPPORT PDF",
        "promo_tip": "🎯 Conseil de promotion",
        "promo_desc": "Partagez votre chanson sur TikTok, Instagram Reels et YouTube Shorts!",
        "best_post_time": "📱 Meilleur moment pour publier",
        "best_post_desc": "Publiez entre 18h et 21h pour un maximum d'auditeurs",
        "slow_ballad": "🎵 Ballade lente",
        "mid_tempo": "🎵 Tempo moyen",
        "fast_song": "🎵 Chanson rapide",
        "very_fast": "🎵 Très rapide",
        "high_energy": "💥 Haute énergie",
        "mid_energy": "✨ Énergie moyenne",
        "low_energy": "🌙 Faible énergie",
        "good_radio": "📻 Bonne pour la radio",
        "ideal_length": "✅ Durée idéale",
        "too_long": "⚠️ Un peu longue",
        "lang_detected": "✅ Langue détectée",
        "lang_not_detected": "🌍 Langue non détectée - marché international",
        "enter_lyrics_tip": "💡 Entrez les paroles pour des recommandations plus précises!",
        "welcome1_title": "🎵 Analyse de base",
        "welcome1_desc": "🥁 Tempo en BPM<br>⚡ Énergie<br>⏱️ Durée<br>🎼 Tonalité",
        "welcome2_title": "✨ Analyse avancée",
        "welcome2_desc": "😊 Ambiance<br>🎸 Instruments<br>📊 Graphiques<br>💡 Recommandations",
        "welcome3_title": "🌍 Fonctions bonus",
        "welcome3_desc": "📻 Stations radio<br>📄 Rapport PDF<br>🔥 Pic de la chanson<br>📱 Conseils promo",
        "moods": {
            "energetic": ("🔥 Énergique et joyeux", "La chanson est pleine d'énergie et de bonnes vibrations!"),
            "melancholic": ("😢 Mélancolique et émotionnel", "La chanson transmet des émotions profondes."),
            "relaxed": ("😌 Détendu et positif", "Une chanson légère et agréable."),
            "dramatic": ("💪 Puissant et dramatique", "La chanson a un sentiment dramatique."),
            "balanced": ("🎵 Équilibré", "La chanson a une ambiance équilibrée.")
        },
        "instruments": {
            "electric_guitar": "🎸 Guitare électrique",
            "piano": "🎹 Piano",
            "drums": "🥁 Batterie",
            "strings": "🎻 Cordes",
            "vocals": "🎤 Voix",
            "acoustic": "🎵 Instruments acoustiques"
        },
        "chorus_late": "⚠️ Le pic arrive trop tard! Envisagez de le déplacer.",
        "chorus_early": "⚠️ Le pic arrive très tôt!",
        "chorus_ok": "✅ Le pic de la chanson est à une excellente position!",
        "advice": "💡 Conseil",
        "choose_language": "🌍 Choisissez la langue de la page",
    },
    "es": {
        "title": "✨ SoundMind AI ✨",
        "subtitle": "✦ ANALIZADOR MUSICAL AI PROFESIONAL ✦",
        "enter_lyrics": "🎤 Ingresa la letra (para detectar el idioma)",
        "lyrics_placeholder": "Pega algunas líneas de la letra aquí...",
        "upload": "🎵 Sube tu canción (MP3 o WAV)",
        "analyzing": "✨ Analizando tu música... ¡Por favor espera!",
        "analysis_done": "✅ ¡Análisis completado con éxito!",
        "results": "📊 Resultados del análisis",
        "tempo": "🥁 TEMPO",
        "energy": "⚡ ENERGÍA",
        "duration": "⏱️ DURACIÓN",
        "key": "🎼 TONALIDAD",
        "mood_title": "😊 Estado de ánimo de la canción",
        "instruments_title": "🎸 Instrumentos detectados",
        "visual_title": "📈 Análisis visual",
        "tips_title": "💡 Recomendaciones para tu canción",
        "strongest_part": "🔥 La parte más fuerte de la canción está en el",
        "second": "segundo",
        "radio_title": "📻 Estaciones de radio recomendadas",
        "best_time": "Mejor horario de emisión",
        "markets_title": "🌍 Mercados musicales recomendados",
        "pdf_title": "📄 Descarga tu informe",
        "pdf_button": "⬇️ DESCARGAR INFORME PDF",
        "promo_tip": "🎯 Consejo de promoción",
        "promo_desc": "¡Comparte tu canción en TikTok, Instagram Reels y YouTube Shorts!",
        "best_post_time": "📱 Mejor hora para publicar",
        "best_post_desc": "Publica entre las 18:00 y las 21:00 para máxima audiencia",
        "slow_ballad": "🎵 Balada lenta",
        "mid_tempo": "🎵 Tempo medio",
        "fast_song": "🎵 Canción rápida",
        "very_fast": "🎵 Muy rápida",
        "high_energy": "💥 Alta energía",
        "mid_energy": "✨ Energía media",
        "low_energy": "🌙 Baja energía",
        "good_radio": "📻 Buena para radio",
        "ideal_length": "✅ Duración ideal",
        "too_long": "⚠️ Un poco larga",
        "lang_detected": "✅ Idioma detectado",
        "lang_not_detected": "🌍 Idioma no detectado - mercado internacional",
        "enter_lyrics_tip": "💡 Ingresa la letra para recomendaciones más precisas!",
        "welcome1_title": "🎵 Análisis básico",
        "welcome1_desc": "🥁 Tempo en BPM<br>⚡ Energía<br>⏱️ Duración<br>🎼 Tonalidad",
        "welcome2_title": "✨ Análisis avanzado",
        "welcome2_desc": "😊 Estado de ánimo<br>🎸 Instrumentos<br>📊 Gráficos<br>💡 Recomendaciones",
        "welcome3_title": "🌍 Funciones extra",
        "welcome3_desc": "📻 Estaciones de radio<br>📄 Informe PDF<br>🔥 Pico de la canción<br>📱 Consejos de promoción",
        "moods": {
            "energetic": ("🔥 Energético y alegre", "¡La canción está llena de energía y buenas vibras!"),
            "melancholic": ("😢 Melancólico y emotivo", "La canción transmite emociones profundas."),
            "relaxed": ("😌 Relajado y positivo", "Una canción ligera y agradable."),
            "dramatic": ("💪 Poderoso y dramático", "La canción tiene un sentimiento dramático."),
            "balanced": ("🎵 Equilibrado", "La canción tiene un estado de ánimo equilibrado.")
        },
        "instruments": {
            "electric_guitar": "🎸 Guitarra eléctrica",
            "piano": "🎹 Piano",
            "drums": "🥁 Batería",
            "strings": "🎻 Cuerdas",
            "vocals": "🎤 Voz",
            "acoustic": "🎵 Instrumentos acústicos"
        },
        "chorus_late": "⚠️ ¡El pico llega demasiado tarde! Considera moverlo antes.",
        "chorus_early": "⚠️ ¡El pico llega muy temprano!",
        "chorus_ok": "✅ ¡El pico de la canción está en una posición excelente!",
        "advice": "💡 Consejo",
        "choose_language": "🌍 Elige el idioma de la página",
    },
    "zh": {
        "title": "✨ SoundMind AI ✨",
        "subtitle": "✦ 专业AI音乐分析器 ✦",
        "enter_lyrics": "🎤 输入歌词（用于语言检测）",
        "lyrics_placeholder": "在此粘贴几行歌词...",
        "upload": "🎵 上传您的歌曲（MP3或WAV）",
        "analyzing": "✨ 正在分析您的音乐...请稍候！",
        "analysis_done": "✅ 分析成功完成！",
        "results": "📊 分析结果",
        "tempo": "🥁 节奏",
        "energy": "⚡ 能量",
        "duration": "⏱️ 时长",
        "key": "🎼 调性",
        "mood_title": "😊 歌曲情绪",
        "instruments_title": "🎸 检测到的乐器",
        "visual_title": "📈 可视化分析",
        "tips_title": "💡 歌曲建议",
        "strongest_part": "🔥 歌曲最强部分在第",
        "second": "秒",
        "radio_title": "📻 推荐电台",
        "best_time": "最佳播出时间",
        "markets_title": "🌍 推荐音乐市场",
        "pdf_title": "📄 下载报告",
        "pdf_button": "⬇️ 下载PDF报告",
        "promo_tip": "🎯 推广建议",
        "promo_desc": "在TikTok、Instagram Reels和YouTube Shorts上分享您的歌曲！",
        "best_post_time": "📱 最佳发布时间",
        "best_post_desc": "在18:00至21:00之间发布，获得最多听众",
        "slow_ballad": "🎵 慢歌/抒情曲",
        "mid_tempo": "🎵 中等节奏",
        "fast_song": "🎵 快歌",
        "very_fast": "🎵 非常快",
        "high_energy": "💥 高能量",
        "mid_energy": "✨ 中等能量",
        "low_energy": "🌙 低能量",
        "good_radio": "📻 适合电台",
        "ideal_length": "✅ 理想时长",
        "too_long": "⚠️ 稍长",
        "lang_detected": "✅ 检测到的语言",
        "lang_not_detected": "🌍 未检测到语言 - 使用国际市场",
        "enter_lyrics_tip": "💡 输入歌词以获得更准确的电台推荐！",
        "welcome1_title": "🎵 基本分析",
        "welcome1_desc": "🥁 BPM节奏<br>⚡ 歌曲能量<br>⏱️ 时长<br>🎼 调性",
        "welcome2_title": "✨ 高级分析",
        "welcome2_desc": "😊 情绪<br>🎸 乐器<br>📊 可视化图表<br>💡 建议",
        "welcome3_title": "🌍 额外功能",
        "welcome3_desc": "📻 电台推荐<br>📄 PDF报告<br>🔥 歌曲高潮<br>📱 推广建议",
        "moods": {
            "energetic": ("🔥 充满活力和快乐", "这首歌充满能量和积极的氛围！"),
            "melancholic": ("😢 忧郁而感性", "这首歌传达深刻的情感和怀旧之情。"),
            "relaxed": ("😌 放松而积极", "轻松愉快的歌曲。"),
            "dramatic": ("💪 强劲而戏剧化", "这首歌具有戏剧性和强烈的感觉。"),
            "balanced": ("🎵 均衡", "这首歌情绪均衡。")
        },
        "instruments": {
            "electric_guitar": "🎸 电吉他",
            "piano": "🎹 钢琴",
            "drums": "🥁 鼓",
            "strings": "🎻 弦乐",
            "vocals": "🎤 人声",
            "acoustic": "🎵 原声乐器"
        },
        "chorus_late": "⚠️ 歌曲高潮来得太晚！考虑提前。",
        "chorus_early": "⚠️ 高潮来得太早！",
        "chorus_ok": "✅ 歌曲高潮位置非常好！",
        "advice": "💡 建议",
        "choose_language": "🌍 选择页面语言",
    }
}

def get_radio_stations(language, tempo, energy_percent):
    if language == "sl":
        return {
            "ime": "🇸🇮 SLOVENIJA",
            "postaje": [
                {"postaja": "Val 202", "cas": "07:00 - 09:00 in 17:00 - 19:00", "opis": "Največja slovenska pop radijska postaja"},
                {"postaja": "Radio 1", "cas": "08:00 - 10:00 in 16:00 - 18:00", "opis": "Primerna za pop in mainstream glasbo"},
                {"postaja": "Antena", "cas": "07:00 - 09:00", "opis": "Dobra za domačo glasbo"},
                {"postaja": "Radio Ognjisce", "cas": "09:00 - 12:00", "opis": "Primerna za bolj umirjeno glasbo"},
            ],
            "nasvet": "Kontaktiraj uredništvo direktno ali pošlji pesem na info@val202.si"
        }
    elif language == "hr":
        return {
            "ime": "🇭🇷 HRVAŠKA",
            "postaje": [
                {"postaja": "HRT Radio 2", "cas": "07:00 - 09:00 in 17:00 - 19:00", "opis": "Največja hrvaška pop postaja"},
                {"postaja": "Narodni Radio", "cas": "08:00 - 10:00", "opis": "Primerna za domačo glasbo"},
                {"postaja": "Radio Yammat", "cas": "12:00 - 15:00", "opis": "Mlado občinstvo, pop glasba"},
            ],
            "nasvet": "Pošlji demo na hrvaške radijske postaje direktno"
        }
    elif language == "de":
        return {
            "ime": "🇩🇪 NEMČIJA / AVSTRIJA",
            "postaje": [
                {"postaja": "SWR3", "cas": "07:00 - 09:00 in 17:00 - 19:00", "opis": "Ena največjih nemških pop postaj"},
                {"postaja": "Ö3 (Avstrija)", "cas": "07:00 - 09:00", "opis": "Največja avstrijska pop postaja"},
                {"postaja": "NDR 2", "cas": "08:00 - 10:00 in 16:00 - 18:00", "opis": "Primerna za mainstream pop"},
            ],
            "nasvet": "Nemske postaje sprejemajo demo prek uradnih spletnih obrazcev"
        }
    elif language == "it":
        return {
            "ime": "🇮🇹 ITALIJA",
            "postaje": [
                {"postaja": "RTL 102.5", "cas": "07:00 - 09:00 in 17:00 - 19:00", "opis": "Najpopularnejša italijanska pop postaja"},
                {"postaja": "Radio DeeJay", "cas": "08:00 - 11:00", "opis": "Mlado občinstvo, dance in pop"},
                {"postaja": "RDS", "cas": "07:00 - 09:00", "opis": "Mainstream pop postaja"},
            ],
            "nasvet": "V Italiji je pomembno imeti glasbenega agenta za doseg do postaj"
        }
    elif language == "fr":
        return {
            "ime": "🇫🇷 FRANCIJA",
            "postaje": [
                {"postaja": "NRJ", "cas": "07:00 - 09:00 in 17:00 - 19:00", "opis": "Največja francoska pop postaja"},
                {"postaja": "Fun Radio", "cas": "10:00 - 13:00", "opis": "Dance in elektronska glasba"},
                {"postaja": "Skyrock", "cas": "08:00 - 10:00", "opis": "Hip-hop in R&B"},
            ],
            "nasvet": "Francija ima kvoto za domačo glasbo - tuje pesmi imajo omejeno predvajanje"
        }
    elif language == "es":
        return {
            "ime": "🇪🇸 ŠPANIJA / LATINSKA AMERIKA",
            "postaje": [
                {"postaja": "Los 40 Principales", "cas": "07:00 - 09:00 in 17:00 - 19:00", "opis": "Največja španska pop postaja"},
                {"postaja": "Europa FM", "cas": "08:00 - 10:00", "opis": "Mainstream pop in dance"},
                {"postaja": "Radio Latina", "cas": "10:00 - 13:00", "opis": "Latinska glasba"},
            ],
            "nasvet": "Španski trg je velik - kontaktiraj agencije v Madridu ali Barceloni"
        }
    elif language == "zh":
        return {
            "ime": "🇨🇳 KITAJSKA",
            "postaje": [
                {"postaja": "China National Radio", "cas": "07:00 - 09:00 in 17:00 - 19:00", "opis": "Največja kitajska radijska postaja"},
                {"postaja": "Hit FM Beijing", "cas": "08:00 - 10:00", "opis": "Pop in mlada glasba"},
                {"postaja": "Dragon FM", "cas": "12:00 - 15:00", "opis": "Mednarodna glasba v Shanghaju"},
            ],
            "nasvet": "Kitajski trg zahteva lokalne partnerje in registracijo glasbe"
        }
    elif language == "pt":
        return {
            "ime": "🇧🇷 BRAZILIJA / PORTUGAL",
            "postaje": [
                {"postaja": "Jovem Pan", "cas": "07:00 - 09:00 in 17:00 - 19:00", "opis": "Največja brazilska pop postaja"},
                {"postaja": "Antena 1 Portugal", "cas": "08:00 - 10:00", "opis": "Primerna za pop glasbo"},
            ],
            "nasvet": "Brazilija je ogromen trg - razmisli o lokalizaciji glasbe"
        }
    else:
        if tempo > 120:
            return {
                "ime": "🌍 MEDNARODNI TRG - Dance/Pop",
                "postaje": [
                    {"postaja": "BBC Radio 1 (UK)", "cas": "07:00 - 09:00 in 17:00 - 19:00", "opis": "Najprestižnejša pop postaja na svetu"},
                    {"postaja": "Z100 New York (USA)", "cas": "06:00 - 09:00", "opis": "Največja pop postaja v ZDA"},
                    {"postaja": "Kiss FM (UK)", "cas": "08:00 - 11:00", "opis": "Dance in urban glasba"},
                ],
                "nasvet": "Za mednarodni trg potrebujes glasbenega menedzerja ali agenta"
            }
        elif tempo < 90:
            return {
                "ime": "🌍 MEDNARODNI TRG - Ballad/Pop",
                "postaje": [
                    {"postaja": "BBC Radio 2 (UK)", "cas": "09:00 - 12:00 in 15:00 - 17:00", "opis": "Primerna za balade in soft pop"},
                    {"postaja": "Smooth Radio (UK)", "cas": "08:00 - 11:00", "opis": "Idealna za pocasne melodicne pesmi"},
                    {"postaja": "Easy 97.9 (USA)", "cas": "07:00 - 10:00", "opis": "Adult contemporary format"},
                ],
                "nasvet": "Balade so popularne v Aziji - razmisli o japonskem in korejskem trgu"
            }
        else:
            return {
                "ime": "🌍 MEDNARODNI TRG - Pop",
                "postaje": [
                    {"postaja": "BBC Radio 1 (UK)", "cas": "07:00 - 09:00 in 17:00 - 19:00", "opis": "Najprestiznejsa pop postaja"},
                    {"postaja": "Hot 100 Radio (USA)", "cas": "06:00 - 09:00", "opis": "Top 100 format"},
                    {"postaja": "Virgin Radio", "cas": "07:00 - 09:00", "opis": "Mainstream pop format"},
                ],
                "nasvet": "Registriraj glasbo pri PRO (SAZAS v Sloveniji) za avtorske pravice"
            }

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
    .stApp {
        background: linear-gradient(135deg, #1a0033 0%, #2d0057 40%, #1a0033 100%);
    }
    .big-title {
        font-size: 4em;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #ff69b4, #da70d6, #9b59b6, #ff1493);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 20px;
        letter-spacing: 2px;
    }
    .subtitle {
        font-size: 1.4em;
        text-align: center;
        color: #da70d6;
        margin-bottom: 30px;
        font-weight: 300;
        letter-spacing: 3px;
    }
    .result-box {
        background: linear-gradient(135deg, rgba(255,105,180,0.2), rgba(147,0,211,0.2));
        border-radius: 20px;
        padding: 25px;
        border: 2px solid #ff69b4;
        margin: 15px 0;
        text-align: center;
    }
    .result-box h2 { color: #ff69b4; font-size: 2em; font-weight: 700; }
    .result-box p { color: #e0b0ff; font-size: 1.2em; }
    .instrument-box {
        background: linear-gradient(135deg, rgba(218,112,214,0.3), rgba(255,20,147,0.2));
        border-radius: 15px;
        padding: 20px;
        border: 2px solid #da70d6;
        text-align: center;
        font-size: 1.3em;
        color: white;
        font-weight: 600;
    }
    .radio-box {
        background: linear-gradient(135deg, rgba(255,20,147,0.2), rgba(147,0,211,0.3));
        border-radius: 15px;
        padding: 20px;
        border: 2px solid #ff1493;
        margin: 10px 0;
        color: white;
    }
    .radio-box h4 { color: #ff69b4; font-size: 1.3em; margin-bottom: 10px; }
    .radio-box p { color: #e0b0ff; font-size: 1.1em; line-height: 1.8; }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,105,180,0.2), rgba(147,0,211,0.3));
        border: 2px solid #ff69b4;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
    }
    div[data-testid="metric-container"] label { color: #ff69b4 !important; font-size: 1.2em !important; font-weight: 700 !important; }
    div[data-testid="metric-container"] div { color: white !important; font-size: 2em !important; font-weight: 900 !important; }
    .stButton > button {
        background: linear-gradient(90deg, #ff69b4, #9b59b6);
        color: white; border: none; border-radius: 25px;
        padding: 15px 40px; font-size: 1.2em; font-weight: 700;
        width: 100%; cursor: pointer; letter-spacing: 1px;
    }
    h1, h2, h3 { color: #ff69b4 !important; font-weight: 700 !important; }
    .welcome-box {
        background: linear-gradient(135deg, rgba(255,105,180,0.15), rgba(147,0,211,0.15));
        border-radius: 20px; padding: 30px;
        border: 2px solid rgba(255,105,180,0.4);
        text-align: center; margin: 10px;
    }
    .welcome-box h3 { color: #ff69b4 !important; font-size: 1.5em !important; }
    .welcome-box p { color: #e0b0ff; font-size: 1.1em; line-height: 2; }
    div[data-testid="stMarkdownContainer"] p { color: #e0b0ff; font-size: 1.1em; }
    [data-testid="stFileUploader"] {
        background: rgba(255,105,180,0.1);
        border-radius: 20px; padding: 20px;
        border: 2px dashed #ff69b4;
    }
    [data-testid="stFileUploader"] p {
        font-weight: 400 !important; text-shadow: none !important;
        -webkit-text-stroke: 0px !important;
        color: #e0b0ff !important; font-size: 1.1em !important;
    }
    [data-testid="stFileUploader"] span {
        font-weight: 400 !important; text-shadow: none !important;
        -webkit-text-stroke: 0px !important;
    }
</style>
""", unsafe_allow_html=True)

# Izbira jezika strani
lang_options = {
    "🇸🇮 Slovenščina": "sl",
    "🇬🇧 English": "en",
    "🇫🇷 Français": "fr",
    "🇪🇸 Español": "es",
    "🇨🇳 中文": "zh"
}

selected_lang_name = st.selectbox(
    "🌍 Izberi jezik / Choose language / Choisir la langue / Elegir idioma / 选择语言",
    list(lang_options.keys())
)
ui_lang = lang_options[selected_lang_name]
t = TRANSLATIONS[ui_lang]

# Naslov
st.markdown(f'<p class="big-title">{t["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">{t["subtitle"]}</p>', unsafe_allow_html=True)
st.markdown("---")

lyrics_input = st.text_area(t["enter_lyrics"], placeholder=t["lyrics_placeholder"], height=100)
uploaded_file = st.file_uploader(t["upload"], type=['mp3', 'wav'])

if uploaded_file is not None:
    st.audio(uploaded_file)
    
    detected_language = "en"
    country_name = "International"
    
    if lyrics_input and len(lyrics_input) > 20 and LANGDETECT_AVAILABLE:
        try:
            detected_language = langdetect.detect(lyrics_input)
            language_names = {
                "sl": "🇸🇮 Slovenščina",
                "hr": "🇭🇷 Hrvaščina",
                "de": "🇩🇪 Nemščina",
                "it": "🇮🇹 Italijanščina",
                "fr": "🇫🇷 Français",
                "es": "🇪🇸 Español",
                "pt": "🇧🇷 Português",
                "en": "🇬🇧 English",
                "zh-cn": "🇨🇳 中文",
                "zh-tw": "🇨🇳 中文"
            }
            country_name = language_names.get(detected_language, "🌍 International")
            st.success(f"{t['lang_detected']}: {country_name}")
        except:
            detected_language = "en"
            st.info(t["lang_not_detected"])
    else:
        st.info(t["enter_lyrics_tip"])
    
    with st.spinner(t["analyzing"]):
        with open("temp_audio.wav", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        y, sr = librosa.load("temp_audio.wav", duration=None)
        
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo_result = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        tempo = float(np.atleast_1d(tempo_result[0])[0])
        if tempo > 200:
            tempo = tempo / 2
        elif tempo > 120:
            tempo = tempo / 2
        elif tempo < 60:
            tempo = tempo * 2
        
        energy = np.array([np.sum(np.abs(y[i:i+sr])) for i in range(0, len(y), sr)])
        avg_energy = float(np.mean(energy))
        max_energy_val = float(np.max(energy))
        energy_percent = int((avg_energy / max_energy_val) * 100)
        
        duration = librosa.get_duration(y=y, sr=sr)
        minutes = int(duration // 60)
        seconds_dur = int(duration % 60)
        
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key_index = int(np.argmax(chroma_mean))
        detected_key = note_names[key_index]
        
        spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(y=y)))
        spectral_rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))
        
        if tempo > 120 and energy_percent > 60:
            mood, mood_desc = t["moods"]["energetic"]
        elif tempo < 80 and energy_percent < 50:
            mood, mood_desc = t["moods"]["melancholic"]
        elif tempo > 100 and energy_percent < 50:
            mood, mood_desc = t["moods"]["relaxed"]
        elif tempo < 80 and energy_percent > 50:
            mood, mood_desc = t["moods"]["dramatic"]
        else:
            mood, mood_desc = t["moods"]["balanced"]
        
        instruments = []
        if spectral_rolloff > 3000:
            instruments.append(t["instruments"]["electric_guitar"])
        if spectral_centroid < 2000:
            instruments.append(t["instruments"]["piano"])
        if zcr > 0.1:
            instruments.append(t["instruments"]["drums"])
        if spectral_centroid > 2000 and spectral_centroid < 4000:
            instruments.append(t["instruments"]["strings"])
        instruments.append(t["instruments"]["vocals"])
        if len(instruments) == 1:
            instruments.append(t["instruments"]["acoustic"])
        
        max_energy_time = int(np.argmax(energy))
        if max_energy_time > duration * 0.7:
            vrhunec_msg = t["chorus_late"]
            vrhunec_ok = False
        elif max_energy_time < duration * 0.2:
            vrhunec_msg = t["chorus_early"]
            vrhunec_ok = False
        else:
            vrhunec_msg = t["chorus_ok"]
            vrhunec_ok = True
        
        radio_data = get_radio_stations(detected_language, tempo, energy_percent)
        
        st.success(t["analysis_done"])
        st.markdown("---")
        
        st.markdown(f"## {t['results']}")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(t["tempo"], f"{tempo:.0f} BPM")
            if tempo < 76:
                st.info(t["slow_ballad"])
            elif tempo < 110:
                st.info(t["mid_tempo"])
            elif tempo < 140:
                st.info(t["fast_song"])
            else:
                st.info(t["very_fast"])
        
        with col2:
            st.metric(t["energy"], f"{energy_percent}%")
            if energy_percent > 70:
                st.info(t["high_energy"])
            elif energy_percent > 40:
                st.info(t["mid_energy"])
            else:
                st.info(t["low_energy"])
        
        with col3:
            st.metric(t["duration"], f"{minutes}:{seconds_dur:02d}")
            if duration < 180:
                st.info(t["good_radio"])
            elif duration < 240:
                st.success(t["ideal_length"])
            else:
                st.warning(t["too_long"])
        
        with col4:
            st.metric(t["key"], detected_key)
            st.info(f"🎵 {detected_key}")
        
        st.markdown("---")
        
        st.markdown(f"## {t['mood_title']}")
        st.markdown(f"""
        <div class="result-box">
            <h2>{mood}</h2>
            <p>{mood_desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"## {t['instruments_title']}")
        cols = st.columns(len(instruments))
        for i, instrument in enumerate(instruments):
            with cols[i]:
                st.markdown(f'<div class="instrument-box">{instrument}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"## {t['visual_title']}")
        fig = plt.figure(figsize=(14, 8))
        fig.patch.set_facecolor('#1a0033')
        gs = gridspec.GridSpec(2, 2, figure=fig)
        
        ax1 = fig.add_subplot(gs[0, :])
        ax1.set_facecolor('#2d0057')
        ax1.plot(energy, color='#ff69b4', linewidth=2.5)
        ax1.fill_between(range(len(energy)), energy, alpha=0.4, color='#da70d6')
        ax1.set_title('Energy over time', color='#ff69b4', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Time (seconds)', color='#e0b0ff')
        ax1.set_ylabel('Energy', color='#e0b0ff')
        ax1.tick_params(colors='#e0b0ff')
        ax1.grid(True, alpha=0.2, color='#da70d6')
        ax1.spines['bottom'].set_color('#ff69b4')
        ax1.spines['left'].set_color('#ff69b4')
        ax1.spines['top'].set_color('#2d0057')
        ax1.spines['right'].set_color('#2d0057')
        
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.set_facecolor('#2d0057')
        bar_colors = ['#da70d6'] * 12
        bar_colors[key_index] = '#ff1493'
        ax2.bar(note_names, chroma_mean, color=bar_colors, alpha=0.9)
        ax2.set_title('Key / Tonality', color='#ff69b4', fontsize=14, fontweight='bold')
        ax2.tick_params(colors='#e0b0ff')
        ax2.grid(True, alpha=0.2, color='#da70d6')
        ax2.spines['bottom'].set_color('#ff69b4')
        ax2.spines['left'].set_color('#ff69b4')
        ax2.spines['top'].set_color('#2d0057')
        ax2.spines['right'].set_color('#2d0057')
        
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.set_facecolor('#2d0057')
        librosa.display.waveshow(y, sr=sr, ax=ax3, color='#ff69b4', alpha=0.8)
        ax3.set_title('Waveform', color='#ff69b4', fontsize=14, fontweight='bold')
        ax3.tick_params(colors='#e0b0ff')
        ax3.spines['bottom'].set_color('#ff69b4')
        ax3.spines['left'].set_color('#ff69b4')
        ax3.spines['top'].set_color('#2d0057')
        ax3.spines['right'].set_color('#2d0057')
        
        plt.tight_layout(pad=3.0)
        st.pyplot(fig)
        
        st.markdown("---")
        
        st.markdown(f"## {t['tips_title']}")
        st.markdown(f"""
        <div class="result-box">
            <p>{t['strongest_part']} <strong>{max_energy_time}. {t['second']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        if vrhunec_ok:
            st.success(vrhunec_msg)
        else:
            st.warning(vrhunec_msg)
        
        st.markdown("---")
        
        st.markdown(f"## {t['radio_title']} - {radio_data['ime']}")
        for postaja in radio_data['postaje']:
            st.markdown(f"""
            <div class="radio-box">
                <h4>📻 {postaja['postaja']}</h4>
                <p>⏰ <strong>{t['best_time']}:</strong> {postaja['cas']}<br>
                ℹ️ {postaja['opis']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="result-box">
            <p>💡 <strong>{t['advice']}:</strong> {radio_data['nasvet']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"## {t['markets_title']}")
        col1, col2 = st.columns(2)
        with col1:
            if tempo > 120:
                st.markdown('<div class="result-box"><p>🇧🇷 <strong>Latin America</strong><br>Loves fast and energetic rhythms</p></div>', unsafe_allow_html=True)
                st.markdown('<div class="result-box"><p>🇺🇸 <strong>USA</strong><br>Great for dance/pop market</p></div>', unsafe_allow_html=True)
            elif tempo > 90:
                st.markdown('<div class="result-box"><p>🇪🇺 <strong>Europe</strong><br>Ideal for pop market</p></div>', unsafe_allow_html=True)
                st.markdown('<div class="result-box"><p>🇬🇧 <strong>UK</strong><br>Mid tempo is very popular</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result-box"><p>🇯🇵 <strong>Japan</strong><br>Appreciates melodic, slow songs</p></div>', unsafe_allow_html=True)
                st.markdown('<div class="result-box"><p>🇸🇪 <strong>Scandinavia</strong><br>Ambient and slow pop is popular</p></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="result-box"><p>{t["promo_tip"]}<br>{t["promo_desc"]}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box"><p>{t["best_post_time"]}<br>{t["best_post_desc"]}</p></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"## {t['pdf_title']}")
        
        def generate_pdf():
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=72)
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle('T', parent=styles['Title'], fontSize=24,
                                        textColor=colors.HexColor('#9b59b6'), spaceAfter=30)
            heading_style = ParagraphStyle('H', parent=styles['Heading1'], fontSize=14,
                                          textColor=colors.HexColor('#9b59b6'), spaceAfter=10, spaceBefore=20)
            normal_style = ParagraphStyle('N', parent=styles['Normal'], fontSize=11,
                                         textColor=colors.black, spaceAfter=8, leading=16)
            
            story = []
            story.append(Paragraph("SoundMind AI - Music Analysis Report", title_style))
            story.append(Paragraph(f"File: {uploaded_file.name}", normal_style))
            story.append(Paragraph(f"Detected language: {country_name}", normal_style))
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("ANALYSIS RESULTS", heading_style))
            data = [
                ['Parameter', 'Value', 'Description'],
                ['Tempo', f'{tempo:.0f} BPM', 'Slow ballad' if tempo < 76 else 'Mid tempo' if tempo < 110 else 'Fast song'],
                ['Energy', f'{energy_percent}%', 'High' if energy_percent > 70 else 'Medium' if energy_percent > 40 else 'Low'],
                ['Duration', f'{minutes}:{seconds_dur:02d}', 'Good for radio' if duration < 180 else 'Ideal length' if duration < 240 else 'A bit long'],
                ['Key', detected_key, 'Main note of the song'],
            ]
            table = Table(data, colWidths=[2*inch, 1.5*inch, 3*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8f0ff'), colors.HexColor('#ffe4f0')]),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#da70d6')),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(table)
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("MOOD", heading_style))
            clean_mood = mood.encode('ascii', 'ignore').decode('ascii')
            clean_mood_desc = mood_desc.encode('ascii', 'ignore').decode('ascii')
            story.append(Paragraph(f"{clean_mood}: {clean_mood_desc}", normal_style))
            story.append(Spacer(1, 10))
            
            story.append(Paragraph("DETECTED INSTRUMENTS", heading_style))
            for instrument in instruments:
                clean_inst = instrument.encode('ascii', 'ignore').decode('ascii')
                story.append(Paragraph(f"- {clean_inst}", normal_style))
            story.append(Spacer(1, 10))
            
            story.append(Paragraph("RECOMMENDATIONS", heading_style))
            story.append(Paragraph(f"Strongest part at: {max_energy_time}. second", normal_style))
            clean_vrhunec = vrhunec_msg.encode('ascii', 'ignore').decode('ascii')
            story.append(Paragraph(clean_vrhunec, normal_style))
            story.append(Spacer(1, 10))
            
            story.append(Paragraph(f"RECOMMENDED RADIO STATIONS - {radio_data['ime']}", heading_style))
            radio_table_data = [['Station', 'Best airtime', 'Description']]
            for postaja in radio_data['postaje']:
                radio_table_data.append([postaja['postaja'], postaja['cas'], postaja['opis']])
            
            radio_table = Table(radio_table_data, colWidths=[1.8*inch, 2*inch, 2.7*inch])
            radio_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff69b4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#fff0f5'), colors.HexColor('#ffe4f0')]),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ff69b4')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(radio_table)
            story.append(Spacer(1, 10))