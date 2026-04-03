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
    
    # En-têtes du tableau
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(45, 10, 'Methode', 1)
    pdf.cell(30, 10, 'Exceptions', 1)
    pdf.cell(35, 10, 'Taux Obs.', 1)
    pdf.cell(40, 10, 'Statut', 1)
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    
    for i, row in df.iterrows():
        # Extraction sécurisée par position pour éviter les KeyError
        methode_val = str(row.iloc[0])    # Colonne 'Methode'
        exceptions_val = str(row.iloc[1]) # Colonne 'Exceptions'
        taux_val = f"{row.iloc[2]}%"     # Colonne 'Taux_Obs'
        statut_raw = str(row.iloc[4])    # Colonne 'Statut'

        # Nettoyage des emojis pour le PDF (FPDF ne supporte pas ✅/❌)
        clean_statut = statut_raw.replace('✅', '').replace('❌', '').strip()

        # Écriture des données
        pdf.cell(45, 10, methode_val, 1)
        pdf.cell(30, 10, exceptions_val, 1)
        pdf.cell(35, 10, taux_val, 1)
        
        # Couleur dynamique pour le statut
        if "Valide" in clean_statut:
            pdf.set_text_color(0, 128, 0) # Vert
        else:
            pdf.set_text_color(255, 0, 0) # Rouge
            
        pdf.cell(40, 10, clean_statut, 1)
        pdf.set_text_color(0, 0, 0) # Reset en noir
        pdf.ln()
        
    # Vérification du dossier outputs
    import os
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
        
    pdf.output(filename)