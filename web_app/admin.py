from django.contrib import admin

from .models import CPU, GPU, RAM, SecondaryMemory, Motherboard, PowerSupply, ComentariosField
# Register your models here.

admin.site.site_header = 'Administração'

class CPUPost(admin.ModelAdmin):
    list_display = ('nome', 'nucleos', 'clock', 'tdp_', 'avaliacao')

class GPUPost(admin.ModelAdmin):
    list_display = ('nome', 'shaders', 'vram', 'tdp', 'avaliacao')

class RAMPost(admin.ModelAdmin):
    list_display = ('nome', 'freq', 'capacidade', 'avaliacao')

class PowerSupplyPost(admin.ModelAdmin):
    list_display = ('nome', 'potencia', 'avaliacao')

class MotherboardPost(admin.ModelAdmin):
    list_display = ('nome', 'soquete', 'avaliacao')

class SecondaryMemoryPost(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'capacidade', 'avaliacao')

class ComentariosPost(admin.ModelAdmin):
    list_display = ('text', 'computer_part')

admin.site.register(CPU, CPUPost)
admin.site.register(GPU, GPUPost)
admin.site.register(RAM, RAMPost)
admin.site.register(PowerSupply, PowerSupplyPost)
admin.site.register(Motherboard, MotherboardPost)
admin.site.register(SecondaryMemory, SecondaryMemoryPost)

admin.site.register(ComentariosField, ComentariosPost)