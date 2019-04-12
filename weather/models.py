from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=50, help_text="这个天气所在的国家")
    country = models.CharField(null=True, blank=True, max_length=50, help_text="这个天气所在的国家")
    query_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="查询时间",
                                       help_text="查询时间")
    latitude = models.FloatField(default=0.0, help_text='纬度', verbose_name='纬度')
    longitude = models.FloatField(default=0.0, help_text="经度", verbose_name="经度")

    weather = models.CharField(null=True, blank=True, max_length=100, help_text="天气，比如多云")
    weather_description = models.CharField(null=True, blank=True, max_length=1000, help_text="天气的描述")
    temperature = models.IntegerField(default=0, help_text="温度，摄氏度")
    max_temperature = models.IntegerField(default=0, help_text="最高温度，摄氏度")
    min_temperature = models.IntegerField(default=0, help_text="最低温度，摄氏度")
    wind_speed = models.FloatField(default=0.0, help_text="风速")
    icon = models.CharField(null=True, blank=True, max_length=100, help_text="天气的图标id")

    def __str__(self):
        if self.country != None:
            return self.name + " " + self.country
        else:
            return self.name

    def to_dict(self):
        return {
            'city': self.name,
            'country': self.country,
            'temperature': self.temperature,
            'description': self.weather_description,
            'icon': self.icon,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'max_temperature': self.max_temperature,
            'min_temperature': self.min_temperature,
            'wind_speed': self.wind_speed,
            'weather': self.weather

        }

    class Meta:
        # 设置name和country联合唯一，类似多字段主键
        # 两个元素联合去重的，防止一个国家中存在重复的城市
        # 注意使用这种方法不要设置主键，让django自己生成一个id作为主键即可
        unique_together = ('name', 'country',)
        verbose_name_plural = 'cities'
