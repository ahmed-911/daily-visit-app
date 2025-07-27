import streamlit as st
import pandas as pd
from datetime import date

# إعدادات عامة
st.set_page_config(page_title="إدارة الزيارات", layout="wide")
st.title("📋 نظام إدارة الزيارات اليومية")

FILENAME = "daily visits.xlsx"

employees = ["Reham Al Otaibi", "Faisal Al Anzi", "Mousa Al Khalifa"]

# تحميل البيانات
def load_visits():
    try:
        return pd.read_excel(FILENAME)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "LicensedNumber", "EventName", "LicenseType", "City", 
            "EmployeeName", "VisitDate", "VisitStatus", 
            "VisitPurpose", "VisitNotes", "GeneralNotes"
        ])

# تحديد نوع المستخدم
role = st.sidebar.selectbox("👤 اختر نوع المستخدم", ["user", "admin"])

# تعبئة بيانات جديدة أو تعديل
st.subheader("➕ إضافة زيارة جديدة")

edit_index = st.session_state.get('edit_index', None)
visits_df = load_visits()

if edit_index is not None:
    edit_row = visits_df.iloc[edit_index]

    licensed_number = st.text_input("🔢 رقم الترخيص", value=edit_row["LicensedNumber"])
    event_name = st.text_input("🎪 اسم الفعالية", value=edit_row["EventName"])
    license_type = st.selectbox("نوع الترخيص", ["مؤقت", "دائم"], index=["مؤقت", "دائم"].index(edit_row["LicenseType"]))
    city = st.text_input("🏙️ المدينة", value=edit_row["City"])
    employee_name = st.selectbox("👥 اسم الموظف", employees, index=employees.index(edit_row["EmployeeName"]))
    visit_date = st.date_input("📅 تاريخ الزيارة", value=pd.to_datetime(edit_row["VisitDate"]).date())
    visit_status = st.radio("🚦 حالة الزيارة", options=["تمت", "لم تتم"], index=["تمت", "لم تتم"].index(edit_row["VisitStatus"]))
    visit_purpose = st.text_area("🎯 الغرض من الزيارة", value=edit_row["VisitPurpose"])
    visit_notes = st.text_area("📝 ملاحظات الزيارة", value=edit_row["VisitNotes"])
    general_notes = st.text_area("🗒️ ملاحظات عامة", value=edit_row["GeneralNotes"])

    if st.button("💾 تحديث البيانات"):
        visits_df.loc[edit_index] = {
            "LicensedNumber": licensed_number,
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
        visits_df.to_excel(FILENAME, index=False)
        st.success("✅ تم تحديث البيانات بنجاح.")
        st.session_state['edit_index'] = None
        st.experimental_rerun()
else:
    licensed_number = st.text_input("🔢 رقم الترخيص")
    event_name = st.text_input("🎪 اسم الفعالية")
    license_type = st.selectbox("نوع الترخيص", ["مؤقت", "دائم"])
    city = st.text_input("🏙️ المدينة")
    employee_name = st.selectbox("👥 اسم الموظف", employees)
    visit_date = st.date_input("📅 تاريخ الزيارة", value=date.today())
    visit_status = st.radio("🚦 حالة الزيارة", options=["تمت", "لم تتم"])
    visit_purpose = st.text_area("🎯 الغرض من الزيارة")
    visit_notes = st.text_area("📝 ملاحظات الزيارة")
    general_notes = st.text_area("🗒️ ملاحظات عامة")

    if st.button("📤 حفظ الزيارة"):
        new_data = {
            "LicensedNumber": licensed_number,
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

        visits_df = pd.concat([visits_df, pd.DataFrame([new_data])], ignore_index=True)
        visits_df.to_excel(FILENAME, index=False)
        st.success("✅ تم حفظ الزيارة بنجاح.")
        st.experimental_rerun()

# عرض أو تحميل البيانات
st.divider()
st.subheader("📥 تحميل / إدارة البيانات")

if visits_df.empty:
    st.info("📭 لا توجد زيارات محفوظة بعد.")
else:
    if role == "user":
        st.download_button("⬇️ تحميل بيانات الزيارات", data=visits_df.to_csv(index=False), file_name="visits.csv", mime="text/csv")
    elif role == "admin":
        for i, row in visits_df.iterrows():
            with st.expander(f"🔹 زيارة {i+1} - {row['LicensedNumber']}"):
                st.write(row)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ تعديل - {i}", key=f"edit_{i}"):
                        st.session_state['edit_index'] = i
                        st.experimental_rerun()

                with col2:
                    if st.button(f"🗑️ حذف - {i}", key=f"delete_{i}"):
                        visits_df.drop(index=i, inplace=True)
                        visits_df.reset_index(drop=True, inplace=True)
                        visits_df.to_excel(FILENAME, index=False)
                        st.success("🗑️ تم حذف الزيارة.")
                        st.experimental_rerun()
