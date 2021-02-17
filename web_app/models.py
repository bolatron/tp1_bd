from django.db import models
from polymorphic.models import PolymorphicModel

class ComputerPart(PolymorphicModel):

    nome = models.CharField(max_length=255, default=None)
    repercussao_twitter = models.IntegerField(default=None)
    avaliacao = models.FloatField(max_length=5.0, default=None)

    def __str__(self):
        return f'{self.nome}'


class ComentariosField(models.Model):
    text = models.TextField(max_length=255)
    computer_part = models.ForeignKey(to=ComputerPart, on_delete=models.CASCADE)

class NoticiaField(models.Model):
    url = models.URLField(max_length=255)
    data_publicacao = models.DateField()
    computer_part = models.ForeignKey(to=ComputerPart, on_delete=models.CASCADE)

class CPU(ComputerPart):
    
    nucleos = models.IntegerField()
    clock = models.FloatField()
    tdp = models.IntegerField()

    def tdp_(self):
        return '%d W' % (self.tdp)

class GPU(ComputerPart):

    vram = models.IntegerField()
    shaders = models.IntegerField()
    tdp = models.IntegerField()

class RAM(ComputerPart):

    freq = models.IntegerField()
    capacidade = models.IntegerField()

class PowerSupply(ComputerPart):

    potencia = models.IntegerField()

class Motherboard(ComputerPart):

    soquete = models.CharField(max_length=255)

class SecondaryMemory(ComputerPart):
    
    tipo = models.CharField(
        max_length=3,
        choices=(
            ('SSD', 'ssd'),
            ('HDD', 'hdd'),
        ),
        default=None
    )
    capacidade = models.IntegerField()