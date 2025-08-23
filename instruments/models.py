from django.db import models
from django.core.exceptions import ValidationError

class Inventory(models.Model):
    # -----------------------------
    # Main group of instruments
    # -----------------------------
    GROUP_CHOICES = [
        ('smyčce', 'Smyčce'),
        ('dřeva', 'Dřeva'),
        ('žestě', 'Žestě'),
        ('bicí', 'Bicí'),
        ('harfy', 'Harfy'),
        ('klavíry', 'Klavíry'),
        ('elektronika', 'Elektronika'),
    ]

    # -----------------------------
    # Subgroup (depends on group)
    # -----------------------------
    SUBGROUP_CHOICES = [
        # Strings
        ('housle', 'Housle'),
        ('violy', 'Violy'),
        ('violoncella', 'Violoncella'),
        ('kontrabasy', 'Kontrabasy'),
        ('smyčce ostatní', 'Ostatní (smyčce)'),

        # Woodwinds
        ('flétny', 'Flétny'),
        ('hoboje', 'Hoboje'),
        ('klarinety', 'Klarinety'),
        ('fagoty', 'Fagoty'),
        ('dřeva ostatní', 'Ostatní (dřeva)'),

        # Brass
        ('lesní rohy', 'Lesní rohy'),
        ('trumpety', 'Trumpety'),
        ('trombony', 'Trombony'),
        ('tuby', 'Tuby'),
        ('žestě ostatní', 'Ostatní (žestě)'),

        # Percussion
        ('bicí', 'Bicí'),
        ('bicí ostatní', 'Ostatní (bicí)'),

        # Harps
        ('harfy', 'Harfy'),
        ('harfy ostatní', 'Ostatní (harfy)'),

        # Pianos
        ('klavíry', 'Klavíry'),
        ('klavíry ostatní', 'Ostatní (klavíry)'),

        # Electronics
        ('klávesy', 'Klávesy'),
        ('elektronika ostatní', 'Ostatní (elektronika)'),
    ]

    # -----------------------------
    # Sub-subgroup
    # -----------------------------
    SUBSUBGROUP_CHOICES = [
        ('smyčec', 'Smyčec'),                # only valid for group = smyčce
        ('nástroj', 'Nástroj'),              # valid for all groups
        ('příslušenství', 'Příslušenství'),  # valid for all groups
        ('obal', 'Obal'),                    # valid for all groups
    ]

    # -----------------------------
    # Fields
    # -----------------------------

    # primary key
    id = models.AutoField(
        primary_key=True
    )

    # internal inventory number text field, can be empty (not null)
    inv_num = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='inventární číslo',
        help_text='filharmonické inventární číslo, pokud existuje'
    )

    # 1st category selection, user has to choose predefined category of instrument, cannot be empty (not null)
    group = models.CharField(
        max_length=10,
        choices=GROUP_CHOICES,
        verbose_name='Skupina',
        help_text='Hlavní skupina nástrojů (např. smyčce, dřeva, žestě...)'
    )

    # 2nd subcategory, user has to choose predefined subcategory of instrument, cannot be empty (not null)
    subgroup = models.CharField(
        max_length=20,
        choices=SUBGROUP_CHOICES,
        verbose_name='Podskupina',
        help_text='Podskupina nástrojů podle zvolené skupiny'
    )

    # 3rd subsubcategory, user has to choose predefined subsubcategory, cannot be empty (not null)
    subsubgroup = models.CharField(
        max_length=13,
        choices=SUBSUBGROUP_CHOICES,
        verbose_name='Dílčí podskupina',
        help_text='Dílčí podskupina (např. smyčec – pouze pro smyčce; nástroj/příslušenství/obal – pro všechny skupiny)'
    )

    # item description, not null
    item = models.CharField(
        max_length=24,
        verbose_name='Nástroj',
        help_text='Co je to za nástroj?'
    )

    # item detail, not null
    description = models.CharField(
        max_length=24,
        verbose_name='Výrobce, název, typ',
        help_text='Výrobce, název, typ'
    )

    # item serial or production number, can be null
    serial_number = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name='Sériové číslo',
        help_text='Sériové číslo nástroje nebo příslušenství'
    )

    # -----------------------------
    # Validation
    # -----------------------------
    def clean(self):
        # Validate subgroup vs group
        valid_subgroups = {
            'smyčce': ['housle', 'violy', 'violoncella', 'kontrabasy', 'smyčce ostatní'],
            'dřeva': ['flétny', 'hoboje', 'klarinety', 'fagoty', 'dřeva ostatní'],
            'žestě': ['lesní rohy', 'trumpety', 'trombony', 'tuby', 'žestě ostatní'],
            'bicí': ['bicí', 'bicí ostatní'],
            'harfy': ['harfy', 'harfy ostatní'],
            'klavíry': ['klavíry', 'klavíry ostatní'],
            'elektronika': ['klávesy', 'elektronika ostatní'],
        }

        if self.subgroup not in valid_subgroups.get(self.group, []):
            raise ValidationError({'subgroup': f"Podskupina '{self.subgroup}' není platná pro skupinu '{self.group}'."})

        # Validate subsubgroup vs group
        if self.subsubgroup == 'smyčec' and self.group != 'smyčce':
            raise ValidationError({'subsubgroup': "Volba 'smyčec' je povolena pouze pro skupinu 'smyčce'."})

    def __str__(self):
        inv = self.inv_num or "Unknown"
        serial = f" [{self.serial_number}]" if self.serial_number else ""
        return f"{inv} – {self.item}{serial} ({self.group} / {self.subgroup})"

class Purchases(models.Model):

    # Primary key for Purchases
    id_purchases = models.AutoField(primary_key=True)

    # Foreign key to link Purchases to Inventory
    inventory_item = models.ForeignKey(
        'Inventory',
        on_delete=models.CASCADE,
        related_name="purchases"
    )

    # purchase date, user input, can be empty when unknown
    purchase_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Datum nákupu',
        help_text='Datum nákupu podle faktury, pokud je neznámé, nech prázdné'
    )

    # supplier name, user input, can be empty when unknown
    supplier = models.CharField(
        max_length=14,
        blank=True,
        verbose_name='Dodavatel',
        help_text='Dodavatel podle faktury, pokud je neznámý, nech prázdné'
    )

    # price, user input, can be empty when unknown
    price = models.CharField(
        max_length=12,
        blank=True,
        verbose_name='Cena',
        help_text='Cena podle faktury, pokud je neznámá, nech prázdné'
    )

    # invoice number, user input, can be empty when unknown
    invoice = models.CharField(
        max_length=12,
        blank=True,
        verbose_name='Číslo faktury',
        help_text='Číslo faktury, pokud je neznámé, nech prázdné'
    )

    # space for user note, optional user input
    notes = models.CharField(
        max_length=24,
        blank=True,
        verbose_name='Poznámka',
        help_text='Prostor pro poznámku, maximálně 24 znaků'
    )

    def clean(self):
        errors = {}

        # fields length validation
        if self.supplier and len(self.supplier) > 14:
            errors['supplier'] = "Dodavatel může mít maximálně 14 znaků."
        if self.price and len(self.price) > 12:
            errors['price'] = "Cena může mít maximálně 12 znaků."
        if self.invoice and len(self.invoice) > 12:
            errors['invoice'] = "Číslo faktury může mít maximálně 12 znaků."
        if self.notes and len(self.notes) > 24:
            errors['notes'] = "Poznámka může mít maximálně 24 znaků."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"Purchase {self.id_purchases} – {self.supplier or 'Unknown'} ({self.purchase_date or 'Unknown'})"

class Servicing(models.Model):
    # Primary key, auto increment for each service record
    id_servicing = models.AutoField(primary_key=True)

    # Foreign key linking to Inventory (table 1)
    inventory_item = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="servicings"
    )

    # Service date (user input, cannot be empty)
    service_date = models.DateField()

    # Supplier name (max 24 chars, required)
    supplier = models.CharField(
        max_length=24,
        verbose_name='Dodavatel',
        help_text='Dodavatel servisu, povinné'
    )

    # Price with currency (max 12 chars, required)
    price = models.CharField(
        max_length=12,
        verbose_name='Cena',
        help_text='Cena servisu, povinné'
    )

    # Invoice number (max 12 chars, can include non-numeric chars, optional)
    invoice = models.CharField(
        max_length=12,
        blank=True,
        verbose_name='Faktura',
        help_text='Číslo faktury, může být prázdné'
    )

    # Notes (max 24 chars, optional)
    notes = models.CharField(
        max_length=24,
        blank=True,
        verbose_name='Poznámka',
        help_text='Volitelná poznámka k servisu'
    )

    def __str__(self):
        # String representation showing supplier, date, and invoice
        return f"Servicing {self.id_servicing} – {self.supplier} ({self.service_date})"

class Rentals(models.Model):
    # Primary key, auto increment for each rental record
    id_rentals = models.AutoField(primary_key=True)

    # Foreign key linking to Inventory (table 1)
    inventory_item = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="rentals"
    )

    # Rental date (user input, cannot be empty)
    rental_date = models.DateField()

    # Renter name (max 24 chars, required)
    renter_name = models.CharField(
        max_length=24,
        verbose_name='Jméno',
        help_text='Jméno osoby, povinné'
    )

    # Logical value – rented yes/no
    is_rented = models.BooleanField(
        default=False,
        verbose_name='Zapůjčeno',
        help_text='Zda je položka aktuálně zapůjčena'
    )

    # Notes (max 24 chars, optional)
    notes = models.CharField(
        max_length=24,
        blank=True,
        verbose_name='Poznámka',
        help_text='Volitelná poznámka'
    )

    def __str__(self):
        # String representation showing renter name and date
        status = 'Yes' if self.is_rented else 'No'
        return f"Rental {self.id_rentals} – {self.renter_name} ({self.rental_date}) – Rented: {status}"

# Disposals model
class Disposals(models.Model):
    # ForeignKey to Inventory
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name='disposals',
        verbose_name='Inventář'
    )

    # Unique ID for each disposal
    id_disposal = models.AutoField(
        primary_key=True,
        verbose_name='ID vyřazení'
    )

    # Disposal date
    date = models.DateField(
        verbose_name='Datum vyřazení',
        help_text='Datum vyřazení položky z inventáře'
    )

    # Optional note
    note = models.CharField(
        max_length=24,
        blank=True,
        null=True,
        verbose_name='Poznámka',
        help_text='Poznámka k vyřazení (max. 24 znaků)'
    )

    def __str__(self):
        return f"Disposal {self.id_disposal} for {self.inventory.item}"