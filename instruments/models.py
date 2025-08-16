from django.db import models

class Inventory(models.Model):
    # Primary key, auto-incremented
    # Django automatically creates an "id" field as the primary key

    inv_num = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Inventární číslo',  # shown to user
        help_text='Inventární číslo, může být prázdné'
    )

    group_choices = [
        ('dřeva', 'Dřeva'),
        ('žestě', 'Žestě'),
        ('smyčce', 'Smyčce'),
        ('bicí', 'Bicí'),
        ('klávesy', 'Klávesy'),
        ('elektronika', 'Elektronika'),
        ('ostatní', 'Ostatní'),
    ]
    group = models.CharField(
        max_length=10,
        choices=group_choices,
        verbose_name='Skupina',
        help_text='Vyberte skupinu nástroje, nesmí být prázdné'
    )

    subgroup_choices = [
        # Woodwinds
        ('flétny', 'Flétny'),
        ('hoboje', 'Hoboje'),
        ('klarinety', 'Klarinety'),
        ('fagoty', 'Fagoty'),
        ('jiné', 'Jiné'),
        # Brass
        ('lesní rohy', 'Lesní rohy'),
        ('trumpety', 'Trumpety'),
        ('trombony', 'Trombony'),
        ('tuby', 'Tuby'),
        # Strings
        ('housle', 'Housle'),
        ('violy', 'Violy'),
        ('violoncella', 'Violoncella'),
        ('kontrabasy', 'Kontrabasy'),
        # Percussion
        ('bicí', 'Bicí'),
        # Keyboards
        ('klávesy', 'Klávesy'),
        # Electronics
        ('elektronika', 'Elektronika'),
        ('other', 'Jiné'),
    ]
    subgroup = models.CharField(
        max_length=14,
        choices=subgroup_choices,
        verbose_name='Podskupina',
        help_text='Vyberte podskupinu podle skupiny, nesmí být prázdné'
    )

    subsubgroup_choices = [
        ('nastroj', 'Nástroj'),
        ('prislusenstvi', 'Příslušenství'),
        ('obal', 'Obal'),
        ('smycec', 'Smyčec'),
    ]
    subsubgroup = models.CharField(
        max_length=14,
        choices=subsubgroup_choices,
        verbose_name='Pod-podskupina',
        help_text='Vyberte typ položky, nesmí být prázdné'
    )

    item = models.CharField(
        max_length=24,
        verbose_name='Položka',
        help_text='Název konkrétní věci, povinné'
    )

    description = models.CharField(
        max_length=24,
        verbose_name='Popis',
        help_text='Popis konkrétní věci, povinné'
    )

    serial = models.CharField(
        max_length=12,
        blank=True,
        verbose_name='Sériové číslo',
        help_text='Sériové nebo výrobní číslo, může být prázdné'
    )

    def __str__(self):
        # This defines how the object is displayed in Django admin
        return f"{self.item} ({self.inv_num})"

class Purchasing(models.Model):
    # Primary key, auto increment for each purchase record
    id_purchases = models.AutoField(primary_key=True)

    # Foreign key linking to Inventory (table 1)
    inventory_item = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="purchases"
    )

    # Purchase date (user input, can be empty = unknown)
    purchase_date = models.DateField(blank=True, null=True)  # DateField can stay with null=True

    # Supplier name (max 14 chars, user input, can be empty = unknown)
    supplier = models.CharField(max_length=14, blank=True)

    # Price with currency (max 12 chars, user input, can be empty = unknown)
    price = models.CharField(max_length=12, blank=True)

    # Invoice number (max 12 chars, can include non-numeric chars, user input, can be empty = unknown)
    invoice = models.CharField(max_length=12, blank=True)

    # Notes (max 24 chars, optional, can be empty)
    notes = models.CharField(max_length=24, blank=True)

    def __str__(self):
        # String representation showing supplier and date
        return f"Purchase {self.id_purchases} – {self.supplier or 'Unknown'} ({self.purchase_date or 'Unknown'})"