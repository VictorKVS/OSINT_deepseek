# start.ps1 - Быстрый старт проекта после перезагрузки
# ИСПРАВЛЕННАЯ ВЕРСИЯ С РЕАЛЬНЫМИ ДАННЫМИ

Write-Host " Запуск OSINT DeepSeek" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

# Переходим в папку проекта
Set-Location G:\1\OSINT_deepseek
Write-Host " Перешёл в: $(Get-Location)" -ForegroundColor Green

# Активируем виртуальное окружение
if (Test-Path ".venv\Scripts\Activate.ps1") {
    .\.venv\Scripts\Activate.ps1
    Write-Host " Виртуальное окружение активировано" -ForegroundColor Green
} else {
    Write-Host " Виртуальное окружение не найдено!" -ForegroundColor Red
    Write-Host "Создайте: python -m venv .venv" -ForegroundColor Yellow
}

# Проверяем Ollama
try {
    $version = ollama --version
    Write-Host " Ollama: $version" -ForegroundColor Green
} catch {
    Write-Host " Ollama не запущена!" -ForegroundColor Red
    Write-Host "Запустите Ollama из меню Пуск" -ForegroundColor Yellow
}

# ========== УЛУЧШЕННОЕ ЛОГИРОВАНИЕ ==========
$logFile = "logs\startup.log"

# Собираем РЕАЛЬНУЮ информацию о системе
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# CPU - реальная нагрузка
$cpu = Get-WmiObject win32_processor | Measure-Object -Property LoadPercentage -Average | Select-Object -ExpandProperty Average
if (-not $cpu) { $cpu = 0 }

# RAM - реальное использование
$ram = Get-WmiObject Win32_OperatingSystem
$ramTotal = [math]::Round($ram.TotalVisibleMemorySize / 1MB, 2)
$ramFree = [math]::Round($ram.FreePhysicalMemory / 1MB, 2)
$ramUsed = $ramTotal - $ramFree
$ramPercent = [math]::Round(($ramUsed / $ramTotal) * 100, 1)

# GPU - если есть
try {
    $gpu = Get-WmiObject win32_videocontroller | Select-Object -First 1
    $gpuName = $gpu.Name
} catch {
    $gpuName = "Неизвестно"
}

# Температура (если есть датчики)
try {
    $temp = Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace "root/wmi" -ErrorAction SilentlyContinue
    if ($temp) {
        $celsius = [math]::Round(($temp.CurrentTemperature / 10) - 273.15, 1)
        $tempStr = "$celsiusC"
    } else {
        $tempStr = "Нет данных"
    }
} catch {
    $tempStr = "Нет данных"
}

# Формируем подробный лог
$logEntry = @"
[$timestamp] ЗАПУСК ПРОЕКТА
  CPU: ${cpu}% нагрузка
  RAM: Всего ${ramTotal}GB, Свободно ${ramFree}GB, Использовано ${ramUsed}GB (${ramPercent}%)
  GPU: ${gpuName}
  Температура: ${tempStr}
  Модели Ollama:
"@

# Добавляем список моделей
try {
    $models = ollama list
    if ($models) {
        foreach ($line in $models) {
            if ($line -match '^(\S+)\s+(\S+)\s+([\d\.]+[MG]B)') {
                $logEntry += "`n    - $($matches[1]) ($($matches[3]))"
            }
        }
    } else {
        $logEntry += "`n    - Нет загруженных моделей"
    }
} catch {
    $logEntry += "`n    - Ошибка получения списка моделей"
}

$logEntry += "`n" + "-"*50 + "`n"

# Сохраняем в лог
$logEntry | Out-File -FilePath $logFile -Encoding utf8 -Append

Write-Host " Подробный лог сохранён в $logFile" -ForegroundColor Green
Write-Host "`n Готово! Теперь можно:" -ForegroundColor Cyan
Write-Host "   Запустить мониторинг: python scripts/monitor.py" -ForegroundColor White
Write-Host "   Запустить умный агент: python scripts/smart_agent.py" -ForegroundColor White
Write-Host "   Протестировать модель: python scripts/rtx3060_agent.py" -ForegroundColor White
Write-Host "   Посмотреть логи: Get-Content logs\startup.log" -ForegroundColor White
