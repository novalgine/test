import sqlite3
import hashlib
import re
import json
import os
import pandas as pd
import google.generativeai as genai
import prompts
import bcrypt
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

DB_NAME = "viral_reels.db"

# --- Database Functions ---

def init_db():
    """Initializes the SQLite database with users, personas, and history tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE NOT NULL, 
                  password_hash TEXT NOT NULL, 
                  full_name TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Migration: Add user_mode and onboarding_complete
    try:
        c.execute("ALTER TABLE users ADD COLUMN user_mode TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        c.execute("ALTER TABLE users ADD COLUMN onboarding_complete BOOLEAN DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    # Personas Table
    c.execute('''CREATE TABLE IF NOT EXISTS personas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER NOT NULL,
                  name TEXT NOT NULL,
                  description TEXT,
                  main_offer TEXT,
                  dna_json TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    # Migration: Add main_offer to personas
    try:
        c.execute("ALTER TABLE personas ADD COLUMN main_offer TEXT")
    except sqlite3.OperationalError:
        pass

    # History Table (Scripts)
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  persona_id INTEGER,
                  topic TEXT, 
                  persona TEXT, 
                  script TEXT, 
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id),
                  FOREIGN KEY(persona_id) REFERENCES personas(id))''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_user(username, password, full_name):
    """Adds a new user to the database with validation."""
    if not re.match("^[a-zA-Z0-9_]+$", username):
        raise ValueError("Kullanıcı adı sadece harf, rakam ve alt çizgi içerebilir.")
    if len(password) < 6:
        raise ValueError("Şifre en az 6 karakter olmalıdır.")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    if c.fetchone():
        conn.close()
        raise ValueError("Bu kullanıcı adı zaten mevcut.")

    try:
        hashed = hash_password(password)
        # Default onboarding_complete to 0 (False)
        c.execute("INSERT INTO users (username, password_hash, full_name, onboarding_complete) VALUES (?, ?, ?, 0)", (username, hashed, full_name))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def login_user(username, password):
    """Checks credentials and returns (id, username, full_name, user_mode, onboarding_complete) if valid."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Fetch user by username only
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user:
        try:
            # Verify password using bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                return dict(user)
        except ValueError:
            # Handle legacy SHA256 hashes gracefully (optional: auto-migrate)
            # For now, just fail login for old users to enforce security as requested
            pass
            
    return None

def set_user_mode(user_id, mode):
    """Updates the user mode and sets onboarding as complete."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET user_mode = ?, onboarding_complete = 1 WHERE id = ?", (mode, user_id))
    conn.commit()
    conn.close()

def update_user_mode(user_id, new_mode):
    """Updates the user mode for an existing user."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET user_mode = ? WHERE id = ?", (new_mode, user_id))
    conn.commit()
    conn.close()

def reset_user_onboarding(user_id):
    """Resets the user's onboarding status and mode."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET user_mode = NULL, onboarding_complete = 0 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_user_details(user_id):
    """Fetches user details including mode and onboarding status."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None

# --- Persona Functions ---

def create_persona(user_id, name, description, main_offer=None):
    """Creates a new persona if limit not reached."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check limit
    c.execute("SELECT COUNT(*) FROM personas WHERE user_id = ?", (user_id,))
    count = c.fetchone()[0]
    
    if count >= 5:
        conn.close()
        raise Exception("Maximum 5 persona limiti!")
    
    # Insert new persona
    empty_dna = json.dumps({})
    c.execute("INSERT INTO personas (user_id, name, description, main_offer, dna_json) VALUES (?, ?, ?, ?, ?)",
              (user_id, name, description, main_offer, empty_dna))
    conn.commit()
    conn.close()

def get_user_personas(user_id):
    """Returns list of all personas for this user."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, name, description, main_offer, dna_json, created_at FROM personas WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_persona_dna(persona_id, dna_dict, main_offer=None):
    """Updates the DNA JSON and main_offer for a persona."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    dna_json = json.dumps(dna_dict)
    if main_offer is not None:
        c.execute("UPDATE personas SET dna_json = ?, main_offer = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (dna_json, main_offer, persona_id))
    else:
        c.execute("UPDATE personas SET dna_json = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (dna_json, persona_id))
    
    conn.commit()
    conn.close()

def get_persona_stats(persona_id):
    """Returns script count and DNA completion percentage."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Script Count
    c.execute("SELECT COUNT(*) FROM history WHERE persona_id = ?", (persona_id,))
    script_count = c.fetchone()[0]
    
    # DNA Completion
    c.execute("SELECT dna_json FROM personas WHERE id = ?", (persona_id,))
    row = c.fetchone()
    conn.close()
    
    completion = 0
    if row and row[0]:
        dna_data = json.loads(row[0])
        required_fields = ['expertise', 'target_audience', 'pain_points', 'voice_tone']
        filled = sum(1 for f in required_fields if dna_data.get(f))
        completion = int((filled / len(required_fields)) * 100)
        
    return {"script_count": script_count, "dna_completion": completion}

def delete_persona(persona_id):
    """Deletes a persona and all associated scripts (Cascade)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Delete scripts first
    c.execute("DELETE FROM history WHERE persona_id = ?", (persona_id,))
    
    # Delete persona
    c.execute("DELETE FROM personas WHERE id = ?", (persona_id,))
    
    conn.commit()
    conn.close()

# --- History & Script Functions ---

def save_script_to_db(user_id, persona_id, topic, persona_name, script):
    """Saves a generated script to the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO history (user_id, persona_id, topic, persona, script) VALUES (?, ?, ?, ?, ?)", 
              (user_id, persona_id, topic, persona_name, script))
    conn.commit()
    conn.close()

def get_user_history(user_id, persona_id=None):
    """Retrieves history for a specific user, optionally filtered by persona."""
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT * FROM history WHERE user_id = ?"
    params = [user_id]
    
    if persona_id:
        query += " AND persona_id = ?"
        params.append(persona_id)
        
    query += " ORDER BY created_at DESC"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def delete_script_db(script_id):
    """Deletes a script from the database by ID."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE id = ?", (script_id,))
    conn.commit()
    conn.close()

def generate_ideas(model, persona):
    """Generates 5 viral content ideas based on the persona."""
    idea_prompt = f"""
    You are an expert Content Strategist.
    Generate 5 VIRAL REELS IDEAS for the following persona:
    
    Persona: {persona}
    
    Create one idea for each of these specific archetypes:
    1. The Mistake (Hata): A common error the target audience makes.
    2. The How-To (Nasıl Yapılır): A quick, actionable tip or fix.
    3. The Contrarian (Aykırı Görüş): A polarizing opinion that challenges industry norms.
    4. The Story (Hikaye): A relatable struggle or "aha!" moment.
    5. The Resource (Araç/Kaynak): A tool, website, or hack that saves time.
    
    Return the result strictly as a JSON list of objects. Each object must have:
    - "type": (string, e.g., "Hata")
    - "content": (string, the idea text in Turkish)
    
    Example format:
    [
        {{"type": "Hata", "content": "..."}},
        {{"type": "Nasıl Yapılır", "content": "..."}}
    ]
    
    Do not include markdown formatting like ```json ... ```. Just the raw JSON string.
    """
    try:
        response = model.generate_content(idea_prompt)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        return []

def parse_script_sections(text):
    """Parses the generated text into script and notes sections."""
    sections = {
        "hook": "", "hook_notes": "",
        "buildup": "", "buildup_notes": "",
        "core": "", "core_notes": "",
        "cta": "", "cta_notes": "",
        "caption": ""
    }
    
    try:
        text = text.replace("\r\n", "\n")
        
        # Define markers
        markers = {
            "hook": "HOOK (KANCA)",
            "buildup": "BUILD UP (GELİŞME)",
            "core": "CORE (ANA GÖVDE)",
            "cta": "CTA (ÇAĞRI)",
            "caption": "CAPTION (AÇIKLAMA)"
        }
        notes_marker = "🎬 ÇEKİM & GÖRSEL NOTLARI:"

        def get_block(start_marker, end_marker=None):
            start_idx = text.find(start_marker)
            if start_idx == -1:
                return ""
            start_idx += len(start_marker)
            
            if end_marker:
                end_idx = text.find(end_marker, start_idx)
                if end_idx == -1:
                    return text[start_idx:].strip()
                return text[start_idx:end_idx].strip()
            else:
                return text[start_idx:].strip()

        # Extract blocks
        hook_block = get_block(markers["hook"], markers["buildup"])
        buildup_block = get_block(markers["buildup"], markers["core"])
        core_block = get_block(markers["core"], markers["cta"])
        cta_block = get_block(markers["cta"], markers["caption"])
        caption_block = get_block(markers["caption"])

        # Parse blocks into content and notes
        def split_notes(block):
            if notes_marker in block:
                parts = block.split(notes_marker)
                return parts[0].strip(), parts[1].strip()
            return block.strip(), ""

        sections["hook"], sections["hook_notes"] = split_notes(hook_block)
        sections["buildup"], sections["buildup_notes"] = split_notes(buildup_block)
        sections["core"], sections["core_notes"] = split_notes(core_block)
        sections["cta"], sections["cta_notes"] = split_notes(cta_block)
        sections["caption"] = caption_block

    except Exception as e:
        print(f"Error parsing script: {e}")
        pass
        
    return sections

def analyze_viral_score(model, script_text, client_persona_data):
    """Analyzes the script for viral potential using Gemini."""
    
    analysis_prompt = prompts.VIRAL_ANALYSIS_PROMPT.format(
        script_text=script_text,
        client_persona_data=client_persona_data
    )

    try:
        response = model.generate_content(analysis_prompt)
        text = response.text.strip()
        
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception as e:
        error_msg = str(e)
        # Try to capture text if it exists in local scope, otherwise generic
        raw_text = locals().get('text', 'No text generated')
        return {
            "overall_score": 0,
            "improvement_tip": f"Hata: {error_msg}",
            "hook": {"score": 0, "reason": f"Raw: {raw_text[:100]}..."},
            "retention": {"score": 0, "reason": "Hata"},
            "conversion": {"score": 0, "reason": "Hata"}
        }
