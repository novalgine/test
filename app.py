
import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import os
import json
from dotenv import load_dotenv

# Import modules
import prompts
import backend as utils
import importlib

# Reload modules for development
importlib.reload(utils)
importlib.reload(prompts)

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Viral Reels Fabrikası",
    page_icon="🎬",
    layout="wide"
)

# --- Custom CSS ---
st.markdown(prompts.CUSTOM_CSS, unsafe_allow_html=True)



# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'full_name' not in st.session_state:
    st.session_state['full_name'] = None
if 'user_mode' not in st.session_state:
    st.session_state['user_mode'] = None

# Active Persona State
if 'active_persona' not in st.session_state:
    st.session_state['active_persona'] = None
if 'unsaved_changes' not in st.session_state:
    st.session_state['unsaved_changes'] = False

# Script Generation State
if 'current_script' not in st.session_state:
    st.session_state['current_script'] = None
if 'script_history_list' not in st.session_state:
    st.session_state['script_history_list'] = []
if 'current_topic' not in st.session_state:
    st.session_state['current_topic'] = ""
if 'current_score' not in st.session_state:
    st.session_state['current_score'] = None
if 'generated_ideas' not in st.session_state:
    st.session_state['generated_ideas'] = []
if 'draft_text' not in st.session_state:
    st.session_state['draft_text'] = ""

import time

# ... (rest of imports)

# API Key Handling
# API Key Handling
api_key = utils.api_key
if not api_key:
    st.error("API Key Eksik!")
    st.stop()

# Initialize DB
utils.init_db()

# --- Helper Functions ---

def mark_unsaved():
    st.session_state['unsaved_changes'] = True

def switch_persona(persona_id):
    st.session_state['active_persona'] = persona_id
    st.session_state['unsaved_changes'] = False
    # Clear script state when switching
    st.session_state['current_script'] = None
    st.session_state['script_history_list'] = []
    st.session_state['generated_ideas'] = []
    st.session_state['draft_text'] = ""
    st.rerun()

def logout():
    # 1. Iterate through all keys in session_state and delete them
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # 2. Force a Rerun immediately to reload the app from scratch
    st.rerun()

def exit_studio():
    st.session_state['active_persona'] = None
    st.session_state['unsaved_changes'] = False
    st.rerun()

def display_script_layout(script_text):
    """Displays the script in a clean, vertical layout."""
    sections = utils.parse_script_sections(script_text)
    
    st.markdown("### 🎣 Kanca")
    st.markdown(sections['hook'])
    if sections['hook_notes']:
        st.markdown(f"<div style='background-color: rgba(255,255,255,0.05); padding: 10px; border-radius: 5px; font-size: 0.9em; color: #aaa;'>🎥 <em>{sections['hook_notes']}</em></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🌉 Gelişme")
    st.markdown(sections['buildup'])
    if sections['buildup_notes']:
        st.markdown(f"<div style='background-color: rgba(255,255,255,0.05); padding: 10px; border-radius: 5px; font-size: 0.9em; color: #aaa;'>🎥 <em>{sections['buildup_notes']}</em></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("### 💎 Değer (Core)")
    st.markdown(sections['core'])
    if sections['core_notes']:
        st.markdown(f"<div style='background-color: rgba(255,255,255,0.05); padding: 10px; border-radius: 5px; font-size: 0.9em; color: #aaa;'>🎥 <em>{sections['core_notes']}</em></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("### 📣 Çağrı (CTA)")
    st.markdown(sections['cta'])
    if sections['cta_notes']:
        st.markdown(f"<div style='background-color: rgba(255,255,255,0.05); padding: 10px; border-radius: 5px; font-size: 0.9em; color: #aaa;'>🎥 <em>{sections['cta_notes']}</em></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    with st.expander("📝 Instagram Açıklaması (Caption)"):
        st.code(sections['caption'], language="text")

# --- Views ---

def show_onboarding():
    st.markdown("""
    <div class="onboarding-card">
        <h1>🎉 Hoş Geldin!</h1>
        <p style="color: #94a3b8; font-size: 1.1em;">Seni daha iyi tanımak ve deneyimini kişiselleştirmek istiyoruz.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mode Selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="mode-card">
            <span class="mode-icon">👤</span>
            <span class="mode-title">Solo Creator</span>
            <span class="mode-desc">Sadece kendim/markam için içerik üretiyorum.</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Seç: Solo Creator", use_container_width=True):
            utils.set_user_mode(st.session_state['user_id'], 'solo')
            # Auto-create default persona
            utils.create_persona(st.session_state['user_id'], "Kişisel Markam", "Varsayılan kişisel marka")
            st.rerun()

    with col2:
        st.markdown("""
        <div class="mode-card">
            <span class="mode-icon">🎭</span>
            <span class="mode-title">Multi-Brand</span>
            <span class="mode-desc">Birden fazla projem veya markam var.</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Seç: Multi-Brand", use_container_width=True):
            utils.set_user_mode(st.session_state['user_id'], 'multi')
            st.rerun()

    with col3:
        st.markdown("""
        <div class="mode-card">
            <span class="mode-icon">🏢</span>
            <span class="mode-title">Ajans / SMM</span>
            <span class="mode-desc">Müşterilerim için profesyonel içerik üretiyorum.</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Seç: Ajans Modu", use_container_width=True):
            utils.set_user_mode(st.session_state['user_id'], 'agency')
            st.rerun()

def show_dashboard(mode='multi'):
    title_map = {
        'multi': "Markalarım",
        'agency': "Müşterilerim"
    }
    btn_map = {
        'multi': "Yeni Marka",
        'agency': "Yeni Müşteri"
    }
    
    page_title = title_map.get(mode, "Markalarım")
    btn_text = btn_map.get(mode, "Yeni Marka")
    
    # --- Global Navbar (Dashboard Version) ---
    with st.container():
        col_logo, col_spacer, col_user = st.columns([1.5, 2, 1.5], vertical_alignment="center")
        with col_logo:
            st.markdown("### 🎬 **Viral Reels Fabrikası**")
        with col_spacer:
            st.write("")
        with col_user:
            c_u_info, c_u_out = st.columns([2, 1])
            with c_u_info:
                st.write(f"👤 {st.session_state['full_name']}")
            with c_u_out:
                if st.button("Çıkış Yap", help="Çıkış", key="dash_logout"):
                    logout()

    # --- Dashboard Content ---
    st.markdown(f"# 🏠 {page_title}")
    
    personas = utils.get_user_personas(st.session_state['user_id'])
    
    # Action Bar
    col_info, col_add = st.columns([3, 1])
    with col_info:
        st.info(f"Toplam {len(personas)} {page_title.lower()[:-1]} yönetiyorsunuz.")
        
    with col_add:
        if len(personas) < 5:
            with st.popover(f"➕ {btn_text}", use_container_width=True):
                with st.form("new_persona_form"):
                    new_p_name = st.text_input("İsim")
                    new_p_desc = st.text_area("Kısa Açıklama")
                    if st.form_submit_button("Oluştur"):
                        if new_p_name:
                            try:
                                utils.create_persona(st.session_state['user_id'], new_p_name, new_p_desc)
                                st.success("Oluşturuldu!")
                                st.rerun()
                            except Exception as e:
                                st.error(str(e))
                        else:
                            st.warning("İsim gerekli.")
        else:
            st.button("➕ Limit Doldu", disabled=True, use_container_width=True)

    st.markdown("---")
    
    if not personas:
        st.info(f"Henüz hiç {page_title.lower()[:-1]} oluşturmadınız. Sağ üstten ekleyerek başlayın.")
    else:
        # Grid Layout
        cols = st.columns(3)
        for i, p in enumerate(personas):
            with cols[i % 3]:
                stats = utils.get_persona_stats(p['id'])
                completion = stats['dna_completion']
                
                # Determine progress color class
                prog_class = "progress-low"
                if completion > 30: prog_class = "progress-mid"
                if completion > 70: prog_class = "progress-high"
                
                # Card HTML
                st.markdown(f"""
                <div class="persona-card">
                    <h3 style="margin-top:0; color:white;">{p['name']}</h3>
                    <p style="color: #94a3b8; font-size: 0.9em; height: 40px; overflow: hidden; margin-bottom: 10px;">{p['description'] or 'Açıklama yok'}</p>
                    <div class="dna-progress">
                        <div class="dna-progress-fill {prog_class}" style="width: {completion}%;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8em; color: #cbd5e1; margin-bottom: 15px;">
                        <span>DNA: %{completion}</span>
                        <span>📝 {stats['script_count']} İçerik</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c_manage, c_del = st.columns([3, 1])
                with c_manage:
                    if st.button(f"YÖNET", key=f"manage_{p['id']}", use_container_width=True):
                        switch_persona(p['id'])
                with c_del:
                    if st.button("🗑️", key=f"del_btn_{p['id']}", use_container_width=True):
                        st.session_state[f"confirm_delete_{p['id']}"] = True
                
                # Delete Confirmation
                if st.session_state.get(f"confirm_delete_{p['id']}", False):
                    st.warning("Emin misiniz?")
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("Evet", key=f"yes_{p['id']}"):
                            utils.delete_persona(p['id'])
                            st.rerun()
                    with col_no:
                        if st.button("Hayır", key=f"no_{p['id']}"):
                            st.session_state[f"confirm_delete_{p['id']}"] = False
                            st.rerun()

def show_studio(is_solo=False):
    # Get current persona data
    personas = utils.get_user_personas(st.session_state['user_id'])
    current_p = next((p for p in personas if p['id'] == st.session_state['active_persona']), None)
    
    if not current_p:
        # Fallback if persona deleted or missing
        if is_solo:
             # Re-create default if missing for solo
             utils.create_persona(st.session_state['user_id'], "Kişisel Markam", "Varsayılan kişisel marka")
             st.rerun()
        else:
            st.error("Persona bulunamadı.")
            if st.button("Dashboard'a Dön"):
                exit_studio()
            return

    # Parse DNA JSON
    dna_data = json.loads(current_p['dna_json']) if current_p['dna_json'] else {}

    # --- Navbar ---
    st.markdown("""
    <style>
        [data-testid="stHeader"] {display: none;}
    </style>
    """, unsafe_allow_html=True)
    
    # --- Unified Global Navbar ---
    with st.container():
        # Use columns with vertical alignment if supported, otherwise just columns
        # Trying to simulate a clean navbar row
        col_logo, col_center, col_right = st.columns([1.5, 2, 1.5], vertical_alignment="center")
        
        with col_logo:
            st.markdown(f"### 🎬 **Viral Reels Fabrikası** <span style='font-size:0.6em; background:#333; padding:2px 6px; border-radius:4px; vertical-align: middle;'>{(st.session_state.get('user_mode') or 'MOD YOK').upper()}</span>", unsafe_allow_html=True)
            
        with col_center:
            if not is_solo:
                # Persona Switcher
                persona_options = {p['id']: p['name'] for p in personas}
                selected_id = st.selectbox(
                    "📂 Aktif Müşteri", 
                    options=list(persona_options.keys()), 
                    format_func=lambda x: persona_options[x],
                    index=list(persona_options.keys()).index(current_p['id']),
                    key="persona_switch",
                    label_visibility="collapsed",
                    placeholder="Müşteri Seçin..."
                )
                
                if selected_id != current_p['id']:
                    if st.session_state.get('unsaved_changes', False):
                        st.warning("⚠️ Kaydedilmemiş değişiklikler!")
                        if st.button("🚫 Kaydetmeden Geç"):
                            switch_persona(selected_id)
                        st.stop()
                    else:
                        switch_persona(selected_id)
            else:
                # For Solo, just show the current persona name cleanly or empty
                st.markdown(f"**👤 {current_p['name']}**")

        with col_right:
            # Action Buttons Row
            c_home, c_set, c_out = st.columns([1, 1, 1])
            
            with c_home:
                if not is_solo:
                    if st.button("Kontrol Paneli", help="Dashboard'a Dön", use_container_width=True):
                        if st.session_state.get('unsaved_changes', False):
                            st.warning("Kaydet!")
                        else:
                            exit_studio()
                else:
                    st.write("") # Spacer

            with c_set:
                if st.button("Ayarlar", help="Ayarlar", key="settings_btn", use_container_width=True):
                    st.session_state['show_settings'] = not st.session_state.get('show_settings', False)

            with c_out:
                if st.button("Çıkış Yap", help="Çıkış Yap", use_container_width=True):
                    logout()
    
    st.markdown("---")

    # --- Settings Dialog ---
    if st.session_state.get('show_settings', False):
        with st.container(border=True):
            st.markdown("### ⚙️ Hesap Ayarları")
            
            st.markdown("#### 👤 Kullanıcı Modu Ayarları")
            
            new_mode_selection = st.radio(
                "Çalışma Modunuzu Seçin:", 
                ["Solo Creator (Tek Marka)", "Multi-Brand (Çoklu Marka)", "Ajans / SMM (Müşteri Yönetimi)"],
                index=["solo", "multi", "agency"].index(st.session_state['user_mode']) if st.session_state['user_mode'] in ["solo", "multi", "agency"] else 0
            )
            
            mode_map = {
                "Solo Creator (Tek Marka)": "solo", 
                "Multi-Brand (Çoklu Marka)": "multi", 
                "Ajans / SMM (Müşteri Yönetimi)": "agency"
            }
            selected_mode_code = mode_map[new_mode_selection]
            
            if selected_mode_code == 'solo' and st.session_state['user_mode'] != 'solo':
                st.warning("⚠️ Solo moda geçtiğinizde diğer personalarınız gizlenir.")
            
            col_s_save, col_s_close = st.columns([1, 1])
            with col_s_save:
                if st.button("💾 Kaydet ve Uygula", type="primary", use_container_width=True):
                    if selected_mode_code != st.session_state['user_mode']:
                        utils.update_user_mode(st.session_state['user_id'], selected_mode_code)
                        st.session_state['user_mode'] = selected_mode_code
                        st.success("Mod güncellendi!")
                        st.session_state['show_settings'] = False
                        st.rerun()
                    else:
                        st.info("Değişiklik yok.")
            with col_s_close:
                if st.button("Kapat", use_container_width=True):
                    st.session_state['show_settings'] = False
                    st.rerun()
        st.markdown("---")

    st.markdown("---")

    # --- Main Studio Tabs ---
    tab_dna, tab_create, tab_history = st.tabs(["🧬 Kimlik & DNA", "🎬 Üretim Stüdyosu", "💾 Geçmiş"])

    # TAB 1: DNA
    # TAB 1: DNA
    with tab_dna:
        st.info("💡 Değişiklik yaptığınızda en alttaki 'Kaydet' butonuna basmayı unutmayın.")
        
        with st.form("dna_form"):
            # SECTION A: HIZLI BAŞLANGIÇ
            with st.container():
                st.markdown("### 🚀 Hızlı Başlangıç (Zorunlu)")
                c1, c2 = st.columns(2)
                with c1:
                    expertise = st.text_input("Uzmanlık / Unvan", value=dna_data.get('expertise', ''), key="dna_expertise", placeholder="Örn: Diyetisyen, Emlak Danışmanı")
                    audience = st.text_input("Hedef Kitle", value=dna_data.get('target_audience', ''), key="dna_audience", placeholder="Örn: Yeni anneler, Yatırımcılar")
                    main_offer = st.text_input("Ana Ürün / Teklif", value=current_p.get('main_offer') or '', key="dna_offer", placeholder="Örn: 30 Günlük Diyet Programı, Lüks Konut Satışı")
                with c2:
                    pain = st.text_area("En Büyük Acı Noktası", value=dna_data.get('pain_points', ''), key="dna_pain", placeholder="Örn: Kilo verememek, Güvenilir kiracı bulamamak")
                    tone = st.selectbox("Ses Tonu", ["Bilge & Otoriter", "Enerjik & Motive Edici", "Mizahi & Eğlenceli", "Sakin & Empatik", "Sert & Gerçekçi"], index=0 if not dna_data.get('voice_tone') else ["Bilge & Otoriter", "Enerjik & Motive Edici", "Mizahi & Eğlenceli", "Sakin & Empatik", "Sert & Gerçekçi"].index(dna_data.get('voice_tone')), key="dna_tone")
                    forbidden_words = st.text_input("Asla Kullanma (Yasaklı Kelimeler)", value=dna_data.get('forbidden_words', ''), key="dna_forbidden", placeholder="Örn: 'Ucuz', 'Garanti', 'Acele et'")

            st.markdown("---")

            # SECTION B: SİHİRLİ DETAYLAR
            with st.expander("✨ Yapay Zekayı %100 Kendine Benzet (Gelişmiş Ayarlar)", expanded=True):
                c3, c4 = st.columns(2)
                with c3:
                    philosophy = st.text_input("Marka Felsefesi", value=dna_data.get('philosophy', ''), key="dna_philosophy", placeholder="Örn: Sürdürülebilir yaşam herkesin hakkı")
                    anti_villain = st.text_input("Ortak Düşman", value=dna_data.get('anti_villain', ''), key="dna_villain", placeholder="Örn: Şok diyetler, Dolandırıcı emlakçılar")
                    knowledge_level = st.select_slider("Kitle Bilgi Seviyesi", options=["Başlangıç", "Orta", "İleri"], value=dna_data.get('knowledge_level', 'Başlangıç'), key="dna_knowledge")
                with c4:
                    sample = st.text_area("Örnek İçerik (Stil Analizi İçin)", value=dna_data.get('sample_content', ''), key="dna_sample", placeholder="Daha önce yazdığınız bir yazıdan örnek yapıştırın.")
                    redlines = st.text_input("Hassas Konular (Red Lines)", value=dna_data.get('red_lines', ''), key="dna_redlines", placeholder="Örn: Siyaset, Din, Futbol")

            # PROGRESS BAR & SAVE
            st.markdown("---")
            
            # Calculate Progress
            mandatory_fields = [expertise, audience, main_offer, pain, tone]
            optional_fields = [philosophy, anti_villain, sample, redlines, forbidden_words] # knowledge_level has default
            
            filled_mandatory = sum(1 for f in mandatory_fields if f)
            filled_optional = sum(1 for f in optional_fields if f)
            
            # 5 Mandatory = 50%, 5 Optional = 50% (approx 10% each)
            progress = int((filled_mandatory / 5) * 50) + int((filled_optional / 5) * 50)
            progress = min(100, progress)
            
            st.markdown(f"**Kimlik Doluluk Oranı: %{progress}**")
            st.progress(progress)

            if st.form_submit_button("💾 Kimliği Kaydet ve Devam Et", use_container_width=True, type="primary"):
                if not all(mandatory_fields):
                    st.error("Lütfen 'Hızlı Başlangıç' bölümündeki tüm alanları doldurun.")
                else:
                    new_dna = {
                        'expertise': expertise,
                        'target_audience': audience,
                        'pain_points': pain,
                        'voice_tone': tone,
                        'philosophy': philosophy,
                        'anti_villain': anti_villain,
                        'knowledge_level': knowledge_level,
                        'sample_content': sample,
                        'red_lines': redlines,
                        'forbidden_words': forbidden_words
                    }
                    utils.update_persona_dna(current_p['id'], new_dna, main_offer=main_offer)
                    st.session_state['unsaved_changes'] = False
                    st.success("DNA Başarıyla Güncellendi!")
                    st.rerun()

    # TAB 2: CREATE
    with tab_create:
        # Check if DNA is ready enough
        if not (dna_data.get('expertise') and dna_data.get('target_audience')):
            st.warning("⚠️ Lütfen önce 'Kimlik & DNA' sekmesinden temel bilgileri doldurun.")
        else:
            col_left, col_right = st.columns([1, 2])
            
            with col_left:
                st.markdown("### ⚙️ Ayarlar")
                model_name = st.selectbox("Model", ["gemini-2.5-flash", "gemini-1.5-flash-8b", "gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash"], key="model_select")
                script_type = st.selectbox("Tür", ["Eğitici", "Hikaye", "Aykırı Fikir", "Satış", "Skeç / Diyalog"], key="type_select")
                
                st.markdown("---")
                st.markdown("### 💡 Fikirmatik")
                if st.button("🧠 5 Fikir Bul"):
                    with st.spinner("Düşünülüyor..."):
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel(model_name)
                        ideas = utils.generate_ideas(model, dna_data.get('expertise'))
                        st.session_state['generated_ideas'] = ideas
                
                if st.session_state['generated_ideas']:
                    for i, idea in enumerate(st.session_state['generated_ideas']):
                        with st.expander(f"{idea['type']}"):
                            st.write(idea['content'])
                            def set_draft(text):
                                st.session_state['draft_text'] = text
                                st.session_state['draft_text_input'] = text # Update the widget key directly
                            
                            st.button("Seç", key=f"sel_{i}_{idea['content'][:10]}", on_click=set_draft, args=(idea['content'],))

            with col_right:
                st.markdown("### ✍️ Üretim Alanı")
                # Initialize key if not present
                if "draft_text_input" not in st.session_state:
                    st.session_state["draft_text_input"] = st.session_state.get("draft_text", "")

                # Use key only, remove value to avoid conflict
                draft_text = st.text_area("Konu / Taslak", height=150, key="draft_text_input")
                
                # Sync back to main state variable
                st.session_state['draft_text'] = draft_text

                if st.button("🚀 Reels Metinini Al", type="primary", use_container_width=True):
                    # Rate Limiting Check
                    if time.time() - st.session_state.get('last_req_time', 0) < 10:
                        st.warning("⏳ Lütfen 10 saniye bekleyin.")
                    elif not st.session_state.get('draft_text'):
                        st.warning("Konu girin.")
                    else:
                        st.session_state['last_req_time'] = time.time()
                        try:
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel(model_name)
                            
                            with st.status("Başlatılıyor...", expanded=True) as status:
                                # 1. Marka DNA'sı Analizi
                                status.update(label="🧬 Marka DNA'sı analiz ediliyor...", state="running")
                                time.sleep(0.8)
                                
                                # Prepare Persona Data String (Real work)
                                persona_str = f"""
                                Role: {dna_data.get('expertise')}
                                Audience: {dna_data.get('target_audience')}
                                Main Offer: {current_p.get('main_offer')}
                                Pain Points: {dna_data.get('pain_points')}
                                Tone: {dna_data.get('voice_tone')}
                                Philosophy: {dna_data.get('philosophy')}
                                Anti-Villain: {dna_data.get('anti_villain')}
                                Knowledge Level: {dna_data.get('knowledge_level')}
                                Sample: {dna_data.get('sample_content')}
                                Red Lines: {dna_data.get('red_lines')}
                                Forbidden Words: {dna_data.get('forbidden_words')}
                                Script Type: {script_type}
                                
                                OFFER CONTEXT: The user sells '{current_p.get('main_offer')}'. Do NOT be overly salesy. Subtly position this offer as the natural solution ONLY in the CTA section or where strictly relevant.
                                """
                                
                                # 2. Kanca Arama
                                status.update(label="🪝 En uygun kanca aranıyor...", state="running")
                                time.sleep(1.0)
                                
                                # 3. Kanca Bulundu
                                status.update(label="✅ Kanca bulundu!", state="running")
                                time.sleep(0.5)
                                
                                # 4. Köprü İhtiyacı
                                status.update(label="🌉 Ana fikir için bir köprüye ihtiyacım var...", state="running")
                                time.sleep(0.8)
                                
                                # 5. Köprü Kuruldu
                                status.update(label="🔗 Köprü kuruldu.", state="running")
                                time.sleep(0.5)
                                
                                # 6. Core Hazırlığı
                                status.update(label="💎 Ana fikiri (core) hazırlıyorum...", state="running")
                                time.sleep(1.2)
                                
                                # 7. CTA Arama
                                status.update(label="📣 Konuya uygun CTA arıyorum...", state="running")
                                time.sleep(0.8)
                                
                                # 8. Hazır mısın?
                                status.update(label="🚀 Hazır mısın?", state="running")
                                time.sleep(0.5)
                                
                                # Generate (Real work)
                                prompt = prompts.SYSTEM_PROMPT.replace("{{ $json.client_persona_data }}", persona_str) + f"\n\nDraft: {st.session_state['draft_text']}"
                                generation_config = genai.types.GenerationConfig(temperature=0.85, top_p=0.9)
                                response = model.generate_content(prompt, generation_config=generation_config)
                                script = response.text
                                
                                st.session_state['current_script'] = script
                                
                                # Analyze
                                score = utils.analyze_viral_score(model, script, persona_str)
                                st.session_state['current_score'] = score
                                
                                # Save
                                utils.save_script_to_db(st.session_state['user_id'], current_p['id'], st.session_state['draft_text'][:50], current_p['name'], script)
                                
                                status.update(label="Bitti!", state="complete")
                                st.rerun()
                                
                        except Exception as e:
                            st.error(f"Hata: {e}")

                # Display Result
                if st.session_state['current_script']:
                    st.markdown("---")
                    # Score Dashboard
                    if st.session_state['current_score']:
                        sc = st.session_state['current_score']
                        st.info(f"Viral Puanı: {sc.get('overall_score')}/100 - {sc.get('improvement_tip')}")
                    
                    display_script_layout(st.session_state['current_script'])
                    
                    # --- Revision Tool ---
                    st.markdown("---")
                    st.markdown("### 🛠️ Revizyon Aracı")
                    with st.form("revision_form"):
                        rev_request = st.text_input("Nasıl bir değişiklik istiyorsunuz?", placeholder="Daha kısa olsun, daha komik olsun, CTA değişsin...")
                        if st.form_submit_button("Revize Et", type="primary"):
                            if rev_request:
                                with st.spinner("Revize ediliyor..."):
                                    try:
                                        genai.configure(api_key=api_key)
                                        model = genai.GenerativeModel(model_name)
                                        
                                        rev_prompt = f"""
                                        ACT AS A SCRIPT EDITOR.
                                        ORIGINAL SCRIPT:
                                        {st.session_state['current_script']}
                                        
                                        USER REQUEST:
                                        {rev_request}
                                        
                                        TASK: Rewrite the script to satisfy the request. Keep the format (HOOK, BUILD UP, CORE, CTA, CAPTION).
                                        IMPORTANT: Do NOT use placeholders like [X] or [Y]. Fill them with relevant content based on the context.
                                        """
                                        
                                        response = model.generate_content(rev_prompt)
                                        new_script = response.text
                                        st.session_state['current_script'] = new_script
                                        
                                        # Re-analyze
                                        persona_str = f"Role: {dna_data.get('expertise')}, Audience: {dna_data.get('target_audience')}"
                                        new_score = utils.analyze_viral_score(model, new_script, persona_str)
                                        st.session_state['current_score'] = new_score
                                        
                                        st.success("Revize edildi!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Hata: {e}")

    # TAB 3: HISTORY
    with tab_history:
        history = utils.get_user_history(st.session_state['user_id'], current_p['id'])
        if history.empty:
            st.info("Bu müşteri için henüz içerik yok.")
        else:
            for idx, row in history.iterrows():
                with st.expander(f"{row['created_at']} - {row['topic'][:40]}..."):
                    st.text(row['script'])
                    if st.button("Sil", key=f"del_hist_{row['id']}"):
                        utils.delete_script_db(row['id'])
                        st.rerun()

# --- Main Logic ---

if not st.session_state['logged_in']:
    # Login Screen
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container(border=True):
            st.markdown('<div class="login-header"><h1>🎬 Viral Reels Fabrikası</h1><p style="color:#9CA3AF;">Profesyonel İçerik Üretim Sistemi</p></div>', unsafe_allow_html=True)
            
            t1, t2 = st.tabs(["Giriş", "Kayıt"])
            with t1:
                with st.form("login_form"):
                    u = st.text_input("Kullanıcı Adı", key="login_u")
                    p = st.text_input("Şifre", type="password", key="login_p")
                    
                    if st.form_submit_button("Giriş Yap", use_container_width=True):
                        print(f"Attempting login for user: {u}")
                        user = utils.login_user(u, p)
                        if user:
                            print(f"Login successful: {user}")
                            st.session_state['logged_in'] = True
                            st.session_state['user_id'] = user['id']
                            st.session_state['username'] = user['username']
                            st.session_state['full_name'] = user['full_name']
                            st.session_state['user_mode'] = user.get('user_mode')
                            st.success("Giriş başarılı! Yönlendiriliyorsunuz...")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            print("Login failed")
                            st.error("Hatalı giriş.")
            with t2:
                with st.form("signup"):
                    fn = st.text_input("Ad Soyad")
                    nu = st.text_input("Kullanıcı Adı")
                    np = st.text_input("Şifre", type="password")
                    if st.form_submit_button("Kayıt Ol", use_container_width=True):
                        if utils.create_user(nu, np, fn):
                            st.success("Kayıt başarılı! Giriş yapılıyor...")
                            # Auto-login
                            user = utils.login_user(nu, np)
                            if user:
                                st.session_state['logged_in'] = True
                                st.session_state['user_id'] = user['id']
                                st.session_state['username'] = user['username']
                                st.session_state['full_name'] = user['full_name']
                                st.session_state['user_mode'] = user.get('user_mode')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Bu kullanıcı adı zaten alınmış.")

else:
    # Check Onboarding Status
    user_details = utils.get_user_details(st.session_state['user_id'])
    
    if user_details is None:
        # User ID in session but not in DB (zombie session)
        st.session_state.clear()
        st.rerun()

    # Safely check onboarding status (default to False/0 if None or missing)
    is_onboarded = user_details.get('onboarding_complete', 0)
    
    if not is_onboarded:
        show_onboarding()
    else:
        # Adaptive UI Routing
        mode = user_details.get('user_mode')
        if not mode:
            mode = 'multi' # Fallback for legacy users
        
        if mode == 'solo':
            # SOLO MODE: Bypass Dashboard, Go to Studio with Default Persona
            personas = utils.get_user_personas(st.session_state['user_id'])
            if not personas:
                # Auto-create if missing (failsafe)
                utils.create_persona(st.session_state['user_id'], "Kişisel Markam", "Varsayılan kişisel marka")
                personas = utils.get_user_personas(st.session_state['user_id'])
            
            # Set active persona automatically
            if not st.session_state['active_persona']:
                st.session_state['active_persona'] = personas[0]['id']
            
            show_studio(is_solo=True)
            
        else:
            # MULTI / AGENCY MODE: Show Dashboard
            if st.session_state['active_persona']:
                show_studio(is_solo=False)
            else:
                show_dashboard(mode=mode)
    
    # Logout Logic (Hidden handler)
    if st.query_params.get("logout"):
        st.session_state.clear()
        st.rerun()
