import streamlit as st
import pandas as pd
import io

reference_file = "All Permits with Details.xlsx"

# -- بيانات المستخدمين مع كلمات السر والصلاحيات --
USERS = {
    "admin": {"password": "NOone@0", "role": "admin"},
    "user1": {"password": "M12345-", "role": "m_sadaa"},
    "user2": {"password": "user234", "role": "user"},  
    
}

# --- دالة تسجيل الدخول ---
def login():
    def check_credentials():
        username = st.session_state.get("username")
        password = st.session_state.get("password")
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = USERS[username]["role"]
            st.success(f"✅ مرحباً، {username}!")
        else:
            st.session_state["logged_in"] = False
            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["role"] = ""

    if not st.session_state["logged_in"]:
        st.title("🔒 تسجيل الدخول")
        st.text_input("اسم المستخدم", key="username")
        st.text_input("كلمة المرور", type="password", key="password")
        st.button("تسجيل الدخول", on_click=check_credentials)
        return False
    else:
        return True

# --- تحميل بيانات قاعدة الترخيص مع كاش لتحسين الأداء ---
@st.cache_data
def load_reference_data():
    cols_to_use = [3, 4, 7, 21]
    col_names = ["LicensedNumber", "LicenseType", "EventName", "City"]
    df = pd.read_excel(reference_file, usecols=cols_to_use)
    df.columns = col_names
    return df

# --- تحميل زيارات اليوم ---
def load_visits():
    try:
        return pd.read_excel("daily visits.xlsx")
    except FileNotFoundError:
        return pd.DataFrame()

# --- بدء التطبيق ---
if login():
    username = st.session_state["username"]
    role = st.session_state["role"]

    st.sidebar.write(f"👤 المستخدم: **{username}**")
    st.sidebar.write(f"🔑 الدور: **{role}**")

    if st.sidebar.button("تسجيل خروج"):
        for key in ["logged_in", "username", "role", "password"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()

    # تحميل بيانات الترخيص
    try:
        db_df = load_reference_data()
    except FileNotFoundError:
        st.warning("⚠️ ملف قاعدة البيانات غير موجود.")
        db_df = pd.DataFrame(columns=["LicensedNumber", "LicenseType", "EventName", "City"])

    st.title("📝 تسجيل زيارة يومية (Daily Visit)")

    licensed_number = st.text_input("رقم الترخيص")

    if licensed_number:
        clean_licensed_number = licensed_number.strip()
        if clean_licensed_number.isdigit():
            match_row = db_df[db_df["LicensedNumber"].astype(str) == clean_licensed_number]
            if not match_row.empty:
                event_name = match_row.iloc[0]["EventName"]
                license_type = match_row.iloc[0]["LicenseType"]
                city = match_row.iloc[0]["City"]
                st.success(f"✅ تم العثور على البيانات:\n- اسم الفعالية: {event_name}\n- نوع الترخيص: {license_type}\n- المدينة: {city}")
            else:
                event_name = ""
                license_type = ""
                city = ""
                st.warning("⚠️ لم يتم العثور على هذا الرقم في قاعدة البيانات.")
        else:
            st.error("⚠️ الرجاء إدخال رقم ترخيص صحيح (أرقام فقط).")
            event_name = ""
            license_type = ""
            city = ""
    else:
        event_name = ""
        license_type = ""
        city = ""

    supervisor_name = st.selectbox("🧑‍💼 اسم المشرف", ["FaisalAl Anzi", "Mousa Al Khalifa", "Saud Al Khrisi", "Reham Al Otaibi"])

    employee_names = [
        "Abdulaziz Al Qahtani", "Abdulaziz Al Dosari", "Abdulelah Al Daraan",
        "Abdulaziz Al Otaibi", "Abdulelah Al Dosari", "Abdulaziz Al Mohamady",
        "Abdulrahman Muhyiddin", "Aisha Al Refai", "Badr Al Dini", "Fahad Manwer",
        "Faisal Al Jadaan", "Faisal Bintasha", "Faleh Mohammed", "Hala Al Kathiri",
        "Hatem Al Harbi", "Khalid Al Hassan", "Mansour Al Marwani", "Mohammed Al Ahmadi",
        "Mohammed Al Subaie", "Mosleh Al Malki", "Nawaf Al Daraan", "Owadhah Al Mansour",
        "Raed Al Anazi", "Rakan Al Otaibi", "Saeed Al Zhrani", "Shahad Al Huwaidi",
        "Taghreed Al Amoudi", "Talal Al Granes", "Turki Al Ruwaili", "Wael Al Anazi",
        "Zayer Al Otaibi", "Nouf Al Khateb", "Majed Al Shammari"
    ]

    employee_name = st.selectbox("Employee Name (EN)", options=employee_names)
    visit_date = st.date_input("Visit Date (اختر تاريخ الزيارة)")
    visit_status = st.selectbox("Visit Status", options=["لم تتم الزيارة", "تمت الزيارة"])
    visit_purpose = st.selectbox("Visit Purpose", options=["جمع بيانات", "تركيب جهاز HoN", "استلام جهاز HoN"])
    visit_notes_options = [
        "النشاط مغلق / غير نشط",
        "لا يوجد مشاكل",
        "لا يوجد زوار / قلة عدد الزوار",
        "النشاط لا يطابق معايير القياس لمحطات رحلة الزائر",
        "دعوات خاصة",
        "موقع النشاط غير دقيق",
        "ضعف شبكة الاتصال داخل النشاط",
        "مخصص للنساء",
        "سوء الأحوال الجوية",
        "عدم تعاون الجهة",
        "النشاط ملغي",
        "الموظف في إجازة"
    ]
    visit_notes = st.selectbox("Visit Notes", options=visit_notes_options)
    general_notes = st.text_area("General Notes")

    if st.button("💾 حفظ في ملف Daily Visits"):
        new_record = {
            "LicensedNumber": clean_licensed_number,
            "EventName": event_name,
            "LicenseType": license_type,
            "City": city,
            "EmployeeName": employee_name,
            "VisitDate": visit_date,
            "VisitStatus": visit_status,
            "VisitPurpose": visit_purpose,
            "VisitNotes": visit_notes,
            "GeneralNotes": general_notes
        }

        try:
            visits_df = pd.read_excel("daily visits.xlsx")
        except FileNotFoundError:
            visits_df = pd.DataFrame(columns=new_record.keys())

        visits_df = pd.concat([visits_df, pd.DataFrame([new_record])], ignore_index=True)
        visits_df.to_excel("daily visits.xlsx", index=False)
        st.success("✅ تم حفظ بيانات الزيارة في ملف daily visits.xlsx")

    # صلاحيات العرض والتنزيل فقط للمدير
    if role == "admin":
        if st.checkbox("📂 عرض زيارات اليوم"):
            visits_df = load_visits()
            if visits_df.empty:
                st.info("لا يوجد ملف daily visits.xlsx بعد. ابدأ بإضافة زيارات.")
            else:
                st.dataframe(visits_df)

        try:
            visits_df = load_visits()
            if not visits_df.empty:
                buffer = io.BytesIO()
                visits_df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                st.download_button(
                    label="⬇️ تحميل ملف Daily Visits",
                    data=buffer,
                    file_name="daily visits.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except FileNotFoundError:
            pass
    else:
        st.info("🔒 لا تملك صلاحية عرض أو تحميل زيارات اليوم.")
