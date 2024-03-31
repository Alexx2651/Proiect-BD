import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import cx_Oracle


class InregistrareWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Înregistrare")


        tk.Label(root, text="Nume:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(root, text="Prenume:").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(root, text="Număr de telefon:").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(root, text="CNP:").grid(row=3, column=0, padx=10, pady=10)

        self.entry_nume = tk.Entry(root)
        self.entry_prenume = tk.Entry(root)
        self.entry_telefon = tk.Entry(root)
        self.entry_cnp = tk.Entry(root)

        self.entry_nume.grid(row=0, column=1, padx=10, pady=10)
        self.entry_prenume.grid(row=1, column=1, padx=10, pady=10)
        self.entry_telefon.grid(row=2, column=1, padx=10, pady=10)
        self.entry_cnp.grid(row=3, column=1, padx=10, pady=10)

        # Buton pentru salvare
        tk.Button(root, text="Salvează", command=self.salveaza_inregistrare).grid(row=4, column=1, pady=10)

    def salveaza_inregistrare(self):

        nume = self.entry_nume.get()
        prenume = self.entry_prenume.get()
        telefon = self.entry_telefon.get()
        cnp = self.entry_cnp.get()

        # Validare simplă
        if not nume or not prenume or not telefon or not cnp:
            messagebox.showwarning("Avertisment", "Toate câmpurile trebuie completate.")
            return

        # Salvare în baza de date Oracle
        try:
            connection = cx_Oracle.connect("bd050", "bd050", "81.180.214.85:1539/orcl")
            cursor = connection.cursor()


            cursor.execute("INSERT INTO inregistrari (nume, prenume, numar_telefon, cnp) VALUES (:1, :2, :3, :4)",
                           (nume, prenume, telefon, cnp))

            connection.commit()
            messagebox.showinfo("Succes", "Înregistrarea a fost salvată cu succes în baza de date.")

            # Închide fereastra de înregistrare după salvare
            self.root.destroy()

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Eroare", f"Eroare la salvarea înregistrării: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class MasiniDisponibileWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Mașini Disponibile")


        self.tree = ttk.Treeview(root, columns=("id","marca", "model", "culoare", "pret", "an_fabricatie", "kilometraj"))
        self.tree.heading("id", text="ID")
        self.tree.heading("marca", text="Marca")
        self.tree.heading("model", text="Model")
        self.tree.heading("culoare", text="Culoare")
        self.tree.heading("pret", text="Pret")
        self.tree.heading("an_fabricatie", text="An Fabricatie")
        self.tree.heading("kilometraj", text="Kilometraj")

        self.tree.pack(expand=True, fill=tk.BOTH)

        # Populează tabelul cu datele din baza de date Oracle
        self.incarca_masini_disponibile()

    def incarca_masini_disponibile(self):
        try:
            # Conectare la baza de date Oracle
            connection = cx_Oracle.connect("bd050", "bd050", "81.180.214.85:1539/orcl")
            cursor = connection.cursor()

            # Execută interogarea pentru a obține mașinile disponibile
            cursor.execute("SELECT id,marca, model, culoare, pret, an_fabricatie, kilometraj FROM Masini")


            rows = cursor.fetchall()
            if not rows:
                print("No data returned from the query.")
            else:
                for row in rows:
                    self.tree.insert("", "end", values=row)




        except cx_Oracle.DatabaseError as e:
            # Tratează erorile la conectare sau interogare
            tk.messagebox.showerror("Eroare", f"Eroare la încărcarea mașinilor disponibile: {e}")

        finally:
            # Închide cursorul și conexiunea
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class InchirieriWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Închirieri")
        #self.root.geometry("600x400")

        # Creează un widget Treeview pentru afișarea tabelului
        self.tree = ttk.Treeview(root, columns=("marca", "model", "an_fabricatie", "pret", "locatie"))
        self.tree.heading("marca", text="Marca")
        self.tree.heading("model", text="Model")
        self.tree.heading("an_fabricatie", text="An Fabricatie")
        self.tree.heading("pret", text="Pret")
        self.tree.heading("locatie", text="Locație")

        self.tree.pack(expand=True, fill=tk.BOTH)

        tk.Button(root, text="Închiriază", command=self.deschide_intrare_nume_prenume).pack(pady=10)

        # Populează tabelul cu datele din baza de date Oracle
        self.incarca_date_inchirieri()

    def deschide_intrare_nume_prenume(self):
        # Deschide o nouă fereastră pentru introducerea numelui și prenumelui
        root_intrare_nume_prenume = tk.Toplevel(self.root)
        IntrareNumePrenumeWindow(root_intrare_nume_prenume, self, self.tree)

    def adauga_in_istoric(self, nume, prenume, marca, model, an_fabricatie, pret, locatie):
            try:
                # Conectare la baza de date Oracle
                connection = cx_Oracle.connect("bd050", "bd050", "81.180.214.85:1539/orcl")
                cursor = connection.cursor()

                # Inserează datele în tabela Istoric_inchirieri
                cursor.execute("""
                        INSERT INTO Istoric_inchirieri (nume, prenume, marca, model, an_fabricatie, pret, locatie)
                        VALUES (:1, :2, :3, :4, :5, :6, :7)
                    """, (nume, prenume, marca, model, an_fabricatie, pret, locatie))

                connection.commit()
                messagebox.showinfo("Succes", "Masina a fost inchiriata și informatiile au fost adăugate în istoric.")

            except cx_Oracle.DatabaseError as e:
                tk.messagebox.showerror("Eroare", f"Eroare la adăugarea în istoricul închirierilor: {e}")

            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

    def incarca_date_inchirieri(self):
        try:
            # Conectare la baza de date Oracle
            connection = cx_Oracle.connect("bd050", "bd050", "81.180.214.85:1539/orcl")
            cursor = connection.cursor()

            # Execută interogarea pentru a obține datele pentru închirieri
            cursor.execute("SELECT marca, model, an_fabricatie, pret_zi, locatie FROM Inchirieri")

            # Fetch all rows at once
            rows = cursor.fetchall()
            if not rows:
                print("No data returned from the query.")
            else:
                for row in rows:
                    self.tree.insert("", "end", values=row)

        except cx_Oracle.DatabaseError as e:
            # Tratează erorile la conectare
            tk.messagebox.showerror("Eroare", f"Eroare la încărcarea datelor pentru închirieri: {e}")

        finally:
            # Închide cursorul și conexiunea
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class LocatiiWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Locații")

        # Creează un widget Treeview pentru afișarea tabelului
        self.tree = ttk.Treeview(root, columns=("oras", "strada", "email", "numar_telefon", "program"))
        self.tree.heading("oras", text="Oraș")
        self.tree.heading("strada", text="Strada")
        self.tree.heading("email", text="Email")
        self.tree.heading("numar_telefon", text="Număr de telefon")
        self.tree.heading("program", text="Program")

        self.tree.pack(expand=True, fill=tk.BOTH)

        # Populează tabelul cu datele din baza de date Oracle
        self.incarca_locatii()

    def incarca_locatii(self):
        try:
            # Conectare la baza de date Oracle
            connection = cx_Oracle.connect("bd050", "bd050", "81.180.214.85:1539/orcl")
            cursor = connection.cursor()

            # Execută interogarea pentru a obține datele pentru locații
            cursor.execute("SELECT oras, strada, email, numar_telefon, program FROM locatii")

            # Fetch all rows at once
            rows = cursor.fetchall()
            if not rows:
                print("No data returned from the query.")
            else:
                for row in rows:
                    self.tree.insert("", "end", values=row)

        except cx_Oracle.DatabaseError as e:
            # Tratează erorile la conectare sau interogare
            tk.messagebox.showerror("Eroare", f"Eroare la încărcarea datelor pentru locații: {e}")

        finally:
            # Închide cursorul și conexiunea
            if cursor:
                cursor.close()
            if connection:
                connection.close()


class IntrareNumePrenumeWindow:
    def __init__(self, root, inchirieri_window, tree_inchirieri):
        self.root = root
        self.inchirieri_window = inchirieri_window
        self.tree_inchirieri = tree_inchirieri  # Stocare referință la tree-ul din InchirieriWindow

        tk.Label(root, text="Nume:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(root, text="Prenume:").grid(row=1, column=0, padx=10, pady=10)

        self.entry_nume = tk.Entry(root)
        self.entry_prenume = tk.Entry(root)

        self.entry_nume.grid(row=0, column=1, padx=10, pady=10)
        self.entry_prenume.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(root, text="Verifică și Închiriază", command=self.verifica_si_inchiriaza).grid(row=2, column=1,
                                                                                                 pady=10)

    def verifica_si_inchiriaza(self):
        nume = self.entry_nume.get()
        prenume = self.entry_prenume.get()

        if not nume or not prenume:
            messagebox.showwarning("Avertisment", "Introduceți Nume și Prenume.")
            return

        # Verifică dacă există înregistrarea cu numele și prenumele date în tabela inregistrari
        self.verifica_existenta_inregistrare(nume, prenume)

    def verifica_existenta_inregistrare(self, nume, prenume):
        try:
            # Conectare la baza de date Oracle
            connection = cx_Oracle.connect("bd050", "bd050", "81.180.214.85:1539/orcl")
            cursor = connection.cursor()

            # Verifică existența înregistrării în tabela inregistrari
            cursor.execute("SELECT COUNT(*) FROM inregistrari WHERE nume = :1 AND prenume = :2", (nume, prenume))
            count = cursor.fetchone()[0]

            if count > 0:
                # Dacă există, obține informațiile despre mașina selectată în tabelul de închirieri
                selected_item = self.tree_inchirieri.selection()  # Folosește tree-ul din InchirieriWindow
                if selected_item:
                    selected_data = self.tree_inchirieri.item(selected_item, 'values')
                    marca = selected_data[0]
                    model = selected_data[1]
                    an_fabricatie = selected_data[2]
                    pret = selected_data[3]
                    locatie = selected_data[4]

                    # Adaugă informațiile în istoricul închirierilor
                    self.inchirieri_window.adauga_in_istoric(nume, prenume, marca, model, an_fabricatie, pret,
                                                             locatie)

                    # Închide fereastra de introducere nume și prenume
                    self.root.destroy()

                else:
                    messagebox.showwarning("Avertisment", "Selectați o mașină din tabelul de închirieri.")
                    return

            else:
                messagebox.showwarning("Avertisment", "Numele și Prenumele nu există în baza de date.")

        except cx_Oracle.DatabaseError as e:
            tk.messagebox.showerror("Eroare", f"Eroare la verificarea existenței înregistrării: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


class ParcAutoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicație Parc Auto")
        self.root.geometry("600x400")

        # Buton pentru înregistrare
        btn_inregistrare = tk.Button(root, text="Înregistrare", command=self.deschide_inregistrare)
        btn_inregistrare.pack(pady=10)

        # Buton pentru mașini disponibile
        btn_masini_disponibile = tk.Button(root, text="Mașini Disponibile", command=self.deschide_masini_disponibile)
        btn_masini_disponibile.pack(pady=10)

        # Buton pentru închirieri
        btn_inchirieri = tk.Button(root, text="Închirieri", command=self.deschide_inchirieri)
        btn_inchirieri.pack(pady=10)

        # Buton pentru locații
        btn_locatii = tk.Button(root, text="Locații", command=self.deschide_locatii)
        btn_locatii.pack(pady=10)

    def deschide_inregistrare(self):
        # Deschide o nouă fereastră pentru înregistrare
        root_inregistrare = tk.Toplevel(self.root)
        InregistrareWindow(root_inregistrare)

    def deschide_masini_disponibile(self):
        # Deschide o nouă fereastră pentru mașini disponibile
        root_masini_disponibile = tk.Toplevel(self.root)
        MasiniDisponibileWindow(root_masini_disponibile)

    def deschide_inchirieri(self):
        # Deschide o nouă fereastră pentru închirieri
        root_inchirieri = tk.Toplevel(self.root)
        InchirieriWindow(root_inchirieri)

    def deschide_locatii(self):
        # Deschide o nouă fereastră pentru locații
        root_locatii = tk.Toplevel(self.root)
        LocatiiWindow(root_locatii)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParcAutoApp(root)
    root.mainloop()