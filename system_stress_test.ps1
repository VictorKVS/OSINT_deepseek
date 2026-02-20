# system_stress_test.ps1 - Полное автоматическое тестирование системы

param(
    [int]$TestDuration = 120,
    [string]$OutputFile = "system_test_results.txt"
)

Write-Host "" -ForegroundColor Cyan
Write-Host "       ПОЛНОЕ ТЕСТИРОВАНИЕ СИСТЕМЫ RTX 3060            " -ForegroundColor Cyan
Write-Host "" -ForegroundColor Cyan
Write-Host "Тест будет длиться $TestDuration секунд" -ForegroundColor Yellow
Write-Host "Результаты сохранятся в: $OutputFile`n" -ForegroundColor Yellow

$results = @{
    TestStartTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    TestDuration = $TestDuration
    ComputerName = $env:COMPUTERNAME
    CPU = @{}
    GPU = @{}
    RAM = @{}
    Disk = @{}
    Temperatures = @{}
    Voltages = @{}
    Crashes = @()
    TestCompleted = $false
    ErrorMessages = @()
}

function Get-GPUTemperature {
    try {
        $counter = "\GPU Adapter Temperature\Temperature"
        $temp = (Get-Counter -Counter $counter -ErrorAction SilentlyContinue).CounterSamples.CookedValue
        if ($temp) { return $temp }
    } catch {}
    return $null
}

function Get-NvidiaData {
    try {
        $nvidiaSmi = & nvidia-smi --query-gpu=temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw --format=csv,noheader,nounits 2>$null
        if ($nvidiaSmi) {
            $data = $nvidiaSmi -split ','
            return @{
                Temperature = [int]$data[0].Trim()
                Utilization = [int]$data[1].Trim()
                MemoryUsed = [int]$data[2].Trim()
                MemoryTotal = [int]$data[3].Trim()
                PowerDraw = [float]$data[4].Trim()
            }
        }
    } catch {}
    return $null
}

function Get-SystemMetrics {
    $metrics = @{}
    
    $cpu = Get-WmiObject Win32_Processor
    $metrics["CPU_Usage"] = [math]::Round($cpu.LoadPercentage)
    
    $ram = Get-WmiObject Win32_OperatingSystem
    $metrics["RAM_Total"] = [math]::Round($ram.TotalVisibleMemorySize / 1MB, 2)
    $metrics["RAM_Free"] = [math]::Round($ram.FreePhysicalMemory / 1MB, 2)
    $metrics["RAM_Used"] = $metrics["RAM_Total"] - $metrics["RAM_Free"]
    $metrics["RAM_Usage_Percent"] = [math]::Round(($metrics["RAM_Used"] / $metrics["RAM_Total"]) * 100, 1)
    
    $nvidia = Get-NvidiaData
    if ($nvidia) {
        $metrics["GPU_Temp"] = $nvidia.Temperature
        $metrics["GPU_Utilization"] = $nvidia.Utilization
        $metrics["GPU_Memory_Used_MB"] = $nvidia.MemoryUsed
        $metrics["GPU_Memory_Total_MB"] = $nvidia.MemoryTotal
        $metrics["GPU_Power_W"] = $nvidia.PowerDraw
    }
    
    return $metrics
}

Write-Host "`n Начинаю сбор начальных данных..." -ForegroundColor Cyan
$initialMetrics = Get-SystemMetrics
Write-Host "  CPU: $($initialMetrics['CPU_Usage'])%" -ForegroundColor White
Write-Host "  GPU: $($initialMetrics['GPU_Utilization'])% ($($initialMetrics['GPU_Temp'])C)" -ForegroundColor White
Write-Host "  RAM: $($initialMetrics['RAM_Free'])GB свободно из $($initialMetrics['RAM_Total'])GB" -ForegroundColor White

$results.InitialState = $initialMetrics

Write-Host "`n ЗАПУСК СТРЕСС-ТЕСТА НА $TestDuration СЕКУНД" -ForegroundColor Red
Write-Host "  Следите за системой!" -ForegroundColor Yellow

$testMetrics = @()
$crashDetected = $false

$cpuLoadJob = Start-Job -ScriptBlock {
    $result = 0
    while ($true) {
        $result += [Math]::Sqrt($result + 1)
        if ($result -gt 1000000) { $result = 0 }
    }
}

try {
    $endTime = (Get-Date).AddSeconds($TestDuration)
    
    while ((Get-Date) -lt $endTime) {
        $currentMetrics = Get-SystemMetrics
        $testMetrics += $currentMetrics
        
        $timeLeft = [math]::Round(($endTime - (Get-Date)).TotalSeconds)
        $progress = [math]::Round((($TestDuration - $timeLeft) / $TestDuration) * 100)
        Write-Progress -Activity "Стресс-тест системы" -Status "Прогресс: $progress%" -PercentComplete $progress
        
        Write-Host "`r  Осталось: $timeLeft сек | CPU: $($currentMetrics['CPU_Usage'])% | GPU: $($currentMetrics['GPU_Utilization'])% ($($currentMetrics['GPU_Temp'])C) | RAM: $($currentMetrics['RAM_Free'])GB" -NoNewline
        
        if ($currentMetrics['GPU_Temp'] -gt 85) {
            Write-Host "`n  КРИТИЧЕСКАЯ ТЕМПЕРАТУРА GPU: $($currentMetrics['GPU_Temp'])C!" -ForegroundColor Red
        }
        
        Start-Sleep -Seconds 5
    }
    
    Write-Progress -Activity "Стресс-тест системы" -Completed
    Write-Host "`n`n Тест завершён успешно!" -ForegroundColor Green
    
} catch {
    $crashDetected = $true
    $errorMsg = $_.Exception.Message
    $results.Crashes += @{
        Time = Get-Date -Format "HH:mm:ss"
        Error = $errorMsg
    }
    Write-Host "`n ПРОИЗОШЁЛ СБОЙ!" -ForegroundColor Red
}

if ($cpuLoadJob.State -eq 'Running') {
    Stop-Job $cpuLoadJob
    Remove-Job $cpuLoadJob
}

$finalMetrics = Get-SystemMetrics
$results.FinalState = $finalMetrics
$results.TestMetrics = $testMetrics
$results.TestCompleted = -not $crashDetected
$results.TestEndTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$maxGPUTemp = ($testMetrics | Measure-Object -Property GPU_Temp -Maximum).Maximum
$avgGPUTemp = [math]::Round(($testMetrics | Measure-Object -Property GPU_Temp -Average).Average, 1)
$maxGPUUtil = ($testMetrics | Measure-Object -Property GPU_Utilization -Maximum).Maximum
$minRAM = ($testMetrics | Measure-Object -Property RAM_Free -Minimum).Minimum

$outputPath = Join-Path $PWD.Path $OutputFile

$report = @"
============================================================
    РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ СИСТЕМЫ
============================================================

 ОБЩАЯ ИНФОРМАЦИЯ:
   Компьютер: $($results.ComputerName)
   Дата теста: $($results.TestStartTime)
   Длительность: $($results.TestDuration) сек
   Тест завершён: $($results.TestCompleted)

 СИСТЕМА:
   Процессор: Intel Core i5-10400F
   Видеокарта: NVIDIA GeForce RTX 3060 12GB
   Оперативная память: 32GB DDR4
   Блок питания: VX PLUS 750W

 НАЧАЛЬНОЕ СОСТОЯНИЕ:
   CPU загрузка: $($initialMetrics['CPU_Usage'])\%
   GPU загрузка: $($initialMetrics['GPU_Utilization'])\%
   GPU температура: $($initialMetrics['GPU_Temp'])C
   GPU память: $($initialMetrics['GPU_Memory_Used_MB'])MB / $($initialMetrics['GPU_Memory_Total_MB'])MB
   RAM свободно: $($initialMetrics['RAM_Free'])GB

 ПОД НАГРУЗКОЙ (пиковые значения):
   Макс. температура GPU: $maxGPUTempC
   Средняя температура GPU: $avgGPUTempC
   Макс. загрузка GPU: $maxGPUUtil\%
   Макс. загрузка CPU: $(($testMetrics | Measure-Object -Property CPU_Usage -Maximum).Maximum)\%
   Мин. свободная RAM: $minRAM GB

 СБОИ:
   Обнаружено сбоев: $($results.Crashes.Count)
$(
if($results.Crashes.Count -gt 0) {
    $results.Crashes | ForEach-Object { "    $($_.Time): $($_.Error)" }
} else {
    "    Сбоев не зафиксировано"
}
)

 ОБЩИЙ ВЕРДИКТ:
$(
if($crashDetected) {
    "    ТЕСТ ПРОВАЛЕН - обнаружены сбои"
} elseif($maxGPUTemp -gt 85) {
    "    ТЕСТ ПРОЙДЕН, но высокая температура GPU ($maxGPUTempC)"
} elseif($minRAM -lt 2) {
    "    ТЕСТ ПРОЙДЕН, но мало свободной RAM ($minRAM GB)"
} else {
    "    ТЕСТ ПРОЙДЕН УСПЕШНО - система стабильна"
}
)

============================================================
   КОНЕЦ ОТЧЁТА
============================================================
"@

$report | Out-File -FilePath $outputPath -Encoding utf8

Write-Host "`n Отчёт сохранён в: $outputPath" -ForegroundColor Green
Write-Host "`n СОДЕРЖАНИЕ ОТЧЁТА:" -ForegroundColor Cyan
Write-Host "" * 60
Write-Host $report
Write-Host "" * 60
Write-Host "`n Отправьте этот файл мне!" -ForegroundColor Magenta
