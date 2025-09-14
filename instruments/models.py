from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# -----------------------------
# Inventory
# -----------------------------
class Inventory(models.Model):
    GROUP_CHOICES = [
        ('smyčce', 'Smyčce'),
        ('dřeva', 'Dřeva'),
        ('žestě', 'Žestě'),
        ('bicí', 'Bicí'),
        ('harfy', 'Harfy'),
        ('klavíry', 'Klavíry'),
        ('elektronika', 'Elektronika'),
    ]

    SUBGROUP_CHOICES = [
        ('housle', 'Housle'), ('violy', 'Violy'), ('violoncella', 'Violoncella'), ('kontrabasy', 'Kontrabasy'), ('smyčce ostatní', 'Ostatní (smyčce)'),
        ('flétny', 'Flétny'), ('hoboje', 'Hoboje'), ('klarinety', 'Klarinety'), ('fagoty', 'Fagoty'), ('dřeva ostatní', 'Ostatní (dřeva)'),
        ('lesní rohy', 'Lesní rohy'), ('trumpety', 'Trumpety'), ('trombony', 'Trombony'), ('tuby', 'Tuby'), ('žestě ostatní', 'Ostatní (žestě)'),
        ('bicí', 'Bicí'), ('bicí ostatní', 'Ostatní (bicí)'),
        ('harfy', 'Harfy'), ('harfy ostatní', 'Ostatní (harfy)'),
        ('klavíry', 'Klavíry'), ('klavíry ostatní', 'Ostatní (klavíry)'),
        ('klávesy', 'Klávesy'), ('elektronika ostatní', 'Ostatní (elektronika)'),
    ]

    SUBSUBGROUP_CHOICES = [
        ('smyčec', 'Smyčec'),
        ('nástroj', 'Nástroj'),
        ('příslušenství', 'Příslušenství'),
        ('obal', 'Obal'),
    ]

    id = models.AutoField(primary_key=True)
    inv_num = models.CharField(max_length=10, blank=True, null=True, verbose_name='inventární číslo', help_text='filharmonické inventární číslo, pokud existuje')
    group = models.CharField(max_length=14, choices=GROUP_CHOICES, verbose_name='Skupina', help_text='Hlavní skupina nástrojů')
    subgroup = models.CharField(max_length=20, choices=SUBGROUP_CHOICES, verbose_name='Podskupina', help_text='Podskupina nástrojů')
    subsubgroup = models.CharField(max_length=14, choices=SUBSUBGROUP_CHOICES, verbose_name='Dílčí podskupina', help_text='Dílčí podskupina')
    item = models.CharField(max_length=24, verbose_name='Nástroj', help_text='Co je to za nástroj?')
    description = models.CharField(max_length=24, verbose_name='Výrobce, název, typ', help_text='Výrobce, název, typ')
    serial_number = models.CharField(max_length=12, blank=True, null=True, verbose_name='Sériové číslo', help_text='Sériové číslo nástroje nebo příslušenství')
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.SET_NULL, null=True, blank=True, related_name="instruments", verbose_name="Výrobce")
    accessories = models.ManyToManyField("Accessory", blank=True, related_name="instruments", verbose_name="Příslušenství")

    def clean(self):
        errors = {}
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
        if self.subsubgroup == 'smyčec' and self.group != 'smyčce':
            errors['subsubgroup'] = "Volba 'smyčec' je povolena pouze pro skupinu 'smyčce'."
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

    def __str__(self):
        parts = [f"{self.inv_num or 'Unknown'} – {self.item}"]
        if self.serial_number:
            parts[-1] += f" [{self.serial_number}]"
        parts.append(f"({self.group} / {self.subgroup})")
        return " | ".join(parts)

    class Meta:
        verbose_name = "Inventář"
        verbose_name_plural = "Inventáře"


# -----------------------------
# Rentals (starý)
# -----------------------------
class Rentals(models.Model):
    inventory_item = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="old_rentals"
    )
    renter_name = models.CharField(max_length=255)
    rental_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    rental_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.renter_name} - {self.inventory_item}"


# -----------------------------
# Rental (nový, pro form)
# -----------------------------
class Rental(models.Model):
    instrument = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="new_rentals"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rentals")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.instrument} rented by {self.user} from {self.start_date} to {self.end_date or 'ongoing'}"


# -----------------------------
# Purchases, Servicing, Disposals
# -----------------------------
class Purchases(models.Model):
    id_purchase = models.AutoField(primary_key=True)
    inventory_item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="purchases")
    purchase_date = models.DateField(verbose_name='Datum nákupu', help_text='Datum pořízení nástroje, povinné')
    supplier = models.CharField(max_length=24, verbose_name='Dodavatel', help_text='Dodavatel nástroje, povinné')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Cena', help_text='Částka podle faktury, povinné')
    currency = models.CharField(max_length=3, verbose_name='Měna', help_text='Měna podle faktury, povinné')
    invoice = models.CharField(max_length=12, verbose_name='Faktura', help_text='Číslo faktury, povinné')
    notes = models.CharField(max_length=24, blank=True, verbose_name='Poznámka', help_text='Volitelná poznámka k nákupu')

    def __str__(self):
        parts = [f"Purchase {self.id_purchase} – {self.supplier} ({self.purchase_date})"]
        parts.append(f"{self.amount} {self.currency}")
        parts.append(f"Invoice: {self.invoice}")
        if self.notes:
            parts.append(f"Note: {self.notes}")
        return " | ".join(parts)

    def clean(self):
        errors = {}
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

    class Meta:
        verbose_name = "Nákup"
        verbose_name_plural = "Nákupy"


# Servicing
class Servicing(models.Model):
    id_servicing = models.AutoField(primary_key=True)
    inventory_item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="servicings")
    service_date = models.DateField(verbose_name='Datum', help_text='Datum servisu, povinné')
    supplier = models.CharField(max_length=24, verbose_name='Dodavatel', help_text='Dodavatel servisu, povinné')
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Cena', help_text='Částka podle faktury, pokud je neznámá, nech prázdné')
    currency = models.CharField(max_length=3, blank=True, verbose_name='Měna', help_text='Měna podle faktury, pokud je neznámá, nech prázdné')
    invoice = models.CharField(max_length=12, blank=True, verbose_name='Faktura', help_text='Číslo faktury, může být prázdné')
    notes = models.CharField(max_length=24, blank=True, verbose_name='Poznámka', help_text='Volitelná poznámka k servisu')

    def __str__(self):
        parts = [f"Servicing {self.id_servicing} – {self.supplier} ({self.service_date})"]
        if self.amount:
            parts.append(f"{self.amount} {self.currency or ''}".strip())
        if self.invoice:
            parts.append(f"Invoice: {self.invoice}")
        return " | ".join(parts)

    def clean(self):
        errors = {}
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

    class Meta:
        verbose_name = "Servis"
        verbose_name_plural = "Servisy"


# Disposals
class Disposals(models.Model):
    DISPOSAL_REASON_CHOICES = [
        ('vyřazení', 'Vyřazení'), ('poškození', 'Poškození'), ('ztráta', 'Ztráta'),
        ('odcizení', 'Odcizení'), ('prodej', 'Prodej'), ('jiné', 'Jiné'),
    ]

    id_disposals = models.AutoField(primary_key=True)
    inventory_item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="disposals")
    disposal_date = models.DateField(verbose_name='Datum likvidace', help_text='Datum, kdy byla položka zlikvidována')
    disposal_reason = models.CharField(max_length=10, choices=DISPOSAL_REASON_CHOICES, verbose_name='Důvod likvidace', help_text='Vyberte důvod, proč byla položka zlikvidována')
    notes = models.CharField(max_length=24, blank=True, verbose_name='Poznámka', help_text='Volitelná poznámka k likvidaci')

    def __str__(self):
        return f"Disposal {self.id_disposals} – {self.inventory_item} ({self.disposal_date}) – {self.disposal_reason}"

    def clean(self):
        errors = {}
        if self.notes and len(self.notes) > 24:
            errors['notes'] = "Poznámka může mít maximálně 24 znaků."
        if self.disposal_reason not in dict(self.DISPOSAL_REASON_CHOICES):
            errors['disposal_reason'] = "Neplatný důvod likvidace."
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = "Likvidace"
        verbose_name_plural = "Likvidace"


# Manufacturer
class Manufacturer(models.Model):
    id_manufacturer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Výrobce")
    country = models.CharField(max_length=50, blank=True, verbose_name="Země")

    def __str__(self):
        return f"{self.name} ({self.country})"

    class Meta:
        verbose_name = "Výrobce"
        verbose_name_plural = "Výrobci"


# Accessory
class Accessory(models.Model):
    id_accessory = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Příslušenství")
    description = models.CharField(max_length=100, blank=True, verbose_name="Popis")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Příslušenství"
        verbose_name_plural = "Příslušenství"