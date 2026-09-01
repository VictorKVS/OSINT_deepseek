param(
    [string] $ReportPath = 'reports\architect_telegram\LATEST_TELEGRAM_NETWORK_DIAGNOSTIC.json',
    [int] $TimeoutMilliseconds = 2500
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

function Test-TcpEndpoint {
    param(
        [Parameter(Mandatory = $true)][string] $HostName,
        [Parameter(Mandatory = $true)][int] $Port,
        [Parameter(Mandatory = $true)][int] $TimeoutMs
    )
    $client = [Net.Sockets.TcpClient]::new()
    try {
        $async = $client.BeginConnect($HostName, $Port, $null, $null)
        if (-not $async.AsyncWaitHandle.WaitOne($TimeoutMs, $false)) {
            return [pscustomobject]@{ host = $HostName; port = $Port; reachable = $false; error = 'TIMEOUT' }
        }
        try {
            $client.EndConnect($async)
            return [pscustomobject]@{ host = $HostName; port = $Port; reachable = $true; error = $null }
        } catch {
            return [pscustomobject]@{ host = $HostName; port = $Port; reachable = $false; error = $_.Exception.GetType().Name }
        }
    } catch {
        return [pscustomobject]@{ host = $HostName; port = $Port; reachable = $false; error = $_.Exception.GetType().Name }
    } finally {
        $client.Dispose()
    }
}

function Get-DnsStatus {
    param([Parameter(Mandatory = $true)][string] $HostName)
    try {
        $addresses = [Net.Dns]::GetHostAddresses($HostName)
        return [pscustomobject]@{ host = $HostName; resolved = ($addresses.Count -gt 0); address_count = $addresses.Count }
    } catch {
        return [pscustomobject]@{ host = $HostName; resolved = $false; address_count = 0; error = $_.Exception.GetType().Name }
    }
}

function Get-SafeProxyServer {
    param([string] $Raw)
    if ([string]::IsNullOrWhiteSpace($Raw)) { return $null }
    return ($Raw -replace '(?i)(://)[^/@;]+@', '$1***@')
}

function Get-InstalledTransportClients {
    $pattern = '(?i)(amnezia|wireguard|openvpn|hiddify|clash|v2ray|xray|sing-box|singbox|outline|tailscale|zerotier|proton vpn|mullvad|windscribe)'
    $found = @{}

    $uninstallRoots = @(
        'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
        'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
        'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*'
    )
    foreach ($root in $uninstallRoots) {
        try {
            foreach ($item in Get-ItemProperty $root -ErrorAction SilentlyContinue) {
                $name = [string]$item.DisplayName
                if ($name -and $name -match $pattern) {
                    $key = $name.ToLowerInvariant()
                    if (-not $found.ContainsKey($key)) {
                        $found[$key] = [pscustomobject]@{
                            name = $name
                            evidence = 'WINDOWS_UNINSTALL_REGISTRY'
                            active_process = $false
                        }
                    }
                }
            }
        } catch { }
    }

    try {
        foreach ($process in Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match $pattern }) {
            $name = [string]$process.ProcessName
            $key = $name.ToLowerInvariant()
            if ($found.ContainsKey($key)) {
                $found[$key].active_process = $true
            } else {
                $found[$key] = [pscustomobject]@{
                    name = $name
                    evidence = 'RUNNING_PROCESS'
                    active_process = $true
                }
            }
        }
    } catch { }

    $commands = @('wireguard','openvpn','hiddify','clash-verge','clash','v2rayN','v2ray','xray','sing-box','tailscale','zerotier-cli')
    foreach ($commandName in $commands) {
        try {
            $command = Get-Command $commandName -ErrorAction SilentlyContinue
            if ($command) {
                $key = $commandName.ToLowerInvariant()
                if (-not $found.ContainsKey($key)) {
                    $found[$key] = [pscustomobject]@{
                        name = $commandName
                        evidence = 'COMMAND_ON_PATH'
                        active_process = $false
                    }
                }
            }
        } catch { }
    }

    return @($found.Values | Sort-Object name)
}

$dns = @(
    Get-DnsStatus -HostName 'telegram.org'
    Get-DnsStatus -HostName 'web.telegram.org'
)

$directTargets = @(
    @{ host = 'telegram.org'; port = 443 },
    @{ host = 'web.telegram.org'; port = 443 },
    @{ host = '149.154.167.50'; port = 443 },
    @{ host = '149.154.167.91'; port = 443 },
    @{ host = '149.154.175.100'; port = 443 },
    @{ host = '91.108.56.130'; port = 443 },
    @{ host = 'telegram.org'; port = 80 },
    @{ host = 'telegram.org'; port = 5222 }
)
$tcp = foreach ($target in $directTargets) {
    Test-TcpEndpoint -HostName $target.host -Port ([int]$target.port) -TimeoutMs $TimeoutMilliseconds
}
$directReachable = [bool]($tcp | Where-Object { $_.reachable } | Select-Object -First 1)

$proxyHost = [Environment]::GetEnvironmentVariable('TELEGRAM_SOCKS5_HOST', 'Process')
$proxyPortRaw = [Environment]::GetEnvironmentVariable('TELEGRAM_SOCKS5_PORT', 'Process')
$explicitProxy = $null
if (-not [string]::IsNullOrWhiteSpace($proxyHost) -and -not [string]::IsNullOrWhiteSpace($proxyPortRaw)) {
    $proxyPort = 0
    if ([int]::TryParse($proxyPortRaw, [ref]$proxyPort) -and $proxyPort -gt 0 -and $proxyPort -le 65535) {
        $probe = Test-TcpEndpoint -HostName $proxyHost.Trim() -Port $proxyPort -TimeoutMs $TimeoutMilliseconds
        $explicitProxy = [pscustomobject]@{
            configured = $true
            host = $proxyHost.Trim()
            port = $proxyPort
            tcp_reachable = [bool]$probe.reachable
        }
    } else {
        $explicitProxy = [pscustomobject]@{ configured = $true; host = $proxyHost.Trim(); port = $null; tcp_reachable = $false; error = 'INVALID_PORT' }
    }
} else {
    $explicitProxy = [pscustomobject]@{ configured = $false; host = $null; port = $null; tcp_reachable = $false }
}

$commonProxyPorts = @(1080, 10808, 2080, 7890, 7891, 9050, 10809, 10080)
$localProxyCandidates = @()
try {
    $listeners = Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object { $commonProxyPorts -contains $_.LocalPort }
    foreach ($listener in $listeners | Sort-Object LocalPort -Unique) {
        $processName = $null
        try { $processName = (Get-Process -Id $listener.OwningProcess -ErrorAction Stop).ProcessName } catch { }
        $localProxyCandidates += [pscustomobject]@{
            port = [int]$listener.LocalPort
            process = $processName
            protocol = 'UNKNOWN_UNTIL_CONFIGURED'
        }
    }
} catch { }

$tunnelAdapters = @()
try {
    $pattern = '(?i)(wireguard|wintun|amnezia|openvpn|tap|tun|tailscale|zerotier|vpn|sing-box|hiddify|clash|v2ray|xray)'
    foreach ($adapter in Get-NetAdapter -ErrorAction Stop | Where-Object { $_.Status -eq 'Up' -and (($_.Name -match $pattern) -or ($_.InterfaceDescription -match $pattern)) }) {
        $tunnelAdapters += [pscustomobject]@{
            name = $adapter.Name
            interface_description = $adapter.InterfaceDescription
            status = $adapter.Status
        }
    }
} catch { }

$installedTransportClients = @(Get-InstalledTransportClients)

$winHttpText = $null
try {
    $raw = (& netsh winhttp show proxy 2>$null | Out-String).Trim()
    if ($raw) { $winHttpText = ($raw -replace '(?i)(://)[^/@\s]+@', '$1***@') }
} catch { }

$userProxyEnabled = $false
$userProxyServer = $null
try {
    $internetSettings = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -ErrorAction Stop
    $userProxyEnabled = [bool]$internetSettings.ProxyEnable
    $userProxyServer = Get-SafeProxyServer -Raw ([string]$internetSettings.ProxyServer)
} catch { }

if ($directReachable) {
    $routeState = 'DIRECT_REACHABLE'
    $exitCode = 0
} elseif ($explicitProxy.configured -and $explicitProxy.tcp_reachable) {
    $routeState = 'SOCKS5_EXPLICIT_REACHABLE'
    $exitCode = 0
} elseif ($localProxyCandidates.Count -gt 0) {
    $routeState = 'LOCAL_PROXY_CANDIDATE_REQUIRES_EXPLICIT_CONFIG'
    $exitCode = 4
} elseif ($tunnelAdapters.Count -gt 0) {
    $routeState = 'TUNNEL_ADAPTER_PRESENT_BUT_TELEGRAM_UNREACHABLE'
    $exitCode = 4
} elseif ($installedTransportClients.Count -gt 0) {
    $routeState = 'TRANSPORT_CLIENT_INSTALLED_NOT_ACTIVE'
    $exitCode = 4
} else {
    $routeState = 'DIRECT_BLOCKED_NO_APPROVED_ALTERNATE_ROUTE'
    $exitCode = 4
}

$report = [ordered]@{
    record_type = 'TELEGRAM_WINDOWS_NETWORK_PATH_DIAGNOSTIC'
    schema_version = '1.1'
    observed_at = [DateTimeOffset]::UtcNow.ToString('o')
    route_state = $routeState
    direct_reachable = $directReachable
    dns = $dns
    tcp = $tcp
    explicit_socks5 = $explicitProxy
    local_proxy_candidates = $localProxyCandidates
    tunnel_adapters = $tunnelAdapters
    installed_transport_clients = $installedTransportClients
    windows_user_proxy = [ordered]@{
        enabled = $userProxyEnabled
        server = $userProxyServer
    }
    winhttp_proxy = $winHttpText
    policy = [ordered]@{
        auto_use_unknown_proxy = $false
        auto_change_windows_routes = $false
        auto_enable_vpn = $false
        auto_launch_transport_client = $false
        secrets_in_report = $false
    }
}

$absoluteReport = if ([IO.Path]::IsPathRooted($ReportPath)) { $ReportPath } else { Join-Path $RepoRoot $ReportPath }
$reportDir = Split-Path -Parent $absoluteReport
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
[IO.File]::WriteAllText($absoluteReport, (($report | ConvertTo-Json -Depth 8) + [Environment]::NewLine), [Text.UTF8Encoding]::new($false))

Write-Host '============================================================'
Write-Host 'FATHER Telegram network path preflight'
Write-Host '============================================================'
Write-Host "Route state: $routeState"
Write-Host "Direct Telegram TCP: $(if ($directReachable) { 'PASS' } else { 'FAIL' })"
Write-Host "Explicit SOCKS5 configured: $($explicitProxy.configured)"
if ($explicitProxy.configured) { Write-Host "Explicit SOCKS5 TCP reachable: $($explicitProxy.tcp_reachable)" }
if ($localProxyCandidates.Count -gt 0) {
    Write-Host ('Local proxy-like listeners: ' + (($localProxyCandidates | ForEach-Object { "$($_.port)/$($_.process)" }) -join ', '))
}
if ($tunnelAdapters.Count -gt 0) {
    Write-Host ('Tunnel-like adapters UP: ' + (($tunnelAdapters | ForEach-Object { $_.name }) -join ', '))
}
if ($installedTransportClients.Count -gt 0) {
    Write-Host ('Installed transport clients: ' + (($installedTransportClients | ForEach-Object { $_.name }) -join ', '))
}
Write-Host "Report: $ReportPath"

if ($routeState -eq 'LOCAL_PROXY_CANDIDATE_REQUIRES_EXPLICIT_CONFIG') {
    Write-Host 'A local listener may be a proxy, but FATHER will not guess its protocol.'
    Write-Host 'After confirming a SOCKS5 port locally, set TELEGRAM_SOCKS5_HOST and TELEGRAM_SOCKS5_PORT in this shell and rerun.'
} elseif ($routeState -eq 'TRANSPORT_CLIENT_INSTALLED_NOT_ACTIVE') {
    Write-Host 'A VPN/proxy client appears installed but no usable Telegram route is active.'
    Write-Host 'Start an approved client in system/full-tunnel mode, then rerun this diagnostic.'
} elseif ($routeState -eq 'DIRECT_BLOCKED_NO_APPROVED_ALTERNATE_ROUTE') {
    Write-Host 'No reachable direct Telegram path was observed.'
    Write-Host 'Enable an approved system tunnel/VPN or configure an explicit SOCKS5 route, then rerun.'
}

exit $exitCode
