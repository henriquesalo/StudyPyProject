from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'<Categoria {self.nome}>'
    

class Flashcard(models.Model):
    DIFICULDADE_CHOICES = (('D', 'Difícil'), ('M', 'Médio'), ('F', 'Fácil'))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    pergunta = models.CharField(max_length=100)
    resposta = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    dificuldade = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES)

    def __str__(self):
        return f'<Flashcard {self.pergunta}>'
    
    @property
    def css_dificuldade(self):
        if self.dificuldade == "F":
            return 'flashcard-facil'
        elif self.dificuldade == "M":
            return 'flashcard-medio'
        return 'flashcard-dificil'


class FlashcardDesafio(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.DO_NOTHING)
    respondido = models.BooleanField(default=False)
    acertou = models.BooleanField(default=False)

    def __str__(self):
        return str(self.flashcard)

class Desafio(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=100)
    categoria = models.ManyToManyField(Categoria)
    quantidade_perguntas = models.IntegerField()
    dificuldade = models.CharField(max_length=1, choices=Flashcard.DIFICULDADE_CHOICES)
    flashcards = models.ManyToManyField(FlashcardDesafio)

    def __str__(self):
        return f'<Desafio {self.titulo}>'
    
    @property
    def status(self):
        count = self.flashcards.filter(respondido=True)
        res = len(count)
        percentage = (res/self.quantidade_perguntas) * 100
        return f'{percentage:.2f}%'
            