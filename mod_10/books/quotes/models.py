from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=120)
    slug = models.CharField(max_length=120, unique=True)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self) -> str:
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self) -> str:
        return self.tag


class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return f"{self.quote[:45]} ..."
