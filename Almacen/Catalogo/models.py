#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
import uuid
from datetime import date

"""
Modelo que representa el material de un tornillo 
P. ej Zinc, Hierro, Inox, Bronce, etc.
"""

class TipoMaterial(models.Model):
	material = models.CharField(max_length=200,help_text='Ingrese un tipo de material (e.g Zincado, Bronce, Inox, etc.)')
	"""
	Cadena que representa a la instancia particular del modelo
	p. ej en el sitio de administración
	"""

	def __str__(self):
		return self.material


class Tornillo(models.Model):
	"""
	Modelo que representa un tornillo (pero no uno muy especifico)
	"""
	Nombre = models.CharField(max_length=200)
	diametro = models.ForeignKey('diametro',on_delete=models.SET_NULL,null=True)
	# ForeignKey, dado que un tornillo tiene un solo diamtreo pero el mismo 
	#diametro puede tener muchas longitudes
	tipomaterial=models.ManyToManyField(TipoMaterial,help_text='Seleccione un tipo de material para este tornillo')

	def display_TipoMaterial(self):
		return ', '.join([tipomaterial.material for tipomaterial in self.tipomaterial.all()[:3]])

	display_TipoMaterial.short_description = 'tipomaterial'



	def get_absolute_url(self):
		"""
		Devuelve el URL a una instancia particular de Tornillo 
		"""
		return reverse("Detalle-Tornillo ", args=[str(self.id)])

	def __str__(self):
		return self.Nombre

class Existencia(models.Model):
	"""
	Modelo que representa la existencia específica de un tornillo(puede ser vendido)
	"""
	id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Codigo particular para el tornillo en todo el inventario')
	tornillo=models.ForeignKey('Tornillo', on_delete=models.SET_NULL,null=True)
	imprint = models.CharField(max_length=500)
	due_back=models.DateField(null=True,blank=True)



	LOAN_STATUS = (
		('d', 'Disponible'),
		('nd', 'No disponible')
	)


	status = models.CharField(max_length=1,choices=LOAN_STATUS,blank=True,default='d',help_text='Disponibilidad del artículo')

	class Meta:
		ordering = ["due_back"]

	def __str__(self):
		return '%s ,%s' % (self.id,self.tornillo.Nombre)



class diametro(models.Model):
	#Modelo que representa los diametros
	primer_diametro = models.CharField(max_length=200)
	ultimo_diametro = models.CharField(max_length=200)


	def get_absolute_url(self):
		return reverse("diametro-detalle",args=[str(self.id)])

	def __str__(self):
		return '%s, %s'%(self.ultimo_diametro,self.primer_diametro)







































