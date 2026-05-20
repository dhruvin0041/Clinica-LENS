import streamlit as st

def empty_state(icon="📄", title="No Data Available", description="Upload a study or run an analysis to see results here."):
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 64px 24px; text-align: center; border: 1px dashed #E2E8F0; border-radius: 12px; background-color: #FFFFFF; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
            <div style="font-size: 40px; color: #94A3B8; margin-bottom: 16px;">{icon}</div>
            <h3 style="margin: 0 0 8px 0; font-size: 16px; font-weight: 600; color: #0F172A;">{title}</h3>
            <p style="margin: 0; font-size: 14px; color: #64748B;">{description}</p>
        </div>
    """, unsafe_allow_html=True)

def skeleton_loader():
    st.markdown("""
        <style>
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: .5; }
        }
        .skeleton {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            background-color: #E2E8F0;
            border-radius: 8px;
        }
        </style>
        <div style="display: flex; flex-direction: column; gap: 16px; margin-top: 16px; padding: 24px; border: 1px solid #E2E8F0; border-radius: 12px; background-color: #FFFFFF;">
            <div class="skeleton" style="height: 180px; width: 100%;"></div>
            <div class="skeleton" style="height: 24px; width: 40%;"></div>
            <div class="skeleton" style="height: 20px; width: 80%;"></div>
            <div class="skeleton" style="height: 20px; width: 60%;"></div>
        </div>
    """, unsafe_allow_html=True)

def status_badge(status):
    color_map = {
        "Verified": "#10B981", # Emerald
        "Pending": "#F59E0B", # Amber
        "Error": "#EF4444", # Rose
        "Unknown": "#64748B" # Slate
    }
    bg_map = {
        "Verified": "#D1FAE5", 
        "Pending": "#FEF3C7", 
        "Error": "#FEE2E2", 
        "Unknown": "#F1F5F9"
    }
    color = color_map.get(status, color_map["Unknown"])
    bg = bg_map.get(status, bg_map["Unknown"])
    
    st.markdown(f"""
    <span style="background-color: {bg}; color: {color}; padding: 4px 8px; border-radius: 9999px; font-size: 12px; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
        <div style="width: 6px; height: 6px; border-radius: 50%; background-color: {color};"></div>
        {status}
    </span>
    """, unsafe_allow_html=True)
