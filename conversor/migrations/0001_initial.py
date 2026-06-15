from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id',          models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome',        models.CharField(max_length=255)),
                ('arquivo_pdf', models.FileField(upload_to='pdfs/')),
                ('conteudo',    models.TextField(blank=True)),
                ('criado_em',   models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
                'ordering': ['-criado_em'],
            },
        ),
    ]
