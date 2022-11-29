from django.db import models
from django.db.models import F

from apps.accounts.models import CustomUser
from apps.core.models import Ability, Color, Faction, PassiveAbility, Type


class Leader(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, unique=True)
    unlocked = models.BooleanField(default=True)  # True - unlocked, False - locked
    faction = models.ForeignKey(Faction, related_name="leaders",
                                on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, related_name='leaders',
                                on_delete=models.PROTECT)
    damage = models.IntegerField(default=0, blank=False, null=False)
    charges = models.IntegerField(default=1, blank=False, null=False)
    image = models.ImageField(upload_to='leaders/', blank=True, null=True)
    has_passive = models.BooleanField(default=False)
    passive_ability = models.ForeignKey(PassiveAbility, related_name='leaders',
                                        on_delete=models.PROTECT,
                                        blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.name}, ability {self.ability}, damage {self.damage} charges {self.charges}'

    class Meta:
        ordering = ("faction", "-damage")


class Card(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    unlocked = models.BooleanField(default=True)  # True - unlocked, False - locked
    faction = models.ForeignKey(Faction, related_name='cards',
                                on_delete=models.PROTECT)
    color = models.ForeignKey(Color, related_name='cards',
                              on_delete=models.PROTECT)
    type = models.ForeignKey(Type, related_name='cards',
                             on_delete=models.PROTECT)
    ability = models.ForeignKey(Ability, related_name='cards',
                                on_delete=models.PROTECT)
    charges = models.IntegerField(default=1, blank=False, null=False)
    damage = models.IntegerField(default=0, blank=False, null=False)
    hp = models.IntegerField(default=0, blank=False, null=False)
    heal = models.IntegerField(default=0, blank=False, null=False)
    image = models.ImageField(upload_to='cards/', blank=True, null=True)
    has_passive = models.BooleanField(default=False)
    has_passive_in_hand = models.BooleanField(default=False)
    passive_ability = models.ForeignKey(PassiveAbility, related_name='cards',
                                        on_delete=models.PROTECT,
                                        blank=True, null=True, default=None)
    timer = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f'{self.id} {self.name}, hp {self.hp}, ' \
               f'ability {self.ability}, damage {self.damage}, heal {self.heal} '

    class Meta:
        ordering = ("-color", "-damage", "-hp", "-charges")

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        # customization to store the original field values on the instance
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    def save(self, *args, **kwargs):
        diff = self.hp - self._loaded_values['hp']
        if not self._state.adding and diff:
            self.change_decks_health(diff)
        super().save(*args, **kwargs)

    def change_decks_health(self, diff):
        """Изменяет параметр health на diff пунктов у всех колод, содержащих
            текущую карту
        """
        decks = Deck.objects.filter(d__card_id=self.id).prefetch_related('d__deck')
        for deck in decks:
            deck.health = F('health') + diff
            deck.save()
        print(f"Deck health changed for {len(decks)} decks")


class Deck(models.Model):
    """Модель колоды"""
    name = models.CharField(max_length=32, blank=False, null=False)
    cards = models.ManyToManyField(Card,
                                   related_name="cards",
                                   through="CardDeck")
    health = models.IntegerField(blank=False, null=False, default=0)
    leader = models.ForeignKey("Leader", related_name="decks",
                               on_delete=models.CASCADE,
                               blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.id}, name {self.name}, health {self.health}, {self.leader}'


class CardDeck(models.Model):
    """Связи колод и карт в них"""
    card = models.ForeignKey("Card", related_name="d", on_delete=models.CASCADE)
    deck = models.ForeignKey("Deck", related_name="d", on_delete=models.CASCADE)


class UserCard(models.Model):
    """связь Юзеров и карт, которые есть у них"""
    card = models.ForeignKey(Card, related_name="u_c",
                             on_delete=models.CASCADE,
                             blank=False, null=False)
    user = models.ForeignKey(CustomUser, related_name="u_c",
                             on_delete=models.CASCADE,
                             blank=False, null=False)
    count = models.IntegerField(default=1, blank=False, null=False)

    class Meta:
        unique_together = ("card", "user")


class UserLeader(models.Model):
    """связь Юзеров и лидеров, которые есть у них"""
    leader = models.ForeignKey(Leader, related_name="u_l",
                               on_delete=models.CASCADE,
                               blank=False, null=False)
    user = models.ForeignKey(CustomUser, related_name="u_l",
                             on_delete=models.CASCADE,
                             blank=False, null=False)
    count = models.IntegerField(default=1, blank=False, null=False)

    class Meta:
        unique_together = ("leader", "user")


class UserDeck(models.Model):
    """связь Юзеров и КОЛОД, которые есть у них"""
    deck = models.ForeignKey(Deck, related_name="u_d",
                             on_delete=models.CASCADE,
                             blank=False, null=False)
    user = models.ForeignKey(CustomUser, related_name="u_d",
                             on_delete=models.CASCADE,
                             blank=False, null=False)

    class Meta:
        unique_together = ("deck", "user")
