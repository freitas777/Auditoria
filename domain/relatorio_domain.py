import os
import json
from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class DominioRelatorio:
    def criar_arquivo_relatorio(self, logs: list[dict], formato: str, tipo: str, id_verificacao: int) -> str:
        os.makedirs("relatorios", exist_ok=True)
        filename = f"{tipo.upper()}_{id_verificacao}.{formato.lower()}"
        path = Path("relatorios") / filename
        
        fmt = formato.lower()
        match fmt:
            case "json":
                self._gerar_json(logs, tipo, id_verificacao, path)
            case "txt":
                self._gerar_txt(logs, tipo, id_verificacao, path)
            case "pdf":
                self._gerar_pdf(logs, tipo, id_verificacao, path)
            case _:
                raise ValueError(f"Formato '{formato}' não suportado.")
        return str(path)

    def _cabecalho(self, tipo: str, id_verificacao: int) -> str:
        return f"Relatório de {tipo.upper()} para Verificação ID: {id_verificacao}"

    def _gerar_json(self, logs: list[dict], tipo: str, id_verificacao: int, path: Path):
        data = {
            "tipo_relatorio": tipo,
            "id_verificacao": id_verificacao,
            "logs": logs
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _gerar_txt(self, logs, tipo, id_verificacao, path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self._cabecalho(tipo, id_verificacao) + "\n\n")
            for log in logs:
                for chave, valor in log.items():
                    f.write(f"{chave}: {valor}\n")
                f.write("---\n")

    def _gerar_pdf(self, logs, tipo, id_verificacao, path):
        doc = SimpleDocTemplate(str(path), pagesize=LETTER)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(self._cabecalho(tipo, id_verificacao), styles['Title']))
        story.append(Spacer(1, 12))

        for log in logs:
            for chave, valor in log.items():
                story.append(Paragraph(f"<b>{chave}:</b> {valor}", styles['Normal']))
            story.append(Spacer(1, 12))

        doc.build(story)