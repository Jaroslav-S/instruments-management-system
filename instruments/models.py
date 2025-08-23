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
    id = models.AutoField(primary_key=True)
    inv_num = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='inventární číslo',
        help_text='filharmonické inventární číslo, pokud existuje'
    )
    group = models.CharField(
        max_length=10,
        choices=GROUP_CHOICES,
        verbose_name='Skupina',
        help_text='Hlavní skupina nástrojů (např. smyčce, dřeva, žestě...)'
    )
    subgroup = models.CharField(
        max_length=20,
        choices=SUBGROUP_CHOICES,
        verbose_name='Podskupina',
        help_text='Podskupina nástrojů podle zvolené skupiny'
    )
    subsubgroup = models.CharField(
        max_length=13,
        choices=SUBSUBGROUP_CHOICES,
        verbose_name='Dílčí podskupina',
        help_text='Dílčí podskupina (např. smyčec – pouze pro smyčce; nástroj/příslušenství/obal – pro všechny skupiny)'
    )
    item = models.CharField(
        max_length=24,
        verbose_name='Nástroj',
        help_text='Co je to za nástroj?'
    )
    description = models.CharField(
        max_length=24,
        verbose_name='Výrobce, název, typ',
        help_text='Výrobce, název, typ'
    )
    serial_number = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name='Sériové číslo',
        help_text='Sériové číslo nástroje nebo příslušenství'
    )

    # -----------------------------
    # Validation (consistent with Purchases & Servicing)
    # -----------------------------
    def clean(self):
        errors = {}

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
            errors['subgroup'] = f"Podskupina '{self.subgroup}' není platná pro skupinu '{self.group}'."

        # Validate subsubgroup vs group
        if self.subsubgroup == 'smyčec' and self.group != 'smyčce':
            errors['subsubgroup'] = "Volba 'smyčec' je povolena pouze pro skupinu 'smyčce'."

        # Field length validations (matching Purchases & Servicing style)
        if self.inv_num and len(self.inv_num) > 10:
            errors['inv_num'] = "Inventární číslo může mít maximálně 10 znaků."
        if self.item and len(self.item) > 24:
            errors['item'] = "Nástroj může mít maximálně 24 znaků."
        if self.description and len(self.description) > 24:
            errors['description'] = "Popis může mít maximálně 24 znaků."
        if self.serial_number and len(self.serial_number) > 12:
            errors['serial_number'] = "Sériové číslo může mít maximálně 12 znaků."

        if errors:
            raise ValidationError(errors)

    # -----------------------------
    # String representation (consistent style)
    # -----------------------------
    def __str__(self):
        parts = [f"{self.inv_num or 'Unknown'} – {self.item}"]
        if self.serial_number:
            parts[-1] += f" [{self.serial_number}]"
        parts.append(f"({self.group} / {self.subgroup})")
        return " | ".join(parts)

class Purchases(models.Model):
    # Primary key, auto increment for each purchase record
    id_purchase = models.AutoField(primary_key=True)

    # Foreign key linking to Inventory (table 1)
    inventory_item = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="purchases"
    )

    # Purchase date (user input, cannot be empty)
    purchase_date = models.DateField(
        verbose_name='Datum nákupu',
        help_text='Datum pořízení nástroje, povinné'
    )

    # Supplier name (max 24 chars, required)
    supplier = models.CharField(
        max_length=24,
        verbose_name='Dodavatel',
        help_text='Dodavatel nástroje, povinné'
    )

    # price - amount, user input, required
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Cena',
        help_text='Částka podle faktury, povinné'
    )

    # price - currency, user input, required
    currency = models.CharField(
        max_length=3,
        verbose_name='Měna',
        help_text='Měna podle faktury, povinné'
    )

    # Invoice number (max 12 chars, can include non-numeric chars, required)
    invoice = models.CharField(
        max_length=12,
        verbose_name='Faktura',
        help_text='Číslo faktury, povinné'
    )

    # Notes (max 24 chars, optional)
    notes = models.CharField(
        max_length=24,
        blank=True,
        verbose_name='Poznámka',
        help_text='Volitelná poznámka k nákupu'
    )

    def __str__(self):
        # String representation showing supplier, date, invoice, amount and currency
        parts = [f"Purchase {self.id_purchase} – {self.supplier} ({self.purchase_date})"]
        parts.append(f"{self.amount} {self.currency}")
        parts.append(f"Invoice: {self.invoice}")
        if self.notes:
            parts.append(f"Note: {self.notes}")
        return " | ".join(parts)

    def clean(self):
        errors = {}

        # fields length validation
        if self.supplier and len(self.supplier) > 24:
            errors['supplier'] = "Dodavatel může mít maximálně 24 znaků."
        if self.amount is not None and self.amount < 0:
            errors['amount'] = "Částka nesmí být záporná."
        if self.currency and len(self.currency) > 3:
            errors['currency'] = "Měna může mít maximálně 3 znaky."
        if self.invoice and len(self.invoice) > 12:
            errors['invoice'] = "Číslo faktury může mít maximálně 12 znaků."
        if self.notes and len(self.notes) > 24:
            errors['notes'] = "Poznámka může mít maximálně 24 znaků."

        if errors:
            raise ValidationError(errors)


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
    service_date = models.DateField(
        verbose_name='Datum',
        help_text='Datum servisu, povinné'
    )

    # Supplier name (max 24 chars, required)
    supplier = models.CharField(
        max_length=24,
        verbose_name='Dodavatel',
        help_text='Dodavatel servisu, povinné'
    )

    # price - amount, user input, can be empty when unknown
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Cena',
        help_text='Částka podle faktury, pokud je neznámá, nech prázdné'
    )

    # price - currency, user input, can be empty when unknown
    currency = models.CharField(
        max_length=3,
        blank=True,
        verbose_name='Měna',
        help_text='Měna podle faktury, pokud je neznámá, nech prázdné'
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
        # String representation showing supplier, date, invoice, amount and currency
        parts = [f"Servicing {self.id_servicing} – {self.supplier} ({self.service_date})"]
        if self.amount:
            parts.append(f"{self.amount} {self.currency or ''}".strip())
        if self.invoice:
            parts.append(f"Invoice: {self.invoice}")
        return " | ".join(parts)

    def clean(self):
        errors = {}

        # fields length validation
        if self.supplier and len(self.supplier) > 24:
            errors['supplier'] = "Dodavatel může mít maximálně 24 znaků."
        if self.amount is not None and self.amount < 0:
            errors['amount'] = "Částka nesmí být záporná."
        if self.currency and len(self.currency) > 3:
            errors['currency'] = "Měna může mít maximálně 3 znaky."
        if self.invoice and len(self.invoice) > 12:
            errors['invoice'] = "Číslo faktury může mít maximálně 12 znaků."
        if self.notes and len(self.notes) > 24:
            errors['notes'] = "Poznámka může mít maximálně 24 znaků."

        if errors:
            raise ValidationError(errors)

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