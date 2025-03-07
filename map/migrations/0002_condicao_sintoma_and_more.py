# Generated by Django 5.1.5 on 2025-03-07 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_condicao', models.CharField(max_length=45)),
                ('gravidade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sintoma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_sintoma', models.CharField(max_length=45)),
            ],
        ),
        migrations.RenameField(
            model_name='unidadeatendimento',
            old_name='convenio',
            new_name='convenios',
        ),
        migrations.AlterField(
            model_name='convenio',
            name='nome_convenio',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='bairro',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='cep',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='cidade',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='estado',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='latitude',
            field=models.DecimalField(decimal_places=5, max_digits=7),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='logradouro',
            field=models.CharField(max_length=75),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='longitude',
            field=models.DecimalField(decimal_places=5, max_digits=7),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='numero',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='pais',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='unidadeatendimento',
            name='especialidade',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='unidadeatendimento',
            name='horario_atendimento',
            field=models.CharField(max_length=75),
        ),
        migrations.AlterField(
            model_name='unidadeatendimento',
            name='nome',
            field=models.CharField(max_length=75),
        ),
        migrations.AlterField(
            model_name='unidadeatendimento',
            name='tempo_medio_espera',
            field=models.TimeField(),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_usuario', models.CharField(max_length=45)),
                ('sobrenome_usuario', models.CharField(max_length=100)),
                ('dt_nasc', models.DateField()),
                ('altura', models.DecimalField(decimal_places=2, max_digits=3)),
                ('dt_cadastro', models.DateField()),
                ('condicoes', models.ManyToManyField(to='map.condicao')),
                ('convenio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='map.convenio')),
            ],
        ),
        migrations.CreateModel(
            name='Triagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('temperatura', models.DecimalField(decimal_places=1, max_digits=3)),
                ('pressao_sistolica', models.IntegerField()),
                ('pressao_diastolica', models.IntegerField()),
                ('gravidez', models.IntegerField()),
                ('horario_realizacao', models.TimeField()),
                ('data_realizacao', models.DateField()),
                ('sintomas', models.ManyToManyField(to='map.sintoma')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.usuario')),
            ],
        ),
    ]
