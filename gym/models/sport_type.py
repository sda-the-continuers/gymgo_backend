from utility.models import EnumBaseModel, BaseModel


class SportType(EnumBaseModel, BaseModel):

    class Meta:
        verbose_name = 'نوع ورزش'
        verbose_name_plural = 'انواع ورزش'
