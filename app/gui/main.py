import customtkinter as ctk
from tkinter import messagebox
from app.services.user_service import authenticate_user, create_user
from app.database.db import initialize_database
from app.services.user_service import authenticate_user
from app.services.role_service import has_permission
from app.services.patient_service import (
    create_patient,
    get_all_patients,
    update_patient,
    delete_patient,
)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
from app.database.db import get_connection

class HospitalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hospital Management System")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.current_user = None
        self.show_login()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()

        container = ctk.CTkFrame(self, corner_radius=18)
        container.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            relwidth=0.42,
            relheight=0.58,
        )

        ctk.CTkLabel(
            container,
            text="Hospital Management System",
            font=ctk.CTkFont(size=25, weight="bold"),
            wraplength=350,
        ).pack(pady=(35, 8), padx=20)

        ctk.CTkLabel(
            container,
            text="Sign in to continue",
            font=ctk.CTkFont(size=14),
            text_color="gray",
        ).pack(pady=(0, 25))

        self.username_entry = ctk.CTkEntry(
            container,
            placeholder_text="Username",
            height=42,
        )
        self.username_entry.pack(fill="x", padx=35, pady=8)

        self.password_entry = ctk.CTkEntry(
            container,
            placeholder_text="Password",
            show="*",
            height=42,
        )
        self.password_entry.pack(fill="x", padx=35, pady=8)
        self.password_entry.bind(
            "<Return>",
            lambda event: self.login(),
        )

        ctk.CTkButton(
            container,
            text="Login",
            height=42,
            command=self.login,
        ).pack(fill="x", padx=35, pady=(20, 12))

        ctk.CTkLabel(
            container,
            text="Authorized users only",
            text_color="gray",
        ).pack(pady=(4, 15))

        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Missing information",
                "Enter both username and password.",
                parent=self,
            )
            return

        try:
            user = authenticate_user(username, password)
        except Exception:
            messagebox.showerror(
                "Login error",
                "Unable to access the user database. "
                "Check the application logs or database configuration.",
                parent=self,
            )
            return

        if user is None:
            messagebox.showerror(
                "Login failed",
                "Invalid username or password, or the account is inactive.",
                parent=self,
            )
            return

        self.current_user = user
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_window()

        user = self.current_user
        role = user["role"]

        sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="HOSPITAL HMS",
            font=ctk.CTkFont(size=21, weight="bold"),
        ).pack(padx=15, pady=(30, 8))

        ctk.CTkLabel(
            sidebar,
            text=f"{user['username']}\\n{role}",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 25))
        if has_permission(role, "view_patients"):
            ctk.CTkButton(
                sidebar,
                text="Patients",
                command=self.show_patient_management,
            ).pack(fill="x", padx=20, pady=8)
        content = ctk.CTkFrame(self, corner_radius=0)
        content.pack(
            side="right",
            fill="both",
            expand=True,
            padx=0,
            pady=0,
        )

        ctk.CTkLabel(
            content,
            text="Dashboard",
            font=ctk.CTkFont(size=30, weight="bold"),
        ).pack(anchor="w", padx=35, pady=(35, 8))

        ctk.CTkLabel(
            content,
            text="Hospital operations overview",
            font=ctk.CTkFont(size=15),
            text_color="gray",
        ).pack(anchor="w", padx=35, pady=(0, 25))

        cards = ctk.CTkFrame(content, fg_color="transparent")
        cards.pack(fill="x", padx=25, pady=5)

        available_sections = [
            ("Patients", "view_patients"),
            ("Doctors", "view_doctors"),
            ("Appointments", "view_appointments"),
            ("Medical Records", "view_medical_records"),
            ("Billing", "view_bills"),
        ]

        for title, permission in available_sections:
            if has_permission(role, permission):
                card = ctk.CTkFrame(cards, corner_radius=12)
                card.pack(
                    fill="x",
                    padx=10,
                    pady=8,
                )

                ctk.CTkLabel(
                    card,
                    text=title,
                    font=ctk.CTkFont(size=18, weight="bold"),
                ).pack(anchor="w", padx=18, pady=(14, 4))

                ctk.CTkLabel(
                    card,
                    text="Management screen will be connected in the next step.",
                    text_color="gray",
                    wraplength=500,
                ).pack(anchor="w", padx=18, pady=(0, 14))
        if role == "Admin":
            ctk.CTkButton(
                sidebar,
                text="Manage Users",
                command=self.show_user_management,
            ).pack(fill="x", padx=20, pady=8)

        if has_permission(role, "view_audit_logs"):
            ctk.CTkLabel(
                content,
                text="Audit log access enabled",
                text_color="green",
            ).pack(anchor="w", padx=35, pady=15)

        ctk.CTkButton(
            sidebar,
            text="Logout",
            command=self.logout,
        ).pack(side="bottom", fill="x", padx=20, pady=25)
    
    def show_user_management(self):
        if not self.current_user or self.current_user["role"] != "Admin":
            messagebox.showerror(
                "Access denied",
                "Only administrators can create user accounts.",
                parent=self,
            )
            return

        self.clear_window()

        content = ctk.CTkFrame(self, corner_radius=0)
        content.pack(fill="both", expand=True, padx=35, pady=30)

        ctk.CTkLabel(
            content,
            text="Create User Account",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(anchor="w", pady=(10, 8))

        ctk.CTkLabel(
            content,
            text="Create an account for an authorized hospital user.",
            text_color="gray",
        ).pack(anchor="w", pady=(0, 20))

        username_entry = ctk.CTkEntry(
            content,
            placeholder_text="Username",
            height=40,
        )
        username_entry.pack(fill="x", pady=8)

        password_entry = ctk.CTkEntry(
            content,
            placeholder_text="Temporary password (minimum 8 characters)",
            show="*",
            height=40,
        )
        password_entry.pack(fill="x", pady=8)

        role_menu = ctk.CTkOptionMenu(
            content,
            values=["Staff", "Doctor", "Admin"],
            height=40,
        )
        role_menu.pack(fill="x", pady=8)

        def submit_user():
            username = username_entry.get().strip()
            password = password_entry.get()
            role = role_menu.get()

            if not username or not password:
                messagebox.showwarning(
                    "Missing information",
                    "Enter a username and password.",
                    parent=self,
                )
                return

            if len(password) < 8:
                messagebox.showwarning(
                    "Invalid password",
                    "Password must contain at least 8 characters.",
                    parent=self,
                )
                return

            try:
                user_id = create_user({
                    "username": username,
                    "password": password,
                    "role": role,
                    "is_active": 1,
                })
            except Exception as exc:
                messagebox.showerror(
                    "Account creation failed",
                    f"Could not create the account.\n{exc}",
                    parent=self,
                )
                return

            messagebox.showinfo(
                "Success",
                f"Account created successfully.\nUser ID: {user_id}",
                parent=self,
            )
            username_entry.delete(0, "end")
            password_entry.delete(0, "end")
            role_menu.set("Staff")

        ctk.CTkButton(
            content,
            text="Create Account",
            height=42,
            command=submit_user,
        ).pack(fill="x", pady=(18, 8))

        ctk.CTkButton(
            content,
            text="Back to Dashboard",
            fg_color="gray",
            hover_color="dimgray",
            command=self.show_dashboard,
        ).pack(fill="x", pady=8)


    def show_patient_management(self):
        user = self.current_user

        if not user or not has_permission(
            user["role"], "view_patients"
        ):
            messagebox.showerror(
                "Access denied",
                "You do not have permission to view patients.",
                parent=self,
            )
            return

        self.clear_window()

        page = ctk.CTkFrame(self, corner_radius=0)
        page.pack(fill="both", expand=True, padx=25, pady=20)

        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            header,
            text="Patient Management",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="Back to Dashboard",
            command=self.show_dashboard,
        ).pack(side="right")

        body = ctk.CTkFrame(page, fg_color="transparent")
        body.pack(fill="both", expand=True)

        # Patient registration form
        form_container = ctk.CTkFrame(body, width=320)
        form_container.pack(side="left", fill="y", padx=(0, 15))
        form_container.pack_propagate(False)

        form = ctk.CTkScrollableFrame(
            form_container,
            width=280,
            label_text="Register Patient",
        )
        form.pack(fill="both", expand=True, padx=5, pady=5)


        fields = {}
        selected_patient = {"id": None}

        def add_field(key, label):
            ctk.CTkLabel(form, text=label).pack(
                anchor="w", padx=15, pady=(5, 0)
            )
            entry = ctk.CTkEntry(form, height=35)
            entry.pack(fill="x", padx=15, pady=(2, 5))
            fields[key] = entry

        add_field("patient_code", "Patient Code")
        add_field("name", "Full Name")
        add_field("age", "Age")

        ctk.CTkLabel(form, text="Gender").pack(
            anchor="w", padx=15, pady=(5, 0)
        )
        gender_menu = ctk.CTkOptionMenu(
            form,
            values=["Male", "Female", "Other"],
            height=35,
        )
        gender_menu.pack(fill="x", padx=15, pady=(2, 5))

        add_field("blood_group", "Blood Group (optional)")
        add_field("phone", "Phone (optional)")
        add_field("address", "Address (optional)")
        add_field("emergency_contact", "Emergency Contact (optional)")

        # Existing patient records
        listing = ctk.CTkFrame(body)
        listing.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            listing,
            text="Registered Patients",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", padx=15, pady=15)

        patient_list = ctk.CTkScrollableFrame(listing)
        patient_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        def refresh_patients():
            for widget in patient_list.winfo_children():
                widget.destroy()

            try:
                patients = get_all_patients(role=user["role"])
            except Exception as exc:
                messagebox.showerror(
                    "Error",
                    f"Could not load patients:\n{exc}",
                    parent=self,
                )
                return

            if isinstance(patients, dict) and not patients.get("success", True):
                messagebox.showerror(
                    "Error",
                    patients.get("message", "Could not load patients."),
                    parent=self,
                )
                return

            if not patients:
                ctk.CTkLabel(
                    patient_list,
                    text="No patient records found.",
                    text_color="gray",
                ).pack(pady=20)
                return

            for patient in patients:
                card = ctk.CTkFrame(patient_list)
                card.pack(fill="x", padx=5, pady=5)

                ctk.CTkLabel(
                    card,
                    text=(
                        f"{patient['patient_code']} — {patient['name']}"
                    ),
                    font=ctk.CTkFont(size=15, weight="bold"),
                ).pack(anchor="w", padx=12, pady=(10, 3))

                ctk.CTkLabel(
                    card,
                    text=(
                        f"Age: {patient['age']} | "
                        f"Gender: {patient['gender']} | "
                        f"Phone: {patient['phone'] or 'Not provided'}"
                    ),
                    wraplength=430,
                ).pack(anchor="w", padx=12, pady=(0, 10))
                actions = ctk.CTkFrame(card, fg_color="transparent")
                actions.pack(fill="x", padx=12, pady=(0, 10))

                if has_permission(user["role"], "update_patients"):
                    def edit_selected(p=patient):
                        selected_patient["id"] = p["id"]

                        for key, entry in fields.items():
                            value = p[key]
                            entry.delete(0, "end")
                            entry.insert(0, "" if value is None else str(value))

                        gender_menu.set(p["gender"])
                        submit_button.configure(text="Save Changes")

                    ctk.CTkButton(
                        actions,
                        text="Edit",
                        width=90,
                        command=edit_selected,
                    ).pack(side="left", padx=(0, 8))

                if has_permission(user["role"], "delete_patients"):
                    def delete_selected(patient):
                    
                        patient_id = patient["id"]

                        if not messagebox.askyesno(
                            "Confirm Deletion",
                            f"Are you sure you want to delete {patient['name']}?",
                            parent=self,
                        ):
                            return

                        connection = get_connection()
                        

                        try:
                            related_records = {
                                "appointments": connection.execute(
                                    "SELECT COUNT(*) FROM appointments WHERE patient_id = ?",
                                    (patient_id,),
                                ).fetchone()[0],
                                "medical records": connection.execute(
                                    "SELECT COUNT(*) FROM medical_records WHERE patient_id = ?",
                                    (patient_id,),
                                ).fetchone()[0],
                                "bills": connection.execute(
                                    "SELECT COUNT(*) FROM bills WHERE patient_id = ?",
                                    (patient_id,),
                                ).fetchone()[0],
                            }
                        except Exception as error:
                            messagebox.showerror(
                                "Database Error",
                                f"Could not check related records:\n{error}",
                                parent=self,
                            )
                            return
                        finally:
                            connection.close()

                        linked = [
                            f"{count} {name}"
                            for name, count in related_records.items()
                            if count > 0
                        ]

                        if linked:
                            messagebox.showwarning(
                                "Cannot Delete Patient",
                                "This patient has linked records:\n\n"
                                + "\n".join(linked)
                                + "\n\nThese records must be preserved. "
                                "The patient cannot be permanently deleted.",
                                parent=self,
                            )
                            return

                        result = delete_patient(
                            patient_id,
                            role=user["role"],
                            user_id=user.get("id"),
                        )

                        if isinstance(result, dict) or not result:
                            details = (
                                result.get("message", "Patient was not deleted.")
                                if isinstance(result, dict)
                                else "Patient was not deleted."
                            )

                            messagebox.showerror(
                                "Deletion Failed",
                                details,
                                parent=self,
                            )
                            return

                        if selected_patient["id"] == patient_id:
                            selected_patient["id"] = None
                            submit_button.configure(text="Register Patient")

                        refresh_patients()

                        messagebox.showinfo(
                            "Success",
                            "Patient deleted successfully.",
                            parent=self,
                        )


                        confirmed = messagebox.askyesno(
                            "Confirm deletion",
                            f"Delete patient {p['name']} ({p['patient_code']})?",
                            parent=self,
                        )

                        if not confirmed:
                            return

                        try:
                            result = delete_patient(
                                p["id"],
                                role=user["role"],
                                user_id=user["id"],
                            )
                        except Exception as exc:
                            messagebox.showerror(
                                "Deletion failed",
                                f"Could not delete patient:\n{exc}",
                                parent=self,
                            )
                            return

                        
                        if isinstance(result, dict) or not result:
                            if isinstance(result, dict):
                                details = result.get("message", "Patient was not deleted.")

                                if result.get("error"):
                                    details += f"\n\nDatabase details:\n{result['error']}"

                                if result.get("errors"):
                                    details += "\n\n" + "\n".join(result["errors"])
                            else:
                                details = "Patient was not deleted."

                            messagebox.showerror(
                                "Deletion failed",
                                details,
                                parent=self,
                            )
                            return


                        selected_patient["id"] = None
                        for entry in fields.values():
                            entry.delete(0, "end")

                        submit_button.configure(text="Register Patient")
                        refresh_patients()

                        messagebox.showinfo(
                            "Success",
                            "Patient deleted successfully.",
                            parent=self,
                        )
                    ctk.CTkButton(
                            actions,
                            text="Delete",
                            width=90,
                            fg_color="#B42318",
                            hover_color="#8E1B13",
                            command=lambda p=patient: delete_selected(p),
                    ).pack(side="left")
                    

        def submit_patient():
            if not has_permission(user["role"], "create_patients"):
                messagebox.showerror(
                    "Access denied",
                    "You cannot register patients.",
                    parent=self,
                )
                return

            data = {
                key: entry.get().strip()
                for key, entry in fields.items()
            }
            data["gender"] = gender_menu.get()

            try:
                data["age"] = int(data["age"])
            except ValueError:
                messagebox.showwarning(
                    "Invalid age",
                    "Enter a valid whole-number age.",
                    parent=self,
                )
                return

            for key in (
                "blood_group",
                "phone",
                "address",
                "emergency_contact",
            ):
                if not data[key]:
                    data[key] = None

            try:
                if selected_patient["id"] is not None:
                    result = update_patient(
                        selected_patient["id"],
                        data,
                        role=user["role"],
                        user_id=user["id"],
                    )
                else:
                    result = create_patient(
                        data,
                        role=user["role"],
                        user_id=user["id"],
                )
            except Exception as exc:
                messagebox.showerror(
                    "Registration error",
                    f"Could not register patient:\n{exc}",
                    parent=self,
                )
                return

            if isinstance(result, dict):
                details = result.get("message", "Registration failed.")
                errors = result.get("errors", [])
                if errors:
                    details += "\n\n" + "\n".join(errors)

                messagebox.showerror(
                    "Registration failed",
                    details,
                    parent=self,
                )
                return

            if not result:
                messagebox.showerror(
                    "Registration failed",
                    "The patient record was not created.",
                    parent=self,
                )
                return

            was_editing = selected_patient["id"] is not None

            messagebox.showinfo(
                "Success",
                "Patient updated successfully."
                if was_editing
                else f"Patient registered successfully.\nPatient ID: {result}",
                parent=self,
            )

            selected_patient["id"] = None

            for entry in fields.values():
                entry.delete(0, "end")

            gender_menu.set("Male")
            submit_button.configure(text="Register Patient")
            refresh_patients()

            for entry in fields.values():
                entry.delete(0, "end")

            gender_menu.set("Male")
            refresh_patients()

        if has_permission(user["role"], "create_patients"):
            submit_button = ctk.CTkButton(
                form,
                text="Register Patient",
                height=40,
                command=submit_patient,
            )
            submit_button.pack(fill="x", padx=15, pady=12)

        refresh_patients()

    def logout(self):
        self.current_user = None
        self.show_login()


def main():
    initialize_database()
    app = HospitalApp()
    app.mainloop()


if __name__ == "__main__":
    main()
