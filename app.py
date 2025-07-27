import streamlit as st
import pandas as pd
import io

reference_file = "All Permits with Details.xlsx"

USERS = {
    "admin": {"password": "NOone@0", "role": "admin"},
    "user1": {"password": "M12345-", "role": "m_sadaa"},
    "user2": {"password": "user234", "role": "user"},  
}

def login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    if "role" not in st.session_state:
        st.session_state["role"] = ""
    if "password" not in st.session_state:
        st.session_state["password"] = ""

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

    if not st.session_state["logged_in"]:
        st.title("🔒 تسجيل الدخول")
        st.text_input("اسم المستخدم", key="username")
        st.text_input("كلمة المرور", type="password", key="password")
        st.button("تسجيل الدخول", on_click=check_credentials)
        return False
    else:
        return True

@st.cache_data
def load_reference_data():
    cols_to_use = [3, 4, 7, 21]
    col_names = ["LicensedNumber", "LicenseType", "EventName", "City"]
    df = pd.read_excel(reference_file, usecols=cols_to_use)
    df.columns = col_names
    return df

def load_visits():
    try:
        return pd.read_excel("daily visits.xlsx")
    except FileNotFoundError:
        return pd.DataFrame()

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

    employee_name = st.selectbox("Employee Name (EN)", options=employee_names)
    visit_date = st.date_input("Visit Date (اختر تاريخ الزيارة)")
    visit_status = st.selectbox("Visit Status", options=["لم تتم الزيارة", "تمت الزيارة"])
    visit_purpose = st.selectbox("Visit Purpose", options=["جمع بيانات", "تركيب جهاز HoN", "استلام جهاز HoN"])
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

    if role == "admin":
        visits_df = load_visits()
        if visits_df.empty:
            st.info("لا يوجد ملف daily visits.xlsx بعد. ابدأ بإضافة زيارات.")
        else:
            st.subheader("📂 عرض وتعديل زيارات اليوم")

            selected_index = st.number_input("اختر رقم صف للتعديل أو الحذف", min_value=0, max_value=len(visits_df)-1, step=1)

            selected_row = visits_df.loc[selected_index]

            with st.form("edit_form"):
                new_licensed_number = st.text_input("رقم الترخيص", value=selected_row["LicensedNumber"])
                new_event_name = st.text_input("اسم الفعالية", value=selected_row["EventName"])
                new_license_type = st.text_input("نوع الترخيص", value=selected_row["LicenseType"])
                new_city = st.text_input("المدينة", value=selected_row["City"])
                new_employee_name = st.selectbox("Employee Name (EN)", options=employee_names, index=employee_names.index(selected_row["EmployeeName"]) if selected_row["EmployeeName"] in employee_names else 0)
                new_visit_date = st.date_input("Visit Date (اختر تاريخ الزيارة)", value=selected_row["VisitDate"])
                new_visit_status = st.selectbox("Visit Status", options=["لم تتم الزيارة", "تمت الزيارة"], index=["لم تتم الزيارة", "تمت الزيارة"].index(selected_row["VisitStatus"]))
                new_visit_purpose = st.selectbox("Visit Purpose", options=["جمع بيانات", "تركيب جهاز HoN", "استلام جهاز HoN"], index=["جمع بيانات", "تركيب جهاز HoN", "استلام جهاز HoN"].index(selected_row["VisitPurpose"]))
                new_visit_notes = st.selectbox("Visit Notes", options=visit_notes_options, index=visit_notes_options.index(selected_row["VisitNotes"]) if selected_row["VisitNotes"] in visit_notes_options else 0)
                new_general_notes = st.text_area("General Notes", value=selected_row["GeneralNotes"])

                submitted = st.form_submit_button("تحديث البيانات")
                delete_clicked = st.form_submit_button("حذف السجل")

                if submitted:
                    visits_df.at[selected_index, "LicensedNumber"] = new_licensed_number
                    visits_df.at[selected_index, "EventName"] = new_event_name
                    visits_df.at[selected_index, "LicenseType"] = new_license_type
                    visits_df.at[selected_index, "City"] = new_city
                    visits_df.at[selected_index, "EmployeeName"] = new_employee_name
                    visits_df.at[selected_index, "VisitDate"] = new_visit_date
                    visits_df.at[selected_index, "VisitStatus"] = new_visit_status
                    visits_df.at[selected_index, "VisitPurpose"] = new_visit_purpose
                    visits_df.at[selected_index, "VisitNotes"] = new_visit_notes
                    visits_df.at[selected_index, "GeneralNotes"] = new_general_notes

                    visits_df.to_excel("daily visits.xlsx", index=False)
                    st.success("✅ تم تحديث بيانات الزيارة بنجاح.")

                if delete_clicked:
                    visits_df = visits_df.drop(selected_index).reset_index(drop=True)
                    visits_df.to_excel("daily visits.xlsx", index=False)
                    st.success("✅ تم حذف السجل بنجاح.")

        # زر تحميل الملف
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
        st.info("🔒 لا تملك صلاحية عرض أو تحميل أو تعديل زيارات اليوم.")
