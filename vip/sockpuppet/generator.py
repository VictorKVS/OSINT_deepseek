"""
Модуль генерации цифровых копий
Sock puppets с полной биографией
"""

import random
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SockPuppetGenerator:
    """
    Генератор полных цифровых личностей
    """
    
    def __init__(self):
        self.persona_db = []
        self.active_personas = {}
        
        # Базы данных для генерации
        self.names_db = self._load_names_db()
        self.countries_db = self._load_countries_db()
        self.occupations_db = self._load_occupations_db()
    
    def _load_names_db(self) -> Dict:
        """Загрузка базы имён"""
        return {
            'US': {
                'male': ['James', 'John', 'Robert', 'Michael', 'William'],
                'female': ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth'],
                'last': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones']
            },
            'RU': {
                'male': ['Александр', 'Дмитрий', 'Максим', 'Сергей', 'Андрей'],
                'female': ['Елена', 'Ольга', 'Татьяна', 'Ирина', 'Светлана'],
                'last': ['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Смирнов']
            },
            'GB': {
                'male': ['Oliver', 'George', 'Harry', 'Noah', 'Jack'],
                'female': ['Olivia', 'Amelia', 'Isla', 'Ava', 'Emily'],
                'last': ['Smith', 'Jones', 'Taylor', 'Brown', 'Williams']
            }
        }
    
    def _load_countries_db(self) -> Dict:
        """Загрузка базы стран"""
        return {
            'US': {'cities': ['New York', 'Los Angeles', 'Chicago'], 'zip_format': '#####'},
            'RU': {'cities': ['Москва', 'Санкт-Петербург', 'Новосибирск'], 'zip_format': '######'},
            'GB': {'cities': ['London', 'Manchester', 'Birmingham'], 'zip_format': '??# #??'}
        }
    
    def _load_occupations_db(self) -> List:
        """Загрузка базы профессий"""
        return [
            'IT Consultant', 'Marketing Manager', 'Freelance Designer',
            'Small Business Owner', 'Research Assistant', 'Journalist',
            'Software Developer', 'Data Analyst', 'PhD Student',
            'Teacher', 'Architect', 'Photographer', 'Writer'
        ]
    
    def generate_persona(self, profile: Dict = None) -> Dict:
        """
        Генерация полной личности
        """
        profile = profile or {}
        country = profile.get('country', random.choice(list(self.names_db.keys())))
        gender = profile.get('gender', random.choice(['male', 'female']))
        
        # 1. Базовые данные
        name_data = self._generate_name(country, gender)
        
        # 2. Дата рождения (18-65 лет)
        birth_date = self._generate_birth_date()
        
        # 3. Местоположение
        location = self._generate_location(country)
        
        # 4. Биография
        bio = self._generate_bio(name_data, birth_date, location, gender)
        
        # 5. Контактные данные
        contacts = self._generate_contacts(name_data)
        
        # 6. Аккаунты в соцсетях
        social = self._generate_social_accounts(name_data)
        
        persona = {
            'id': self._generate_id(),
            'name': name_data,
            'gender': gender,
            'birth_date': birth_date.isoformat(),
            'age': self._calculate_age(birth_date),
            'location': location,
            'bio': bio,
            'contacts': contacts,
            'social_media': social,
            'interests': self._generate_interests(),
            'digital_footprint': self._generate_digital_footprint(),
            'created': datetime.now().isoformat(),
            'status': 'active',
            'profile': profile
        }
        
        # Сохраняем
        persona_id = persona['id']
        self.active_personas[persona_id] = persona
        self.persona_db.append(persona)
        
        return persona
    
    def _generate_name(self, country: str, gender: str) -> Dict:
        """Генерация имени"""
        names = self.names_db[country]
        
        first = random.choice(names[gender])
        last = random.choice(names['last'])
        
        return {
            'first': first,
            'last': last,
            'full': f"{first} {last}",
            'username': f"{first.lower()}{last.lower()}{random.randint(1, 999)}"
        }
    
    def _generate_birth_date(self) -> datetime:
        """Генерация даты рождения"""
        today = datetime.now()
        min_date = today - timedelta(days=65*365)
        max_date = today - timedelta(days=18*365)
        
        delta = max_date - min_date
        random_days = random.randint(0, delta.days)
        
        return min_date + timedelta(days=random_days)
    
    def _generate_location(self, country: str) -> Dict:
        """Генерация местоположения"""
        country_data = self.countries_db[country]
        
        return {
            'country': country,
            'city': random.choice(country_data['cities']),
            'address': f"{random.randint(1, 999)} {random.choice(['Main St', 'Oak Ave', 'Maple Dr'])}",
            'zip': self._generate_zip(country_data['zip_format'])
        }
    
    def _generate_zip(self, format_str: str) -> str:
        """Генерация почтового индекса"""
        result = []
        for char in format_str:
            if char == '#':
                result.append(str(random.randint(0, 9)))
            elif char == '?':
                result.append(chr(random.randint(65, 90)))
            else:
                result.append(char)
        return ''.join(result)
    
    def _generate_bio(self, name: Dict, birth_date: datetime, location: Dict, gender: str) -> Dict:
        """Генерация биографии"""
        pronoun = 'he' if gender == 'male' else 'she'
        possessive = 'his' if gender == 'male' else 'her'
        
        occupation = random.choice(self.occupations_db)
        
        bio_text = f"{name['full']} is a {occupation} based in {location['city']}. "
        bio_text += f"{pronoun.capitalize()} has {self._calculate_age(birth_date)} years of experience in {possessive} field. "
        
        return {
            'occupation': occupation,
            'summary': bio_text,
            'education': self._generate_education(),
            'languages': random.sample(['English', 'Spanish', 'French', 'German', 'Russian', 'Chinese'], k=random.randint(1, 3))
        }
    
    def _generate_education(self) -> List[Dict]:
        """Генерация образования"""
        degrees = [
            "Bachelor's in Computer Science",
            "Master's in Business Administration",
            "Bachelor's in Marketing",
            "PhD in Data Science",
            "Bachelor's in Communications"
        ]
        
        universities = [
            "Stanford University", "MIT", "Harvard University",
            "University of Cambridge", "University of Oxford",
            "МГУ", "СПбГУ"
        ]
        
        return [{
            'degree': random.choice(degrees),
            'university': random.choice(universities),
            'year': random.randint(2000, 2018)
        }]
    
    def _calculate_age(self, birth_date: datetime) -> int:
        """Вычисление возраста"""
        today = datetime.now()
        return today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
    
    def _generate_contacts(self, name: Dict) -> Dict:
        """Генерация контактов"""
        return {
            'email': f"{name['username']}@protonmail.com",
            'phone': self._generate_phone(),
            'website': f"https://{name['username']}.com"
        }
    
    def _generate_phone(self) -> str:
        """Генерация номера телефона"""
        area = random.randint(200, 999)
        prefix = random.randint(200, 999)
        line = random.randint(1000, 9999)
        return f"+1-{area}-{prefix}-{line}"
    
    def _generate_social_accounts(self, name: Dict) -> Dict:
        """Генерация аккаунтов в соцсетях"""
        return {
            'twitter': f"@{name['username']}",
            'linkedin': f"in/{name['username']}",
            'github': name['username'],
            'facebook': name['full'].replace(' ', '.'),
            'instagram': f"@{name['username']}_life"
        }
    
    def _generate_interests(self) -> List[str]:
        """Генерация интересов"""
        interests_pool = [
            'photography', 'hiking', 'reading', 'cycling', 'gaming',
            'cooking', 'travel', 'music production', '3D printing',
            'yoga', 'painting', 'writing', 'podcasting', 'coffee'
        ]
        return random.sample(interests_pool, k=random.randint(3, 6))
    
    def _generate_digital_footprint(self) -> Dict:
        """Генерация цифрового следа"""
        return {
            'google_searches': random.randint(1000, 50000),
            'forum_posts': random.randint(0, 500),
            'years_active': random.randint(1, 10),
            'data_points': random.randint(50, 500)
        }
    
    def _generate_id(self) -> str:
        """Генерация уникального ID"""
        import uuid
        return str(uuid.uuid4())[:12]
    
    def get_persona(self, persona_id: str) -> Optional[Dict]:
        """Получение личности по ID"""
        return self.active_personas.get(persona_id)
    
    def list_personas(self, limit: int = 10) -> List[Dict]:
        """Список активных личностей"""
        return list(self.active_personas.values())[:limit]
    
    def deactivate_persona(self, persona_id: str) -> bool:
        """Деактивация личности"""
        if persona_id in self.active_personas:
            self.active_personas[persona_id]['status'] = 'inactive'
            return True
        return False


# Тестовый запуск
if __name__ == "__main__":
    generator = SockPuppetGenerator()
    
    # Генерируем несколько личностей
    for country in ['US', 'RU', 'GB']:
        persona = generator.generate_persona({'country': country})
        print(f"\n {persona['name']['full']} ({persona['age']} years)")
        print(f"    {persona['location']['city']}, {persona['location']['country']}")
        print(f"    {persona['bio']['occupation']}")
        print(f"    {persona['contacts']['email']}")
        print(f"    {persona['social_media']['twitter']}")
