# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Estaciones(models.Model):
    id_regla = models.ForeignKey('ReglasMedicion', models.DO_NOTHING, db_column='id_regla')
    nombre = models.CharField(max_length=100, blank=True, null=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=17)
    dir_mac = models.CharField(unique=True, max_length=16)
    id_tarifa = models.ForeignKey('Tarifas', models.DO_NOTHING, db_column='id_tarifa', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estaciones'


class InicioUserprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    user_type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'inicio_userprofile'


class Mediciones(models.Model):
    valor = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fecha = models.DateTimeField()
    id_estacion = models.ForeignKey(Estaciones, models.DO_NOTHING, db_column='id_estacion', blank=True, null=True)
    id_tipo_medicion = models.ForeignKey('TiposMedicion', models.DO_NOTHING, db_column='id_tipo_medicion', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mediciones'


class ParametrosMedicion(models.Model):
    id_regla = models.ForeignKey('ReglasMedicion', models.DO_NOTHING, db_column='id_regla')
    id_tipo_medicion = models.ForeignKey('TiposMedicion', models.DO_NOTHING, db_column='id_tipo_medicion')
    valor_min = models.DecimalField(max_digits=5, decimal_places=2)
    valor_ide = models.DecimalField(max_digits=5, decimal_places=2)
    valor_max = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'parametros_medicion'
        unique_together = (('id_regla', 'id_tipo_medicion'),)


class ReglasMedicion(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reglas_medicion'


class Reportes(models.Model):
    id_medicion = models.ForeignKey(Mediciones, models.DO_NOTHING, db_column='id_medicion')

    class Meta:
        managed = False
        db_table = 'reportes'


class SesionesCarga(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(blank=True, null=True)
    id_estacion = models.ForeignKey(Estaciones, models.DO_NOTHING, db_column='id_estacion')
    tarifa_aplicada = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sesiones_carga'


class Tarifas(models.Model):
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    moneda = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'tarifas'


class TiposMedicion(models.Model):
    descripcion = models.CharField(unique=True, max_length=50)
    tipo_medicion = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'tipos_medicion'
