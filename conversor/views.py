import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from pypdf import PdfReader

from .models import Documento


def _extrair_texto(caminho_pdf: str) -> str:
    """Lê todas as páginas do PDF e retorna o texto concatenado."""
    reader = PdfReader(caminho_pdf)
    partes = []
    for i, pagina in enumerate(reader.pages, start=1):
        texto = pagina.extract_text() or ""
        partes.append(f"=== Página {i} ===\n{texto}")
    return "\n\n".join(partes)


# ─── Upload e conversão ───────────────────────────────────────────────────────

def upload(request):
    erro = None

    if request.method == 'POST':
        arquivo = request.FILES.get('pdf')

        if not arquivo:
            erro = 'Selecione um arquivo PDF antes de enviar.'
        elif not arquivo.name.lower().endswith('.pdf'):
            erro = 'Somente arquivos .pdf são aceitos.'
        else:
            # Salva o registro (o arquivo é gravado em media/pdfs/)
            doc = Documento(nome=arquivo.name, arquivo_pdf=arquivo)
            doc.save()

            # Extrai texto do PDF já salvo em disco
            caminho_pdf = os.path.join(settings.MEDIA_ROOT, doc.arquivo_pdf.name)
            doc.conteudo = _extrair_texto(caminho_pdf)
            doc.save()

            return redirect('detalhe', pk=doc.pk)

    return render(request, 'conversor/upload.html', {'erro': erro})


# ─── Detalhe / prévia ─────────────────────────────────────────────────────────

def detalhe(request, pk):
    doc = get_object_or_404(Documento, pk=pk)
    return render(request, 'conversor/detalhe.html', {'doc': doc})


# ─── Download do .txt ─────────────────────────────────────────────────────────

def baixar_txt(request, pk):
    doc = get_object_or_404(Documento, pk=pk)
    nome_txt = os.path.splitext(doc.nome)[0] + '.txt'
    response = HttpResponse(doc.conteudo, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{nome_txt}"'
    return response


# ─── Lista de documentos ─────────────────────────────────────────────────────

def lista(request):
    documentos = Documento.objects.all()
    return render(request, 'conversor/lista.html', {'documentos': documentos})


# ─── Excluir documento ───────────────────────────────────────────────────────

def excluir(request, pk):
    doc = get_object_or_404(Documento, pk=pk)
    if request.method == 'POST':
        # Remove arquivo físico do PDF
        if doc.arquivo_pdf and os.path.exists(doc.arquivo_pdf.path):
            os.remove(doc.arquivo_pdf.path)
        doc.delete()
        return redirect('lista')
    return render(request, 'conversor/confirmar_exclusao.html', {'doc': doc})
