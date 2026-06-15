from django.db import models


class Documento(models.Model):
    nome        = models.CharField(max_length=255)
    arquivo_pdf = models.FileField(upload_to='pdfs/')
    conteudo    = models.TextField(blank=True)
    criado_em   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        return self.nome
