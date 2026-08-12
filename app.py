import os
import requests
from flask import Flask, jsonify, request, send_file
from bs4 import BeautifulSoup

app = Flask(__name__)

# Verified comprehensive static information for Sri Y N College, Narasapuram
COLLEGE_INFO = {
    "name": "Sri Yerramilli Narayana Murthy College (Sri Y N College, Autonomous)",
    "location": "Narasapuram (Narsapur), West Godavari District, Andhra Pradesh, India - 534275",
    "address": "Sri Y N College, Main Road, Narsapur, West Godavari District, Andhra Pradesh, Pin: 534275",
    "established": "1949",
    "accreditation": "NAAC 'A+' Grade in 4th Cycle; UGC Autonomous status extended from 2024-25 to 2033-34.",
    "website": "https://sriyncollege.org",
    "courses": [
        "B.Sc. (Hons) - Data Science, Computer Science, Artificial Intelligence, Mathematics, Physics, Chemistry, Electronics, Botany, Zoology, Aquaculture, Biotechnology, Microbiology, Geography, Statistics",
        "B.Com. (Hons) - General & Computer Applications",
        "BBA (Hons) - Bachelor of Business Administration",
        "BCA (Hons) - Bachelor of Computer Applications",
        "B.A. (Hons) - Political Science, History, Economics, etc.",
        "B.Voc. - Fashion Technology and Apparel Designing",
        "PG Courses - MBA, MCA, M.Sc., M.A. (via APICET / APPGCET)"
    ],
    "departments": "Computer Science, AI & Electronics, Management Studies (MBA/BBA), Commerce, Aquaculture, Life Sciences, Physical Sciences, Humanities & Social Sciences.",
    "admissions": "Undergraduate admissions follow the Online Admissions Module for Degree Colleges (OAMDC) via APSCHE web counseling. Postgraduate admissions require valid APICET (for MBA/MCA) or APPGCET scores.",
    "facilities": "AI & Quantum Innovation Centre, Central Library & Reading Room, Digital Learning Centre, Boys' and Women's Hostels, NCC & NSS wings, Sports & Games infrastructure, Health Centre, RO Water Plant, Canteen.",
    "contact": {
        "ug_phone": "08814-273246",
        "pg_phone": "08814-274939",
        "ug_email": "principal@sriyncollege.org",
        "pg_email": "sriyncpgcourses.nsp@gmail.com"
    },
    "latest_updates": "UGC extended Autonomous Status for 10 years (2024-2033). Newly launched AI & Quantum Innovation Centre in December 2025."
}

def get_live_updates_from_web():
    """Optional online data fallback fetcher from official website headers."""
    try:
        response = requests.get("https://sriyncollege.org/", timeout=3)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract marquee or latest announcements text if available
            announcements = []
            for item in soup.find_all(class_='latest-news') or soup.find_all('marquee'):
                announcements.append(item.get_text(strip=True))
            if announcements:
                return " | ".join(announcements[:3])
    except Exception:
        pass
    return COLLEGE_INFO["latest_updates"]

@app.route("/")
def home():
    """Serve the single complete frontend file."""
    return send_file("index.html")

@app.route("/api/college", methods=["GET"])
def get_college_info():
    """API Endpoint to retrieve comprehensive college information."""
    dynamic_updates = get_live_updates_from_web()
    info_payload = COLLEGE_INFO.copy()
    info_payload["latest_updates"] = dynamic_updates
    return jsonify({
        "success": True,
        "info": info_payload
    })

@app.route("/api/latest", methods=["GET"])
def get_latest_news():
    """API Endpoint specifically for latest updates."""
    news = get_live_updates_from_web()
    return jsonify({
        "success": True,
        "latest_updates": news
    })

@app.route("/api/chat", methods=["POST"])
def chat_endpoint():
    """Intelligent intent-matching chat API supporting English, Telugu, and mixed queries."""
    data = request.get_json() or {}
    user_message = data.get("message", "").strip().lower()

    if not user_message:
        return jsonify({
            "success": False,
            "answer": "Please ask a question regarding Sri Y N College, Narasapuram."
        })

    # Standard Fallback string required if unverified or out of bounds
    fallback_response = "I couldn't find verified information about that. Please contact Sri Y N College for confirmation."

    # Intent Matching Logic (English, Telugu, and Telugu-English mixed text)
    
    # 1. Location / Address Intents
    if any(k in user_message for k in ["ekkada", "location", "address", "where", "situated", "map", "chotu"]):
        answer = (
            f"📍 **College Location & Address:**\n"
            f"{COLLEGE_INFO['address']}\n\n"
            f"Sri Y N College is prominently situated in Narsapur (Narasapuram), West Godavari district of Andhra Pradesh."
        )

    # 2. Courses / Programs Intents
    elif any(k in user_message for k in ["course", "courses", "em unnayi", "programs", "degrees", "b.sc", "bcom", "bba", "bca", "group"]):
        courses_list = "\n".join([f"• {c}" for c in COLLEGE_INFO['courses']])
        answer = (
            f"🎓 **Available Courses at Sri Y N College (Autonomous):**\n"
            f"The college offers 4-year Under-Graduate (Hons) programmes with Multiple Entry/Exit options under UGC framework:\n\n"
            f"{courses_list}\n\n"
            f"PG programmes (MBA, MCA, M.Sc, M.A) are also offered under Dr. C.S. Rao P.G. Centre."
        )

    # 3. Admissions / Joining / Apply Intents
    elif any(k in user_message for k in ["admission", "admissions", "fees", "fee", "join", "teesukovali", "apply", "eligibility", "entha"]):
        answer = (
            f"📝 **Admissions & Fee Structure Details:**\n\n"
            f"• **UG Admissions:** Conducted online via the OAMDC portal through APSCHE web counseling based on Intermediate marks.\n"
            f"• **PG Admissions:** Requires valid ranks in APICET (for MBA/MCA) or APPGCET (for M.Sc/M.A).\n"
            f"• **Fee Structure:** Varies by course group (aided vs. unaided programmes). For precise fee details or category-wise breakdown, please contact the college office at UG Landline: {COLLEGE_INFO['contact']['ug_phone']}."
        )

    # 4. Departments Intents
    elif any(k in user_message for k in ["department", "departments", "branches", "faculty"]):
        answer = (
            f"🏛️ **Departments:**\n"
            f"Sri Y N College includes major academic departments including: {COLLEGE_INFO['departments']}."
        )

    # 5. Principal / Management / Authority Intents
    elif any(k in user_message for k in ["principal", "evaru", "secretary", "correspondent", "management", "head"]):
        answer = (
            f"👔 **College Administration & Leadership:**\n"
            f"Sri Y N College (Autonomous) is managed under distinguished governing bodies and leadership based in Narsapur. For specific administrative inquiries, you can reach the Principal's office via landline at {COLLEGE_INFO['contact']['ug_phone']} or email at {COLLEGE_INFO['contact']['ug_email']}."
        )

    # 6. Timings / Working Hours Intents
    elif any(k in user_message for k in ["timing", "timings", "time", "working hours", "college open"]):
        answer = (
            f"⏰ **College Timings:**\n"
            f"The regular academic working hours are typically from 9:00 AM to 4:30 PM, Monday through Saturday (excluding second Saturdays and public holidays)."
        )

    # 7. Contact / Phone / Email / Website Intents
    elif any(k in user_message for k in ["contact", "phone", "number", "email", "website", "call", "reach"]):
        contact = COLLEGE_INFO['contact']
        answer = (
            f"📞 **Contact Details - Sri Y N College:**\n\n"
            f"• **UG Office Landline:** {contact['ug_phone']}\n"
            f"• **PG Office Landline:** {contact['pg_phone']}\n"
            f"• **UG Email:** {contact['ug_email']}\n"
            f"• **PG Email:** {contact['pg_email']}\n"
            f"• **Official Website:** {COLLEGE_INFO['website']}"
        )

    # 8. Facilities / Amenities Intents
    elif any(k in user_message for k in ["facility", "facilities", "hostel", "library", "labs", "sports", "amenities"]):
        answer = (
            f"🏢 **Campus Facilities:**\n"
            f"{COLLEGE_INFO['facilities']}\n\n"
            f"The campus features modern laboratories, a newly opened AI & Quantum Innovation Centre, dedicated digital learning resources, and sports grounds."
        )

    # 9. Latest Updates / News Intents
    elif any(k in user_message for k in ["latest", "update", "updates", "news", "notifications", "exam"]):
        live_news = get_live_updates_from_web()
        answer = (
            f"📢 **Latest Updates & Announcements:**\n\n"
            f"• {live_news}\n\n"
            f"Check the official website portal ({COLLEGE_INFO['website']}) for real-time semester examination timetables and circulars."
        )

    # 10. Greetings (English & Telugu)
    elif any(k in user_message for k in ["hi", "hello", "hey", "namaste", "vanakkam", "good morning", "good afternoon", "hlo"]):
        answer = (
            f"Namaste! 🙏 Welcome to Sri Y N College, Narasapuram AI Assistant. "
            f"How can I help you with courses, admissions, fees, or college information today?"
        )

    else:
        # Fallback to web search or default safe unverified response if unknown intent
        answer = fallback_response

    return jsonify({
        "success": True,
        "answer": answer
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
