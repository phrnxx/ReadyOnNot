import time
import os
import random
from datetime import datetime

class Soldier:
    RANKS = ["Рядовий", "Капрал", "Сержант", "Лейтенант", "Капітан", "Майор"]
    STATUS_TYPES = ["Активний", "Поранений", "Недоступний", "У відпустці", "Зниклий безвісти"]
    
    def __init__(self, name, status, location, rank="Рядовий", health=100, equipment=None):
        self.name = name
        self.status = status if status in self.STATUS_TYPES else "Активний"
        self.location = location  # координати (x, y)
        self.rank = rank
        self.health = health
        self.equipment = equipment or {}
        self.mission = None
        self.messages_received = []
        self.experience = 0
        self.skills = {"бойові": 1, "медичні": 1, "розвідка": 1, "лідерство": 1}
        self.history = []
        self.log_event(f"Солдат створений зі званням {rank}")
    
    def update_status(self, new_status):
        if new_status not in self.STATUS_TYPES:
            return False
            
        old_status = self.status
        self.status = new_status
        self.log_event(f"Статус оновлено з {old_status} на {self.status}")
        return True
    
    def update_location(self, new_location):
        distance = self._calculate_distance(self.location, new_location)
        self.location = new_location
        self.log_event(f"Локацію оновлено на {self.location} (переміщено на {distance:.2f} одиниць)")
        return True
    
    def send_message(self, message):
        msg = f"{self.rank} {self.name} відправляє: {message}"
        self.log_event(f"Надіслано повідомлення: {message}")
        return msg
    
    def receive_message(self, sender, message):
        self.messages_received.append((sender, message, datetime.now()))
        self.log_event(f"Отримано повідомлення від {sender}")
    
    def assign_mission(self, mission):
        self.mission = mission
        self.log_event(f"Призначено на місію: {mission}")
    
    def update_health(self, amount):
        old_health = self.health
        self.health += amount
        
        if self.health > 100:
            self.health = 100
        elif self.health <= 0:
            self.health = 0
            self.status = "Поранений"
            self.log_event("Поранений і потребує медичної допомоги!")
        
        self.log_event(f"Здоров'я змінено з {old_health} на {self.health}")
        return self.health
    
    def add_equipment(self, item, quantity=1):
        if item in self.equipment:
            self.equipment[item] += quantity
        else:
            self.equipment[item] = quantity
        self.log_event(f"Отримано {quantity} {item}")
    
    def use_equipment(self, item, quantity=1):
        if item in self.equipment and self.equipment[item] >= quantity:
            self.equipment[item] -= quantity
            self.log_event(f"Використано {quantity} {item}")
            if self.equipment[item] == 0:
                del self.equipment[item]
            return True
        else:
            self.log_event(f"Недостатньо {item}")
            return False
    
    def report_status(self):
        return {
            "ім'я": self.name,
            "звання": self.rank,
            "статус": self.status,
            "локація": self.location,
            "здоров'я": self.health,
            "спорядження": self.equipment,
            "місія": self.mission,
            "досвід": self.experience,
            "навички": self.skills
        }
    
    def gain_experience(self, amount):
        self.experience += amount
        self.log_event(f"Отримано {amount} очок досвіду")
        
        # Перевірка на підвищення звання
        current_rank_index = self.RANKS.index(self.rank) if self.rank in self.RANKS else 0
        if self.experience >= 100 * (current_rank_index + 1) and current_rank_index < len(self.RANKS) - 1:
            self.rank = self.RANKS[current_rank_index + 1]
            self.log_event(f"Підвищено до звання {self.rank}")
    
    def improve_skill(self, skill_name, amount=1):
        if skill_name in self.skills:
            self.skills[skill_name] += amount
            self.log_event(f"Навичка {skill_name} покращена на {amount}")
            return True
        return False
    
    def log_event(self, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = f"{timestamp}: {self.rank} {self.name} - {description}"
        self.history.append(event)
        return event
    
    def _calculate_distance(self, point1, point2):
        return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5
    
    def __str__(self):
        return f"{self.rank} {self.name} ({self.status}, Здоров'я: {self.health}%)"


class Team:
    def __init__(self, name, commander=None):
        self.name = name
        self.members = []
        self.commander = commander
        self.mission_log = []
        self.created_date = datetime.now()
        self.team_chat = []
        self.equipment_inventory = {}
        self.location = (0, 0)
        self.status = "У резерві"
    
    def add_member(self, soldier):
        self.members.append(soldier)
        self.log_event(f"{soldier.rank} {soldier.name} додано до команди")
        return True
    
    def remove_member(self, soldier):
        if soldier in self.members:
            self.members.remove(soldier)
            self.log_event(f"{soldier.rank} {soldier.name} видалено з команди")
            return True
        return False
    
    def set_commander(self, soldier):
        if soldier in self.members:
            self.commander = soldier
            self.log_event(f"{soldier.rank} {soldier.name} тепер командир")
            return True
        else:
            self.log_event(f"{soldier.rank} {soldier.name} не в команді")
            return False
    
    def team_status(self):
        active_count = sum(1 for member in self.members if member.status == "Активний")
        injured_count = sum(1 for member in self.members if member.status == "Поранений")
        
        status_report = f"\nЗвіт про стан команди {self.name}:\n"
        status_report += f"Всього членів: {len(self.members)}, Активні: {active_count}, Поранені: {injured_count}\n"
        
        if self.commander:
            status_report += f"Командир: {self.commander.rank} {self.commander.name}\n"
        
        status_report += f"Поточна локація: {self.location}\n"
        status_report += f"Поточний статус: {self.status}\n\n"
        
        status_report += "Члени команди:\n"
        for member in self.members:
            status_report += f"{member.rank} {member.name}: {member.status} на {member.location}, Здоров'я: {member.health}%\n"
        
        self.log_event("Згенеровано звіт про стан команди")
        return status_report
    
    def broadcast_message(self, message, sender="Штаб"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        broadcast = f"{timestamp} - {sender}: {message}"
        self.team_chat.append(broadcast)
        
        for member in self.members:
            member.receive_message(sender, message)
        
        self.log_event(f"Повідомлення відправлено від {sender}: {message}")
        return True
    
    def direct_message(self, sender, recipient_name, message):
        for member in self.members:
            if member.name == recipient_name:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dm = f"{timestamp} - {sender} до {recipient_name}: {message}"
                self.team_chat.append(dm)
                
                member.receive_message(sender, message)
                self.log_event(f"Пряме повідомлення від {sender} до {recipient_name}")
                return True
                
        self.log_event(f"Отримувача {recipient_name} не знайдено")
        return False
    
    def assign_team_mission(self, mission_description):
        mission_id = len(self.mission_log) + 1
        mission = f"Місія #{mission_id}: {mission_description}"
        
        for member in self.members:
            if member.status == "Активний":
                member.assign_mission(mission)
        
        self.mission_log.append(mission)
        self.status = "На місії"
        self.log_event(f"Команда призначена на місію {mission}")
        return mission_id
    
    def move_team(self, new_location, formation_spacing=5):
        if not self.members:
            return False
        
        self.log_event(f"Команда переміщується до {new_location}")
        
        # Створення формації навколо цільової локації
        positions = []
        for i, member in enumerate(self.members):
            if member.status == "Активний":
                # Проста формація
                if i == 0:  # Командир або перший солдат у центрі
                    pos = new_location
                elif i % 2 == 1:  # Позиції праворуч
                    offset = ((i + 1) // 2) * formation_spacing
                    pos = (new_location[0] + offset, new_location[1])
                else:  # Позиції ліворуч
                    offset = (i // 2) * formation_spacing
                    pos = (new_location[0] - offset, new_location[1])
                
                positions.append((member, pos))
        
        # Виконання переміщення
        for member, pos in positions:
            member.update_location(pos)
        
        self.location = new_location
        return True
    
    def equipment_report(self):
        report = {}
        for member in self.members:
            for item, quantity in member.equipment.items():
                if item in report:
                    report[item] += quantity
                else:
                    report[item] = quantity
        
        self.equipment_inventory = report
        self.log_event("Згенеровано звіт про спорядження")
        
        report_str = f"\nЗвіт про спорядження команди {self.name}:\n"
        for item, quantity in report.items():
            report_str += f"- {item}: {quantity}\n"
        
        return report_str
    
    def distribute_equipment(self, equipment_dict):
        """Розподілити спорядження рівномірно серед активних членів команди"""
        active_members = [m for m in self.members if m.status == "Активний"]
        if not active_members:
            self.log_event("Немає активних членів для розподілу спорядження")
            return False
            
        for item, quantity in equipment_dict.items():
            per_person = quantity // len(active_members)
            remainder = quantity % len(active_members)
            
            if per_person > 0:
                for member in active_members:
                    member.add_equipment(item, per_person)
                    
            # Розподіл залишку
            for i in range(remainder):
                active_members[i].add_equipment(item, 1)
                
        self.log_event(f"Спорядження розподілено серед {len(active_members)} активних членів")
        return True
    
    def team_skill_report(self):
        """Згенерувати звіт про навички команди"""
        skills = {"бойові": 0, "медичні": 0, "розвідка": 0, "лідерство": 0}
        
        for member in self.members:
            for skill, value in member.skills.items():
                if skill in skills:
                    skills[skill] += value
        
        report_str = f"\nЗвіт про навички команди {self.name}:\n"
        for skill, value in skills.items():
            avg = value / len(self.members) if self.members else 0
            report_str += f"- {skill.capitalize()}: Всього {value}, Середнє {avg:.1f}\n"
            
        self.log_event("Згенеровано звіт про навички команди")
        return report_str
    
    def log_event(self, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = f"{timestamp}: Команда {self.name} - {description}"
        self.mission_log.append(event)
        return event
    
    def __str__(self):
        return f"Команда {self.name} ({len(self.members)} членів, Командир: {self.commander.name if self.commander else 'Немає'})"


class Mission:
    STATUS_TYPES = ["Очікує", "Активна", "Завершена", "Провалена", "Перервана"]
    
    def __init__(self, name, description, location, teams=None):
        self.name = name
        self.description = description
        self.location = location
        self.teams = teams or []
        self.status = "Очікує"
        self.objectives = []
        self.events = []
        self.start_time = None
        self.end_time = None
        self.difficulty = 1  # Шкала 1-10
        self.success_rate = 0
        self.rewards = {"досвід": 10}
        
        self.log_event(f"Місія створена: {name}")
    
    def add_team(self, team):
        self.teams.append(team)
        self.log_event(f"Команда {team.name} додана до місії")
        return True
    
    def add_objective(self, objective, completed=False):
        self.objectives.append({"description": objective, "completed": completed, "added": datetime.now()})
        self.log_event(f"Додано ціль: {objective}")
        return True
    
    def complete_objective(self, index):
        if 0 <= index < len(self.objectives):
            self.objectives[index]["completed"] = True
            self.objectives[index]["completed_time"] = datetime.now()
            self.log_event(f"Ціль завершена: {self.objectives[index]['description']}")
            
            # Перевірка, чи всі цілі завершені
            if all(obj["completed"] for obj in self.objectives):
                self.status = "Завершена"
                self.end_time = datetime.now()
                self.success_rate = 100
                self.log_event("Всі цілі завершені")
                
                # Нагородження досвідом членів команди
                for team in self.teams:
                    for member in team.members:
                        member.gain_experience(self.rewards["досвід"])
                
            return True
        return False
    
    def log_event(self, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = f"{timestamp}: {description}"
        self.events.append(event)
        return event
    
    def update_status(self, new_status):
        if new_status not in self.STATUS_TYPES:
            return False
            
        old_status = self.status
        self.status = new_status
        
        if new_status == "Активна" and not self.start_time:
            self.start_time = datetime.now()
        elif new_status in ["Завершена", "Провалена", "Перервана"] and not self.end_time:
            self.end_time = datetime.now()
            
        self.log_event(f"Статус оновлено з {old_status} на {self.status}")
        return True
    
    def set_difficulty(self, level):
        """Встановити складність місії за шкалою 1-10"""
        if 1 <= level <= 10:
            self.difficulty = level
            self.rewards["досвід"] = level * 10  # Вища складність, вищі нагороди
            self.log_event(f"Складність встановлено на {level}")
            return True
        return False
    
    def add_reward(self, reward_type, value):
        self.rewards[reward_type] = value
        self.log_event(f"Додано нагороду: {reward_type} = {value}")
        return True
    
    def mission_report(self):
        completed = sum(1 for obj in self.objectives if obj["completed"])
        
        report = f"\nЗвіт про місію: {self.name}\n"
        report += f"Статус: {self.status}\n"
        report += f"Локація: {self.location}\n"
        report += f"Опис: {self.description}\n"
        report += f"Складність: {self.difficulty}/10\n"
        
        if self.start_time:
            report += f"Час початку: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        if self.end_time:
            report += f"Час завершення: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            if self.start_time:
                duration = self.end_time - self.start_time
                report += f"Тривалість: {duration}\n"
        
        report += f"Цілі: {completed}/{len(self.objectives)} завершено\n"
        
        for i, obj in enumerate(self.objectives):
            status = "✓" if obj["completed"] else "✗"
            report += f"  {status} {i+1}. {obj['description']}\n"
        
        report += "\nКоманди, призначені на місію:\n"
        for team in self.teams:
            report += f"- {team.name} ({len(team.members)} членів)\n"
        
        if self.events:
            report += "\nОстанні події:\n"
            for event in self.events[-5:]:
                report += f"  - {event}\n"
        
        self.log_event("Згенеровано звіт про місію")
        return report
    
    def calculate_success_probability(self):
        """Розрахувати ймовірність успіху місії на основі складу команди"""
        if not self.teams or not any(team.members for team in self.teams):
            return 0
            
        total_members = sum(len(team.members) for team in self.teams)
        active_members = sum(sum(1 for m in team.members if m.status == "Активний") for team in self.teams)
        
        if active_members == 0:
            return 0
            
        active_ratio = active_members / total_members
        
        # Розрахунок середнього рівня навичок у всіх командах
        combat = medical = recon = leadership = 0
        for team in self.teams:
            for member in team.members:
                if member.status == "Активний":
                    combat += member.skills["бойові"]
                    medical += member.skills["медичні"]
                    recon += member.skills["розвідка"]
                    leadership += member.skills["лідерство"]
        
        # Середній рівень навичок (шкала 1-10)
        avg_skill = (combat + medical + recon + leadership) / (active_members * 4) if active_members > 0 else 0
        
        # Формула ймовірності успіху: нормалізований рівень навичок проти складності, з урахуванням активного складу
        probability = (avg_skill / 10) * (1 / self.difficulty) * active_ratio * 100
        probability = min(100, max(0, probability))
        
        self.success_rate = round(probability, 1)
        self.log_event(f"Розраховано ймовірність успіху: {self.success_rate}%")
        return self.success_rate
    
    def __str__(self):
        return f"Місія: {self.name} ({self.status})"


class MilitarySimulator:
    def __init__(self):
        self.soldiers = []
        self.teams = []
        self.missions = []
        self.events_log = []
        self.equipment_database = {
            "Гвинтівка": {"вага": 4.5, "ефективність": 7},
            "Пістолет": {"вага": 1.0, "ефективність": 4},
            "Аптечка": {"вага": 2.0, "ефективність": 8},
            "Рація": {"вага": 1.5, "ефективність": 6},
            "Бінокль": {"вага": 1.0, "ефективність": 5},
            "Патрони": {"вага": 0.5, "ефективність": 6},
            "Граната": {"вага": 0.7, "ефективність": 8},
            "Рація": {"вага": 1.0, "ефективність": 3},
            "Вода": {"вага": 1.5, "ефективність": 4},
            "Нічний приціл": {"вага": 1.2, "ефективність": 7}
        }
        self.log_event("Військовий симулятор ініціалізовано")
    
    def create_soldier(self, name, status="Активний", location=(0, 0), rank="Рядовий"):
        soldier = Soldier(name, status, location, rank)
        self.soldiers.append(soldier)
        self.log_event(f"Солдат створено: {name}")
        return soldier
    
    def create_team(self, name):
        team = Team(name)
        self.teams.append(team)
        self.log_event(f"Команда створена: {name}")
        return team
    
    def create_mission(self, name, description, location):
        mission = Mission(name, description, location)
        self.missions.append(mission)
        self.log_event(f"Місія створена: {name}")
        return mission
    
    def assign_soldier_to_team(self, soldier_name, team_name):
        soldier = self.find_soldier(soldier_name)
        team = self.find_team(team_name)
        
        if soldier and team:
            team.add_member(soldier)
            self.log_event(f"{soldier.name} призначено до команди {team.name}")
            return True
        return False
    
    def assign_team_to_mission(self, team_name, mission_name):
        team = self.find_team(team_name)
        mission = self.find_mission(mission_name)
        
        if team and mission:
            mission.add_team(team)
            team.assign_team_mission(mission.name)
            self.log_event(f"Команда {team.name} призначена на місію {mission.name}")
            return True
        return False
    
    def find_soldier(self, name):
        for soldier in self.soldiers:
            if soldier.name.lower() == name.lower():
                return soldier
        return None
    
    def find_team(self, name):
        for team in self.teams:
            if team.name.lower() == name.lower():
                return team
        return None
    
    def find_mission(self, name):
        for mission in self.missions:
            if mission.name.lower() == name.lower():
                return mission
        return None
    
    def log_event(self, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = f"{timestamp}: {description}"
        self.events_log.append(event)
        return event
    
    def global_status_report(self):
        report = "\n===== ЗАГАЛЬНИЙ ЗВІТ ПРО СТАН =====\n"
        
        report += f"Всього персоналу: {len(self.soldiers)}\n"
        report += f"Активні команди: {len(self.teams)}\n"
        report += f"Місії: {len(self.missions)}\n\n"
        
        status_counts = {}
        for soldier in self.soldiers:
            if soldier.status in status_counts:
                status_counts[soldier.status] += 1
            else:
                status_counts[soldier.status] = 1
                
        report += "Статус персоналу:\n"
        for status, count in status_counts.items():
            report += f"- {status}: {count}\n"
        
        mission_status = {}
        for mission in self.missions:
            if mission.status in mission_status:
                mission_status[mission.status] += 1
            else:
                mission_status[mission.status] = 1
                
        report += "\nСтатус місій:\n"
        for status, count in mission_status.items():
            report += f"- {status}: {count}\n"
        
        return report
    
    def distribute_equipment(self, team_name, equipment_dict):
        team = self.find_team(team_name)
        if team:
            return team.distribute_equipment(equipment_dict)
        return False
    
    def simulate_mission_progress(self, mission_name, success_chance=None):
        """Симулювати прогрес місії автоматично"""
        mission = self.find_mission(mission_name)
        if not mission:
            return False
            
        if mission.status not in ["Очікує", "Активна"]:
            return False
            
        # Початок місії, якщо вона очікує
        if mission.status == "Очікує":
            mission.update_status("Активна")
            
        # Розрахунок ймовірності успіху, якщо не вказано
        if success_chance is None:
            success_chance = mission.calculate_success_probability()
            
        # Обробка кожної цілі
        for i, objective in enumerate(mission.objectives):
            if not objective["completed"]:
                # Випадковий шанс завершення цілі на основі ймовірності успіху
                if random.random() * 100 < success_chance:
                    mission.complete_objective(i)
                    
                    # Випадкові події під час місії
                    if random.random() < 0.3:  # 30% шанс випадкової події
                        events = [
                            "зустріли легкий опір",
                            "знайшли цінну інформацію",
                            "знайшли альтернативний маршрут",
                            "сталася поломка обладнання",
                            "погода погіршилася"
                        ]
                        mission.log_event(f"Випадкова подія: {random.choice(events)}")
                    
                    # Випадкові поранення
                    if random.random() < 0.2:  # 20% шанс поранення
                        for team in mission.teams:
                            for member in team.members:
                                if member.status == "Активний" and random.random() < 0.1:
                                    damage = random.randint(5, 25)
                                    member.update_health(-damage)
                                    mission.log_event(f"{member.name} отримав {damage} пошкоджень")
                else:
                    # Ціль провалена
                    mission.log_event(f"Не вдалося завершити ціль: {objective['description']}")
                    if random.random() < 0.3:  # 30% шанс провалу місії при провалі цілі
                        mission.update_status("Провалена")
                        return mission.status
                        
                break  # Обробляти одну ціль за раз
                
        return mission.status
    
    def clear_screen(self):
        """Очистити екран консолі"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Показати головне меню"""
        self.clear_screen()
        print("\n===== ВІЙСЬКОВИЙ СИМУЛЯТОР =====")
        print("1. Керування солдатами")
        print("2. Керування командами")
        print("3. Керування місіями")
        print("4. Керування симуляцією")
        print("5. Звіти")
        print("6. Вийти")
        
        choice = input("\nВведіть ваш вибір (1-6): ")
        return choice
    
    def soldier_menu(self):
        """Показати меню керування солдатами"""
        self.clear_screen()
        print("\n===== КЕРУВАННЯ СОЛДАТАМИ =====")
        print("1. Створити нового солдата")
        print("2. Переглянути деталі солдата")
        print("3. Оновити статус солдата")
        print("4. Додати спорядження солдату")
        print("5. Оновити здоров'я солдата")
        print("6. Список усіх солдатів")
        print("7. Повернутися до головного меню")
        
        choice = input("\nВведіть ваш вибір (1-7): ")
        
        if choice == "1":
            name = input("Введіть ім'я солдата: ")
            rank = input("Введіть звання солдата (за замовчуванням: Рядовий): ") or "Рядовий"
            status = input("Введіть статус (Активний/Поранений/Недоступний, за замовчуванням: Активний): ") or "Активний"
            
            soldier = self.create_soldier(name, status=status, rank=rank)
            print(f"Солдат створено: {soldier}")
            
        elif choice == "2":
            name = input("Введіть ім'я солдата: ")
            soldier = self.find_soldier(name)
            
            if soldier:
                print("\n===== ДЕТАЛІ СОЛДАТА =====")
                for key, value in soldier.report_status().items():
                    print(f"{key.capitalize()}: {value}")
                    
                print("\nОстанні події:")
                for event in soldier.history[-5:]:
                    print(f"- {event}")
            else:
                print(f"Солдата '{name}' не знайдено")
                
        elif choice == "3":
            name = input("Введіть ім'я солдата: ")
            soldier = self.find_soldier(name)
            
            if soldier:
                print(f"Поточний статус: {soldier.status}")
                status = input("Введіть новий статус (Активний/Поранений/Недоступний/У відпустці/Зниклий безвісти): ")
                if soldier.update_status(status):
                    print(f"Статус оновлено на {status}")
                else:
                    print("Невірний статус")
            else:
                print(f"Солдата '{name}' не знайдено")
                
        elif choice == "4":
            name = input("Введіть ім'я солдата: ")
            soldier = self.find_soldier(name)
            
            if soldier:
                print("Доступне спорядження:")
                for item in self.equipment_database:
                    print(f"- {item}")
                    
                item = input("Введіть спорядження для додавання: ")
                if item in self.equipment_database:
                    try:
                        quantity = int(input("Введіть кількість: "))
                        soldier.add_equipment(item, quantity)
                        print(f"Додано {quantity} {item} до {soldier.name}")
                    except ValueError:
                        print("Невірна кількість")
                else:
                    print(f"Спорядження '{item}' не знайдено в базі даних")
            else:
                print(f"Солдата '{name}' не знайдено")
                
        elif choice == "5":
            name = input("Введіть ім'я солдата: ")
            soldier = self.find_soldier(name)
            
            if soldier:
                print(f"Поточне здоров'я: {soldier.health}")
                try:
                    amount = int(input("Введіть зміну здоров'я (додатнє для лікування, від'ємне для пошкоджень): "))
                    new_health = soldier.update_health(amount)
                    print(f"Здоров'я оновлено до {new_health}")
                except ValueError:
                    print("Невірне введення")
            else:
                print(f"Солдата '{name}' не знайдено")
                
        elif choice == "6":
            if not self.soldiers:
                print("Солдатів не знайдено")
            else:
                print("\n===== УСІ СОЛДАТИ =====")
                for i, soldier in enumerate(self.soldiers, 1):
                    print(f"{i}. {soldier}")
                    
        input("\nНатисніть Enter, щоб продовжити...")
        
    def team_menu(self):
        """Показати меню керування командами"""
        self.clear_screen()
        print("\n===== КЕРУВАННЯ КОМАНДАМИ =====")
        print("1. Створити нову команду")
        print("2. Додати солдата до команди")
        print("3. Призначити командира команди")
        print("4. Переглянути статус команди")
        print("5. Перемістити команду")
        print("6. Згенерувати звіт про спорядження")
        print("7. Розподілити спорядження")
        print("8. Список усіх команд")
        print("9. Повернутися до головного меню")
        
        choice = input("\nВведіть ваш вибір (1-9): ")
        
        if choice == "1":
            name = input("Введіть назву команди: ")
            team = self.create_team(name)
            print(f"Команда створена: {team}")
            
        elif choice == "2":
            team_name = input("Введіть назву команди: ")
            team = self.find_team(team_name)
            
            if team:
                soldier_name = input("Введіть ім'я солдата для додавання: ")
                soldier = self.find_soldier(soldier_name)
                
                if soldier:
                    team.add_member(soldier)
                    print(f"{soldier.name} додано до команди {team_name}")
                else:
                    print(f"Солдата '{soldier_name}' не знайдено")
            else:
                print(f"Команду '{team_name}' не знайдено")
                
        elif choice == "3":
            team_name = input("Введіть назву команди: ")
            team = self.find_team(team_name)
            
            if team:
                print("Поточні члени команди:")
                for i, member in enumerate(team.members, 1):
                    print(f"{i}. {member}")
                    
                commander_name = input("Введіть ім'я солдата, якого призначити командиром: ")
                commander = self.find_soldier(commander_name)
                
                if commander and commander in team.members:
                    team.set_commander(commander)
                    print(f"{commander.name} призначено командиром команди {team_name}")
                else:
                    print(f"Солдата '{commander_name}' не знайдено або він не в команді")
            else:
                print(f"Команду '{team_name}' не знайдено")
                
        elif choice == "4":
            team_name = input("Введіть назву команди: ")
            team = self.find_team(team_name)
            
            if team:
                print(team.team_status())
            else:
                print(f"Команду '{team_name}' не знайдено")
                
        elif choice == "5":
            team_name = input("Введіть назву команди: ")
            team = self.find_team(team_name)
            
            if team:
                try:
                    x = int(input("Введіть x-координату: "))
                    y = int(input("Введіть y-координату: "))
                    
                    spacing = int(input("Введіть інтервал формації (за замовчуванням: 5): ") or "5")
                    
                    team.move_team((x, y), formation_spacing=spacing)
                    print(f"Команда {team_name} переміщена до ({x}, {y})")
                except ValueError:
                    print("Невірний формат координат")
            else:
                print(f"Команду '{team_name}' не знайдено")
                
        elif choice == "6":
            team_name = input("Введіть назву команди: ")
            team = self.find_team(team_name)
            
            if team:
                print(team.equipment_report())
            else:
                print(f"Команду '{team_name}' не знайдено")
                
        elif choice == "7":
            team_name = input("Введіть назву команди: ")
            team = self.find_team(team_name)
            
            if team:
                print("Доступне спорядження:")
                for item in self.equipment_database:
                    print(f"- {item}")
                    
                equipment = {}
                while True:
                    item = input("Введіть спорядження для розподілу (або 'done' для завершення): ")
                    if item.lower() == 'done':
                        break
                    
                    if item in self.equipment_database:
                        try:
                            quantity = int(input("Введіть кількість: "))
                            equipment[item] = quantity
                        except ValueError:
                            print("Невірна кількість")
                    else:
                        print(f"Спорядження '{item}' не знайдено в базі даних")
                
                if equipment:
                    team.distribute_equipment(equipment)
                    print(f"Спорядження розподілено в команді {team_name}")
            else:
                print(f"Команду '{team_name}' не знайдено")
                
        elif choice == "8":
            if not self.teams:
                print("Команд не знайдено")
            else:
                print("\n===== УСІ КОМАНДИ =====")
                for i, team in enumerate(self.teams, 1):
                    commander_name = team.commander.name if team.commander else "Немає"
                    print(f"{i}. {team.name} - Членів: {len(team.members)}, Командир: {commander_name}")
                    
        input("\nНатисніть Enter, щоб продовжити...")
        
    def mission_menu(self):
        """Показати меню керування місіями"""
        self.clear_screen()
        print("\n===== КЕРУВАННЯ МІСІЯМИ =====")
        print("1. Створити нову місію")
        print("2. Додати команду до місії")
        print("3. Додати ціль до місії")
        print("4. Завершити ціль")
        print("5. Змінити статус місії")
        print("6. Переглянути звіт про місію")
        print("7. Розрахувати ймовірність успіху")
        print("8. Встановити складність місії")
        print("9. Список усіх місій")
        print("0. Повернутися до головного меню")
        
        choice = input("\nВведіть ваш вибір (0-9): ")
        
        if choice == "1":
            name = input("Введіть назву місії: ")
            description = input("Введіть опис місії: ")
            
            try:
                x = int(input("Введіть x-координату: "))
                y = int(input("Введіть y-координату: "))
                location = (x, y)
                
                mission = self.create_mission(name, description, location)
                
                difficulty = input("Введіть складність місії (1-10, за замовчуванням: 1): ") or "1"
                try:
                    mission.set_difficulty(int(difficulty))
                except ValueError:
                    print("Невірна складність, використовується за замовчуванням")
                    
                print(f"Місія створена: {mission}")
            except ValueError:
                print("Невірний формат координат")
                
        elif choice == "2":
            mission_name = input("Введіть назву місії: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                team_name = input("Введіть назву команди для додавання: ")
                team = self.find_team(team_name)
                
                if team:
                    mission.add_team(team)
                    team.assign_team_mission(mission.name)
                    print(f"Команда {team_name} додана до місії {mission_name}")
                else:
                    print(f"Команду '{team_name}' не знайдено")
            else:
                print(f"Місію '{mission_name}' не знайдено")
                
        elif choice == "3":
            mission_name = input("Введіть назву місії: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                objective = input("Введіть опис цілі: ")
                mission.add_objective(objective)
                print(f"Ціль додано до місії {mission_name}")
            else:
                print(f"Місію '{mission_name}' не знайдено")
                
        elif choice == "4":
            mission_name = input("Введіть назву місії: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                print("Поточні цілі:")
                for i, obj in enumerate(mission.objectives):
                    status = "✓" if obj["completed"] else "✗"
                    print(f"{i+1}. {status} {obj['description']}")
                    
                try:
                    index = int(input("Введіть номер цілі для завершення: ")) - 1
                    if mission.complete_objective(index):
                        print("Ціль завершена")
                    else:
                        print("Невірний номер цілі")
                except ValueError:
                    print("Невірне введення")
            else:
                print(f"Місію '{mission_name}' не знайдено")
              
        elif choice == "5":
            mission_name = input("Введіть назву місії: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                print(f"Поточний статус: {mission.status}")
                print("Доступні статуси: Очікує, Активна, Завершена, Провалена, Перервана")
                
                status = input("Введіть новий статус: ")
                if mission.update_status(status):
                    print(f"Статус оновлено на {status}")
                else:
                    print("Невірний статус")
            else:
                print(f"Місію '{mission_name}' не знайдено")
              
        elif choice == "6":
            mission_name = input("Введіть назву місії: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                print(mission.mission_report())
            else:
                print(f"Місію '{mission_name}' не знайдено")
              
        elif choice == "7":
            mission_name = input("Введіть назву місії: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                probability = mission.calculate_success_probability()
                print(f"Ймовірність успіху місії: {probability}%")
            else:
                print(f"Місію '{mission_name}' не знайдено")
              
        elif choice == "8":
            mission_name = input("Введіть назву місії: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                try:
                    difficulty = int(input("Введіть рівень складності (1-10): "))
                    if mission.set_difficulty(difficulty):
                        print(f"Складність встановлено на {difficulty}")
                    else:
                        print("Невірний рівень складності")
                except ValueError:
                    print("Невірне введення")
            else:
                print(f"Місію '{mission_name}' не знайдено")
              
        elif choice == "9":
            if not self.missions:
                print("Місій не знайдено")
            else:
                print("\n===== УСІ МІСІЇ =====")
                for i, mission in enumerate(self.missions, 1):
                    completed = sum(1 for obj in mission.objectives if obj["completed"])
                    total = len(mission.objectives)
                    print(f"{i}. {mission.name} - Статус: {mission.status}, Цілі: {completed}/{total}, Команди: {len(mission.teams)}")
                    
        input("\nНатисніть Enter, щоб продовжити...")
    
    def simulation_menu(self):
        """Показати меню керування симуляцією"""
        self.clear_screen()
        print("\n===== КЕРУВАННЯ СИМУЛЯЦІЄЮ =====")
        print("1. Симулювати прогрес місії")
        print("2. Автоматично завершити місію")
        print("3. Згенерувати подію з пораненням")
        print("4. Згенерувати випадкову подію")
        print("5. Повернутися до головного меню")
        
        choice = input("\nВведіть ваш вибір (1-5): ")
        
        if choice == "1":
            mission_name = input("Введіть назву місії: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                status = self.simulate_mission_progress(mission_name)
                print(f"Прогрес місії симульовано. Новий статус: {status}")
            else:
                print(f"Місію '{mission_name}' не знайдено")
              
        elif choice == "2":
            mission_name = input("Введіть назву місії: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                if mission.status not in ["Завершена", "Провалена", "Перервана"]:
                    mission.update_status("Активна")
                    
                    print(f"Автоматичне завершення місії {mission_name}...")
                    for i in range(len(mission.objectives)):
                        if not mission.objectives[i]["completed"]:
                            mission.complete_objective(i)
                            time.sleep(0.5)  # Невелика затримка для ефекту
                    
                    mission.update_status("Завершена")
                    print(f"Місія {mission_name} автоматично завершена")
                else:
                    print(f"Місія {mission_name} вже завершена зі статусом: {mission.status}")
            else:
                print(f"Місію '{mission_name}' не знайдено")
              
        elif choice == "3":
            team_name = input("Введіть назву команди: ")
            team = self.find_team(team_name)
            
            if team:
                active_members = [m for m in team.members if m.status == "Активний"]
                if not active_members:
                    print("Немає активних членів у команді")
                else:
                    victim = random.choice(active_members)
                    damage = random.randint(10, 50)
                    
                    print(f"Згенеровано подію з пораненням для {victim.name}")
                    victim.update_health(-damage)
                    
                    team.log_event(f"Подія з пораненням: {victim.name} отримав {damage} пошкоджень")
                    print(f"Здоров'я {victim.name} знижено до {victim.health}")
                    
                    if victim.status == "Поранений":
                        print(f"{victim.name} тепер поранений і потребує медичної допомоги!")
            else:
                print(f"Команду '{team_name}' не знайдено")
              
        elif choice == "4":
            mission_name = input("Введіть назву місії: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                events = [
                    "зустріли неочікуваний опір",
                    "знайшли цінну інформацію",
                    "виникла поломка обладнання",
                    "погода погіршилася",
                    "знайшли альтернативний маршрут",
                    "зв'язок порушено",
                    "отримали постачання",
                    "зустріли дружні сили",
                    "виявили ворожу патрульну групу",
                    "зайняли ключову позицію"
                ]
                
                event = random.choice(events)
                mission.log_event(f"Випадкова подія: {event}")
                print(f"Згенеровано випадкову подію для місії {mission_name}: {event}")
            else:
                print(f"Місію '{mission_name}' не знайдено")
              
        input("\nНатисніть Enter, щоб продовжити...")
    
    def reports_menu(self):
        """Показати меню звітів"""
        self.clear_screen()
        print("\n===== ЗВІТИ =====")
        print("1. Загальний звіт про стан")
        print("2. Оцінка навичок команди")
        print("3. Ймовірності успіху місій")
        print("4. Журнал останніх подій")
        print("5. Підсумок спорядження")
        print("6. Статус персоналу")
        print("7. Повернутися до головного меню")
        
        choice = input("\nВведіть ваш вибір (1-7): ")
        
        if choice == "1":
            print(self.global_status_report())
              
        elif choice == "2":
            print("\n===== ОЦІНКА НАВИЧОК КОМАНДИ =====")
            if not self.teams:
                print("Команд не знайдено")
            else:
                for team in self.teams:
                    print(team.team_skill_report())
              
        elif choice == "3":
            print("\n===== ЙМОВІРНОСТІ УСПІХУ МІСІЙ =====")
            if not self.missions:
                print("Місій не знайдено")
            else:
                for mission in self.missions:
                    probability = mission.calculate_success_probability()
                    print(f"Місія: {mission.name}")
                    print(f"Статус: {mission.status}")
                    print(f"Складність: {mission.difficulty}/10")
                    print(f"Ймовірність успіху: {probability}%")
                    
                    # Показати причини на основі складу команди
                    print("Чинники, що впливають на ймовірність:")
                    
                    # Кількість команд
                    team_count = len(mission.teams)
                    print(f"- Команд призначено: {team_count}")
                    
                    # Кількість персоналу
                    total_personnel = sum(len(team.members) for team in mission.teams)
                    active_personnel = sum(sum(1 for m in team.members if m.status == "Активний") for team in mission.teams)
                    print(f"- Персонал: {active_personnel} активних з {total_personnel} всього")
                    
                    print("\n")
              
        elif choice == "4":
            print("\n===== ЖУРНАЛ ОСТАННІХ ПОДІЙ =====")
            logs_to_show = min(20, len(self.events_log))
            for log in self.events_log[-logs_to_show:]:
                print(log)
              
        elif choice == "5":
            print("\n===== ПІДСУМОК СПОРЯДЖЕННЯ =====")
            all_equipment = {}
            
            # Підрахунок усього спорядження серед усіх солдатів
            for soldier in self.soldiers:
                for item, qty in soldier.equipment.items():
                    if item in all_equipment:
                        all_equipment[item] += qty
                    else:
                        all_equipment[item] = qty
            
            if not all_equipment:
                print("Спорядження не знайдено")
            else:
                for item, qty in all_equipment.items():
                    info = self.equipment_database.get(item, {})
                    weight = info.get("вага", "Н/Д")
                    effectiveness = info.get("ефективність", "Н/Д")
                    
                    print(f"- {item}: {qty} одиниць (Вага: {weight}, Ефективність: {effectiveness})")
              
        elif choice == "6":
            print("\n===== СТАТУС ПЕРСОНАЛУ =====")
            if not self.soldiers:
                print("Персоналу не знайдено")
            else:
                status_groups = {}
                for soldier in self.soldiers:
                    if soldier.status not in status_groups:
                        status_groups[soldier.status] = []
                    status_groups[soldier.status].append(soldier)
                
                for status, soldiers in status_groups.items():
                    print(f"\n{status} Персонал ({len(soldiers)}):")
                    for soldier in soldiers:
                        print(f"- {soldier.rank} {soldier.name}, Здоров'я: {soldier.health}%")
              
        input("\nНатисніть Enter, щоб продовжити...")
    
    def run(self):
        """Запустити інтерфейс симулятора"""
        while True:
            choice = self.display_menu()
            
            if choice == "1":
                self.soldier_menu()
            elif choice == "2":
                self.team_menu()
            elif choice == "3":
                self.mission_menu()
            elif choice == "4":
                self.simulation_menu()
            elif choice == "5":
                self.reports_menu()
            elif choice == "6":
                print("Вихід з симулятора...")
                break
            else:
                print("Невірний вибір")


# Приклад даних
def create_sample_data(simulator):
    # Створення солдатів
    s1 = simulator.create_soldier("Джонсон", rank="Сержант", location=(10, 10))
    s2 = simulator.create_soldier("Сміт", rank="Капрал", location=(12, 10))
    s3 = simulator.create_soldier("Вільямс", rank="Медик", location=(8, 10))
    s4 = simulator.create_soldier("Міллер", rank="Рядовий", location=(10, 12))
    s5 = simulator.create_soldier("Девіс", rank="Рядовий", location=(10, 8))
    s6 = simulator.create_soldier("Гарсія", rank="Сержант", location=(20, 20))
    s7 = simulator.create_soldier("Вілсон", rank="Капрал", location=(22, 20))
    s8 = simulator.create_soldier("Тейлор", rank="Рядовий", location=(20, 22))
    
    # Додавання спорядження
    s1.add_equipment("Гвинтівка", 1)
    s1.add_equipment("Патрони", 5)
    s2.add_equipment("Рація", 1)
    s2.add_equipment("Пістолет", 1)
    s3.add_equipment("Аптечка", 3)
    s3.add_equipment("Вода", 2)
    s4.add_equipment("Бінокль", 1)
    s4.add_equipment("Патрони", 3)
    s5.add_equipment("Гвинтівка", 1)
    s5.add_equipment("Граната", 2)
    s6.add_equipment("Гвинтівка", 1)
    s6.add_equipment("Нічний приціл", 1)
    s7.add_equipment("Рація", 1)
    s7.add_equipment("Патрони", 4)
    s8.add_equipment("Гвинтівка", 1)
    s8.add_equipment("Рація", 3)
    
    # Створення команд
    alpha = simulator.create_team("Альфа")
    bravo = simulator.create_team("Браво")
    
    # Додавання членів до команд
    alpha.add_member(s1)
    alpha.add_member(s2)
    alpha.add_member(s3)
    alpha.add_member(s4)
    alpha.add_member(s5)
    bravo.add_member(s6)
    bravo.add_member(s7)
    bravo.add_member(s8)
    
    # Призначення командирів
    alpha.set_commander(s1)
    bravo.set_commander(s6)
    
    # Створення місій
    recon = simulator.create_mission("Орлине око", "Розвідка ворожої території", (50, 60))
    recon.set_difficulty(3)
    recon.add_objective("Досягти точки спостереження")
    recon.add_objective("Зібрати розвіддані")
    recon.add_objective("Задокументувати рух ворога")
    recon.add_objective("Повернутися на базу")
    
    assault = simulator.create_mission("Удар молота", "Знищення ворожого опорного пункту", (80, 30))
    assault.set_difficulty(7)
    assault.add_objective("Забезпечити периметр")
    assault.add_objective("Знищити ворожі сили")
    assault.add_objective("Забезпечити об'єкт")
    assault.add_objective("Отримати розвіддані")
    assault.add_objective("Відступити з території")
    
    # Призначення команд на місії
    recon.add_team(alpha)
    alpha.assign_team_mission(recon.name)
    
    assault.add_team(bravo)
    bravo.assign_team_mission(assault.name)
    
    # Симуляція деякого прогресу
    recon.update_status("Активна")
    recon.complete_objective(0)
    recon.log_event("Команда Альфа досягла точки спостереження")
    
    simulator.log_event("Прикладні дані успішно створено")
    return simulator


# Основне виконання
if __name__ == "__main__":
    simulator = MilitarySimulator()
    
    # Запит на завантаження прикладних даних
    print("Військовий симулятор")
    use_sample = input("Бажаєте завантажити прикладні дані? (y/n): ").lower()
    
    if use_sample == 'y':
        simulator = create_sample_data(simulator)
        print("Прикладні дані завантажено!")
    
    # Запуск інтерфейсу симулятора
    simulator.run()