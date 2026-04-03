import pandas as pd
from fpdf import FPDF

def export_to_excel(df, filename="outputs/Reporting_VaR.xlsx"):
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Backtesting', index=False)
    writer.close()

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Rapport Risque - Synthese VaR', 0, 1, 'C')
        self.ln(5)

def generate_pdf(df, filename="outputs/Rapport_Direction.pdf"):
    pdf = PDF()
    pdf.add_page()
    
    # En-têtes
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(45, 10, 'Methode', 1)
    pdf.cell(30, 10, 'Exceptions', 1)
    pdf.cell(35, 10, 'Taux Obs.', 1)
    pdf.cell(40, 10, 'Statut', 1)
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    
    # Utilisation des indices numériques pour éviter les erreurs de KeyError
    # row[0] est la 1ère colonne, row[1] la 2ème, etc.
    for i, row in df.iterrows():
        # On extrait les données par position pour être sûr
        methode_val = str(row.iloc[0])
        exceptions_val = str(row.iloc[1])
        taux_val = f"{row.iloc[2]}%"
        statut_val = str(row.iloc[4])

        pdf.cell(45, 10, methode_val, 1)
        pdf.cell(30, 10, exceptions_val, 1)
        pdf.cell(35, 10, taux_val, 1)
        
        # Couleur du texte pour le statut
        if "Valide" in statut_val:
            pdf.set_text_color(0, 128, 0) # Vert
        else:
            pdf.set_text_color(255, 0, 0) # Rouge
            
        pdf.cell(40, 10, statut_val, 1)
        pdf.set_text_color(0, 0, 0) # Retour au noir
        pdf.ln()
        
    pdf.output(filename)