# Generated by Django 4.2.11 on 2024-11-26 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('recruit_id', models.AutoField(primary_key=True, serialize=False)),
                ('job_url', models.URLField(blank=True, default='회사 홈페이지에 방문하거나 E-mail로 지원 바랍니다.', max_length=500, null=True)),
                ('company_url', models.CharField(blank=True, default='회사 홈페이지에 방문하거나 E-mail로 지원 바랍니다.', max_length=500, null=True)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('job_title', models.CharField(blank=True, max_length=255, null=True)),
                ('job_code', models.CharField(blank=True, default='0', max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('required_education', models.CharField(blank=True, max_length=255, null=True)),
                ('experience_type', models.CharField(blank=True, max_length=50, null=True)),
                ('min_experience', models.IntegerField(blank=True, null=True)),
                ('max_experience', models.IntegerField(blank=True, null=True)),
                ('job_type', models.CharField(blank=True, max_length=50, null=True)),
                ('salary', models.CharField(blank=True, max_length=100, null=True)),
                ('interest', models.CharField(blank=True, max_length=255, null=True)),
                ('posting_date', models.DateField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('support_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default='홈페이지에 방문하거나 연락처로 컨택 바랍니다.', max_length=500, null=True)),
                ('description', models.CharField(blank=True, default='상세정보는 홈페이지 참고 및 연락 바랍니다.', max_length=500, null=True)),
                ('content', models.CharField(default=True, max_length=500, null=True)),
                ('scale', models.CharField(blank=True, default='상세인원은 홈페이지 참고 및 연락 바랍니다.', max_length=500, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('start_age', models.IntegerField(blank=True, null=True)),
                ('end_age', models.IntegerField(blank=True, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('contact', models.CharField(blank=True, max_length=50, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.URLField(default='회사 홈페이지에 방문하거나 E-mail로 지원 바랍니다.', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='UserRecruitInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recruit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interested_users', to='recruits.recruit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_recruit_interests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
