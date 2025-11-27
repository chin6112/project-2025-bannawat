from django.db import models

class Car(models.Model):
    license_plate = models.CharField(max_length=20, verbose_name="ทะเบียนรถ")
    name = models.CharField(max_length=50, blank=True, verbose_name="ชื่อรถ")
    color = models.CharField(max_length=30, blank=True, verbose_name="สีรถ")
    active = models.BooleanField(default=True, verbose_name="ใช้งาน")

    def __str__(self):
        return f"{self.license_plate} ({self.color})" if self.color else self.license_plate


class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class ShuttleRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอดำเนินการ'),
        ('approved', 'อนุมัติ'),
        ('on_the_way', 'กำลังถึงต้นทาง'),
        ('in_progress', 'กำลังเดินทาง'),
        ('done', 'เสร็จสิ้น'),
        ('cancelled', 'ยกเลิก'),
    ]

    user_name = models.CharField(max_length=100, verbose_name="ชื่อผู้ใช้")
    line_user_id = models.CharField(max_length=100, blank=True, verbose_name="LINE ID")
    pickup_location = models.CharField(max_length=200, verbose_name="จุดรับ")
    dropoff_location = models.CharField(max_length=200, verbose_name="จุดส่ง")
    start_time = models.DateTimeField(verbose_name="เวลาเริ่มต้น")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="สถานะ")

    car = models.ForeignKey(Car, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="รถ")
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="คนขับ")

    queue_number = models.IntegerField(null=True, blank=True, verbose_name="เลขคิว")
    notification_sent = models.BooleanField(default=False, verbose_name="ส่งการแจ้งเตือนแล้ว")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="สร้างเมื่อ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="อัปเดตเมื่อ")

    class Meta:
        ordering = ['start_time']
        verbose_name = "คำขอใช้รถ"
        verbose_name_plural = "คำขอใช้รถทั้งหมด"

    def __str__(self):
        return f"#{self.queue_number} {self.user_name} @ {self.start_time}" if self.queue_number else f"{self.user_name} @ {self.start_time}"
