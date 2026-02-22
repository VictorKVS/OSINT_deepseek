"""
Модуль анонимности и маскировки
Базовые классы для дальнейшей реализации
"""

class AnonymityBase:
    """
    Базовый класс для всех модулей анонимности
    """
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.name = self.__class__.__name__
        self.active = False
    
    def activate(self) -> bool:
        """Активация модуля"""
        self.active = True
        return True
    
    def deactivate(self) -> bool:
        """Деактивация модуля"""
        self.active = False
        return True
    
    def status(self) -> dict:
        """Статус модуля"""
        return {
            'name': self.name,
            'active': self.active,
            'config': self.config
        }
    
    def __repr__(self) -> str:
        return f"<{self.name} active={self.active}>"
