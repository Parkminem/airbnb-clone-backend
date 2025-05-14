import os
import django
import random
from django.utils import timezone
from faker import Faker

# Django 설정 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from users.models import User
from rooms.models import Room, Amenity
from experiences.models import Experience, Perk
from reviews.models import Review

# Faker 인스턴스
faker = Faker("ko_KR")

# 데이터 초기화
print("🧹 기존 데이터 삭제 중...")
Review.objects.all().delete()
Room.objects.all().delete()
Amenity.objects.all().delete()
Experience.objects.all().delete()
Perk.objects.all().delete()
User.objects.exclude(is_superuser=True).delete()

# 사용자 생성
print("👤 사용자 생성...")
user, _ = User.objects.get_or_create(username="tester", email="tester@example.com")
user.set_password("1234")
user.save()

# 어메니티 생성
print("🛏 어메니티 생성...")
amenities = []
for name in ["Wi-Fi", "TV", "에어컨", "수건", "샴푸"]:
    amenity = Amenity.objects.create(name=name, description=faker.sentence())
    amenities.append(amenity)

# 룸 생성
print("🏠 룸 생성...")
rooms = []
for i in range(5):
    room = Room.objects.create(
        name=faker.word() + " 하우스",
        owner=user,
        country="한국",
        city="서울",
        price=random.randint(30000, 100000),
        rooms=random.randint(1, 3),
        toilets=random.randint(1, 2),
        address=faker.address(),
        description=faker.text(),
    )
    room.amenities.set(random.sample(amenities, k=3))
    rooms.append(room)

# 퍼크 생성
print("🎁 퍼크 생성...")
perks = []
for name in ["음료", "가이드", "기념품", "사진촬영", "픽업"]:
    perk = Perk.objects.create(
        name=name,
        details=faker.sentence(),
        explanation=faker.text(),
    )
    perks.append(perk)

# 체험 생성
print("🚴 체험 생성...")
experiences = []
for i in range(5):
    experience = Experience.objects.create(
        name=faker.catch_phrase(),
        host=user,
        country="한국",
        city="서울",
        price=random.randint(10000, 50000),
        address=faker.address(),
        start=timezone.now(),
        end=timezone.now(),
        description=faker.text(),
    )
    experience.perks.set(random.sample(perks, k=2))
    experiences.append(experience)

# 리뷰 생성
print("⭐️ 리뷰 생성...")
for i in range(5):
    Review.objects.create(
        user=user,
        room=random.choice(rooms),
        rating=random.randint(3, 5),
        payload=faker.sentence(),
    )

for i in range(5):
    Review.objects.create(
        user=user,
        experience=random.choice(experiences),
        rating=random.randint(3, 5),
        payload=faker.sentence(),
    )

print("✅ 모든 seed 데이터가 생성되었습니다!")
