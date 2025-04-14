import tkinter as tk
import re
import random
import string

# --- Vérification de la robustesse du mot de passe ---
def check_password_strength(password):
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 10
    else:
        suggestions.append("Utilisez au moins 8 caractères.")
    if len(password) >= 12:
        score += 10
    if re.search(r'[a-z]', password):
        score += 20
    else:
        suggestions.append("Ajoutez des lettres minuscules.")
    if re.search(r'[A-Z]', password):
        score += 20
    else:
        suggestions.append("Ajoutez des lettres majuscules.")
    if re.search(r'\d', password):
        score += 20
    else:
        suggestions.append("Ajoutez des chiffres.")
    if re.search(r'[^A-Za-z0-9]', password):
        score += 20
    else:
        suggestions.append("Ajoutez des caractères spéciaux.")
    if re.search(r'(123|abc|password|aaa|111)', password, re.IGNORECASE):
        score -= 20
        suggestions.append("Évitez les séquences simples.")

    return score, suggestions

# --- Affiche le score et les conseils ---
def afficher_resultat():
    pwd = entry.get()
    score, tips = check_password_strength(pwd)

    if score < 50:
        color = "#D32F2F"
        force = "Faible"
    elif score < 70:
        color = "#FBC02D"
        force = "Moyenne"
    elif score < 90:
        color = "#388E3C"
        force = "Bonne"
    else:
        color = "#2E7D32"
        force = "Excellente"

    score_label.config(text="Score :", fg="black")
    score_value.config(text=f"{score}%", fg=color, font=("Arial", 12, "bold"))

    force_label.config(text="Force :", fg="black")
    force_value.config(text=force, fg="black", font=("Arial", 12, "bold"))

    if tips:
        conseils = "\n".join(f"- {tip}" for tip in tips)
        tips_label.config(text=conseils, fg="#FBC02D")
    else:
        conseils = "Mot de passe solide !"
        tips_label.config(text=conseils, fg="black")
        
    crack_time = estimer_temps_crack(pwd)
    crack_time_label.config(text=f"Temps estimé pour le cracker : {crack_time}")



def estimer_temps_crack(pwd):
    charset_size = 0
    if re.search(r'[a-z]', pwd):
        charset_size += 26
    if re.search(r'[A-Z]', pwd):
        charset_size += 26
    if re.search(r'\d', pwd):
        charset_size += 10
    if re.search(r'[^A-Za-z0-9]', pwd):
        charset_size += 32  # caractères spéciaux usuels

    nb_combinaisons = charset_size ** len(pwd)
    attempts_per_second = 1e9  # 1 milliard/sec
    seconds = nb_combinaisons / attempts_per_second

    # Conversion en durée lisible
    if seconds < 60:
        return f"{seconds:.2f} secondes"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} heures"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} jours"
    elif seconds < 3.154e+8:
        return f"{seconds/31536000:.2f} années"
    else:
        return f"{seconds/3.154e+8:.2f} siècles"

    

# --- Génère un mot de passe fort en intégrant l'entrée utilisateur ---
def generer_mot_de_passe():
    original = entry.get()
    base = ""

    if not re.search(r'[A-Z]', original):
        base += random.choice(string.ascii_uppercase)
    if not re.search(r'[a-z]', original):
        base += random.choice(string.ascii_lowercase)
    if not re.search(r'\d', original):
        base += random.choice(string.digits)
    if not re.search(r'[^A-Za-z0-9]', original):
        base += random.choice("!@#$%&*?")

    while len(base) + len(original) < 12:
        base += random.choice(string.ascii_letters + string.digits + "!@#$%&*?")

    insert_pos = random.randint(0, len(base))
    final_password = base[:insert_pos] + original + base[insert_pos:]

    attempt = 0
    while True:
        score, _ = check_password_strength(final_password)
        if score >= 90 or attempt > 10:
            break
        final_password += random.choice(string.ascii_letters + string.digits + "!@#$%&*?")
        attempt += 1

    # Affiche le mot de passe généré sans modifier le champ d’entrée
    generated_title.config(text="Mot de passe sécurisé généré :", fg="black")
    generated_label.config(text=final_password, fg="#2E7D32")
    copy_button.config(state="normal")
    crack_time = estimer_temps_crack(final_password)
    crack_time_label.config(text=f"Temps estimé pour le cracker : {crack_time}")


# --- Copier dans le presse-papier ---
def copier_mot_de_passe():
    root.clipboard_clear()
    root.clipboard_append(generated_label.cget("text"))
    copy_button.config(text="Copié ! ✅", fg="green")
    root.after(1500, lambda: copy_button.config(text="Copier", fg="white"))

# --- GUI ---
root = tk.Tk()
root.title("PASSWORD")
root.geometry("550x500")
root.configure(bg="white")

label = tk.Label(root, text="Entrez pour generer ou tester votre Password :", bg="white", fg="black", font=("Arial", 13))
label.pack(pady=15)

entry = tk.Entry(root, show="", font=("Arial", 14), width=35, bg="white", fg="black")
entry.pack(pady=5)

btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=10)

btn_verif = tk.Button(btn_frame, text="Vérifier", command=afficher_resultat, bg="#1976D2", fg="white", font=("Arial", 12, "bold"), width=15)
btn_verif.grid(row=0, column=0, padx=10)

btn_gen = tk.Button(btn_frame, text="Générer", command=generer_mot_de_passe, bg="#388E3C", fg="white", font=("Arial", 12, "bold"), width=15)
btn_gen.grid(row=0, column=1, padx=10)

# Résultats
score_frame = tk.Frame(root, bg="white")
score_frame.pack(pady=5)

score_label = tk.Label(score_frame, text="", bg="white", font=("Arial", 12))
score_label.grid(row=0, column=0, padx=5, sticky="w")
score_value = tk.Label(score_frame, text="", bg="white", font=("Arial", 12, "bold"))
score_value.grid(row=0, column=1, padx=5, sticky="w")

force_label = tk.Label(score_frame, text="", bg="white", font=("Arial", 12))
force_label.grid(row=1, column=0, padx=5, sticky="w")
force_value = tk.Label(score_frame, text="", bg="white", font=("Arial", 12, "bold"))
force_value.grid(row=1, column=1, padx=5, sticky="w")

# Conseils
tips_label = tk.Label(root, text="", bg="white", font=("Consolas", 11), justify="left", anchor="w", wraplength=500)
tips_label.pack(padx=20, pady=(10, 5), fill="both")

# Zone affichage mot de passe généré
generated_title = tk.Label(root, text="", bg="white", fg="black", font=("Arial", 12, "bold"), justify="center")
generated_title.pack(pady=(15, 0))

generated_label = tk.Label(root, text="", bg="white", fg="#2E7D32", font=("Consolas", 14), justify="center")
generated_label.pack(pady=(5, 0))

crack_time_label = tk.Label(root, text="", bg="white", fg="#444", font=("Arial", 10), justify="center")
crack_time_label.pack(pady=(5, 10))

copy_button = tk.Button(root, text="Copier", command=copier_mot_de_passe,
                        bg="black", fg="white", font=("Arial", 10),
                        relief="solid", borderwidth=1, cursor="hand2")
copy_button.pack(pady=(5, 15))
copy_button.config(state="disabled")

root.mainloop()
