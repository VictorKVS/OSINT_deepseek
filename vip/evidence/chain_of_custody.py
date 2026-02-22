"""
Модуль цепочки доказательств
Хэширование, аудит, верификация
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class EvidenceCollector:
    """
    Сбор и фиксация доказательств
    """
    
    def __init__(self, case_id: Optional[str] = None):
        self.case_id = case_id or self._generate_id()
        self.evidence_log = []
        self.hashes = {}
        self.chain_of_custody = []
        self.start_time = datetime.now()
        
        # Создаём папку для кейса
        self.case_dir = Path(f"data/evidence/{self.case_id}")
        self.case_dir.mkdir(parents=True, exist_ok=True)
    
    def capture(self, source: str, data: Any, evidence_type: str, metadata: Dict = None) -> Dict:
        """
        Фиксация доказательства
        """
        timestamp = datetime.now()
        evidence_id = self._generate_id()
        
        # Вычисляем хэш
        if isinstance(data, str):
            content = data.encode('utf-8')
        elif isinstance(data, bytes):
            content = data
        else:
            content = json.dumps(data, ensure_ascii=False).encode('utf-8')
        
        hash_value = hashlib.sha256(content).hexdigest()
        
        # Сохраняем данные
        data_path = self.case_dir / f"{evidence_id}.dat"
        with open(data_path, 'wb') as f:
            f.write(content)
        
        # Метаданные
        evidence = {
            'id': evidence_id,
            'case_id': self.case_id,
            'timestamp': timestamp.isoformat(),
            'source': source,
            'type': evidence_type,
            'hash': hash_value,
            'size': len(content),
            'metadata': metadata or {},
            'chain_position': len(self.chain_of_custody)
        }
        
        # Сохраняем метаданные
        meta_path = self.case_dir / f"{evidence_id}.meta.json"
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(evidence, f, indent=2)
        
        # Логируем
        self.evidence_log.append(evidence)
        self.hashes[evidence_id] = hash_value
        
        # Добавляем в цепочку хранения
        self._add_to_chain('capture', evidence_id, metadata)
        
        return evidence
    
    def _add_to_chain(self, action: str, evidence_id: str, metadata: Dict = None):
        """Добавление записи в цепочку хранения"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'evidence_id': evidence_id,
            'actor': 'system',
            'metadata': metadata or {}
        }
        self.chain_of_custody.append(entry)
        
        # Сохраняем цепочку
        chain_path = self.case_dir / "chain_of_custody.json"
        with open(chain_path, 'w', encoding='utf-8') as f:
            json.dump(self.chain_of_custody, f, indent=2)
    
    def verify(self, evidence_id: str) -> Dict:
        """
        Проверка целостности доказательства
        """
        if evidence_id not in self.hashes:
            return {'valid': False, 'error': 'Evidence not found'}
        
        # Загружаем данные
        data_path = self.case_dir / f"{evidence_id}.dat"
        if not data_path.exists():
            return {'valid': False, 'error': 'Data file missing'}
        
        with open(data_path, 'rb') as f:
            content = f.read()
        
        current_hash = hashlib.sha256(content).hexdigest()
        original_hash = self.hashes[evidence_id]
        
        # Проверяем метаданные
        meta_path = self.case_dir / f"{evidence_id}.meta.json"
        if meta_path.exists():
            with open(meta_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        else:
            metadata = None
        
        return {
            'valid': current_hash == original_hash,
            'evidence_id': evidence_id,
            'original_hash': original_hash,
            'current_hash': current_hash,
            'metadata': metadata,
            'chain_entries': [e for e in self.chain_of_custody if e['evidence_id'] == evidence_id]
        }
    
    def export_case(self) -> Dict:
        """
        Экспорт всего кейса
        """
        return {
            'case_id': self.case_id,
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'evidence_count': len(self.evidence_log),
            'evidence': self.evidence_log,
            'chain_of_custody': self.chain_of_custody,
            'hash_manifest': self.hashes
        }
    
    def generate_report(self) -> str:
        """
        Генерация отчёта
        """
        report = []
        report.append("=" * 60)
        report.append(f" ЦЕПОЧКА ДОКАЗАТЕЛЬСТВ: {self.case_id}")
        report.append("=" * 60)
        report.append(f"Начато: {self.start_time.isoformat()}")
        report.append(f"Завершено: {datetime.now().isoformat()}")
        report.append(f"Всего доказательств: {len(self.evidence_log)}")
        report.append("")
        
        for i, evidence in enumerate(self.evidence_log, 1):
            report.append(f" Доказательство #{i}: {evidence['id']}")
            report.append(f"   Источник: {evidence['source']}")
            report.append(f"   Тип: {evidence['type']}")
            report.append(f"   Время: {evidence['timestamp']}")
            report.append(f"   Хэш: {evidence['hash'][:16]}...")
            report.append("")
        
        report.append("=" * 60)
        report.append("ЦЕПОЧКА ХРАНЕНИЯ:")
        for entry in self.chain_of_custody[-10:]:  # последние 10 записей
            report.append(f"  {entry['timestamp']} | {entry['action']} | {entry['evidence_id']}")
        
        report.append("=" * 60)
        
        return '\n'.join(report)
    
    def _generate_id(self) -> str:
        """Генерация уникального ID"""
        import uuid
        return str(uuid.uuid4())[:12]


class MetadataSanitizer:
    """
    Очистка метаданных из файлов
    """
    
    def __init__(self):
        self.supported_formats = ['jpg', 'png', 'pdf', 'docx', 'mp3', 'mp4']
    
    def sanitize_image(self, image_path: str) -> str:
        """
        Удаление EXIF данных из изображения
        """
        try:
            from PIL import Image, ImageOps
            
            image = Image.open(image_path)
            
            # Создаём копию без метаданных
            data = list(image.getdata())
            clean_image = Image.new(image.mode, image.size)
            clean_image.putdata(data)
            
            # Сохраняем
            clean_path = image_path.replace('.', '_clean.')
            clean_image.save(clean_path)
            
            return clean_path
            
        except Exception as e:
            return f"Error: {e}"
    
    def sanitize_pdf(self, pdf_path: str) -> str:
        """
        Удаление метаданных из PDF
        """
        try:
            import PyPDF2
            
            with open(pdf_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                
                # Создаём новый PDF без метаданных
                writer = PyPDF2.PdfWriter()
                for page in pdf.pages:
                    writer.add_page(page)
                
                clean_path = pdf_path.replace('.', '_clean.')
                with open(clean_path, 'wb') as out:
                    writer.write(out)
            
            return clean_path
            
        except Exception as e:
            return f"Error: {e}"
    
    def remove_metadata(self, file_path: str) -> str:
        """
        Универсальная очистка метаданных
        """
        ext = file_path.split('.')[-1].lower()
        
        if ext in ['jpg', 'jpeg', 'png']:
            return self.sanitize_image(file_path)
        elif ext == 'pdf':
            return self.sanitize_pdf(file_path)
        else:
            return f"Unsupported format: {ext}"


# Тестовый запуск
if __name__ == "__main__":
    # Создаём кейс
    evidence = EvidenceCollector(case_id="TEST_CASE_001")
    
    # Добавляем доказательства
    evidence.capture(
        source="https://example.com",
        data="Пример собранной информации",
        evidence_type="web_page",
        metadata={"url": "https://example.com"}
    )
    
    evidence.capture(
        source="telegram_channel",
        data={"message": "Тестовое сообщение", "date": "2026-02-22"},
        evidence_type="telegram_message",
        metadata={"channel": "test_channel"}
    )
    
    # Проверяем
    print(evidence.generate_report())
    
    # Верифицируем последнее
    last_id = evidence.evidence_log[-1]['id']
    verification = evidence.verify(last_id)
    print(f"\n Верификация: {verification['valid']}")
