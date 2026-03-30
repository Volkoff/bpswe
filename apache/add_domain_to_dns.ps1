$hostsPath = "C:\Windows\System32\drivers\etc\hosts"

$entries = @(
    "127.0.0.1   www.mojefirma.cz"
    "127.0.0.1   eshop.mojefirma.cz"
    "127.0.0.1   blog.mojefirma.cz"
    "127.0.0.1   admin.mojefirma.cz"
    "127.0.0.1   ftp.mojefirma.cz"
    )

$hostsContent = Get-Content $hostsPath

foreach ($entry in $entries) {
    if ($hostsContent -notcontains $entry) {
        Add-Content -Path $hostsPath -Value $entry
        Write-Host "Přidáno: $entry"
    } else {
        Write-Host "Už existuje: $entry"
    }
}

Write-Host "Hotovo."
